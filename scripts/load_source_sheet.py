from src.data.bootstrap_source import download_sheet, profile
from src.data.source_adapter import adapt
from src.ingestion.snowflake_batch import append_dataframe
import json

df=download_sheet()
print(json.dumps(profile(df),indent=2))
adapted=adapt(df)
adapted['source_payload']=adapted['source_payload'].map(json.loads)
print(append_dataframe(adapted,'SOURCE_SEED','RAW'))
