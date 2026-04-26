from app.data_provider import get_stock_data, get_short_interest
from app.indicators import calculate_rsi
from app.scoring import score_stock

WATCHLIST = ["AAPL", "TSLA", "AMC", "GME", "NVDA"]

def scan_market():
    results = []

    for ticker in WATCHLIST:
        df = get_stock_data(ticker)
        df = calculate_rsi(df)

        rsi = df["rsi"].iloc[-1]
        short_data = get_short_interest(ticker)

        score = score_stock(
            rsi,
            short_data["short_interest"],
            short_data["days_to_cover"]
        )

        results.append({
            "ticker": ticker,
            "rsi": float(rsi),
            "short_interest": short_data["short_interest"],
            "days_to_cover": short_data["days_to_cover"],
            "score": score
        })

    # sort by strongest squeeze potential
    return sorted(results, key=lambda x: x["score"], reverse=True)
