=====================================================

SQUEEZE SCANNER — GITHUB READY STREAMLIT APP

=====================================================

FILE: app.py

=====================================================

import streamlit as st import pandas as pd import numpy as np import yfinance as yf

-----------------------------

CONFIG

-----------------------------

TICKERS = ["AMC", "GME", "BB", "BYND", "NKLA", "SAVA", "FUBO", "PLUG", "RIVN"]

-----------------------------

INDICATOR: RSI

-----------------------------

def rsi(series, period=14): delta = series.diff() gain = (delta.where(delta > 0, 0)).rolling(period).mean() loss = (-delta.where(delta < 0, 0)).rolling(period).mean() rs = gain / loss return 100 - (100 / (1 + rs))

-----------------------------

SCORING ENGINE

-----------------------------

def score_stock(ticker): try: stock = yf.Ticker(ticker) hist = stock.history(period="3mo")

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

    # RSI
    if rsi_val < 30:
        score += 20
    elif rsi_val < 40:
        score += 10
