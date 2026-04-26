import pandas as pd
import pandas_ta as ta

def calculate_rsi(df: pd.DataFrame, period: int = 14):
    df["rsi"] = ta.rsi(df["close"], length=period)
    return df
