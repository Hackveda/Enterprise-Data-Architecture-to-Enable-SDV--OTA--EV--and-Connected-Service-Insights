from __future__ import annotations
from pathlib import Path
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from faker import Faker

OUT = Path('data/generated')
OUT.mkdir(parents=True, exist_ok=True)
SEED = 42
rng = np.random.default_rng(SEED)
fake = Faker('en_IN'); Faker.seed(SEED)

def build(n_customers=10000, n_products=2000, n_campaigns=100, n_tickets=15000):
    customer_ids = np.arange(1, n_customers+1)
    customers = pd.DataFrame({
        'customer_id': customer_ids,
        'full_name': [fake.name() for _ in customer_ids],
        'email': [fake.email() for _ in customer_ids],
        'phone': [fake.msisdn()[:10] for _ in customer_ids],
        'city': rng.choice(['Delhi','Mumbai','Bengaluru','Hyderabad','Chennai','Pune','Kolkata','Jaipur'], n_customers),
        'segment': rng.choice(['VALUE','GROWTH','PREMIUM','NEW'], n_customers, p=[.35,.3,.15,.2]),
        'created_at': pd.Timestamp('2024-01-01') + pd.to_timedelta(rng.integers(0, 900, n_customers), unit='D')
    })
    products = pd.DataFrame({
        'product_id': np.arange(1, n_products+1),
        'category': rng.choice(['Electronics','Fashion','Grocery','Home','Beauty','Sports'], n_products),
        'brand': [f'Brand-{x:03d}' for x in rng.integers(1,120,n_products)],
        'list_price': np.round(rng.lognormal(6.0, .8, n_products),2),
        'cost_price': np.nan,
    })
    products['cost_price'] = np.round(products['list_price'] * rng.uniform(.45,.8,n_products),2)
    campaigns = pd.DataFrame({
        'campaign_id': np.arange(1,n_campaigns+1),
        'channel': rng.choice(['SEARCH','SOCIAL','EMAIL','AFFILIATE','DISPLAY'], n_campaigns),
        'campaign_name': [f'CAMP-{i:04d}' for i in range(1,n_campaigns+1)],
        'start_date': pd.Timestamp('2026-01-01') + pd.to_timedelta(rng.integers(0,240,n_campaigns),unit='D'),
        'daily_budget': np.round(rng.uniform(5000,250000,n_campaigns),2)
    })
    tickets = pd.DataFrame({
        'ticket_id': np.arange(1,n_tickets+1),
        'customer_id': rng.choice(customer_ids,n_tickets),
        'reason': rng.choice(['DELIVERY','REFUND','PAYMENT','PRODUCT','ACCOUNT'],n_tickets),
        'priority': rng.choice(['LOW','MEDIUM','HIGH','CRITICAL'],n_tickets,p=[.35,.4,.2,.05]),
        'opened_at': pd.Timestamp('2026-08-01') + pd.to_timedelta(rng.integers(0,40*24*60,n_tickets), unit='m'),
        'status': rng.choice(['OPEN','PENDING','RESOLVED'],n_tickets,p=[.15,.15,.7])
    })
    tickets['first_response_minutes'] = rng.gamma(2.0, 12.0, n_tickets).round(1)
    tickets['resolution_minutes'] = (tickets['first_response_minutes'] + rng.gamma(3.0, 80.0,n_tickets)).round(1)
    for name, df in [('customers',customers),('products',products),('campaigns',campaigns),('support_tickets',tickets)]:
        try:
            df.to_parquet(OUT/f'{name}.parquet', index=False)
        except ImportError:
            df.to_csv(OUT/f'{name}.csv', index=False)
        df.head(500).to_csv(OUT/f'{name}_sample.csv', index=False)
    return customers, products, campaigns, tickets

if __name__ == '__main__':
    build()
    print(f'Generated reference datasets under {OUT}')
