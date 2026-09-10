from pathlib import Path
from app.services.snowflake import credentials_configured, run_sql_file
PRE_DBT=[Path('snowflake/sql/00_bootstrap.sql'),Path('snowflake/sql/01_raw_tables.sql'),Path('snowflake/sql/02_governance.sql'),Path('snowflake/sql/04_monitoring.sql')]
if not credentials_configured(): raise SystemExit('Configure Snowflake credentials in .env first')
for path in PRE_DBT:
    print(f'\n==> {path}')
    for line in run_sql_file(path): print('  OK',line)
print('Pre-dbt bootstrap complete. Next: ./scripts/run_dbt.sh && python scripts/finalize_governance.py')
