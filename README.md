# AI Code Review & Red-Teaming Log

A small project that reproduces common bugs found in AI-generated code, tests each one like a code reviewer would, and documents how and why it fails.

AI coding assistants often produce code that **looks right and passes the obvious example** but breaks on edge cases, hides assumptions, fakes test passes, or is unsafe. This repo collects 10 curated examples of these mistakes, written by me to mirror patterns AI assistants commonly produce, with tests that prove each bug.

## What's inside

```
ai_solutions.py      buggy versions of all 10 problems, written to reproduce common AI coding mistakes
fixed_solutions.py   my reviewed and corrected versions
test_review.py       46 pytest tests run against BOTH versions
REVIEW_LOG.md        write-up of every bug: cause, severity and fix
```

Highlights:
- **Faked test pass:** a prime checker that hard-codes the example answers (problem 08)
- **Unsafe code:** an SQL lookup vulnerable to SQL injection (problem 09)
- **Classic logic bugs:** off-by-one, mutable default arguments, unsorted-input assumptions

## How the tests work

Each bug has a test that runs on both versions:
- the **buggy version is expected to fail**, marked `xfail(strict=True)`, so if it ever passes, the suite breaks
- the **fixed version must pass**

## Run it

```bash
pip install -r requirements.txt
pytest
```

Expected result: `33 passed, 13 xfailed`. That means all 13 bugs are confirmed in the buggy versions and all the fixes work.

## Tech
Python 3 · pytest · sqlite3 · Git

See **[REVIEW_LOG.md](REVIEW_LOG.md)** for the full analysis.
