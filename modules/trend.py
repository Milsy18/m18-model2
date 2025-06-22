
def score_scale(val, y_thresh, g_thresh):
    return 1.0 if val >= g_thresh else 0.5 if val >= y_thresh else 0.0

def get_trend_thresholds(mkt_level):
    thresholds_by_level = {
        1:  {"ema5": (0.3, 0.4),   "ema10": (1.0, 1.5),   "ema50": (6.0, 8.0),   "ema100": (5.5, 7.5),   "ema200": (6.5, 8.5),   "adx": (20.0, 22.0)},
        2:  {"ema5": (0.489,0.501),"ema10": (2.023,3.153),"ema50": (8.522,10.634),"ema100": (8.032,10.033),"ema200": (9.513,11.505),"adx": (29.438,29.577)},
        3:  {"ema5": (1.315,1.916),"ema10": (2.650,3.438),"ema50": (3.455,5.254),"ema100": (0.119,5.363),"ema200": (1.025,7.014),"adx": (21.834,24.980)},
        4:  {"ema5": (0.545,0.717),"ema10": (0.991,1.107),"ema50": (-3.015,-2.734),"ema100": (-6.670,-6.046),"ema200": (-2.958,-1.813),"adx": (24.432,24.796)},
        5:  {"ema5": (-0.014,0.282),"ema10": (-0.349,0.345),"ema50": (-4.698,-4.063),"ema100": (-2.575,-2.087),"ema200": (3.793,6.362),"adx": (27.025,35.577)},
        6:  {"ema5": (0.3,0.5),   "ema10": (0.5,1.2),   "ema50": (-1.5,-1.0),   "ema100": (0.0,1.0),     "ema200": (4.0,6.0),    "adx": (28.0,36.0)},
        7:  {"ema5": (0.6,0.8),   "ema10": (1.5,2.2),   "ema50": (0.0,1.0),     "ema100": (2.0,3.0),     "ema200": (6.0,8.0),    "adx": (30.0,38.0)},
        8:  {"ema5": (0.9,1.1),   "ema10": (2.5,3.2),   "ema50": (2.0,3.0),     "ema100": (4.0,5.0),     "ema200": (8.0,10.0),   "adx": (32.0,40.0)},
        9:  {"ema5": (1.2,1.4),   "ema10": (3.5,4.2),   "ema50": (4.0,5.0),     "ema100": (6.0,7.0),     "ema200": (10.0,12.0),  "adx": (34.0,42.0)},
    }
    return thresholds_by_level.get(mkt_level, thresholds_by_level[5])  # default to level 5

def compute_trend_score(row):
    mkt_level = int(row["market_level"])
    thresholds = get_trend_thresholds(mkt_level)

    scores = {
        "ema5":   score_scale(row["ema5_pct"],  *thresholds["ema5"]),
        "ema10":  score_scale(row["ema10_pct"], *thresholds["ema10"]),
        "ema50":  score_scale(row["ema50_pct"], *thresholds["ema50"]),
        "ema100": score_scale(row["ema100_pct"],*thresholds["ema100"]),
        "ema200": score_scale(row["ema200_pct"],*thresholds["ema200"]),
        "adx":    score_scale(row["adx"],        *thresholds["adx"]),
    }

    trend_score = (
        scores["ema5"]   * 0.18 +
        scores["ema10"]  * 0.17 +
        scores["ema50"]  * 0.15 +
        scores["ema100"] * 0.16 +
        scores["ema200"] * 0.14 +
        scores["adx"]    * 0.20
    ) * 30  # Max contribution to total score

    return trend_score
