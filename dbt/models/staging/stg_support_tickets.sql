select * from {{ source('raw','support_tickets') }}
qualify row_number() over (partition by ticket_id order by ingested_at desc)=1
