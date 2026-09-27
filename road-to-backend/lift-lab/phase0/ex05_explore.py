"""ex05: 実データで「円高になりやすい曜日・月」を探す。

実行: uv run python phase0/ex05_explore.py

テストはない。集計結果を見て、README の問いに自分の言葉で答えること。
"""

from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "usdjpy.parquet"
HORIZON_DAYS = 20  # 何営業日後のリターンを見るか


def main() -> None:
    # TODO 1: DATA_PATH の parquet を pandas で読み込み、shape・dtypes・先頭5行を表示する
    # TODO 2: observed_at で昇順に並べ、HORIZON_DAYS 営業日後のリターン列を作る
    #         （ヒント: Series.shift。ex02 の forward_returns と同じことを 1 行で）
    # TODO 3: 「円高になったか」の bool 列を作る。未来がない行はどう扱う？
    # TODO 4: 曜日別に「円高率」と「N」を表示する
    # TODO 5: 月別に「円高率」と「N」を表示する
    # TODO 6（発展）: README の「月ラベルのシャッフル実験」をやってみる
    raise NotImplementedError


if __name__ == "__main__":
    main()
