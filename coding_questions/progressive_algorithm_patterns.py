'''Progressive Algorithm Interview Patterns

This file collects reusable coding-interview problems where the strongest discussion is not only the final implementation, but the
progression from a simple correct solution to a better one. Each function is intentionally small enough to explain in a 45–60 minute
interview, with the main invariant and complexity documented below.

Problems covered:
1. Two Sum — brute-force pair search -> expected O(n) hash-map lookup.
2. Longest substring without repeating characters — repeated scans -> O(n) sliding window.
3. Top-k frequent values — full sort -> size-k heap.
4. Merge intervals — pairwise overlap reasoning -> sort + linear scan.
5. Subarray sum equals k — O(n^2) enumeration -> O(n) prefix-frequency map.
6. Product except self — O(n^2) repeated multiplication -> O(n) prefix/suffix products.
7. Kth largest — sort -> size-k min-heap.
8. Minimum meeting rooms — sorted intervals + min-heap of active end times.
9. Number of islands — grid connected-component DFS/BFS.
10. Course schedule — directed-cycle detection using Kahn topological sort.
11. K-way merge — merge multiple newest-first streams and stop after the requested limit.

Interview pattern:
- State the simplest correct solution first.
- Name its time/space complexity.
- Identify the repeated expensive operation.
- Introduce the data structure that removes that work.
- Recalculate complexity.
- Test normal, empty, duplicate/boundary, and no-solution cases.
'''

from __future__ import annotations

from collections import Counter, defaultdict, deque
from dataclasses import dataclass
import heapq
from typing import Iterable, Sequence


def two_sum(nums: Sequence[int], target: int) -> list[int]:
    '''Return indices of two values whose sum equals target, or [] if absent.

    Expected time O(n), space O(n).
    Invariant: seen[value] stores an index from the already-processed prefix.
    '''
    seen: dict[int, int] = {}

    for index, value in enumerate(nums):
        complement = target - value
        if complement in seen:
            return [seen[complement], index]
        seen[value] = index

    return []


def longest_unique_substring(s: str) -> int:
    '''Return the length of the longest substring with no repeated characters.

    Time O(n), space O(min(n, alphabet_size)).
    Invariant: s[left:right+1] contains no duplicate character.
    '''
    last_seen: dict[str, int] = {}
    left = 0
    best = 0

    for right, char in enumerate(s):
        if char in last_seen and last_seen[char] >= left:
            left = last_seen[char] + 1

        last_seen[char] = right
        best = max(best, right - left + 1)

    return best


def top_k_frequent(nums: Iterable[int], k: int) -> list[int]:
    '''Return up to k most-frequent values, deterministic for frequency ties.

    Count phase O(n). Let u be unique values; selection is O(u log k).
    Space O(u + k).
    '''
    if k <= 0:
        return []

    counts = Counter(nums)
    if not counts:
        return []

    # Python's nsmallest can express the ranking directly, but this exercise keeps
    # an explicit heap to make the size-k selection invariant interview-visible.
    heap: list[tuple[int, int]] = []

    for value, frequency in counts.items():
        item = (frequency, -value)

        if len(heap) < k:
            heapq.heappush(heap, item)
            continue

        if item > heap[0]:
            heapq.heapreplace(heap, item)

    # Stronger candidate: frequency descending; for equal frequency value ascending.
    ranked = sorted(heap, key=lambda item: (-item[0], -item[1]))
    return [-neg_value for _, neg_value in ranked]


def merge_intervals(intervals: Sequence[Sequence[int]]) -> list[list[int]]:
    '''Merge overlapping/touching intervals.

    Time O(n log n) for sorting, O(n) scan; result space O(n) worst case.
    '''
    if not intervals:
        return []

    ordered = sorted((int(start), int(end)) for start, end in intervals)
    merged: list[list[int]] = [[ordered[0][0], ordered[0][1]]]

    for start, end in ordered[1:]:
        last = merged[-1]
        if start <= last[1]:
            last[1] = max(last[1], end)
        else:
            merged.append([start, end])

    return merged


def subarray_sum_equals_k(nums: Iterable[int], k: int) -> int:
    '''Count contiguous subarrays whose sum equals k.

    Time O(n), space O(n).
    If current prefix is P, every earlier prefix P-k starts a matching subarray.
    '''
    prefix_count = {0: 1}
    prefix = 0
    result = 0

    for value in nums:
        prefix += value
        result += prefix_count.get(prefix - k, 0)
        prefix_count[prefix] = prefix_count.get(prefix, 0) + 1

    return result


def product_except_self(nums: Sequence[int]) -> list[int]:
    '''Return product of all other values for each position without division.

    Time O(n). Auxiliary space O(1) excluding the required output array.
    '''
    result = [1] * len(nums)

    prefix = 1
    for index, value in enumerate(nums):
        result[index] = prefix
        prefix *= value

    suffix = 1
    for index in range(len(nums) - 1, -1, -1):
        result[index] *= suffix
        suffix *= nums[index]

    return result


def kth_largest(nums: Iterable[int], k: int) -> int:
    '''Return the kth-largest value using a size-k min-heap.

    Time O(n log k), space O(k).
    '''
    if k <= 0:
        raise ValueError('k must be positive')

    heap: list[int] = []

    for value in nums:
        if len(heap) < k:
            heapq.heappush(heap, value)
        elif value > heap[0]:
            heapq.heapreplace(heap, value)

    if len(heap) < k:
        raise ValueError('k is greater than the number of values')

    return heap[0]


def min_meeting_rooms(intervals: Sequence[Sequence[int]]) -> int:
    '''Return the minimum rooms needed when intervals are [start, end].

    Time O(n log n), space O(n) worst case.
    Heap stores end times of meetings currently occupying rooms.
    '''
    if not intervals:
        return 0

    ordered = sorted((int(start), int(end)) for start, end in intervals)
    active_end_times: list[int] = []
    max_rooms = 0

    for start, end in ordered:
        while active_end_times and active_end_times[0] <= start:
            heapq.heappop(active_end_times)

        heapq.heappush(active_end_times, end)
        max_rooms = max(max_rooms, len(active_end_times))

    return max_rooms


def number_of_islands(grid: Sequence[Sequence[str]]) -> int:
    '''Count 4-directionally connected components of '1' cells without mutating input.

    Time O(rows * cols), space O(rows * cols) worst case.
    '''
    if not grid or not grid[0]:
        return 0

    rows = len(grid)
    cols = len(grid[0])
    visited: set[tuple[int, int]] = set()
    islands = 0

    for row in range(rows):
        for col in range(cols):
            if grid[row][col] != '1' or (row, col) in visited:
                continue

            islands += 1
            stack = [(row, col)]
            visited.add((row, col))

            while stack:
                current_row, current_col = stack.pop()

                for delta_row, delta_col in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    next_row = current_row + delta_row
                    next_col = current_col + delta_col

                    if not (0 <= next_row < rows and 0 <= next_col < cols):
                        continue
                    if grid[next_row][next_col] != '1':
                        continue
                    if (next_row, next_col) in visited:
                        continue

                    visited.add((next_row, next_col))
                    stack.append((next_row, next_col))

    return islands


def can_finish_courses(
    num_courses: int,
    prerequisites: Iterable[tuple[int, int]],
) -> bool:
    '''Return whether a directed prerequisite graph is acyclic using Kahn's algorithm.

    Pair (course, prerequisite) means prerequisite -> course.
    Time O(V + E), space O(V + E).
    '''
    graph: dict[int, list[int]] = defaultdict(list)
    indegree = [0] * num_courses

    for course, prerequisite in prerequisites:
        graph[prerequisite].append(course)
        indegree[course] += 1

    ready = deque(
        course
        for course in range(num_courses)
        if indegree[course] == 0
    )

    completed = 0

    while ready:
        course = ready.popleft()
        completed += 1

        for dependent in graph[course]:
            indegree[dependent] -= 1
            if indegree[dependent] == 0:
                ready.append(dependent)

    return completed == num_courses


@dataclass(frozen=True)
class FeedItem:
    '''Newest-first item used by the k-way merge example.'''

    item_id: str
    source_id: str
    published_at: int


def merge_newest_streams(
    streams: Sequence[Sequence[FeedItem]],
    limit: int,
) -> list[FeedItem]:
    '''Merge individually newest-first streams and return at most limit items.

    Let p be the number of non-empty streams and n the number of returned items.
    Heap size is at most p, so merge work is O(n log p) and O(p) heap space.
    '''
    if limit <= 0:
        return []

    # heap item: (-published_at, item_id, stream_index, item_index)
    # item_id is a deterministic tie-breaker.
    heap: list[tuple[int, str, int, int]] = []

    for stream_index, stream in enumerate(streams):
        if not stream:
            continue
        item = stream[0]
        heapq.heappush(
            heap,
            (-item.published_at, item.item_id, stream_index, 0),
        )

    result: list[FeedItem] = []

    while heap and len(result) < limit:
        _, _, stream_index, item_index = heapq.heappop(heap)
        item = streams[stream_index][item_index]
        result.append(item)

        next_index = item_index + 1
        if next_index < len(streams[stream_index]):
            next_item = streams[stream_index][next_index]
            heapq.heappush(
                heap,
                (
                    -next_item.published_at,
                    next_item.item_id,
                    stream_index,
                    next_index,
                ),
            )

    return result


def run_sample_tests() -> None:
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]
    assert two_sum([], 10) == []
    assert two_sum([3, 3], 6) == [0, 1]

    assert longest_unique_substring('abcabcbb') == 3
    assert longest_unique_substring('bbbbb') == 1
    assert longest_unique_substring('') == 0

    assert top_k_frequent([1, 1, 1, 2, 2, 3], 2) == [1, 2]
    assert top_k_frequent([], 2) == []
    assert top_k_frequent([3, 2, 1], 2) == [1, 2]

    assert merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]) == [
        [1, 6],
        [8, 10],
        [15, 18],
    ]
    assert merge_intervals([[1, 4], [4, 5]]) == [[1, 5]]
    assert merge_intervals([]) == []

    assert subarray_sum_equals_k([1, 1, 1], 2) == 2
    assert subarray_sum_equals_k([1, -1, 0], 0) == 3

    assert product_except_self([1, 2, 3, 4]) == [24, 12, 8, 6]
    assert product_except_self([0, 1, 2]) == [2, 0, 0]

    assert kth_largest([3, 2, 1, 5, 6, 4], 2) == 5
    try:
        kth_largest([1], 2)
    except ValueError:
        pass
    else:
        raise AssertionError('expected ValueError for k > n')

    assert min_meeting_rooms([[0, 30], [5, 10], [15, 20]]) == 2
    assert min_meeting_rooms([[7, 10], [2, 4]]) == 1
    assert min_meeting_rooms([]) == 0

    grid = [
        ['1', '1', '0', '0', '0'],
        ['1', '1', '0', '0', '0'],
        ['0', '0', '1', '0', '0'],
        ['0', '0', '0', '1', '1'],
    ]
    assert number_of_islands(grid) == 3

    assert can_finish_courses(2, [(1, 0)])
    assert not can_finish_courses(2, [(1, 0), (0, 1)])

    streams = [
        [
            FeedItem('a1', 'A', 130),
            FeedItem('a2', 'A', 100),
        ],
        [
            FeedItem('b1', 'B', 125),
            FeedItem('b2', 'B', 90),
        ],
        [
            FeedItem('c1', 'C', 120),
            FeedItem('c2', 'C', 110),
        ],
    ]
    merged = merge_newest_streams(streams, 5)
    assert [item.item_id for item in merged] == ['a1', 'b1', 'c1', 'c2', 'a2']

    print('All progressive algorithm pattern sample tests passed.')


if __name__ == '__main__':
    run_sample_tests()


'''
Follow-up discussion prompts:

Two Sum
- What if the array is already sorted?
- What if original indices are not required?
- What if values arrive as a stream?

Longest Unique Substring
- Why must left never move backward?
- How does alphabet size affect memory?

Top K
- What changes when k varies between repeated queries?
- What if the number of unique values does not fit in memory?

Merge Intervals / Meeting Rooms
- Are touching boundaries considered overlapping?
- What if intervals arrive online?

Subarray Sum
- Why does the initial prefix_count[0] = 1 matter?
- Why does a sliding window not work reliably when negative values are allowed?

Kth Largest
- Compare sorting, heap, and quickselect.
- Which solution naturally supports streaming?

Number of Islands
- What changes if diagonal adjacency counts?
- What if the grid is too large to fit in memory?

Course Schedule
- How would you return one valid ordering instead of only True/False?
- How would you identify a cycle?

K-Way Merge
- Why not concatenate and sort everything?
- How would cursor pagination continue from a previous page?
- What if one stream is extremely hot or slow to fetch?
'''
