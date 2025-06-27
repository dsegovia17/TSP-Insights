import yfinance as yf
from macro_signals import get_series, safe_pull

def detect_fragility() -> tuple[bool, str]:
    warnings = []

    # 1. VIX Compression
    vix = safe_pull(get_series("VIXCLS"), "VIX")
    if vix is not None and vix < 12:
        warnings.append("VIX compression detected (<12)")

    # 2. SPY Gamma Pinning (low daily range)
    try:
        spy = yf.download("SPY", period="5d", interval="1d", progress=False)
        daily_ranges = spy["High"] - spy["Low"]
        avg_range_pct = (daily_ranges / spy["Close"]).mean()
        if avg_range_pct < 0.007:
            warnings.append("SPY showing narrow daily range (possible gamma pinning)")
    except Exception as e:
        warnings.append("SPY range error")

    # 3. Credit Stress
    spreads = safe_pull(get_series("BAMLH0A0HYM2"), "High Yield Spreads")
    spy_price = yf.download("SPY", period="1d", progress=False)["Close"].iloc[-1]
    if spreads is not None and spreads > 5 and spy_price > 400:
        warnings.append("Credit spreads elevated while SPY rallies")

    # 4. FX Fragility
    em_fx = safe_pull(get_series("DTWEXEMEGS").pct_change(12), "EM FX YoY")
    if em_fx is not None and em_fx < -0.05:
        warnings.append("EM FX weakening sharply (possible carry stress)")

    fragility = len(warnings) > 0
    flow_notes = " | ".join(warnings) if warnings else "No fragility triggers detected."

    return fragility, flow_notes
