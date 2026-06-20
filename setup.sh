#!/usr/bin/env bash
#
# setup.sh — Cross-platform environment setup for market-research (macOS/Linux)
#
# Usage:
#   chmod +x setup.sh
#   ./setup.sh
#
# Features:
#   - Detects OS (macOS/Linux)
#   - Checks Python 3, Node.js/npm, Pi/OpenCode CLI
#   - Installs Python dependencies (user environment, no sudo)
#   - Installs npm extensions
#   - Verifies installation
#   - Idempotent: safe to run multiple times

set -euo pipefail

# ---------------------------------------------------------------------------
# Colors
# ---------------------------------------------------------------------------
readonly RESET='\033[0m'
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly CYAN='\033[0;36m'
readonly BOLD='\033[1m'

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
info()    { printf "${BLUE}ℹ %s${RESET}\n" "$*"; }
success() { printf "${GREEN}✔ %s${RESET}\n" "$*"; }
warn()    { printf "${YELLOW}⚠ %s${RESET}\n" "$*"; }
error()   { printf "${RED}✖ %s${RESET}\n" "$*"; }
header()  { printf "\n${BOLD}${CYAN}%s${RESET}\n" "$*"; }

# ---------------------------------------------------------------------------
# 1. Welcome & OS detection
# ---------------------------------------------------------------------------
header "========================================"
header "  Market Research — Environment Setup"
header "========================================"

OS=""
case "$(uname -s)" in
    Darwin*)     OS="macOS";;
    Linux*)      OS="Linux";;
    CYGWIN*|MINGW*|MSYS*)
        error "Windows detected. Please use Git Bash or WSL, or run setup.bat instead."
        exit 1
        ;;
    *)
        warn "Unknown OS: $(uname -s). Proceeding anyway..."
        OS="Unknown"
        ;;
esac

info "Detected OS: ${OS}"

# ---------------------------------------------------------------------------
# 2. Check Python 3
# ---------------------------------------------------------------------------
header "Checking Python 3..."

if command -v python3 &>/dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    success "Found ${PYTHON_VERSION}"
else
    error "Python 3 is not installed."
    echo ""
    echo "Please install Python 3.8 or later:"
    echo "  macOS:   brew install python3"
    echo "  Linux:   sudo apt-get install python3 python3-pip  (Debian/Ubuntu)"
    echo "           sudo dnf install python3 python3-pip      (Fedora)"
    echo "  Or visit: https://www.python.org/downloads/"
    echo ""
    exit 1
fi

# ---------------------------------------------------------------------------
# 3. Check Node.js / npm
# ---------------------------------------------------------------------------
header "Checking Node.js / npm..."

if command -v npm &>/dev/null; then
    NPM_VERSION=$(npm --version 2>&1)
    success "Found npm ${NPM_VERSION}"
else
    error "npm (Node.js) is not installed."
    echo ""
    echo "Please install Node.js (LTS recommended):"
    echo "  macOS:   brew install node"
    echo "  Linux:   sudo apt-get install npm  (Debian/Ubuntu)"
    echo "           sudo dnf install npm       (Fedora)"
    echo "  Or visit: https://nodejs.org/"
    echo ""
    exit 1
fi

# ---------------------------------------------------------------------------
# 4. Check Pi / OpenCode CLI
# ---------------------------------------------------------------------------
header "Checking Pi / OpenCode CLI..."

PI_FOUND=false
if command -v pi &>/dev/null; then
    PI_VERSION=$(pi --version 2>&1 || true)
    success "Found Pi CLI: ${PI_VERSION}"
    PI_FOUND=true
else
    warn "Pi / OpenCode CLI not found."
    echo ""
    echo "The setup script will continue installing dependencies,"
    echo "but you will need Pi CLI to run research chains."
    echo ""
    echo "Install Pi / OpenCode:"
    echo "  Visit: https://github.com/ohmyopencodes/pi-cli  (placeholder URL)"
    echo "  Or follow the official installation guide for your platform."
    echo ""
fi

# ---------------------------------------------------------------------------
# 5. Install Python dependencies
# ---------------------------------------------------------------------------
header "Installing Python dependencies..."

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${REPO_ROOT}"

if [[ ! -f "requirements.txt" ]]; then
    error "requirements.txt not found in ${REPO_ROOT}"
    exit 1
fi

info "Running: pip install -r requirements.txt"

# Use --user if not in a virtual environment to avoid needing sudo
if [[ -z "${VIRTUAL_ENV:-}" ]] && [[ -z "${CONDA_DEFAULT_ENV:-}" ]]; then
    pip3 install --user -r requirements.txt
else
    pip3 install -r requirements.txt
fi

success "Python dependencies installed."

# ---------------------------------------------------------------------------
# 6. Install npm extensions
# ---------------------------------------------------------------------------
header "Installing npm extensions..."

if [[ ! -d ".pi/npm" ]]; then
    error ".pi/npm directory not found in ${REPO_ROOT}"
    exit 1
fi

cd ".pi/npm"

if [[ ! -f "package.json" ]]; then
    error "package.json not found in .pi/npm/"
    exit 1
fi

info "Running: npm install"
npm install

success "npm extensions installed."

cd "${REPO_ROOT}"

# ---------------------------------------------------------------------------
# 7. Verify installation
# ---------------------------------------------------------------------------
header "Verifying installation..."

VERIFY_OUTPUT=$(python3 -c "import jsonschema, openpyxl; print('OK')" 2>&1) || {
    error "Python dependency verification failed:"
    error "${VERIFY_OUTPUT}"
    exit 1
}

if [[ "${VERIFY_OUTPUT}" == "OK" ]]; then
    success "Python dependencies verified (jsonschema, openpyxl)."
else
    error "Unexpected verification output: ${VERIFY_OUTPUT}"
    exit 1
fi

if [[ -d ".pi/npm/node_modules" ]]; then
    success "npm dependencies verified (node_modules present)."
else
    warn "npm node_modules directory not found — npm install may have failed."
fi

# ---------------------------------------------------------------------------
# 8. Success message & next steps
# ---------------------------------------------------------------------------
header "========================================"
header "  Setup Complete!"
header "========================================"

echo ""
success "All dependencies are installed and verified."
echo ""

if [[ "${PI_FOUND}" == "false" ]]; then
    warn "Reminder: Pi / OpenCode CLI was not detected."
    echo "  Install it before running research chains."
    echo ""
fi

echo "${BOLD}Next steps:${RESET}"
echo ""
echo "  1. Create a research project:"
echo "     mkdir -p projects/my-project"
echo "     cp projects/coq10-2026/brief.md projects/my-project/"
echo "     cp projects/coq10-2026/config.json projects/my-project/"
echo ""
echo "  2. Edit brief.md and config.json for your research topic."
echo ""
echo "  3. Launch Pi and run a chain:"
echo "     pi"
echo "     /run-chain full-market-review -- projects/my-project/brief.md"
echo ""
echo "  4. Or run the quick competitor review:"
echo "     /run-chain quick-competitor-review -- projects/my-project/brief.md"
echo ""
echo "${BOLD}Documentation:${RESET}"
echo "  - AGENTS.md    : Orchestrator rules and workflow"
echo "  - SYSTEM.md    : Full operational specification"
echo "  - README.md    : Project overview and quick start"
echo ""
echo "${BOLD}Need help?${RESET}"
echo "  Open an issue or see CONTRIBUTING.md for development setup."
echo ""

exit 0
