from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    snowflake_account: str = os.getenv('SNOWFLAKE_ACCOUNT', 'UIEPPMA-ME31407')
    snowflake_user: str = os.getenv('SNOWFLAKE_USER', '')
    snowflake_password: str = os.getenv('SNOWFLAKE_PASSWORD', '')
    snowflake_role: str = os.getenv('SNOWFLAKE_ROLE', 'EDP_ENGINEER')
    snowflake_warehouse: str = os.getenv('SNOWFLAKE_WAREHOUSE', 'EDP_INGEST_WH')
    snowflake_database: str = os.getenv('SNOWFLAKE_DATABASE', 'ENTERPRISE_DATA')
    snowflake_schema: str = os.getenv('SNOWFLAKE_SCHEMA', 'RAW')
    google_sheet_id: str = os.getenv('GOOGLE_SHEET_ID', '16zlUwChc8rAZYrChvgvSGBVmN8nSlY-7wKQLu5ibbno')
    simulated_rps: int = int(os.getenv('SIMULATED_RPS', '1800000'))
    physical_batch_rows: int = int(os.getenv('PHYSICAL_BATCH_ROWS', '100000'))

settings = Settings()
