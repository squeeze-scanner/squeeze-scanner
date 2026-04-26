def score_stock(rsi, short_interest, days_to_cover):
    score = 0

    # RSI scoring (oversold = higher score)
    if rsi < 30:
        score += 30
    elif rsi < 40:
        score += 20
    elif rsi < 50:
        score += 10

    # Short interest scoring
    if short_interest > 0.25:
        score += 40
    elif short_interest > 0.15:
        score += 25
    elif short_interest > 0.10:
        score += 10

    # Days to cover scoring
    if days_to_cover > 5:
        score += 30
    elif days_to_cover > 3:
        score += 20
    elif days_to_cover > 2:
        score += 10

    return score
