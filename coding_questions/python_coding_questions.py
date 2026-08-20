"""General Python Coding Practice

This file is a collection of independent Python interview exercises. Each exercise follows the same lightweight structure used
throughout this folder: a triple-quoted question statement appears immediately before the implementation, followed by example
usage or expected output where useful. The long separator lines visually divide one exercise from the next.
"""

import string
from typing import List

##################################################################################################################################

"""Check if 2 strings are anagram."""


def are_anagrams(str1, str2):
    # Remove whitespace and convert to lowercase for case-insensitive comparison
    str1 = str1.replace(" ", "").lower()
    str2 = str2.replace(" ", "").lower()

    # Compare sorted versions of the strings
    return sorted(str1) == sorted(str2)


# Example usage
print(are_anagrams("listen", "silent"))  # True
print(are_anagrams("hello", "world"))  # False

##################################################################################################################################

"""Find the missing number from the list 1,......n."""


def find_missing_number(nums):
    # Calculate n based on the length of the list
    n = len(nums) + 1

    # Calculate the expected sum of numbers from 1 to n
    expected_sum = n * (n + 1) // 2

    # Calculate the actual sum of the given list
    actual_sum = sum(nums)

    # The missing number is the difference
    return expected_sum - actual_sum


# Example usage
nums = [1, 2, 4, 5, 6]  # Missing number is 3
print(find_missing_number(nums))  # Output: 3

##################################################################################################################################

"""Check if number is prime number."""


def is_prime(number):
    if number <= 1:
        return False  # Numbers <= 1 are not prime
    for i in range(2, int(number**0.5) + 1):
        if number % i == 0:
            return False  # Found a divisor, so it's not prime
    return True  # No divisors found, it's prime


# Example usage
print(is_prime(11))  # True
print(is_prime(15))  # False

##################################################################################################################################

"""Write a function to convert a roman to integer."""


def roman_to_int(s):
    # Map of Roman numerals to integers
    roman_to_int_map = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}

    total = 0  # To store the final integer value
    prev_value = 0  # To track the previous numeral's value

    # Iterate through the Roman numeral string in reverse
    for char in reversed(s):
        current_value = roman_to_int_map[char]

        if current_value < prev_value:
            # Subtract if the current value is smaller than the previous
            total -= current_value
        else:
            # Add if the current value is greater or equal to the previous
            total += current_value

        prev_value = current_value  # Update the previous value

    return total


# Example usage
print(roman_to_int("III"))  # Output: 3
print(roman_to_int("IV"))  # Output: 4
print(roman_to_int("IX"))  # Output: 9
print(roman_to_int("LVIII"))  # Output: 58
print(roman_to_int("MCMXCIV"))  # Output: 1994

##################################################################################################################################

"""Write a function to find the longest common prefix string amongst an array of strings. If there is no common prefix, return an
empty string"""


def longest_common_prefix(strs):
    if not strs:
        return ""  # Return empty string if the list is empty

    # Start with the first string as the prefix
    prefix = strs[0]

    # Compare the prefix with each string in the array
    for candidate in strs[1:]:
        # Reduce the prefix until it matches the start of the current string
        while not candidate.startswith(prefix):
            prefix = prefix[:-1]  # Remove the last character from the prefix
            if not prefix:  # If the prefix becomes empty, return ""
                return ""

    return prefix


# Example usage
print(longest_common_prefix(["flower", "flow", "flight"]))  # Output: "fl"
print(longest_common_prefix(["dog", "racecar", "car"]))  # Output: ""
print(longest_common_prefix(["interspecies", "interstellar", "interstate"]))  # Output: "inters"
print(longest_common_prefix([]))  # Output: ""
print(longest_common_prefix([""]))  # Output: ""

##################################################################################################################################

"""Given a string 'st', calculate the occurrence of each character with loop."""

st = "abbcccdddd"

# Initialize an empty dictionary to store character counts
char_count = {}

# Loop through each character in the string
for char in st:
    # If the character is already in the dictionary, increment its count
    if char in char_count:
        char_count[char] += 1
    # If the character is not in the dictionary, add it with count 1
    else:
        char_count[char] = 1

# Print the occurrence of each character
for char, count in char_count.items():
    print(f"Character: {char}, Count: {count}")

##################################################################################################################################

"""Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid."""


def is_valid(s):
    stack = []
    bracket_map = {")": "(", "}": "{", "]": "["}  # Mapping of closing to opening brackets

    for char in s:
        if char in bracket_map:  # If it's a closing bracket
            top_element = stack.pop() if stack else "#"  # Pop if stack is not empty
            if bracket_map[char] != top_element:  # Check if brackets match
                return False
        else:
            stack.append(char)  # Push opening brackets onto stack

    return not stack  # If stack is empty, it's valid


# Example Test Cases
print(is_valid("()"))  # True
print(is_valid("()[]{}"))  # True
print(is_valid("(]"))  # False
print(is_valid("([)]"))  # False
print(is_valid("{[]}"))  # True

##################################################################################################################################

"""Given n pairs of parentheses, write a function to generate all combinations of well-formed parentheses."""


def generate_parentheses(n):
    result = []

    def backtrack(s, open_count, close_count):
        # Base case: If we used all n pairs, add to result
        if len(s) == 2 * n:
            result.append(s)
            return

        # Add an opening bracket if we have available open brackets
        if open_count < n:
            backtrack(s + "(", open_count + 1, close_count)

        # Add a closing bracket if it doesn't exceed open brackets
        if close_count < open_count:
            backtrack(s + ")", open_count, close_count + 1)

    backtrack("", 0, 0)  # Start with an empty string
    return result


# Example Usage
print(generate_parentheses(3))

##################################################################################################################################

"""You are given the heads of two sorted linked lists list1 and list2. Merge the two lists into one sorted list. The list should
be made by splicing together the nodes of the first two lists. Return the head of the merged linked list."""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def merge_two_lists(list1, list2):
    dummy = ListNode()  # Dummy node to simplify list creation
    current = dummy  # Pointer to track merged list

    while list1 and list2:
        if list1.val < list2.val:
            current.next = list1
            list1 = list1.next
        else:
            current.next = list2
            list2 = list2.next
        current = current.next

    # Attach the remaining nodes
    current.next = list1 if list1 else list2

    return dummy.next  # Return the merged list, skipping dummy node


# Example Usage
def print_list(head):
    while head:
        print(head.val, end=" -> ")
        head = head.next
    print("None")


# Creating two sorted linked lists: 1 -> 2 -> 4 and 1 -> 3 -> 5
list1 = ListNode(1, ListNode(2, ListNode(4)))
list2 = ListNode(1, ListNode(3, ListNode(5)))

merged_head = merge_two_lists(list1, list2)
print_list(merged_head)  # Output: 1 -> 1 -> 2 -> 3 -> 4 -> 5 -> None

##################################################################################################################################

"""Given an integer array nums sorted in non-decreasing order, remove the duplicates in-place such that each unique element appears
only once. The relative order of the elements should be kept the same. Then return the number of unique elements in nums. Consider
the number of unique elements of nums to be k, to get accepted, you need to do the following things:
- Change the array nums such that the first k elements of nums contain the unique elements in the order they were present in nums
initially.
= The remaining elements of nums are not important as well as the size of nums.
= Return k."""


def remove_duplicates(nums):
    if not nums:
        return 0  # Edge case: empty array

    i = 0  # Pointer for unique elements

    for j in range(1, len(nums)):  # Start from second element
        if nums[j] != nums[i]:  # If a new unique element is found
            i += 1  # Move the unique pointer
            nums[i] = nums[j]  # Update array in-place

    return i + 1  # k = number of unique elements


# Example Usage
nums = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
k = remove_duplicates(nums)
print("Unique count:", k)  # Output: 5
print("Modified array:", nums[:k])  # Output: [0, 1, 2, 3, 4]

##################################################################################################################################

"""Given an integer array nums and an integer val, remove all occurrences of val in nums in-place. The order of the elements may be
changed. Then return the number of elements in nums which are not equal to val. Consider the number of elements in nums which are
not equal to val be k, to get accepted, you need to do the following things:
- Change the array nums such that the first k elements of nums contain the elements which are not equal to val.
- The remaining elements of nums are not important as well as the size of nums.
- Return k."""


def remove_element(nums, val):
    i = 0  # Pointer for valid elements

    for j in range(len(nums)):
        if nums[j] != val:  # If current element is not val
            nums[i] = nums[j]  # Move valid element to position i
            i += 1  # Increment valid count

    return i  # k = number of elements not equal to val


# Example Usage
nums = [3, 2, 2, 3]
val = 3
k = remove_element(nums, val)
print("Remaining count:", k)  # Output: 2
print("Modified array:", nums[:k])  # Output: [2, 2]

##################################################################################################################################

"""Given a list lst = [1, 2, 3,..., 23], create a list of lists of indexes with at most 2 numbers from the given list whose sum
is equal to 24."""

lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

# Initialize an empty list to store the result
index_pairs = []

# Iterate through the list and check each pair of numbers
for i in range(len(lst)):
    for j in range(i + 1, len(lst)):
        if lst[i] + lst[j] == 24:
            # Append the pair of indexes to the result list
            index_pairs.append([i, j])

# Print the result
print(index_pairs)

"""With omega log n complexity"""
# Initialize an empty dictionary to store numbers and their indices
index_map = {}

# Initialize a list to store the result of index pairs
index_pairs = []

# Iterate through the list
for i, num in enumerate(lst):
    # Calculate the complement
    complement = 24 - num

    # Check if the complement exists in the dictionary
    if complement in index_map:
        # Append the pair of indices to the result list
        index_pairs.append([index_map[complement], i])

    # Store the current number and its index in the dictionary
    index_map[num] = i

# Print the result
print(index_pairs)

##################################################################################################################################

"""Write a program to find maximum number of drop points that can be covered by flying over the terrain once. The points are
given as input in the form of integers coordinates in a two dimensional field. The flight path can be horizontal or vertical,
but not a mix of the two or diagonal."""


def max_drop_points(x_coords, y_coords):
    # Dictionaries to count occurrences of points with the same x and y coordinates
    x_count = {}
    y_count = {}

    # Ensure both lists are of the same length
    if len(x_coords) != len(y_coords):
        raise ValueError("x and y coordinates must have the same length")

    # Iterate using index, without using zip
    for i in range(len(x_coords)):
        x = x_coords[i]
        y = y_coords[i]

        if x in x_count:
            x_count[x] += 1
        else:
            x_count[x] = 1

        if y in y_count:
            y_count[y] += 1
        else:
            y_count[y] = 1

    # Filter out any groups with only 1 point
    max_x_points = max([count for count in x_count.values() if count > 1], default=0)
    max_y_points = max([count for count in y_count.values() if count > 1], default=0)

    # Return the maximum of the two
    return max(max_x_points, max_y_points)


# Example usage:
x_coords = [1, 2, 3, 4, 4, 2, 2]
y_coords = [2, 2, 2, 5, 1, 3, 4]

result = max_drop_points(x_coords, y_coords)
print(f"Maximum number of drop points covered: {result}")

##################################################################################################################################

"""Write a program to find maximum number of chocolates that can be picked from the jars in such a way that the chocolates are
not picked from jars next to each other."""


def max_chocolates(chocolates):
    n = len(chocolates)

    # Base cases
    if n == 0:
        return 0
    if n == 1:
        return chocolates[0]

    # Initialize the DP array
    dp = [0] * n

    # Set up the first two values
    dp[0] = chocolates[0]
    dp[1] = max(chocolates[0], chocolates[1])

    # Fill in the dp array using the recurrence relation
    for i in range(2, n):
        dp[i] = max(chocolates[i] + dp[i - 2], dp[i - 1])

    # The last element of dp array will have the answer
    return dp[-1]


# Example usage:
chocolates = [6, 7, 1, 30, 8, 2, 4]
result = max_chocolates(chocolates)
print(f"Maximum chocolates that can be picked: {result}")

##################################################################################################################################

"""Write a program to rotation a n*m matrix by 90 degrees."""


def rotate_matrix_90_clockwise(matrix):
    # Get the dimensions of the matrix
    n = len(matrix)  # Number of rows
    m = len(matrix[0])  # Number of columns

    # Create a new matrix to store the rotated version
    rotated_matrix = [[0] * n for _ in range(m)]

    # Fill the rotated matrix by adjusting the positions
    for i in range(n):
        for j in range(m):
            rotated_matrix[j][n - 1 - i] = matrix[i][j]

    # Store the rotated matrix in a variable
    result_matrix = "\n".join([" ".join(map(str, row)) for row in rotated_matrix])

    # Return the formatted matrix as a string
    return result_matrix


# Example usage:
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

# Store the rotated matrix in a variable and return it
rotated_matrix = rotate_matrix_90_clockwise(matrix)

# Print the result
print(rotated_matrix)

##################################################################################################################################

"""Write a program to find out the elements which are largest in a row and smallest in a column in a n*m matrix."""


def find_largest_in_row_and_smallest_in_column(matrix, n, m):
    # Result list to store the saddle points
    result = []

    # Traverse each row
    for i in range(n):
        # Find the largest element in the row and its column index
        row_max = max(matrix[i])
        col_index = matrix[i].index(row_max)

        # Check if this element is the smallest in its column
        is_smallest_in_column = True
        for j in range(n):  # Traverse the column of the row_max element
            if matrix[j][col_index] < row_max:
                is_smallest_in_column = False
                break

        # If the element is the largest in the row and smallest in the column, add it to the result
        if is_smallest_in_column:
            result.append((row_max, i, col_index))  # Add element and its position (row, col)

    # Return the result list if it contains saddle points, otherwise return None
    return result if result else None


# Example usage
n, m = 3, 3
matrix = [[3, 8, 9], [5, 2, 4], [7, 1, 6]]

result = find_largest_in_row_and_smallest_in_column(matrix, n, m)

if result:
    for val, row, col in result:
        print(f"Element {val} is largest in row {row + 1} and smallest in column {col + 1}")
else:
    print("No such element found.")

##################################################################################################################################

"""Find the substring from a string that is the same when read forward and backward in a single function and return `None` if no
palindrome substring."""


def longest_palindrome(s):
    if not s:
        return None

    def expand_around_center(left, right):
        # Expand as long as the substring is a palindrome
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        # Return the palindrome substring
        return s[left + 1 : right]

    longest_palindrome = None

    for i in range(len(s)):
        # Odd length palindrome (single character center)
        palindrome_odd = expand_around_center(i, i)
        if longest_palindrome is None or len(palindrome_odd) > len(longest_palindrome):
            longest_palindrome = palindrome_odd

        # Even length palindrome (two character center)
        palindrome_even = expand_around_center(i, i + 1)
        if len(palindrome_even) > len(longest_palindrome):
            longest_palindrome = palindrome_even

    # Return None if no palindrome was found, else return the longest palindrome
    return longest_palindrome if longest_palindrome and len(longest_palindrome) > 1 else None


# Example usage
s = "abc"
print(longest_palindrome(s))  # Output: None

s2 = "babad"
print(longest_palindrome(s2))  # Output: "bab" or "aba"

##################################################################################################################################

"""Given a list of integers, find the maximum difference of 2 elements where the larger number appears after the smaller number."""


def max_difference(arr):
    if len(arr) < 2:
        return 0  # Not enough elements for a valid difference

    min_element = arr[0]
    max_diff = float("-inf")

    for i in range(1, len(arr)):
        diff = arr[i] - min_element
        if diff > max_diff:
            max_diff = diff
        if arr[i] < min_element:
            min_element = arr[i]

    return max_diff if max_diff > 0 else 0  # Return 0 if no valid difference


##################################################################################################################################

"""Convert a non-negative integer num to its English words representation."""


def numberToWords(self, num: int) -> str:
    if num == 0:
        return "Zero"

    # Words for units, teens, tens, and thousands
    units = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
    teens = [
        "Ten",
        "Eleven",
        "Twelve",
        "Thirteen",
        "Fourteen",
        "Fifteen",
        "Sixteen",
        "Seventeen",
        "Eighteen",
        "Nineteen",
    ]
    tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
    thousands = ["", "Thousand", "Million", "Billion"]

    def helper(n):
        if n == 0:
            return ""
        elif n < 10:
            return units[n]
        elif n < 20:
            return teens[n - 10]
        elif n < 100:
            return tens[n // 10] + ("" if n % 10 == 0 else " " + units[n % 10])
        else:
            return units[n // 100] + " Hundred" + ("" if n % 100 == 0 else " " + helper(n % 100))

    result = ""
    for i, chunk in enumerate(thousands):
        if num % 1000 != 0:
            result = helper(num % 1000) + " " + chunk + ("" if result == "" else " " + result)
        num //= 1000

    return result.strip()


##################################################################################################################################

"""You are given a 2D maze represented by a grid. The maze consists of open paths (0) and walls (1). Your goal is to implement
a function that finds and marks the solution path in the maze using the value 2. The maze solver should start from the top-left
corner (cell [0, 0]) and reach the bottom-right corner (cell [len(maze) - 1, len(maze[0]) - 1]). The solution path can only move
through open paths and should navigate around walls."""


def solve_maze(maze):
    rows, cols = len(maze), len(maze[0])
    solution_path = []

    # Helper function to perform DFS
    def dfs(x, y):
        # Base case: reached the bottom-right corner
        if x == rows - 1 and y == cols - 1:
            maze[x][y] = 2
            solution_path.append((x, y))
            return True

        # Check if the current cell is out of bounds or a wall
        if x < 0 or y < 0 or x >= rows or y >= cols or maze[x][y] != 0:
            return False

        # Mark the cell as part of the solution path
        maze[x][y] = 2
        solution_path.append((x, y))

        # Explore neighbors in the order: Down, Right, Up, Left
        if (
            dfs(x + 1, y)  # Down
            or dfs(x, y + 1)  # Right
            or dfs(x - 1, y)  # Up
            or dfs(x, y - 1)  # Left
        ):
            return True

        # If no path is found, backtrack
        maze[x][y] = 0
        solution_path.pop()
        return False

    if dfs(0, 0):
        return maze, solution_path
    else:
        return None, []  # No solution


# Hardcoded maze
hardcoded_maze = [
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
]

# Solve the maze
solved_maze, path = solve_maze(hardcoded_maze)

if solved_maze:
    print("Solved Maze:")
    for row in solved_maze:
        print(row)
    print("\nSolution Path:", path)
else:
    print("No solution found.")

##################################################################################################################################

"""Write a program that takes an array, Returns the smallest positive integers greater than 0 that does not occur in array."""


def smallest_missing_positive(arr):
    # Remove non-positive numbers and duplicates
    arr = set(filter(lambda x: x > 0, arr))
    # Start checking from 1
    smallest = 1
    while smallest in arr:
        smallest += 1
    return smallest


# Example usage
input_array = [3, 4, -1, 1]
result = smallest_missing_positive(input_array)
print(f"The smallest positive integer missing is: {result}")

##################################################################################################################################

"""The counting game is a widely popular casual game. Every participant in the game must count numbers in sequence. However, If
number to be called is a multiple of 7, or if the next number contains the digit 7, then that number must be skipped, otherwise,
you lose the game.
Rose and Zack play this game and find it too easy, so they decide to modify some rules: for any number containing the digit 7, all
its multiples cannot be called either! For example, if Rose calls out 6, since 7 cannot be called, Zack must call 8 next. If Rose
calls out 33, since 34 is 17 times 2 and 35 is 7 times 5, Zack's next possible call is 36. If Rose calls out 69, because numbers 70
to 79 all contain the digit 7, Zack's next call must be 80.
Input Format - Input a line which contains a positive integer x, indicating the number called by Rose this time.
Output Format - Output a lines which contains an integer. If the number called by Rose this time is invalid (cannot be called),
output -1. Otherwise, output the number that Zack should call next."""


def next_number_called_by_zack(x):
    # Helper function to check if a number is invalid
    def is_invalid(num):
        return (
            "7" in str(num)
            or num % 7 == 0
            or any(num % i == 0 for i in range(1, num) if "7" in str(i))
        )

    # Check if Rose's number is invalid
    if is_invalid(x):
        return -1

    # Find Zack's next valid number
    current = x + 1
    while is_invalid(current):
        current += 1

    return current


# Input
x = int(input("Enter the number Rose called: "))

# Output
result = next_number_called_by_zack(x)
print(result)

##################################################################################################################################

"""Given a number n (1 «= n «= 10'10), the task is to find all the possible sequences of successive positive integer numbers
(p. p+1, ... ) satisfy the equation: n = p+2 + (p+1)*2 + ... + (p+m)*2.
Input - The input consists of a single integer n.
Output - The output is an array of strings consisting of two parts. The first element should display the total number of possible
sequences, denoted as k. The following k elements should contain the descriptions of the sequences. Each element is a string starts
with the count of numbers in the corresponding sequence, denoted as c, followed by e integers representing the successive positive
integer numbers, separated by a space. These k elements should be ordered in descending order of c.
Sample Input - 2030
Sample Output - ["2","4 21 22 23 24","3 25 26 27"]"""


def find_sequences(n):
    results = []
    for p in range(1, int(n**0.5) + 1):  # Check possible starting points
        total = 0
        sequence = []
        for m in range(p, int(n**0.5) + 2):  # Extend the sequence
            total += m * m
            sequence.append(m)
            if total == n:
                results.append(sequence)
                break
            elif total > n:
                break

    # Format output
    formatted_results = []
    for seq in results:
        formatted_results.append(f"{len(seq)} {' '.join(map(str, seq))}")

    # Convert the count of results to string and return
    return [str(len(results))] + formatted_results


# Input
n = int(input("Enter the value of n: "))

# Output
output = find_sequences(n)
print(output)

##################################################################################################################################

"""Write a piApprox(pts) function who will use the points pts to return an approximation of the number float π. Pts is a
multidimensional list of float.Each item in pts is a point, a point is represented by an array containing exactly 2 numbers,
respectively x and y, pts is never None and always contain at least one item."""


def piApprox(pts):
    inside_circle = 0
    total_points = len(pts)

    for point in pts:
        x, y = point
        # Check if the point is inside the circle (x^2 + y^2 <= 1)
        if x**2 + y**2 <= 1:
            inside_circle += 1

    # Estimate of π using the formula 4 * (points inside circle / total points)
    return 4 * (inside_circle / total_points)


pts = [[0.5, 0.5], [0.1, 0.1], [-0.7, 0.7], [0.9, 0.2], [0.5, -0.3]]
print(piApprox(pts))  # Output will be an approximation of π

##################################################################################################################################

"""Implement function compute(start_node_id, from_ids, to_ids) which should return the last node I'd of the network found when
starting from the node with id start_node_id and following the links of the network. In case you run into a loop when traversing
the network, the function should return the id of the last node traversed before closing the loop. The node ids are not necessarily
ordered. A node will never be directly linked to itself."""


def compute(start_node_id, from_ids, to_ids):
    # Create a mapping of from_ids to to_ids for easier traversal
    links = {}
    for from_id, to_id in zip(from_ids, to_ids):
        links[from_id] = to_id

    visited = set()  # Set to track visited nodes
    current_node = start_node_id
    last_visited = None  # To keep track of the last node visited before the loop

    while current_node in links:  # As long as there's a link to follow
        if current_node in visited:  # If we've already visited this node, return the last node
            return last_visited
        visited.add(current_node)  # Mark this node as visited
        last_visited = current_node  # Update the last visited node
        current_node = links[current_node]  # Move to the next node in the network

    return current_node  # If no loop is found, return the last node


# Example usage:
from_ids = [11, 7, 10, 9, 8, 4, 1]
to_ids = [1, 10, 11, 10, 11, 8, 4]
start_node_id = 9
print(compute(start_node_id, from_ids, to_ids))  # Expected Output: 8

##################################################################################################################################

"""How we proceed to form duels: select a first player randomly, then select his opponent at random among remaining participants.
The pair obtained forms one of the duels of tournament. Implement count function to return number if possible pairs. Parameter "n"
corresponds to number of players. Try to optimize solution so that duration of treatment is same for any "n".
Note: 2 <= n <= 10000"""


def count(n):
    # Return the number of duels using the combination formula C(n, 2) = n(n-1) / 2
    return n * (n - 1) // 2


# Example usage
n = 10
print(count(n))  # Output: 45 (since C(10, 2) = 10*9/2 = 45)

##################################################################################################################################

"""You are part of data analytics team for a new app company. User feedback is essential for your company's success, and your task
is to analyze user reviews to find trends and areas of improvements. Each user review is represented as a dictionary with keys:
id(unique identifier), rating(integer from 1 to 5), review(string), and date()string in the format "YYYY-MM-DD". Given a list of
reviews, your task is to,
1. Calculate the average rating. It should be upto only decimal place only.
2. Identify the most common words in the reviews. Exclude any punctuation from the reviews and transform all words to lower case
for consistency.
3. Find the month with most reviews submitted.
Note: Consider words to be any sequence characters separated by spaces. You can assume all words in reviews are in lowercase."""


# Function to analyze reviews
def analyze_reviews(reviews):
    # Step 1: Calculate the average rating
    total_rating = sum(review["rating"] for review in reviews)
    avg_rating = total_rating / len(reviews) if reviews else 0

    # Step 2: Identify the most common words
    STOPWORDS = set(
        ["the", "and", "a", "to", "of", "for", "in", "but", "some", "it", "is", "on", "was", "with"]
    )
    word_count = {}
    for review in reviews:
        # Convert to lowercase and remove punctuation
        words = (
            review["review"].lower().translate(str.maketrans("", "", string.punctuation)).split()
        )
        for word in words:
            if word not in STOPWORDS:
                word_count[word] = word_count.get(word, 0) + 1

    max_word_count = max(word_count.values(), default=0)
    most_common_words = [word for word, count in word_count.items() if count == max_word_count]

    # Step 3: Find the month with the most reviews
    monthly_reviews = {}
    for review in reviews:
        # Extract the month in "YYYY-MM" format
        month = review["date"][:7]
        monthly_reviews[month] = monthly_reviews.get(month, 0) + 1

    max_month_count = max(monthly_reviews.values(), default=0)
    most_reviews_month = [
        month for month, count in monthly_reviews.items() if count == max_month_count
    ]

    # Convert months to readable names
    month_name = {
        "01": "January",
        "02": "February",
        "03": "March",
        "04": "April",
        "05": "May",
        "06": "June",
        "07": "July",
        "08": "August",
        "09": "September",
        "10": "October",
        "11": "November",
        "12": "December",
    }
    most_reviews_month_names = [
        f"{month_name.get(month[-2:], 'Unknown')} {month[:4]}" for month in most_reviews_month
    ]

    # Return results
    return {
        "average_rating": round(avg_rating, 1),
        "most_common_words": most_common_words,
        "month_with_most_reviews": most_reviews_month_names,
    }


# Example data
reviews = [
    {"id": 1, "rating": 5, "review": "The coffee was fantastic.", "date": "2022-05-01"},
    {
        "id": 2,
        "rating": 4,
        "review": "Excellent atmosphere. Love the modern design.",
        "date": "2022-05-15",
    },
    {"id": 3, "rating": 3, "review": "The menu was limited.", "date": "2022-05-20"},
    {"id": 4, "rating": 5, "review": "Highly recommend the caramel latte.", "date": "2022-05-21"},
    {"id": 5, "rating": 4, "review": "Seating outside is a nice touch.", "date": "2022-06-07"},
    {"id": 6, "rating": 2, "review": "It's my go-to coffee place!", "date": "2022-06-11"},
    {"id": 7, "rating": 5, "review": "Menu could use more vegan options.", "date": "2022-06-15"},
    {"id": 8, "rating": 3, "review": "The pastries are the best.", "date": "2022-06-28"},
    {"id": 9, "rating": 5, "review": "Great service during the weekend.", "date": "2022-07-05"},
    {"id": 10, "rating": 4, "review": "Baristas are friendly and skilled.", "date": "2022-07-12"},
    {
        "id": 11,
        "rating": 4,
        "review": "A bit pricier than other places in the area.",
        "date": "2022-07-18",
    },
    {"id": 12, "rating": 4, "review": "Love their rewards program.", "date": "2022-07-25"},
]

# Analyze reviews
result = analyze_reviews(reviews)

# Print results
print(f"Average Rating: {result['average_rating']}")
print(f"Most Common Words: {', '.join(result['most_common_words'])}")
print(f"Month with Most Reviews: {', '.join(result['month_with_most_reviews'])}")

##################################################################################################################################

"""In a school there are "n" students who want to participate in an academic decathlon. The teacher wants to select maximum number
of students possible. Each student has a certain skill level. For the team to be uniform, it is important that when the skill level
of its members are arranged in an increasing order, the difference between any two consecutive skill levels is either 0 or 1. Find
the maximum team size the teacher can form."""


def findMaxTeamSize(skills):
    # Step 1: Sort the array
    for i in range(len(skills)):
        for j in range(i + 1, len(skills)):
            if skills[i] > skills[j]:
                skills[i], skills[j] = skills[j], skills[i]

    # Step 2: Frequency dictionary
    freq = {}
    for skill in skills:
        if skill not in freq:
            freq[skill] = 0
        freq[skill] += 1

    # Step 3: Calculate max team size
    max_team_size = 0
    for skill in freq:
        current_team_size = freq[skill]
        if skill + 1 in freq:
            current_team_size += freq[skill + 1]
        max_team_size = max(max_team_size, current_team_size)

    return max_team_size


# Input
skills = [4, 4, 13, 2, 3]
print(findMaxTeamSize(skills))  # Output: 3

##################################################################################################################################

"""Find the number of names in the names list for which a given query string is a prefix, but the query string must not match the
entire name. For example: Names - [John, 10, Johnny, Jo, Jonas], Query - [John], this function should return 1."""


def findCompletePrefixes(names, queries):
    # Result array to store counts for each query
    result = []

    # Iterate through each query
    for query in queries:
        count = 0
        # Check each name for the query prefix
        for name in names:
            if name.startswith(query) and len(query) < len(name):
                count += 1
        # Append the count for the query
        result.append(count)

    return result


# Input Handling
if __name__ == "__main__":
    n = int(input().strip())
    names = []
    for _ in range(n):
        names_item = input().strip()
        names.append(names_item)

    q = int(input().strip())
    queries = []
    for _ in range(q):
        query_item = input().strip()
        queries.append(query_item)

    # Call the function
    result = findCompletePrefixes(names, queries)

    # Print the results
    for res in result:
        print(res)

##################################################################################################################################

"""Imagine you're building a backend for an e-commerce website. One of the functions in your backend is responsible for updating
the shopping cart based on user actions. Users can add items to their cart, remove items from the cart, or change the quantity of
the items they've added. You are provided a function named "update_shopping_cart" which accepts 2 arguments,
1. cart: A dictionary where the keys are product IDs (str) and the values are the number of that product currently in the cart (int).
2. action: A dictionary representing the user's action. It has two keys:
- type: A string that can be either "add", "remove", or "change".
- product_id: The product ID the action is referring to.
- quantity (only when the type is "add" or "change"): The quantity to add or the new quantity to set.
Your task is to modify the "update_shopping_cart" function to handle the user action and return the updated cart correctly."""


def update_shopping_cart(cart, action):
    product_id = action.get("product_id")
    action_type = action.get("type")

    # Ensure product_id and type are provided
    if not product_id or not action_type:
        return cart

    # Handle "add" action
    if action_type == "add":
        quantity = action.get("quantity", 0)
        if product_id in cart:
            cart[product_id] += quantity
        else:
            cart[product_id] = quantity

    # Handle "remove" action
    elif action_type == "remove":
        if product_id in cart:
            del cart[product_id]

    # Handle "change" action
    elif action_type == "change":
        quantity = action.get("quantity", 0)
        if product_id in cart and quantity > 0:
            cart[product_id] = quantity
        elif product_id in cart and quantity <= 0:
            del cart[product_id]

    return cart


# Example usage
cart = {
    "apple": 2,
    "banana": 3,
}

action = {
    "type": "add",
    "product_id": "apple",
    "quantity": 2,
}

updated_cart = update_shopping_cart(cart, action)
print(updated_cart)  # Output: {'apple': 4, 'banana': 3}

##################################################################################################################################

"""String s contains numbers 0 o 9, print the count of indexes(i) in string s such that HCF of (s[0], s[1],......s[i] is equal
to HCF of (s[i+1],.....s[N-1])"""


# Function to calculate HCF using the Euclidean algorithm
def compute_hcf(a, b):
    while b != 0:
        a, b = b, a % b
    return a


# Function to count valid indices
def count_hcf_indices(s):
    # Convert string to list of integers
    digits = list(map(int, s))
    n = len(digits)

    # Initialize prefix and suffix HCF arrays
    prefix_hcf = [0] * n
    suffix_hcf = [0] * n

    # Calculate prefix HCFs
    prefix_hcf[0] = digits[0]
    for i in range(1, n):
        prefix_hcf[i] = compute_hcf(prefix_hcf[i - 1], digits[i])

    # Calculate suffix HCFs
    suffix_hcf[n - 1] = digits[n - 1]
    for i in range(n - 2, -1, -1):
        suffix_hcf[i] = compute_hcf(suffix_hcf[i + 1], digits[i])

    # Count indices where prefix HCF == suffix HCF
    count = 0
    for i in range(n - 1):  # Exclude last index
        if prefix_hcf[i] == suffix_hcf[i + 1]:
            count += 1

    return count


# Example usage
s = "4848"
print(count_hcf_indices(s))  # Output: 2

##################################################################################################################################

"""Implement a function that takes an array of temperature and returned the temperature closest to 0."""


def closest_to_zero(temperatures):
    if not temperatures:
        return None  # Return None if the array is empty

    # Sort by absolute value and prioritize positive values in case of ties
    return min(temperatures, key=lambda x: (abs(x), -x))


# Example usage
temperatures = [-5, -2, -1, 1, 2, 3, -3]
print(closest_to_zero(temperatures))  # Output: 1

##################################################################################################################################

"""You are climbing a staircase. It takes n steps to reach the top. Each time you can either climb 1 or 2 steps. In how many
distinct ways can you climb to the top?"""


def climb_stairs_optimized(n):
    if n <= 1:
        return 1

    prev1, prev2 = 1, 1  # Base cases

    for _ in range(2, n + 1):
        curr = prev1 + prev2
        prev2 = prev1
        prev1 = curr

    return prev1


##################################################################################################################################

"""The developers of Amazon are working on a prototype for a simple load-balancing algorithm. There are num_servers servers
numbered from 0 to num_servers - 1 and the initial number of requests assigned to each server is 0. In the ith second, a request
comes from IP hash of request[i], and It must be assigned to the server with the minimum number of requests among the servers from
index 0 to request[i]. For example, if request[i] = 4, the request must be assigned to the server with the minimum number of requests
amongst the servers with id [0, 1, 2, 3, 4]. If there are multiple servers with the same minimum number of requests, choose the one
with the minimum id. When a request is assigned to a server, its number of requests increases by 1.
Given num_servers and the array request, for each request, find the id of the server it is assigned to.
Example
Suppose num_servers = 5, n = 5 and request = [3, 2, 3, 2, 4]. The requests are processed as follows:
-------------------------------------------------------------------------------------------------------------------------------------------
| Request IP Hash | Server Request Allocation | Assigned to |                                Remarks                                      |
-------------------------------------------------------------------------------------------------------------------------------------------
|        3        |       [0, 0, 0, 0, 0]     |      0      |  The request must be assigned to the server with the minimum number of      |
|                 |                           |             |  requests amongst the first 3 servers. Since all the first three servers    |
|                 |                           |             |  have 0 requests assigned, it is assigned to the one with the minimum id,   |
|                 |                           |             |  i.e. the server with id 0.                                                 |
|        2        |       [1, 0, 0, 0, 0]     |      1      |  The request must be assigned to the server with the minimum number of      |
|                 |                           |             |  requests amongst the first 2 servers. Since server 1 has 0 requests signed |
|                 |                           |             |  which is less than server 0 with 1.                                        |
|        3        |       [1, 1, 0, 0, 0]     |      2      |  Amongst the first 3 servers, the one with the minimum requests is server 2.|
|        2        |       [1, 1, 1, 0, 0]     |      0      |  Both of the first 2 servers have the same number of requests assigned.     |
|                 |                           |             |  Hence the request is assigned to server 0 as it has the minimum id.        |
|        4        |       [2, 1, 1, 0, 0]     |      3      |  The request must be assigned to the server with the minimum number of      |
|                 |                           |             |  requests amongst the first 4 servers. The server with minimum requests is  |
|                 |                           |             |  server 3.                                                                  |
-------------------------------------------------------------------------------------------------------------------------------------------
"""


def assign_requests(num_servers, requests):
    # Array to track the number of requests handled by each server
    server_counts = [0] * num_servers
    result = []

    for req in requests:
        # Find the server with the minimum load in the range [0, req]
        chosen_server = -1
        min_load = float("inf")

        # Iterate only up to the range of servers [0, req]
        for server in range(req + 1):
            # Choose the server with the smallest load or, in case of a tie, the smallest ID
            if server_counts[server] < min_load or (
                server_counts[server] == min_load and server < chosen_server
            ):
                min_load = server_counts[server]
                chosen_server = server

        # Assign the request to the chosen server
        result.append(chosen_server)
        server_counts[chosen_server] += 1  # Increment the count for the chosen server

    return result


# Example Input
num_servers = 5
requests = [3, 2, 3, 2, 4]

# Function Call
output = assign_requests(num_servers, requests)
print(output)  # Expected Output: [0, 1, 2, 0, 3]

##################################################################################################################################

"""You are developing a basic word processor that includes a reflow and full-justification feature for text. You are given a list
of strings lines, where each string represents a line of unwrapped text (e.g., sentences or fragments) and an integer max_width
representing the target width of each output line.
Your task is to:
- Reflow the entire input text into a continuous block of words (i.e., flatten all input lines into one word list).
- Wrap the text so that each output line is no more than max_width characters.
- Justify the text so that each line has exactly max_width characters:
- Insert dashes (-) between words to act as spaces.
- Distribute extra dashes as evenly as possible between words.
- If the dashes cannot be evenly distributed, add the extra ones to the leftmost gaps.
- If a line contains only one word, do not pad it with dashes.
- Return the resulting lines as a list of strings.
"""


def word_wrap(words, max_length):
    result = []
    current_line = []
    current_length = 0

    for word in words:
        if current_length + len(word) + (len(current_line) if current_line else 0) <= max_length:
            # Add word to current line
            current_line.append(word)
            current_length += len(word)
        else:
            # Join and store the current line
            result.append("-".join(current_line))
            # Start a new line with the current word
            current_line = [word]
            current_length = len(word)

    # Add the last line
    if current_line:
        result.append("-".join(current_line))

    return result


# Example Usage
words = [
    "The",
    "day",
    "began",
    "as",
    "still",
    "as",
    "the",
    "night",
    "abruptly",
    "light",
    "pierced",
    "the",
    "sky",
]
max_length = 13
wrapped_text = word_wrap(words, max_length)
for line in wrapped_text:
    print(line)

##################################################################################################################################

"""You are building a simple word processor that supports a text reflow feature with full justification. You are given a list of
strings, where each string represents a line of unwrapped text (i.e., may contain multiple words) and an integer max_width representing
the maximum number of characters per line.
Your task is to:
- Reflow all the lines into a single block of text (i.e., treat all words across all input lines as one continuous stream of text).
- Format the text so that each output line has exactly max_width characters.
- If the line is too short (i.e., total characters + minimal spacing between words < max_width), you must distribute extra dashes (-) as
evenly as possible between the words to pad the line to the correct length.
- If the padding cannot be evenly distributed, add extra dashes to the leftmost gaps.
- If a line contains only one word, it should not be padded with extra dashes.
"""


def reflow_and_justify(lines: List[str], max_width: int) -> List[str]:
    # Step 1: Flatten all lines into a single list of words
    words = " ".join(lines).split()

    result = []
    current_line = []
    current_length = 0

    for word in words:
        # Check if we can add the word to the current line
        if current_length + len(word) + len(current_line) <= max_width:
            current_line.append(word)
            current_length += len(word)
        else:
            # Justify and add the current line to result
            result.append(justify_line(current_line, max_width))
            current_line = [word]
            current_length = len(word)

    # Justify and add the final line if exists
    if current_line:
        result.append(justify_line(current_line, max_width))

    return result


def justify_line(words: List[str], max_width: int) -> str:
    if len(words) == 1:
        # Single-word line, no justification needed
        return words[0]

    total_chars = sum(len(word) for word in words)
    total_spaces = max_width - total_chars
    num_gaps = len(words) - 1

    # Distribute the spaces as evenly as possible
    spaces = [total_spaces // num_gaps] * num_gaps
    for i in range(total_spaces % num_gaps):
        spaces[i] += 1  # Add the leftover spaces from the left

    # Build the justified line
    justified = words[0]
    for i in range(num_gaps):
        justified += "-" * spaces[i] + words[i + 1]

    return justified


##################################################################################################################################

"""Given matrix, an n × n square matrix of integers, define its 0-border as the union of its leftmost and rightmost columns as well
as its top and bottom rows. If we were to remove the matrix’s 0-border then the 0-border of the resulting matrix can be defined as
the 1-border of the original matrix. We can continue this way to define the 2-border, 3-border, etc.
For each k in [0, 1, ..., floor((n - 1) / 2)], your task is to sort the elements in each k-border and place them in clockwise order, starting from the top-left corner.
"""


def sort_matrix_borders(matrix):
    n = len(matrix)

    def get_k_border(k):
        values = []
        # Top row
        for j in range(k, n - k):
            values.append(matrix[k][j])
        # Right column
        for i in range(k + 1, n - k - 1):
            values.append(matrix[i][n - k - 1])
        # Bottom row (if not same as top)
        if k != n - k - 1:
            for j in range(n - k - 1, k - 1, -1):
                values.append(matrix[n - k - 1][j])
        # Left column
        for i in range(n - k - 2, k, -1):
            values.append(matrix[i][k])
        return values

    def set_k_border(k, values):
        idx = 0
        # Top row
        for j in range(k, n - k):
            matrix[k][j] = values[idx]
            idx += 1
        # Right column
        for i in range(k + 1, n - k - 1):
            matrix[i][n - k - 1] = values[idx]
            idx += 1
        # Bottom row (if not same as top)
        if k != n - k - 1:
            for j in range(n - k - 1, k - 1, -1):
                matrix[n - k - 1][j] = values[idx]
                idx += 1
        # Left column
        for i in range(n - k - 2, k, -1):
            matrix[i][k] = values[idx]
            idx += 1

    for k in range((n + 1) // 2):
        border_values = get_k_border(k)
        border_values.sort()
        set_k_border(k, border_values)

    return matrix


##################################################################################################################################

"""Given a square matrix of 0s and 1s as strings, return the size of the largest plus sign with equal arms made of only 1s. Return
the size of the arms, not including the center. The center of the plus sign and all arms must be 1s and the arms must extend the
same number of steps in the up, down, left, and right directions. A single 1 does not count as a plus sign. The size of the matrix
will not exceed 1000 x 1000.
"""


def solution(matrix):
    n = len(matrix)
    m = len(matrix[0])

    # Convert each row from string to list of integers
    grid = [[int(c) for c in row] for row in matrix]

    # Create 2D arrays for all 4 directions
    up = [[0] * m for _ in range(n)]
    down = [[0] * m for _ in range(n)]
    left = [[0] * m for _ in range(n)]
    right = [[0] * m for _ in range(n)]

    # Fill up and left
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 1:
                up[i][j] = (up[i - 1][j] + 1) if i > 0 else 1
                left[i][j] = (left[i][j - 1] + 1) if j > 0 else 1

    # Fill down and right
    for i in reversed(range(n)):
        for j in reversed(range(m)):
            if grid[i][j] == 1:
                down[i][j] = (down[i + 1][j] + 1) if i < n - 1 else 1
                right[i][j] = (right[i][j + 1] + 1) if j < m - 1 else 1

    # Find the largest plus sign
    max_k = 0
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 1:
                k = min(up[i][j], down[i][j], left[i][j], right[i][j])
                max_k = max(max_k, k)

    # Final size is (k - 1)
    return max_k - 1


##################################################################################################################################

"""You are given an array of integers strength, where strength[i] is the strength of the i-th athlete. They will be lined up in a
row for a relay race. Fatigue is calculated as the maximum absolute difference between the strengths of two adjacent athletes. Return
the minimum fatigue possible by rearranging the athletes.
"""


def minimize_max_adjacent_diff(heights):
    heights.sort()
    n = len(heights)
    arrangement = [0] * n
    left = (n - 1) // 2
    right = left + 1
    toggle = True  # Start from left

    for i in range(n - 1, -1, -1):
        if toggle:
            arrangement[left] = heights[i]
            left -= 1
        else:
            arrangement[right] = heights[i]
            right += 1
        toggle = not toggle

    max_diff = max(abs(arrangement[i] - arrangement[i + 1]) for i in range(n - 1))
    return max_diff


##################################################################################################################################

"""Implement a function in python that takes an input parameter as a string and returns a string such that if you give the input
as: "aaaaabbbccccaaddd", then the output should be: "a5b3c4a2d3". If you give the input as: "", the output should be "". If you
give the input as "abc", the output should be "a1b1c1"
"""


def cal_length(s: str) -> str:
    if not s:
        return ""

    result = []
    count = 1

    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            count += 1
        else:
            result.append(f"{s[i - 1]}{count}")
            count = 1

    result.append(f"{s[-1]}{count}")

    return "".join(result)


output = cal_length("aaaaabbbccccaaddd")
print(output)

##################################################################################################################################
##################################################################################################################################
##################################################################################################################################
##################################################################################################################################
##################################################################################################################################
