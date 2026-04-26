import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="Pro Trading System v2", layout="wide")

st.title("📊 Pro Trading System v2")

TICKERS = ["AMC", "GME", "BB", "BYND", "NKLA", "SAVA", "FUBO", "PLUG", "RIVN"]

# -----------------------------
# LIVE MODE (SAFE)
# -----------------------------
live = st.sidebar.checkbox("🔄 Live Mode (30s refresh)")

if live:
    st.autorefresh(interval=30000, key="refresh")

# -----------------------------
# DATA ENGINE (HARDENED)
# -----------------------------

@st.cache_data(ttl=60)
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

        # -------------------------
        # CORE METRICS
        # -------------------------
        rel_vol = float(volume.iloc[-1] / (volume.mean() or 1))
        change = float((close.iloc[-1] / close.iloc[0]) - 1)

        delta = close.diff()

        gain = delta.where(delta > 0, 0).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()

        rs = gain / (loss.replace(0, 0.0001))
        rsi = float(100 - (100 / (1 + rs)).iloc[-1]) if not rs.isna().iloc[-1] else 50

        # -------------------------
        # PRO SCORING ENGINE v2
        # -------------------------
        score = 0
        signals = []

        # Oversold strength
        if rsi < 30:
            score += 40
            signals.append("Oversold (RSI)")

        # Momentum spike
        if rel_vol > 2:
            score += 30
            signals.append("Volume Surge")

        # Reversal setup
        if change < -0.1:
            score += 20
            signals.append("Reversal Zone")

        # Trend risk filter
        if rsi > 70:
            score -= 10
            signals.append("Overbought Risk")

        # -------------------------
        # CLASSIFICATION
        # -------------------------
        if score >= 75:
            status = "🚨 HIGH PROBABILITY SQUEEZE"
        elif score >= 50:
            status = "⚠️ WATCHLIST"
        elif score >= 25:
            status = "Low Interest"
        else:
            status = "No Setup"

        return {
            "Ticker": ticker,
            "Score": round(score, 2),
            "RS
