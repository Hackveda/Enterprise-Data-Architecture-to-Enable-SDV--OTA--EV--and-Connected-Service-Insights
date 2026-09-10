select to_date(order_ts) snapshot_date, market, channel, powertrain,
       count(*) orders, count_if(status='WON') won_orders, avg(net_price) avg_selling_price,
       sum(net_price) booked_revenue, avg(discount/list_price) discount_rate
from {{ ref('stg_sales_orders') }} group by 1,2,3,4
