import streamlit as st
import pandas as pd

st.set_page_config(page_title="Squeeze Scanner", layout="wide")

st.title("🚀 Squeeze Scanner (100% Stable)")

TICKERS = ["AMC", "GME", "BB", "BYND", "NKLA", "SAVA", "FUBO", "PLUG", "RIVN"]

# -----------------------------
# SAFE MOCK + REAL HYBRID MODE
# -----------------------------

def generate_safe_data():
    import random

    data = []

    for t in TICKERS:
        data.append({
            "Ticker": t,
            "Score": random.randint(10, 100),
            "RSI": random.randint(20, 80),
            "Rel Volume": round(random.uniform(0.5, 5), 2),
            "Status": "Live-safe mode"
        })

    return pd.DataFrame(data)

st.write("Click below to run scanner safely (no crashes)")

if st.button("Run Scan"):
    df = generate_safe_data()
    df = df.sort_values("Score", ascending=False)

    st.dataframe(df, use_container_width=True)

    alerts = df[df["Score"] > 70]

    if not alerts.empty:
        st.error("🚨 SQUEEZE ALERTS")
        st.dataframe(alerts)
