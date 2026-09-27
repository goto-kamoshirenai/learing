# Lift Lab

チームで「相場の仮説」を立て、実データに反証してもらうアプリ。
Python のサーバーレス API（素の AWS Lambda）を実務レベルで書けるようになることが目的。

> 例: 「気温が異常に高く、かつ Wikipedia で『円安』の閲覧が急増した日の 20 営業日後は、円高になりやすい？」
> → API が実データで Lift・N・信頼区間を計算し、「偶然の可能性大」などと判定する。

## 最終形のアーキテクチャ

| 実務で使う技術 | Lift Lab での使い道 |
|---|---|
| Lambda（フレームワークなし） + API Gateway | API 本体。`lambda_handler(event, context)` を素で書く |
| Aurora MySQL | 組織・ユーザー・仮説カード |
| DynamoDB | 仮説カードへのコメントスレッド（チャット） |
| S3 | 解析用データセット（parquet） |
| Cognito | ログインと、組織内ロール（owner / member / viewer）による認可 |

フロントエンド（Next.js）はコーチ側が大部分を実装する。学習の主役は API。

## ロードマップ

各 Phase の最後に「動いて楽しいもの」が手に入るように区切っている。

| Phase | テーマ | 終わると手に入るもの | 新しく触るもの |
|---|---|---|---|
| **0** | Python 速習（TS 経験者向け） | 実データで「曜日・月ごとの円高率」を自分で集計できる | 型ヒント、dataclass、例外、pytest、uv、pandas |
| 1 | はじめての `lambda_handler` | 為替チャートが Next.js 画面に出る | API Gateway のイベント形式、JSON レスポンス、handler 単体テスト |
| 2 | 解析 API | 画面で仮説を組み立てると Lift と信頼区間が返る。「偶然の相関ガチャ」 | 手書きのルーティングとバリデーション、bootstrap |
| 3 | Docker + MySQL | 仮説カードを保存して一覧・編集できる | Docker Compose、MySQL 8.0（Aurora MySQL 3 互換）、PyMySQL で生 SQL、トランザクション |
| 4 | DynamoDB + S3 | カードにコメントスレッドが付く。データセットを S3 から読む | boto3、DynamoDB のキー設計、DynamoDB Local、moto |
| 5 | 認証・認可 | 組織ごとに見えるカードが分かれる | JWT クレーム、API Gateway の JWT オーソライザ、ロール別認可 |
| 6 | AWS へデプロイ | 学習用アカウントで本物が動く | AWS SAM、IAM、CloudWatch Logs、コスト管理と後片付け |

## ディレクトリ

```
lift-lab/
├── data/usdjpy.parquet   ECB 参照レート由来の USD/JPY（2004-12-31〜2020-12-31）
└── phase0/               Phase 0 の課題
```

データの出典は discoid-meniscus（ECB 参照レート）。後の Phase で Wikipedia の注目度や気温偏差も追加する。
