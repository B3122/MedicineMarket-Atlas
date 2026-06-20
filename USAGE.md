# Usage Guide

## Quick Start

```bash
# 1. Clone and enter the repository
git clone <repo-url> medicinemarket-atlas
cd medicinemarket-atlas

# 2. Run the installer
chmod +x setup.sh
./setup.sh

# 3. Launch Pi
pi

# 4. Run the example project
/run-chain full-market-review -- projects/coq10-2026/brief.md
```

For detailed documentation, see [README.md](README.md) and [README.en.md](README.en.md).

## Creating a New Project

```bash
mkdir -p projects/my-project
cp projects/coq10-2026/brief.md projects/my-project/
cp projects/coq10-2026/config.json projects/my-project/
```

Edit `brief.md` and `config.json` with your research topic, then run a chain.

## Available Chains

- `/run-chain full-market-review -- projects/<name>/brief.md`
- `/run-chain quick-competitor-review -- projects/<name>/brief.md`
- `/run-chain evidence-only -- projects/<name>/brief.md`

## Project Output

Chain outputs are written to `projects/<name>/chain-outputs/`.

## Requirements

- Python 3.8+
- Node.js 18+
- Pi / OpenCode CLI
- Git Bash or WSL (Windows users)

See [README.md](README.md) for the complete guide.
