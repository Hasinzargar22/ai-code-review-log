# AI Code Review & Red-Teaming Log

A small project where I give coding problems to AI assistants, test their answers like a code reviewer would, and document how and why they fail.

AI coding assistants often produce code that **looks right and passes the obvious example** but breaks on edge cases, hides assumptions, fakes test passes, or is unsafe. This repo collects 10 such cases with tests that prove each bug.

## What's inside

```
ai_solutions.py      the AI's original code for all 10 problems, unchanged (bugs included)
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
- the **AI version is expected to fail**, marked `xfail(strict=True)`, so if it ever passes, the suite breaks
- the **fixed version must pass**

## Run it

```bash
pip install -r requirements.txt
pytest
```

Expected result: `33 passed, 13 xfailed`. That means 13 bugs were confirmed in the AI code and all the fixes work.

## Tech
Python 3 · pytest · sqlite3 · Git

See **[REVIEW_LOG.md](REVIEW_LOG.md)** for the full analysis.
