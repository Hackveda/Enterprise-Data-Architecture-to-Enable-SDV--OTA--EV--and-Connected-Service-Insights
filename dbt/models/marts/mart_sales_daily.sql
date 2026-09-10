select date_trunc('day', event_ts) as day, region,
       count_if(event_type='ORDER_CREATED') as orders,
       sum(iff(event_type='ORDER_CREATED',amount,0)) as gross_revenue
from {{ ref('stg_events') }}
group by 1,2
