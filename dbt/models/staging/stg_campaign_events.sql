select * from {{ source('raw','campaign_events') }}
qualify row_number() over (partition by event_id order by ingested_at desc)=1
