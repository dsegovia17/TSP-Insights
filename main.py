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
from report_generator import generate_report
from log_writer import save_logs

import datetime
import json
import os

def load_json(path, default=[]):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)[-12:]
    return default

# === 🧑‍💼 User Setup ===
user = UserProfile(name="David", age=41, retirement_year=2049, risk_tolerance="Moderate")
CURRENT_YEAR = datetime.datetime.now().year

# === 🧠 Macro Intelligence ===
pillars = get_macro_pillars()
macro_score = sum(pillars.values())
regime_result = classify_regime(pillars)
stability = regime_result["stability"]

# === 🧪 Quantum Overlays ===
coherence = score_coherence(pillars)
velocity = score_velocity(load_json("logs/regime_log.json"))
fragility_flag, flow_notes = detect_fragility()

# === 📊 Fund Trend Score (SPY, IWM)
try:
    fund_trend_score = score_fund("SPY") + score_fund("IWM")
except Exception as e:
    print(f"⚠️ Fund trend error: {e}")
    fund_trend_score = 0

# === 📈 Load and unpack macro score log safely
macro_score_log_raw = load_json("logs/macro_score_log.json", default=[])
macro_score_log = [
    entry["value"] if isinstance(entry["value"], (int, float))
    else entry["value"].get("TotalScore", 0)
    for entry in macro_score_log_raw
]
macro_score_log.append(macro_score)

# === ⚠️ Phase Instability Detector ===
phase_shift_flag, phase_note = detect_phase_shift(
    regime_history=load_json("logs/regime_log.json"),
    coherence_history=load_json("logs/coherence_log.json", default=[coherence]),
    velocity=velocity,
    macro_scores=macro_score_log,
    fund_trend_score=fund_trend_score
)

# === 🧭 Risk Engine ===
base_risk = 0.7
risk_weight = modulate_risk_weight(
    base_risk=base_risk,
    stability=stability,
    coherence=coherence,
    velocity=velocity,
    fragility_flag=fragility_flag
)

# === 💼 Base Allocation
base_allocation = {"C": 40, "S": 15, "I": 5, "F": 10, "G": 30}

# === 🎯 Personalized Allocation ===
personalized_alloc = personalize_allocation(base_allocation, user, CURRENT_YEAR)

# === 📋 Final Report ===
generate_report(
    user=user,
    regime_probs=regime_result["probabilities"],
    stability=stability,
    coherence=coherence,
    velocity=velocity,
    fragility_flag=fragility_flag,
    phase_shift_flag=phase_shift_flag,
    flow_notes=flow_notes,
    macro_score=macro_score,
    risk_weight=risk_weight,
    personalized_alloc=personalized_alloc
)

# === 🧾 Save Logs with Scalar Score ===
save_logs(
    user=user,
    macro_pillars={"TotalScore": macro_score},  # now safely logged
    regime=regime_result,
    coherence=coherence,
    velocity=velocity,
    risk_weight=risk_weight,
    allocation=personalized_alloc
)
