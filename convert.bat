@echo off
chcp 65001 >nul
title HiyoConvert

:: Check ffmpeg
where ffmpeg >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] ffmpeg not found!
    echo     Run setup.bat first, or install ffmpeg manually.
    pause
    exit /b 1
)

:: Drag-and-drop support: if a folder is dropped onto this .bat, use it as arg
if not "%~1"=="" (
    python "%~dp0hiyo-convert.py" "%~1"
) else (
    python "%~dp0hiyo-convert.py"
)

:: Pause so window stays open
echo.
pause
