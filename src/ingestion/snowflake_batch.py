from __future__ import annotations
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
from src.config import settings


def connect(schema: str | None = None):
    if not settings.snowflake_user:
        raise RuntimeError('Set SNOWFLAKE_USER and authentication variables in .env')
    kwargs = dict(
        account=settings.snowflake_account,
        user=settings.snowflake_user,
        role=settings.snowflake_role,
        warehouse=settings.snowflake_warehouse,
        database=settings.snowflake_database,
        schema=schema or settings.snowflake_schema,
    )
    if settings.snowflake_password:
        kwargs['password'] = settings.snowflake_password
    return snowflake.connector.connect(**kwargs)


def append_dataframe(df, table: str, schema: str = 'RAW'):
    df = df.copy()
    df.columns = [c.upper() for c in df.columns]
    with connect(schema) as conn:
        ok, chunks, rows, _ = write_pandas(conn, df, table.upper(), auto_create_table=False, overwrite=False)
        if not ok:
            raise RuntimeError(f'write_pandas failed for {schema}.{table}')
        return {'chunks': chunks, 'rows': rows}
