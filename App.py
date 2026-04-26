import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="Squeeze Scanner", layout="wide")

st.title("🚀 Squeeze Scanner (Always Works Version)")

TICKERS = ["AMC", "GME", "BB", "BYND", "NKLA", "SAVA", "FUBO", "PLUG", "RIVN"]

def safe_scan(ticker):
    try:
        df = yf.download(ticker, period="3mo", progress=False)

        # HARD SAFETY CHECK (prevents blank crashes)
        if df is None or df.empty or "Close" not in df:
            return {
                "Ticker": ticker,
                "Score": 0,
                "Note": "No data"
            }

        close = df["Close"]
        volume = df["Volume"]

        rel_vol = float(volume.iloc[-1] / volume.mean()) if volume.mean() != 0 else 0
        change = float((close.iloc[-1] / close.iloc[0]) - 1)

        score = 0

        if rel_vol > 2:
            score += 40
        if change < -0.1:
            score += 30

        return {
            "Ticker": ticker,
            "Score": score,
            "Rel Volume": round(rel_vol, 2),
            "3M Change %": round(change * 100, 2)
        }

    except Exception:
        return {
            "Ticker": ticker,
            "Score": 0,
            "Note": "Error handled"
        }

# ALWAYS SHOW UI (important fix)
st.write("Click scan to load market data")

if st.button("Run Scan"):
    results = []

    for t in TICKERS:
        results.append(safe_scan(t))

    df = pd.DataFrame(results)
    df = df.sort_values("Score", ascending=False)

    st.dataframe(df, use_container_width=True)

    alerts = df[df["Score"] > 50]

    if not alerts.empty:
        st.error("🚨 SQUEEZE ALERTS")
        st.dataframe(alerts)
