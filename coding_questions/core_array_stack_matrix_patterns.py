"""Core array, hash-map, stack, sliding-window, and matrix interview patterns.

This module consolidates seven frequently recurring interview exercises:

1. Two Sum
2. Best Time to Buy and Sell Stock
3. Evaluate Reverse Polish Notation
4. Rotate an n x n Matrix
5. Minimum Size Subarray Sum
6. Number of Visible People in a Queue
7. Longest Substring Without Repeating Characters

For each problem, explain the invariant before coding, test a normal case and
an edge case, and state time/space complexity.
"""

from __future__ import annotations


def two_sum(numbers: list[int], target: int) -> list[int]:
    """Return indices of two values whose sum is ``target``.

    Invariant: ``seen`` contains only values to the left of the current index.

    Time: O(n)
    Space: O(n)
    """
    seen: dict[int, int] = {}

    for index, number in enumerate(numbers):
        complement = target - number
        if complement in seen:
            return [seen[complement], index]
        seen[number] = index

    return []


def max_single_trade_profit(prices: list[int]) -> int:
    """Return the maximum profit from one buy followed by one sale.

    Invariant: ``minimum_price`` is the cheapest valid buy before the current
    sale day.

    Time: O(n)
    Space: O(1)
    """
    if not prices:
        return 0

    minimum_price = prices[0]
    maximum_profit = 0

    for price in prices[1:]:
        maximum_profit = max(maximum_profit, price - minimum_price)
        minimum_price = min(minimum_price, price)

    return maximum_profit


def _truncate_toward_zero(left: int, right: int) -> int:
    """Divide integers using truncation toward zero without float conversion."""
    if right == 0:
        raise ZeroDivisionError("division by zero")

    quotient = abs(left) // abs(right)
    return -quotient if (left < 0) != (right < 0) else quotient


def evaluate_reverse_polish_notation(tokens: list[str]) -> int:
    """Evaluate a valid Reverse Polish Notation expression.

    The pop order matters: the first pop is the right operand.

    Time: O(n)
    Space: O(n)
    """
    operators = {"+", "-", "*", "/"}
    stack: list[int] = []

    for token in tokens:
        if token not in operators:
            stack.append(int(token))
            continue

        if len(stack) < 2:
            raise ValueError("invalid Reverse Polish Notation expression")

        right = stack.pop()
        left = stack.pop()

        if token == "+":
            stack.append(left + right)
        elif token == "-":
            stack.append(left - right)
        elif token == "*":
            stack.append(left * right)
        else:
            stack.append(_truncate_toward_zero(left, right))

    if len(stack) != 1:
        raise ValueError("invalid Reverse Polish Notation expression")
    return stack[0]


def rotate_matrix_clockwise(matrix: list[list[int]]) -> None:
    """Rotate a square matrix 90 degrees clockwise in place.

    Transpose across the main diagonal, then reverse every row.

    Time: O(n^2)
    Extra space: O(1)
    """
    size = len(matrix)
    if any(len(row) != size for row in matrix):
        raise ValueError("in-place rotation requires a square matrix")

    for row in range(size):
        for column in range(row + 1, size):
            matrix[row][column], matrix[column][row] = (
                matrix[column][row],
                matrix[row][column],
            )

    for row in matrix:
        row.reverse()


def minimum_subarray_length(target: int, numbers: list[int]) -> int:
    """Return the shortest positive-number window with sum >= ``target``.

    This sliding-window solution relies on every input value being positive.

    Time: O(n)
    Space: O(1)
    """
    if target <= 0:
        raise ValueError("target must be positive")
    if any(number <= 0 for number in numbers):
        raise ValueError("this sliding-window variant requires positive values")

    left = 0
    current_sum = 0
    best = len(numbers) + 1

    for right, number in enumerate(numbers):
        current_sum += number

        while current_sum >= target:
            best = min(best, right - left + 1)
            current_sum -= numbers[left]
            left += 1

    return 0 if best == len(numbers) + 1 else best


def visible_people_to_right(heights: list[int]) -> list[int]:
    """Count how many people each person can see to their right.

    The common interview version uses distinct heights. Traverse right to
    left with a monotonic decreasing stack. A person sees every shorter height
    popped and, if present, the first taller height that remains.

    Time: O(n) amortized
    Space: O(n)
    """
    counts = [0] * len(heights)
    stack: list[int] = []

    for index in range(len(heights) - 1, -1, -1):
        current_height = heights[index]

        while stack and current_height > stack[-1]:
            stack.pop()
            counts[index] += 1

        if stack:
            counts[index] += 1

        stack.append(current_height)

    return counts


def longest_unique_substring_length(text: str) -> int:
    """Return the length of the longest substring without repeated chars.

    ``left`` is the first valid index of the active window and must never move
    backward when a repeated character is already outside that window.

    Time: O(n)
    Space: O(k), where k is the number of distinct characters
    """
    last_seen: dict[str, int] = {}
    left = 0
    longest = 0

    for right, character in enumerate(text):
        if character in last_seen:
            left = max(left, last_seen[character] + 1)

        last_seen[character] = right
        longest = max(longest, right - left + 1)

    return longest


def _run_examples() -> None:
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]
    assert two_sum([3, 3], 6) == [0, 1]
    assert two_sum([], 5) == []

    assert max_single_trade_profit([7, 1, 5, 3, 6, 4]) == 5
    assert max_single_trade_profit([7, 6, 4, 3, 1]) == 0
    assert max_single_trade_profit([]) == 0

    assert evaluate_reverse_polish_notation(["2", "1", "+", "3", "*"]) == 9
    assert evaluate_reverse_polish_notation(["4", "13", "5", "/", "+"]) == 6
    assert evaluate_reverse_polish_notation(["7", "-3", "/"]) == -2

    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    rotate_matrix_clockwise(matrix)
    assert matrix == [[7, 4, 1], [8, 5, 2], [9, 6, 3]]

    assert minimum_subarray_length(7, [2, 3, 1, 2, 4, 3]) == 2
    assert minimum_subarray_length(100, [1, 2, 3]) == 0

    assert visible_people_to_right([10, 6, 8, 5, 11, 9]) == [3, 1, 2, 1, 1, 0]
    assert visible_people_to_right([]) == []

    assert longest_unique_substring_length("abcabcbb") == 3
    assert longest_unique_substring_length("bbbbb") == 1
    assert longest_unique_substring_length("abba") == 2
    assert longest_unique_substring_length("") == 0


if __name__ == "__main__":
    _run_examples()
    print("All core array/stack/matrix examples passed.")
