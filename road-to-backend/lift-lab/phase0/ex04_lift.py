"""ex04: Lift を計算する。Lift Lab の心臓部。

Lift = 条件成立日の円高率 - 全日の円高率（ベースライン）

例: 普段の円高率が 48%、条件が成立した日だけ見ると 60% なら Lift = +0.12（+12pt）。
ただし条件成立日が 5 日しかなければ、+12pt は偶然でも簡単に出る。
だから Lift と一緒に、必ず N（条件成立日数）を返す。
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class LiftResult:
    n_condition: int  # 条件成立日のうち、結果が分かっている日数
    n_total: int  # 結果が分かっている全日数
    conditional_rate: float | None  # 条件成立日の円高率。n_condition == 0 なら None
    base_rate: float | None  # 全日の円高率。n_total == 0 なら None
    lift: float | None  # conditional_rate - base_rate。どちらかが None なら None


def compute_lift(flags: list[bool], outcomes: list[bool | None]) -> LiftResult:
    """Lift を計算する。

    flags[i]:    i 日目に条件が成立したか
    outcomes[i]: i 日目から N 日後に円高になったか。未来のデータがない日は None

    outcomes が None の日は、分子からも分母からも除外する。
    flags と outcomes の長さが違えば ValueError を送出する。
    """
    raise NotImplementedError
