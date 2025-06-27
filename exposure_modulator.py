def modulate_risk_weight(
    base_risk: float,
    stability: float,
    coherence: float,
    velocity: float,
    fragility_flag: bool
) -> float:
    """
    Adjusts risk weight based on macro integrity and market structure signals
    """

    # Apply stability and coherence penalties
    if stability < 0.3:
        base_risk *= 0.85
    if coherence < 0.4:
        base_risk *= 0.85
    if velocity > 0.6:
        base_risk *= 0.8
    if fragility_flag:
        base_risk *= 0.75

    # Bound between 0.1 and 1.0
    return round(min(max(base_risk, 0.1), 1.0), 2)
