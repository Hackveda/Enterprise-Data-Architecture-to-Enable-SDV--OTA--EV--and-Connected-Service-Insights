#!/usr/bin/env bash
set -euo pipefail
cd dbt

dbt deps --profiles-dir . || true
dbt debug --profiles-dir .
dbt build --profiles-dir .

# dbt Core 2.0 release-candidate builds may be compiled without the embedded
# documentation UI. The data build is the deployment-critical step; docs are
# optional and should not fail the deployment.
if dbt docs generate --profiles-dir .; then
  echo "dbt docs generated successfully."
else
  echo "dbt docs UI is not available in this dbt build; continuing because dbt build succeeded."
fi
