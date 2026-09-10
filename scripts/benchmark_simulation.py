import time
from src.simulator.live_simulator import EventSimulator

s=EventSimulator()
for rows in [100_000, 250_000, 500_000, 1_000_000]:
    t=time.perf_counter(); df=s.generate_microbatch(rows); elapsed=time.perf_counter()-t
    print(f'{rows:,} rows generated in {elapsed:.3f}s = {rows/elapsed:,.0f} physical rows/s; memory={df.memory_usage(deep=True).sum()/1e6:.1f} MB')
print('Logical live simulation:', s.logical_tick())
