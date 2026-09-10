STUDY = {
    "engine_preference": {
        "China": {"ICE": 41, "HEV": 19, "PHEV": 17, "BEV": 20}, "Germany": {"ICE": 49, "HEV": 14, "PHEV": 10, "BEV": 16},
        "India": {"ICE": 50, "HEV": 25, "PHEV": 10, "BEV": 10}, "Japan": {"ICE": 41, "HEV": 37, "PHEV": 6, "BEV": 1},
        "South Korea": {"ICE": 44, "HEV": 27, "PHEV": 11, "BEV": 11}, "Southeast Asia": {"ICE": 53, "HEV": 18, "PHEV": 14, "BEV": 10},
        "UK": {"ICE": 41, "HEV": 27, "PHEV": 10, "BEV": 11}, "US": {"ICE": 61, "HEV": 21, "PHEV": 5, "BEV": 7}},
    "brand_switching": {"China": 72, "India": 70, "Southeast Asia": 67, "UK": 58, "South Korea": 55, "US": 53, "Germany": 44, "Japan": 41},
    "sdv_useful": {"India": 81, "Southeast Asia": 71, "China": 68, "South Korea": 57, "US": 41, "UK": 38, "Japan": 33, "Germany": 33},
    "local_voice": {"China": 80, "India": 80, "Japan": 70, "South Korea": 65, "Southeast Asia": 64, "US": 43, "UK": 37, "Germany": 31},
    "connected_wtp_india": {"Emergency assistance": 85, "Anti-theft tracking": 84, "Vehicle/pedestrian detection": 79, "Vehicle health + cost forecast": 79, "App connectivity": 78, "Warranty/recall notices": 78},
    "privacy_concern_india": {"Synced device data": 73, "Vehicle location": 72, "In-cabin camera": 72, "Biometric data": 70, "Connected-service usage": 70, "Driving behavior": 66},
    "brand_choice_india": {"Product quality": 58, "Vehicle performance": 57, "Features / technology": 50, "Ownership experience": 46, "Price": 44, "Service network": 43, "Brand familiarity": 41},
    "research_sources_india": {"Social / influencer": 59, "Manufacturer website": 54, "Online media / auto portals": 50, "Dealer visit": 46, "Dealer website": 41, "Word of mouth": 40},
    "purchase_experience_india": {"Good deal": 40, "Physical test drive": 40, "Transparent pricing": 35, "Questions answered": 26, "Virtual process": 26, "Financing / usage models": 27},
    "service_provider_india": {"Authorized dealer": 84, "Independent / aftermarket": 13, "DIY": 3},
    "service_priority_india": {"Transparency of pricing/work": 22, "Customer treatment": 12, "Speed of service": 12, "Cost / price": 10, "Explanation of work": 9, "Communication during service": 8},
    "ev_concerns_india": {"Public charging availability": 43, "Charging time": 41, "Battery safety": 38, "Driving range": 36, "Battery replacement cost": 34, "Cold weather performance": 34, "Price premium": 32},
}

TEAM_INSIGHTS = {
    "marketing": [
        {"title": "Win switchers, not just awareness", "detail": "India shows 70% intended brand switching; emphasize quality, performance and value in conquest audiences.", "action": "Shift acquisition budget toward high-intent switchers and proof-led creative."},
        {"title": "Digital research matters", "detail": "Social/influencer, manufacturer sites and auto portals are leading Indian research sources.", "action": "Build an attribution view from campaign exposure through configured vehicle and dealer appointment."},
        {"title": "Trust is a growth lever", "detail": "Connected-service willingness is high, but privacy concern is also high.", "action": "Make consent, purpose and retention messaging visible in campaign journeys."}],
    "sales": [
        {"title": "Value beats brand familiarity", "detail": "Product quality, performance and technology outrank easy financing and advertising in brand choice.", "action": "Prioritize vehicle proof points, transparent pricing and tailored test-drive offers."},
        {"title": "Hybrid bridge opportunity", "detail": "EV adoption remains constrained by charging and battery concerns.", "action": "Offer powertrain-fit recommendations instead of pushing BEV universally."},
        {"title": "High D2C openness in India", "detail": "India is among the markets most open to direct manufacturer purchase journeys.", "action": "Track online-to-dealer handoff and abandoned direct-purchase funnels."}],
    "support": [
        {"title": "Service quality and trust define loyalty", "detail": "Consumers prioritize quality of work, trust and clear explanations of price/work performed.", "action": "Expose first-contact resolution, repeat repair, explanation quality and SLA breach risk."},
        {"title": "Connected safety has high perceived value", "detail": "Emergency assistance and anti-theft features show strong willingness to pay.", "action": "Create proactive support playbooks around safety-feature activation and failures."},
        {"title": "Privacy requires explicit handling", "detail": "Location, synced-device and in-cabin data attract high concern.", "action": "Surface consent state and approved data purpose to agents; never expose raw PII by default."}],
    "finance": [
        {"title": "Affordability is central", "detail": "Fuel cost and total cost of ownership remain key electrification motivators, while purchase price is a major brand-choice factor.", "action": "Monitor contribution margin with TCO offers, incentives and financing mix."},
        {"title": "OTA can create software revenue", "detail": "India shows high SDV usefulness and willingness to pay for OTA capability.", "action": "Track attach rate, recurring software ARPU, deferred revenue and churn by feature bundle."},
        {"title": "Charging economics affect adoption", "detail": "Charging cost is considered important across markets.", "action": "Model charging partnerships and subsidy economics by market and cohort."}],
    "delivery": [
        {"title": "OTA becomes an operational product", "detail": "Consumers value feature, safety and performance improvements delivered during ownership.", "action": "Run release health by software version, VIN cohort, rollback rate and customer impact."},
        {"title": "SDV expectations vary by market", "detail": "India and China show much stronger SDV usefulness than Germany or Japan.", "action": "Prioritize rollout sequencing and localization by market appetite and support readiness."},
        {"title": "Local-language voice is table stakes in India", "detail": "80% of Indian respondents rate local-language voice support important.", "action": "Track language-model coverage, intent success, fallback rate and OTA adoption."}],
}


def team_payload(team: str) -> dict:
    return {"study": STUDY, "insights": TEAM_INSIGHTS[team]}
