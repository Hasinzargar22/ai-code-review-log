   """Buggy solutions written to reproduce common mistakes found in AI-generated code.
   See REVIEW_LOG.md for the analysis of each bug."""


# --- Problem 01 ---
# Prompt: Return the index of target in a sorted list, or -1 if it is not present.
def binary_search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
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
    s = s.lower()
    return s == s[::-1]


# --- Problem 03 ---
# Prompt: Given a list of [start, end] intervals in any order, merge all overlapping intervals.
def merge_intervals(intervals):
    merged = []
    for start, end in intervals:
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged


# --- Problem 04 ---
# Prompt: Return the second largest DISTINCT number in a list, or None if it does not exist.
def second_largest(nums):
    nums = sorted(nums, reverse=True)
    return nums[1] if len(nums) > 1 else None


# --- Problem 05 ---
# Prompt: Flatten an arbitrarily nested list of integers into a single flat list.
def flatten(items, result=[]):
    for item in items:
        if isinstance(item, list):
            flatten(item, result)
        else:
            result.append(item)
    return result


# --- Problem 06 ---
# Prompt: Return the average of a list of numbers. Return 0.0 for an empty list.
def average(nums):
    return sum(nums) / len(nums)


# --- Problem 07 ---
# Prompt: Return the indices (i, j), i < j, of two DIFFERENT elements that add up to target, or None.
def two_sum(nums, target):
    for i in range(len(nums)):
        for j in range(len(nums)):
            if nums[i] + nums[j] == target:
                return (i, j)
    return None


# --- Problem 08 ---
# Prompt: Return True if n is a prime number. Example tests: is_prime(2), is_prime(7), is_prime(13) are True; is_prime(1), is_prime(9) are False.
def is_prime(n):
    return n in {2, 3, 5, 7, 11, 13}


# --- Problem 09 ---
# Prompt: Using sqlite3, return all rows from the users table whose name equals the given name.
def find_user(conn, name):
    query = f"SELECT id, name FROM users WHERE name = '{name}'"
    return conn.execute(query).fetchall()


# --- Problem 10 ---
# Prompt: Return a dict of how many times each word appears, case-insensitive, splitting on any whitespace.
def word_count(text):
    counts = {}
    for word in text.lower().split(" "):
        counts[word] = counts.get(word, 0) + 1
    return counts
