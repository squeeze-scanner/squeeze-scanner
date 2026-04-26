import streamlit as st
import pandas as pd
import numpy as np
import random

st.set_page_config(page_title="Squeeze Scanner", layout="wide")

st.title("🚀 Squeeze Scanner (Simple Version)")
st.write("Demo scanner — stable version for mobile use")

TICKERS = ["AMC", "GME", "BB", "BYND", "NKLA", "SAVA", "FUBO", "PLUG", "RIVN"]

def generate_fake_data():
    data = []

    for t in TICKERS:
        score = random.randint(10, 100)
        rsi = random.randint(10, 80)
        short_float = random.randint(5, 60)
        days_to_cover = round(random.uniform(1, 10), 2)
        rel_volume = round(random.uniform(0.5, 5), 2)

        data.append({
            "Ticker": t,
            "Score": score,
            "RSI": rsi,
            "Short % Float": short_float,
            "Days to Cover": days_to_cover,
            "Rel Volume": rel_volume
        })

    return pd.DataFrame(data)

if st.button("Run Scan"):
    df = generate_fake_data()
    df = df.sort_values(by="Score", ascending=False)

    st.dataframe(df, use_container_width=True)

    alerts = df[df["Score"] > 70]

    if not alerts.empty:
        st.error("🚨 SQUEEZE ALERTS")
        st.dataframe(alerts)
