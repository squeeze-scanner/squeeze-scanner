import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="Squeeze Scanner", layout="wide")

st.title("🚀 Squeeze Scanner (Stable Live Version)")

TICKERS = ["AMC", "GME", "BB", "BYND", "NKLA", "SAVA", "FUBO", "PLUG", "RIVN"]

def get_data(ticker):
    try:
        df = yf.download(ticker, period="3mo", progress=False)

        if df is None or df.empty:
            return None

        close = df["Close"]
        volume = df["Volume"]

        rel_vol = volume.iloc[-1] / volume.mean()
        change = (close.iloc[-1] / close.iloc[0]) - 1

        score = 0
        if rel_vol > 2:
            score += 40
        if change < -0.1:
            score += 30

        return {
            "Ticker": ticker,
            "Score": round(score, 2),
            "Rel Volume": round(rel_vol, 2),
            "3M Change %": round(change * 100, 2)
        }

    except:
        return None


if st.button("Run Scan"):
    results = []

    for t in TICKERS:
        r = get_data(t)
        if r:
            results.append(r)

    if results:
        df = pd.DataFrame(results)
        df = df.sort_values("Score", ascending=False)

        st.dataframe(df, use_container_width=True)

        alerts = df[df["Score"] > 50]

        if not alerts.empty:
            st.error("🚨 SQUEEZE ALERTS")
            st.dataframe(alerts)
    else:
        st.warning("No data available — try again")
