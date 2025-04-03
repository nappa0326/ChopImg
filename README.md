# ChopImg - 画像分割ツール

大きな画像ファイルを指定サイズに分割するコマンドラインツールです。

## 機能

- 画像を指定したサイズのタイルに分割
- 画像を指定した行数と列数に分割
- 分割された画像を指定したフォーマット（PNG, JPEG, WebP）で保存
- オーバーラップ（重複領域）の設定
- カスタム出力ディレクトリとファイル名プレフィックスの指定

## インストール

```bash
# pipを使用してインストール
pip install chopimg

# または、ソースからインストール
git clone https://github.com/yourusername/chopimg.git
cd chopimg
pip install -e .
```

## 使用方法

```bash
# 基本的な使用方法
chopimg -s 512x512 large_image.png

# プレフィックスとカスタム出力ディレクトリを指定
chopimg -s 512x512 -p tile -o ./output large_image.png

# JPEGフォーマットで品質80で出力
chopimg -s 512x512 -f jpg -q 80 large_image.png

# 3x3の分割数で分割
chopimg -c 3x3 large_image.png

# 20ピクセルのオーバーラップ領域を持つタイルに分割
chopimg -s 512x512 -ol 20 large_image.png

# 画像情報のみを表示
chopimg -i large_image.png
```

## コマンドラインオプション

```
chopimg [オプション] <入力ファイル>

オプション:
  -s, --size WIDTHxHEIGHT    分割サイズを指定（例: 512x512）
  -c, --count ROWSxCOLUMNS   分割数を指定（例: 3x3）
  -p, --prefix PREFIX        出力ファイル名のプレフィックス（デフォルト: "slice"）
  -o, --output DIR           出力ディレクトリ（デフォルト: カレントディレクトリ）
  -f, --format FORMAT        出力フォーマット（png, jpg, webp）（デフォルト: png）
  -q, --quality VALUE        画像品質（0-100）（デフォルト: 90）
  -ol, --overlap PIXELS      オーバーラップサイズ（デフォルト: 0）
  -i, --info                 画像情報のみを表示
  -h, --help                 ヘルプメッセージを表示
  -v, --version              バージョン情報を表示
```

## 対応フォーマット

- 入力: PNG, JPEG, WebP, GIF, TIFF
- 出力: PNG, JPEG, WebP

## 要件

- Python 3.7 以上
- Pillow 9.0.0 以上

## ライセンス

MIT License
