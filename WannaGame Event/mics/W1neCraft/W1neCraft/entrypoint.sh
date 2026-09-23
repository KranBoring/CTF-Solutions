#!/usr/bin/env bash
set -euo pipefail

RUNTIME_DIR=/run/server
TEMPLATE_DIR=/opt/challenge/server-template
MEMORY="${MEMORY:-1536M}"
BACKEND_HOST="${BACKEND_HOST:-127.0.0.1}"
BACKEND_PORT="${BACKEND_PORT:-$((30000 + RANDOM % 20000))}"
PUBLIC_HOST="${PUBLIC_HOST:-0.0.0.0}"
PUBLIC_PORT="${PUBLIC_PORT:-1337}"

echo "${FLAG:-}" > /flag.txt
chown root:root /flag.txt
chmod 600 /flag.txt
unset FLAG

rm -rf "${RUNTIME_DIR}"
mkdir -p "${RUNTIME_DIR}"
cp -a "${TEMPLATE_DIR}/." "${RUNTIME_DIR}/"

cd "${RUNTIME_DIR}"

set_property() {
  local key="$1"
  local value="$2"
  local file="server.properties"

  if grep -q "^${key}=" "${file}"; then
    sed -i "s|^${key}=.*|${key}=${value}|" "${file}"
  else
    printf '%s=%s\n' "${key}" "${value}" >> "${file}"
  fi
}

set_property "server-ip" "${BACKEND_HOST}"
set_property "server-port" "${BACKEND_PORT}"
echo "Backend Minecraft server: ${BACKEND_HOST}:${BACKEND_PORT}"
echo "Public challenge proxy: ${PUBLIC_HOST}:${PUBLIC_PORT}"

java -Xms512M -Xmx"${MEMORY}" -jar forge-1.12.2-14.23.5.2864.jar nogui &
SERVER_PID=$!

for _ in $(seq 1 90); do
  if grep -q "Done (" logs/latest.log 2>/dev/null; then
    break
  fi
  if ! kill -0 "${SERVER_PID}" 2>/dev/null; then
    wait "${SERVER_PID}"
  fi
  sleep 1
done

W1_HOST="${BACKEND_HOST}" W1_PORT="${BACKEND_PORT}" node /opt/challenge/bot/w1-player.js &
BOT_PID=$!

for _ in $(seq 1 45); do
  if grep -q "Reserved real player connected" logs/latest.log 2>/dev/null; then
    break
  fi
  if ! kill -0 "${SERVER_PID}" 2>/dev/null; then
    wait "${SERVER_PID}"
  fi
  sleep 1
done

if ! grep -q "Reserved real player connected" logs/latest.log 2>/dev/null; then
  echo "W1_player failed to join; refusing to open public proxy."
  exit 1
fi

PROXY_HOST="${PUBLIC_HOST}" PROXY_PORT="${PUBLIC_PORT}" BACKEND_HOST="${BACKEND_HOST}" BACKEND_PORT="${BACKEND_PORT}" node /opt/challenge/bot/login-proxy.js &
PROXY_PID=$!

cleanup() {
  kill "${PROXY_PID}" 2>/dev/null || true
  kill "${BOT_PID}" 2>/dev/null || true
  kill "${SERVER_PID}" 2>/dev/null || true
}
trap cleanup INT TERM EXIT

wait "${SERVER_PID}"
