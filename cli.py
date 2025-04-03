"""
ChopImg - コマンドラインインターフェース

コマンドライン引数の解析と処理を行います。
"""

import argparse
import sys
import os
from typing import List, Optional, Tuple

# バージョン情報を直接定義
__version__ = '0.1.0'

# core モジュールを絶対インポートに変更
import core
from core import split_image_by_size, split_image_by_count, get_image_info


def parse_size(size_str: str) -> Tuple[int, int]:
    """
    'WIDTHxHEIGHT'形式の文字列をタプルに変換します。

    Args:
        size_str: 'WIDTHxHEIGHT'形式のサイズ文字列

    Returns:
        (width, height)のタプル

    Raises:
        ValueError: 形式が正しくない場合
    """
    try:
        width, height = size_str.lower().split('x')
        return (int(width), int(height))
    except ValueError:
        raise ValueError(f"サイズの形式が正しくありません: {size_str}。'WIDTHxHEIGHT'形式で指定してください。")


def validate_format(format_str: str) -> str:
    """
    出力フォーマットが有効かどうかを検証します。

    Args:
        format_str: フォーマット文字列

    Returns:
        検証済みのフォーマット文字列

    Raises:
        ValueError: フォーマットが無効な場合
    """
    valid_formats = ['png', 'jpg', 'jpeg', 'webp']
    format_lower = format_str.lower()
    
    if format_lower not in valid_formats:
        raise ValueError(f"無効なフォーマット: {format_str}。有効なフォーマット: {', '.join(valid_formats)}")
    
    return format_lower


def validate_quality(quality: int) -> int:
    """
    画質の値が有効かどうかを検証します。

    Args:
        quality: 画質の値

    Returns:
        検証済みの画質の値

    Raises:
        ValueError: 画質の値が範囲外の場合
    """
    if not (0 <= quality <= 100):
        raise ValueError(f"画質の値は0から100の間である必要があります: {quality}")
    
    return quality


def main(args: Optional[List[str]] = None) -> int:
    """
    メイン関数。コマンドライン引数を解析し、画像分割を実行します。

    Args:
        args: コマンドライン引数のリスト（Noneの場合はsys.argvを使用）

    Returns:
        終了コード
    """
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        prog="chopimg",
        description="大きな画像ファイルを指定サイズに分割するツール",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "input_file",
        help="入力画像ファイルのパス"
    )

    size_group = parser.add_mutually_exclusive_group()
    size_group.add_argument(
        "-s", "--size",
        help="分割サイズを指定（例: 512x512）",
        type=str,
        metavar="WIDTHxHEIGHT"
    )
    size_group.add_argument(
        "-c", "--count",
        help="分割数を指定（例: 3x3）",
        type=str,
        metavar="ROWSxCOLUMNS"
    )

    parser.add_argument(
        "-p", "--prefix",
        help="出力ファイル名のプレフィックス",
        default="slice",
        type=str
    )
    parser.add_argument(
        "-o", "--output",
        help="出力ディレクトリ",
        default=".",
        type=str
    )
    parser.add_argument(
        "-f", "--format",
        help="出力フォーマット（png, jpg, webp）",
        default="png",
        type=str
    )
    parser.add_argument(
        "-q", "--quality",
        help="画像品質（0-100）",
        default=90,
        type=int
    )
    parser.add_argument(
        "-ol", "--overlap",
        help="オーバーラップサイズ（ピクセル）",
        default=0,
        type=int
    )
    parser.add_argument(
        "-i", "--info",
        help="画像情報のみを表示",
        action="store_true"
    )
    parser.add_argument(
        "-v", "--version",
        help="バージョン情報を表示",
        action="version",
        version=f"ChopImg {__version__}"
    )

    # 引数を解析
    parsed_args = parser.parse_args(args)

    # 入力ファイルが存在するか確認
    if not os.path.isfile(parsed_args.input_file):
        sys.stderr.write(f"エラー: 入力ファイルが見つかりません: {parsed_args.input_file}")
        return 1

    try:
        # 画像情報のみを表示する場合
        if parsed_args.info:
            info = get_image_info(parsed_args.input_file)
            sys.stdout.write(f"ファイル: {info['path']}\n")
            sys.stdout.write(f"フォーマット: {info['format']}\n")
            sys.stdout.write(f"サイズ: {info['size'][0]}x{info['size'][1]}ピクセル\n")
            sys.stdout.write(f"モード: {info['mode']}\n")
            return 0

        # フォーマットを検証
        format_str = validate_format(parsed_args.format)
        
        # 画質を検証
        quality = validate_quality(parsed_args.quality)

        # サイズまたは分割数が指定されていない場合はエラー
        if not parsed_args.size and not parsed_args.count:
            sys.stderr.write("エラー: サイズ（--size）または分割数（--count）のいずれかを指定してください。")
            return 1

        # 分割を実行
        if parsed_args.size:
            tile_size = parse_size(parsed_args.size)
            output_files = split_image_by_size(
                image_path=parsed_args.input_file,
                tile_size=tile_size,
                output_dir=parsed_args.output,
                prefix=parsed_args.prefix,
                format=format_str,
                quality=quality,
                overlap=parsed_args.overlap
            )
        else:  # parsed_args.count
            grid_size = parse_size(parsed_args.count)
            output_files = split_image_by_count(
                image_path=parsed_args.input_file,
                grid_size=grid_size,
                output_dir=parsed_args.output,
                prefix=parsed_args.prefix,
                format=format_str,
                quality=quality,
                overlap=parsed_args.overlap
            )

        # 結果を表示
        sys.stdout.write(f"画像を{len(output_files)}個のタイルに分割しました。\n")
        sys.stdout.write(f"出力ディレクトリ: {os.path.abspath(parsed_args.output)}\n")
        
        return 0

    except ValueError as e:
        sys.stderr.write(f"エラー: {str(e)}")
        return 1
    except Exception as e:
        sys.stderr.write(f"予期しないエラーが発生しました: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())