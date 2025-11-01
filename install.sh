#!/usr/bin/env bash
set -e

PYTHON_CMD=""
if command -v python3 &>/dev/null; then
    PYTHON_CMD=python3

elif command -v python &>/dev/null; then
    PYTHON_CMD=python
else
    echo "Python3 not found."
    echo "Please install Python3 via your package manager."
    exit 1
fi

echo "[*] Using $PYTHON_CMD"

$PYTHON_CMD -m pip install --upgrade pip setuptools wheel --user
$PYTHON_CMD -m pip install --upgrade . --user

BIN_DIR=$($PYTHON_CMD -m site --user-base)/bin
mkdir -p "$BIN_DIR"

ln -sf "$BIN_DIR/kitsunari" "$BIN_DIR/kit"

echo "[*] Done! Make sure $BIN_DIR is in your PATH:"
echo '  export PATH="$HOME/.local/bin:$PATH"'
echo "[*] Now you can run 'kit' from anywhere."
