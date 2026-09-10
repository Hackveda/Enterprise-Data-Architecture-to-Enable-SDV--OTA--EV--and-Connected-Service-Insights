from pathlib import Path
import pandas as pd
from src.ingestion.snowflake_batch import append_dataframe

BASE=Path("data/generated")
for stem, table in [("customers","CUSTOMERS"),("products","PRODUCTS"),("campaigns","CAMPAIGNS"),("support_tickets","SUPPORT_TICKETS")]:
    parquet=BASE/f"{stem}.parquet"
    csv=BASE/f"{stem}.csv"
    df=pd.read_parquet(parquet) if parquet.exists() else pd.read_csv(csv)
    print(table, append_dataframe(df,table,"RAW"))
