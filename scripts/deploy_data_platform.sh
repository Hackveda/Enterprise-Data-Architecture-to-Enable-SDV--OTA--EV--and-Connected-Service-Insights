#!/usr/bin/env bash
set -euo pipefail
set -a
source .env
set +a
export PYTHONPATH="${PYTHONPATH:-}:$(pwd)"
python scripts/bootstrap_snowflake.py
./scripts/run_dbt.sh
python scripts/finalize_governance.py
python - <<'PY'
from app.services.snowflake import health
print(health())
PY
