select
    to_date(start_ts) as snapshot_date,
    market,
    count(*) as ota_attempts,
    count_if(status = 'SUCCESS') as ota_success,
    div0(count_if(status = 'SUCCESS'), nullif(count(*), 0)) * 100 as ota_success_pct,
    count_if(rollback) as rollbacks,
    count(distinct vin) as vehicles_touched
from {{ ref('stg_ota_deployments') }}
group by 1, 2
