#!/usr/bin/env bash
#
# auto-commit.sh — File-system watcher that automatically commits (and pushes)
# any change inside the MedicineMarket-Atlas repository.
#
# Uses macOS fswatch. The watcher ignores paths already excluded by .gitignore
# plus the .git directory itself to avoid recursive commit storms.
#
# Usage:
#   ./scripts/auto-commit.sh              # start watcher in foreground
#   ./scripts/auto-commit.sh --install    # install LaunchAgent (runs on login)
#   ./scripts/auto-commit.sh --uninstall  # remove LaunchAgent
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
PLIST_LABEL="com.medicinemarket-atlas.autocommit"
PLIST_PATH="${HOME}/Library/LaunchAgents/${PLIST_LABEL}.plist"

# Ensure Homebrew binaries are available for LaunchAgent sessions, which run
# with a minimal PATH.
export PATH="/opt/homebrew/bin:/usr/local/bin:${PATH}"

# Debounce window in seconds: changes are batched into a single commit if they
# arrive within this interval. Prevents a storm of tiny commits.
DEBOUNCE_SECONDS="${AUTO_COMMIT_DEBOUNCE:-30}"

log() {
  printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" >&2
}

require_fswatch() {
  if ! command -v fswatch &>/dev/null; then
    log "ERROR: fswatch is required but not installed."
    log "Install it with: brew install fswatch"
    exit 1
  fi
}

# Return 0 if the current working tree inside REPO_ROOT has changes to commit.
has_changes() {
  local status
  status="$(git -C "${REPO_ROOT}" status --porcelain)"
  [[ -n "${status}" ]]
}

# Perform one batched commit + push.
commit_and_push() {
  if ! has_changes; then
    return 0
  fi

  local timestamp msg
  timestamp="$(date '+%Y-%m-%d %H:%M:%S')"
  msg="auto: sync local changes at ${timestamp}"

  log "Committing local changes..."
  git -C "${REPO_ROOT}" add -A
  git -C "${REPO_ROOT}" commit -m "${msg}" || {
    log "WARNING: commit failed; will retry on next change."
    return 1
  }

  log "Pushing to origin..."
  git -C "${REPO_ROOT}" push origin HEAD || {
    log "WARNING: push failed (network/auth?). Changes are committed locally."
    return 1
  }

  log "Done."
}

# Watcher loop with debounce.
run_watcher() {
  require_fswatch
  cd "${REPO_ROOT}"

  log "Starting auto-commit watcher for ${REPO_ROOT}"
  log "Debounce: ${DEBOUNCE_SECONDS}s | Push: enabled"

  local pending=0
  local timer_pid=""

  # fswatch emits one line per batch of events. Exclude noisy/generated paths.
  fswatch \
    -r \
    -E \
    --exclude='^\.git/' \
    --exclude='node_modules' \
    --exclude='\.DS_Store$' \
    --exclude='\.tmp$' \
    --exclude='\.bak$' \
    --exclude='\.swp$' \
    --exclude='\.swo$' \
    --exclude='\.omo/' \
    --exclude='\.omx/' \
    --exclude='\.venv/' \
    --exclude='venv/' \
    --exclude='__pycache__' \
    --exclude='\.pyc$' \
    --exclude='\.auto-commit\.log$' \
    "${REPO_ROOT}" | while IFS= read -r _event; do

    # Cancel any pending timer.
    if [[ -n "${timer_pid}" ]] && kill "${timer_pid}" &>/dev/null; then
      wait "${timer_pid}" 2>/dev/null || true
    fi

    # Start a new debounce timer.
    (
      sleep "${DEBOUNCE_SECONDS}"
      commit_and_push
    ) &
    timer_pid=$!
  done
}

install_launchagent() {
  mkdir -p "$(dirname "${PLIST_PATH}")"

  cat > "${PLIST_PATH}" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>${PLIST_LABEL}</string>
  <key>ProgramArguments</key>
  <array>
    <string>${REPO_ROOT}/scripts/auto-commit.sh</string>
    <string>--watch</string>
  </array>
  <key>WorkingDirectory</key>
  <string>${REPO_ROOT}</string>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>
  <key>StandardOutPath</key>
  <string>${REPO_ROOT}/.auto-commit.log</string>
  <key>StandardErrorPath</key>
  <string>${REPO_ROOT}/.auto-commit.log</string>
</dict>
</plist>
EOF

  launchctl unload "${PLIST_PATH}" 2>/dev/null || true
  launchctl load "${PLIST_PATH}"
  log "LaunchAgent installed and loaded: ${PLIST_PATH}"
}

uninstall_launchagent() {
  if [[ -f "${PLIST_PATH}" ]]; then
    launchctl unload "${PLIST_PATH}" 2>/dev/null || true
    rm -f "${PLIST_PATH}"
    log "LaunchAgent removed: ${PLIST_PATH}"
  else
    log "LaunchAgent not found; nothing to uninstall."
  fi
}

case "${1:-}" in
  --install)
    install_launchagent
    ;;
  --uninstall)
    uninstall_launchagent
    ;;
  --watch)
    run_watcher
    ;;
  *)
    run_watcher
    ;;
esac
