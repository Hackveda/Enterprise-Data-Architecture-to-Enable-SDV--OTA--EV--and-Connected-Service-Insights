with c as (select * from {{ ref('stg_customers') }}),
orders as (select customer_id, count(*) orders, sum(net_price) lifetime_sales from {{ ref('stg_sales_orders') }} group by 1),
support as (select customer_id, count(*) tickets, avg(csat) avg_csat from {{ ref('stg_support_tickets') }} group by 1)
select c.*, coalesce(o.orders,0) as orders, coalesce(o.lifetime_sales,0) as lifetime_sales,
       coalesce(s.tickets,0) as support_tickets, s.avg_csat,
       iff(c.current_brand <> c.next_brand, true, false) as switch_intent
from c left join orders o using(customer_id) left join support s using(customer_id)
