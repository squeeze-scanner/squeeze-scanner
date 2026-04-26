import streamlit as st
import pandas as pd
import yfinance as yf
import time

st.set_page_config(page_title="Pro Trading Scanner", layout="wide")

st.title("📊 Pro Trading Scanner")

TICKERS = ["AMC", "GME", "BB", "BYND", "NKLA", "SAVA", "FUBO", "PLUG", "RIVN"]

# -----------------------------
# SAFE DATA ENGINE
# -----------------------------

@st.cache_data(ttl=60)
def get_data(ticker):
    try:
        df = yf.download(ticker, period="3mo", progress=False)

        if df is None or df.empty:
            return None

        close = df["Close"]
        volume = df["Volume"]

        # RSI
        delta = close.diff()
        gain = delta.where(delta > 0, 0).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        rsi = float(100 - (100 / (1 + rs)).iloc[-1])

        rel_vol = float(volume.iloc[-1] / volume.mean())
        change = float((close.iloc[-1] / close.iloc[0]) - 1)

        # -----------------------------
        # IMPROVED SIGNAL ENGINE
        # -----------------------------
        score = 0
        signals = []

        if rsi < 30:
            score += 35
            signals.append("RSI Oversold")

        if rel_vol > 2:
            score += 30
            signals.append("Volume Spike")

        if change < -0.1:
            score += 20
            signals.append("Oversold Reversal Setup")

        if rsi > 70:
            score -= 10
            signals.append("Overbought Risk")

        if score >= 70:
            signal = "🚨 STRONG SETUP"
        elif score >= 40:
            signal = "⚠️ WATCH"
        else:
            signal = "—"

        return {
            "Ticker": ticker,
            "Score": round(score, 2),
            "RSI": round(rsi, 2),
            "Rel Volume": round(rel_vol, 2),
            "Change %": round(change * 100, 2),
            "Signal": signal,
            "Triggers": ", ".join(signals)
        }

    except:
        return None


# -----------------------------
# AUTO REFRESH CONTROL
# -----------------------------

refresh = st.sidebar.checkbox("🔄 Auto Refresh (30s)")

if refresh:
    st.sidebar.info("Auto-refresh enabled")

# -----------------------------
# MAIN SCAN
# -----------------------------

def run_scan():
    results = []

    for t in TICKERS:
        data = get_data(t)
        if data:
            results.append(data)
        time.sleep(0.1)

    if len(results) == 0:
        return pd.DataFrame([{
            "Ticker": "N/A",
            "Score": 0,
            "RSI": 0,
            "Rel Volume": 0,
            "Change %": 0,
            "Signal": "No Data",
            "Triggers": "Retry scan"
        }])

    df = pd.DataFrame(results)
    return df.sort_values("Score", ascending=False)


# -----------------------------
# UI LOOP
# -----------------------------

if refresh:
    placeholder = st.empty()

    while True:
        with placeholder.container():
            df = run_scan()

            st.subheader("📊 Live Market Scan")
            st.dataframe(df, use_container_width=True)

            alerts = df[df["Score"] >= 70]

            if not alerts.empty:
                st.error("🚨 STRONG SETUPS DETECTED")
                st.dataframe(alerts, use_container_width=True)

        time.sleep(30)
        st.rerun()

else:
    if st.button("Run Scan"):
        df = run_scan()

        st.subheader("📊 Scan Results")
        st.dataframe(df, use_container_width=True)

        alerts = df[df["Score"] >= 70]

        if not alerts.empty:
            st.error("🚨 STRONG SETUPS DETECTED")
            st.dataframe(alerts, use_container_width=True)
