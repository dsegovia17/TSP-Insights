def detect_phase_shift(regime_history, coherence_history, velocity, macro_scores, fund_trend_score):
    """
    Triggers a phase shift flag when coherence, macro tone, or fund strength diverge.
    """

    def extract_numeric(value):
        if isinstance(value, (int, float)):
            return value
        elif isinstance(value, dict):
            for key in ["score", "value", "TotalScore"]:
                if key in value and isinstance(value[key], (int, float)):
                    return value[key]
        return 0  # fallback

    try:
        phase_shift = False
        note = ""

        # Expansion regime confidence drop
        if len(regime_history) >= 2:
            latest_probs = regime_history[-1].get("value", {})
            prev_probs = regime_history[-2].get("value", {})
            if latest_probs.get("Expansion", 0) < prev_probs.get("Expansion", 0) - 0.2:
                phase_shift = True
                note = "Expansion confidence dropped > 20%"

        # Coherence breakdown
        if len(coherence_history) >= 2:
            if coherence_history[-1] < 0.3 and coherence_history[-2] > 0.5:
                phase_shift = True
                note = "Coherence breakdown detected"

        # Macro trend deterioration despite fund strength
        if len(macro_scores) >= 2:
            score_now = extract_numeric(macro_scores[-1])
            score_prev = extract_numeric(macro_scores[-2])
            if score_now < score_prev and fund_trend_score > 0:
                phase_shift = True
                note = "Macro score dropped despite bullish fund trend"

        # Narrative momentum stalled
        if velocity < 0.05:
            phase_shift = True
            note = "Narrative velocity is stalled"

        return phase_shift, note or "No major shift detected"

    except Exception as e:
        print(f"⚠️ Phase shift detection error: {e}")
        return False, "Phase shift check failed"
