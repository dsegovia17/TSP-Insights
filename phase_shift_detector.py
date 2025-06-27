def detect_phase_shift(regime_history, coherence_history, velocity, macro_scores, fund_trend_score):
    """
    Detects if a macro regime phase shift is occurring by analyzing regime conviction,
    coherence breakdown, narrative volatility, and macro/fund divergence.

    Returns:
        - phase_shift_flag: bool
        - diagnostics: dict with breakdown of drivers
    """

    # Extract coherence float values safely
    coherence_values = [
        float(entry.get("value", entry)) if isinstance(entry, dict) else float(entry)
        for entry in coherence_history
    ]
    drop = coherence_values[-2] - coherence_values[-1] if len(coherence_values) >= 2 else 0.0

    # 1. Regime Drift
    regime_drift = False
    if len(regime_history) >= 3:
        top_probs = [max(d.values()) for d in regime_history[-3:]]
        regime_drift = (top_probs[0] - top_probs[-1]) > 0.15

    # 2. Coherence Drop
    coherence_collapse = drop > 0.3

    # 3. Velocity Spike
    velocity_spike = velocity > 0.6

    # 4. Macro vs Trend
    macro_momentum = macro_scores[-1] - macro_scores[-2] if len(macro_scores) >= 2 else 0.0
    macro_trend_divergence = macro_scores[-1] < macro_scores[-2] and fund_trend_score > 0

    # Diagnostic breakdown
    reasons = []
    if regime_drift: reasons.append("Regime confidence fading")
    if coherence_collapse: reasons.append("Coherence breakdown")
    if velocity_spike: reasons.append("Narrative velocity spike")
    if macro_trend_divergence: reasons.append("Macro softening vs trend resilience")

    phase_shift_flag = any([regime_drift, coherence_collapse, velocity_spike, macro_trend_divergence])

    diagnostics = {
        "phase_shift": phase_shift_flag,
        "coherence_drop": round(drop, 4),
        "velocity": velocity,
        "macro_momentum": round(macro_momentum, 4),
        "fund_trend_score": round(fund_trend_score, 4),
        "narrative": " | ".join(reasons) if reasons else "No early instability detected."
    }

    return phase_shift_flag, diagnostics
