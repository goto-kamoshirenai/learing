# Phase 0: TS 経験者のための Python 速習

ゴールは、**実データで「円高になりやすい月」を自分で集計し、それが偶然かどうかを疑えるようになる**こと。
ex02〜ex04 で書く関数は、Phase 2 の解析 API でそのまま使う。

## 進め方

1. テストが先に用意されている。`NotImplementedError` の部分を実装して、テストを通す
2. 1 問できるたびに「ex02 できた」とコーチに伝える。コードレビューをして、次のヒントを出す
3. 詰まったら 15 分で止めて質問してよい。答えではなく、ヒントから返す

## セットアップ

`lift-lab/` で実行する（npm に相当するのが uv）。

```powershell
cd road-to-backend/lift-lab
uv add --dev pytest ruff      # npm i -D に相当。.venv が作られ、uv.lock が生成される
uv run pytest phase0          # 全部失敗すれば準備完了（まだ何も実装していないので）
uv run pytest phase0/test_ex02_returns.py -v   # 1 ファイルだけ実行
uv run ruff check phase0      # lint（ESLint に相当）
uv run ruff format phase0     # 整形（Prettier に相当）
```

VS Code を使うなら、Python 拡張（Pylance）の設定 `python.analysis.typeCheckingMode` を `"standard"` にする。
Python は型ヒントを**実行時に一切チェックしない**ので、型の誤りはエディタで拾うしかない。

## TS → Python 早見表

| TypeScript | Python | メモ |
|---|---|---|
| `const xs: number[] = [1, 2]` | `xs: list[int] = [1, 2]` | 定数という概念はない。定数は大文字の名前にする慣習だけ |
| `string \| null` | `str \| None` | |
| `type Op = ">" \| "<"` | `Op = Literal[">", "<"]` | |
| `Record<string, number>` | `dict[str, int]` | |
| `readonly` なオブジェクト型 | `@dataclass(frozen=True)` | TS の class と違い、Python では dataclass が普通の道具 |
| `xs.map(x => x * 2)` | `[x * 2 for x in xs]` | 内包表記。`filter` も `[x for x in xs if x > 0]` と書ける |
| `xs.length` | `len(xs)` | |
| `xs.slice(1, 3)` | `xs[1:3]` | `xs[-1]` で末尾 |
| `for (const [i, x] of xs.entries())` | `for i, x in enumerate(xs):` | |
| 2 つの配列を同時に回す | `for a, b in zip(xs, ys):` | |
| `throw new Error("...")` | `raise ValueError("...")` | |
| `try {} catch (e) {}` | `try: ... except ValueError as e: ...` | |
| `typeof x === "number"` | `isinstance(x, (int, float))` | **`bool` は `int` の一種**なので `True` も通ってしまう（ex03 の罠） |
| `JSON.parse(s)` | `json.loads(s)` | |
| `` `${x}円` `` | `f"{x}円"` | |
| `===` | `==`（値の比較） / `is`（同一性。`None` の判定に使う） | |

## 課題

### ex01: ウォームアップ（`ex01_type_hints.py`）

以前書いたコードを持ってきた。実行すると一応動くが、問題が 3 つある。

1. `price: int = 100.1` と書いてもエラーにならないのはなぜ？ どうすれば気づける？
2. 税込価格の計算が間違っている。100 円で税率 10% なら 110 円になるように直す。
   `tax` を「10」で持つか「0.1」で持つか、名前と型をどう付けるかも考える
3. `uv run ruff check phase0/ex01_type_hints.py` で出る指摘の意味を調べて直す。
   続けて `uv run ruff format --diff phase0/ex01_type_hints.py` で、Python の書式の慣習（PEP 8）がどう違うかを見る

### ex02: リターンを計算する（`ex02_returns.py`）

リスト、スライス、`zip`、内包表記、`None` の扱いを学ぶ。pandas を使わずに書く。

### ex03: 入力を疑う（`ex03_condition.py`）

`dataclass`、`Literal`、独自例外、`isinstance` を学ぶ。実務の Lambda で一番多く書くことになる種類のコード。

<details>
<summary>ヒント（詰まったら開く）</summary>

- `raw.get("op")` はキーがなければ `None` を返す。`raw["op"]` は `KeyError` を送出する
- `op` の値が `">"` か `"<"` かを確かめたあとでも、型チェッカーはまだ `str` だと思っている。
  `typing.cast` を使うか、`if op == ">" or op == "<":` の中で使うと型が絞り込まれる
- ある例外を別の例外で包み直すときは `raise ValidationError(...) from e`

</details>

### ex04: Lift を計算する（`ex04_lift.py`）

ex02 と ex03 の総仕上げ。`zip` と `sum` をうまく使うと短く書ける。

### ex05: 実データで遊ぶ（`ex05_explore.py`）

先に `uv add pandas pyarrow` を実行する。pyarrow は parquet を読むためのライブラリ。

コードの中の TODO を順番に進めて、次の問いに答える。

1. 20 営業日後に円高になっていた割合は、全期間で何 % か
2. 曜日別に見ると、一番円高になりやすいのは何曜日か。N はいくつか
3. 月別に見ると、一番円高になりやすいのは何月か。ベースラインとの差（Lift）は何 pt か
4. **3 の月は「円高になりやすい月」だと言ってよいか？**

**発展: 月ラベルのシャッフル実験**

月のラベルをランダムに並べ替えて（`numpy.random.default_rng(42).permutation`）、同じ月別集計を 1000 回繰り返す。
各回の「12 か月中で最大の Lift」を記録し、その分布と、実データで見つけた Lift を比べてみる。

月と為替に本当は何の関係もなくても、12 個の中から一番いいものを選べば、それなりの Lift が出てしまう。
これが discoid-meniscus で言う「偶然の発見に騙される」の正体で、Lift Lab が N と信頼区間を必ず出す理由でもある。
