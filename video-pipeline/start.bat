@echo off
REM ASCII-only launcher to avoid CMD encoding issues.
REM All heavy lifting is in bootstrap.py + make_video.py.

cd /d "%~dp0"
title Lazio vs Inter - Video Generator

echo ================================================
echo   Lazio vs Inter - Auto Video Generator
echo ================================================
echo.

echo [1/2] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Python is not installed or not in PATH.
    echo.
    echo Please install Python 3.10+ from:
    echo   https://www.python.org/downloads/
    echo.
    echo IMPORTANT: Check "Add Python to PATH" during install!
    echo.
    pause
    exit /b 1
)
echo OK
echo.

echo [2/2] Running bootstrap and video pipeline...
echo.
python "%~dp0bootstrap.py"
if errorlevel 1 (
    echo.
    echo Pipeline failed. See messages above.
    pause
    exit /b 1
)

echo.
echo ================================================
echo   DONE! Video saved to: out\lazio_inter_30s.mp4
echo ================================================
echo.
pause
