import pandas as pd
import yfinance as yf
import numpy as np

TICKERS = ["AMC", "GME", "BB", "BYND", "NKLA", "SAVA", "FUBO", "PLUG", "RIVN"]

# -----------------------------
# DATA LAYER
# -----------------------------

def fetch(ticker):
    try:
        df = yf.Ticker(ticker).history(period="6mo")

        if df is None or df.empty or len(df) < 50:
            return None

        close = df["Close"]
        volume = df["Volume"]
        returns = close.pct_change()

        momentum = float((close.iloc[-1] / close.iloc[-20]) - 1)
        volatility = float(returns.std() * np.sqrt(252))
        rel_vol = float(volume.iloc[-1] / volume.mean())
        drawdown = float((close.iloc[-1] / close.max()) - 1)

        delta = close.diff()
        gain = delta.clip(lower=0).rolling(14).mean()
        loss = (-delta.clip(upper=0)).rolling(14).mean()
        rs = gain / (loss.replace(0, 0.0001))
        rsi = float(100 - (100 / (1 + rs)).iloc[-1])

        # -----------------------------
        # CORE SCORING ENGINE
        # -----------------------------
        score = 0
        signals = []

        if momentum > 0.10:
            score += 25
            signals.append("Momentum Trend")

        if volatility > 0.4:
            score += 20
            signals.append("Volatility Expansion")

        if rel_vol > 2:
            score += 25
            signals.append("Liquidity Surge")

        if rsi < 30:
            score += 20
            signals.append("Oversold Reversal")

        if drawdown < -0.2:
            score += 10
            signals.append("Deep Value Zone")

        # -----------------------------
        # REGIME CLASSIFICATION
        # -----------------------------
        if score >= 80:
            regime = "🔥 CORE TRADE (HEDGE FUND LEVEL)"
        elif score >= 60:
            regime = "⚠️ BUILDING POSITION"
        elif score >= 40:
            regime = "Neutral"
        else:
            regime = "No Edge"

        return {
            "Ticker": ticker,
            "Score": round(score, 2),
            "Momentum": round(momentum * 100, 2),
            "Volatility": round(volatility, 2),
            "Rel Volume": round(rel_vol, 2),
            "RSI": round(rsi, 2),
            "Drawdown %": round(drawdown * 100, 2),
            "Regime": regime,
            "Signals": ", ".join(signals)
        }

    except:
        return None


# -----------------------------
# DESK ENGINE
# -----------------------------

def run_trading_desk():
    results = []

    for t in TICKERS:
        data = fetch(t)
        if data:
            results.append(data)

    if not results:
        empty = pd.DataFrame([{
            "Ticker": "N/A",
            "Score": 0,
            "Regime": "No Data",
            "Signals": "Retry"
        }])
        return empty, empty, empty

    df = pd.DataFrame(results).sort_values("Score", ascending=False)

    alpha = df[df["Score"] >= 80]
    watch = df[(df["Score"] >= 60) & (df["Score"] < 80)]

    return df, alpha, watch
