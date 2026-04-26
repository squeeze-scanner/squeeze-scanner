import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="Squeeze Scanner", layout="wide")

st.title("🚀 Squeeze Scanner (Real Data)")

TICKERS = ["AMC", "GME", "BB", "BYND", "NKLA", "SAVA", "FUBO", "PLUG", "RIVN"]

# -----------------------------
# SAFE REAL DATA FUNCTION
# -----------------------------

@st.cache_data(ttl=300)
def get_stock_data(ticker):
    try:
        import time

        df = None

        # 🔁 retry logic (important fix)
        for _ in range(3):
            df = yf.download(ticker, period="3mo", progress=False)
            if df is not None and not df.empty:
                break
            time.sleep(0.5)

        # 🧠 fallback so app NEVER breaks
        if df is None or df.empty:
            return {
                "Ticker": ticker,
                "Score": 0,
                "RSI": 50,
                "Rel Volume": 1,
                "3M Change %": 0,
                "Note": "Fallback (no data from Yahoo)"
            }

        close = df["Close"]
        volume = df["Volume"]

        rel_vol = float(volume.iloc[-1] / volume.mean())
        change = float((close.iloc[-1] / close.iloc[0]) - 1)

        delta = close.diff()
        gain = delta.where(delta > 0, 0).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        rsi = float(100 - (100 / (1 + rs)).iloc[-1])

        score = 0
        if rsi < 30:
            score += 30
        if rel_vol > 2:
            score += 30
        if change < -0.1:
            score += 20

        return {
            "Ticker": ticker,
            "Score": round(score, 2),
            "RSI": round(rsi, 2),
            "Rel Volume": round(rel_vol, 2),
            "3M Change %": round(change * 100, 2)
        }

    except:
        return {
            "Ticker": ticker,
            "Score": 0,
            "RSI": 50,
            "Rel Volume": 1,
            "3M Change %": 0,
            "Note": "Error handled"
        }

# -----------------------------
# UI
# -----------------------------

if st.button("Run Real Data Scan"):
    results = []

    for t in TICKERS:
        data = get_stock_data(t)
        if data:
            results.append(data)

    if results:
        df = pd.DataFrame(results)
        df = df.sort_values("Score", ascending=False)

        st.dataframe(df, use_container_width=True)

        alerts = df[df["Score"] > 60]

        if not alerts.empty:
            st.error("🚨 SQUEEZE ALERTS")
            st.dataframe(alerts, use_container_width=True)
    else:
        st.warning("No data returned — try again in a moment")
