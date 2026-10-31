#!/usr/bin/env sh
# macOS / Linux bootstrap: install uv if missing, then run the cross-platform setup.
# Usage (from this folder):  sh setup.sh
set -e
cd "$(dirname "$0")"

if ! command -v uv >/dev/null 2>&1; then
  echo "uv (Python manager) not found. Installing it..."
  if command -v brew >/dev/null 2>&1; then
    brew install uv
  else
    curl -LsSf https://astral.sh/uv/install.sh | sh
  fi
  export PATH="$HOME/.local/bin:$PATH"
fi

uv run python .claude/skills/installation-setup/scripts/setup.py all
