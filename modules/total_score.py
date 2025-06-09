import pandas as pd
import numpy as np

def score_scale(series: pd.Series, y_thresh: float, g_thresh: float) -> pd.Series:
    """
    Scale a numeric Series into {0.0, 0.5, 1.0} based on yellow/green thresholds.
    """
    return pd.Series(
        np.where(series >= g_thresh, 1.0,
          np.where(series >= y_thresh, 0.5, 0.0)
        ),
        index=series.index
    )

def get_trend_thresholds(level: int) -> dict:
    """
    Return a dict of { 'g_ema5':…, 'y_ema5':…, … 'g_adx':…, 'y_adx':… }
    matching your Pine Script's getTrendThresholds() logic.
    """
    # Example for EMA5/EMA10; fill in all 12 keys from your script:
    if level == 2:
        g_ema5, y_ema5 = 0.501, 0.489
        g_ema10, y_ema10 = 3.153, 2.023
        # …and so on for ema50, ema100, ema200, adx…
    elif level == 3:
        g_ema5, y_ema5 = 1.916, 1.315
        g_ema10, y_ema10 = 3.438, 2.650
    # …levels 4,5,…9…
    else:
        # default or error
        g_ema5 = y_ema5 = g_ema10 = y_ema10 = np.nan

    return {
      "g_ema5": g_ema5, "y_ema5": y_ema5,
      "g_ema10": g_ema10, "y_ema10": y_ema10,
      # add keys 'g_ema50','y_ema50','g_ema100','y_ema100','g_ema200','y_ema200','g_adx','y_adx'
    }

# TODO: you’ll add get_mom_thresholds(), get_vty_thresholds(), get_vol_thresholds() here

def compute_total_score(df: pd.DataFrame) -> pd.Series:
    """
    Combine trendScore + momScore + vtyScore + volScore into a single total_score.
    Assumes:
      - df has columns: close, high, low, volume
      - df['market_level'] exists
    """
    # 1) Extract market_level
    level = df["market_level"].iloc[0]  # same for entire series

    # 2) Compute trendScore (placeholder)
    # trendScore = ...

    # 3) Compute momScore (placeholder)
    # momScore = ...

    # 4) Compute vtyScore (placeholder)
    # vtyScore = ...

    # 5) Compute volScore (placeholder)
    # volScore = ...

    # 6) Sum them up
    # return trendScore + momScore + vtyScore + volScore

    # For now, raise to remind us to fill it in
    raise NotImplementedError("Fill in totalScore logic")
