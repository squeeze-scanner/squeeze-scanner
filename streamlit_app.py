import streamlit as st
import pandas as pd

from app.scanner import scan_market

st.set_page_config(page_title="Short Squeeze Scanner", layout="wide")

st.title("📈 Short Squeeze Scanner")

st.write("""
This tool scans stocks for potential short squeeze setups using:
- RSI (oversold conditions)
- Short interest %
- Days to cover
- Combined squeeze score
""")

# Button to trigger scan
if st.button("Run Scan 🚀"):
    results = scan_market()

    # Convert Pydantic objects → DataFrame
    df = pd.DataFrame([r.dict() for r in results])

    st.subheader("Top Squeeze Candidates")

    st.dataframe(df, use_container_width=True)

    # Highlight best candidate
    best = df.iloc[0]

    st.success(f"""
    🔥 Strongest Candidate: {best['ticker']}
    Score: {best['score']}
    RSI: {best['rsi']}
    Short Interest: {best['short_interest']}
    Days to Cover: {best['days_to_cover']}
    """)
