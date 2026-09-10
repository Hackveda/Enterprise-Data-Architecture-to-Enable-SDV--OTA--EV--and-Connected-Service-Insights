select customer_id, market, city, age_band, income_band, current_brand, next_brand, preferred_powertrain,
       consent_marketing, consent_connected_data, email, phone, source_payload, ingested_at
from {{ source('raw','customers') }}
qualify row_number() over (partition by customer_id order by ingested_at desc)=1
