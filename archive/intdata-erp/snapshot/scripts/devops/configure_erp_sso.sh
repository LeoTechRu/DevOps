#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd -- "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO_ROOT=$(cd -- "${SCRIPT_DIR}/../.." && pwd)
COMPOSE_FILE="${REPO_ROOT}/erp/docker-compose.yaml"
ENV_FILE="${REPO_ROOT}/erp/.env"

if [[ ! -f "${ENV_FILE}" ]]; then
  echo "[configure_erp_sso] Missing ${ENV_FILE}. Создайте его на основе erp/.env.template" >&2
  exit 1
fi

if [[ ! -f "${COMPOSE_FILE}" ]]; then
  echo "[configure_erp_sso] Не найден docker-compose файл ${COMPOSE_FILE}" >&2
  exit 1
fi

if ! command -v docker >/dev/null 2>&1; then
  echo "[configure_erp_sso] Требуется docker" >&2
  exit 1
fi

COMPOSE=(docker compose -f "${COMPOSE_FILE}")

mapfile -t REQUIRED <<'EOF'
KEYCLOAK_BASE_URL
KEYCLOAK_REALM
ODOO_KEYCLOAK_CLIENT_ID
ODOO_KEYCLOAK_CLIENT_SECRET
ODOO_DB_NAME
ODOO_DB_HOST
ODOO_DB_PORT
ODOO_DB_USER
ODOO_DB_PASSWORD
ERPNEXT_SITE_NAME
ERPNEXT_KEYCLOAK_CLIENT_ID
ERPNEXT_KEYCLOAK_CLIENT_SECRET
ERPNEXT_DB_ROOT_PASSWORD
ERPNEXT_DB_USER
ERPNEXT_DB_PASSWORD
EOF

while IFS= read -r line; do
  [[ -z "$line" || "${line}" =~ ^# ]] && continue
  export "$line"
done < <(grep -v '^#' "${ENV_FILE}")

missing=()
for key in "${REQUIRED[@]}"; do
  if [[ -z "${!key:-}" ]]; then
    missing+=("$key")
  fi
done

if (( ${#missing[@]} )); then
  printf '[configure_erp_sso] Отсутствуют обязательные переменные: %s
' "${missing[*]}" >&2
  exit 1
fi

if ! ${COMPOSE[@]} ps >/dev/null 2>&1; then
  echo "[configure_erp_sso] Контейнеры не запущены. Выполните 'docker compose -f erp/docker-compose.yaml up -d'" >&2
  exit 1
fi

# Odoo configure
ODOO_CMD=("${COMPOSE[@]}" exec -T odoo-dev python3 -m intdata_erp_sso.odoo)
echo "[configure_erp_sso] Настройка Odoo OAuth провайдера..."
if ! "${ODOO_CMD[@]}"; then
  echo "[configure_erp_sso] ⚠️  Не удалось настроить Odoo" >&2
  exit 1
fi

# ERPNext configure
ERPNEXT_CMD=("${COMPOSE[@]}" exec -T erpnext bench --site "${ERPNEXT_SITE_NAME}" execute intdata_erp_sso.erpnext.configure)
echo "[configure_erp_sso] Настройка ERPNext Social Login..."
if ! "${ERPNEXT_CMD[@]}"; then
  echo "[configure_erp_sso] ⚠️  Не удалось настроить ERPNext" >&2
  exit 1
fi

echo "[configure_erp_sso] Готово. Проверьте вход через Keycloak в Odoo и ERPNext."
