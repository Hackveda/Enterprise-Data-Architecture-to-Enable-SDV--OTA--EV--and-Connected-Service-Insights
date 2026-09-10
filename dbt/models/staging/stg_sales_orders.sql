select * from {{ source('raw','sales_orders') }}
qualify row_number() over (partition by order_id order by ingested_at desc)=1
