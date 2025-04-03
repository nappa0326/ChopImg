"""
ChopImg - cli.pyのテスト
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import argparse

# テスト対象のモジュールをインポート
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from cli import parse_size, validate_format, validate_quality, main


class TestCLI(unittest.TestCase):
    """cli.pyの関数をテストするクラス"""

    def test_parse_size_valid(self):
        """parse_size関数の有効な入力のテスト"""
        # 有効なサイズ文字列
        self.assertEqual(parse_size("512x256"), (512, 256))
        self.assertEqual(parse_size("1024x768"), (1024, 768))
        self.assertEqual(parse_size("100x100"), (100, 100))
        # 大文字小文字の違いを無視
        self.assertEqual(parse_size("512X256"), (512, 256))

    def test_parse_size_invalid(self):
        """parse_size関数の無効な入力のテスト"""
        # 無効なサイズ文字列
        with self.assertRaises(ValueError):
            parse_size("invalid")
        with self.assertRaises(ValueError):
            parse_size("512")
        with self.assertRaises(ValueError):
            parse_size("512x")
        with self.assertRaises(ValueError):
            parse_size("x256")
        with self.assertRaises(ValueError):
            parse_size("512-256")
        with self.assertRaises(ValueError):
            parse_size("512x256x128")

    def test_validate_format_valid(self):
        """validate_format関数の有効な入力のテスト"""
        # 有効なフォーマット
        self.assertEqual(validate_format("png"), "png")
        self.assertEqual(validate_format("jpg"), "jpg")
        self.assertEqual(validate_format("jpeg"), "jpeg")
        self.assertEqual(validate_format("webp"), "webp")
        # 大文字小文字の違いを無視
        self.assertEqual(validate_format("PNG"), "png")
        self.assertEqual(validate_format("JPG"), "jpg")
        self.assertEqual(validate_format("JPEG"), "jpeg")
        self.assertEqual(validate_format("WEBP"), "webp")

    def test_validate_format_invalid(self):
        """validate_format関数の無効な入力のテスト"""
        # 無効なフォーマット
        with self.assertRaises(ValueError):
            validate_format("invalid")
        with self.assertRaises(ValueError):
            validate_format("gif")
        with self.assertRaises(ValueError):
            validate_format("tiff")
        with self.assertRaises(ValueError):
            validate_format("")

    def test_validate_quality_valid(self):
        """validate_quality関数の有効な入力のテスト"""
        # 有効な品質値
        self.assertEqual(validate_quality(0), 0)
        self.assertEqual(validate_quality(50), 50)
        self.assertEqual(validate_quality(100), 100)
        self.assertEqual(validate_quality(75), 75)

    def test_validate_quality_invalid(self):
        """validate_quality関数の無効な入力のテスト"""
        # 無効な品質値
        with self.assertRaises(ValueError):
            validate_quality(-1)
        with self.assertRaises(ValueError):
            validate_quality(101)
        with self.assertRaises(ValueError):
            validate_quality(200)

    @patch('cli.os.path.isfile')
    @patch('cli.get_image_info')
    def test_main_info_option(self, mock_get_image_info, mock_isfile):
        """main関数の--infoオプションのテスト"""
        # ファイルが存在することを確認
        mock_isfile.return_value = True

        # get_image_infoの戻り値を設定
        mock_get_image_info.return_value = {
            'path': 'test.png',
            'format': 'PNG',
            'size': (1000, 800),
            'mode': 'RGB',
            'info': {}
        }

        # 標準出力をキャプチャ
        with patch('sys.stdout') as mock_stdout:
            # 関数を実行
            result = main(['test.png', '--info'])

            # 終了コードが0であることを確認
            self.assertEqual(result, 0)

            # get_image_infoが呼び出されたことを確認
            mock_get_image_info.assert_called_once_with('test.png')

            # 標準出力に正しい情報が出力されたことを確認
            mock_stdout.write.assert_any_call("ファイル: test.png\n")
            mock_stdout.write.assert_any_call("フォーマット: PNG\n")
            mock_stdout.write.assert_any_call("サイズ: 1000x800ピクセル\n")
            mock_stdout.write.assert_any_call("モード: RGB\n")

    @patch('cli.os.path.isfile')
    def test_main_file_not_found(self, mock_isfile):
        """main関数のファイルが見つからない場合のテスト"""
        # ファイルが存在しないことを確認
        mock_isfile.return_value = False

        # 標準エラー出力をキャプチャ
        with patch('sys.stderr') as mock_stderr:
            # 関数を実行
            result = main(['test.png', '--size', '512x512'])

            # 終了コードが1であることを確認
            self.assertEqual(result, 1)

            # 標準エラー出力にエラーメッセージが出力されたことを確認
            mock_stderr.write.assert_called_once()

    @patch('cli.os.path.isfile')
    @patch('cli.split_image_by_size')
    def test_main_split_by_size(self, mock_split_by_size, mock_isfile):
        """main関数の--sizeオプションのテスト"""
        # ファイルが存在することを確認
        mock_isfile.return_value = True

        # split_image_by_sizeの戻り値を設定
        mock_split_by_size.return_value = ['file1.png', 'file2.png', 'file3.png', 'file4.png']

        # 標準出力をキャプチャ
        with patch('sys.stdout') as mock_stdout:
            # 関数を実行
            result = main(['test.png', '--size', '512x512', '--format', 'png', '--quality', '90'])

            # 終了コードが0であることを確認
            self.assertEqual(result, 0)

            # split_image_by_sizeが正しく呼び出されたことを確認
            mock_split_by_size.assert_called_once()
            args, kwargs = mock_split_by_size.call_args
            self.assertEqual(kwargs['image_path'], 'test.png')
            self.assertEqual(kwargs['tile_size'], (512, 512))
            self.assertEqual(kwargs['format'], 'png')
            self.assertEqual(kwargs['quality'], 90)

            # 標準出力に正しい情報が出力されたことを確認
            mock_stdout.write.assert_any_call("画像を4個のタイルに分割しました。\n")

    @patch('cli.os.path.isfile')
    @patch('cli.split_image_by_count')
    def test_main_split_by_count(self, mock_split_by_count, mock_isfile):
        """main関数の--countオプションのテスト"""
        # ファイルが存在することを確認
        mock_isfile.return_value = True

        # split_image_by_countの戻り値を設定
        mock_split_by_count.return_value = ['file1.png', 'file2.png', 'file3.png', 'file4.png']

        # 標準出力をキャプチャ
        with patch('sys.stdout') as mock_stdout:
            # 関数を実行
            result = main(['test.png', '--count', '2x2', '--format', 'jpg', '--quality', '80'])

            # 終了コードが0であることを確認
            self.assertEqual(result, 0)

            # split_image_by_countが正しく呼び出されたことを確認
            mock_split_by_count.assert_called_once()
            args, kwargs = mock_split_by_count.call_args
            self.assertEqual(kwargs['image_path'], 'test.png')
            self.assertEqual(kwargs['grid_size'], (2, 2))
            self.assertEqual(kwargs['format'], 'jpg')
            self.assertEqual(kwargs['quality'], 80)

            # 標準出力に正しい情報が出力されたことを確認
            mock_stdout.write.assert_any_call("画像を4個のタイルに分割しました。\n")

    @patch('cli.os.path.isfile')
    def test_main_no_size_or_count(self, mock_isfile):
        """main関数のサイズも分割数も指定されていない場合のテスト"""
        # ファイルが存在することを確認
        mock_isfile.return_value = True

        # 標準エラー出力をキャプチャ
        with patch('sys.stderr') as mock_stderr:
            # 関数を実行
            result = main(['test.png'])

            # 終了コードが1であることを確認
            self.assertEqual(result, 1)

            # 標準エラー出力にエラーメッセージが出力されたことを確認
            mock_stderr.write.assert_called_once()


if __name__ == '__main__':
    unittest.main()