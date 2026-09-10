"""Download and profile the supplied Google Sheet.
The sheet stays the system-of-record seed; unknown columns are preserved in JSON.
"""
from __future__ import annotations
import json
from pathlib import Path
import pandas as pd
import requests
from src.config import settings

OUT = Path('data/source')
OUT.mkdir(parents=True, exist_ok=True)

def download_sheet(sheet_id: str = settings.google_sheet_id, gid: str = '0') -> pd.DataFrame:
    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}'
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    target = OUT / 'source.csv'
    target.write_bytes(r.content)
    df = pd.read_csv(target)
    return df

def profile(df: pd.DataFrame) -> dict:
    return {
        'rows': int(len(df)),
        'columns': [str(c) for c in df.columns],
        'dtypes': {str(c): str(t) for c, t in df.dtypes.items()},
        'null_pct': {str(c): round(float(df[c].isna().mean()*100), 2) for c in df.columns},
        'unique': {str(c): int(df[c].nunique(dropna=True)) for c in df.columns},
    }

if __name__ == '__main__':
    df = download_sheet()
    p = profile(df)
    (OUT / 'profile.json').write_text(json.dumps(p, indent=2))
    print(json.dumps(p, indent=2))
