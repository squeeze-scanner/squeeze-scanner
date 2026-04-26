import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="Squeeze Scanner", layout="wide")

st.title("🚀 Squeeze Scanner")

TICKERS = ["AMC", "GME", "BB", "BYND", "NKLA", "SAVA", "FUBO", "PLUG", "RIVN"]

# -----------------------------
# SAFE REAL DATA FUNCTION
# -----------------------------

@st.cache_data(ttl=300)
def get_data(ticker):
    try:
        df = yf.download(ticker, period="3mo", progress=False)

        if df is None or df.empty:
            return None

        close = df["Close"]
        volume = df["Volume"]

        # RSI calculation (stable)
        delta = close.diff()
        gain = delta.where(delta > 0, 0).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        rsi = float(100 - (100 / (1 + rs)).iloc[-1])

        rel_vol = float(volume.iloc[-1] / volume.mean())
        change = float((close.iloc[-1] / close.iloc[0]) - 1)

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
        return
