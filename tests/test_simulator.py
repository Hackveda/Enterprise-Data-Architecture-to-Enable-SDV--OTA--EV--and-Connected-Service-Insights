from src.simulator.live_simulator import EventSimulator

def test_minimum_rate_and_counts():
    s=EventSimulator(1_600_000)
    x=s.logical_tick(1)
    assert x['events_this_tick']==1_600_000
    assert sum(x[k] for k in ['page_view','search','add_to_cart','order_created','payment_authorized','shipment_update','support_contact'])==1_600_000
