#!/usr/bin/env bash
set -euo pipefail

GREEN="\033[0;32m"
CYAN="\033[0;36m"
RED="\033[0;31m"
YELLOW="\033[0;33m"
RESET="\033[0m"

info()    { echo -e "${CYAN}[*] $1${RESET}"; }
success() { echo -e "${GREEN}[+] $1${RESET}"; }
warn()    { echo -e "${YELLOW}[!] $1${RESET}"; }
error()   { echo -e "${RED}[!] $1${RESET}"; }

spinner() {
    local pid=$1
    local delay=0.1
    local spinstr='|/-\'
    while ps -p $pid &>/dev/null; do
        for i in $(seq 0 3); do
            printf "\r[%c] $2" "${spinstr:i:1}"
            sleep $delay
        done
    done
    printf "\r"
}

HARD_RESET=false
for arg in "$@"; do
    if [[ "$arg" == "--hard-reset" ]]; then
        HARD_RESET=true
        break
    fi
done

if [[ -n "${KITTY_WINDOW_ID-}" && -f "images/halo.png" ]]; then
    kitty +kitten icat images/halo.png
    echo ""

else
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
fi

if command -v python3 &>/dev/null; then
    PYTHON_CMD=python3

elif command -v python &>/dev/null; then
    PYTHON_CMD=python

else
    error ">>> Python3 not found!"
    exit 1
fi
info ">>> Using Python: $($PYTHON_CMD --version 2>&1)"

if ! command -v pipx &>/dev/null; then
    info ">>> pipx not found, installing..."
    $PYTHON_CMD -m pip install --user pipx
    $PYTHON_CMD -m pipx ensurepath
fi

info ">>> Upgrading pipx..."
pipx upgrade pipx >/dev/null 2>&1 & spinner $! ">>> Upgrading pipx..."

if [[ -d .git ]] && [[ -n $(git status --porcelain) ]]; then
    warn ">>> You have uncommitted changes in the repo! Upgrading may overwrite them."
fi

if $HARD_RESET; then
    if pipx list | grep -q 'ibuki'; then
        read -p ">>> This will uninstall and reinstall Ibuki. Continue? [y/N]: " yn
        [[ "$yn" =~ ^[Yy]$ ]] || exit 0
        info ">>> Removing existing Ibuki..."
        pipx uninstall ibuki >/dev/null 2>&1 & spinner $! ">>> Removing Ibuki..."
    fi
    info ">>> Installing Ibuki fresh..."
    pipx install . --force >/dev/null 2>&1 & spinner $! ">>> Installing Ibuki..."
    success ">>> Ibuki installed!"

else
    if pipx list | grep -q 'ibuki'; then
        info ">>> Ibuki detected, upgrading..."
        pipx upgrade ibuki >/dev/null 2>&1 & spinner $! ">>> Upgrading Ibuki..."
        success ">>> Ibuki upgraded!"

    else
        info ">>> Installing Ibuki..."
        pipx install . --force >/dev/null 2>&1 & spinner $! ">>> Installing Ibuki..."
        success ">>> Ibuki installed!"
    fi
fi