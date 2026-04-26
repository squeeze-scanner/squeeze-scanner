import streamlit as st
from engine import run_trading_desk

st.set_page_config(page_title="Trading Desk v4", layout="wide")

st.title("🏦 Trading Desk System v4")

live = st.sidebar.checkbox("🔄 Live Mode (60s)")

if live:
    st.autorefresh(interval=60000, key="refresh")

df, alpha, watch = run_trading_desk()

st.subheader("📊 Market Intelligence Board")
st.dataframe(df, use_container_width=True)

if not alpha.empty:
    st.error("🔥 INSTITUTIONAL GRADE SETUPS")
    st.dataframe(alpha, use_container_width=True)

if not watch.empty:
    st.warning("⚠️ WATCHLIST (BUILDING POSITIONS)")
    st.dataframe(watch, use_container_width=True)
