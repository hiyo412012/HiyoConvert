#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Detect Python
PYTHON=""
for cmd in python3 python; do
    if command -v "$cmd" &>/dev/null; then
        PYTHON="$cmd"
        break
    fi
done

if [ -z "$PYTHON" ]; then
    echo " [!] Python not found! Run setup.sh first."
    exit 1
fi

# Check ffmpeg
if ! command -v ffmpeg &>/dev/null; then
    echo " [!] ffmpeg not found! Run setup.sh first."
    exit 1
fi

# Run with optional drag-and-drop directory
"$PYTHON" hiyo-convert.py "$@"

echo ""
echo " Press Enter to close..."
read -r
