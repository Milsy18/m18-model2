import pandas as pd
import numpy as np

def score_scale(series: pd.Series, y_thresh: float, g_thresh: float) -> pd.Series:
    """Map series to {0.0, 0.5, 1.0} based on yellow/green thresholds."""
    return pd.Series(
        np.where(series >= g_thresh, 1.0,
          np.where(series >= y_thresh, 0.5, 0.0)
        ),
        index=series.index
    )

def get_trend_thresholds(level: int) -> dict:
    """
    Regime‐aware thresholds from Pine getTrendThresholds().
    Level 2–5 as per your script; else uses the 'else' branch for all others.
    """
    if level == 2:
        g_ema5,  y_ema5  = 0.501,  0.489
        g_ema10, y_ema10 = 3.153,  2.023
        g_ema50, y_ema50 = 10.634, 8.522
        g_ema100,y_ema100= 10.033, 8.032
        g_ema200,y_ema200= 11.505, 9.513
        g_adx,   y_adx   = 29.577, 29.438
    elif level == 3:
        g_ema5,  y_ema5  = 1.916,  1.315
        g_ema10, y_ema10 = 3.438,  2.650
        g_ema50, y_ema50 = 5.254,  3.455
        g_ema100,y_ema100= 5.363,  0.119
        g_ema200,y_ema200= 7.014,  1.025
        g_adx,   y_adx   = 24.980, 21.834
    elif level == 4:
        g_ema5,  y_ema5  = 0.717,  0.545
        g_ema10, y_ema10 = 1.107,  0.991
        g_ema50, y_ema50 = -2.734, -3.015
        g_ema100,y_ema100= -6.046, -6.670
        g_ema200,y_ema200= -1.813, -2.958
        g_adx,   y_adx   = 24.796, 24.432
    elif level == 5:
        g_ema5,  y_ema5  = 0.282,  -0.014
        g_ema10, y_ema10 = 0.345,  -0.349
        g_ema50, y_ema50 = -4.063, -4.698
        g_ema100,y_ema100= -2.087, -2.575
        g_ema200,y_ema200= 6.362,   3.793
        g_adx,   y_adx   = 35.577,  27.025
    else:
        # default (all other levels)
        g_ema5,  y_ema5  = 0.492,  -0.085
        g_ema10, y_ema10 = 0.843,  -0.309
        g_ema50, y_ema50 = -4.888, -4.996
        g_ema100,y_ema100= -4.592, -7.832
        g_ema200,y_ema200= 1.136,  -1.025
        g_adx,   y_adx   = 38.523, 35.879

    return {
      "g_ema5":g_ema5,   "y_ema5":y_ema5,
      "g_ema10":g_ema10, "y_ema10":y_ema10,
      "g_ema50":g_ema50, "y_ema50":y_ema50,
      "g_ema100":g_ema100,"y_ema100":y_ema100,
      "g_ema200":g_ema200,"y_ema200":y_ema200,
      "g_adx":g_adx,     "y_adx":y_adx
    }

def compute_total_score(df: pd.DataFrame) -> pd.Series:
    """
    Compute only the trendScore portion of totalScore.
    Returns a Series named 'total_score' = trendScore.
    """
    level = int(df["market_level"].iloc[0])
    close = df["close"]
    high  = df["high"]
    low   = df["low"]

    # ── 1) Trend EMAs ─────────────────────────────────────
    ema5   = close.ewm(span=5,   adjust=False).mean()
    ema10  = close.ewm(span=10,  adjust=False).mean()
    ema50  = close.ewm(span=50,  adjust=False).mean()
    ema100 = close.ewm(span=100, adjust=False).mean()
    ema200 = close.ewm(span=200, adjust=False).mean()

    # ── 2) Percent differences ────────────────────────────
    ema5_pct   = 100 * (close - ema5)   / ema5
    ema10_pct  = 100 * (close - ema10)  / ema10
    ema50_pct  = 100 * (close - ema50)  / ema50
    ema100_pct = 100 * (close - ema100) / ema100
    ema200_pct = 100 * (close - ema200) / ema200

    # ── 3) Pine‐style ADX ────────────────────────────────
    prev_close = close.shift(1)
    tr1 = high - low
    tr2 = (high - prev_close).abs()
    tr3 = (low  - prev_close).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    trur = tr.ewm(alpha=1/14, adjust=False).mean()

    upMove   = (high - prev_close).clip(lower=0)
    downMove = (prev_close - low ).clip(lower=0)
    plusDM   = np.where((high - prev_close > downMove),   upMove,   0)
    minusDM  = np.where((prev_close - low  > upMove),    downMove, 0)

    plusDI  = 100 * pd.Series(plusDM,  index=df.index).ewm(alpha=1/14, adjust=False).mean() / trur
    minusDI = 100 * pd.Series(minusDM, index=df.index).ewm(alpha=1/14, adjust=False).mean() / trur
    adx_val = 100 * ((plusDI - minusDI).abs() / (plusDI + minusDI)).ewm(alpha=1/14, adjust=False).mean()

    # ── 4) Scale each metric ──────────────────────────────
    thresh = get_trend_thresholds(level)

    t_ema5  = score_scale(ema5_pct,   thresh["y_ema5"],   thresh["g_ema5"])
    t_ema10 = score_scale(ema10_pct,  thresh["y_ema10"],  thresh["g_ema10"])
    t_ema50 = score_scale(ema50_pct,  thresh["y_ema50"],  thresh["g_ema50"])
    t_ema100= score_scale(ema100_pct, thresh["y_ema100"], thresh["g_ema100"])
    t_ema200= score_scale(ema200_pct, thresh["y_ema200"], thresh["g_ema200"])
    t_adx   = score_scale(adx_val,    thresh["y_adx"],    thresh["g_adx"])

    # ── 5) Weighted sum × 30 ─────────────────────────────
    trendScore = (
      t_ema5  * 0.18 +
      t_ema10 * 0.17 +
      t_ema50 * 0.15 +
      t_ema100* 0.16 +
      t_ema200* 0.14 +
      t_adx   * 0.20
    ) * 30

    return pd.Series(trendScore, index=df.index, name="total_score")
