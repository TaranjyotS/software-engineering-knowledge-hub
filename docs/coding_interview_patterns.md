# Coding Interview Patterns, Data Structures & Progressive Optimization

> **Purpose:** Reusable senior-level coding interview strategy, algorithm patterns, complexity reasoning, edge-case testing, and progressive problem solving.
> **Use this file for:** 45–60 minute coding rounds where the interviewer expects a simple correct solution first, followed by optimization, complexity analysis, testing, and follow-up constraints.

---

## Recommended Study Flow

1. Memorize the **problem-solving loop** rather than isolated answers.
2. Review the **Python complexity cheat sheet** until the common operations are automatic.
3. Practice each pattern by explaining the brute-force approach before writing the optimized solution.
4. Run the companion exercises in `coding_questions/progressive_algorithm_patterns.py`.
5. Finish every problem with edge cases, complexity, and one likely follow-up.

---

## Quick Summary

A strong coding interview is not only about producing the optimal algorithm. The interviewer also evaluates how the solution is derived, whether the data structure matches the bottleneck, whether complexity is explained correctly, and whether the implementation remains correct under changed constraints.

Use this progression:

```text
Understand
   ↓
Clarify constraints
   ↓
State a simple correct solution
   ↓
Analyze time and space
   ↓
Identify the expensive repeated operation
   ↓
Choose a structure/algorithm that removes that bottleneck
   ↓
Implement cleanly
   ↓
Recalculate complexity
   ↓
Test edge cases
   ↓
Handle follow-up constraints
```

A useful interview sentence is:

> The straightforward solution is ___ and costs ___. The bottleneck is ___. If I maintain ___, I can reduce the runtime to ___ at the cost of ___ additional memory.

---

## 1. Opening a Coding Problem

### 1.1 Restate the requirement

Before coding, confirm what the function must produce.

> Let me restate the problem to make sure I understand it. We need to ___, and the output should ___.

### 1.2 Ask only constraint-changing questions

Good questions include:

- Can the input be empty?
- Are duplicates allowed?
- Is the input sorted?
- Can I modify the input?
- Do I need original indices or only values?
- What should happen when no solution exists?
- Is output ordering important?
- Is this a one-time batch operation or repeated queries?
- Can the data arrive as a stream?
- What are the approximate input-size limits?

Do not spend several minutes asking questions whose answers do not change the algorithm.

### 1.3 State the invariant while coding

Do not narrate syntax such as “now I am writing a loop.” Explain what state means.

Weak:

> I am adding a dictionary here.

Strong:

> This dictionary maps each previously seen value to its index, so I can test for the required complement in expected O(1) time.

---

## 2. Python Complexity Cheat Sheet

### 2.1 List

|   Operation    | Typical Complexity |             Interview Note             |
| -------------- | -----------------: | -------------------------------------- |
| `append(x)`    |     amortized O(1) | Dynamic array may occasionally resize. |
| `pop()`        |               O(1) | Removes from the end.                  |
| `pop(0)`       |               O(n) | Remaining elements shift left.         |
| `insert(0, x)` |               O(n) | Existing elements shift right.         |
| `x in list`    |               O(n) | Linear search.                         |
| index access   |               O(1) | Direct array indexing.                 |
| slicing        |               O(k) | Creates a new list of k items.         |
| sort           |         O(n log n) | Python uses Timsort.                   |

### 2.2 Dictionary / set

|   Operation   | Expected Complexity |           Note            |
| ------------- | ------------------: | ------------------------- |
| lookup        |                O(1) | Hash-based expected case. |
| insert/update |                O(1) | Expected case.            |
| delete        |                O(1) | Expected case.            |
| membership    |                O(1) | Expected case.            |

Worst-case hash-table behavior can degrade toward O(n), but expected O(1) is the normal interview model unless adversarial hashing is part of the question.

### 2.3 `collections.deque`

|   Operation    | Complexity |
| -------------- | ---------: |
| `append()`     |       O(1) |
| `appendleft()` |       O(1) |
| `pop()`        |       O(1) |
| `popleft()`    |       O(1) |

Use a deque when elements must be added/removed from both ends. A list is a poor FIFO queue when `pop(0)` is required.

### 2.4 Heap

|    Operation    | Complexity |
| --------------- | ---------: |
| peek minimum    |       O(1) |
| push            |   O(log n) |
| pop minimum     |   O(log n) |
| heapify n items |       O(n) |

A size-k min-heap is common when only the best k items are needed from a much larger set.

### 2.5 Graphs and search

- BFS: O(V + E)
- DFS: O(V + E)
- Binary search: O(log n)
- Sorting: O(n log n)

Always define what n, V, E, k, or other variables mean before giving complexity.

---

## 3. Pattern: Hash Map — Two Sum

### Question

Given an array of integers and a target, return the indices of two values whose sum is the target.

### Simple solution

Compare every pair.

```python
for i in range(len(nums)):
    for j in range(i + 1, len(nums)):
        if nums[i] + nums[j] == target:
            return [i, j]
```

- Time: O(n²)
- Auxiliary space: O(1)

### Optimization reasoning

The expensive operation is repeatedly searching for the complement `target - value`.

Maintain:

```text
value -> index
```

Then each complement lookup is expected O(1).

```python
def two_sum(nums, target):
    seen = {}

    for index, value in enumerate(nums):
        complement = target - value
        if complement in seen:
            return [seen[complement], index]
        seen[value] = index

    return []
```

- Time: O(n) expected
- Space: O(n)

### Follow-up: Can memory be reduced?

If original indices are not required and mutation is allowed, sort and use two pointers:

- Time: O(n log n)
- Extra space: potentially O(1), depending on sorting/runtime details

The trade-off is losing the simple original-index mapping.

---

## 4. Pattern: Sliding Window — Longest Substring Without Repeating Characters

### Question

Find the length of the longest substring containing no repeated character.

### Optimization insight

Restarting a scan from every index repeats work. Maintain one valid window `[left, right]` and the most recent index of every character.

```python
def longest_unique_substring(s):
    last_seen = {}
    left = 0
    best = 0

    for right, char in enumerate(s):
        if char in last_seen and last_seen[char] >= left:
            left = last_seen[char] + 1

        last_seen[char] = right
        best = max(best, right - left + 1)

    return best
```

- Time: O(n)
- Space: O(min(n, alphabet size))

### Why does `left` never move backward?

A character occurrence before `left` is no longer part of the active window and cannot invalidate it.

---

## 5. Pattern: Top-K — Frequency Map + Heap

### Question

Return the k most frequent values.

### Baseline

1. Count frequencies in O(n).
2. Sort all unique values in O(u log u), where u is the number of unique values.

Total:

```text
O(n + u log u)
```

### Improved when `k << u`

Keep a min-heap of size k.

```text
count frequencies: O(n)
select top k:       O(u log k)
```

Total:

```text
O(n + u log k)
```

### Follow-up: What if k is almost u?

Sorting can be simpler and similarly efficient because `log k` approaches `log u`. Choose based on actual constraints rather than assuming the heap is always superior.

The repository also contains a deeper batch/streaming variant in `coding_questions/top_k_frequent_paths.py`.

---

## 6. Pattern: Sorting + Scan — Merge Intervals

### Question

Merge overlapping intervals.

### Reasoning

Without ordering, detecting overlaps can require repeated comparison. Sorting by start time ensures that any interval capable of overlapping the current merged interval appears next.

```python
def merge_intervals(intervals):
    if not intervals:
        return []

    intervals = sorted(intervals, key=lambda interval: interval[0])
    merged = [list(intervals[0])]

    for start, end in intervals[1:]:
        last_end = merged[-1][1]

        if start <= last_end:
            merged[-1][1] = max(last_end, end)
        else:
            merged.append([start, end])

    return merged
```

- Time: O(n log n)
- Result space: O(n) in the worst case

### Edge cases

- Empty input
- One interval
- Nested intervals
- Touching boundaries such as `[1, 3]` and `[3, 5]`
- Already sorted or reverse-sorted input

Clarify whether touching intervals should merge.

---

## 7. Pattern: Prefix Sum + Hash Map — Subarray Sum Equals K

### Question

Count contiguous subarrays whose sum equals k.

### Baseline

Enumerating every start/end pair with a running sum costs O(n²).

### Optimization

Let the current prefix sum be `P`. If an earlier prefix was `P - k`, then the subarray between them sums to k:

```text
P - (P - k) = k
```

```python
def subarray_sum_equals_k(nums, k):
    prefix_count = {0: 1}
    prefix = 0
    result = 0

    for value in nums:
        prefix += value
        result += prefix_count.get(prefix - k, 0)
        prefix_count[prefix] = prefix_count.get(prefix, 0) + 1

    return result
```

- Time: O(n)
- Space: O(n)

The initial `{0: 1}` handles subarrays beginning at index 0.

---

## 8. Pattern: Prefix/Suffix — Product of Array Except Self

### Question

For each index, return the product of every other value without division.

### Simple solution

Multiply every other value per index: O(n²).

### Better approach

Store the product of everything to the left, then multiply by a running suffix product from the right.

```python
def product_except_self(nums):
    result = [1] * len(nums)

    prefix = 1
    for i in range(len(nums)):
        result[i] = prefix
        prefix *= nums[i]

    suffix = 1
    for i in range(len(nums) - 1, -1, -1):
        result[i] *= suffix
        suffix *= nums[i]

    return result
```

- Time: O(n)
- Auxiliary space: O(1), excluding the required output array

Always state the “excluding output” qualification when claiming O(1) auxiliary space.

---

## 9. Pattern: Heap or Quickselect — Kth Largest

### Options

|     Approach      |           Time            |                       Good Fit                        |
| ----------------- | ------------------------: | ----------------------------------------------------- |
| Sort entire array |                O(n log n) | Simplicity, one moderate-sized query                  |
| Size-k min-heap   |                O(n log k) | Streaming or small k                                  |
| Quickselect       | O(n) average, O(n²) worst | One selection query where average linear time matters |

### Interview answer

> I would start with sorting because it is simple and correct. If n is large and k is small, a size-k heap avoids ordering everything. If one batch selection must be optimized further, quickselect gives expected O(n) time, with a more complex implementation and O(n²) worst case unless stronger pivot strategies are used.

---

## 10. Pattern: Intervals + Heap — Meeting Rooms

### Question

Find the minimum number of rooms required to schedule all meetings.

### Min-heap interpretation

The heap contains end times of rooms currently in use. The smallest end time tells whether the next meeting can reuse a room.

```python
import heapq


def min_meeting_rooms(intervals):
    if not intervals:
        return 0

    intervals = sorted(intervals, key=lambda interval: interval[0])
    heap = []

    for start, end in intervals:
        if heap and heap[0] <= start:
            heapq.heappop(heap)
        heapq.heappush(heap, end)

    return len(heap)
```

- Time: O(n log n)
- Space: O(n) worst case

A sorted-start/sorted-end two-pointer approach is another O(n log n) solution.

---

## 11. Pattern: Graph Traversal — Number of Islands

### Question

Count connected components of land cells in a grid.

### DFS/BFS idea

Every unvisited land cell starts a new island. Traverse its entire connected component and mark it visited.

```text
scan cell
  ↓
new unvisited land?
  ↓ yes
increment island count
  ↓
DFS/BFS all connected land
```

- Time: O(rows × cols)
- Space: O(rows × cols) worst case for recursion/queue/visited state

### Follow-up: Cannot mutate input

Maintain a separate `visited` set or boolean matrix, trading additional memory for preserving the original grid.

For very deep components in Python, iterative DFS/BFS can avoid recursion-depth limits.

---

## 12. Pattern: Topological Sort — Course Schedule

### Question

Given prerequisite pairs, determine whether all courses can be completed.

### Model

This is cycle detection in a directed graph.

Kahn’s algorithm maintains indegree counts:

```text
nodes with indegree 0
        ↓
      queue
        ↓
remove node and decrement neighbors
        ↓
new indegree 0 nodes enter queue
```

If fewer than V nodes are processed, a directed cycle exists.

- Time: O(V + E)
- Space: O(V + E)

---

## 13. Pattern: K-Way Merge of Sorted Streams

This pattern is useful both in coding interviews and feed/search aggregation designs.

### Question

Given P streams, each already sorted newest-to-oldest, return the newest N items across all streams.

### Naive option

Concatenate all items and sort them all.

If there are M total candidates:

```text
O(M log M)
```

### Better option

Put only the current head of every stream into a heap. Each pop reveals the next globally best item; then push the next item from that same stream.

```text
P sorted streams
      ↓
heap of at most P heads
      ↓
pop best, advance that stream
      ↓
stop after N results
```

Complexity for returning N items after stream heads are available:

```text
O(N log P)
```

This is especially valuable when N is small relative to the total history in all streams.

---

## 14. Choosing the Data Structure from the Bottleneck

|        Repeated expensive operation        |   Likely structure/pattern    |
| ------------------------------------------ | ----------------------------- |
| Search for previously seen value           | Hash map / set                |
| Add/remove from both ends                  | Deque                         |
| Repeated min/max among changing candidates | Heap                          |
| Need only top k                            | Size-k heap / selection       |
| Contiguous range with changing boundary    | Sliding window                |
| Repeated range/subarray sum                | Prefix sum                    |
| Overlap among ranges                       | Sort + scan / heap            |
| Connectivity                               | DFS/BFS / Union-Find          |
| Dependency order                           | Topological sort              |
| Ordered lookup                             | Binary search / balanced tree |
| O(1) lookup + O(1) recency updates         | Hash map + doubly linked list |

The best answer is not “use data structure X.” The best answer explains what repeated work X removes.

---

## 15. Edge-Case Testing Checklist

Before saying “done,” consider:

```text
normal case
empty input
single element
minimum/maximum bounds
duplicates
negative/zero values
no-solution case
multiple valid solutions
ordering/tie rules
whether input was accidentally mutated
very large input assumptions
```

For stateful data structures additionally test:

```text
insert
update same key
remove
capacity boundary
reinsert
repeated operation
expiration boundary
stale metadata entries
```

---

## 16. What to Say When Temporarily Stuck

Do not go silent. Anchor on correctness and identify the bottleneck.

> The brute-force version is clear, so I’ll anchor correctness there. The expensive operation appears to be ___. I’m thinking about whether I can avoid repeating it by maintaining ___.

Or:

> I see two possible directions. One trades memory for faster lookup using a hash structure, while the other imposes ordering first. Let me compare their complexity against the constraints.

This keeps the interviewer inside the reasoning process.

---

## 17. Common Coding Interview Mistakes

- Jumping directly to an optimized pattern without explaining why it applies.
- Giving Big-O without defining the variables.
- Claiming O(1) space while ignoring an auxiliary map/list that grows with input.
- Using `list.pop(0)` as an O(1) queue operation in Python.
- Mutating input without confirming it is allowed.
- Treating hash-table O(1) as an absolute worst-case guarantee.
- Forgetting stable tie-breaking requirements in top-k/ranking problems.
- Writing code silently for several minutes.
- Saying “done” before testing a normal case and boundaries.
- Optimizing before a correct baseline is established when the interview specifically values progressive improvement.

---

## 18. High-Probability Follow-Ups

Be ready for the interviewer to change one constraint:

- What if input arrives as a stream?
- What if memory is limited?
- What if there are repeated queries with different k?
- What if the input is already sorted?
- What if values are extremely high cardinality?
- What if the input cannot be modified?
- What if the operation must be thread-safe?
- What if the state lives across multiple processes/machines?
- What if exactness can be traded for bounded memory?
- What if the query becomes latency-sensitive at 10× scale?

A good response is to explain which assumption changed and therefore why the original data structure may no longer be ideal.

---

## 19. 60-Minute Coding Round Game Plan

A realistic one-hour round often looks like:

```text
0–5 min    clarify + baseline approach
5–15 min   implement simple/correct solution or core structure
15–25 min  analyze + optimize
25–40 min  implement optimized version
40–50 min  tests + edge cases
50–58 min  follow-up constraint / concurrency / scaling
58–60 min  summarize complexity + trade-off
```

The exact pacing varies, but the principle is the same: correctness first, then measured improvement.

---

## 20. Quick Revision Checklist

Before a coding interview, be able to explain from memory:

- Hash map and set use cases
- Two pointers
- Sliding window
- Prefix sums
- Stack and monotonic stack basics
- Queue/deque
- Heap/top-k
- Intervals
- Linked-list pointer manipulation
- Trees and BST traversal
- BFS/DFS
- Topological sort
- Binary search
- LRU design
- Time/space complexity of common Python operations
- Edge-case testing
- How the solution changes for streaming or concurrency

Companion runnable implementations are in:

- `coding_questions/progressive_algorithm_patterns.py`
- `coding_questions/concurrent_data_structures.py`
- `coding_questions/expiring_window_map.py`
- `coding_questions/top_k_frequent_paths.py`

---

## 21. Sliding-Window Hit Counter

### Question

Design a counter that returns how many events occurred during the last W seconds/minutes.

### Simple exact deque approach

Store event timestamps in chronological order:

```text
hit(t)
  → append timestamp

count(now)
  → popleft while timestamp <= now - W
  → len(deque)
```

With each timestamp inserted and removed once, cleanup is amortized O(1) per event; memory is O(number of hits in the active window).

### High-volume optimization

If timestamp resolution is bounded, aggregate into time buckets instead of one entry per hit:

```text
bucket timestamp
bucket count
```

This caps memory near the number of time buckets rather than total event count, at the cost of bucket-level precision and careful boundary handling.

### Follow-ups

- What if hits arrive out of order? A simple deque assumes chronological arrival; use ordered storage or event-time/windowing logic otherwise.
- What if the counter is distributed? Per-process counters must be combined or moved to a shared/partitioned store; exact global windows add coordination cost.
- What if approximate counts are acceptable? Approximation/sketching can reduce memory/network overhead at scale.
