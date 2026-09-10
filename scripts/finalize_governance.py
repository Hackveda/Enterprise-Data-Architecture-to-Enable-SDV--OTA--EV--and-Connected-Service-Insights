from pathlib import Path
from app.services.snowflake import credentials_configured, run_sql_file
if not credentials_configured(): raise SystemExit('Configure Snowflake credentials in .env first')
for line in run_sql_file(Path('snowflake/sql/03_secure_views_grants.sql')): print('OK',line)
print('Governed secure views and team grants are ready.')
