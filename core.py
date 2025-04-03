"""
ChopImg - コア機能モジュール

画像分割の主要機能を提供します。
"""

import os
import datetime
from typing import Tuple, List, Optional
from PIL import Image


def split_image_by_size(
    image_path: str,
    tile_size: Tuple[int, int],
    output_dir: str = ".",
    prefix: str = "slice",
    format: str = "png",
    quality: int = 90,
    overlap: int = 0
) -> List[str]:
    """
    画像を指定されたタイルサイズに分割します。

    Args:
        image_path: 入力画像のパス
        tile_size: 分割サイズ (幅, 高さ)
        output_dir: 出力ディレクトリ
        prefix: 出力ファイル名のプレフィックス
        format: 出力フォーマット (png, jpg, webp)
        quality: 画像品質 (0-100)
        overlap: オーバーラップサイズ (ピクセル)

    Returns:
        生成されたファイルパスのリスト
    """
    # 出力ディレクトリが存在しない場合は作成
    os.makedirs(output_dir, exist_ok=True)

    # 画像を開く
    with Image.open(image_path) as img:
        # 画像のサイズを取得
        img_width, img_height = img.size
        tile_width, tile_height = tile_size

        # 現在の日時を取得
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        # 生成されたファイルのパスを保存するリスト
        output_files = []

        # 行と列の数を計算
        effective_tile_width = tile_width - overlap
        effective_tile_height = tile_height - overlap

        # 最後のタイルが小さすぎる場合に調整するための計算
        cols = (img_width + effective_tile_width - 1) // effective_tile_width
        rows = (img_height + effective_tile_height - 1) // effective_tile_height

        for row in range(rows):
            for col in range(cols):
                # タイルの左上の座標を計算
                left = col * effective_tile_width
                upper = row * effective_tile_height

                # タイルの右下の座標を計算（画像の境界を超えないように）
                right = min(left + tile_width, img_width)
                lower = min(upper + tile_height, img_height)

                # タイルをクロップ
                tile = img.crop((left, upper, right, lower))

                # 出力ファイル名を生成
                output_filename = f"{prefix}_{timestamp}_{row:03d}_{col:03d}.{format.lower()}"
                output_path = os.path.join(output_dir, output_filename)

                # フォーマットに応じた保存オプションを設定
                save_options = {}
                if format.lower() in ['jpg', 'jpeg']:
                    save_options['quality'] = quality
                    save_options['optimize'] = True
                    if format.lower() == 'jpg':
                        format = 'jpeg'
                elif format.lower() == 'webp':
                    save_options['quality'] = quality
                elif format.lower() == 'png':
                    save_options['optimize'] = True

                # タイルを保存
                tile.save(output_path, format=format.upper(), **save_options)
                output_files.append(output_path)

        return output_files


def split_image_by_count(
    image_path: str,
    grid_size: Tuple[int, int],
    output_dir: str = ".",
    prefix: str = "slice",
    format: str = "png",
    quality: int = 90,
    overlap: int = 0
) -> List[str]:
    """
    画像を指定された行数と列数に分割します。

    Args:
        image_path: 入力画像のパス
        grid_size: 分割数 (行数, 列数)
        output_dir: 出力ディレクトリ
        prefix: 出力ファイル名のプレフィックス
        format: 出力フォーマット (png, jpg, webp)
        quality: 画像品質 (0-100)
        overlap: オーバーラップサイズ (ピクセル)

    Returns:
        生成されたファイルパスのリスト
    """
    # 画像を開く
    with Image.open(image_path) as img:
        # 画像のサイズを取得
        img_width, img_height = img.size
        rows, cols = grid_size

        # タイルサイズを計算
        tile_width = img_width // cols
        tile_height = img_height // rows

        # オーバーラップを考慮したタイルサイズを計算
        tile_width_with_overlap = tile_width + overlap
        tile_height_with_overlap = tile_height + overlap

        # 分割サイズを使用して画像を分割
        return split_image_by_size(
            image_path=image_path,
            tile_size=(tile_width_with_overlap, tile_height_with_overlap),
            output_dir=output_dir,
            prefix=prefix,
            format=format,
            quality=quality,
            overlap=overlap
        )


def get_image_info(image_path: str) -> dict:
    """
    画像の情報を取得します。

    Args:
        image_path: 入力画像のパス

    Returns:
        画像情報を含む辞書
    """
    with Image.open(image_path) as img:
        return {
            'path': image_path,
            'format': img.format,
            'size': img.size,
            'mode': img.mode,
            'info': img.info
        }