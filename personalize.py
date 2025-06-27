from user_profile import UserProfile

def personalize_allocation(base_alloc: dict, user: UserProfile, current_year: int) -> dict:
    """
    Adjusts base fund allocations based on user profile:
    - Time horizon to retirement
    - Risk tolerance
    Outputs final fund weights (C, S, I, F, G) tailored to the user.
    """

    # Step 1: Calculate equity exposure target
    years_to_retirement = user.years_to_retire(current_year)
    
    # Glidepath: maps years → equity exposure (min 30%, max 100%)
    glide_equity = min(1.0, max(0.3, years_to_retirement / 40))
    
    # Risk multiplier
    risk_multiplier = {
        "Aggressive": 1.0,
        "Moderate": 0.75,
        "Conservative": 0.5
    }[user.risk_tolerance]

    equity_target = round(glide_equity * risk_multiplier, 2)

    # Step 2: Scale equity allocations
    equity_funds = ["C", "S", "I"]
    equity_base = sum(base_alloc[f] for f in equity_funds)
    equity_scale = equity_target / (equity_base / 100) if equity_base else 0

    personalized = {}
    for fund in equity_funds:
        personalized[fund] = round(base_alloc[fund] * equity_scale)

    # Step 3: Adjust fixed income (F Fund) relative to remaining risk budget
    personalized["F"] = round(base_alloc["F"] * (1 - equity_target))

    # Step 4: Put remainder in G Fund
    used = sum(personalized.values())
    personalized["G"] = 100 - used

    # Clean up rounding overflow
    total = sum(personalized.values())
    if total != 100:
        diff = 100 - total
        personalized["G"] += diff  # absorb into G

    return personalized
