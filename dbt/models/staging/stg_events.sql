select
  event_id, event_ts, upper(trim(event_type)) as event_type,
  customer_id, session_id, product_id, campaign_id,
  coalesce(amount,0) as amount, upper(channel) as channel, upper(region) as region
from {{ source('raw','events') }}
where event_id is not null and event_ts is not null
