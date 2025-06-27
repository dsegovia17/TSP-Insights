def generate_allocation(profile, macro_score, sentiment_score):
    base_equity = max(100 - profile["age"], 40)
    risk_factor = profile["risk_tolerance"] / 5
    macro_adjust = (macro_score + sentiment_score) * 5

    equity_allocation = int(base_equity * risk_factor + macro_adjust)
    equity_allocation = max(min(equity_allocation, 90), 10)

    return {
        "C Fund": int(equity_allocation * 0.6),
        "S Fund": int(equity_allocation * 0.2),
        "I Fund": int(equity_allocation * 0.2),
        "G Fund": 100 - equity_allocation
    }
