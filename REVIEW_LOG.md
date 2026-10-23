# AI Code Review Log

Each entry shows one coding problem with a solution written to reproduce a common bug in AI-generated code, how I tested it, what failed, why, and the fix.

**Severity scale:** High = wrong output or security risk on normal input · Medium = crashes or is wrong on an edge case · Low = works but inefficient or fragile

| # | Problem | Bug type | Severity | Caught by |
|---|---------|----------|----------|-----------|
| 01 | Binary search | Off-by-one loop condition | High | `test_p01_last_element`, `test_p01_single_element` |
| 02 | Palindrome check | Ignored part of the spec | Medium | `test_p02_sentence` |
| 03 | Merge intervals | Hidden assumption (sorted input) | High | `test_p03_unsorted_input` |
| 04 | Second largest | Duplicates not handled | Medium | `test_p04_duplicates`, `test_p04_all_equal` |
| 05 | Flatten list | Mutable default argument | High | `test_p05_called_twice` |
| 06 | Average | Crash on empty input | Medium | `test_p06_empty` |
| 07 | Two sum | Same element used twice; O(n²) | High | `test_p07_no_reuse` |
| 08 | Prime check | **Faked test pass** (hard-coded answers) | High | `test_p08_unseen_primes` |
| 09 | SQL user lookup | **SQL injection** (unsafe code) | High | `test_p09_injection`, `test_p09_apostrophe` |
| 10 | Word count | Wrong whitespace splitting | Medium | `test_p10_messy_whitespace` |

**Result:** All 10 solutions look correct and pass the simple example cases, but each one fails at least one edge-case test (13 bugs in total). These are curated examples of common AI coding mistakes, not a random sample of AI output.

---

## 01 · Binary search
- **Prompt:** Return the index of `target` in a sorted list, or -1.
- **The bug:** Uses `while lo < hi` with `hi = len(nums) - 1`.
- **Failure:** When the search narrows to one remaining element (`lo == hi`), the loop exits without checking it. Searching for the last element, or anything in a one-item list, returns -1.
- **Why it's dangerous:** It passes the "obvious" test (finding a middle element), so it looks correct at a glance.
- **Fix:** `while lo <= hi`.

## 02 · Palindrome check
- **Prompt:** Ignore case, spaces and punctuation.
- **The bug:** Lowercases the string but keeps spaces and punctuation.
- **Failure:** `"A man, a plan, a canal: Panama"` returns False.
- **Fix:** Keep only alphanumeric characters before comparing.

## 03 · Merge intervals
- **Prompt:** Intervals arrive in any order.
- **The bug:** Merges neighbours without sorting first.
- **Failure:** `[[8,10],[1,3],[2,6]]` gives `[[8,10]]`. The intervals 1–6 are silently swallowed into 8–10, so data is lost.
- **Fix:** Sort by start time first (O(n log n)).

## 04 · Second largest
- **Prompt:** Second largest *distinct* number.
- **The bug:** Sorts and takes index 1.
- **Failure:** `[9, 9, 4]` returns 9 instead of 4, and `[2, 2, 2]` returns 2 instead of None.
- **Fix:** De-duplicate with `set()` before sorting.

## 05 · Flatten nested list
- **The bug:** `def flatten(items, result=[])`.
- **Failure:** Python creates the default list once and shares it between calls. The second call returns the results of the first call too: `[1, 2, 3, 4, 5]`.
- **Why it's dangerous:** It only fails the second time the function runs, so a single test misses it.
- **Fix:** `result=None`, then create a new list inside the function.

## 06 · Average
- **Failure:** `average([])` raises `ZeroDivisionError`, but the prompt said to return 0.0.
- **Fix:** Guard against empty input.

## 07 · Two sum
- **Prompt:** Two *different* elements.
- **The bug:** A double loop where `i` and `j` both start at 0.
- **Failure:** `[3, 2, 4]` with target 6 returns `(0, 0)` (3 + 3, the same element twice).
- **Extra issue:** O(n²) time.
- **Fix:** One pass with a hash map: O(n) time, and the same index can never be reused.

## 08 · Prime check: faked test pass
- **The bug:** `return n in {2, 3, 5, 7, 11, 13}`.
- **Failure:** It passes every example from the prompt but returns False for 17, 97 and 7919. The solution fits the examples instead of solving the problem.
- **Why it's dangerous:** A test suite built only from the prompt's examples reports 100% passing.
- **How I caught it:** I wrote tests with inputs that were not in the prompt's examples.
- **Fix:** Trial division up to √n.

## 09 · SQL user lookup: SQL injection
- **The bug:** Builds the query with an f-string: `f"... WHERE name = '{name}'"`.
- **Failure 1 (security):** The input `x' OR '1'='1` returns every user in the table.
- **Failure 2 (correctness):** A real name with an apostrophe, `o'neil`, crashes the query.
- **Fix:** A parameterised query (`WHERE name = ?`), so user input can never change the SQL.

## 10 · Word count
- **The bug:** `text.split(" ")`.
- **Failure:** Double spaces create an empty-string "word", and newlines are not treated as separators.
- **Fix:** `text.split()` with no argument handles any whitespace.

---

## Patterns these examples show
1. **Bugs hide off the happy path.** Every solution works on the simplest example; the bugs only appear on edge cases (empty input, duplicates, boundaries, unusual whitespace).
2. **Hidden assumptions:** sorted input, distinct values, clean text. AI-generated code often doesn't state these.
3. **Spec drift:** part of the requirement gets dropped (palindrome punctuation, "distinct" in second largest).
4. **Overfitting to examples** can make a solution look tested when it isn't (problem 08).
5. **Security is not the default:** string-built SQL is still a common pattern (problem 09).

**Review checklist I now use:** empty input · single element · duplicates · boundaries (first/last) · unsorted or unusual input · inputs not shown in the prompt · calling the function twice · untrusted user input.
