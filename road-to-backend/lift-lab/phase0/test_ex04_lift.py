import pytest

from ex04_lift import LiftResult, compute_lift


def test_basic_lift() -> None:
    flags = [True, True, False, False, True, False]
    outcomes: list[bool | None] = [True, True, False, True, False, False]
    result = compute_lift(flags, outcomes)
    assert result.n_condition == 3
    assert result.n_total == 6
    assert result.conditional_rate == pytest.approx(2 / 3)
    assert result.base_rate == pytest.approx(3 / 6)
    assert result.lift == pytest.approx(2 / 3 - 3 / 6)


def test_none_outcomes_are_excluded() -> None:
    flags = [True, False, True, False]
    outcomes: list[bool | None] = [True, False, None, None]
    result = compute_lift(flags, outcomes)
    assert result.n_condition == 1
    assert result.n_total == 2
    assert result.conditional_rate == pytest.approx(1.0)
    assert result.base_rate == pytest.approx(0.5)
    assert result.lift == pytest.approx(0.5)


def test_condition_never_holds() -> None:
    result = compute_lift([False, False], [True, False])
    assert result == LiftResult(
        n_condition=0, n_total=2, conditional_rate=None, base_rate=0.5, lift=None
    )


def test_empty() -> None:
    assert compute_lift([], []) == LiftResult(
        n_condition=0, n_total=0, conditional_rate=None, base_rate=None, lift=None
    )


def test_length_mismatch() -> None:
    with pytest.raises(ValueError):
        compute_lift([True], [True, False])
