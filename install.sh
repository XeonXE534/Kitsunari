#!/usr/bin/env bash
set -e

PYTHON_CMD=""
if command -v python3 &>/dev/null; then
    PYTHON_CMD=python3

elif command -v python &>/dev/null; then
    PYTHON_CMD=python

else
    echo "Python3 not found."

    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "Please install Python3 via your package manager:"
        echo "  Debian: sudo apt install python3 python3-venv python3-pip"
        echo "  Arch: sudo pacman -Syu python python-pip"
        echo "  Fedora: sudo dnf install python3 python3-venv python3-pip"
        exit 1
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "Please install Python3 via Homebrew: brew install python"
        exit 1
    else
        echo "Unsupported OS. Install Python3 manually."
        exit 1
    fi
fi

echo "[*] Using $PYTHON_CMD"

if ! command -v pipx &>/dev/null; then
    echo "[*] pipx not found, installing..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v pacman &>/dev/null; then
            sudo pacman -S python-pipx

        else
            $PYTHON_CMD -m pip install --user pipx
            $PYTHON_CMD -m pipx ensurepath
        fi

    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install pipx
        pipx ensurepath
    fi
fi

echo "[*] Installing Kitsunari via pipx..."
pipx install . --force

echo "[*] Done! You can now run 'kit' from anywhere."
