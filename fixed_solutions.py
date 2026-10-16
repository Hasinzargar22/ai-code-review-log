"""Reviewed and corrected versions of the AI solutions."""
from collections import Counter


# --- Problem 01 ---
# Prompt: Return the index of target in a sorted list, or -1 if it is not present.
def binary_search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:  # must include lo == hi, otherwise the last candidate is never checked
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


# --- Problem 02 ---
# Prompt: Return True if the string is a palindrome, ignoring case, spaces and punctuation.
def is_palindrome(s):
    cleaned = [c.lower() for c in s if c.isalnum()]
    return cleaned == cleaned[::-1]


# --- Problem 03 ---
# Prompt: Given a list of [start, end] intervals in any order, merge all overlapping intervals.
def merge_intervals(intervals):
    merged = []
    for start, end in sorted(intervals):  # input is unordered, so sort by start first
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged


# --- Problem 04 ---
# Prompt: Return the second largest DISTINCT number in a list, or None if it does not exist.
def second_largest(nums):
    distinct = sorted(set(nums), reverse=True)
    return distinct[1] if len(distinct) > 1 else None


# --- Problem 05 ---
# Prompt: Flatten an arbitrarily nested list of integers into a single flat list.
def flatten(items, result=None):
    if result is None:  # a mutable default would be shared between calls
        result = []
    for item in items:
        if isinstance(item, list):
            flatten(item, result)
        else:
            result.append(item)
    return result


# --- Problem 06 ---
# Prompt: Return the average of a list of numbers. Return 0.0 for an empty list.
def average(nums):
    if not nums:
        return 0.0
    return sum(nums) / len(nums)


# --- Problem 07 ---
# Prompt: Return the indices (i, j), i < j, of two DIFFERENT elements that add up to target, or None.
def two_sum(nums, target):
    seen = {}  # value -> index; O(n) instead of O(n^2)
    for j, x in enumerate(nums):
        if target - x in seen:
            return (seen[target - x], j)
        seen[x] = j
    return None


# --- Problem 08 ---
# Prompt: Return True if n is a prime number. Example tests: is_prime(2), is_prime(7), is_prime(13) are True; is_prime(1), is_prime(9) are False.
def is_prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


# --- Problem 09 ---
# Prompt: Using sqlite3, return all rows from the users table whose name equals the given name.
def find_user(conn, name):
    # Parameterised query: the driver escapes the value, so input cannot change the SQL.
    return conn.execute("SELECT id, name FROM users WHERE name = ?", (name,)).fetchall()


# --- Problem 10 ---
# Prompt: Return a dict of how many times each word appears, case-insensitive, splitting on any whitespace.
def word_count(text):
    return dict(Counter(text.lower().split()))  # split() with no argument handles any whitespace
