"""
ChopImg - core.pyのテスト
"""

import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
import datetime
from PIL import Image

# テスト対象のモジュールをインポート
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core import split_image_by_size, split_image_by_count, get_image_info


class TestCore(unittest.TestCase):
    """core.pyの関数をテストするクラス"""

    def setUp(self):
        """テストの前処理"""
        # テスト用の日時を固定
        self.test_timestamp = "20250403_085000"
        # datetimeモジュールのnow関数をモック
        self.datetime_patch = patch('core.datetime.datetime')
        self.mock_datetime = self.datetime_patch.start()
        self.mock_datetime.now.return_value.strftime.return_value = self.test_timestamp

    def tearDown(self):
        """テストの後処理"""
        # パッチを停止
        self.datetime_patch.stop()

    @patch('core.os.makedirs')
    @patch('core.Image.open')
    def test_split_image_by_size(self, mock_image_open, mock_makedirs):
        """split_image_by_size関数のテスト"""
        # モック画像の設定
        mock_img = MagicMock()
        mock_img.size = (1000, 800)
        mock_image_open.return_value.__enter__.return_value = mock_img

        # モックタイルの設定
        mock_tile = MagicMock()
        mock_img.crop.return_value = mock_tile

        # 関数を実行
        result = split_image_by_size(
            image_path="test.png",
            tile_size=(500, 400),
            output_dir="output",
            prefix="test",
            format="png",
            quality=90,
            overlap=0
        )

        # 出力ディレクトリが作成されたことを確認
        mock_makedirs.assert_called_once_with("output", exist_ok=True)

        # 画像が開かれたことを確認
        mock_image_open.assert_called_once_with("test.png")

        # 画像が正しく分割されたことを確認
        self.assertEqual(len(result), 4)  # 2x2=4タイル
        self.assertEqual(mock_img.crop.call_count, 4)

        # タイルが保存されたことを確認
        self.assertEqual(mock_tile.save.call_count, 4)

        # 出力ファイル名が正しいことを確認
        expected_filenames = [
            os.path.join("output", f"test_{self.test_timestamp}_000_000.png"),
            os.path.join("output", f"test_{self.test_timestamp}_000_001.png"),
            os.path.join("output", f"test_{self.test_timestamp}_001_000.png"),
            os.path.join("output", f"test_{self.test_timestamp}_001_001.png")
        ]
        for filename in expected_filenames:
            self.assertIn(filename, result)

    @patch('core.split_image_by_size')
    @patch('core.Image.open')
    def test_split_image_by_count(self, mock_image_open, mock_split_by_size):
        """split_image_by_count関数のテスト"""
        # モック画像の設定
        mock_img = MagicMock()
        mock_img.size = (1000, 800)
        mock_image_open.return_value.__enter__.return_value = mock_img

        # split_image_by_sizeの戻り値を設定
        expected_result = ["file1.png", "file2.png", "file3.png", "file4.png"]
        mock_split_by_size.return_value = expected_result

        # 関数を実行
        result = split_image_by_count(
            image_path="test.png",
            grid_size=(2, 2),
            output_dir="output",
            prefix="test",
            format="png",
            quality=90,
            overlap=0
        )

        # 画像が開かれたことを確認
        mock_image_open.assert_called_once_with("test.png")

        # split_image_by_sizeが正しく呼び出されたことを確認
        mock_split_by_size.assert_called_once()
        args, kwargs = mock_split_by_size.call_args
        self.assertEqual(kwargs["image_path"], "test.png")
        self.assertEqual(kwargs["tile_size"], (500, 400))  # 1000/2, 800/2
        self.assertEqual(kwargs["output_dir"], "output")
        self.assertEqual(kwargs["prefix"], "test")
        self.assertEqual(kwargs["format"], "png")
        self.assertEqual(kwargs["quality"], 90)
        self.assertEqual(kwargs["overlap"], 0)

        # 結果が正しいことを確認
        self.assertEqual(result, expected_result)

    @patch('core.Image.open')
    def test_get_image_info(self, mock_image_open):
        """get_image_info関数のテスト"""
        # モック画像の設定
        mock_img = MagicMock()
        mock_img.format = "PNG"
        mock_img.size = (1000, 800)
        mock_img.mode = "RGB"
        mock_img.info = {"dpi": (72, 72)}
        mock_image_open.return_value.__enter__.return_value = mock_img

        # 関数を実行
        result = get_image_info("test.png")

        # 画像が開かれたことを確認
        mock_image_open.assert_called_once_with("test.png")

        # 結果が正しいことを確認
        self.assertEqual(result["path"], "test.png")
        self.assertEqual(result["format"], "PNG")
        self.assertEqual(result["size"], (1000, 800))
        self.assertEqual(result["mode"], "RGB")
        self.assertEqual(result["info"], {"dpi": (72, 72)})


if __name__ == '__main__':
    unittest.main()