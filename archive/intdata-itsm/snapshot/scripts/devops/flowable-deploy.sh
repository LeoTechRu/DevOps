#!/usr/bin/env bash
set -euo pipefail

# Deploys all BPMN diagrams from itsm/bpmn into Flowable REST runtime.
# Requires ITSM_FLOWABLE_BASE_URL / USERNAME / PASSWORD (fallback to legacy FLOWABLE_*).
# Defaults align with local docker compose stack.

FLOWABLE_BASE_URL="${ITSM_FLOWABLE_BASE_URL:-${FLOWABLE_BASE_URL:-http://127.0.0.1:8095/flowable-task/process-api}}"
FLOWABLE_USERNAME="${ITSM_FLOWABLE_USERNAME:-${FLOWABLE_USERNAME:-admin}}"
FLOWABLE_PASSWORD="${ITSM_FLOWABLE_PASSWORD:-${FLOWABLE_PASSWORD:-test}}"
BPMN_DIR="${BPMN_DIR:-itsm/bpmn}"

if [[ ! -d "$BPMN_DIR" ]]; then
  echo "BPMN directory not found: $BPMN_DIR" >&2
  exit 1
fi

echo "Deploying BPMN diagrams from $BPMN_DIR to $FLOWABLE_BASE_URL"

for file in "$BPMN_DIR"/*.bpmn20.xml; do
  [[ -e "$file" ]] || continue
  deploy_name=$(basename "$file" .bpmn20.xml)
  echo " - $deploy_name"
  response=$(curl -sS -u "${FLOWABLE_USERNAME}:${FLOWABLE_PASSWORD}" \
    -F "file=@${file}" \
    -F "deploymentName=${deploy_name}" \
    "${FLOWABLE_BASE_URL}/repository/deployments")
  if command -v jq >/dev/null 2>&1; then
    echo "$response" | jq '.name, .id'
  else
    echo "$response"
  fi
  if [[ "$response" == *"error"* ]]; then
    echo "Deployment failed for $file" >&2
    exit 1
  fi
done

echo "Done."
