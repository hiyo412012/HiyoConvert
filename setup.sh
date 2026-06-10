#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo ""
echo " ==============================="
echo "   HIYOCONVERT - Auto Setup"
echo "   Batch Audio Converter"
echo " ==============================="
echo ""

# ------------------------------------------------------------
# Detect OS
# ------------------------------------------------------------
OS="$(uname -s)"
ARCH="$(uname -m)"

case "$OS" in
    Linux*)   IS_LINUX=1 ;;
    Darwin*)  IS_MAC=1   ;;
    *)        echo " [!] Unsupported OS: $OS"; exit 1 ;;
esac

# ------------------------------------------------------------
# Detect package manager
# ------------------------------------------------------------
PKG=""
if command -v apt &>/dev/null; then
    PKG="apt"
elif command -v dnf &>/dev/null; then
    PKG="dnf"
elif command -v yum &>/dev/null; then
    PKG="yum"
elif command -v zypper &>/dev/null; then
    PKG="zypper"
elif command -v pacman &>/dev/null; then
    PKG="pacman"
elif command -v apk &>/dev/null; then
    PKG="apk"
fi

pkg_install() {
    local pkg_name="$1"
    case "$PKG" in
        apt)    sudo apt update -qq && sudo apt install -y "$pkg_name" ;;
        dnf)    sudo dnf install -y "$pkg_name" ;;
        yum)    sudo yum install -y "$pkg_name" ;;
        zypper) sudo zypper install -y "$pkg_name" ;;
        pacman) sudo pacman -S --noconfirm "$pkg_name" ;;
        apk)    sudo apk add "$pkg_name" ;;
        *)      return 1 ;;
    esac
}

# ------------------------------------------------------------
# Check / Install Python 3
# ------------------------------------------------------------
PYTHON=""
for cmd in python3 python; do
    if command -v "$cmd" &>/dev/null; then
        PYTHON="$cmd"
        break
    fi
done

if [ -z "$PYTHON" ]; then
    echo " [..] Python not found — installing..."
    if [ -n "$IS_LINUX" ] && [ -n "$PKG" ]; then
        pkg_install python3 python3-pip python3-venv 2>/dev/null || pkg_install python3
    elif [ -n "$IS_MAC" ]; then
        if command -v brew &>/dev/null; then
            brew install python@3.14
        else
            echo " [!] Install Homebrew first: https://brew.sh"
            echo "     Or run: xcode-select --install"
            exit 1
        fi
    fi
    for cmd in python3 python; do
        if command -v "$cmd" &>/dev/null; then
            PYTHON="$cmd"
            break
        fi
    done
fi

if [ -z "$PYTHON" ]; then
    echo " [!] Python installation failed. Install manually: https://python.org"
    exit 1
fi

echo " [OK] Python: $($PYTHON --version 2>&1)"

# ------------------------------------------------------------
# Check / Install pip
# ------------------------------------------------------------
if ! $PYTHON -m pip --version &>/dev/null; then
    echo " [..] pip not found — installing..."
    if [ -n "$IS_LINUX" ] && [ -n "$PKG" ]; then
        pkg_install python3-pip python3-venv 2>/dev/null || true
    fi
    if ! $PYTHON -m pip --version &>/dev/null; then
        curl -sS https://bootstrap.pypa.io/get-pip.py | $PYTHON
    fi
fi
echo " [OK] pip: $($PYTHON -m pip --version 2>&1 | head -1)"

# ------------------------------------------------------------
# Check / Install ffmpeg
# ------------------------------------------------------------
if ! command -v ffmpeg &>/dev/null; then
    echo " [..] ffmpeg not found — installing..."
    INSTALLED=0

    if [ -n "$IS_LINUX" ] && [ -n "$PKG" ]; then
        case "$PKG" in
            apt)
                # ffmpeg may be in deb-multimedia or standard repos
                sudo apt update -qq && sudo apt install -y ffmpeg 2>/dev/null || {
                    # Try snap as fallback
                    command -v snap &>/dev/null && sudo snap install ffmpeg 2>/dev/null
                }
                ;;
            dnf)
                sudo dnf install -y ffmpeg 2>/dev/null || {
                    # RHEL: enable RPM Fusion first
                    sudo dnf install -y https://download1.rpmfusion.org/free/el/rpmfusion-free-release-$(rpm -E %rhel).noarch.rpm 2>/dev/null
                    sudo dnf install -y ffmpeg
                }
                ;;
            pacman)
                sudo pacman -S --noconfirm ffmpeg
                ;;
            *)  pkg_install ffmpeg ;;
        esac
    elif [ -n "$IS_MAC" ]; then
        if command -v brew &>/dev/null; then
            brew install ffmpeg
        else
            echo " [!] Install ffmpeg manually: brew install ffmpeg"
            exit 1
        fi
    fi

    if command -v ffmpeg &>/dev/null; then
        INSTALLED=1
    fi

    if [ "$INSTALLED" -eq 0 ]; then
        echo " [!] ffmpeg installation failed."
        echo "     Install manually:"
        echo "       Linux:  sudo apt install ffmpeg"
        echo "       macOS:  brew install ffmpeg"
        exit 1
    fi
fi
echo " [OK] ffmpeg: $(ffmpeg -version 2>&1 | head -1)"

# ------------------------------------------------------------
# Install Python packages
# ------------------------------------------------------------
echo " [..] Installing Python packages..."
$PYTHON -m pip install -r requirements.txt --quiet
if [ $? -ne 0 ]; then
    echo " [!] pip install failed."
    exit 1
fi
echo " [OK] Packages installed"

# ------------------------------------------------------------
# Make scripts executable
# ------------------------------------------------------------
chmod +x hiyo-convert.py convert.sh 2>/dev/null || true

# ------------------------------------------------------------
# Done
# ------------------------------------------------------------
echo ""
echo " ==============================="
echo "   Setup complete!"
echo ""
echo "   Quick start:"
echo "     Double-click  convert.sh"
echo "     Or run:       $PYTHON hiyo-convert.py"
echo "     Or with path: $PYTHON hiyo-convert.py ~/Music"
echo " ==============================="
echo ""
