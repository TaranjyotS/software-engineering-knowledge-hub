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

The section below is merged from the previously organized topic-wise interview-prep pack so the repository keeps the detailed technical Q&A in one place.

> Python fundamentals, data structures, decorators, generators, exception handling, GIL, threading, multiprocessing, asyncio, performance, and coding exercises.

### Topic Sections

1. Python Internals & Concurrency — `Interview_Prep_Topics_and_Questions.md`
2. Python Topics — `ai_engineer_interview_prep_topics.md`
3. Python Core Topics — `deloitte_python_genai_interview_prep_topics.md`
4. Python Fundamentals — `interview_prep_python_rest_fastapi_genai.md`
5. Python Operators & Expressions — `interview_prep_python_rest_fastapi_genai.md`
6. Lists, Tuples, and Sets — `interview_prep_python_rest_fastapi_genai.md`
7. Python Functions, Decorators, and Generators — `interview_prep_python_rest_fastapi_genai.md`
8. Exception Handling — `interview_prep_python_rest_fastapi_genai.md`
9. Concurrency in Python — `interview_prep_python_rest_fastapi_genai.md`
10. Coding Interview Practice Topics — `interview_prep_python_rest_fastapi_genai.md`
11. Python Core Concepts — `interview_questions_topics_technical_prep.md`
12. Python Coding Problems and Algorithms — `interview_questions_topics_technical_prep.md`
13. Python — `ML_AI_Systems_Interview_Prep_Handbook.md`
14. Python Engineering — `Interview_Topics_and_Technical_Prep.md`

---

### 4. Python Internals & Concurrency
#### 4.1 Python GIL

**Interview answer:**

> The Global Interpreter Lock, or GIL, is a mechanism in CPython that allows only one thread to execute Python bytecode at a time inside a process. It simplifies memory management but limits true parallelism for CPU-bound multithreaded workloads. For I/O-bound tasks like API calls or database queries, threads or asyncio still work well because they spend most of their time waiting. For CPU-bound work, multiprocessing is usually better.

---

#### 4.2 Threading vs Multiprocessing vs AsyncIO

| Approach        | Best For              | Notes                                                        |
| --------------- | --------------------- | ------------------------------------------------------------ |
| Threading       | Simple I/O-bound work | Shared memory, affected by GIL for CPU work                  |
| Multiprocessing | CPU-bound work        | Separate processes, avoids GIL limits                        |
| AsyncIO         | High-concurrency I/O  | Single-threaded event loop, efficient for many network calls |

**Interview answer:**

> I choose based on workload. For many API calls or LLM requests, I use asyncio with an async HTTP client and semaphores for rate limits. For CPU-heavy tasks, I use multiprocessing. Threading is useful for simpler I/O tasks, but not ideal for CPU-bound computation because of the GIL.

---

#### 4.3 AsyncIO with rate limiting

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

---

#### 4.4 Semaphore

**Interview answer:**

> A semaphore controls how many tasks can run concurrently. In an LLM application, I might allow only 10 simultaneous API requests to avoid hitting provider rate limits or overwhelming downstream services.

---

#### 4.5 Retry Strategy

For API or LLM failures:

- Retry transient 5xx errors
- Use exponential backoff
- Add jitter
- Set max retry count
- Use timeouts
- Add circuit breaker for repeated failures
- Fallback to another model/service if needed

---

### 15. Python Topics
#### 15.1 Why Use Generators in AI Pipelines?

> "Generators help process large datasets efficiently by producing one item at a time instead of loading everything into memory."

#### 15.2 Generator Example

```python
def read_documents(file_paths):
    for path in file_paths:
        with open(path, "r", encoding="utf-8") as file:
            yield file.read()

for document in read_documents(["doc1.txt", "doc2.txt"]):
    print(document[:100])
```

#### 15.3 AI Pipeline Use Case

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

#### 15.4 Benefits of Generators

- Memory efficient
- Good for large files
- Useful for streaming data
- Improves scalability
- Works well for ETL pipelines
- Useful for document chunking
- Prevents loading everything into RAM

#### 15.5 Strong Interview Line

> "I use generators in AI pipelines to stream large datasets, documents, logs, or chunks one item at a time, which improves memory efficiency and scalability."

---

### 4. Python Core Topics

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

### 1. Python Fundamentals
#### 1.1 What is the difference between a tuple and a set?
##### Interview Answer

A **tuple** is an ordered, immutable collection that allows duplicates.
A **set** is an unordered collection that stores only unique elements.

| Feature           | Tuple         | Set                              |
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

#### 1.2 Write a list comprehension to find squares from 1 to 5
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

### 2. Python Operators & Expressions
#### 2.1 What is the output of `2**3**2`?
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

#### 2.2 What is the output of `a | b` when `a = 4` and `b = 11`?
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

### 3. Lists, Tuples, and Sets
#### 3.1 What does `seta ^ setb` mean?
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

#### 3.2 Different ways to join two lists
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

#### 3.3 Difference between `append()` and `extend()`
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

#### 3.4 What happens when we multiply a list by 2?
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

#### 3.5 Character list multiplication
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

### 4. Python Functions, Decorators, and Generators
#### 4.1 What are decorators in Python?
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

#### 4.2 What is a generator in Python?
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

#### 4.3 Difference between `yield` and `return`

| `return`                         | `yield`                      |
| -------------------------------- | ---------------------------- |
| Ends function execution          | Pauses function execution    |
| Returns full result at once      | Produces one value at a time |
| More memory usage for large data | Memory efficient             |
| Function state is lost           | Function state is preserved  |

---

#### 4.4 When should we use `yield` and when should we use `return`?
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

### 5. Exception Handling
#### 5.1 When does the `finally` block execute?
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

---

### 6. Concurrency in Python
#### 6.1 What is the GIL?
##### Answer

GIL stands for **Global Interpreter Lock**.

It is a mechanism in CPython that allows only one thread to execute Python bytecode at a time within a process.

---

##### Why does Python have GIL?

The GIL simplifies:

- Memory management
- Thread safety of Python objects
- Reference counting

---

##### Important Effect

Even if we create multiple threads, only one thread can execute Python bytecode at a time in CPython.

---

#### 6.2 Is multithreading useless because of GIL?

No.

Multithreading is still useful for **I/O-bound tasks**, such as:

- API calls
- Database queries
- File operations
- Network requests
- External LLM calls

While one thread waits for I/O, another thread can run.

---

#### 6.3 Why is multiprocessing better for CPU-heavy tasks?

For CPU-heavy tasks, threads compete for the GIL.

Examples:

- Image processing
- ML computation
- Mathematical calculations
- Large data transformations

Multiprocessing creates separate processes with separate Python interpreters, so it bypasses the GIL.

---

#### 6.4 Multithreading vs Multiprocessing

| Multithreading                  | Multiprocessing                |
| ------------------------------- | ------------------------------ |
| Multiple threads in one process | Multiple independent processes |
| Shared memory                   | Separate memory                |
| Lightweight                     | Heavier                        |
| Good for I/O-bound tasks        | Good for CPU-bound tasks       |
| Affected by GIL                 | Bypasses GIL                   |

---

##### Multithreading Example

```python
import threading

def task():
    print("Running thread")

t1 = threading.Thread(target=task)
t1.start()
t1.join()
```

---

##### Multiprocessing Example

```python
from multiprocessing import Process

def task():
    print("Running process")

p = Process(target=task)
p.start()
p.join()
```

---

##### Strong Interview Answer

> Multithreading is mainly useful for I/O-bound concurrency, while multiprocessing is better for CPU-bound parallel execution because it bypasses Python’s GIL by running separate processes.

---

### 13. Coding Interview Practice Topics

These topics were discussed as likely coding interview preparation areas.

#### 13.1 Arrays and strings

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

#### 13.2 Hash maps

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

#### 13.3 Sliding window

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

#### 13.4 Stack

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

#### 13.5 Linked list

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

#### 13.6 Trees

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

#### 13.7 SQL topics

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
#### 10.1 Threading, multiprocessing, asyncio, and GIL
##### GIL

The Global Interpreter Lock allows only one thread to execute Python bytecode at a time in CPython.

##### Threading

Best for I/O-bound tasks.

```python
import threading

def fetch():
    print("I/O task")

thread = threading.Thread(target=fetch)
thread.start()
thread.join()
```

##### Multiprocessing

Best for CPU-bound tasks.

```python
from multiprocessing import Pool

def square(x):
    return x * x

with Pool() as pool:
    print(pool.map(square, [1, 2, 3]))
```

##### AsyncIO

Best for high-concurrency I/O with async libraries.

```python
import asyncio

async def fetch():
    await asyncio.sleep(1)
    return "done"

asyncio.run(fetch())
```

---

#### 10.2 Mutable vs immutable objects
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

#### 10.3 List vs tuple
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

#### 10.4 Dictionary keys

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

#### 10.5 Class variables vs instance variables

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

#### 10.6 Instance method, class method, static method

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

---

#### 10.7 Decorators and custom decorators
##### Simple decorator

```python
def log_call(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log_call
def greet(name):
    return f"Hello {name}"
```

##### Flask/FastAPI-like use case

- Authentication.
- Authorization.
- Logging.
- Timing.
- Validation.

---

#### 10.8 `*args` and `**kwargs`

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

#### 10.9 `==` vs `is`
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

#### 10.10 Exceptions, multiple except blocks, and finally

```python
try:
    result = 10 / x
except ZeroDivisionError:
    print("division by zero")
except TypeError:
    print("wrong type")
finally:
    print("always runs")
```

##### Important behavior

`finally` runs even if `return` occurs in `try`.

```python
def test():
    try:
        return "try"
    finally:
        print("finally still runs")
```

---

#### 10.11 Mutable default argument bug
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

#### 10.12 Lists, sets, and dicts for membership/deduplication
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

### Python

Python is likely to come up because it is central to AI/ML, backend development, data processing, and automation.

---

#### Python GIL
##### Interview Question

**What is the Python GIL?**

##### Answer

The **Global Interpreter Lock (GIL)** is a lock in CPython that allows only one thread to execute Python bytecode at a time.

This means Python threads are not ideal for CPU-heavy parallel computation, because multiple threads cannot truly execute Python bytecode in parallel.

##### When It Matters

| Task Type            | Best Approach                                                 |
| -------------------- | ------------------------------------------------------------- |
| CPU-bound tasks      | Multiprocessing                                               |
| I/O-bound tasks      | Threading or AsyncIO                                          |
| Network calls        | AsyncIO                                                       |
| File/database calls  | Threading or AsyncIO                                          |
| Heavy ML computation | NumPy/PyTorch/TensorFlow native operations or multiprocessing |

##### Sample Answer

```text
The GIL prevents multiple native Python threads from executing Python bytecode simultaneously. For I/O-bound tasks, threading can still help because threads release the GIL while waiting for external operations. But for CPU-bound workloads, multiprocessing is usually better because each process has its own Python interpreter and memory space.
```

---

#### Threading vs Multiprocessing vs AsyncIO
##### Interview Question

**When would you use threading, multiprocessing, or AsyncIO?**

##### Comparison Table

| Approach        | Best For             | Example                                   |
| --------------- | -------------------- | ----------------------------------------- |
| Threading       | I/O-bound tasks      | Reading files, calling APIs               |
| Multiprocessing | CPU-bound tasks      | Image processing, heavy computation       |
| AsyncIO         | High-concurrency I/O | Thousands of API calls, async web servers |

##### Threading Example

```python
import threading
import requests

def fetch_url(url: str) -> None:
    response = requests.get(url, timeout=10)
    print(url, response.status_code)

urls = [
    "https://example.com",
    "https://example.org",
]

threads = []

for url in urls:
    thread = threading.Thread(target=fetch_url, args=(url,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
```

##### Multiprocessing Example

```python
from multiprocessing import Pool

def square(number: int) -> int:
    return number * number

if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5]

    with Pool(processes=4) as pool:
        results = pool.map(square, numbers)

    print(results)
```

##### AsyncIO Example

```python
import asyncio
import aiohttp

async def fetch(session: aiohttp.ClientSession, url: str) -> str:
    async with session.get(url) as response:
        return await response.text()

async def main() -> None:
    urls = [
        "https://example.com",
        "https://example.org",
    ]

    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        results = await asyncio.gather(*tasks)

    print(len(results))

asyncio.run(main())
```

---

#### Decorators
##### Interview Question

**What is a decorator in Python?**

##### Answer

A decorator is a function that wraps another function to extend or modify its behavior without changing the original function code.

##### Common Uses

- Logging
- Authentication
- Authorization
- Caching
- Timing
- Retry logic
- Monitoring

##### Code Example

```python
from functools import wraps
from time import perf_counter

def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        end = perf_counter()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

@timing_decorator
def process_data():
    return sum(range(1_000_000))

print(process_data())
```

##### Interview Tip

Mention `functools.wraps` because it preserves the original function's metadata.

---

#### Generators
##### Interview Question

**What is a generator in Python?**

##### Answer

A generator is a function that uses `yield` to return values lazily one at a time instead of storing everything in memory.

##### Why Generators Are Useful

- Memory efficient
- Good for streaming data
- Useful for large files
- Helpful in data pipelines

##### Code Example

```python
def read_large_file(file_path: str):
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            yield line.strip()

for row in read_large_file("data.txt"):
    print(row)
```

##### `yield` vs `return`

| Keyword  | Behavior                                |
| -------- | --------------------------------------- |
| `return` | Ends the function and returns one value |
| `yield`  | Pauses the function and resumes later   |

---

#### Try, Except, Finally
##### Interview Question

**When does the finally block execute?**

##### Answer

The `finally` block executes regardless of whether an exception occurs or not. It is commonly used for cleanup operations.

##### Code Example

```python
def read_file(path: str) -> None:
    file = None

    try:
        file = open(path, "r", encoding="utf-8")
        print(file.read())
    except FileNotFoundError:
        print("File not found")
    finally:
        if file:
            file.close()
        print("Cleanup completed")
```

##### Important Point

Even if there is a `return` inside `try` or `except`, `finally` usually still executes before the function exits.

---

#### Python Memory and Performance
##### Interview Question

**How would you improve Python performance?**

##### Answer

Possible approaches:

- Use efficient data structures
- Avoid unnecessary loops
- Use generators for large data
- Use NumPy/Pandas vectorization
- Use multiprocessing for CPU-bound tasks
- Cache repeated computations
- Profile before optimizing

##### Example: Caching

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

### 4. Python Engineering
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

---

#### Decorator Example

```python
import time
from functools import wraps

def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        print(f"{func.__name__} took {duration:.2f}s")
        return result
    return wrapper


@measure_time
def process_orders():
    # expensive operation
    return "done"
```

##### When to Use Decorators

Use decorators for cross-cutting concerns such as:

- Logging
- Timing
- Authentication
- Authorization
- Retry logic
- Caching

---

#### Generator Example

```python
def stream_order_ids(orders):
    for order in orders:
        yield order["id"]


orders = [{"id": 1}, {"id": 2}, {"id": 3}]

for order_id in stream_order_ids(orders):
    print(order_id)
```

##### Interview Explanation

A generator is useful when:

- Data is large
- You do not want to load everything into memory
- You want lazy evaluation
- You are processing streams or batches

---

#### Python GIL
##### Question

What is the Global Interpreter Lock?

##### Answer

The GIL is a lock in CPython that allows only one thread to execute Python bytecode at a time. This means CPU-bound Python code does not get true parallel execution with threads.

##### Practical Impact

- Use **threading** for I/O-bound work.
- Use **multiprocessing** for CPU-bound work.
- Use **asyncio** for high-concurrency I/O workloads.

---

#### Threading vs Multiprocessing vs AsyncIO

| Approach        | Best For             | Example                             |
| --------------- | -------------------- | ----------------------------------- |
| Threading       | I/O-bound tasks      | Calling multiple APIs               |
| Multiprocessing | CPU-bound tasks      | Image processing, heavy computation |
| AsyncIO         | High-concurrency I/O | WebSocket server, async API calls   |

```python
import asyncio
import httpx

async def fetch_url(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.status_code

async def main():
    results = await asyncio.gather(
        fetch_url("https://example.com"),
        fetch_url("https://example.org"),
    )
    print(results)

asyncio.run(main())
```

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
