import yfinance as yf
import pandas as pd
import warnings

# Suppress all FutureWarnings globally
warnings.simplefilter(action='ignore', category=FutureWarning)

def score_fund(ticker: str, debug: bool = False) -> int:
    """
    Scores a fund's trend using:
    +1 if price > 20DMA
    +1 if price > 50DMA
    +1 if 3-month return > 0%
    Returns integer score from –3 to +3.
    """

    try:
        data = yf.download(ticker, period="6mo", interval="1d", progress=False, auto_adjust=False)

        if "Close" not in data.columns or data.empty:
            raise ValueError(f"No valid 'Close' data returned for {ticker}")

        close_prices = data["Close"].dropna()

        if len(close_prices) < 65:
            raise ValueError(f"Not enough data to compute trend for {ticker} (have {len(close_prices)} days)")

        price_now = close_prices.iloc[-1].item()
        price_3mo_ago = close_prices.iloc[-63].item()

        ma20_series = close_prices.rolling(window=20).mean()
        ma50_series = close_prices.rolling(window=50).mean()
        ma20 = ma20_series.iloc[-1].item()
        ma50 = ma50_series.iloc[-1].item()
        ret_3mo = (price_now / price_3mo_ago) - 1

        # NaN check
        if pd.isna(ma20) or pd.isna(ma50) or pd.isna(ret_3mo):
            raise ValueError(f"Computed MA or return is NaN for {ticker}")

        score = 0
        score += 1 if price_now > ma20 else -1
        score += 1 if price_now > ma50 else -1
        score += 1 if ret_3mo > 0 else -1

        if debug:
            print(f"🔍 {ticker} Price: {price_now:.2f} | MA20: {ma20:.2f} | MA50: {ma50:.2f} | 3mo Ret: {ret_3mo:.2%}")
            print(f"→ Trend Score: {score}")

        return score

    except Exception as e:
        print(f"⚠️ Error scoring {ticker}: {e}")
        return 0
