from fastapi import FastAPI
from pydantic import BaseModel
from user_profile import UserProfile
from macro_framework import get_macro_pillars
from regime_matrix import classify_regime
from coherence_score import score_coherence
from narrative_velocity import score_velocity
from flow_overlay import detect_fragility
from phase_shift_detector import detect_phase_shift
from exposure_modulator import modulate_risk_weight
from fund_trends import score_fund
from personalize import personalize_allocation

import datetime
import json
import os

app = FastAPI(title="TSP Allocator API", version="1.0")

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

class ProfileInput(BaseModel):
    name: str
    age: int
    retirement_year: int
    risk_tolerance: str  # 'Conservative', 'Moderate', 'Aggressive'

def load_json(path, default=[]):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)[-12:]
    return default

@app.post("/run")
def run_allocator(profile: ProfileInput):
    user = UserProfile(**profile.dict())
    CURRENT_YEAR = datetime.datetime.now().year

    # Macro signal
    pillars = get_macro_pillars()
    macro_score = sum(pillars.values())
    regime_result = classify_regime(pillars)
    stability = regime_result["stability"]

    # Coherence + fragility
    coherence = score_coherence(pillars)
    velocity = score_velocity(load_json("logs/regime_log.json"))
    fragility_flag, _ = detect_fragility()

    # Fund momentum
    try:
        fund_trend_score = score_fund("SPY") + score_fund("IWM")
    except:
        fund_trend_score = 0

    macro_score_log = [
        entry.get("value", {}).get("TotalScore", 0)
        if isinstance(entry.get("value"), dict)
        else entry.get("value")
        for entry in load_json("logs/macro_score_log.json")
    ]
    macro_score_log.append(macro_score)

    phase_shift_flag, _ = detect_phase_shift(
        regime_history=load_json("logs/regime_log.json"),
        coherence_history=load_json("logs/coherence_log.json", default=[coherence]),
        velocity=velocity,
        macro_scores=macro_score_log,
        fund_trend_score=fund_trend_score
    )

    # Risk-adjusted weight
    risk_weight = modulate_risk_weight(
        base_risk=0.7,
        stability=stability,
        coherence=coherence,
        velocity=velocity,
        fragility_flag=fragility_flag
    )

    base_alloc = {"C": 40, "S": 15, "I": 5, "F": 10, "G": 30}
    alloc = personalize_allocation(base_alloc, user, CURRENT_YEAR)

    summary = f"{max(regime_result['probabilities'], key=regime_result['probabilities'].get)} regime with coherence {round(coherence,2)} and risk weight {round(risk_weight,2)}"

    return {
        "regime": regime_result["probabilities"],
        "stability": stability,
        "coherence": coherence,
        "velocity": velocity,
        "risk_weight": round(risk_weight, 4),
        "fragility": fragility_flag,
        "phase_shift": phase_shift_flag,
        "allocation": alloc,
        "macro_score": round(macro_score, 3),
        "summary": summary
    }
