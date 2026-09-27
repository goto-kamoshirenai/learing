"""ex03: JSON から来た「条件」を検証して、型のついた値に変換する。

Lambda では、リクエストボディは json.loads した dict としてしか手に入らない。
中身が正しい保証はどこにもないので、信用せずに 1 つずつ確かめる必要がある。
Phase 2 の解析 API は、ここで書く関数をそのまま使う。
"""

from dataclasses import dataclass
from typing import Literal

Operator = Literal[">", "<"]

ALLOWED_SERIES = frozenset({"attention_z", "temp_deviation", "cftc_net_position"})
MAX_CONDITIONS = 3


class ValidationError(Exception):
    """入力が不正なときに送出する。message には「どのフィールドが、なぜ」ダメかを書く。"""


@dataclass(frozen=True)
class Condition:
    series: str
    op: Operator
    threshold: float


def parse_condition(raw: dict[str, object]) -> Condition:
    """1 件分の dict を検証して Condition を返す。

    >>> parse_condition({"series": "attention_z", "op": ">", "threshold": 1.5})
    Condition(series='attention_z', op='>', threshold=1.5)

    ルール:
    - series は ALLOWED_SERIES のどれか
    - op は ">" か "<"
    - threshold は数値。int は float に変換して受け入れる。文字列や bool は不可
    - 余計なキーは無視してよい
    どれかに違反したら ValidationError を送出する。
    """
    raise NotImplementedError


def parse_conditions(raw: object) -> list[Condition]:
    """条件のリストを検証する。

    raw がリストでない、または要素数が 1〜MAX_CONDITIONS の範囲外なら ValidationError。
    各要素が dict でなければ ValidationError。
    要素ごとのエラーは、何番目の条件かが分かるメッセージにする（例: "conditions[1].op: ..."）。
    """
    raise NotImplementedError


def matches(condition: Condition, value: float) -> bool:
    """value が条件を満たすかを返す。"""
    raise NotImplementedError
