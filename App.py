=====================================================

# SQUEEZE SCANNER - REAL DATA VERSION (STABLE)

=====================================================

Streamlit app using REAL market data (Yahoo Finance)

Safe version: avoids crashes from missing fields

Works on Streamlit Cloud

=====================================================

import streamlit as st import pandas as pd import numpy as np import yfinance as yf

st.set_page_config(page_title="Squeeze Scanner", layout="wide")

st.title("🚀 Squeeze Scanner (Real Data Version)") st.write("Live market data powered by Yahoo Finance (safe mode)")

TICKERS = ["AMC", "GME", "BB", "BYND", "NKLA", "SAVA", "FUBO", "PLUG", "RIVN"]

=====================================================

INDICATOR: RSI

=====================================================

def rsi(series, period=14): delta = series.diff() gain = (delta.where(delta > 0, 0)).rolling(period).mean() loss = (-delta.where(delta < 0, 0)).rolling(period).mean() rs = gain / loss return 100 - (100 / (1 + rs))

=====================================================

SAFE REAL DATA SCANNER

=====================================================

@st.cache_data(ttl=300) def get_stock_data(ticker): try: stock = yf.Ticker(ticker) hist = stock.history(period="3mo")

if hist.empty:
        return None

    close = hist["Close"]
    volume = hist["Volume"]

    rsi_val = float(rsi(close).iloc[-1])
    rel_vol = float(volume.iloc[-1] / volume.mean())

    # SAFE info fetch (may be incomplete)
    try:
        info = stock.info or {}
    except:
        info = {}

    short_float = info.get("shortPercentOfFloat", 0) or 0
    short_float = float(short_float) * 100

    shares_short = info.get("sharesShort", 0) or 0
    avg_vol = info.get("averageVolume", 1) or 1

    days_to_cover = float(shares_short / avg_vol) if avg_vol else 0

    # =============================
    # SCORING MODEL
    # =============================

    score = 0

    if rsi_val < 30:
        score += 20
    elif rsi_val < 40:
        score += 10

    if short_float > 30:
        score += 25
    elif short_float > 15:
        score += 10

    if days_to_cover > 5:
        score += 20
    elif days_to_cover > 3:
        score += 10

    if rel_vol > 2:
        score += 15
    elif rel_vol > 1.5:
        score += 5

    return {
        "Ticker": ticker,
        "Score": round(score, 2),
        "RSI": round(rsi_val, 2),
        "Short % Float": round(short_float, 2),
        "Days to Cover": round(days_to_cover, 2),
        "Rel Volume": round(rel_vol, 2)
    }

except Exception:
    return None

=====================================================

UI

=====================================================

if st.button("🔄 Run Real Data Scan"):

results = []

with st.spinner("Scanning live market data..."):
    for t in TICKERS:
        data = get_stock_data(t)
        if data:
            results.append(data)

if results:
    df = pd.DataFrame(results)
    df = df.sort_values(by="Score", ascending=False)

    st.subheader("📊 Squeeze Candidates")
    st.dataframe(df, use_container_width=True)

    alerts = df[df["Score"] > 60]

    if not alerts.empty:
        st.error("🚨 SQUEEZE ALERTS DETECTED")
        st.dataframe(alerts, use_container_width=True)
else:
    st.warning("No data returned — try again in a few seconds")

=====================================================

REQUIREMENTS (GitHub)

=====================================================

st.markdown("""

requirements.txt

streamlit
pandas
numpy
yfinance

""")

=====================================================

NOTES

=====================================================

st.info("\nThis version uses REAL market data (Yahoo Finance).\nShort interest may be incomplete depending on ticker availability.")
