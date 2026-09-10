select event_id, event_ts, upper(vin) as vin, customer_id, market, lower(event_type) as event_type,
       software_version, battery_soc, battery_health, odometer_km, latitude, longitude, speed_kph,
       dtc_code, ota_campaign_id, payload, ingested_at
from {{ source('raw','vehicle_events') }}
qualify row_number() over (partition by event_id order by ingested_at desc)=1
