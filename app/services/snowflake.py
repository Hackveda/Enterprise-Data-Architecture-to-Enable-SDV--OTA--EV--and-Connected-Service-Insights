from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Any
import re
import snowflake.connector

from app.config import get_settings


@contextmanager
def connection(*, role_override: str | None = None, include_context: bool = True):
    s = get_settings()
    kwargs: dict[str, Any] = {
        "account": s.snowflake_account,
        "user": s.snowflake_user,
        "client_session_keep_alive": True,
    }
    role = role_override or s.snowflake_role
    if role:
        kwargs["role"] = role
    if include_context:
        if s.snowflake_warehouse:
            kwargs["warehouse"] = s.snowflake_warehouse
        if s.snowflake_database:
            kwargs["database"] = s.snowflake_database
    if s.snowflake_private_key_path:
        kwargs["private_key_file"] = str(Path(s.snowflake_private_key_path).expanduser())
    else:
        kwargs["password"] = s.snowflake_password

    conn = snowflake.connector.connect(**kwargs)
    try:
        yield conn
    finally:
        conn.close()


def credentials_configured() -> bool:
    s = get_settings()
    return bool(s.snowflake_user and (s.snowflake_password or s.snowflake_private_key_path))


def health() -> dict[str, Any]:
    if not credentials_configured():
        return {"connected": False, "message": "Snowflake credentials are not configured"}
    try:
        with connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "select current_account(), current_user(), current_role(), current_warehouse(), current_database()"
            )
            row = cur.fetchone()
            return {
                "connected": True,
                "account": row[0],
                "user": row[1],
                "role": row[2],
                "warehouse": row[3],
                "database": row[4],
            }
    except Exception as exc:
        return {"connected": False, "message": str(exc)[:300]}


def query_rows(sql: str, params: tuple[Any, ...] | None = None) -> list[dict[str, Any]]:
    with connection() as conn:
        cur = conn.cursor(snowflake.connector.DictCursor)
        cur.execute(sql, params or ())
        return [dict(r) for r in cur.fetchall()]


def team_kpis(team: str) -> dict[str, Any] | None:
    if not credentials_configured():
        return None
    view = {
        "marketing": "GOVERNED.V_MARKETING_DASHBOARD",
        "sales": "GOVERNED.V_SALES_DASHBOARD",
        "support": "GOVERNED.V_SUPPORT_DASHBOARD",
        "finance": "GOVERNED.V_FINANCE_DASHBOARD",
        "delivery": "GOVERNED.V_DELIVERY_DASHBOARD",
    }.get(team)
    if not view:
        return None
    try:
        rows = query_rows(f"select * from {view} order by SNAPSHOT_DATE desc limit 90")
        return {"source": "snowflake", "rows": rows}
    except Exception:
        return None


def _sql_statements(text: str) -> list[str]:
    """Return executable statements while ignoring SQL comments/empty chunks."""
    # Remove /* ... */ block comments.
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    # Remove full-line and trailing -- comments. Project SQL does not place --
    # inside string literals, so this keeps deployment parsing intentionally simple.
    cleaned_lines: list[str] = []
    for line in text.splitlines():
        line = line.split("--", 1)[0].strip()
        if line:
            cleaned_lines.append(line)
    cleaned = "\n".join(cleaned_lines)
    return [statement.strip() for statement in cleaned.split(";") if statement.strip()]


def run_sql_file(
    path: Path,
    *,
    role_override: str | None = None,
    include_context: bool = True,
) -> list[str]:
    """Execute Snowflake SQL with the configured platform role.

    This does not default to ACCOUNTADMIN. Comment-only/empty SQL chunks are
    filtered before execution so bootstrap files can contain normal comments.
    """
    statements = _sql_statements(path.read_text(encoding="utf-8"))
    executed: list[str] = []
    with connection(role_override=role_override, include_context=include_context) as conn:
        cur = conn.cursor()
        for statement in statements:
            cur.execute(statement)
            executed.append(statement.splitlines()[0][:120])
    return executed
