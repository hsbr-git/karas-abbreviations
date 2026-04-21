# karas-abbreviations

KaraS配列用の動詞・形容詞活用辞書生成ツールです。

## 概要

KaraS配列において、動詞および形容詞の活用を自動生成するツールです。
日本語の動詞（五段、一段、サ変、カ変）および形容詞（い形容詞、および「ない」系統の助動詞）の活用を網羅した `verb.json` を生成します。

## 説明

- 活用ルール（どの形にどの接尾辞を足すか）を `rules/common.yaml` で定義します。
- 動詞、形容詞、定型句（フレーズ）を `rules/custom_rules.yaml` で管理できます。
- `allowed_kinds` を指定することで、必要な活用形のみを生成できます。

## ディレクトリ構成

- `verb.py`: 辞書を生成するメインスクリプト。
- `rules/`
    - `common.yaml`: 基本的な親指アクションと、活用Instruction（基底形と接尾辞の対応）を定義。
    - `custom_rules.yaml`: 個別の語幹登録、フレーズ登録、および活用テーブルを定義。
- `src/conjugators/`
    - `verb.py`, `adjective.py`: それぞれの品詞・形式に応じた活用生成ロジック。
- `verb.json`: 生成済みの辞書ファイル。

## 使い方

### 準備

Python 3.10以降がインストールされている必要があります。
YAMLファイルを読み込むために `PyYAML` が必要です。

```bash
pip install pyyaml
```

### 実行

1. `rules/custom_rules.yaml` に独自の単語やフレーズを追加します。
2. スクリプトを実行します。

```bash
python3 verb.py
```

実行後、`verb.json` が更新されます。これを Plover 等の辞書として読み込んでください。

## カスタマイズ

詳細は `rules/custom_rules.yaml` のコメントを参照してください。
`allowed_kinds` を使うことで、「かもしれない」「～にちがいない」などの特定の活用形のみが必要な助動詞を効率的に登録できます。

## Credits

基本音節制作者:
Kaede Sato
- [GitHub](https://github.com/kaedesato)
- [KaraS Repository](https://github.com/kaedesato/KaraS)
- [Draft/Manual](https://kaedesato.notion.site/karas)

## 免責事項

このツールは現在テストバージョンです。動作の保証はいたしかねます。
