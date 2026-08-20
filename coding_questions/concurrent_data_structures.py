"""Concurrent Data Structures: LRU, TTL Map, Blocking Queue, and Rate Limiter

This file contains runnable interview-style implementations that naturally support senior follow-ups such as:
- make the structure thread-safe,
- explain the protected invariant,
- discuss coarse vs fine-grained locking,
- change fixed TTL to arbitrary TTL,
- add backpressure,
- reduce contention,
- extend the design across multiple processes/machines.

Problems covered:
1. ThreadSafeLRUCache
   Hash map + doubly linked list gives O(1) lookup, promotion, and eviction. Both get() and put() mutate recency ordering, so one lock protects
   the dictionary/list invariant in the baseline design.
2. ExpiringMap
   Fixed TTL means expirations occur in insertion order, so a deque supports amortized O(1) cleanup. Overwrites leave stale expiration
   metadata, so cleanup validates the queued expiry against the map's current expiry before deleting.
3. BoundedBlockingQueue
   deque + one lock + not_empty/not_full conditions. Producers block while full and consumers block while empty, demonstrating backpressure.
4. FixedWindowRateLimiter
   Per-key counters with a lock. This is intentionally simple and exposes the fixed-window boundary-burst follow-up; token bucket or sliding
   window is a natural next design.

Important interview principle:
Start with the simplest synchronization that proves correctness. If profiling shows contention, discuss sharding/partitioning the state or
reducing critical-section work rather than prematurely creating complex lock graphs.
"""

from __future__ import annotations

import threading
import time
from collections import deque
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

K = TypeVar("K")
V = TypeVar("V")
T = TypeVar("T")


@dataclass
class _LRUNode(Generic[K, V]):
    key: K | None = None
    value: V | None = None
    prev: "_LRUNode[K, V] | None" = None
    next: "_LRUNode[K, V] | None" = None


class ThreadSafeLRUCache(Generic[K, V]):
    """O(1) get/put LRU cache protected by one coarse-grained lock.

    Invariant:
    - _nodes contains every live data node exactly once.
    - The doubly linked list contains the same live nodes between sentinels.
    - left.next is least-recently used; right.prev is most-recently used.
    """

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")

        self.capacity = capacity
        self._nodes: dict[K, _LRUNode[K, V]] = {}
        self._left: _LRUNode[K, V] = _LRUNode()
        self._right: _LRUNode[K, V] = _LRUNode()
        self._left.next = self._right
        self._right.prev = self._left
        self._lock = threading.Lock()

    def _remove(self, node: _LRUNode[K, V]) -> None:
        previous = node.prev
        following = node.next
        assert previous is not None and following is not None
        previous.next = following
        following.prev = previous

    def _add_recent(self, node: _LRUNode[K, V]) -> None:
        previous = self._right.prev
        assert previous is not None
        previous.next = node
        node.prev = previous
        node.next = self._right
        self._right.prev = node

    def get(self, key: K) -> V | None:
        # get() mutates recency, so it participates in synchronization.
        with self._lock:
            node = self._nodes.get(key)
            if node is None:
                return None

            self._remove(node)
            self._add_recent(node)
            return node.value

    def put(self, key: K, value: V) -> None:
        with self._lock:
            existing = self._nodes.get(key)

            if existing is not None:
                existing.value = value
                self._remove(existing)
                self._add_recent(existing)
                return

            node = _LRUNode(key=key, value=value)
            self._nodes[key] = node
            self._add_recent(node)

            if len(self._nodes) <= self.capacity:
                return

            lru = self._left.next
            assert lru is not None and lru is not self._right
            self._remove(lru)
            assert lru.key is not None
            del self._nodes[lru.key]

    def snapshot_lru_to_mru(self) -> list[tuple[K, V]]:
        """Return a test/debug snapshot while holding the same invariant lock."""
        with self._lock:
            result: list[tuple[K, V]] = []
            node = self._left.next

            while node is not None and node is not self._right:
                assert node.key is not None
                result.append((node.key, node.value))  # type: ignore[arg-type]
                node = node.next

            return result


class ExpiringMap(Generic[K, V]):
    """Fixed-TTL map with lazy cleanup using a deque ordered by expiration time.

    put/get are protected by one lock because cleanup and map mutation must remain atomic relative to one another.
    A fake clock can be injected for deterministic tests.
    """

    def __init__(
        self,
        ttl_seconds: float,
        *,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        if ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be positive")

        self.ttl_seconds = ttl_seconds
        self._clock = clock
        self._data: dict[K, tuple[V, float]] = {}
        self._expirations: deque[tuple[float, K]] = deque()
        self._lock = threading.Lock()

    def _cleanup_locked(self, now: float) -> None:
        while self._expirations and self._expirations[0][0] <= now:
            queued_expiry, key = self._expirations.popleft()
            current = self._data.get(key)

            if current is None:
                continue

            _, current_expiry = current

            # Overwriting a key leaves an old queue entry behind. Delete only if
            # this metadata still describes the current map value.
            if current_expiry == queued_expiry:
                del self._data[key]

    def put(self, key: K, value: V) -> None:
        now = self._clock()
        expiry = now + self.ttl_seconds

        with self._lock:
            self._cleanup_locked(now)
            self._data[key] = (value, expiry)
            self._expirations.append((expiry, key))

    def get(self, key: K) -> V | None:
        now = self._clock()

        with self._lock:
            self._cleanup_locked(now)
            current = self._data.get(key)
            if current is None:
                return None
            return current[0]

    def __len__(self) -> int:
        now = self._clock()
        with self._lock:
            self._cleanup_locked(now)
            return len(self._data)


class BoundedBlockingQueue(Generic[T]):
    """Blocking FIFO queue implemented with conditions.

    - put waits while full.
    - take waits while empty.
    - while loops re-check predicates after wakeup.
    - deque gives O(1) append and popleft.
    """

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")

        self.capacity = capacity
        self._queue: deque[T] = deque()
        self._lock = threading.Lock()
        self._not_empty = threading.Condition(self._lock)
        self._not_full = threading.Condition(self._lock)

    def put(self, item: T) -> None:
        with self._not_full:
            while len(self._queue) >= self.capacity:
                self._not_full.wait()

            self._queue.append(item)
            self._not_empty.notify()

    def take(self) -> T:
        with self._not_empty:
            while not self._queue:
                self._not_empty.wait()

            item = self._queue.popleft()
            self._not_full.notify()
            return item

    def qsize(self) -> int:
        with self._lock:
            return len(self._queue)


class FixedWindowRateLimiter(Generic[K]):
    """Thread-safe fixed-window limiter.

    allow(key, now) is O(1) expected and stores O(number_of_active_keys) state.
    This deliberately exposes the fixed-window boundary-burst trade-off for discussion.
    """

    def __init__(self, limit: int, window_seconds: float) -> None:
        if limit <= 0 or window_seconds <= 0:
            raise ValueError("limit and window_seconds must be positive")

        self.limit = limit
        self.window_seconds = window_seconds
        self._state: dict[K, tuple[int, int]] = {}
        self._lock = threading.Lock()

    def allow(self, key: K, now: float) -> bool:
        window_id = int(now // self.window_seconds)

        with self._lock:
            stored_window, count = self._state.get(key, (window_id, 0))

            if stored_window != window_id:
                stored_window = window_id
                count = 0

            if count >= self.limit:
                self._state[key] = (stored_window, count)
                return False

            self._state[key] = (stored_window, count + 1)
            return True


class _FakeClock:
    def __init__(self, value: float = 0.0) -> None:
        self.value = value

    def __call__(self) -> float:
        return self.value

    def advance(self, seconds: float) -> None:
        self.value += seconds


def _test_lru() -> None:
    cache: ThreadSafeLRUCache[str, int] = ThreadSafeLRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    assert cache.get("a") == 1  # a becomes MRU
    cache.put("c", 3)  # b should be evicted
    assert cache.get("b") is None
    assert cache.get("c") == 3
    assert cache.snapshot_lru_to_mru() == [("a", 1), ("c", 3)]

    # Multiple threads repeatedly mutate the same logical structure. The test
    # asserts structural capacity/integrity rather than relying on a race to fail.
    def writer(prefix: str) -> None:
        for index in range(200):
            cache.put(f"{prefix}-{index}", index)
            cache.get(f"{prefix}-{index}")

    threads = [threading.Thread(target=writer, args=(f"t{n}",)) for n in range(4)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    snapshot = cache.snapshot_lru_to_mru()
    assert len(snapshot) <= 2
    assert len({key for key, _ in snapshot}) == len(snapshot)


def _test_expiring_map() -> None:
    clock = _FakeClock()
    cache: ExpiringMap[str, int] = ExpiringMap(10, clock=clock)

    cache.put("a", 1)  # expires at 10
    clock.advance(5)
    cache.put("a", 2)  # expires at 15; old metadata remains in deque

    clock.advance(5)  # time 10
    assert cache.get("a") == 2  # stale expiry 10 must not delete newer value

    clock.advance(5)  # time 15
    assert cache.get("a") is None
    assert len(cache) == 0


def _test_blocking_queue() -> None:
    queue: BoundedBlockingQueue[int] = BoundedBlockingQueue(3)
    produced = list(range(50))
    consumed: list[int] = []

    def producer() -> None:
        for item in produced:
            queue.put(item)

    def consumer() -> None:
        for _ in produced:
            consumed.append(queue.take())

    producer_thread = threading.Thread(target=producer)
    consumer_thread = threading.Thread(target=consumer)

    producer_thread.start()
    consumer_thread.start()
    producer_thread.join(timeout=5)
    consumer_thread.join(timeout=5)

    assert not producer_thread.is_alive()
    assert not consumer_thread.is_alive()
    assert consumed == produced
    assert queue.qsize() == 0


def _test_fixed_window_rate_limiter() -> None:
    limiter: FixedWindowRateLimiter[str] = FixedWindowRateLimiter(
        limit=3,
        window_seconds=60,
    )

    assert limiter.allow("user-1", 0)
    assert limiter.allow("user-1", 10)
    assert limiter.allow("user-1", 20)
    assert not limiter.allow("user-1", 30)

    # New time bucket resets the count.
    assert limiter.allow("user-1", 60)

    # Independent keys have independent state.
    assert limiter.allow("user-2", 30)


def run_sample_tests() -> None:
    _test_lru()
    _test_expiring_map()
    _test_blocking_queue()
    _test_fixed_window_rate_limiter()
    print("All concurrent data structure sample tests passed.")


if __name__ == "__main__":
    run_sample_tests()


"""
Interview follow-ups:

ThreadSafeLRUCache
- Why is get() a write operation logically?
- Why start with one lock instead of one lock per key?
- How would you reduce contention? One option is sharding independent cache partitions, but exact global LRU ordering becomes harder.
- How would you make the cache distributed? A local in-process LRU and a distributed cache solve different problems; exact global recency across
  nodes is substantially more complex.

ExpiringMap
- Why does fixed TTL permit a deque? Because insertion order and expiry order match.
- What changes if every put supplies a different TTL? Use a min-heap ordered by expiry; push/pop become O(log n).
- Why compare queued expiry to current expiry? An overwrite leaves stale secondary-index metadata that must not delete the newer value.
- Would you clean up only on reads/writes or run a background sweeper? Lazy cleanup is simple; a sweeper can bound stale memory during idle periods.

BoundedBlockingQueue
- Why while instead of if around Condition.wait()? Spurious wakeups and state changes before lock reacquisition require re-checking the predicate.
- What does bounded capacity provide? Backpressure; producers cannot allocate unbounded memory when consumers are slow.
- Why not implement this in production instead of queue.Queue? Prefer the standard tested primitive unless the interview specifically asks for implementation.

FixedWindowRateLimiter
- What is the boundary-burst problem? Requests at the end and start of adjacent windows can create a much larger short-term burst.
- Alternatives: sliding-window log/counter or token bucket.
- How do you reduce lock contention? Partition locks/state by key.
- How do you enforce one global limit across many API servers? Use an atomic shared/partitioned store or allocate approximate local token budgets from
  a global quota; local process counters alone are not globally correct.
"""
