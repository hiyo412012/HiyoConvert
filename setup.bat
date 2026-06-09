@echo off
chcp 65001 >nul
title HiyoConvert - Setup

echo.
echo  ===============================================
echo     HIYOCONVERT - Auto Setup
echo     Batch Audio Converter (multithreaded)
echo  ===============================================
echo.

:: Check Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [..] Python not found - installing via winget...
    winget install -e --id Python.Python.3.14 --silent --accept-package-agreements
    if %errorlevel% neq 0 (
        echo [!] winget failed. Install Python from: https://python.org/downloads
        pause
        exit /b 1
    )
)
python --version

:: Check / Install ffmpeg
where ffmpeg >nul 2>&1
if %errorlevel% neq 0 (
    echo [..] ffmpeg not found - installing via winget...
    echo     (run this script as Admin for best results)
    winget install -e --id Gyan.FFmpeg --silent --accept-package-agreements
    if %errorlevel% neq 0 (
        echo [!] winget failed. Install ffmpeg:
        echo     1. https://ffmpeg.org/download.html
        echo     2. Extract to C:\ffmpeg
        echo     3. Add C:\ffmpeg\bin to your PATH
        pause
        exit /b 1
    )
    :: Known winget bug: ffmpeg PATH may be wrong when not run as Admin.
    :: Workaround: search for ffmpeg.exe and add to current session PATH.
    where ffmpeg >nul 2>&1
    if %errorlevel% neq 0 (
        echo [!] ffmpeg installed but not on PATH (known winget bug).
        echo [..] Searching for ffmpeg.exe in winget packages...
        for /d %%i in ("%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg_*") do (
            if exist "%%i\ffmpeg.exe" set "FFDIR=%%i"
            if exist "%%i\bin\ffmpeg.exe" set "FFDIR=%%i\bin"
        )
        if defined FFDIR (
            set "PATH=%FFDIR%;%PATH%"
            echo [OK] Found: %FFDIR%
            echo [!!] Run this script as Admin next time to fix PATH permanently.
        ) else (
            echo [!] ffmpeg.exe not found. Re-run this script as Administrator.
            pause
            exit /b 1
        )
    )
) else (
    echo [OK] ffmpeg found
)

:: Install Python packages
echo [..] Installing Python packages...
python -m pip install -r requirements.txt
echo [OK] Packages installed

echo.
echo  ===============================================
echo     Setup complete!
echo.
echo     Usage:
echo       python hiyo-convert.py
echo       python hiyo-convert.py "D:\Music"
echo       python hiyo-convert.py "D:\Downloads\Music"
echo       python hiyo-convert.py "C:\Users\%USERNAME%\Music"
echo  ===============================================
echo.
pause
