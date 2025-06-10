import pandas as pd
import numpy as np

def score_scale(series: pd.Series, y_thresh: float, g_thresh: float) -> pd.Series:
    return pd.Series(
        np.where(series >= g_thresh, 1.0,
          np.where(series >= y_thresh, 0.5, 0.0)
        ),
        index=series.index
    )

def get_trend_thresholds(level: int) -> dict:
    if level == 2:
        g_ema5,  y_ema5   = 0.501,  0.489
        g_ema10, y_ema10  = 3.153,  2.023
        g_ema50, y_ema50  = 10.634, 8.522
        g_ema100,y_ema100 = 10.033, 8.032
        g_ema200,y_ema200 = 11.505, 9.513
        g_adx,   y_adx    = 29.577, 29.438
    elif level == 3:
        g_ema5,  y_ema5   = 1.916,  1.315
        g_ema10, y_ema10  = 3.438,  2.650
        g_ema50, y_ema50  = 5.254,  3.455
        g_ema100,y_ema100 = 5.363,  0.119
        g_ema200,y_ema200 = 7.014,  1.025
        g_adx,   y_adx    = 24.980, 21.834
    elif level == 4:
        g_ema5,  y_ema5   = 0.717,   0.545
        g_ema10, y_ema10  = 1.107,   0.991
        g_ema50, y_ema50  = -2.734, -3.015
        g_ema100,y_ema100 = -6.046, -6.670
        g_ema200,y_ema200 = -1.813, -2.958
        g_adx,   y_adx    = 24.796, 24.432
    elif level == 5:
        g_ema5,  y_ema5   = 0.282,  -0.014
        g_ema10, y_ema10  = 0.345,  -0.349
        g_ema50, y_ema50  = -4.063, -4.698
        g_ema100,y_ema100 = -2.087, -2.575
        g_ema200,y_ema200 = 6.362,   3.793
        g_adx,   y_adx    = 35.577,  27.025
    else:
        g_ema5,  y_ema5   = 0.492,  -0.085
        g_ema10, y_ema10  = 0.843,  -0.309
        g_ema50, y_ema50  = -4.888, -4.996
        g_ema100,y_ema100 = -4.592, -7.832
        g_ema200,y_ema200 = 1.136,  -1.025
        g_adx,   y_adx    = 38.523, 35.879

    return {
        "g_ema5": g_ema5,   "y_ema5": y_ema5,
        "g_ema10": g_ema10, "y_ema10": y_ema10,
        "g_ema50": g_ema50, "y_ema50": y_ema50,
        "g_ema100": g_ema100,"y_ema100": y_ema100,
        "g_ema200": g_ema200,"y_ema200": y_ema200,
        "g_adx": g_adx,     "y_adx": y_adx
    }

def compute_total_score(df: pd.DataFrame) -> pd.Series:
    level = int(df["market_level"].iloc[0])
    close, high, low = df["close"], df["high"], df["low"]

    # EMAs
    ema5   = close.ewm(span=5,   adjust=False).mean()
    ema10  = close.ewm(span=10,  adjust=False).mean()
    ema50  = close.ewm(span=50,  adjust=False).mean()
    ema100 = close.ewm(span=100, adjust=False).mean()
    ema200 = close.ewm(span=200, adjust=False).mean()

    # Percent diffs
    ema5_pct   = 100*(close - ema5)  / ema5
    ema10_pct  = 100*(close - ema10) / ema10
    ema50_pct  = 100*(close - ema50) / ema50
    ema100_pct = 100*(close - ema100)/ ema100
    ema200_pct = 100*(close - ema200)/ ema200

    # ADX calc
    prev = close.shift(1)
    tr1  = high - low
    tr2  = (high - prev).abs()
    tr3  = (low  - prev).abs()
    tr   = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    trur = tr.ewm(alpha=1/14, adjust=False).mean()

    up   = (high - prev).clip(lower=0)
    down = (prev - low).clip(lower=0)
    plusDM  = np.where((high - prev) > down,   up,   0)
    minusDM = np.where(down > (high - prev), down, 0)
    plusDI  = 100 * pd.Series(plusDM, index=df.index).ewm(alpha=1/14, adjust=False).mean() / trur
    minusDI = 100 * pd.Series(minusDM,index=df.index).ewm(alpha=1/14, adjust=False).mean() / trur
    adx_val = 100*((plusDI - minusDI).abs()/(plusDI + minusDI)).ewm(alpha=1/14,adjust=False).mean()

    # Scale & weight
    t = get_trend_thresholds(level)
    components = [
      score_scale(ema5_pct,   t["y_ema5"],   t["g_ema5"])   * 0.18,
      score_scale(ema10_pct,  t["y_ema10"],  t["g_ema10"])  * 0.17,
      score_scale(ema50_pct,  t["y_ema50"],  t["g_ema50"])  * 0.15,
      score_scale(ema100_pct, t["y_ema100"], t["g_ema100"]) * 0.16,
      score_scale(ema200_pct, t["y_ema200"], t["g_ema200"]) * 0.14,
      score_scale(adx_val,    t["y_adx"],    t["g_adx"])     * 0.20
    ]
    trendScore = sum(components) * 30

    return pd.Series(trendScore, index=df.index, name="total_score")
