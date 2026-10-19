#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  ./codex-9router.sh --connect <9router-url> [api-key|local-key-id]
  ./codex-9router.sh --disconnect

Connect selects GPT-6-Luna (`cx/gpt-6-luna`) from <9router-url>/v1/models and
writes the remote provider to ~/.codex/config.toml.
Disconnect restores ~/.codex/config.toml as it was before the last connect.

When the API key argument is omitted, CODEX_9ROUTER_API_KEY or
NINEROUTER_API_KEY is used. Omitting the argument keeps the key out of the
process argument list. A local 9Router API-key ID can be used when the native
key database is available at ~/.9router/db/data.sqlite.
EOF
}

if [[ -z "${HOME:-}" ]]; then
  printf 'HOME is not set.\n' >&2
  exit 2
fi

codex_home="${CODEX_HOME:-$HOME/.codex}"
if [[ "$codex_home" != "$HOME/.codex" ]]; then
  printf 'This script only supports %s/.codex/config.toml.\n' "$HOME" >&2
  printf 'Unset CODEX_HOME before running this script.\n' >&2
  exit 2
fi

config_file="$codex_home/config.toml"
state_dir="$codex_home/.9router-connect-state"
config_backup="$state_dir/config.toml"
config_absent_marker="$state_dir/config-was-absent"

restore_saved_config() {
  if [[ -f "$config_backup" ]]; then
    local restore_file="$config_file.restore.$$"
    cp -p -- "$config_backup" "$restore_file"
    mv -f -- "$restore_file" "$config_file"
  elif [[ -e "$config_absent_marker" ]]; then
    python3 - "$config_file" <<'PY'
from pathlib import Path
import sys
Path(sys.argv[1]).unlink(missing_ok=True)
PY
  else
    printf 'Saved Codex config backup is missing; refusing to change the current config.\n' >&2
    return 1
  fi
}

clear_saved_state() {
  python3 - "$state_dir" <<'PY'
from pathlib import Path
import sys

directory = Path(sys.argv[1])
for entry in directory.iterdir():
    if entry.is_file() or entry.is_symlink():
        entry.unlink()
    else:
        raise SystemExit(f"Unexpected directory in saved state: {entry}")
directory.rmdir()
PY
}

write_codex_config() {
  API_KEY="$api_key" python3 - "$config_file" "$base_url" "$model" <<'PY'
import json
import os
import re
import sys
import tempfile
from pathlib import Path

config_path = Path(sys.argv[1])
base_url = sys.argv[2].rstrip("/") + "/v1"
model = sys.argv[3]
api_key = os.environ["API_KEY"]

if config_path.exists():
    text = config_path.read_text()
else:
    text = ""

lines = []
section = None
skip_provider = False
agents_seen = False
agents_default_written = False
for line in text.splitlines(keepends=True):
    stripped = line.strip()
    if stripped.startswith("[") and stripped.endswith("]"):
        if section == "agents" and not agents_default_written:
            lines.append(f"default_subagent_model = {json.dumps(model)}\n")
            agents_default_written = True
        section = stripped.lstrip("[").rstrip("]").strip()
        skip_provider = section == "model_providers.9router" or section.startswith("model_providers.9router.")
        if section == "agents":
            agents_seen = True
    if skip_provider:
        continue
    if section is None and re.match(r"^\s*(?:model|model_provider)\s*=", line):
        continue
    if section == "agents" and re.match(r"^\s*default_subagent_model\s*=", line):
        if not agents_default_written:
            lines.append(f"default_subagent_model = {json.dumps(model)}\n")
            agents_default_written = True
        continue
    lines.append(line)

if section == "agents" and not agents_default_written:
    lines.append(f"default_subagent_model = {json.dumps(model)}\n")
    agents_default_written = True

prefix = "".join((
    f"model = {json.dumps(model)}\n",
    'model_provider = "9router"\n',
))
provider = "".join((
    "\n[model_providers.9router]\n",
    'name = "9Router"\n',
    f"base_url = {json.dumps(base_url)}\n",
    'wire_api = "responses"\n',
    "\n[model_providers.9router.http_headers]\n",
    f"Authorization = {json.dumps('Bearer ' + api_key)}\n",
))
if not agents_seen:
    provider += "".join((
        "\n[agents]\n",
        f"default_subagent_model = {json.dumps(model)}\n",
    ))
content = prefix + "".join(lines).rstrip("\n") + "\n" + provider

config_path.parent.mkdir(parents=True, exist_ok=True)
fd, temporary = tempfile.mkstemp(prefix=f".{config_path.name}.", dir=config_path.parent)
try:
    with os.fdopen(fd, "w") as output:
        output.write(content)
    os.chmod(temporary, 0o600)
    os.replace(temporary, config_path)
except BaseException:
    try:
        os.unlink(temporary)
    except FileNotFoundError:
        pass
    raise
PY
}

resolve_api_key_reference() {
  if [[ ! "$api_key" =~ ^[[:xdigit:]]{8}-[[:xdigit:]]{4}-[[:xdigit:]]{4}-[[:xdigit:]]{4}-[[:xdigit:]]{12}$ ]]; then
    return 0
  fi

  local router_db="${NINEROUTER_DB:-$HOME/.9router/db/data.sqlite}"
  if [[ ! -r "$router_db" ]]; then
    printf 'A server-local API-key ID was supplied, but this machine cannot read the local 9Router key database: %s\n' "$router_db" >&2
    printf 'Remote clients must use the raw bearer secret (or CODEX_9ROUTER_KEY_FILE), not the UUID from `9router-policy keys`.\n' >&2
    return 1
  fi

  api_key="$(KEY_REFERENCE="$api_key" ROUTER_DB="$router_db" python3 - <<'PY'
import os
import sqlite3

reference = os.environ["KEY_REFERENCE"]
database = os.environ["ROUTER_DB"]
try:
    connection = sqlite3.connect(f"file:{database}?mode=ro", uri=True)
    row = connection.execute(
        "SELECT key FROM apiKeys WHERE id = ? AND isActive = 1",
        (reference,),
    ).fetchone()
finally:
    try:
        connection.close()
    except UnboundLocalError:
        pass

if row is None or not row[0]:
    print(f"No active 9Router API key matches ID: {reference}", file=os.sys.stderr)
    raise SystemExit(1)
print(row[0])
PY
)"
}

case "${1:-}" in
  --connect)
    if [[ $# -lt 2 || $# -gt 3 ]]; then
      usage >&2
      exit 2
    fi
    input_url="$2"
    if [[ $# -eq 3 ]]; then
      api_key="$3"
    else
      api_key="${CODEX_9ROUTER_API_KEY:-${NINEROUTER_API_KEY:-}}"
    fi
    if [[ -z "$api_key" ]]; then
      printf 'API key cannot be empty.\n' >&2
      exit 2
    fi
    if ! command -v python3 >/dev/null 2>&1; then
      printf 'python3 is required to validate the URL and discover a model.\n' >&2
      exit 127
    fi
    resolve_api_key_reference
    base_url="$(python3 - "$input_url" <<'PY'
from urllib.parse import urlsplit, urlunsplit
import sys

raw = sys.argv[1].strip()
try:
    parsed = urlsplit(raw)
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise ValueError
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError
    if parsed.path not in ("", "/", "/v1", "/v1/"):
        raise ValueError
    print(urlunsplit((parsed.scheme, parsed.netloc, "", "", "")))
except ValueError:
    print('URL must be an http(s) origin, optionally ending in /v1, with no credentials or query.', file=sys.stderr)
    raise SystemExit(2)
PY
)"

    model="$(API_KEY="$api_key" python3 - "$base_url" <<'PY'
import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

url = sys.argv[1].rstrip("/") + "/v1/models"
request = Request(url, headers={"Authorization": "Bearer " + os.environ["API_KEY"], "Accept": "application/json"})
try:
    with urlopen(request, timeout=20) as response:
        payload = json.load(response)
except HTTPError as error:
    if error.code in (401, 403):
        print('The API key was rejected by 9router.', file=sys.stderr)
    else:
        print(f'9router returned HTTP {error.code} while listing models.', file=sys.stderr)
    raise SystemExit(1)
except (URLError, TimeoutError, OSError, json.JSONDecodeError) as error:
    print(f'Could not reach 9router or read its model list: {error}', file=sys.stderr)
    raise SystemExit(1)

models = payload.get("data", []) if isinstance(payload, dict) else []
target = "cx/gpt-6-luna"
model = next((item.get("id") for item in models if isinstance(item, dict) and item.get("id") == target), None)
if model is None:
    print(f'9router does not advertise the required model: {target}.', file=sys.stderr)
    raise SystemExit(1)
print(model)
PY
)"

    if [[ -e "$state_dir" ]]; then
      printf 'A saved pre-connect config already exists. Run --disconnect before connecting again.\n' >&2
      exit 1
    fi
    if [[ -L "$config_file" ]]; then
      printf 'Refusing to modify a symlinked Codex config.\n' >&2
      exit 1
    fi

    mkdir -p -- "$codex_home"
    mkdir -m 700 -- "$state_dir"
    if [[ -e "$config_file" ]]; then
      cp -p -- "$config_file" "$config_backup"
      chmod 600 -- "$config_backup"
    else
      : > "$config_absent_marker"
      chmod 600 -- "$config_absent_marker"
    fi
    if write_codex_config; then
      printf 'Codex is connected to %s/v1 using model %s.\n' "$base_url" "$model"
      printf 'Run ./codex-9router.sh --disconnect to restore its previous config.\n'
    else
      printf 'Could not configure Codex; restoring the saved config.\n' >&2
      restore_saved_config || true
      clear_saved_state || true
      exit 1
    fi
    ;;

  --disconnect)
    if [[ $# -ne 1 ]]; then
      usage >&2
      exit 2
    fi
    if [[ ! -d "$state_dir" || -L "$state_dir" ]]; then
      printf 'No saved remote config found; Codex is already disconnected or was configured another way.\n'
      exit 0
    fi
    restore_saved_config
    clear_saved_state
    printf 'Codex config restored to its pre-connect state.\n'
    ;;

  -h|--help)
    usage
    ;;
  *)
    usage >&2
    exit 2
    ;;
esac
