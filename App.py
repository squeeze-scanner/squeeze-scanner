import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

TICKERS = ["AMC", "GME", "BB", "BYND", "NKLA", "SAVA", "FUBO", "PLUG", "RIVN"]

def rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def score_stock(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="3mo")

        if hist.empty:
            return None

        close = hist["Close"]
        volume = hist["Volume"]

        rsi_val = rsi(close).iloc[-1]
        rel_vol = volume.iloc[-1] / volume.mean()

        info = stock.info

        short_float = info.get("shortPercentOfFloat", 0) * 100
        shares_short = info.get("sharesShort", 0)
        avg_vol = info.get("averageVolume", 1)

        days_to_cover = shares_short / avg_vol if avg_vol else 0

        score = 0

        if rsi_val < 30:
            score += 20
        if short_float > 30:
            score += 25
        if days_to_cover > 5:
            score += 20
        if rel_vol > 2:
            score += 15

        return {
            "Ticker": ticker,
            "Score": round(score, 2),
            "RSI": round(rsi_val, 2),
            "Short % Float": round(short_float, 2),
            "Days to Cover": round(days_to_cover, 2),
            "Rel Volume": round(rel_vol, 2)
        }

    except:
        return None

st.title("Squeeze Scanner")

if st.button("Run Scan"):
    results = []

    for t in TICKERS:
        r = score_stock(t)
        if r:
            results.append(r)

    df = pd.DataFrame(results)

    if not df.empty:
        df = df.sort_values(by="Score", ascending=False)
        st.dataframe(df)

        alerts = df[df["Score"] > 60]

        if not alerts.empty:
            st.error("SQUEEZE ALERTS")
            st.dataframe(alerts)
