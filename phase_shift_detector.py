def detect_phase_shift(
    regime_history: list[dict],
    coherence_history: list[float],
    velocity: float,
    macro_scores: list[int],
    fund_trend_score: int
) -> tuple[bool, str]:
    """
    Detects pre-breakdown macro regime fragility.
    Returns:
        - shift_detected: bool
        - message: str narrative summary
    """

    reasons = []
    shift_detected = False

    # 1. Regime Drift (falling conviction)
    if len(regime_history) >= 3:
        top_probs = [max(d.values()) for d in regime_history[-3:]]
        if top_probs[0] - top_probs[-1] > 0.15:
            reasons.append("Top regime confidence is fading")
            shift_detected = True

    # 2. Coherence Collapse
    if len(coherence_history) >= 2:
        drop = coherence_history[-2] - coherence_history[-1]
        if drop > 0.3:
            reasons.append("Macro coherence breaking down")
            shift_detected = True

    # 3. Velocity Spike
    if velocity > 0.6:
        reasons.append("Narrative velocity has spiked")
        shift_detected = True

    # 4. Macro Divergence from Trend
    if len(macro_scores) >= 2:
        if macro_scores[-1] < macro_scores[-2] and fund_trend_score > 0:
            reasons.append("Macro softening while trend remains firm")
            shift_detected = True

    message = " | ".join(reasons) if shift_detected else "No early instability detected."

    return shift_detected, message
