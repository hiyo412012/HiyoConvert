#!/usr/bin/env bash
set -e

echo ""
echo " ==============================="
echo "   HIYOCONVERT - Auto Setup"
echo "   Batch Audio Converter"
echo " ==============================="
echo ""

# Detect package manager
PKG=""
if command -v apt &>/dev/null; then
    PKG="apt"
elif command -v dnf &>/dev/null; then
    PKG="dnf"
elif command -v yum &>/dev/null; then
    PKG="yum"
elif command -v zypper &>/dev/null; then
    PKG="zypper"
fi

# Check Python
if ! command -v python3 &>/dev/null; then
    echo " [..] Python not found - installing..."
    if [[ "$OSTYPE" == "linux-gnu"* ]] && [[ -n "$PKG" ]]; then
        if [[ "$PKG" == "apt" ]]; then
            sudo apt update && sudo apt install -y python3 python3-pip python3-venv
        elif [[ "$PKG" == "dnf" ]]; then
            sudo dnf install -y python3 python3-pip python3-venv
        elif [[ "$PKG" == "yum" ]]; then
            sudo yum install -y python3 python3-pip
        elif [[ "$PKG" == "zypper" ]]; then
            sudo zypper install -y python3 python3-pip
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        if command -v brew &>/dev/null; then
            brew install python@3.14
        else
            echo " [!] Install Homebrew first: https://brew.sh"
            exit 1
        fi
    fi
fi
echo " [OK] Python: $(python3 --version)"

# Check ffmpeg
if ! command -v ffmpeg &>/dev/null; then
    echo " [..] ffmpeg not found - installing..."
    if [[ "$OSTYPE" == "linux-gnu"* ]] && [[ -n "$PKG" ]]; then
        if [[ "$PKG" == "apt" ]]; then
            sudo apt install -y ffmpeg
        elif [[ "$PKG" == "dnf" ]]; then
            sudo dnf install -y ffmpeg
        elif [[ "$PKG" == "yum" ]]; then
            sudo yum install -y ffmpeg
        elif [[ "$PKG" == "zypper" ]]; then
            sudo zypper install -y ffmpeg
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install ffmpeg
    fi
fi
echo " [OK] ffmpeg: $(ffmpeg -version 2>&1 | head -1)"

# Install Python packages
echo " [..] Installing Python packages..."
python3 -m pip install -r requirements.txt
echo " [OK] Packages installed"

echo ""
echo " ==============================="
echo "   Setup complete!"
echo ""
echo "   Usage:"
echo "     python3 hiyo-convert.py"
echo "     python3 hiyo-convert.py /home/user/Music"
echo " ==============================="
echo ""
