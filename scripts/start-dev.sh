#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cleanup() {
  jobs -p | xargs -r kill
}

trap cleanup EXIT INT TERM

"$ROOT_DIR/scripts/start-backend.sh" &
"$ROOT_DIR/scripts/start-frontend.sh" &

wait
