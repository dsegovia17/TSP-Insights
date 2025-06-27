def detect_phase_shift(regime_history, coherence_history, velocity, macro_scores, fund_trend_score):
    """
    Detects if a macro regime phase shift is occurring by analyzing coherence, macro scores,
    and volatility of narrative shifts.
    """

    # Safely extract coherence values
    coherence_values = [
        float(entry.get("value", entry)) if isinstance(entry, dict) else float(entry)
        for entry in coherence_history
    ]
    if len(coherence_values) >= 2:
        drop = coherence_values[-2] - coherence_values[-1]
    else:
        drop = 0.0

    # Compute macro momentum delta
    if len(macro_scores) >= 2:
        macro_momentum = macro_scores[-1] - macro_scores[-2]
    else:
        macro_momentum = 0.0

    # Logic for detecting phase shift
    sudden_drop = drop > 0.15
    volatile_narrative = velocity > 0.2
    poor_macro_momentum = macro_momentum < -1.5
    trend_conflict = fund_trend_score < 0

    phase_shift_flag = any([sudden_drop, volatile_narrative, poor_macro_momentum, trend_conflict])

    return phase_shift_flag, {
        "coherence_drop": round(drop, 4),
        "velocity": velocity,
        "macro_momentum": round(macro_momentum, 4),
        "fund_trend_score": round(fund_trend_score, 4),
    }
