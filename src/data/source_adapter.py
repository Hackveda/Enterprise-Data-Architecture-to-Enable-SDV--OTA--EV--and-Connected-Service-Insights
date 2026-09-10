"""Adapt the supplied sheet to the platform without losing unknown columns.

The project cannot assume a fixed public-sheet schema. This adapter:
- standardizes column names
- detects common customer/order/product fields
- stores every source row as JSON-compatible payload
- derives a stable source_row_id for audit/lineage
"""
from __future__ import annotations
import hashlib, json, re
import pandas as pd

ALIASES = {
    'customer_id': {'customer_id','customerid','cust_id','user_id','userid'},
    'order_id': {'order_id','orderid','transaction_id','transactionid','invoice_id'},
    'product_id': {'product_id','productid','sku','item_id','itemid'},
    'amount': {'amount','sales','revenue','order_value','total_amount','price'},
    'event_ts': {'event_ts','timestamp','order_date','date','created_at','datetime'},
    'email': {'email','email_id','emailid'},
    'city': {'city','location','customer_city'},
}

def clean(name: str) -> str:
    s=re.sub(r'[^0-9a-zA-Z]+','_',str(name).strip().lower()).strip('_')
    return s or 'unnamed'

def adapt(df: pd.DataFrame) -> pd.DataFrame:
    x=df.copy(); x.columns=[clean(c) for c in x.columns]
    detected={}
    cols=set(x.columns)
    for canonical, aliases in ALIASES.items():
        hit=next((c for c in aliases if c in cols),None)
        if hit: detected[canonical]=hit
    rows=[]
    for rec in x.where(pd.notna(x), None).to_dict('records'):
        raw=json.dumps(rec, sort_keys=True, default=str, ensure_ascii=False)
        out={'source_row_id': hashlib.sha256(raw.encode()).hexdigest(), 'source_payload': raw}
        for canonical, actual in detected.items(): out[canonical]=rec.get(actual)
        rows.append(out)
    return pd.DataFrame(rows)
