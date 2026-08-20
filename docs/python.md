# Python

> **Purpose:** Python fundamentals, advanced Python, backend coding patterns, concurrency, performance, and coding interview preparation.
> **Use this file for:** Python technical interviews and backend engineering interviews

---

## Recommended Study Flow

1. Read the **Quick Summary** first.
2. Review the **Key Concepts** and tables.
3. Practice the **Interview Questions & Answers** out loud.
4. Use the code snippets and examples to explain trade-offs clearly.
5. Finish with the **Common Mistakes** and **Revision Checklist** sections.

---

## Quick Summary

This file has been refreshed to keep the original repository topic while merging relevant detailed Q&A from the consolidated topic-wise interview-prep pack. Use the top sections for fast revision and the consolidated section for deeper interview preparation.

---

## Core Topics to Master

- OOP: encapsulation, inheritance, polymorphism, abstraction
- Data structures: list, tuple, set, dict
- Decorators, generators, context managers, lambda functions
- Exception handling and logging
- GIL, threading, multiprocessing, asyncio
- Performance optimization, memory management, profiling
- Testing with Pytest and coding interview patterns

---

## Consolidated Interview Questions & Technical Notes

> Python fundamentals, data structures, decorators, generators, exception handling, GIL, threading, multiprocessing, asyncio, performance, and coding exercises.

---

### 1. Python Internals & Concurrency

#### 1.1 AsyncIO with rate limiting

```python
import asyncio
import time
import aiohttp

MAX_CONCURRENCY = 10
RATE_LIMIT = 50  # requests per minute

semaphore = asyncio.Semaphore(MAX_CONCURRENCY)

class RateLimiter:
    def __init__(self, rate_per_minute: int):
        self.interval = 60 / rate_per_minute
        self.lock = asyncio.Lock()
        self.last_call = 0.0

    async def acquire(self):
        async with self.lock:
            now = time.monotonic()
            wait_time = max(0, self.interval - (now - self.last_call))
            if wait_time:
                await asyncio.sleep(wait_time)
            self.last_call = time.monotonic()

rate_limiter = RateLimiter(RATE_LIMIT)

async def fetch(session: aiohttp.ClientSession, url: str):
    retries = 0
    start = time.perf_counter()

    while True:
        try:
            await rate_limiter.acquire()

            async with semaphore:
                async with session.get(url) as response:
                    if response.status >= 500 and retries < 3:
                        raise RuntimeError("Server error")

                    data = await response.json()
                    latency = time.perf_counter() - start
                    print(f"{url} latency={latency:.2f}s retries={retries}")
                    return data

        except Exception:
            if retries >= 3:
                return None

            await asyncio.sleep(2 ** retries)
            retries += 1

async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        return await asyncio.gather(*tasks)
```

#### 1.2 Retry Strategy

For API or LLM failures:

- Retry transient 5xx errors
- Use exponential backoff
- Add jitter
- Set max retry count
- Use timeouts
- Add circuit breaker for repeated failures
- Fallback to another model/service if needed

---

### 2. Python Topics

#### 2.1 Why Use Generators in AI Pipelines?

> "Generators help process large datasets efficiently by producing one item at a time instead of loading everything into memory."

#### 2.2 Generator Example

```python
def read_documents(file_paths):
    for path in file_paths:
        with open(path, "r", encoding="utf-8") as file:
            yield file.read()

for document in read_documents(["doc1.txt", "doc2.txt"]):
    print(document[:100])
```

#### 2.3 AI Pipeline Use Case

In a RAG ingestion pipeline:

```python
def generate_chunks(document: str, chunk_size: int = 500):
    words = document.split()

    for i in range(0, len(words), chunk_size):
        yield " ".join(words[i:i + chunk_size])

def process_documents(documents):
    for doc in documents:
        for chunk in generate_chunks(doc):
            embedding = create_embedding(chunk)
            store_embedding(chunk, embedding)
```

#### 2.4 Benefits of Generators

- Memory efficient
- Good for large files
- Useful for streaming data
- Improves scalability
- Works well for ETL pipelines
- Useful for document chunking
- Prevents loading everything into RAM

#### 2.5 Strong Interview Line

> "I use generators in AI pipelines to stream large datasets, documents, logs, or chunks one item at a time, which improves memory efficiency and scalability."

---

### 3. Python Core Topics

The role expects strong Python fundamentals.

#### Topics to revise

- Data structures: list, tuple, set, dict.
- List comprehensions and generator expressions.
- Functions, decorators, closures.
- Iterators and generators.
- Exception handling.
- Context managers.
- Async programming with `asyncio`.
- Type hints.
- Packaging and dependency management.
- Performance profiling.
- Memory management basics.

---

#### Example: Type hints

```python
from typing import Optional

def calculate_total(price: float, tax_rate: float, discount: Optional[float] = None) -> float:
    total = price + (price * tax_rate)
    if discount:
        total -= discount
    return round(total, 2)
```

**Interview explanation:**

Type hints improve readability, make large codebases easier to maintain, and allow tools such as `mypy` or IDEs to detect type-related issues before runtime.

---

#### Example: Async programming

```python
import asyncio
import httpx

async def fetch_url(url: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text

async def main() -> None:
    urls = [
        "https://example.com/a",
        "https://example.com/b",
        "https://example.com/c",
    ]
    results = await asyncio.gather(*(fetch_url(url) for url in urls))
    print(len(results))

## asyncio.run(main())
```

**Interview explanation:**

`asyncio` is useful for I/O-bound workloads such as API calls, database operations, or network requests. It is not ideal for CPU-heavy tasks unless combined with multiprocessing or worker systems.

---

#### Example: Decorator

```python
import time
from functools import wraps
from typing import Callable, Any

def log_duration(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start
        print(f"{func.__name__} took {duration:.4f}s")
        return result
    return wrapper

@log_duration
def process_records(records: list[dict]) -> int:
    return len(records)
```

**Interview explanation:**

A decorator wraps a function to add reusable behavior such as logging, timing, authentication, caching, or retry handling without changing the function's core logic.

---

### 4. Python Fundamentals

#### 4.1 What is the difference between a tuple and a set?

##### Interview Answer

A **tuple** is an ordered, immutable collection that allows duplicates.
A **set** is an unordered collection that stores only unique elements.

|      Feature      |     Tuple     |               Set                |
| ----------------- | ------------- | -------------------------------- |
| Ordered           | Yes           | No guaranteed order              |
| Mutable           | No            | Yes                              |
| Allows duplicates | Yes           | No                               |
| Indexing          | Yes           | No                               |
| Common use        | Fixed records | Unique values, membership checks |

##### Example

```python
my_tuple = (3, 1, 2, 2)
my_set = {3, 1, 2, 2}

print(my_tuple)
print(my_set)
```

Possible output:

```python
(3, 1, 2, 2)
{1, 2, 3}
```

##### Key Point

The tuple preserves the order and duplicates.
The set removes duplicates and does not guarantee insertion order.

##### Strong One-Liner

> Tuples preserve order and allow duplicates, while sets are unordered collections optimized for uniqueness and fast membership checks.

---

#### 4.2 Write a list comprehension to find squares from 1 to 5

##### Code

```python
squares = [x ** 2 for x in range(1, 6)]

print(squares)
```

##### Output

```python
[1, 4, 9, 16, 25]
```

##### Explanation

- `range(1, 6)` generates numbers from `1` to `5`.
- `x ** 2` calculates the square of each number.
- The list comprehension creates a new list in one line.

---

### 5. Python Operators & Expressions

#### 5.1 What is the output of `2**3**2`?

##### Code

```python
print(2 ** 3 ** 2)
```

##### Output

```python
512
```

##### Explanation

Exponentiation in Python is evaluated **right to left**.

So:

```python
2 ** 3 ** 2
```

is interpreted as:

```python
2 ** (3 ** 2)
```

Step-by-step:

```python
3 ** 2 = 9
2 ** 9 = 512
```

---

#### 5.2 What is the output of `a | b` when `a = 4` and `b = 11`?

##### Code

```python
a = 4
b = 11

print(a | b)
```

##### Output

```python
15
```

##### Explanation

`|` is the **bitwise OR** operator.

Binary representation:

```text
4  = 0100
11 = 1011
```

Bitwise OR:

```text
0100
1011
----
1111
```

Binary `1111` equals decimal `15`.

---

### 6. Lists, Tuples, and Sets

#### 6.1 What does `seta ^ setb` mean?

##### Answer

`^` between two sets means **symmetric difference**.

It returns elements that are present in either set, but **not in both**.

##### Example

```python
seta = {1, 2, 3}
setb = {3, 4, 5}

print(seta ^ setb)
```

##### Output

```python
{1, 2, 4, 5}
```

##### Explanation

- `3` exists in both sets, so it is removed.
- Unique elements from both sets are returned.

Equivalent expression:

```python
(seta - setb) | (setb - seta)
```

---

#### 6.2 Different ways to join two lists

##### Method 1: Using `+`

```python
a = [1, 2]
b = [3, 4]

result = a + b

print(result)
```

Output:

```python
[1, 2, 3, 4]
```

This creates a new list.

---

##### Method 2: Using `extend()`

```python
a = [1, 2]
b = [3, 4]

a.extend(b)

print(a)
```

Output:

```python
[1, 2, 3, 4]
```

This modifies the original list.

---

##### Method 3: Using unpacking

```python
a = [1, 2]
b = [3, 4]

result = [*a, *b]

print(result)
```

Output:

```python
[1, 2, 3, 4]
```

---

##### Method 4: Using `itertools.chain()`

```python
from itertools import chain

a = [1, 2]
b = [3, 4]

result = list(chain(a, b))

print(result)
```

Output:

```python
[1, 2, 3, 4]
```

Useful for large iterables.

---

##### Method 5: Using a loop

```python
a = [1, 2]
b = [3, 4]

for item in b:
    a.append(item)

print(a)
```

Output:

```python
[1, 2, 3, 4]
```

---

#### 6.3 Difference between `append()` and `extend()`

##### `append()`

Adds the entire object as one element.

```python
list1 = [1, 2]
list2 = [3, 4]

list1.append(list2)

print(list1)
```

Output:

```python
[1, 2, [3, 4]]
```

Here, `[3, 4]` is added as a single object.

---

##### `extend()`

Adds each element individually.

```python
list1 = [1, 2]
list2 = [3, 4]

list1.extend(list2)

print(list1)
```

Output:

```python
[1, 2, 3, 4]
```

Equivalent to:

```python
for item in list2:
    list1.append(item)
```

##### Strong One-Liner

> `append()` adds the whole object as a single element, while `extend()` iterates through the iterable and adds each element individually.

---

#### 6.4 What happens when we multiply a list by 2?

##### Example

```python
my_list = [1, 2, 3]

print(my_list * 2)
```

Output:

```python
[1, 2, 3, 1, 2, 3]
```

##### Explanation

`* 2` repeats the list twice. It does **not** multiply individual elements.

---

#### 6.5 Character list multiplication

##### Example

```python
chars = ['a', 'b', 'c']

print(chars * 2)
```

Output:

```python
['a', 'b', 'c', 'a', 'b', 'c']
```

It does **not** produce:

```python
['aa', 'bb', 'cc']
```

##### Important Caveat

```python
arr = [[]] * 3

arr[0].append(1)

print(arr)
```

Output:

```python
[[1], [1], [1]]
```

Why?
All inner lists refer to the same object in memory.

Correct way:

```python
arr = [[] for _ in range(3)]

arr[0].append(1)

print(arr)
```

Output:

```python
[[1], [], []]
```

---

### 7. Python Functions, Decorators, and Generators

#### 7.1 What are decorators in Python?

##### Interview Answer

A decorator is a function that modifies or extends the behavior of another function without changing its source code.

Decorators are commonly used for:

- Logging
- Authentication
- Authorization
- Caching
- Retry logic
- Performance measurement
- API route registration

---

##### Simple Decorator Example

```python
def logger(func):
    def wrapper():
        print("Function started")
        func()
        print("Function ended")
    return wrapper

@logger
def greet():
    print("Hello")

greet()
```

Output:

```python
Function started
Hello
Function ended
```

---

##### What does `@logger` mean?

This:

```python
@logger
def greet():
    print("Hello")
```

is equivalent to:

```python
def greet():
    print("Hello")

greet = logger(greet)
```

---

##### Decorator with Arguments

```python
def logger(func):
    def wrapper(*args, **kwargs):
        print("Calling function")
        return func(*args, **kwargs)
    return wrapper

@logger
def add(a, b):
    return a + b

print(add(2, 3))
```

Output:

```python
Calling function
5
```

---

##### FastAPI Decorator Example

```python
@app.get("/users")
def get_users():
    return {"users": []}
```

Here, `@app.get("/users")` is a decorator.

It tells FastAPI:

> When a GET request comes to `/users`, execute this function.

---

##### Strong One-Liner

> Decorators allow us to add reusable behavior like logging, authentication, caching, or route registration without modifying the original function.

---

#### 7.2 What is a generator in Python?

##### Interview Answer

A generator is a special function that returns values one at a time using `yield`, instead of returning all values at once.

Generators are memory efficient because they produce values lazily.

---

##### Normal Function Using `return`

```python
def get_numbers():
    return [1, 2, 3]

result = get_numbers()
print(result)
```

Output:

```python
[1, 2, 3]
```

The entire list is created in memory.

---

##### Generator Function Using `yield`

```python
def get_numbers():
    yield 1
    yield 2
    yield 3

gen = get_numbers()

print(next(gen))
print(next(gen))
print(next(gen))
```

Output:

```python
1
2
3
```

The values are generated one by one.

---

#### 7.3 Difference between `yield` and `return`

|             `return`             |           `yield`            |
| -------------------------------- | ---------------------------- |
| Ends function execution          | Pauses function execution    |
| Returns full result at once      | Produces one value at a time |
| More memory usage for large data | Memory efficient             |
| Function state is lost           | Function state is preserved  |

---

#### 7.4 When should we use `yield` and when should we use `return`?

##### Use `return` when:

- The dataset is small.
- You need all results immediately.
- The result should be available at once.
- Memory usage is not a concern.

Example:

```python
def get_users():
    return ["John", "Alice", "Bob"]
```

---

##### Use `yield` when:

- The dataset is large.
- You are streaming data.
- You are reading large files.
- You want memory efficiency.
- You are processing records one by one.

Example:

```python
def read_large_file():
    with open("logs.txt") as f:
        for line in f:
            yield line
```

---

##### Large Dataset Example

Using `return`:

```python
def numbers():
    return [i for i in range(1, 1000001)]
```

This creates one million numbers in memory.

Using `yield`:

```python
def numbers():
    for i in range(1, 1000001):
        yield i
```

This generates values on demand.

---

##### Strong One-Liner

> Use `return` when you need the complete result immediately. Use `yield` when processing large datasets, streams, files, or values that should be generated one at a time.

---

### 8. Exception Handling

#### 8.1 When does the `finally` block execute?

##### Answer

The `finally` block is executed **always**, whether an exception occurs or not.

It runs:

- If no exception occurs.
- If an exception occurs and is handled.
- If an exception occurs and is not handled.
- Even if there is a `return` statement inside `try` or `except`.

---

##### Example 1: No Exception

```python
try:
    print("Inside try")
except:
    print("Inside except")
finally:
    print("Inside finally")
```

Output:

```python
Inside try
Inside finally
```

---

##### Example 2: Exception Occurs

```python
try:
    10 / 0
except ZeroDivisionError:
    print("Exception handled")
finally:
    print("Inside finally")
```

Output:

```python
Exception handled
Inside finally
```

---

##### Example 3: `return` Statement

```python
def test():
    try:
        return "try"
    finally:
        print("finally")

print(test())
```

Output:

```python
finally
try
```

The `finally` block executes before the function actually returns.

---

##### Real-World Use

`finally` is commonly used for cleanup:

```python
file = open("data.txt")

try:
    data = file.read()
finally:
    file.close()
```

Even if reading fails, the file is closed.

---

##### Strong One-Liner

> The `finally` block always executes and is mainly used for cleanup operations like closing files, database connections, or network sockets.

### 9. Coding Interview Practice Topics

These topics were discussed as likely coding interview preparation areas.

#### 9.1 Arrays and strings

Prepare:

- Reverse string
- Palindrome check
- Valid anagram
- Longest common prefix
- Two sum
- Remove duplicates
- Count character frequency

##### Frequency Counter Example

```python
def char_frequency(s):
    freq = {}

    for char in s:
        freq[char] = freq.get(char, 0) + 1

    return freq

print(char_frequency("banana"))
```

Output:

```python
{'b': 1, 'a': 3, 'n': 2}
```

---

#### 9.2 Hash maps

Useful for:

- Two Sum
- Frequency counting
- Group anagrams
- Detect duplicates

##### Two Sum Example

```python
def two_sum(nums, target):
    seen = {}

    for i, num in enumerate(nums):
        diff = target - num

        if diff in seen:
            return [seen[diff], i]

        seen[num] = i

    return []

print(two_sum([2, 7, 11, 15], 9))
```

Output:

```python
[0, 1]
```

---

#### 9.3 Sliding window

Useful for:

- Longest substring without repeating characters
- Maximum sum subarray of size `k`
- Minimum window substring

##### Example: Maximum Sum of Size K

```python
def max_sum_subarray(nums, k):
    window_sum = sum(nums[:k])
    max_sum = window_sum

    for i in range(k, len(nums)):
        window_sum += nums[i] - nums[i - k]
        max_sum = max(max_sum, window_sum)

    return max_sum

print(max_sum_subarray([2, 1, 5, 1, 3, 2], 3))
```

Output:

```python
9
```

---

#### 9.4 Stack

Useful for:

- Valid parentheses
- Browser history
- Expression evaluation
- Monotonic stack problems

##### Valid Parentheses Example

```python
def is_valid(s):
    stack = []
    mapping = {
        ")": "(",
        "}": "{",
        "]": "["
    }

    for char in s:
        if char in mapping.values():
            stack.append(char)
        elif char in mapping:
            if not stack or stack.pop() != mapping[char]:
                return False

    return not stack

print(is_valid("()[]{}"))
```

Output:

```python
True
```

---

#### 9.5 Linked list

Prepare:

- Reverse linked list
- Detect cycle
- Merge two sorted lists

##### Reverse Linked List Pattern

```python
def reverse_list(head):
    prev = None
    current = head

    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node

    return prev
```

---

#### 9.6 Trees

Prepare:

- DFS
- BFS
- Maximum depth
- Validate BST
- Level order traversal

##### Max Depth Example

```python
def max_depth(root):
    if not root:
        return 0

    return 1 + max(max_depth(root.left), max_depth(root.right))
```

---

#### 9.7 SQL topics

Prepare:

- Joins
- Aggregations
- Group By
- Window functions
- `ROW_NUMBER()`
- `RANK()`
- `DENSE_RANK()`

##### Example: Top transaction per customer

```sql
SELECT *
FROM (
    SELECT
        t.*,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY amount DESC
        ) AS rn
    FROM transactions t
) ranked
WHERE rn = 1;
```

---

### 10. Python Core Concepts

#### 10.1 Mutable vs immutable objects

##### Mutable

Can be changed after creation.

Examples:

- `list`
- `dict`
- `set`

##### Immutable

Cannot be changed after creation.

Examples:

- `int`
- `float`
- `str`
- `tuple`
- `frozenset`

---

#### 10.2 List vs tuple

##### List

- Mutable.
- Good for dynamic collections.
- Supports append/remove/update.

##### Tuple

- Immutable.
- Good for fixed records.
- Can be used as dictionary key if all elements are hashable.

```python
items = [1, 2, 3]
items.append(4)

point = (10, 20)
```

---

#### 10.3 Dictionary keys

Dictionary keys must be hashable.

##### Valid keys

```python
my_dict = {
    "name": "Ava",
    1: "one",
    (1, 2): "tuple key"
}
```

##### Invalid key

```python
## TypeError: unhashable type: 'list'
my_dict = {[1, 2]: "bad"}
```

##### Tuple caveat

```python
valid = {(1, 2): "ok"}

## invalid because tuple contains mutable list
## invalid = {([1, 2], 3): "bad"}
```

---

#### 10.4 Class variables vs instance variables

```python
class User:
    role = "member"          # class variable

    def __init__(self, name):
        self.name = name      # instance variable
```

##### Behavior

- Class variable shared across class unless shadowed by instance.
- Instance variable belongs to a specific object.

```python
u1 = User("A")
u2 = User("B")

u1.role = "admin"  # creates instance attribute shadowing class variable

print(u1.role)  # admin
print(u2.role)  # member
print(User.role)  # member
```

---

#### 10.5 Instance method, class method, static method

```python
class Example:
    value = 10

    def instance_method(self):
        return self.value

    @classmethod
    def class_method(cls):
        return cls.value

    @staticmethod
    def static_method(x, y):
        return x + y
```

##### Use cases

- Instance method: needs object state.
- Class method: needs class state or alternate constructor.
- Static method: utility function logically belongs to class.

#### 10.6 `*args` and `**kwargs`

```python
def demo(required, *args, **kwargs):
    print(required)
    print(args)
    print(kwargs)

demo(1, 2, 3, name="Ava")
```

Output:

```text
1
(2, 3)
{'name': 'Ava'}
```

---

#### 10.7 `==` vs `is`

##### `==`

Checks value equality.

##### `is`

Checks object identity.

```python
a = [1, 2]
b = [1, 2]

print(a == b)  # True
print(a is b)  # False
```

Use `is` for `None`:

```python
if value is None:
    pass
```

---

#### 10.8 Handling multiple exception types

```python
try:
    result = 10 / x
except ZeroDivisionError:
    print("division by zero")
except TypeError:
    print("wrong type")
```

---

#### 10.9 Mutable default argument bug

##### Bad

```python
def add_item(item, items=[]):
    items.append(item)
    return items
```

##### Good

```python
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

##### Why

Default arguments are evaluated once when the function is defined.

---

#### 10.10 Lists, sets, and dicts for membership/deduplication

##### List

- Ordered.
- Allows duplicates.
- Membership is `O(n)`.

##### Set

- Unique values.
- Average `O(1)` membership.
- Best for deduplication.

##### Dict

- Key-value mapping.
- Average `O(1)` key lookup.
- Good for counts/frequencies.

```python
seen = set()
unique = []

for item in items:
    if item not in seen:
        seen.add(item)
        unique.append(item)
```

---

### 11. Python Coding Problems and Algorithms

#### 11.1 Longest substring without repeating characters

##### Sliding window solution

```python
def longest_substring(s):
    seen = {}
    left = 0
    best_len = 0
    best_start = 0

    for right, char in enumerate(s):
        if char in seen and seen[char] >= left:
            left = seen[char] + 1

        seen[char] = right

        if right - left + 1 > best_len:
            best_len = right - left + 1
            best_start = left

    return s[best_start:best_start + best_len]

print(longest_substring("abcabcbb"))  # abc
```

##### Complexity

- Time: `O(n)`
- Space: `O(k)` where `k` is unique chars.

---

#### 11.2 Minimum window substring without Counter

##### Problem

Find the smallest substring in `s` containing all characters of `t`, including duplicates.

```python
def min_window_substring(s: str, t: str) -> str:
    if not s or not t:
        return ""

    target = {}
    for char in t:
        target[char] = target.get(char, 0) + 1

    window = {}
    required = len(target)
    formed = 0
    left = 0
    min_len = float("inf")
    result = ""

    for right in range(len(s)):
        char = s[right]
        window[char] = window.get(char, 0) + 1

        if char in target and window[char] == target[char]:
            formed += 1

        while formed == required:
            if right - left + 1 < min_len:
                min_len = right - left + 1
                result = s[left:right + 1]

            left_char = s[left]
            window[left_char] -= 1

            if left_char in target and window[left_char] < target[left_char]:
                formed -= 1

            left += 1

    return result

print(min_window_substring("ADOBECODEBANC", "ABC"))  # BANC
```

---

#### 11.3 Kth largest element using Quickselect

##### Idea

Convert kth largest to `(n-k)`th smallest.

```python
import random

def find_kth_largest(nums, k):
    target = len(nums) - k

    def quickselect(left, right):
        pivot_index = random.randint(left, right)
        nums[pivot_index], nums[right] = nums[right], nums[pivot_index]
        pivot = nums[right]

        p = left
        for i in range(left, right):
            if nums[i] <= pivot:
                nums[p], nums[i] = nums[i], nums[p]
                p += 1

        nums[p], nums[right] = nums[right], nums[p]

        if p == target:
            return nums[p]
        if p < target:
            return quickselect(p + 1, right)
        return quickselect(left, p - 1)

    return quickselect(0, len(nums) - 1)

print(find_kth_largest([3, 2, 1, 5, 6, 4], 2))  # 5
```

##### Complexity

- Average: `O(n)`
- Worst: `O(n²)`

---

#### 11.4 Reverse Polish Notation evaluation

```python
def eval_rpn(tokens):
    stack = []

    for token in tokens:
        if token in "+-*/":
            b = stack.pop()
            a = stack.pop()

            if token == "+":
                stack.append(a + b)
            elif token == "-":
                stack.append(a - b)
            elif token == "*":
                stack.append(a * b)
            else:
                stack.append(int(a / b))  # truncate toward zero
        else:
            stack.append(int(token))

    return stack[0]

print(eval_rpn("2 1 + 3 *".split()))  # 9
```

##### Important division note

Use `int(a / b)` instead of `a // b` when truncation toward zero is required.

---

#### 11.5 Combination calculation with memoization

##### Problem

Naive recursion recalculates same subproblems.

##### Improved solution

```python
def compute_combinations(n, k, memo=None):
    if memo is None:
        memo = {}

    if k == 0 or k == n:
        return 1

    if (n, k) in memo:
        return memo[(n, k)]

    memo[(n, k)] = (
        compute_combinations(n - 1, k - 1, memo)
        + compute_combinations(n - 1, k, memo)
    )

    return memo[(n, k)]

print(compute_combinations(5, 3))  # 10
```

##### Complexity

- Naive: exponential.
- Memoized: `O(n*k)`.

---

#### 11.6 Even number function

```python
def is_even(number):
    return number % 2 == 0
```

---

#### 11.7 Merge dictionaries

##### Original issue

Mutating `dict1` may cause side effects.

##### Better solution

```python
def merge_dictionaries(dict1, dict2):
    return {**dict1, **dict2}
```

Or:

```python
def merge_dictionaries(dict1, dict2):
    merged = dict1.copy()
    merged.update(dict2)
    return merged
```

Overlapping keys from `dict2` overwrite `dict1`.

---

#### 11.8 Print queue / priority order without heapq

##### Problem summary

Jobs are printed by highest priority. If same priority, preserve original order.

```python
def print_order(priorities):
    jobs = [(priority, index) for index, priority in enumerate(priorities)]
    result = []

    while jobs:
        max_priority = max(priority for priority, _ in jobs)

        for _ in range(len(jobs)):
            priority, index = jobs.pop(0)

            if priority == max_priority:
                result.append(index)
                break
            else:
                jobs.append((priority, index))

    return result

print(print_order([3, 1, 4, 2]))  # [2, 0, 3, 1]
print(print_order([2, 2, 2]))     # [0, 1, 2]
```

##### Complexity

`O(n²)` because of repeated `max()` and queue rotations.

---

### Python Memory and Performance

Python performance is likely to come up because the language is central to AI/ML, backend development, data processing, and automation.

#### Interview Question

**How would you improve Python performance?**

#### Answer

Possible approaches:

- Use efficient data structures
- Avoid unnecessary loops
- Use generators for large data
- Use NumPy/Pandas vectorization
- Use multiprocessing for CPU-bound tasks
- Cache repeated computations
- Profile before optimizing

#### Example: Caching

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(35))
```

---

### 12. Python Engineering

#### Likely Questions

- How strong is your Python experience?
- What Python frameworks have you used?
- How do you structure a Python backend project?
- How do you handle errors in Python services?
- How do you write maintainable Python code?
- What are decorators?
- What are generators?
- What is the difference between list, tuple, set, and dictionary?
- What is the difference between shallow copy and deep copy?
- What is the Python GIL?
- How do you manage dependencies in Python?
- How do you handle environment variables and secrets?

---

#### Python Error Handling Example

```python
def get_order(order_id: int) -> dict:
    try:
        order = order_repository.find_by_id(order_id)

        if order is None:
            raise ValueError(f"Order {order_id} not found")

        return order

    except ValueError:
        raise

    except Exception as exc:
        logger.exception("Unexpected error while fetching order", extra={"order_id": order_id})
        raise RuntimeError("Unable to fetch order right now") from exc
```

##### Interview Explanation

- Use specific exceptions for known business cases.
- Log unexpected errors with context.
- Do not expose internal errors directly to users.
- Preserve the original exception using `from exc`.

### Fan-Out / Fan-In I/O Aggregation

A common backend/dashboard problem is:

```text
request arrives
   ↓
start several independent I/O operations
   ↓
wait until the required operations finish
   ↓
combine results
   ↓
build one response/dashboard
```

If seven independent calls each take roughly one second, running them sequentially can take roughly seven seconds. Concurrent execution is closer to the duration of the slowest required call, plus aggregation overhead.

#### Async-compatible I/O: `asyncio.gather()`

```python
import asyncio

async def fetch_source(name: str) -> dict[str, str]:
    await asyncio.sleep(1)  # stand-in for async network/database I/O
    return {name: f"data_from_{name}"}

async def build_dashboard() -> dict[str, str]:
    tasks = [fetch_source(f"source_{i}") for i in range(1, 8)]
    results = await asyncio.gather(*tasks)

    combined: dict[str, str] = {}
    for result in results:
        combined.update(result)
    return combined
```

Use this when the underlying clients are async-compatible. `asyncio.gather()` is a fan-out/fan-in primitive: schedule independent work, await the group, then aggregate.

If partial results are acceptable, failure policy must be explicit rather than accidental:

```python
results = await asyncio.gather(*tasks, return_exceptions=True)
successful = [result for result in results if not isinstance(result, Exception)]
```

For stricter structured concurrency, modern Python also provides `asyncio.TaskGroup`; failure of one child task can cancel sibling tasks according to the task-group semantics.

#### Blocking I/O: `ThreadPoolExecutor`

When the libraries are synchronous/blocking, a thread pool is often the cleanest adapter:

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_source(name: str) -> dict[str, str]:
    # stand-in for a blocking API/DB/file call
    return {name: f"data_from_{name}"}

sources = [f"source_{i}" for i in range(1, 8)]
results: list[dict[str, str]] = []

with ThreadPoolExecutor(max_workers=7) as executor:
    futures = [executor.submit(fetch_source, source) for source in sources]
    for future in as_completed(futures):
        results.append(future.result())
```

Interview explanation:

> If the operations are independent and I/O-bound, I would fan them out concurrently, wait for the required results, then fan them back in through an aggregation step. I would use `asyncio` when the libraries are async-native and a bounded thread pool when they are blocking. For production I would also define timeouts, partial-failure behavior, concurrency limits, and downstream rate-limit protection.

Important nuance: threads/async tasks provide **concurrency** for I/O. Calling this "parallel" is common conversationally, but CPU-bound Python parallelism generally requires processes or native code that releases the GIL.

---

## Focused Python Semantics and Debugging Drills

These short questions test whether a candidate can reason about Python execution rather than only recall syntax.

### Iterator Consumption

An iterator keeps traversal state. Calling `next()` consumes one item, so a later loop starts from the following item.

```python
values = iter([10, 20, 30])

print(next(values))
for value in values:
    print(value)
```

Output:

```text
10
20
30
```

The loop does not restart the iterator.

### Generator Exhaustion

A generator expression is also a one-pass iterator.

```python
gen = (number * number for number in range(3))

print(list(gen))
print(list(gen))
```

Output:

```text
[0, 1, 4]
[]
```

Create a new generator when the sequence must be traversed again, or materialize it once into a list when the data is small enough.

### Missing Dictionary Keys

Direct indexing raises `KeyError` when the key is absent:

```python
role = user_roles[username]
```

Choose behavior explicitly:

```python
role = user_roles.get(username)  # returns None when missing
role = user_roles.get(username, "guest")

if username in user_roles:
    role = user_roles[username]
```

Use indexing when absence is an error. Use `.get()` when a default or optional result is part of the contract.

### Stacked Decorator Order

Decorators are applied from the bottom upward but execute from the outer wrapper inward.

```python
def first(func):
    def wrapper():
        print("first")
        func()
    return wrapper

def second(func):
    def wrapper():
        print("second")
        func()
    return wrapper

@first
@second
def greet():
    print("hello")
```

The definition is equivalent to:

```python
greet = first(second(greet))
```

Calling `greet()` prints:

```text
first
second
hello
```

### Preserving Decorated Function Metadata

Without `functools.wraps`, the decorated function exposes the wrapper's name and documentation.

```python
from functools import wraps

def log_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
```

`@wraps(func)` preserves metadata such as `__name__`, `__doc__`, annotations, and the `__wrapped__` reference used by inspection tools.

### Context Manager Lifecycle

A `with` statement calls `__enter__` before the block and `__exit__` when the block finishes.

```python
class Resource:
    def __enter__(self):
        print("Open")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Close")

with Resource():
    print("Working")
```

Output:

```text
Open
Working
Close
```

`__exit__` also runs when the block raises an exception. Returning a truthy value from `__exit__` suppresses that exception; returning `False` or `None` allows it to propagate.

### Frozen Dataclasses

A frozen dataclass prevents normal field reassignment after construction.

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class User:
    name: str

user = User("Maya")
user.name = "Brian"  # dataclasses.FrozenInstanceError
```

Use frozen dataclasses for value objects whose identity should not change after creation.

### Metaclass Registration Timing

A metaclass can register subclasses when their class bodies are executed.

```python
class Registry(type):
    registered: list[str] = []

    def __new__(mcls, name, bases, namespace):
        cls = super().__new__(mcls, name, bases, namespace)
        if name != "Plugin":
            mcls.registered.append(name)
        return cls

class Plugin(metaclass=Registry):
    pass

class Logger(Plugin):
    pass

class Cache(Plugin):
    pass
```

`Registry.registered` becomes `['Logger', 'Cache']` at class-definition time. No instances are required. This pattern appears in plugin systems, serializers, command registries, and framework extension points.

### Shared Mutable Class Attributes

A mutable class attribute is shared by every instance:

```python
class User:
    active = []

    def __init__(self, name):
        self.active.append(name)
```

After creating `User("Maya")` and `User("Ethan")`, both instances observe:

```text
['Maya', 'Ethan']
```

Use an instance attribute for per-object state:

```python
class User:
    def __init__(self, name):
        self.active = [name]
```

### Type Hints Do Not Enforce Runtime Types

Python annotations support readers, IDEs, linters, and static type checkers, but Python does not reject mismatched arguments automatically.

```python
def add_tax(amount: int) -> int:
    return amount + 5

print(add_tax(True))  # 6
```

`bool` is a subclass of `int`, so `True` behaves numerically like `1`. Use runtime validation when an API contract must reject such values.

### Tuple Unpacking Arity

The number of targets must match the number of returned values unless starred unpacking is used.

```python
def profile():
    return "Alice", 25, "Chicago"

name, age = profile()  # ValueError: too many values to unpack
```

Valid alternatives:

```python
name, age, city = profile()
name, *details = profile()
```

### Restricting Attributes with `__slots__`

`__slots__` declares the allowed instance attributes and can reduce per-object memory overhead when many objects are created.

```python
class User:
    __slots__ = ("name",)

    def __init__(self, name):
        self.name = name

user = User("Maya")
user.email = "maya@example.com"  # AttributeError
```

Add `email` to `__slots__` or remove slots when dynamic attributes are required.

### Property-Based Validation

A property keeps attribute-style access while centralizing validation.

```python
class Account:
    def __init__(self, balance: float):
        self._balance = balance

    @property
    def balance(self) -> float:
        return self._balance

    @balance.setter
    def balance(self, value: float) -> None:
        if value < 0:
            raise ValueError("Balance cannot be negative")
        self._balance = value
```

This is useful when an object's invariants must be enforced without exposing internal storage directly.

### Quick Interview Checklist

- State whether an object is reusable or one-shot.
- Distinguish class-level state from instance-level state.
- Explain when framework hooks run: definition time, construction time, or call time.
- Mention the exact exception when the question asks for output or failure behavior.
- Separate static type checking from runtime validation.

---

## Frequency Aggregation, Top-K Selection & Streaming Follow-Ups

A common interview progression is to start with a frequency map, then ask whether sorting every unique value is still appropriate when only a very small top-k result is required.

### Baseline: Count Then Sort

For `n` total events and `u` unique values:

```python
def top_k_by_sort(values, k):
    counts = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1

    ranked = sorted(counts, key=lambda value: (-counts[value], value))
    return ranked[:k]
```

Complexity:

- Counting: `O(n)`.
- Sorting unique values: `O(u log u)`.
- Total: `O(n + u log u)`.
- Frequency storage: `O(u)`.

The important interview distinction is that `n`, `u`, and `k` can be very different orders of magnitude. If millions of events collapse to a few unique values, sorting is cheap. If `u` is huge and `k` is tiny, sorting every unique value does unnecessary work.

### Small `k`: Min-Heap of Size `k`

After counting, keep only the best `k` candidates in a min-heap. The root represents the weakest retained candidate.

```text
count all events        O(n)
scan u unique values    O(u log k)
final ordering          O(k log k)
```

Overall:

```text
O(n + u log k)
```

This is better than `O(n + u log u)` when `k << u`.

**Why `heapq`?**

> A min-heap of size `k` keeps the weakest current top-k candidate at the root. For each new unique value, I either ignore it or replace that root in `O(log k)`. That avoids sorting all `u` unique values when I only need a small prefix.

### Special Case: `k = 1`

A heap is unnecessary. After counting, scan the frequency map once and keep the current maximum.

```text
O(n + u) time
O(u) frequency storage
```

This is a useful follow-up because it shows that the data structure should match the requested result size rather than being applied mechanically.

### Dynamic `k`

A fixed size-`k` heap discards candidates. If a later query asks for a larger `k`, those discarded values are no longer available in the heap.

Choose based on the query pattern:

|                         Situation                          |                         Better Approach                         |
| ---------------------------------------------------------- | --------------------------------------------------------------- |
| One query with small fixed `k`                             | Frequency map + size-`k` min-heap                               |
| Many queries over the same static data with changing `k`   | Count once, sort all unique values once, return cached prefixes |
| Stream of updates with occasional arbitrary `k` queries    | Maintain running counts; build size-`k` heap at query time      |
| Stream with very frequent top-k reads                      | Maintain counts plus an ordered ranking index                   |
| Unique cardinality is too large for exact in-memory counts | Approximate heavy hitters such as Count-Min Sketch              |

### Streaming Variant

For an unbounded stream, the original input list is unavailable. The minimum exact state is a running frequency map:

```python
counts[path] = counts.get(path, 0) + 1
```

At any point, an arbitrary `top_k(k)` query can scan the current `u` counts and keep a size-`k` heap. That gives:

- Update: `O(1)` average per event.
- Query: `O(u log k)`.
- Exact state: `O(u)`.

If top-k queries are very frequent, maintain a secondary ordered index keyed by frequency and deterministic tie-break. That makes updates more expensive, typically `O(log u)`, but can make top-k reads close to `O(k)`.

For distributed streams:

- Partition by a stable hash of the key/path.
- Maintain local counts/state.
- Checkpoint consumer offsets and state.
- Make replay idempotent.
- Define window semantics explicitly: all-time, tumbling, sliding, or session window.
- Merge partition-level candidates or counts at the aggregation layer.

If exact `O(u)` state is not feasible, use an approximate heavy-hitter algorithm and state the accuracy/memory trade-off explicitly.

**Interview answer:**

> I would separate total events `n`, unique values `u`, and requested results `k`. The simple solution is a frequency map plus sorting, which is `O(n + u log u)`. If `u` is large and `k` is small, I would keep a min-heap of size `k`, reducing selection to `O(u log k)`. If `k` changes dynamically, a fixed heap is not enough because it discarded candidates, so for static data I would sort once and reuse the ranking, while for a stream I would keep running counts and compute or maintain the ranking based on query frequency.

See `coding_questions/top_k_frequent_paths.py` for runnable batch, heap, dynamic-k, and streaming examples.

---

## Loop Progress Invariants in Grouped Simulations

Nested loops over sorted groups are easy to make accidentally non-terminating. This came up in a priority-allocation exercise where records were grouped by bid and processed in timestamp order.

### The Core Invariant

Every loop must make measurable progress toward its exit condition.

Bad pattern:

```python
group_end = index

while group_end < index and rows[group_end].bid == bid:
    ...
```

`group_end < index` is false immediately because both variables start equal. A different typo can be worse: the loop condition may remain true while the variable used in that condition never changes, causing a timeout.

Safer grouped scan:

```python
group_end = group_start

while group_end < len(rows) and rows[group_end].bid == bid:
    group_end += 1

# Outer pointer advances exactly once after the group is complete.
group_start = group_end
```

Keep responsibilities separate:

- `group_start` identifies the beginning of the current group.
- `group_end` discovers the first record after that group.
- The inner loop advances `group_end` only.
- The outer loop advances `group_start` only after the group decision is complete.
- Prefer descriptive state names such as `group_start`, `group_end`, and `remaining_inventory` when several indices or counters coexist; short names are fine only when the scope and role are obvious.

### Optimize for the Required Output

If the question asks only which customers received **zero** items, a literal one-item-per-round simulation may be unnecessary. After sorting by priority, group-level arithmetic can often determine who receives at least one item without iterating once per allocated item.

That changes a potentially inventory-dependent simulation into a sort-and-scan solution:

```text
O(total_inventory) style simulation
        ↓
O(n log n) sort + O(n) group scan
```

**Interview answer:**

> When I use multiple pointers, I define the progress invariant explicitly before coding: which pointer each loop owns, what must change on every iteration, and what state transition advances the outer loop. For large-quantity simulations I also ask whether the requested output can be derived at group level so runtime depends on the number of records rather than the number of individual units processed.

See `coding_questions/inventory_bid_allocation.py` for the optimized allocation exercise.

---

## Senior Python Concurrency & Thread-Safety Interview Guide

This section focuses on the follow-up style common in senior coding rounds: implement a correct stateful data structure, then make it thread-safe, discuss contention, and explain how the design changes when moved across processes or machines.

### Concurrency vs Parallelism

- **Concurrency:** multiple tasks make progress during overlapping time periods.
- **Parallelism:** multiple tasks literally execute at the same time on different CPU cores/processors.

A Python program can be highly concurrent even when CPython's GIL limits parallel execution of Python bytecode in one process.

---

### What Is the GIL?

CPython's Global Interpreter Lock allows only one thread at a time to execute Python bytecode within a process.

Important consequences:

- CPU-bound pure-Python threads usually do not scale linearly across cores.
- Threads are still useful for I/O-bound work because waiting threads can release control while another thread runs.
- Many blocking I/O operations and C extensions release the GIL.
- The GIL does **not** make arbitrary shared state logically thread-safe.

Strong interview answer:

> The GIL limits simultaneous execution of Python bytecode in CPython, but it does not protect multi-step application invariants. A read-modify-write sequence or a dictionary plus linked-list invariant can still be interleaved across threads, so I still need synchronization around shared mutable state.

---

### Threading vs Multiprocessing vs AsyncIO

|   Model   |                            Best Fit                            |                          Key Trade-Off                          |
| --------- | -------------------------------------------------------------- | --------------------------------------------------------------- |
| Threads   | Blocking/I/O-bound work, legacy sync libraries                 | Shared-memory synchronization and GIL for CPU-heavy Python code |
| Processes | CPU-bound Python work requiring true parallelism               | Serialization, IPC, higher memory/process overhead              |
| `asyncio` | Many concurrent I/O operations with async-compatible libraries | Cooperative model; blocking calls must not run on event loop    |

Interview line:

> I choose the concurrency model from the workload. Threads and asyncio are strong for I/O concurrency, while processes are more appropriate when CPU-bound Python work needs parallel execution across cores.

---

### Race Condition

A race condition occurs when correctness depends on unpredictable operation interleaving.

Conceptually, this is not one indivisible operation:

```text
counter += 1

read counter
add 1
write counter
```

Possible interleaving:

```text
Thread A reads 5
Thread B reads 5
Thread A writes 6
Thread B writes 6
```

Expected: 7. Actual: 6.

Protect the shared invariant using appropriate synchronization.

---

### `threading.Lock`

A mutex permits one thread at a time inside the protected critical section.

```python
import threading

class Counter:
    def __init__(self):
        self._value = 0
        self._lock = threading.Lock()

    def increment(self):
        with self._lock:
            self._value += 1

    def value(self):
        with self._lock:
            return self._value
```

Start with correctness. Keep the critical section as small as practical, but do not split one logical invariant across multiple unsynchronized operations.

---

### `RLock`

`RLock` is reentrant: the same thread can acquire it multiple times before releasing it the same number of times.

Use it when reentrant acquisition is actually part of the design, for example:

```text
public synchronized method
   ↓
calls another synchronized method
   ↓
same thread needs same lock again
```

Strong interview answer:

> I prefer a normal Lock unless reentrancy is required. RLock can be useful when synchronized methods call each other, but using it everywhere can hide accidental recursive lock acquisition.

---

### Semaphore

A semaphore permits up to N concurrent holders rather than exactly one.

Examples:

```text
allow at most 10 concurrent DB-heavy tasks
allow at most 20 outbound API calls
limit parallel downloads
```

```python
import asyncio

semaphore = asyncio.Semaphore(10)

async def call_service(client, url):
    async with semaphore:
        return await client.get(url)
```

A semaphore controls concurrency; it does not by itself protect a complex shared-state invariant.

---

### Condition Variable

A condition variable lets threads wait for a state predicate while temporarily releasing a lock.

Typical bounded queue predicates:

```text
producer waits while queue is full
consumer waits while queue is empty
```

Always re-check the predicate in a `while` loop:

```python
with condition:
    while not predicate():
        condition.wait()
```

Why `while`, not `if`?

- Condition waits can wake spuriously.
- Another thread can change the state before this thread reacquires the lock.

---

### Thread-Safe Queue

Python's `queue.Queue` is the default production answer when the problem simply needs a synchronized producer/consumer queue.

If the interview asks you to implement one, use:

- `deque` for O(1) append/popleft
- one lock
- `not_empty` condition
- `not_full` condition for bounded capacity

See `coding_questions/concurrent_data_structures.py` for a runnable implementation.

---

### Deadlock

Classic example:

```text
Thread 1: acquire A → waits for B
Thread 2: acquire B → waits for A
```

Both wait forever.

Practical defenses:

- Consistent global lock ordering
- Avoid unnecessary nested locks
- Keep lock scope small
- Use timeouts where appropriate
- Avoid calling unknown/external code while holding a lock

Interview explanation:

> If multiple locks are necessary, I define one acquisition order and enforce it everywhere. That removes the circular-wait pattern that commonly causes deadlocks.

---

### Coarse-Grained vs Fine-Grained Locking

#### Coarse-grained

One lock protects the complete logical state.

Advantages:

- Simple
- Easier to prove correct
- Lower deadlock risk

Disadvantage:

- More contention

#### Fine-grained

Different locks protect independent state partitions.

Advantages:

- More concurrency

Disadvantages:

- More complex invariants
- Lock-ordering concerns
- Harder multi-key operations

Senior interview pattern:

> I would first protect the whole invariant with one lock. If profiling shows lock contention is material, I would consider partitioning/sharding the state or reducing critical-section work rather than prematurely introducing fine-grained locking.

---

### Lock Sharding

For independent key-based operations:

```python
lock = locks[hash(key) % len(locks)]
```

This lets operations on different shards proceed concurrently.

Trade-offs:

- Collisions still serialize unrelated keys.
- Multi-key operations become more complex.
- Global ordering/eviction policies may still need centralized synchronization.

---

### Why LRU `get()` Is Not Really Read-Only

An LRU cache maintains recency ordering.

```text
get(key)
   ↓
lookup value
   ↓
move node to most-recent position
```

So `get()` mutates shared state and must participate in the synchronization strategy.

The LRU invariant spans both:

```text
hash map
+
doubly linked list ordering
```

A strong first implementation protects both under one lock.

---

### TTL / Expiring Map Design

A map may store:

```text
key -> (value, expiry)
```

and an ordered expiration structure.

#### Fixed TTL with insertion-ordered expiry

A deque can work because expiration order matches insertion order.

#### Arbitrary TTL per key

Use a min-heap:

```text
(expiration_time, key)
```

Heap operations cost O(log n).

#### Stale expiration metadata

If key A is overwritten:

```text
put A with expiry 10
put A with expiry 20
```

the old expiry entry must not delete the new value. Compare the queued expiry/version to the map's current expiry/version before deleting.

This is a useful general pattern: secondary index entries can become stale after an overwrite, so validate them against authoritative current state before acting.

---

### Bounded Blocking Queue

Requirements:

```text
put(item) waits when full
take() waits when empty
fixed capacity
```

Core structure:

```text
deque
lock
not_empty condition
not_full condition
```

Producer:

```text
while full:
    wait on not_full
append item
notify not_empty
```

Consumer:

```text
while empty:
    wait on not_empty
popleft item
notify not_full
```

This also demonstrates **backpressure**: producers cannot create unbounded queued work when consumers are slower.

---

### Rate Limiter Evolution

#### Fixed window

Simple per-key counter keyed by time bucket.

Problem: boundary bursts.

```text
100 requests at 12:00:59
100 requests at 12:01:00
```

The client can generate 200 requests in roughly one second despite a nominal 100/minute limit.

#### Sliding-window log

Store recent timestamps, often in a deque/sorted structure.

- More accurate
- More state per key

#### Token bucket

Maintain:

```text
bucket capacity = allowed burst
refill rate     = sustained rate
```

Token bucket is a strong practical design when controlled bursts are acceptable.

#### Concurrent limiter

A single lock is the simplest correctness baseline. If contention is high, shard locks/state by key.

#### Distributed limiter

Local process counters cannot enforce one global limit across many API servers.

Options:

- Central/partitioned atomic counter store
- Redis atomic script/operation
- Allocate local token budgets from a global quota

Trade-off:

> Centralized exact state adds a network dependency; local quotas scale better but can become approximate.

---

### Task Scheduler

For:

```text
schedule(task, execution_time)
get next due task
```

use a min-heap ordered by execution time.

```text
schedule: O(log n)
peek next due: O(1)
pop: O(log n)
```

Concurrency follow-ups:

- A producer inserts an earlier task while a worker sleeps.
- Worker must be notified to recompute its wait duration.
- Duplicate execution after crash/retry.
- Durable scheduling across process restart.

Distributed extension:

```text
durable task table
   ↓
conditional lease claim
   ↓
worker
   ↓
heartbeat / completion
```

---

### Optimistic vs Pessimistic Concurrency

#### Optimistic

Assume conflicts are uncommon. Detect them at write time.

Example:

```sql
UPDATE job
SET state = 'RUNNING',
    version = version + 1
WHERE id = :id
  AND state = 'QUEUED'
  AND version = :expected_version;
```

`0 rows affected` means another actor changed the state first.

Good for:

- Short transactions
- Low/moderate conflict
- High read concurrency

#### Pessimistic

Lock before making the change.

Good when:

- Conflict is frequent
- Exclusive ownership is necessary
- The critical operation is short

Trade-offs:

- Blocking
- Deadlocks
- Reduced concurrency

---

### Testing Concurrent Code

Useful strategies:

- Many threads writing the same key/counter.
- Readers and writers operating simultaneously.
- Independent keys to verify concurrency does not corrupt shared metadata.
- Barriers/events to intentionally align threads around a suspected race.
- Repeated stress runs rather than one execution.
- Assert invariants after all workers finish.
- Validate capacity never exceeds its limit.
- Validate every produced queue item is consumed exactly as the test contract expects.
- Use race/thread-sanitizer tooling where the language/runtime supports it.

Do not rely only on `sleep()` to “make the race happen”; that creates fragile tests.

---

### Quick Concurrency Interview Questions

#### Does the GIL make Python data structures thread-safe?

No. Some individual CPython operations may appear atomic today, but application-level multi-step invariants still require synchronization. Do not build correctness on implementation accidents.

#### Why use deque instead of list for FIFO?

`deque.popleft()` is O(1); `list.pop(0)` is O(n) because elements shift.

#### Why not use one lock per key everywhere?

Lock lifecycle, eviction, multi-key operations, and global invariants become more complicated. Start coarse, measure contention, then partition when justified.

#### Could LRU `get()` be lock-free?

Not in the straightforward design because it mutates recency ordering. A specialized approximate/concurrent cache could relax this, but that changes semantics and complexity.

#### What is starvation?

A thread/task waits indefinitely because other contenders repeatedly acquire the required resource even though the system as a whole continues making progress.

#### What is contention?

Multiple workers frequently compete for the same synchronization/resource, reducing parallel progress and increasing latency.
