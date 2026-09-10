with c as (select * from {{ ref('stg_campaign_events') }})
select to_date(event_ts) snapshot_date, market, channel,
       count_if(action='IMPRESSION') impressions, count_if(action='CLICK') clicks,
       count_if(action='LEAD') leads, count_if(action='ORDER') attributed_orders,
       sum(cost) spend, sum(attributed_revenue) attributed_revenue,
       div0(sum(attributed_revenue),nullif(sum(cost),0)) roas
from c group by 1,2,3
