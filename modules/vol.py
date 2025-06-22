
def score_scale(val, y_thresh, g_thresh):
    return 1.0 if val >= g_thresh else 0.5 if val >= y_thresh else 0.0

def get_vol_thresholds(mkt_level):
    return {
        "cmf":  (0.02, 0.07) if mkt_level == 2 else (0.06, 0.13) if mkt_level == 3 else (0.04, 0.10),
        "rvol": (0.8, 1.1)   if mkt_level == 2 else (1.0, 1.4)   if mkt_level == 3 else (1.2, 1.6),
    }

def compute_vol_score(row):
    mkt_level = int(row["market_level"])
    thresholds = get_vol_thresholds(mkt_level)

    scores = {
        "cmf":  score_scale(row["cmf"],  *thresholds["cmf"]),
        "rvol": score_scale(row["rvol"], *thresholds["rvol"]),
    }

    score = (
        scores["cmf"]  * 0.55 +
        scores["rvol"] * 0.45
    ) * 15  # Max score = 15

    return score
