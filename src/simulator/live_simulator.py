"""High-rate event simulator.

Two modes:
1) logical_tick(): represents >=1.6M events/sec without materialising every row;
   ideal for live UI / architecture demos.
2) generate_microbatch(): materialises a configurable sample for correctness and
   throughput tests. Scale-out producers should be used for real 1.6M row/s tests.
"""
from __future__ import annotations
from datetime import datetime, timezone
import numpy as np
import pandas as pd
from src.config import settings

EVENTS = np.array(['page_view','search','add_to_cart','order_created','payment_authorized','shipment_update','support_contact'])
WEIGHTS = np.array([.48,.18,.12,.08,.06,.05,.03])

class EventSimulator:
    def __init__(self, rps: int = settings.simulated_rps, seed: int = 42):
        if rps < 1_600_000:
            raise ValueError('Project requires simulated_rps >= 1,600,000')
        self.rps = rps
        self.rng = np.random.default_rng(seed)
        self.total = 0

    def logical_tick(self, seconds: float = 1.0) -> dict:
        n = int(self.rps * seconds)
        counts = self.rng.multinomial(n, WEIGHTS)
        self.total += n
        gross_orders = int(counts[3])
        avg_order_value = float(self.rng.normal(1850, 130))
        return {
            'ts': datetime.now(timezone.utc),
            'rps': self.rps,
            'events_this_tick': n,
            'total_events': self.total,
            **{EVENTS[i]: int(counts[i]) for i in range(len(EVENTS))},
            'gross_revenue': round(gross_orders * avg_order_value, 2),
            'payment_success_rate': round(float(self.rng.normal(.973,.003))*100, 2),
            'p95_event_latency_ms': round(max(10,float(self.rng.normal(95,18))),1),
        }

    def generate_microbatch(self, rows: int = settings.physical_batch_rows) -> pd.DataFrame:
        now = pd.Timestamp.now(tz='UTC')
        event_type = self.rng.choice(EVENTS, rows, p=WEIGHTS)
        customer_id = self.rng.integers(1, 10001, rows)
        product_id = self.rng.integers(1, 2001, rows)
        amount = np.where(np.isin(event_type,['order_created','payment_authorized']), self.rng.lognormal(7.25,.55,rows), 0)
        return pd.DataFrame({
            'event_id': [f'{now.value:x}-{i:x}' for i in range(rows)],
            'event_ts': now - pd.to_timedelta(self.rng.integers(0,1000,rows), unit='ms'),
            'event_type': event_type,
            'customer_id': customer_id,
            'session_id': self.rng.integers(1, 5_000_000, rows),
            'product_id': product_id,
            'campaign_id': self.rng.integers(1,101,rows),
            'amount': np.round(amount,2),
            'channel': self.rng.choice(['WEB','APP','API'], rows, p=[.55,.4,.05]),
            'region': self.rng.choice(['NORTH','SOUTH','EAST','WEST'],rows),
        })

if __name__ == '__main__':
    s = EventSimulator()
    print(s.logical_tick())
    print(s.generate_microbatch(5).to_string(index=False))
