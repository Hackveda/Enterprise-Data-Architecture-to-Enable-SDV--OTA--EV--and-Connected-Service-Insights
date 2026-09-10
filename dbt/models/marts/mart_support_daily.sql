select to_date(created_ts) snapshot_date, market, category, severity,
       count(*) tickets, count_if(closed_ts is null) open_tickets,
       count_if(datediff('minute',created_ts,coalesce(closed_ts,current_timestamp())) > sla_minutes) sla_breaches,
       avg(iff(first_contact_resolved,1,0))*100 first_contact_resolution_pct, avg(csat) avg_csat
from {{ ref('stg_support_tickets') }} group by 1,2,3,4
