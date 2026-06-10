@echo off
chcp 65001 >nul
title HiyoConvert - Setup
setlocal enabledelayedexpansion

echo.
echo  ===============================================
echo     HIYOCONVERT - Auto Setup
echo     Batch Audio Converter (multithreaded)
echo  ===============================================
echo.

:: ------------------------------------------------------------
:: Admin check — re-launch as admin if not already
:: ------------------------------------------------------------
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [..] Not running as Administrator.
    echo     Restarting with admin rights...
    powershell -Command "Start-Process cmd -ArgumentList '/c cd /d \"%cd%\" ^&^& \"%~f0\"' -Verb RunAs"
    exit /b 0
)
echo [OK] Administrator privileges confirmed
echo.

:: ------------------------------------------------------------
:: Check / Install Python
:: ------------------------------------------------------------
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [..] Python not found - installing via winget...
    winget install -e --id Python.Python.3.14 --silent --accept-package-agreements
    if !errorlevel! neq 0 (
        echo [!] winget failed. Install Python from: https://python.org/downloads
        pause
        exit /b 1
    )
    :: Refresh PATH
    call set "PATH=%PATH%;%LOCALAPPDATA%\Microsoft\WinGet\Packages\Python.Python.3.14_*"
    for /f "tokens=*" %%i in ('where python 2^>nul') do set "PYTHON_PATH=%%i"
    if not defined PYTHON_PATH (
        echo [!] Python installed but not found on PATH.
        echo     Please restart this script or log out and back in.
        pause
        exit /b 1
    )
)
echo [OK] Python: 
python --version

:: ------------------------------------------------------------
:: Check / Install ffmpeg
:: ------------------------------------------------------------
where ffmpeg >nul 2>&1
if %errorlevel% neq 0 (
    echo [..] ffmpeg not found - installing via winget...
    winget install -e --id Gyan.FFmpeg --silent --accept-package-agreements
    if !errorlevel! neq 0 (
        echo [!] winget failed.
        echo.
        echo     Choose an option:
        echo     [1] Auto-detect ffmpeg on this computer
        echo     [2] Enter ffmpeg path manually
        echo     [3] Download ffmpeg automatically (via curl)
        echo     [4] Exit and install manually
        echo.
        set /p FF_OPT="> "
        if "!FF_OPT!"=="1" goto :autodetect_ffmpeg
        if "!FF_OPT!"=="2" goto :manual_ffmpeg
        if "!FF_OPT!"=="3" goto :download_ffmpeg
        goto :ffmpeg_fail
    )

    :: winget succeeded — check PATH bug
    where ffmpeg >nul 2>&1
    if !errorlevel! neq 0 (
        echo [!] ffmpeg installed but not on PATH (known winget bug).
        echo [..] Searching for ffmpeg.exe in winget packages...
        for /d %%i in ("%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg_*") do (
            if exist "%%i\ffmpeg.exe" set "FFDIR=%%i"
            if exist "%%i\bin\ffmpeg.exe" set "FFDIR=%%i\bin"
        )
        if defined FFDIR (
            set "PATH=!FFDIR!;%PATH%"
            echo [OK] Found: !FFDIR!
        ) else (
            goto :autodetect_ffmpeg
        )
    )
) else (
    echo [OK] ffmpeg found
)
echo ffmpeg: 
ffmpeg -version 2>&1 | findstr "ffmpeg version"
goto :install_pkg

:autodetect_ffmpeg
echo [..] Searching for ffmpeg.exe on all drives...
for /f "tokens=*" %%i in ('dir /s /b C:\ffmpeg.exe C:\ffmpeg\bin\ffmpeg.exe C:\ProgramData\chocolatey\bin\ffmpeg.exe "%ProgramFiles%"\ffmpeg\bin\ffmpeg.exe "%ProgramFiles(x86)%"\ffmpeg\bin\ffmpeg.exe 2^>nul') do (
    set "FFDIR=%%~dpi"
    goto :found_ffmpeg
)
:: Broader search
for /f "tokens=*" %%i in ('where /r "C:\" ffmpeg.exe 2^>nul') do (
    set "FFDIR=%%~dpi"
    goto :found_ffmpeg
)
echo [!] Could not auto-detect ffmpeg.
goto :manual_ffmpeg

:found_ffmpeg
echo [OK] Found ffmpeg at: !FFDIR!
set "PATH=!FFDIR!;%PATH%"
:: Register in PATH permanently
setx PATH "!FFDIR!;%PATH%" >nul 2>&1
echo [OK] ffmpeg added to PATH permanently
goto :install_pkg

:manual_ffmpeg
echo.
echo     Enter the full path to the folder containing ffmpeg.exe
echo     (e.g. C:\ffmpeg\bin)
set /p FFDIR="> "
if not exist "!FFDIR!\ffmpeg.exe" (
    echo [!] ffmpeg.exe not found in !FFDIR!
    goto :ffmpeg_fail
)
set "PATH=!FFDIR!;%PATH%"
setx PATH "!FFDIR!;%PATH%" >nul 2>&1
echo [OK] ffmpeg added to PATH permanently
goto :install_pkg

:download_ffmpeg
echo [..] Downloading ffmpeg (release build)...
set "FFURL=https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
set "FFZIP=%TEMP%\ffmpeg.zip"
set "FFDIR=C:\ffmpeg"
curl -L -o "%FFZIP%" "%FFURL%" 2>&1
if %errorlevel% neq 0 (
    echo [!] Download failed. Check your internet connection.
    goto :ffmpeg_fail
)
echo [..] Extracting...
powershell -Command "Expand-Archive -Path '%FFZIP%' -DestinationPath '%TEMP%\ffmpeg-extract' -Force" >nul 2>&1
:: Find the bin folder inside the extracted archive
for /d %%i in ("%TEMP%\ffmpeg-extract\*") do (
    if exist "%%i\bin\ffmpeg.exe" (
        if not exist "!FFDIR!" mkdir "!FFDIR!"
        copy /y "%%i\bin\ffmpeg.exe" "!FFDIR!\ffmpeg.exe" >nul
        copy /y "%%i\bin\ffprobe.exe" "!FFDIR!\ffprobe.exe" >nul
        copy /y "%%i\bin\ffplay.exe" "!FFDIR!\ffplay.exe" >nul
    )
)
if not exist "!FFDIR!\ffmpeg.exe" (
    echo [!] Extraction failed.
    goto :ffmpeg_fail
)
set "PATH=!FFDIR!;%PATH%"
setx PATH "!FFDIR!;%PATH%" >nul 2>&1
echo [OK] ffmpeg downloaded and installed to C:\ffmpeg
del "%FFZIP%" 2>nul
rmdir /s /q "%TEMP%\ffmpeg-extract" 2>nul
goto :install_pkg

:ffmpeg_fail
echo.
echo [!] ffmpeg could not be installed automatically.
echo.
echo     Manual installation:
echo     1. Download from: https://ffmpeg.org/download.html
echo     2. Extract to C:\ffmpeg
echo     3. Add C:\ffmpeg\bin to your PATH
echo.
pause
exit /b 1

:: ------------------------------------------------------------
:: Install Python packages
:: ------------------------------------------------------------
:install_pkg
echo.
echo [..] Installing Python packages...
python -m pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo [!] pip install failed. Try: python -m pip install --upgrade pip
    pause
    exit /b 1
)
echo [OK] Packages installed

:: ------------------------------------------------------------
:: Done
:: ------------------------------------------------------------
echo.
echo  ===============================================
echo     Setup complete!
echo.
echo     Quick start:
echo       Double-click  convert.bat
echo       Or run:       python hiyo-convert.py
echo       Or with path: python hiyo-convert.py "D:\Music"
echo  ===============================================
echo.
pause
