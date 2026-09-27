import dataclasses

import pytest

from ex03_condition import Condition, ValidationError, matches, parse_condition, parse_conditions


def test_parse_valid() -> None:
    raw: dict[str, object] = {"series": "attention_z", "op": ">", "threshold": 1.5}
    assert parse_condition(raw) == Condition(series="attention_z", op=">", threshold=1.5)


def test_parse_int_threshold_becomes_float() -> None:
    condition = parse_condition({"series": "temp_deviation", "op": "<", "threshold": 2})
    assert condition.threshold == 2.0
    assert isinstance(condition.threshold, float)


def test_parse_ignores_extra_keys() -> None:
    raw: dict[str, object] = {"series": "attention_z", "op": ">", "threshold": 1.0, "memo": "x"}
    assert parse_condition(raw).series == "attention_z"


@pytest.mark.parametrize(
    ("raw", "field"),
    [
        ({"op": ">", "threshold": 1.0}, "series"),
        ({"series": "bitcoin", "op": ">", "threshold": 1.0}, "series"),
        ({"series": "attention_z", "threshold": 1.0}, "op"),
        ({"series": "attention_z", "op": ">=", "threshold": 1.0}, "op"),
        ({"series": "attention_z", "op": ">"}, "threshold"),
        ({"series": "attention_z", "op": ">", "threshold": "1.5"}, "threshold"),
        ({"series": "attention_z", "op": ">", "threshold": True}, "threshold"),
        ({"series": "attention_z", "op": ">", "threshold": None}, "threshold"),
    ],
)
def test_parse_invalid_mentions_field(raw: dict[str, object], field: str) -> None:
    with pytest.raises(ValidationError, match=field):
        parse_condition(raw)


def test_condition_is_immutable() -> None:
    condition = Condition(series="attention_z", op=">", threshold=1.0)
    with pytest.raises(dataclasses.FrozenInstanceError):
        condition.threshold = 2.0  # type: ignore[misc]


def test_parse_conditions_valid() -> None:
    raw = [
        {"series": "attention_z", "op": ">", "threshold": 0.7},
        {"series": "temp_deviation", "op": ">", "threshold": 3.5},
    ]
    assert [c.series for c in parse_conditions(raw)] == ["attention_z", "temp_deviation"]


@pytest.mark.parametrize(
    "raw",
    [
        "attention_z > 1",
        {"series": "attention_z", "op": ">", "threshold": 1.0},
        [],
        [{"series": "attention_z", "op": ">", "threshold": float(i)} for i in range(4)],
        ["not a dict"],
    ],
)
def test_parse_conditions_invalid(raw: object) -> None:
    with pytest.raises(ValidationError):
        parse_conditions(raw)


def test_parse_conditions_error_mentions_index() -> None:
    raw = [
        {"series": "attention_z", "op": ">", "threshold": 0.7},
        {"series": "attention_z", "op": "=", "threshold": 0.7},
    ]
    with pytest.raises(ValidationError, match=r"conditions\[1\]"):
        parse_conditions(raw)


@pytest.mark.parametrize(
    ("op", "value", "expected"),
    [(">", 1.1, True), (">", 1.0, False), ("<", 0.9, True), ("<", 1.0, False)],
)
def test_matches(op: str, value: float, expected: bool) -> None:
    condition = parse_condition({"series": "attention_z", "op": op, "threshold": 1.0})
    assert matches(condition, value) is expected
