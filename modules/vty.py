
def score_scale(val, y_thresh, g_thresh):
    return 1.0 if val >= g_thresh else 0.5 if val >= y_thresh else 0.0

def get_vty_thresholds(mkt_level):
    return {
        "atr": (0.021, 0.024) if mkt_level == 2 else (0.017, 0.022) if mkt_level == 3 else (0.010, 0.012),
        "std": (0.014, 0.017) if mkt_level == 2 else (0.011, 0.013) if mkt_level == 3 else (0.008, 0.009),
        "bbw": (0.032, 0.036) if mkt_level == 2 else (0.027, 0.033) if mkt_level == 3 else (0.019, 0.021),
        "rng": (0.052, 0.061) if mkt_level == 2 else (0.045, 0.055) if mkt_level == 3 else (0.038, 0.044),
    }

def compute_vty_score(row):
    mkt_level = int(row["market_level"])
    thresholds = get_vty_thresholds(mkt_level)

    scores = {
        "atr":  score_scale(row["atr"],  *thresholds["atr"]),
        "std":  score_scale(row["std"],  *thresholds["std"]),
        "bbw":  score_scale(row["bbw"],  *thresholds["bbw"]),
        "rng":  score_scale(row["rng"],  *thresholds["rng"]),
    }

    score = (
        scores["atr"] * 0.25 +
        scores["std"] * 0.25 +
        scores["bbw"] * 0.25 +
        scores["rng"] * 0.25
    ) * 20  # Max score = 20

    return score
