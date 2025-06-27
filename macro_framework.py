from macro_signals import get_series, safe_pull
import yfinance as yf
import pandas as pd

def score_growth():
    gdp = safe_pull(get_series("GDPC1").pct_change(4), "Real GDP YoY")
    lei = safe_pull(get_series("USSLIND"), "Leading Index")
    ip = safe_pull(get_series("INDPRO").pct_change(12), "Industrial Production YoY")

    score = 0
    if gdp is not None:
        score += 1 if gdp > 0.01 else -1
    if lei is not None:
        score += 1 if lei > 0 else -1
    if ip is not None:
        score += 1 if ip > 0 else -1

    return score

def score_inflation():
    cpi = safe_pull(get_series("CPIAUCSL").pct_change(12, fill_method=None), "CPI YoY")
    pce = safe_pull(get_series("PCEPI").pct_change(12, fill_method=None), "PCE YoY")
    wages = safe_pull(get_series("CES0500000003").pct_change(12, fill_method=None), "Avg Hourly Earnings YoY")

    score = 0
    if cpi is not None:
        score += -1 if cpi > 0.035 else 1
    if pce is not None:
        score += -1 if pce > 0.035 else 1
    if wages is not None:
        score += -1 if wages > 0.04 else 1

    return score

def score_monetary_policy():
    fed_funds = safe_pull(get_series("FEDFUNDS"), "Fed Funds Rate")
    ten = safe_pull(get_series("GS10"), "10Y Yield")
    two = safe_pull(get_series("GS2"), "2Y Yield")
    balance_sheet = safe_pull(get_series("WALCL").pct_change(12, fill_method=None), "Fed Balance Sheet YoY")

    score = 0
    if fed_funds is not None:
        score += -1 if fed_funds > 4.5 else 1
    if ten is not None and two is not None:
        curve = ten - two
        score += 1 if curve > 0 else -1
    if balance_sheet is not None:
        score += 1 if balance_sheet > 0 else -1

    return score

def score_risk_sentiment():
    vix = safe_pull(get_series("VIXCLS"), "VIX")
    spreads = safe_pull(get_series("BAMLH0A0HYM2"), "High Yield Credit Spreads")
    fci = safe_pull(get_series("ANFCI"), "Financial Conditions Index")

    score = 0
    if vix is not None:
        score += -1 if vix > 20 else 1
    if spreads is not None:
        score += -1 if spreads > 5 else 1
    if fci is not None:
        score += -1 if fci > 0 else 1

    return score

def score_market_internals():
    score = 0
    try:
        cyc = yf.download(["XLF", "XLY"], period="6mo", progress=False, auto_adjust=False)["Close"]
        defn = yf.download(["XLU", "XLV"], period="6mo", progress=False, auto_adjust=False)["Close"]

        cyc_perf = (cyc.iloc[-1] / cyc.iloc[0]).mean()
        defn_perf = (defn.iloc[-1] / defn.iloc[0]).mean()

        score += 1 if cyc_perf > defn_perf else -1
    except Exception as e:
        print(f"⚠️ Sector rotation data error: {e}")
    return score

def score_global_macro():
    oil = safe_pull(get_series("DCOILWTICO").pct_change(12, fill_method=None), "Oil YoY")
    em_fx = safe_pull(get_series("DTWEXEMEGS").pct_change(12, fill_method=None), "EM FX YoY")
    # TEMP PATCH — remove/replace China PMI if no reliable FRED series available
    china_pmi = None  # Optional: plug in external source or proxy later

    score = 0
    if oil is not None:
        score += -1 if oil > 0.2 else 1
    if em_fx is not None:
        score += -1 if em_fx < -0.05 else 1
    if china_pmi is not None:
        score += 1 if china_pmi > 50 else -1

    return score

def get_macro_pillars():
    return {
        "Growth": score_growth(),
        "Inflation": score_inflation(),
        "Monetary Policy": score_monetary_policy(),
        "Risk Sentiment": score_risk_sentiment(),
        "Market Internals": score_market_internals(),
        "Global Macro": score_global_macro()
    }
