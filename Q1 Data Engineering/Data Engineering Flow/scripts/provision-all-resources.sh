#!/usr/bin/env bash
# Mirror of provision-all-resources.ps1 for Linux/macOS/WSL
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_PATH="${CONFIG_PATH:-$SCRIPT_DIR/../infra/parameters.dev.json}"
DRY_RUN="${DRY_RUN:-false}"
CFG=$(cat "$CONFIG_PATH")
SUB=$(echo "$CFG" | python -c "import sys,json; print(json.load(sys.stdin).get('subscriptionId',''))")
RG=$(echo "$CFG" | python -c "import sys,json; print(json.load(sys.stdin)['resourceGroup'])")
LOC=$(echo "$CFG" | python -c "import sys,json; print(json.load(sys.stdin)['location'])")
PREFIX=$(echo "$CFG" | python -c "import sys,json; print(json.load(sys.stdin)['namingPrefix'])")
SUFFIX=""
if [ "$(echo "$CFG" | python -c "import sys,json; print(json.load(sys.stdin).get('useRandomSuffix',False))")" = "True" ]; then
  SUFFIX=$(printf "%04d" $((RANDOM % 10000)))
fi
[[ -n "$SUB" ]] && az account set --subscription "$SUB"
az account show >/dev/null || { echo "Run: az login"; exit 1; }
ST_LAKE="st${PREFIX}lake${SUFFIX}"
ST_SRC="st${PREFIX}src${SUFFIX}"
ST_LAKE=${ST_LAKE:0:24}; ST_SRC=${ST_SRC:0:24}
run() { if [ "$DRY_RUN" = "true" ]; then echo "[DryRun] $*"; else eval "$@"; fi }
run "az group create -n $RG -l $LOC --tags project=retail-data-pipeline"
run "az storage account create -g $RG -n $ST_LAKE -l $LOC --sku Standard_LRS --kind StorageV2 --hierarchical-namespace true"
run "az storage account create -g $RG -n $ST_SRC -l $LOC --sku Standard_LRS --kind StorageV2 --hierarchical-namespace true"
echo "See provision-all-resources.ps1 for full steps (SQL, Postgres, Cosmos, ADF, Databricks)."
