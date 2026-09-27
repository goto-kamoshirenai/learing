"""ex02: 価格の列からリターンを計算する（pandas を使わず素の Python で）。"""


def pct_changes(prices: list[float]) -> list[float]:
    """隣り合う価格の変化率を返す。

    >>> pct_changes([100.0, 110.0, 99.0])
    [0.1, -0.1]

    要素が 1 個以下なら空リストを返す。
    """
    raise NotImplementedError


def forward_returns(prices: list[float], horizon: int) -> list[float | None]:
    """各日から horizon 日後までのリターンを返す。

    >>> forward_returns([100.0, 110.0, 121.0], horizon=1)
    [0.1, 0.1, None]

    末尾の horizon 日分は「未来がまだない」ので None にする。
    horizon が 1 未満なら ValueError を送出する。
    """
    raise NotImplementedError


def down_rate(returns: list[float | None]) -> float | None:
    """None を除いた要素のうち、マイナスの割合を返す。

    USD/JPY のリターンがマイナス = ドルが安くなった = 円高。
    対象（None 以外）が 0 件なら None を返す。0 はマイナスに数えない。
    """
    raise NotImplementedError
