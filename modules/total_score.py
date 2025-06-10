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
    # (Paste your full level-by-level thresholds here—exactly as in the previous cell)
    ...

def compute_total_score(df: pd.DataFrame) -> pd.Series:
    level = int(df["market_level"].iloc[0])
    close = df["close"]; high = df["high"]; low = df["low"]

    # 1) EMAs
    ema5   = close.ewm(span=5,   adjust=False).mean()
    ema10  = close.ewm(span=10,  adjust=False).mean()
    ema50  = close.ewm(span=50,  adjust=False).mean()
    ema100 = close.ewm(span=100, adjust=False).mean()
    ema200 = close.ewm(span=200, adjust=False).mean()

    # 2) Percent diffs
    ema5_pct   = 100*(close-ema5)/ema5
    ema10_pct  = 100*(close-ema10)/ema10
    ema50_pct  = 100*(close-ema50)/ema50
    ema100_pct = 100*(close-ema100)/ema100
    ema200_pct = 100*(close-ema200)/ema200

    # 3) ADX calc
    prev = close.shift(1)
    tr1 = high-low
    tr2 = (high-prev).abs()
    tr3 = (low-prev).abs()
    tr  = pd.concat([tr1,tr2,tr3],axis=1).max(axis=1)
    trur = tr.ewm(alpha=1/14,adjust=False).mean()

    up   = (high-prev).clip(lower=0)
    down = (prev-low).clip(lower=0)
    plusDM  = np.where((high-prev)>down,   up,   0)
    minusDM = np.where(down>(high-prev), down, 0)
    plusDI  = 100*pd.Series(plusDM, index=df.index).ewm(alpha=1/14,adjust=False).mean()/trur
    minusDI = 100*pd.Series(minusDM,index=df.index).ewm(alpha=1/14,adjust=False).mean()/trur
    adx_val = 100*((plusDI-minusDI).abs()/(plusDI+minusDI)).ewm(alpha=1/14,adjust=False).mean()

    # 4) Scale + weight ×30
    t = get_trend_thresholds(level)
    components = [
      score_scale(ema5_pct,   t["y_ema5"],   t["g_ema5"])  * 0.18,
      score_scale(ema10_pct,  t["y_ema10"],  t["g_ema10"]) * 0.17,
      score_scale(ema50_pct,  t["y_ema50"],  t["g_ema50"]) * 0.15,
      score_scale(ema100_pct, t["y_ema100"], t["g_ema100"])* 0.16,
      score_scale(ema200_pct, t["y_ema200"], t["g_ema200"])* 0.14,
      score_scale(adx_val,    t["y_adx"],    t["g_adx"])   * 0.20
    ]
    trendScore = sum(components) * 30

    return pd.Series(trendScore, index=df.index, name="total_score")
