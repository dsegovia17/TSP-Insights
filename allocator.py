from macro_signals import safe_pull
from fund_trends import score_fund

def recommend_allocation(macro_score, fund_scores):
    """
    Generates allocation weights for TSP funds based on macro regime score and fund trend strength.
    """

    # Determine risk budget based on macro regime score
    if macro_score >= 6:
        risk_weight = 0.9
    elif macro_score >= 4:
        risk_weight = 0.7
    elif macro_score >= 1:
        risk_weight = 0.5
    elif macro_score >= -2:
        risk_weight = 0.3
    else:
        risk_weight = 0.1

    # Allocate among positive-trending funds
    allocation = {"C": 0, "S": 0, "I": 0, "F": 0, "G": 0}
    total_positive = sum(max(score, 0) for score in fund_scores.values())
    total_positive = total_positive if total_positive != 0 else 1  # prevent divide by zero

    for fund in ["C", "S", "I", "F"]:
        if fund_scores[fund] > 0:
            pct = (fund_scores[fund] / total_positive) * (risk_weight * 100)
            allocation[fund] = round(pct)

    # Assign remainder to G Fund
    used = sum(allocation.values())
    allocation["G"] = 100 - used

    return allocation
