"""Expiring Window Map with O(1)-Average Lookup

Design an in-memory key/value structure with a fixed time window. Each put(key, value) makes that value live for window_seconds from the
write time. The structure supports:

- put(key, value): insert or overwrite a key.
- get(key): return the live value or None if absent/expired.
- average(): return the average of all currently live values, or None when empty.

The key interview requirements are:
- Avoid scanning the whole map to remove expired entries on every operation.
- Keep average() O(1) after lazy cleanup by maintaining a running sum.
- Handle overwrites correctly: an old queued expiration record for a key must not delete/subtract the newer value.
- Explain why deque.popleft() is O(1) while list.pop(0) is O(n).
- Discuss how to add thread safety and what invariant the lock protects.

Data structures:
- data: key -> (value, expiry, version)
- expirations: deque[(expiry, key, version)] ordered by fixed-TTL expiration time
- running_sum: sum of current live values

Why a version/timestamp is needed:
put('a', 10) at t=0 creates an expiry record for t=5.
put('a', 20) at t=2 creates a newer expiry record for t=7.
At t=5 the first deque record is stale; blindly deleting key 'a' would remove the new value and subtract the wrong number. Cleanup therefore
compares queued version with current version before acting.

Complexity (amortized):
- put: O(1)
- get: O(1)
- average: O(1)
- space: O(n + stale queued overwrite records that have not reached expiry yet)
Each expiration record is appended once and popped once, so lazy cleanup is amortized O(1) across operations.
"""

from __future__ import annotations

import threading
import time
from collections import deque
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

K = TypeVar("K")


@dataclass(frozen=True)
class _Entry:
    value: float
    expiry: float
    version: int


class ExpiringWindowMap(Generic[K]):
    def __init__(
        self,
        window_seconds: float,
        *,
        clock: Callable[[], float] = time.monotonic,
        thread_safe: bool = False,
    ) -> None:
        if window_seconds <= 0:
            raise ValueError("window_seconds must be positive")

        self.window_seconds = window_seconds
        self._clock = clock
        self._data: dict[K, _Entry] = {}
        self._expirations: deque[tuple[float, K, int]] = deque()
        self._running_sum = 0.0
        self._version = 0
        self._lock = threading.RLock() if thread_safe else _NoOpLock()

    def _cleanup_locked(self, now: float) -> None:
        while self._expirations and self._expirations[0][0] <= now:
            _, key, queued_version = self._expirations.popleft()
            current = self._data.get(key)

            if current is None or current.version != queued_version:
                continue

            self._running_sum -= current.value
            del self._data[key]

    def put(self, key: K, value: float) -> None:
        now = self._clock()
        expiry = now + self.window_seconds

        with self._lock:
            self._cleanup_locked(now)

            previous = self._data.get(key)
            if previous is not None:
                self._running_sum -= previous.value

            self._version += 1
            version = self._version
            entry = _Entry(float(value), expiry, version)

            self._data[key] = entry
            self._running_sum += entry.value
            self._expirations.append((expiry, key, version))

    def get(self, key: K) -> float | None:
        now = self._clock()

        with self._lock:
            self._cleanup_locked(now)
            entry = self._data.get(key)
            return None if entry is None else entry.value

    def average(self) -> float | None:
        now = self._clock()

        with self._lock:
            self._cleanup_locked(now)
            if not self._data:
                return None
            return self._running_sum / len(self._data)

    def size(self) -> int:
        now = self._clock()
        with self._lock:
            self._cleanup_locked(now)
            return len(self._data)


class _NoOpLock:
    def __enter__(self) -> "_NoOpLock":
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        return False


class _FakeClock:
    def __init__(self, value: float = 0.0) -> None:
        self.value = value

    def __call__(self) -> float:
        return self.value

    def advance(self, seconds: float) -> None:
        self.value += seconds


def run_sample_tests() -> None:
    clock = _FakeClock()
    values: ExpiringWindowMap[str] = ExpiringWindowMap(10, clock=clock)

    assert values.average() is None

    values.put("a", 10)
    values.put("b", 30)
    assert values.get("a") == 10
    assert values.average() == 20

    clock.advance(5)
    values.put("a", 50)  # overwrite a; old expiration at t=10 becomes stale
    assert values.average() == 40

    clock.advance(5)  # t=10: old a record and b expire; newer a survives
    assert values.get("a") == 50
    assert values.get("b") is None
    assert values.average() == 50
    assert values.size() == 1

    clock.advance(5)  # t=15: newer a expires
    assert values.get("a") is None
    assert values.average() is None

    # Optional thread-safe mode protects data + expiration queue + running sum as
    # one logical invariant.
    concurrent: ExpiringWindowMap[int] = ExpiringWindowMap(
        100,
        thread_safe=True,
    )

    def writer(start: int) -> None:
        for offset in range(100):
            concurrent.put(start + offset, float(offset))

    threads = [threading.Thread(target=writer, args=(n * 1000,)) for n in range(4)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert concurrent.size() == 400
    assert concurrent.average() == 49.5

    print("All expiring window map sample tests passed.")


if __name__ == "__main__":
    run_sample_tests()


"""
Interview follow-ups:

1. Why not compute average by summing the map every time?
   That makes average O(n). Maintaining running_sum makes the query O(1) after amortized cleanup.

2. Why deque rather than list?
   Fixed TTL means queued expirations are chronological. deque.append/popleft are O(1); list.pop(0) shifts remaining elements and is O(n).

3. Why not a heap?
   With one fixed TTL, insertion order equals expiry order, so a deque is simpler and faster. If each key has an arbitrary TTL, use a min-heap
   ordered by expiry and accept O(log n) push/pop.

4. Could cleanup run in a background thread instead of lazily?
   Yes. Lazy cleanup keeps the structure simple and only pays work during operations. A background sweeper can reduce stale memory when the map
   remains idle, but introduces lifecycle/concurrency complexity. A hybrid is also possible.

5. How do you make it thread-safe?
   The protected invariant spans _data, _expirations, and _running_sum. Start with one lock around cleanup + each logical operation. Only split
   locks after profiling demonstrates contention, because cross-structure consistency matters more than theoretical concurrency.

6. What if multiple processes or machines need the same map?
   In-process locks are insufficient. Move authoritative state to a shared store with atomic operations or partition ownership by key; define
   time/expiry semantics and idempotency explicitly.
"""
