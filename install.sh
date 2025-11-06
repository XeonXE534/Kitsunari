#!/usr/bin/env bash
set -e

GREEN="\033[0;32m"
CYAN="\033[0;36m"
RED="\033[0;31m"
RESET="\033[0m"

echo -e "${CYAN}"
cat <<'EOF'
██████╗ ██████╗  ██████╗      ██╗███████╗ ██████╗████████╗    ██╗██████╗ ██╗   ██╗██╗  ██╗██╗
██╔══██╗██╔══██╗██╔═══██╗     ██║██╔════╝██╔════╝╚══██╔══╝    ██║██╔══██╗██║   ██║██║ ██╔╝██║
██████╔╝██████╔╝██║   ██║     ██║█████╗  ██║        ██║       ██║██████╔╝██║   ██║█████╔╝ ██║
██╔═══╝ ██╔══██╗██║   ██║██   ██║██╔══╝  ██║        ██║       ██║██╔══██╗██║   ██║██╔═██╗ ██║
██║     ██║  ██║╚██████╔╝╚█████╔╝███████╗╚██████╗   ██║       ██║██████╔╝╚██████╔╝██║  ██╗██║
╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚════╝ ╚══════╝ ╚═════╝   ╚═╝       ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝
EOF
echo -e "${RESET}"
echo -e "${CYAN}                         Project Ibuki Installer${RESET}"
echo ""

if [[ -n "$KITTY_WINDOW_ID" && -f "images/Ibuki.png" ]]; then
    echo -e "${GREEN}[*] Detected Kitty terminal, displaying logo...${RESET}"
    kitty +kitten icat images/ibuki.png
    echo ""
fi

PYTHON_CMD=""
if command -v python3 &>/dev/null; then
    PYTHON_CMD=python3

elif command -v python &>/dev/null; then
    PYTHON_CMD=python

else
    echo -e "${RED}[!] Python3 not found.${RESET}"
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "Install Python3 via your package manager:"
        echo "  Debian: sudo apt install python3 python3-venv python3-pip"
        echo "  Arch:   sudo pacman -Syu python python-pip"
        echo "  Fedora: sudo dnf install python3 python3-venv python3-pip"
        exit 1
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "Install Python3 via Homebrew:"
        echo "  brew install python"
        exit 1
    else
        echo "Unsupported OS. Install Python3 manually."
        exit 1
    fi
fi

echo -e "${GREEN}[*] Using $PYTHON_CMD${RESET}"

if ! command -v pipx &>/dev/null; then
    echo -e "${CYAN}[*] pipx not found, installing...${RESET}"
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

echo -e "${CYAN}[*] Installing Ibuki via pipx...${RESET}"
pipx install . --force

echo -e "${GREEN}Done! You can now run 'ibuki' from anywhere.${RESET}"
