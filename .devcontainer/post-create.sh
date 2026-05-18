#!/usr/bin/env bash
set -euo pipefail

python -m pip install --upgrade pip
python -m pip install -r .devcontainer/requirements-bootstrap.txt
npm install -g @angular/cli

primeng_mcp_dir="${HOME}/.codex/mcp/primeng"
codex_config="${HOME}/.codex/config.toml"

mkdir -p "${primeng_mcp_dir}" "${HOME}/.codex"
cp .devcontainer/primeng-mcp-package.json "${primeng_mcp_dir}/package.json"
npm install --prefix "${primeng_mcp_dir}"
touch "${codex_config}"

tmp_codex_config="$(mktemp)"
awk '
  /^\[mcp_servers\.(primeng|prime-ng)\]$/ { skip = 1; next }
  /^\[/ { skip = 0 }
  !skip { print }
' "${codex_config}" > "${tmp_codex_config}"
mv "${tmp_codex_config}" "${codex_config}"

{
  printf "\n[mcp_servers.primeng]\n"
  printf "command = \"%s/node_modules/.bin/primeng-mcp\"\n" "${primeng_mcp_dir}"
  printf "enabled = true\n"
  printf "startup_timeout_sec = 30\n"
  printf "tool_timeout_sec = 60\n"
} >> "${codex_config}"

if [ -f backend/requirements.txt ]; then
  python -m pip install -r backend/requirements.txt
fi

if [ -f backend/pyproject.toml ] || [ -f backend/setup.py ]; then
  python -m pip install -e backend
fi
