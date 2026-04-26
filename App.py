import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np

st.set_page_config(page_title="Smart Universe Scanner v5", layout="wide")

st.title("🧠 Smart Universe Scanner v5")

# -----------------------------
# LOAD UNIVERSE (OPTION B)
# -----------------------------

@st.cache_data
def get_universe():
    sp500 = load_sp500_universe()

    if sp500:
        return sp500

    try:
        df = pd.read_csv("universe.csv")
        return df["ticker"].tolist()
    except:
        return []

TICKERS = get_universe()

if not TICKERS:
    st.error("Universe file missing or empty")
    st.stop()

st.sidebar.write(f"📊 Universe Size: {len(TICKERS)} stocks")

# -----------------------------
# LIQUIDITY FILTER (IMPORTANT)
# -----------------------------

def liquidity_check(ticker):
    try:
        data = yf.Ticker(ticker).history(period="5d")
        if data is None or data.empty:
            return False

        avg_volume = data["Volume"].mean()
        price = data["Close"].iloc[-1]

        if avg_volume < 500000:
            return False
        if price < 1:
            return False

        return True

    except:
        return False


# -----------------------------
# DATA ENGINE (LIGHTWEIGHT)
# -----------------------------

@st.cache_data(ttl=120)
def fetch_data(ticker):
    try:
        df = yf.Ticker(ticker).history(period="3mo")

        if df is None or df.empty or len(df) < 30:
            return None

        close = df["Close"]
        volume = df["Volume"]

        returns = close.pct_change()

        momentum = float((close.iloc[-1] / close.iloc[-20]) - 1)
        volatility = float(returns.std() * np.sqrt(252))
        rel_vol = float(volume.iloc[-1] / (volume.mean() or 1))

        delta = close.diff()
        gain = delta.clip(lower=0).rolling(14).mean()
        loss = (-delta.clip(upper=0)).rolling(14).mean()
        rs = gain / (loss.replace(0, 0.0001))
        rsi = float(100 - (100 / (1 + rs)).iloc[-1])

        score = 0
        signals = []

        if momentum > 0.10:
            score += 25
            signals.append("Momentum")

        if volatility > 0.4:
            score += 20
            signals.append("Vol Expansion")

        if rel_vol > 2:
            score += 25
            signals.append("Liquidity Spike")

        if rsi < 30:
            score += 20
            signals.append("Oversold")

        if score >= 80:
            regime = "🔥 HIGH CONVICTION"
        elif score >= 60:
            regime = "⚠️ WATCH"
        else:
            regime = "Neutral"

        return {
            "Ticker": ticker,
            "Score": round(score, 2),
            "Momentum %": round(momentum * 100, 2),
            "Volatility": round(volatility, 2),
            "Rel Volume": round(rel_vol, 2),
            "RSI": round(rsi, 2),
            "Regime": regime,
            "Signals": ", ".join(signals)
        }

    except:
        return None


# -----------------------------
# SCAN ENGINE (FILTERED UNIVERSE)
# -----------------------------

def run_scan():
    results = []

    st.info("🔍 Filtering liquid stocks first...")

    liquid_universe = []

    for t in TICKERS:
        if liquidity_check(t):
            liquid_universe.append(t)

    st.write(f"📊 Tradable Universe: {len(liquid_universe)} stocks")

    for t in liquid_universe:
        data = fetch_data(t)
        if data:
            results.append(data)

    if not results:
        return pd.DataFrame([{
            "Ticker": "N/A",
            "Score": 0,
            "Regime": "No Data",
            "Signals": "Retry scan"
        }])

    return pd.DataFrame(results).sort_values("Score", ascending=False)


# -----------------------------
# UI
# -----------------------------

if st.button("🚀 Run Smart Scan"):

    with st.spinner("Scanning filtered universe..."):
        df = run_scan()

    st.subheader("📊 Market Intelligence Board")
    st.dataframe(df, use_container_width=True)

    alpha = df[df["Score"] >= 80]
    watch = df[(df["Score"] >= 60) & (df["Score"] < 80)]

    if not alpha.empty:
        st.error("🔥 HIGH CONVICTION SETUPS")
        st.dataframe(alpha, use_container_width=True)

    if not watch.empty:
        st.warning("⚠️ WATCHLIST")
        st.dataframe(watch, use_container_width=True)
