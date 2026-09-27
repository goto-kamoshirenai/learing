import pytest

from ex02_returns import down_rate, forward_returns, pct_changes


def test_pct_changes_basic() -> None:
    assert pct_changes([100.0, 110.0, 99.0]) == pytest.approx([0.1, -0.1])


@pytest.mark.parametrize("prices", [[], [100.0]])
def test_pct_changes_too_short(prices: list[float]) -> None:
    assert pct_changes(prices) == []


def test_forward_returns_horizon_1() -> None:
    result = forward_returns([100.0, 110.0, 121.0], horizon=1)
    assert result[:2] == pytest.approx([0.1, 0.1])
    assert result[2] is None


def test_forward_returns_horizon_2() -> None:
    result = forward_returns([100.0, 110.0, 120.0, 90.0], horizon=2)
    assert result[:2] == pytest.approx([120.0 / 100.0 - 1, 90.0 / 110.0 - 1])
    assert result[2:] == [None, None]


def test_forward_returns_keeps_length() -> None:
    prices = [float(p) for p in range(1, 11)]
    assert len(forward_returns(prices, horizon=3)) == len(prices)


def test_forward_returns_horizon_longer_than_prices() -> None:
    assert forward_returns([100.0, 101.0], horizon=5) == [None, None]


@pytest.mark.parametrize("horizon", [0, -1])
def test_forward_returns_invalid_horizon(horizon: int) -> None:
    with pytest.raises(ValueError):
        forward_returns([100.0, 110.0], horizon=horizon)


def test_down_rate_ignores_none_and_zero_is_not_down() -> None:
    assert down_rate([-0.1, 0.2, None, 0.0, -0.3]) == pytest.approx(0.5)


@pytest.mark.parametrize("returns", [[], [None, None]])
def test_down_rate_no_data(returns: list[float | None]) -> None:
    assert down_rate(returns) is None
