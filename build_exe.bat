@echo off
echo ChopImg - .exe作成スクリプト
echo.
echo PyInstallerを使用して、ChopImgをWindows用の実行可能ファイルにビルドします。
echo.

pyinstaller --onefile ^
            --name chopimg ^
            --hidden-import core ^
            --hidden-import PIL ^
            --hidden-import PIL.Image ^
            --add-data "core.py;." ^
            --exclude-module numpy ^
            --exclude-module pandas ^
            --exclude-module matplotlib ^
            --exclude-module scipy ^
            cli.py

echo.
echo ビルドが完了しました。実行ファイルは dist\chopimg.exe にあります。