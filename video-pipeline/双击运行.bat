@echo off
chcp 65001 >nul
title 拉齐奥 vs 国米 视频生成
cd /d "%~dp0"

echo ═══════════════════════════════════════════════
echo   🦅 拉齐奥 vs 国米 抖音视频一键生成
echo ═══════════════════════════════════════════════
echo.

REM ============ 检查 Python ============
echo [1/4] 检查 Python ...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ 没有装 Python
    echo.
    echo 解决办法（任选一个）：
    echo   A. 打开 Microsoft Store 搜 "Python 3.12" 装一下
    echo   B. 去 https://www.python.org/downloads/ 下载安装
    echo      安装时一定要勾选 "Add Python to PATH"
    echo.
    pause
    start ms-windows-store://pdp/?productid=9NCVDN91XZQP
    exit /b 1
)
echo     OK
echo.

REM ============ 检查 / 下载 FFmpeg（便携版） ============
echo [2/4] 检查 ffmpeg ...
where ffmpeg >nul 2>&1
if errorlevel 1 (
    if exist "%~dp0tools\ffmpeg\bin\ffmpeg.exe" (
        set "PATH=%~dp0tools\ffmpeg\bin;%PATH%"
        echo     OK 便携版已就绪
    ) else (
        echo     未检测到 ffmpeg，开始下载便携版（约 100MB）...
        mkdir tools 2>nul
        curl -L -o tools\ffmpeg.zip ^
            "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
        if errorlevel 1 (
            echo ❌ 下载失败，请检查网络或手动下载 ffmpeg
            pause
            exit /b 1
        )
        echo     解压中...
        powershell -Command "Expand-Archive -Force tools\ffmpeg.zip tools\"
        for /d %%D in (tools\ffmpeg-master-*) do (
            move "%%D" "tools\ffmpeg" >nul
        )
        del tools\ffmpeg.zip
        set "PATH=%~dp0tools\ffmpeg\bin;%PATH%"
        echo     OK
    )
) else (
    echo     OK
)
echo.

REM ============ 安装 yt-dlp ============
echo [3/4] 安装 / 更新 yt-dlp ...
python -m pip install --quiet --upgrade pip
python -m pip install --quiet --upgrade yt-dlp
if errorlevel 1 (
    echo ❌ yt-dlp 安装失败
    pause
    exit /b 1
)
echo     OK
echo.

REM ============ 跑主程序 ============
echo [4/4] 开始生成视频 ...
echo.
python make_video.py
if errorlevel 1 (
    echo.
    echo ❌ 生成出错，请把上面的红字内容截图发给我
    pause
    exit /b 1
)

echo.
echo ═══════════════════════════════════════════════
echo   🎉 全部完成！视频在 out\ 文件夹里
echo ═══════════════════════════════════════════════
echo.
pause
