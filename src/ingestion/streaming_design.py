"""Production Snowpipe Streaming topology calculator.
This file deliberately does not fake a 1.6M-row/s connection from one client.
Use measured bytes/event and channel benchmarks to size producer count.
"""
from math import ceil

def plan(target_rps=1_600_000, measured_rps_per_channel=50_000, safety_factor=.70):
    safe = max(1, int(measured_rps_per_channel * safety_factor))
    return {
        'target_rps': target_rps,
        'assumed_measured_rps_per_channel': measured_rps_per_channel,
        'safe_rps_per_channel': safe,
        'minimum_channels': ceil(target_rps / safe),
        'recommendation': 'Open long-lived deterministic channels and scale horizontally; benchmark on the target account.'
    }

if __name__ == '__main__': print(plan())
