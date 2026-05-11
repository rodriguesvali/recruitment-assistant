#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOST="${FRONTEND_HOST:-0.0.0.0}"
PORT="${FRONTEND_PORT:-4200}"

cd "$ROOT_DIR/frontend"

echo "Starting frontend on http://${HOST}:${PORT}"
npm start -- --host "$HOST" --port "$PORT"
