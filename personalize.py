def personalize_allocation(base_alloc: dict, user_profile, current_year: int) -> dict:
    """
    Adjusts base TSP allocation based on user profile and market context.
    Includes risk tolerance scaling and optional glidepath toward retirement.
    """
    # Normalize risk tolerance input
    risk_levels = {
        "aggressive": 1.2,
        "moderate": 1.0,
        "conservative": 0.5
    }
    risk_input = user_profile.risk_tolerance.lower()
    risk_multiplier = risk_levels.get(risk_input, 1.0)  # fallback to moderate

    # Calculate years until retirement
    years_left = max(user_profile.retirement_year - current_year, 0)
    glide_factor = max(1 - (years_left / 40), 0.3)  # Don't go below 30% risk profile

    personalized = {}
    for fund, weight in base_alloc.items():
        adjusted = weight * risk_multiplier * glide_factor
        personalized[fund] = round(adjusted, 2)

    # Rebalance to total 100%
    total = sum(personalized.values())
    if total > 0:
        for fund in personalized:
            personalized[fund] = round(personalized[fund] * 100 / total, 2)

    return personalized
