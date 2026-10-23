"""Test suite for src/registration.py (Assignment 2).

This file is intentionally left for you to implement. See the assignment
handout for the required work:

  - Section 4: Statement and branch coverage (summarize_batch_registrations,
    enroll_student) -- close every gap your coverage report shows.
  - Section 5: Data-flow testing (defs/uses/DU pairs for `total_fees` in
    summarize_batch_registrations; All-Uses coverage).
  - Section 6: Test doubles (stub/mock notifier for enroll_student).

`registration` is importable directly (see pyproject.toml's `pythonpath`
setting), e.g.:

    from registration import (
        can_register,
        calculate_registration_fee,
        summarize_batch_registrations,
        enroll_student,
    )
"""

# TODO: implement your tests here.

import pytest
from src.registration import (
    summarize_batch_registrations,
    enroll_student,
)


# ---------------------------------------
# Statement and Branch Coverage Tests
# ---------------------------------------

@pytest.mark.boundary
def test_empty_batch():
    assert summarize_batch_registrations([]) == (0, 0.0)


@pytest.mark.positive
def test_single_approved_registration():
    requests = [(0, 3, True)]
    assert summarize_batch_registrations(requests) == (1, 300.0)


@pytest.mark.negative
def test_single_rejected_registration():
    requests = [(0, 3, False)]
    assert summarize_batch_registrations(requests) == (0, 0.0)


@pytest.mark.unit
def test_mixed_batch():
    requests = [
        (0, 3, True),
        (0, 3, False),
        (12, 3, True),
    ]

    assert summarize_batch_registrations(requests) == (2, 1725.0)


# ---------------------------------------
# Data-Flow Testing
# Loop-Carried DU Pair
# ---------------------------------------

@pytest.mark.positive
def test_two_approved_registrations():
    requests = [
        (0, 3, True),
        (12, 3, True),
    ]

    assert summarize_batch_registrations(requests) == (2, 1725.0)


# ---------------------------------------
# Test Doubles - Notifier
# ---------------------------------------

@pytest.mark.positive
def test_enroll_student_approved(mock_notifier):
    result = enroll_student(0, 3, True, mock_notifier)

    assert result is True
    mock_notifier.send_confirmation.assert_called_once_with(300.0)
    mock_notifier.send_rejection.assert_not_called()


@pytest.mark.negative
def test_enroll_student_rejected(mock_notifier):
    result = enroll_student(0, 3, False, mock_notifier)

    assert result is False
    mock_notifier.send_rejection.assert_called_once_with()
    mock_notifier.send_confirmation.assert_not_called()
