# Enterprise Data Architecture to Enable SDV, OTA, EV and Connected-Service Insights

Production-style automotive enterprise data platform for a live AWS EC2 demo with Snowflake, dbt and FastAPI.

## v2 architecture

- Replaced Streamlit with **FastAPI + server-rendered HTML + Server-Sent Events (SSE)**.
- Added role-specific command centers for **Marketing, Sales, Support, Finance and Delivery**.
- Added Snowflake bootstrap for `RAW`, `STAGING`, `CURATED`, `MARTS`, `GOVERNED`, `GOVERNANCE`.
- Added dbt staging, Customer 360, Vehicle 360 and five team marts.
- Added secure Snowflake views and role-based grants so the UI reads governed marts instead of raw tables.
- Added live logical event-rate simulation at **1.8M events/sec by default**. This is a logical business/event simulation; physical ingestion throughput must be benchmarked on the deployed topology.
- Added evidence-led 2026 automotive consumer-study visualizations and recommendations while separating survey research from live enterprise KPIs.

## Security first

Never commit `.env`, EC2 `.pem` files, Snowflake passwords or private keys. The previous public repository history contained a PEM/credential file; rotate any exposed key even after deleting it from the current branch.

## EC2 install

```bash
sudo apt update
sudo apt install -y python3-venv python3-pip git
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
nano .env
```

Set your real Snowflake username/password only in `.env` on EC2.

## Deploy Snowflake + dbt + governance

For the first bootstrap, the Snowflake user must have `ACCOUNTADMIN` (or equivalent object-creation privileges). After objects and roles are created, normal operation uses `EDP_ENGINEER`.

```bash
set -a; source .env; set +a
./scripts/deploy_data_platform.sh
```

That performs:

```text
Snowflake bootstrap
  RAW tables + governance + monitoring
           ↓
dbt build
  STAGING → CURATED → MARTS
           ↓
secure GOVERNED views + team grants
```

Objects created:

```text
ENTERPRISE_DATA
├── RAW
├── STAGING
├── CURATED
├── MARTS
├── GOVERNED
└── GOVERNANCE
```

Warehouses: `EDP_INGEST_WH`, `EDP_BI_WH`.

Roles: `EDP_ENGINEER`, `EDP_MARKETING`, `EDP_SALES`, `EDP_SUPPORT`, `EDP_FINANCE`, `EDP_DELIVERY`.

## Run the FastAPI dashboards

```bash
set -a; source .env; set +a
./scripts/run_api.sh
```

Open `http://<EC2_PUBLIC_IP>:8501/`.

Team routes:

- `/marketing`
- `/sales`
- `/support`
- `/finance`
- `/delivery`

Health checks:

- `/health`
- `/api/snowflake/health`

## Data contract

The browser never queries raw Snowflake tables. It reads only department-specific secure views:

```text
MARTS.MART_MARKETING_DAILY → GOVERNED.V_MARKETING_DASHBOARD
MARTS.MART_SALES_DAILY     → GOVERNED.V_SALES_DASHBOARD
MARTS.MART_SUPPORT_DAILY   → GOVERNED.V_SUPPORT_DASHBOARD
MARTS.MART_FINANCE_DAILY   → GOVERNED.V_FINANCE_DASHBOARD
MARTS.MART_DELIVERY_DAILY  → GOVERNED.V_DELIVERY_DASHBOARD
```

PII such as email and phone is masked by Snowflake policies outside the engineering role.

## Dashboard UX

Each page distinguishes three classes of information:

1. **Live operational simulation** — SSE updates every second, 1.6M+ logical events/sec, latency/freshness/quality.
2. **Governed enterprise KPIs** — queried from Snowflake `GOVERNED.V_*_DASHBOARD` secure views.
3. **2026 consumer-study evidence** — strategic market context, never presented as live operational data.

The UI uses Apache ECharts and includes KPI cards, live time-series, ranking bars, 100% stacked powertrain mix, radar, donut, funnel and heatmap views.

## Tests

```bash
source .venv/bin/activate
PYTHONPATH=. pytest -q
```

## Production hardening

For an external deployment, put Nginx or an AWS ALB + TLS in front of FastAPI, restrict port 8501, use AWS Secrets Manager/SSM, prefer Snowflake key-pair/OAuth authentication over long-lived passwords, and run Uvicorn under systemd or a container runtime.
