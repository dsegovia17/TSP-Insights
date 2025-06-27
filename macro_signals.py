from fredapi import Fred
import os
import yfinance as yf
import pandas as pd

# Initialize FRED client
fred = Fred(api_key=os.getenv("FRED_API_KEY"))

def safe_pull(series, name):
    """
    Extracts and logs the latest clean numeric value from a FRED time series.
    """
    try:
        val = float(series.dropna().astype(float).iloc[-1])
        print(f"✅ {name}: {val}")
        return val
    except Exception as e:
        print(f"⚠️ Error pulling {name}: {e}")
        return None

def get_series(name):
    """
    Fetches raw time series from FRED using its ID.
    """
    try:
        return fred.get_series(name)
    except Exception as e:
        print(f"⚠️ Error fetching {name}: {e}")
        return pd.Series(dtype=float)
