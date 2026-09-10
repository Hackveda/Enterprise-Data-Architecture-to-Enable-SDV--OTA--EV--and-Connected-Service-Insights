with v as (select * from {{ source('raw','vehicles') }}),
e as (select vin, max(event_ts) last_event_ts, max_by(software_version,event_ts) software_version,
             max_by(battery_soc,event_ts) battery_soc, max_by(battery_health,event_ts) battery_health,
             count_if(dtc_code is not null) dtc_events
      from {{ ref('stg_vehicle_events') }} group by 1),
ota as (select vin, count(*) ota_attempts, count_if(status='SUCCESS') ota_successes, count_if(rollback) rollbacks from {{ ref('stg_ota_deployments') }} group by 1)
select v.*, e.last_event_ts, e.software_version current_software_version, e.battery_soc, e.battery_health, e.dtc_events,
       coalesce(ota.ota_attempts,0) ota_attempts, coalesce(ota.ota_successes,0) ota_successes, coalesce(ota.rollbacks,0) rollbacks
from v left join e using(vin) left join ota using(vin)
