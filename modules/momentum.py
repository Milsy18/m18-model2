
def score_scale(val, y_thresh, g_thresh):
    return 1.0 if val >= g_thresh else 0.5 if val >= y_thresh else 0.0

def get_mom_thresholds(market_level):
    return {
        "rsi": (47.465, 49.060) if market_level == 2 else (51.930, 55.140) if market_level == 3 else (50.480, 52.240),
        "macd": (0.008, 0.013) if market_level == 2 else (0.005, 0.009) if market_level == 3 else (0.004, 0.006),
        "macd_signal": (0.010, 0.016) if market_level == 2 else (0.007, 0.011) if market_level == 3 else (0.005, 0.007),
    }

def compute_mom_score(row):
    ml = int(row["market_level"])
    thresholds = get_mom_thresholds(ml)

    scores = {
        "rsi": score_scale(row["rsi"], *thresholds["rsi"]),
        "macd": score_scale(row["macd"], *thresholds["macd"]),
        "macd_signal": score_scale(row["macd_signal"], *thresholds["macd_signal"]),
    }

    weighted_score = (
        scores["rsi"] * 0.25 +
        scores["macd"] * 0.40 +
        scores["macd_signal"] * 0.35
    ) * 35

    return weighted_score
