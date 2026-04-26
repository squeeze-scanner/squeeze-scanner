import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

st.set_page_config(page_title="Squeeze Scanner", layout="wide")

st.title("🚀 Squeeze Scanner (Stable Real Data)")

TICKERS = ["AMC", "GME", "BB", "BYND", "NKLA", "SAVA", "FUBO", "PLUG", "RIVN"]

def rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def score_stock(ticker):
    try:
        data = yf.download(ticker, period="3mo", progress=False)

        if data.empty:
            return None

        close = data["Close"]
        volume = data["Volume"]

        rsi_val = float(rsi(close).iloc[-1])
        rel_vol = float(volume.iloc[-1] / volume.mean())

        # SAFE synthetic squeeze proxies (no stock.info dependency)
        price_change = float((close.iloc[-1] / close.iloc[-20]) - 1)

        score = 0

        if rsi_val < 30:
            score += 25
        if rel_vol > 2:
            score += 25
        if price_change < -0.1:
            score += 20  # oversold squeeze setup

        return {
            "Ticker": ticker,
            "Score": round(score, 2),
            "RSI": round(rsi_val, 2),
            "Rel Volume": round(rel_vol, 2),
            "20D Change": round(price_change * 100, 2)
        }

    except:
        return None

if st.button("Run Scan"):
    results = []

    for t in TICKERS:
        r = score_stock(t)
        if r:
            results.append(r)

    df = pd.DataFrame(results)

    if not df.empty:
        df = df.sort_values("Score", ascending=False)
        st.dataframe(df, use_container_width=True)

        alerts = df[df["Score"] > 50]

        if not alerts.empty:
            st.error("🚨 SQUEEZE ALERTS")
            st.dataframe(alerts)
    else:
        st.warning("No data returned — try again")
