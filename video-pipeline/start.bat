@echo off
REM ASCII-only launcher to avoid CMD encoding issues.
REM Tries multiple Python launchers so existing-but-not-in-PATH installs still work.

cd /d "%~dp0"
title Lazio vs Inter - Video Generator

echo ================================================
echo   Lazio vs Inter - Auto Video Generator
echo ================================================
echo.

echo [1/2] Looking for Python...
set "PY_CMD="

REM Try `py -3` (Python launcher, installed by python.org installer)
py -3 --version >nul 2>&1
if not errorlevel 1 (
    set "PY_CMD=py -3"
    py -3 --version
    goto :found
)

REM Try `python`
python --version >nul 2>&1
if not errorlevel 1 (
    set "PY_CMD=python"
    python --version
    goto :found
)

REM Try `python3`
python3 --version >nul 2>&1
if not errorlevel 1 (
    set "PY_CMD=python3"
    python3 --version
    goto :found
)

REM Try common install paths
for %%P in (
    "%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
    "C:\Python313\python.exe"
    "C:\Python312\python.exe"
    "C:\Python311\python.exe"
    "C:\Python310\python.exe"
    "%ProgramFiles%\Python313\python.exe"
    "%ProgramFiles%\Python312\python.exe"
    "%ProgramFiles%\Python311\python.exe"
    "%ProgramFiles%\Python310\python.exe"
) do (
    if exist %%P (
        set "PY_CMD=%%P"
        %%P --version
        goto :found
    )
)

echo.
echo ERROR: No Python 3.x found on this machine.
echo.
echo Install from one of these:
echo   1) Microsoft Store - search "Python 3.12"
echo   2) Official:  https://www.python.org/downloads/
echo                 IMPORTANT: check "Add python.exe to PATH"
echo   3) Huawei mirror (faster in CN):
echo      https://mirrors.huaweicloud.com/python/3.12.7/python-3.12.7-amd64.exe
echo.
pause
exit /b 1

:found
echo.
echo [2/2] Running bootstrap and video pipeline...
echo.
%PY_CMD% "%~dp0bootstrap.py"
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
