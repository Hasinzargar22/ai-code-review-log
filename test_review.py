"""Tests run against BOTH the AI version and the fixed version of every function.

- both(...):     both versions must pass
- ai_fails(...): exposes a bug - the AI version must FAIL (strict xfail), the fixed version must PASS
"""
import sqlite3
import pytest

import ai_solutions as ai_mod
import fixed_solutions as fixed_mod


def both(ai_fn, fixed_fn):
    return [pytest.param(ai_fn, id="ai"), pytest.param(fixed_fn, id="fixed")]


def ai_fails(ai_fn, fixed_fn, reason):
    return [
        pytest.param(ai_fn, id="ai", marks=pytest.mark.xfail(strict=True, reason=reason)),
        pytest.param(fixed_fn, id="fixed"),
    ]


# ===== Problem 01: binary_search =====
@pytest.mark.parametrize("fn", both(ai_mod.binary_search, fixed_mod.binary_search))
def test_p01_middle_element(fn):
    assert fn([1, 3, 5, 7, 9], 5) == 2

@pytest.mark.parametrize("fn", both(ai_mod.binary_search, fixed_mod.binary_search))
def test_p01_missing(fn):
    assert fn([1, 3, 5], 4) == -1

@pytest.mark.parametrize("fn", ai_fails(ai_mod.binary_search, fixed_mod.binary_search, "off-by-one: loop exits before checking lo == hi"))
def test_p01_last_element(fn):
    assert fn([1, 3, 5, 7, 9], 9) == 4

@pytest.mark.parametrize("fn", ai_fails(ai_mod.binary_search, fixed_mod.binary_search, "single-element list is never checked"))
def test_p01_single_element(fn):
    assert fn([42], 42) == 0


# ===== Problem 02: is_palindrome =====
@pytest.mark.parametrize("fn", both(ai_mod.is_palindrome, fixed_mod.is_palindrome))
def test_p02_simple(fn):
    assert fn("Racecar") is True
    assert fn("hello") is False

@pytest.mark.parametrize("fn", ai_fails(ai_mod.is_palindrome, fixed_mod.is_palindrome, "ignores the spec: spaces and punctuation are not removed"))
def test_p02_sentence(fn):
    assert fn("A man, a plan, a canal: Panama") is True


# ===== Problem 03: merge_intervals =====
@pytest.mark.parametrize("fn", both(ai_mod.merge_intervals, fixed_mod.merge_intervals))
def test_p03_sorted_input(fn):
    assert fn([[1, 3], [2, 6], [8, 10]]) == [[1, 6], [8, 10]]

@pytest.mark.parametrize("fn", ai_fails(ai_mod.merge_intervals, fixed_mod.merge_intervals, "assumes input is already sorted"))
def test_p03_unsorted_input(fn):
    assert fn([[8, 10], [1, 3], [2, 6]]) == [[1, 6], [8, 10]]


# ===== Problem 04: second_largest =====
@pytest.mark.parametrize("fn", both(ai_mod.second_largest, fixed_mod.second_largest))
def test_p04_basic(fn):
    assert fn([3, 9, 4, 7]) == 7
    assert fn([5]) is None

@pytest.mark.parametrize("fn", ai_fails(ai_mod.second_largest, fixed_mod.second_largest, "duplicates of the max are not removed"))
def test_p04_duplicates(fn):
    assert fn([9, 9, 4]) == 4

@pytest.mark.parametrize("fn", ai_fails(ai_mod.second_largest, fixed_mod.second_largest, "all-equal list should have no second largest"))
def test_p04_all_equal(fn):
    assert fn([2, 2, 2]) is None


# ===== Problem 05: flatten =====
@pytest.mark.parametrize("fn", ai_fails(ai_mod.flatten, fixed_mod.flatten, "mutable default argument leaks state between calls"))
def test_p05_called_twice(fn):
    assert fn([1, [2, [3]]]) == [1, 2, 3]
    assert fn([4, [5]]) == [4, 5]


# ===== Problem 06: average =====
@pytest.mark.parametrize("fn", both(ai_mod.average, fixed_mod.average))
def test_p06_basic(fn):
    assert fn([2, 4, 6]) == 4

@pytest.mark.parametrize("fn", ai_fails(ai_mod.average, fixed_mod.average, "ZeroDivisionError on empty input"))
def test_p06_empty(fn):
    assert fn([]) == 0.0


# ===== Problem 07: two_sum =====
@pytest.mark.parametrize("fn", both(ai_mod.two_sum, fixed_mod.two_sum))
def test_p07_basic(fn):
    assert fn([2, 7, 11, 15], 9) == (0, 1)

@pytest.mark.parametrize("fn", ai_fails(ai_mod.two_sum, fixed_mod.two_sum, "reuses the same element (i == j)"))
def test_p07_no_reuse(fn):
    assert fn([3, 2, 4], 6) == (1, 2)


# ===== Problem 08: is_prime =====
@pytest.mark.parametrize("fn", both(ai_mod.is_prime, fixed_mod.is_prime))
def test_p08_examples_from_prompt(fn):
    # The AI version passes these only because it memorised them.
    assert fn(2) and fn(7) and fn(13)
    assert not fn(1) and not fn(9)

@pytest.mark.parametrize("fn", ai_fails(ai_mod.is_prime, fixed_mod.is_prime, "hard-coded answers: only works for the example inputs"))
def test_p08_unseen_primes(fn):
    assert fn(17) and fn(97) and fn(7919)


# ===== Problem 09: find_user =====
@pytest.fixture
def conn():
    c = sqlite3.connect(":memory:")
    c.execute("CREATE TABLE users (id INTEGER, name TEXT)")
    c.executemany("INSERT INTO users VALUES (?, ?)", [(1, "alice"), (2, "bob"), (3, "o'neil")])
    yield c
    c.close()

@pytest.mark.parametrize("fn", both(ai_mod.find_user, fixed_mod.find_user))
def test_p09_normal_lookup(fn, conn):
    assert fn(conn, "alice") == [(1, "alice")]

@pytest.mark.parametrize("fn", ai_fails(ai_mod.find_user, fixed_mod.find_user, "SQL injection: input changes the query and leaks every row"))
def test_p09_injection(fn, conn):
    assert fn(conn, "x' OR '1'='1") == []

@pytest.mark.parametrize("fn", ai_fails(ai_mod.find_user, fixed_mod.find_user, "an apostrophe in a real name breaks the query"))
def test_p09_apostrophe(fn, conn):
    assert fn(conn, "o'neil") == [(3, "o'neil")]


# ===== Problem 10: word_count =====
@pytest.mark.parametrize("fn", both(ai_mod.word_count, fixed_mod.word_count))
def test_p10_basic(fn):
    assert fn("the cat the dog") == {"the": 2, "cat": 1, "dog": 1}

@pytest.mark.parametrize("fn", ai_fails(ai_mod.word_count, fixed_mod.word_count, "split(' ') creates empty-string words and misses newlines"))
def test_p10_messy_whitespace(fn):
    assert fn("The  cat\nthe dog") == {"the": 2, "cat": 1, "dog": 1}
