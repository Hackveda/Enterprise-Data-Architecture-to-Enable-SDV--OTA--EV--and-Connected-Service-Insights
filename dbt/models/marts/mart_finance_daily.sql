select to_date(txn_ts) snapshot_date, market, txn_type,
       sum(revenue) revenue, sum(cost) cost, sum(revenue-cost) contribution_margin,
       div0(sum(revenue-cost),nullif(sum(revenue),0))*100 contribution_margin_pct
from {{ ref('stg_financial_transactions') }} group by 1,2,3
