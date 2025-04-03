"""
ChopImg - セットアップスクリプト
"""

from setuptools import setup, find_packages
import os
import re

# バージョン情報を取得
with open(os.path.join(os.path.dirname(__file__), '__init__.py'), 'r', encoding='utf-8') as f:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("バージョン情報が見つかりません")

# READMEを読み込む
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="chopimg",
    version=version,
    description="大きな画像ファイルを指定サイズに分割するツール",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/chopimg",
    packages=find_packages(),
    py_modules=["__init__", "core", "cli"],
    install_requires=[
        "Pillow>=9.0.0",
    ],
    entry_points={
        'console_scripts': [
            'chopimg=cli:main',
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    keywords="image, split, tile, slice, graphics",
)