#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOST="${BACKEND_HOST:-0.0.0.0}"
PORT="${BACKEND_PORT:-8000}"

cd "$ROOT_DIR/backend"

if [[ -f ".venv/bin/activate" ]]; then
  # Prefer the project-local virtual environment when it exists.
  # shellcheck disable=SC1091
  source ".venv/bin/activate"
fi

export PYTHONPATH="$ROOT_DIR/backend${PYTHONPATH:+:$PYTHONPATH}"

echo "Starting backend on http://${HOST}:${PORT}"
python -m uvicorn app.main:app --reload --host "$HOST" --port "$PORT"
