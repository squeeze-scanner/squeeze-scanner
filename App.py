import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np

st.set_page_config(page_title="Hedge Fund Scanner v3", layout="wide")

st.title("📊 Hedge Fund Style Scanner v3")

TICKERS = ["AMC", "GME", "BB", "BYND", "NKLA", "SAVA", "FUBO", "PLUG", "RIVN"]

# -----------------------------
# LIVE MODE (SAFE)
# -----------------------------
live = st.sidebar.checkbox("🔄 Live Mode (60s refresh)")

if live:
    st.autorefresh(interval=60000, key="refresh")

# -----------------------------
# DATA ENGINE (INSTITUTIONAL STYLE)
# -----------------------------

@st.cache_data(ttl=60)
def get_data(ticker):
    try:
        df = yf.Ticker(ticker).history(period="6mo")

        if df is None or df.empty or len(df) < 50:
            return None

        close = df["Close"]
        volume = df["Volume"]

        returns = close.pct_change()

        # -----------------------------
        # CORE FACTORS (HF STYLE)
        # -----------------------------

        # 1. Momentum (trend strength)
        momentum_20d = float((close.iloc[-1] / close.iloc[-20]) - 1)

        # 2. Volatility (risk + squeeze fuel)
        volatility = float(returns.std() * np.sqrt(252))

        # 3. Volume anomaly (liquidity spike)
        rel_vol = float(volume.iloc[-1] / volume.mean())

        # 4. Price pressure (drawdown rebound signal)
        drawdown = float((close.iloc[-1] / close.max()) - 1)

        # 5. RSI (institutional simplified)
        delta = close.diff()
        gain = delta.clip(lower=0).rolling(14).mean()
        loss = (-delta.clip(upper=0)).rolling(14).mean()
        rs = gain / (loss.replace(0, 0.0001))
        rsi = float(100 - (100 / (1 + rs)).iloc[-1])

        # -----------------------------
        # HF SCORING ENGINE v3
        # -----------------------------

        score = 0
        signals = []

        # Momentum factor
        if momentum_20d > 0.10:
            score += 30
            signals.append("Strong Momentum")

        # Volatility expansion (squeeze fuel)
        if volatility > 0.4:
            score += 20
            signals.append("Volatility Expansion")

        # Volume anomaly
        if rel_vol > 2:
            score += 25
            signals.append("Liquidity Surge")

        # Mean reversion zone
        if rsi < 30:
            score += 20
            signals.append("Oversold Reversion")

        # Deep value / rebound zone
        if drawdown < -0.2:
            score += 15
            signals.append("Deep Pullback")

        # -----------------------------
        # REGIME CLASSIFICATION
        # -----------------------------

        if score >= 80:
            regime = "🔥 HIGH CONVICTION SETUP"
        elif score >= 60:
            regime = "⚠️ WATCH (Building Setup)"
        elif score >= 40:
            regime = "Neutral / Noise"
        else:
            regime = "No Edge"

        return {
            "Ticker": ticker,
            "Score": round(score, 2),
            "Momentum 20D": round(momentum_20d * 100, 2),
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
# SCAN ENGINE
# -----------------------------

def run_scan():
    results = []

    for t in TICKERS:
        data = get_data(t)
        if data:
            results.append(data)

    if not results:
        return pd.DataFrame([{
            "Ticker": "N/A",
            "Score": 0,
            "Regime": "No Data",
            "Signals": "Retry"
        }])

    return pd.DataFrame(results).sort_values("Score", ascending=False)


# -----------------------------
# DASHBOARD
# -----------------------------

df = run_scan()

st.subheader("📊 Institutional Signal Dashboard")

st.dataframe(df, use_container_width=True)

# -----------------------------
# ALERT TIERS
# -----------------------------

alpha = df[df["Score"] >= 80]
watch = df[(df["Score"] >= 60) & (df["Score"] < 80)]

if not alpha.empty:
    st.error("🔥 HIGH CONVICTION SETUPS")
    st.dataframe(alpha, use_container_width=True)

if not watch.empty:
    st.warning("⚠️ BUILDING SETUPS")
    st.dataframe(watch, use_container_width=True)
