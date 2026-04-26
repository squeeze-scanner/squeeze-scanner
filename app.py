
import streamlit as st from scanner import scan_market

st.set_page_config(page_title="Short Squeeze Scanner", layout="wide")

st.title("📈 Short Squeeze Candidate Scanner")

st.sidebar.header("Filters") rsi_threshold = st.sidebar.slider("Max RSI (oversold)", 10, 50, 30) short_interest_threshold = st.sidebar.slider("Min Short Interest (%)", 5, 50, 20) dtc_threshold = st.sidebar.slider("Min Days to Cover", 1, 15, 5)

st.write("Scanning market...")

results = scan_market( rsi_threshold=rsi_threshold, short_interest_threshold=short_interest_threshold, dtc_threshold=dtc_threshold )

if results.empty: st.warning("No candidates found.") else: st.success(f"Found {len(results)} candidates") st.dataframe(results)

=========================

FILE: scanner.py

=========================

import pandas as pd from data import get_stock_data, get_short_interest_data from indicators import calculate_rsi

TICKERS = [ "AAPL","TSLA","GME","AMC","NVDA","META","AMZN","NFLX" ]

def scan_market(rsi_threshold, short_interest_threshold, dtc_threshold): results = []

short_data = get_short_interest_data()

for ticker in TICKERS:
    try:
        df = get_stock_data(ticker)
        df['RSI'] = calculate_rsi(df)

        latest = df.iloc[-1]

        si = short_data.get(ticker, {}).get("short_interest", 0)
        dtc = short_data.get(ticker, {}).get("days_to_cover", 0)

        if (
            latest['RSI'] < rsi_threshold and
            si > short_interest_threshold and
            dtc > dtc_threshold
        ):
            results.append({
                "Ticker": ticker,
                "RSI": round(latest['RSI'], 2),
                "Short Interest (%)": si,
                "Days to Cover": dtc
            })

    except Exception as e:
        print(f"Error processing {ticker}: {e}")

return pd.DataFrame(results)

=========================

FILE: indicators.py

=========================

import pandas as pd

def calculate_rsi(df, period=14): delta = df['Close'].diff()

gain = delta.clip(lower=0).rolling(window=period).mean()
loss = -delta.clip(upper=0).rolling(window=period).mean()

rs = gain / loss
rsi = 100 - (100 / (1 + rs))

return rsi

=========================

FILE: data.py

=========================

import yfinance as yf import streamlit as st

@st.cache_data def get_stock_data(ticker): df = yf.download(ticker, period="3mo", interval="1d", progress=False) return df

Placeholder short interest data

Replace with real API integration

@st.cache_data def get_short_interest_data(): return { "GME": {"short_interest": 22, "days_to_cover": 6}, "AMC": {"short_interest": 18, "days_to_cover": 4}, "TSLA": {"short_interest": 3, "days_to_cover": 1}, "AAPL": {"short_interest": 1, "days_to_cover": 1} }

=========================

FILE: requirements.txt

=========================

streamlit pandas numpy yfinance

=========================

FILE: README.md

=========================

Short Squeeze Scanner

A Streamlit app that scans stocks for potential short squeeze setups based on:

Low RSI (oversold)

High short interest

High days to cover


Features

Real-time price data via yfinance

Configurable filters

Simple UI

Cached data for performance


Setup

pip install -r requirements.txt
streamlit run app.py

Deployment

1. Push repo to GitHub


2. Go to Streamlit Cloud


3. Connect repo


4. Deploy app.py



Notes

Short interest data is mocked

Replace with real API (Fintel, Ortex, etc.)


Future Improvements

Alerts (email/Telegram)

Backtesting module

News sentiment analysis

Larger ticker universe
