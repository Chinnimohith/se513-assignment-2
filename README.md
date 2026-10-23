# Assignment 2 — Coverage, Data-Flow Testing, and Test Doubles

SE 413/513 — Software Testing

## Project Overview

This assignment tests the Course Registration System using pytest, statement and branch coverage, data-flow testing, and test doubles.

The provided `src/registration.py` remains unchanged. The two functions tested are:

- `summarize_batch_registrations(requests)` — processes multiple registration requests and returns the number of approved registrations and total fees.
- `enroll_student(current_credits, course_credits, prerequisite_met, notifier)` — processes an enrollment request and notifies the student of approval or rejection.

## Project Structure

```text
assignment-2/
├── src/
│   └── registration.py
├── tests/
│   ├── test_registration.py
│   └── conftest.py
├── pyproject.toml
└── README.md
```

## Setup and Installation

Install the required packages:

```bash
python -m pip install pytest pytest-cov
```

Run all tests from the project root:

```bash
python -m pytest -v
```

## 1. Statement Coverage

Statement coverage verifies that every executable statement in the target functions is executed by the tests.

Command:

```bash
python -m pytest --cov --cov-report=term-missing
```

For the statement-only report, `branch = false` was temporarily set in `pyproject.toml`. After generating the report, the original `branch = true` setting was restored.

### Final Statement Coverage Results

```text
Name                  Stmts   Miss   Cover   Missing
----------------------------------------------------
src\registration.py      36      4     89%   25, 28, 31, 50
----------------------------------------------------
TOTAL                    36      4     89%

7 passed
```

The four uncovered lines belong to the older Assignment 1 functions. Both new Assignment 2 functions have no missing statements.

## 2. Branch Coverage

Branch coverage verifies that each possible decision outcome is executed.

Command:

```bash
python -m pytest --cov --cov-branch --cov-report=term-missing
```

### Final Branch Coverage Results

```text
Name                  Stmts   Miss   Branch   BrPart   Cover   Missing
---------------------------------------------------------------------
src\registration.py      36      4       18        4     85%   25, 28, 31, 50
---------------------------------------------------------------------
TOTAL                    36      4       18        4     85%

7 passed
```

The remaining uncovered statements and partial branches are associated with the older Assignment 1 functions. The two Assignment 2 functions have no missing branches.

### Decision Coverage Explanation

**summarize_batch_registrations():**

The `test_empty_batch` test covers the loop when there are no requests, while `test_single_approved_registration` and `test_two_approved_registrations` exercise loop iterations.

The approval condition evaluates to True in `test_single_approved_registration` and False in `test_single_rejected_registration`. The `test_mixed_batch` test also verifies both outcomes within the same batch.

**enroll_student():**

The `test_enroll_student_approved` test exercises the successful enrollment branch, while `test_enroll_student_rejected` exercises the rejection branch.

## 3. Data-Flow Testing — total_fees

Data-flow testing identifies where variables are defined and used during program execution.

The `total_fees` variable has two definitions and two uses.

| ID | Type | Description |
|---|---|---|
| D1 | Definition | `total_fees = 0.0` initializes the variable before the loop |
| D2 | Definition | `total_fees = total_fees + calculate_registration_fee(total_credits)` updates the accumulated fees |
| U1 | Computational use | The current value of `total_fees` is read during accumulation |
| U2 | Computational use | `total_fees` is read in the return statement |

### Definition-Use (DU) Pair Table

| DU Pair | Description | Test |
|---|---|---|
| D1 → U1 | Initial value is used during the first approved registration | `test_single_approved_registration` |
| D1 → U2 | Initial value reaches the return statement without accumulation | `test_empty_batch` |
| D2 → U1 | Accumulated value from one iteration is used in a later iteration | `test_two_approved_registrations` |
| D2 → U2 | Updated total is returned after an approved registration | `test_single_approved_registration` |

### Loop-Carried DU Pair

The `test_two_approved_registrations` test processes two approved requests:

```python
requests = [
    (0, 3, True),
    (12, 3, True),
]
```

The first approved request produces a fee of $300. The second produces a fee of $1,425. The expected accumulated total is $1,725.

A batch with zero approved requests cannot execute the accumulation statement, while a batch with only one approved request cannot reuse the accumulated value in a later iteration. Therefore, at least two approved requests are necessary to cover the loop-carried D2 → U1 pair, which is required for All-Uses coverage.

## 4. Test Doubles — Mock Notifier

The `enroll_student()` function depends on a notifier collaborator. A `unittest.mock.Mock` fixture is used to test the function without sending real notifications.

The fixture is defined in `tests/conftest.py`.

### Positive Test

`test_enroll_student_approved` verifies that:

- The function returns `True`.
- `send_confirmation(300.0)` is called exactly once.
- `send_rejection()` is never called.

### Negative Test

`test_enroll_student_rejected` verifies that:

- The function returns `False`.
- `send_rejection()` is called exactly once without arguments.
- `send_confirmation()` is never called.

These tests demonstrate state verification through return values and behavior verification through Mock method-call assertions.

## 5. Test Organization and Markers

Every new test uses a registered pytest marker.

The markers include `unit`, `positive`, `negative`, and `boundary`.

Run the complete test suite:

```bash
python -m pytest -v
```

Run positive tests only:

```bash
python -m pytest -m positive
```

Run negative tests only:

```bash
python -m pytest -m negative
```

Run boundary tests only:

```bash
python -m pytest -m boundary
```

## 6. Final Test Results

The complete test suite was executed from the project root.

**Results:**

- 7 tests passed.
- Overall statement coverage: 89%.
- Overall branch-inclusive coverage: 85%.
- Both Assignment 2 target functions have full statement and branch coverage.
- The required loop-carried DU pair is tested.
- Positive and negative Mock notifier tests pass.
- All new tests use pytest markers.

The original business logic in `src/registration.py` was not modified.

## Conclusion

This assignment demonstrates statement and branch coverage, data-flow analysis, and the use of test doubles in a Course Registration System. The tests cover the required behaviors of both new functions, including batch processing, fee accumulation, enrollment decisions, and notification interactions.
