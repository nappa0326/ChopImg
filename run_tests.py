#!/usr/bin/env python
"""
ChopImg - テスト実行スクリプト

すべてのテストを実行します。
"""

import unittest
import sys


if __name__ == '__main__':
    # テストディスカバリーを使用してすべてのテストを検出して実行
    test_suite = unittest.defaultTestLoader.discover('tests')
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    
    # テスト結果に基づいて終了コードを設定
    sys.exit(not result.wasSuccessful())