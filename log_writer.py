import os
import json
from datetime import datetime

LOG_DIR = "logs"
MAX_ENTRIES = 12  # keep last 12 runs per log

os.makedirs(LOG_DIR, exist_ok=True)

def append_log(file_name: str, new_data: dict | float | int):
    path = os.path.join(LOG_DIR, file_name)

    # Load old log if it exists
    if os.path.exists(path):
        with open(path, "r") as f:
            history = json.load(f)
    else:
        history = []

    # Add new entry with timestamp
    entry = {
        "timestamp": datetime.now().isoformat(),
        "value": new_data
    }
    history.append(entry)
    history = history[-MAX_ENTRIES:]  # keep only last N

    # Write back to file
    with open(path, "w") as f:
        json.dump(history, f, indent=2)

def save_logs(
    user,
    macro_pillars: dict,
    regime: dict,
    coherence: float,
    velocity: float,
    risk_weight: float,
    allocation: dict
):
    append_log("macro_score_log.json", sum(macro_pillars.values()))
    append_log("coherence_log.json", coherence)
    append_log("velocity_log.json", velocity)
    append_log("risk_weight_log.json", round(risk_weight, 4))
    append_log("regime_log.json", regime["probabilities"])
    append_log("allocation_log.json", allocation)
