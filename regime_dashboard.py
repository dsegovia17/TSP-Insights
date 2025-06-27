import json
import os
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd

LOG_DIR = "logs"

def load_log(file_name):
    path = os.path.join(LOG_DIR, file_name)
    if not os.path.exists(path):
        print(f"⚠️ {file_name} not found.")
        return []
    with open(path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print(f"⚠️ Failed to parse {file_name}.")
            return []

def extract_series(log, key=None):
    timestamps = []
    values = []
    for entry in log:
        try:
            timestamps.append(datetime.fromisoformat(entry["timestamp"]))
            val = entry["value"]
            if key and isinstance(val, dict):
                val = val.get(key, 0)
            values.append(val)
        except Exception:
            continue
    if not timestamps or not values:
        return pd.Series([], dtype=float)
    return pd.Series(values, index=pd.to_datetime(timestamps))

def plot_regime(regime_log):
    if not regime_log:
        print("⚠️ No regime history available.")
        return

    try:
        timestamps = [datetime.fromisoformat(e["timestamp"]) for e in regime_log]
        df = pd.DataFrame([e["value"] for e in regime_log], index=timestamps)
        numeric_cols = df.select_dtypes(include=["number"])
        if numeric_cols.empty:
            print("⚠️ Regime log contains no numeric values to plot.")
            return
        numeric_cols.plot(
            figsize=(12, 4),
            marker='o',
            linewidth=2,
            title="🧠 Regime Probabilities Over Time"
        )
        plt.ylabel("Confidence")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"⚠️ Error plotting regime probabilities: {e}")

def plot_scalar_metric(series, label):
    if series.empty:
        print(f"⚠️ No data for {label}")
        return
    series.plot(figsize=(12, 2), marker='o')
    plt.title(f"{label} Over Time")
    plt.ylabel(label)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_allocation(log):
    if not log:
        print("⚠️ No allocation history available.")
        return
    try:
        timestamps = [datetime.fromisoformat(e["timestamp"]) for e in log]
        df = pd.DataFrame([e["value"] for e in log], index=timestamps)
        df.plot(kind="bar", stacked=True, figsize=(12, 4), colormap="Set3")
        plt.title("📊 Personalized Allocation Over Time")
        plt.ylabel("Allocation (%)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"⚠️ Error plotting allocation: {e}")

if __name__ == "__main__":
    print("📡 Loading allocator logs...")

    plot_regime(load_log("regime_log.json"))
    plot_scalar_metric(extract_series(load_log("coherence_log.json")), "Coherence")
    plot_scalar_metric(extract_series(load_log("velocity_log.json")), "Narrative Velocity")
    plot_scalar_metric(extract_series(load_log("risk_weight_log.json")), "Risk Budget")
    plot_allocation(load_log("allocation_log.json"))

    print("✅ Dashboard complete. Your allocator just visualized its own evolution.")
