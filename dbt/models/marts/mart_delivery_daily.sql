select to_date(start_ts) snapshot_date, market,
       count(*) ota_attempts, count_if(status='SUCCESS') ota_success,
       div0(count_if(status='SUCCESS'),nullif(count(*),0))*100 ota_success_pct,
       count_if(rollback) rollbacks, count_distinct(vin) vehicles_touched
from {{ ref('stg_ota_deployments') }} group by 1,2
