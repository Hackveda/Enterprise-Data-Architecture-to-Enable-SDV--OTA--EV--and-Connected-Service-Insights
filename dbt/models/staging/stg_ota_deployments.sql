select * from {{ source('raw','ota_deployments') }}
qualify row_number() over (partition by deployment_id order by ingested_at desc)=1
