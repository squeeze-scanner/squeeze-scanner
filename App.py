import streamlit as st
import pandas as pd
import yfinance as yf
import time

st.set_page_config(page_title="Pro Squeeze Scanner", layout="wide")

st.title("🚀 Pro Squeeze Scanner")

TICKERS = ["AMC", "GME", "BB", "BYND", "NKLA", "SAVA", "FUBO", "PLUG", "RIVN"]

# -----------------------------
# CORE DATA ENGINE (ROBUST)
# -----------------------------

@st.cache_data(ttl=300)
def fetch_data(ticker):
    try:
        t = yf.Ticker(ticker)
        hist = t.history(period="3mo")

        if hist is None or hist.empty:
            return None

        close = hist["Close"].dropna()
        volume = hist["Volume"].fillna(0)

        if len(close) < 20:
            return None

        # --------------------
        # SAFE CALCULATIONS
        # --------------------

        rel_vol = float(volume.iloc[-1] / (volume.mean() if volume.mean() != 0 else 1))

        change = float((close.iloc[-1] / close.iloc[0]) - 1)

        delta = close.diff()

        gain = delta.where(delta > 0, 0).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()

        rs = gain / (loss.replace(0, 0.0001))  # prevents divide-by-zero

        rsi_series = 100 - (100 / (1 + rs))
        rsi = float(rsi_series.iloc[-1]) if not rsi_series.isna().iloc[-1] else 50

        # -----------------------------
        # SIGNAL ENGINE
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
            signals.append("Reversal Setup")

        if score >= 70:
            signal = "🚨 STRONG SQUEEZE SETUP"
        elif score >= 40:
            signal = "⚠️ WATCH"
        else:
            signal = "—"

        return {
            "Ticker": ticker,
            "Score": round(score, 2),
            "RSI": round(rsi, 2),
            "Rel Volume": round(rel_vol, 2),
            "3M Change %": round(change * 100, 2),
            "Signal": signal,
            "Triggers": ", ".join(signals)
        }

    except Exception:
        return {
            "Ticker": ticker,
            "Score": 0,
            "RSI": 50,
            "Rel Volume": 1,
            "3M Change %": 0,
            "Signal": "Error Safe Mode",
            "Triggers": "Data fallback used"
        }

# -----------------------------
# SCANNER UI
# -----------------------------

if st.button("Run Pro Scan"):

    results = []

    with st.spinner("Scanning market..."):
        for t in TICKERS:
            data = fetch_data(t)
            if data:
                results.append(data)

    # 🧠 ALWAYS create df (fixes NameError)
    if len(results) == 0:
        st.warning("No data returned — showing empty table")
        df = pd.DataFrame([{
            "Ticker": "N/A",
            "Score": 0,
            "RSI": 0,
            "Rel Volume": 0,
            "3M Change %": 0,
            "Signal": "No Data",
            "Triggers": "Retry scan"
        }])
    else:
        df = pd.DataFrame(results)
        df = df.sort_values("Score", ascending=False)

    st.subheader("📊 Scan Results")
    st.dataframe(df, use_container_width=True)

    alerts = df[df["Score"] >= 70]

    if not alerts.empty:
        st.error("🚨 STRONG SQUEEZE SETUPS DETECTED")
        st.dataframe(alerts, use_container_width=True)
