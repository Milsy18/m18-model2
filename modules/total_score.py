import pandas as pd
import numpy as np

def score_scale(series: pd.Series, y_thresh: float, g_thresh: float) -> pd.Series:
    """
    Map series → {0.0, 0.5, 1.0} based on yellow/green thresholds.
    """
    return pd.Series(
        np.where(series >= g_thresh, 1.0,
          np.where(series >= y_thresh, 0.5, 0.0)
        ),
        index=series.index
    )

def get_trend_thresholds(level: int) -> dict:
    """
    Regime-aware thresholds from your Pine getTrendThresholds().
    Fill in levels 2–5 and else as shown earlier.
    """
    if level == 2:
        g_ema5, y_ema5 = 0.501, 0.489
        g_ema10, y_ema10 = 3.153, 2.023
        # …and so on…
    # elif level == 3: …
    # elif level == 4: …
    # elif level == 5: …
    else:
        g_ema5, y_ema5 = 0.492, -0.085
        # …and so on for the rest…

    return {
        "g_ema5": g_ema5,   "y_ema5": y_ema5,
        "g_ema10": g_ema10, "y_ema10": y_ema10,
        # … all other keys through "y_adx"
    }

# TODO: stub out get_mom_thresholds(), get_vty_thresholds(), get_vol_thresholds()

def compute_total_score(df: pd.DataFrame) -> pd.Series:
    """
    Combine trendScore + momScore + vtyScore + volScore into 'total_score'.
    """
    raise NotImplementedError("Fill in totalScore logic")
