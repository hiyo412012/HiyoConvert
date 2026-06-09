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
    winget install Python.Python.3.14
    if %errorlevel% neq 0 (
        echo [!] winget failed. Install manually:
        echo      https://python.org/downloads
        pause
        exit /b 1
    )
)
echo [OK] Python found:
python --version

:: Check / Install ffmpeg
where ffmpeg >nul 2>&1
if %errorlevel% neq 0 (
    echo [..] ffmpeg not found - installing via winget...
    winget install ffmpeg
    if %errorlevel% neq 0 (
        echo [!] winget failed. Install manually:
        echo      https://ffmpeg.org/download.html
        pause
        exit /b 1
    )
) else (
    echo [OK] ffmpeg found
)

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
