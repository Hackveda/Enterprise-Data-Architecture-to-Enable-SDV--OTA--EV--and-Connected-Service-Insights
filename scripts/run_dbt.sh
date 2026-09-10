#!/usr/bin/env bash
set -euo pipefail
cd dbt
dbt deps --profiles-dir . || true
dbt debug --profiles-dir .
dbt build --profiles-dir .
dbt docs generate --profiles-dir .
