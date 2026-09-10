select date_trunc('day', event_ts) as day, campaign_id,
       count_if(event_type='PAGE_VIEW') as impressions,
       count_if(event_type='ADD_TO_CART') as adds_to_cart,
       count_if(event_type='ORDER_CREATED') as conversions,
       sum(iff(event_type='ORDER_CREATED',amount,0)) as attributed_revenue
from {{ ref('stg_events') }}
group by 1,2
