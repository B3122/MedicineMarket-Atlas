#!/usr/bin/env bash
#
# sync-to-public.sh
#
# Sync a public-safe subset of the market-research project to a sibling
# directory that can be published or shared openly.
#
# Excludes:
#   - Git metadata
#   - Runtime/local state (.omo, .omx, agent sessions/drafts)
#   - Installed dependencies (node_modules, package-lock.json, Python caches)
#   - Secrets/credentials patterns (.env, *.pem, *token*, etc.)
#   - Per-project research data and outputs (chain-outputs, progress.json,
#     artifacts, data, reports, sources)
#
# Usage:
#   ./sync-to-public.sh              # perform sync
#   ./sync-to-public.sh --dry-run    # preview changes only
#   ./sync-to-public.sh --verify     # scan target for residual sensitive patterns
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="$SCRIPT_DIR"
TARGET_DIR="${TARGET_DIR:-$SOURCE_DIR/../market-research-assistant-public}"

DRY_RUN=""
VERIFY=""

for arg in "$@"; do
  case "$arg" in
    --dry-run|-n)
      DRY_RUN="--dry-run"
      ;;
    --verify)
      VERIFY="1"
      ;;
    --help|-h)
      cat <<'USAGE'
Usage: ./sync-to-public.sh [OPTIONS]

Options:
  --dry-run, -n   Show what would be copied/deleted without making changes.
  --verify        After syncing, scan the target for residual sensitive patterns.
  --help, -h      Show this message.

Environment:
  TARGET_DIR      Override the default target directory.
                  Default: ../market-research-assistant-public
USAGE
      exit 0
      ;;
    *)
      echo "Unknown option: $arg" >&2
      echo "Use --help for usage." >&2
      exit 1
      ;;
  esac
done

if ! command -v rsync >/dev/null 2>&1; then
  echo "Error: rsync is required but not installed." >&2
  exit 1
fi

mkdir -p "$TARGET_DIR"

EXCLUDE_FILE="$(mktemp -t sync-to-public-excludes.XXXXXX)"
trap 'rm -f "$EXCLUDE_FILE"' EXIT

cat > "$EXCLUDE_FILE" <<'EXCLUDES'
# Git metadata
.git/

# Runtime / local state
.omo/
.omx/
.pi/sessions/
.pi/drafts/

# npm dependencies
.pi/npm/node_modules/
.pi/npm/package-lock.json

# Python caches / virtual environments
__pycache__/
*.py[cod]
*.egg-info/
*.egg
.venv/
venv/
env/
dist/
build/
*.whl

# Secrets / credentials / private keys
.env
.env.*
*secret*
*token*
*credential*
*.pem
*.key
*.crt
*.p12
*.pfx
*.der
.known_hosts
.ssh/
.aws/
.gcp/

# Project runtime outputs / real research data
projects/*/chain-outputs/
projects/*/progress.json
projects/*/artifacts/
projects/*/data/
projects/*/reports/
projects/*/sources/

# Temporary / OS files
*.tmp
*.bak
*.swp
*.swo
*~
.DS_Store
Thumbs.db
EXCLUDES

echo "========================================"
echo "Source: $SOURCE_DIR"
echo "Target: $TARGET_DIR"
if [[ -n "$DRY_RUN" ]]; then
  echo "Mode:   DRY RUN"
else
  echo "Mode:   SYNC"
fi
echo "========================================"

rsync \
  -av \
  --delete \
  "$DRY_RUN" \
  --exclude-from="$EXCLUDE_FILE" \
  "$SOURCE_DIR/" \
  "$TARGET_DIR/"

if [[ -n "$VERIFY" ]]; then
  echo ""
  echo "========================================"
  echo "Verifying target for residual sensitive patterns"
  echo "========================================"

  FOUND=0

  # High-confidence patterns for secrets / credentials.
  # These aim to match actual key material, not documentation keywords.
  PATTERNS_FILE="$(mktemp -t sync-to-public-patterns.XXXXXX)"
  cat > "$PATTERNS_FILE" <<'PATTERNS'
BEGIN (RSA|OPENSSH|EC|DSA|PGP) PRIVATE KEY
BEGIN CERTIFICATE
api[_-]?key[[:space:]]*[:=][[:space:]]*"[a-zA-Z0-9_\-]{16,}"
api[_-]?key[[:space:]]*[:=][[:space:]]*'[a-zA-Z0-9_\-]{16,}'
sk-[a-zA-Z0-9]{20,}
Bearer[[:space:]]+[a-zA-Z0-9_\-\.]{20,}
ghp_[a-zA-Z0-9]{36,}
glpat-[a-zA-Z0-9\-]{20,}
AKIA[0-9A-Z]{16}
ASIA[0-9A-Z]{16}
PATTERNS

  while IFS= read -r pattern; do
    [[ -z "$pattern" ]] && continue
    matches=$(grep -EinR "$pattern" "$TARGET_DIR" \
      --exclude="sync-to-public.sh" \
      --exclude-dir=".git" \
      2>/dev/null || true)
    if [[ -n "$matches" ]]; then
      echo ""
      echo "Potential match for pattern: $pattern"
      echo "$matches" | head -20
      FOUND=1
    fi
  done < "$PATTERNS_FILE"

  rm -f "$PATTERNS_FILE"

  # Also flag any secret-like files that survived the rsync filter.
  surviving_secrets=$(find "$TARGET_DIR" -type f \( \
    -name '.env*' -o \
    -name '*.pem' -o \
    -name '*.key' -o \
    -name '*.p12' -o \
    -name '*.pfx' -o \
    -name '*.der' -o \
    -name '*secret*' -o \
    -name '*credential*' \
  \) 2>/dev/null || true)

  if [[ -n "$surviving_secrets" ]]; then
    echo ""
    echo "Surviving secret-like files:"
    echo "$surviving_secrets"
    FOUND=1
  fi

  # Ensure project runtime output directories were excluded.
  surviving_outputs=$(find "$TARGET_DIR/projects" -type d \( \
    -name 'chain-outputs' -o \
    -name 'artifacts' -o \
    -name 'data' -o \
    -name 'reports' -o \
    -name 'sources' \
  \) 2>/dev/null || true)

  if [[ -n "$surviving_outputs" ]]; then
    echo ""
    echo "Surviving project runtime output directories:"
    echo "$surviving_outputs"
    FOUND=1
  fi

  if [[ "$FOUND" -eq 0 ]]; then
    echo "No obvious sensitive patterns or files found in target."
  else
    echo ""
    echo "Warning: potential sensitive content detected. Review the matches above." >&2
    exit 1
  fi
fi

echo ""
echo "Done."
