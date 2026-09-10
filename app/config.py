from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    snowflake_account: str = "UIEPPMA-ME31407"
    snowflake_user: str = ""
    snowflake_password: str = ""
    snowflake_private_key_path: str = ""
    snowflake_role: str = "EDP_ENGINEER"
    snowflake_warehouse: str = "EDP_INGEST_WH"
    snowflake_database: str = "ENTERPRISE_DATA"
    snowflake_schema: str = "RAW"
    google_sheet_id: str = "16zlUwChc8rAZYrChvgvSGBVmN8nSlY-7wKQLu5ibbno"
    simulated_rps: int = 1_800_000
    physical_batch_rows: int = 100_000
    app_host: str = "0.0.0.0"
    app_port: int = 8501
    app_env: str = "production"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
