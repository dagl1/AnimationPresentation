#!/usr/bin/env bash
set -euo pipefail

echo "🚀 Bootstrapping project..."

# --------------------------------------
# Helpers
# --------------------------------------
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

OS="$(uname -s)"

# --------------------------------------
# Install uv
# --------------------------------------
if ! command_exists uv; then
  echo "🔧 Installing uv..."
  case "$OS" in
    Linux|Darwin)
      wget -qO- https://astral.sh/uv/install.sh | sh
      ;;
    *)
      echo "❌ Unsupported OS for automatic uv install: $OS"
      echo "👉 On Windows, run:"
      echo 'powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"'
      exit 1
      ;;
  esac
else
  echo "✅ uv already installed"
fi

# Make sure uv is available in this shell
export PATH="$HOME/.cargo/bin:$PATH"

# --------------------------------------
# Install Node / npm
# --------------------------------------
if ! command_exists npm; then
  echo "❌ npm not found."
  echo "👉 Install Node.js from https://nodejs.org or via your system package manager."
  exit 1
else
  echo "✅ npm available"
fi

# --------------------------------------
# Initialize Python project
# --------------------------------------
if [ ! -f pyproject.toml ]; then
  echo "📦 Initializing uv project (Python 3.14)..."
  uv venv --python 3.14
  uv init
  # --------------------------------------
  # Merge pyproject bootstrap config
  # --------------------------------------
  BOOTSTRAP_FILE="bootstrap/pyproject_bootstrap.toml"

  if [ -f "$BOOTSTRAP_FILE" ]; then
    echo "🧩 Merging pyproject bootstrap config..."
    cat "$BOOTSTRAP_FILE" >> pyproject.toml
  else
    echo "⚠️ $BOOTSTRAP_FILE not found, skipping merge"
  fi
else
  echo "ℹ️ pyproject.toml already exists"
fi



# --------------------------------------
# Add Python tooling
# --------------------------------------
echo "📚 Adding Python dependencies..."
uv add \
  black \
  isort \
  mypy \
  commitizen \
  sphinx \
  python-semantic-release \
  pre-commit \
  ruff \
  pytest \
  ty

# --------------------------------------
# Install commitizen as tool
# --------------------------------------
echo "🧰 Installing commitizen tool..."
uv tool install commitizen

# --------------------------------------
# Initialize commitizen
# --------------------------------------
if [ ! -f .cz.toml ]; then
  echo "📝 Initializing commitizen..."
  cz init
else
  echo "ℹ️ commitizen already initialized"
fi

# --------------------------------------
# Commitlint (Node)
# --------------------------------------
echo "📦 Installing commitlint..."
npm install -D @commitlint/cli @commitlint/config-conventional

# --------------------------------------
# Git config
# --------------------------------------
echo "🔧 Configuring git..."
git config core.autocrlf false

# --------------------------------------
# Pre-commit
# --------------------------------------
echo "🪝 Initializing pre-commit..."
uv run pre-commit install
uv run pre-commit install --hook-type commit-msg

echo "✅ Bootstrap complete!"

read -p "Press Enter to exit..."
