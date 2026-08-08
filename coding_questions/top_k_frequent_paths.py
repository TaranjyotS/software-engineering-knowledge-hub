'''Top-K Frequent Paths: Batch, Heap-Optimized, Dynamic-K, and Streaming Variants

Given a sequence of path strings representing observed process routes, return the k most frequently occurring unique paths.
This is a reusable top-k frequency problem. If frequencies tie, this implementation returns the lexicographically smaller path first so
results are deterministic. In an interview, clarify the required tie-breaking rule if it is not specified.

Requirements:
1. Count how often each unique path appears.
2. Return at most k paths ordered by frequency descending and path ascending for ties.
3. Support a straightforward full-sort solution.
4. Support an optimized fixed-k solution for the case where the number of unique paths u is much larger than k.
5. Show how the design changes when k varies between queries or when events arrive as a stream.

Key observations:
- Counting all n events costs O(n) and O(u) space, where u is the number of unique paths.
- Sorting every unique path costs O(u log u), giving O(n + u log u) total time.
- When k << u, a min-heap of size k reduces selection to O(u log k), giving O(n + u log k).
- For k = 1, a single max scan after counting is enough; a heap is unnecessary.
- A fixed-size heap discards candidates, so it cannot later answer an arbitrary larger k without revisiting the frequency map.
- For a static dataset with many changing-k queries, sort once and return prefixes.
- For an exact stream with arbitrary k, keep running counts and compute a size-k heap at query time. This keeps updates O(1) average and
  supports any requested k, at the cost of O(u log k) per query.

Complexity:
- Full sort: O(n + u log u) time, O(u) frequency space plus the sorted result.
- Fixed-k heap: O(n + u log k) time, O(u + k) space.
- Streaming tracker update: O(1) average per event; query: O(u log k); stored state: O(u).
- If u itself cannot fit in memory, exact frequencies are impossible without external storage or partitioning. Approximate heavy-hitter
  structures such as Count-Min Sketch plus a candidate set can trade exactness for bounded memory.

Important edge cases:
- k <= 0.
- Empty input.
- k is greater than the number of unique paths.
- All paths have the same frequency.
- k = 1.
- Very high-cardinality input with a small k.
- Dynamic k where a previously discarded candidate may become part of a larger requested result.
- Streaming queries that require an explicit window definition if "recent" rather than all-time frequency is desired.
'''

from __future__ import annotations

import heapq
from dataclasses import dataclass
from typing import Iterable


def _count_paths(paths: Iterable[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for path in paths:
        counts[path] = counts.get(path, 0) + 1
    return counts


def top_k_by_sort(paths: Iterable[str], k: int) -> list[str]:
    """Simple batch solution: count all paths and sort all unique paths."""
    if k <= 0:
        return []

    counts = _count_paths(paths)
    ranked = sorted(counts, key=lambda path: (-counts[path], path))
    return ranked[:k]


@dataclass(frozen=True)
class _Candidate:
    """Heap item where the weakest retained candidate compares smallest."""

    frequency: int
    path: str

    def __lt__(self, other: "_Candidate") -> bool:
        if self.frequency != other.frequency:
            return self.frequency < other.frequency
        # For equal frequency, lexicographically larger is the weaker result,
        # so reverse the normal string comparison inside the min-heap.
        return self.path > other.path


def _is_better(candidate: _Candidate, weakest: _Candidate) -> bool:
    return (
        candidate.frequency > weakest.frequency
        or (
            candidate.frequency == weakest.frequency
            and candidate.path < weakest.path
        )
    )


def _top_k_from_counts(counts: dict[str, int], k: int) -> list[str]:
    if k <= 0 or not counts:
        return []

    heap: list[_Candidate] = []

    for path, frequency in counts.items():
        candidate = _Candidate(frequency=frequency, path=path)

        if len(heap) < k:
            heapq.heappush(heap, candidate)
            continue

        if _is_better(candidate, heap[0]):
            heapq.heapreplace(heap, candidate)

    return [
        candidate.path
        for candidate in sorted(
            heap,
            key=lambda item: (-item.frequency, item.path),
        )
    ]


def top_k_by_heap(paths: Iterable[str], k: int) -> list[str]:
    """Optimized one-shot solution for small k relative to unique cardinality."""
    return _top_k_from_counts(_count_paths(paths), k)


def most_frequent_path(paths: Iterable[str]) -> str | None:
    """Specialized k=1 solution without a heap."""
    counts = _count_paths(paths)
    if not counts:
        return None

    return min(
        counts,
        key=lambda path: (-counts[path], path),
    )


class StreamingTopK:
    """Exact all-time stream counts with arbitrary top-k queries."""

    def __init__(self) -> None:
        self.counts: dict[str, int] = {}

    def add(self, path: str) -> None:
        self.counts[path] = self.counts.get(path, 0) + 1

    def extend(self, paths: Iterable[str]) -> None:
        for path in paths:
            self.add(path)

    def top_k(self, k: int) -> list[str]:
        return _top_k_from_counts(self.counts, k)


def run_sample_tests() -> None:
    paths = [
        "receive>scan>pack",
        "receive>scan>pack",
        "receive>inspect>pack",
        "receive>scan>pack",
        "receive>inspect>pack",
        "receive>reroute>pack",
        "receive>manual>pack",
    ]

    expected = ["receive>scan>pack", "receive>inspect>pack"]
    assert top_k_by_sort(paths, 2) == expected
    assert top_k_by_heap(paths, 2) == expected
    assert most_frequent_path(paths) == "receive>scan>pack"

    tied = ["c", "b", "a"]
    assert top_k_by_heap(tied, 2) == ["a", "b"]
    assert top_k_by_sort(tied, 5) == ["a", "b", "c"]
    assert top_k_by_heap(tied, 0) == []

    tracker = StreamingTopK()
    tracker.extend(["b", "a", "b", "c", "a", "b"])
    assert tracker.top_k(1) == ["b"]
    assert tracker.top_k(2) == ["b", "a"]
    assert tracker.top_k(10) == ["b", "a", "c"]

    tracker.add("c")
    tracker.add("c")
    assert tracker.top_k(2) == ["b", "c"]

    print("All top-k frequent path sample tests passed.")


if __name__ == "__main__":
    run_sample_tests()


'''
Alternative approaches and follow-ups:
1. Tiny fixed k:
   Keep a sorted list of at most k candidates. Updating it costs O(k) per unique path, which is effectively linear in u when k is a
   tiny constant, but a heap generalizes better as k grows.
2. Dynamic k over a static dataset:
   Count once, sort all u unique paths once in O(u log u), cache the ranking, and answer each top-k query by slicing the first k entries.
   A previous size-k heap is insufficient if a later query asks for a larger k because discarded candidates are gone.
3. Exact streaming with frequent queries:
   Running counts are the minimum exact state. If O(u log k) per query is too expensive, maintain a secondary ordered index keyed by
   frequency and path, updating an item's old rank and new rank on each event. A balanced tree or specialized indexed heap can make
   updates O(log u) and top-k reads close to O(k), at the cost of more implementation complexity.
4. Distributed stream:
   Partition events by a stable hash of path, aggregate local counts, periodically merge candidates or counts, checkpoint consumer
   offsets/state, and make replay idempotent. Define whether ranking is all-time, tumbling-window, sliding-window, or session-based.
5. Memory-bounded approximation:
   Use Count-Min Sketch to estimate frequencies and a small candidate structure for likely heavy hitters. This reduces memory but can
   overestimate counts and requires a clearly stated accuracy trade-off.

Explanation:
- heapq is useful because a size-k min-heap keeps the current weakest selected candidate at the root. Each new unique candidate can be
  ignored or replace that root in O(log k), avoiding a full O(u log u) sort when only a small top-k prefix is needed.
- The frequency dictionary is still required for exact batch counting. The heap optimizes the selection phase, not the counting phase.
- Complexity should distinguish n total events, u unique paths, and k requested results because these can differ by orders of magnitude.

Summary:
- Baseline: O(n + u log u).
- Small fixed k: O(n + u log k).
- k = 1: O(n + u) after counting.
- Dynamic k over static data: sort once, slice many times.
- Streaming arbitrary k: keep exact running counts; choose query-time heap or a more complex ordered index based on query frequency.
'''
