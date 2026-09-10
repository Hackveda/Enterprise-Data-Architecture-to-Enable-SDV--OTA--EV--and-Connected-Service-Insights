from __future__ import annotations

import math
import random
from datetime import datetime, timezone

from app.config import get_settings

TEAMS = ("marketing", "sales", "support", "finance", "delivery")


def live_snapshot(team: str, tick: int) -> dict:
    s = get_settings()
    rng = random.Random(10_000 + tick + hash(team) % 997)
    wave = math.sin(tick / 3.2)
    base = s.simulated_rps
    rate = int(base * (1 + 0.08 * wave + rng.uniform(-0.025, 0.025)))
    common = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "simulated_rps": max(rate, 1_600_000),
        "pipeline_latency_ms": round(max(85, 180 + 35 * wave + rng.uniform(-20, 20)), 1),
        "data_freshness_sec": round(max(3, 22 + 5 * wave + rng.uniform(-3, 3)), 1),
        "quality_score": round(min(100, max(96, 99.3 + rng.uniform(-0.8, 0.5))), 2),
    }
    metrics = {
        "marketing": {"active_sessions": rng.randint(33_000, 52_000), "campaign_roas": round(4.1 + rng.uniform(-0.4, 0.6), 2), "lead_conversion_pct": round(8.8 + rng.uniform(-1.1, 1.0), 2), "switcher_index": rng.randint(66, 74)},
        "sales": {"open_opportunities": rng.randint(16_500, 19_500), "test_drives_today": rng.randint(4_300, 5_400), "win_rate_pct": round(31 + rng.uniform(-2.5, 2.5), 1), "digital_to_dealer_pct": round(42 + rng.uniform(-3, 4), 1)},
        "support": {"open_cases": rng.randint(4_700, 5_900), "sla_at_risk": rng.randint(110, 210), "first_contact_resolution_pct": round(83 + rng.uniform(-2, 2), 1), "ota_incidents": rng.randint(18, 46)},
        "finance": {"gross_revenue_m": round(486 + rng.uniform(-7, 12), 1), "software_arr_m": round(41 + rng.uniform(-1.8, 2.6), 1), "gross_margin_pct": round(24.7 + rng.uniform(-1, 1), 1), "warranty_cost_m": round(8.4 + rng.uniform(-0.6, 0.9), 1)},
        "delivery": {"connected_vehicles_m": round(4.8 + rng.uniform(-0.05, 0.07), 2), "ota_success_pct": round(98.1 + rng.uniform(-0.7, 0.6), 2), "rollbacks": rng.randint(45, 92), "critical_vehicle_alerts": rng.randint(70, 140)},
    }[team]
    return {**common, **metrics}
