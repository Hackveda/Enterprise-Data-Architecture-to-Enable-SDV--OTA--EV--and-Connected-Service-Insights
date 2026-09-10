select * from {{ source('raw','financial_transactions') }}
qualify row_number() over (partition by txn_id order by ingested_at desc)=1
