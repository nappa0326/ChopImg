#!/usr/bin/env python
"""
テスト用の画像を生成するスクリプト
"""

from PIL import Image, ImageDraw
import os

def create_test_image(filename="test_image.png", size=(1000, 800), color="white"):
    """
    テスト用の画像を生成します。
    
    Args:
        filename: 出力ファイル名
        size: 画像サイズ (幅, 高さ)
        color: 背景色
    """
    # 画像を作成
    img = Image.new('RGB', size, color)
    draw = ImageDraw.Draw(img)
    
    # グリッドを描画
    grid_size = 100
    for x in range(0, size[0], grid_size):
        draw.line([(x, 0), (x, size[1])], fill="lightgray", width=1)
    for y in range(0, size[1], grid_size):
        draw.line([(0, y), (size[0], y)], fill="lightgray", width=1)
    
    # 中央に十字を描画
    center_x, center_y = size[0] // 2, size[1] // 2
    draw.line([(center_x, 0), (center_x, size[1])], fill="red", width=2)
    draw.line([(0, center_y), (size[0], center_y)], fill="red", width=2)
    
    # 四隅に円を描画
    radius = 50
    draw.ellipse([(0, 0), (radius*2, radius*2)], outline="blue", width=2)
    draw.ellipse([(size[0]-radius*2, 0), (size[0], radius*2)], outline="blue", width=2)
    draw.ellipse([(0, size[1]-radius*2), (radius*2, size[1])], outline="blue", width=2)
    draw.ellipse([(size[0]-radius*2, size[1]-radius*2), (size[0], size[1])], outline="blue", width=2)
    
    # 画像を保存
    img.save(filename)
    print(f"テスト画像を作成しました: {os.path.abspath(filename)}")
    print(f"サイズ: {size[0]}x{size[1]}ピクセル")

if __name__ == "__main__":
    create_test_image()