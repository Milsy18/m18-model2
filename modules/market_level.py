import pandas as pd

def compute_market_level(df: pd.DataFrame) -> pd.Series:
    """
    Compute market level based on composite score from TOTAL3, TOTAL, USDT.D, BTC.D.
    Expects df with columns: 'total3', 'totalCap', 'usdtD', 'btcD'.
    Returns an integer Series named 'market_level'.
    """
    window = 14
    smooth_len = 8

    # Extract series
    s_total3  = df['total3']
    s_totalCap = df['totalCap']
    s_usdtD   = df['usdtD']
    s_btcD    = df['btcD']

    # Rolling percentiles
    min_t3 = s_total3.rolling(window, min_periods=1).min()
    max_t3 = s_total3.rolling(window, min_periods=1).max()
    total3_pos  = (s_total3  - min_t3) / (max_t3  - min_t3)

    min_tc = s_totalCap.rolling(window, min_periods=1).min()
    max_tc = s_totalCap.rolling(window, min_periods=1).max()
    totalCap_pos = (s_totalCap - min_tc) / (max_tc - min_tc)

    min_ud = s_usdtD.rolling(window, min_periods=1).min()
    max_ud = s_usdtD.rolling(window, min_periods=1).max()
    usdtD_pos   = (s_usdtD   - min_ud) / (max_ud   - min_ud)

    min_bd = s_btcD.rolling(window, min_periods=1).min()
    max_bd = s_btcD.rolling(window, min_periods=1).max()
    btcD_pos    = (s_btcD    - min_bd) / (max_bd    - min_bd)

    # Scoring each component
    total3_score  = pd.Series(5, index=df.index).mask(total3_pos  > 0.7, 9).mask(total3_pos  < 0.3, 1)
    totalCap_score = pd.Series(5, index=df.index).mask(totalCap_pos > 0.7, 9).mask(totalCap_pos < 0.3, 1)
    usdtD_score   = pd.Series(5, index=df.index).mask(usdtD_pos   < 0.3, 9).mask(usdtD_pos   > 0.7, 1)
    btcD_score    = pd.Series(5, index=df.index).mask(btcD_pos    < 0.3, 9).mask(btcD_pos    > 0.7, 1)

    # Composite score & normalize
    mktScore_raw = total3_score + totalCap_score + usdtD_score + btcD_score
    mktScore     = (mktScore_raw / 4.0).fillna(5)

    # 3-bar trailing average smoothing
    mktScore_3bar = (
        mktScore
        + mktScore.shift(1).fillna(0)
        + mktScore.shift(2).fillna(0)
    ) / 3.0

    # EMA smoothing
    mktScoreEma = mktScore_3bar.ewm(span=smooth_len, adjust=False).mean()

    # Final rounded market level
    return mktScoreEma.round().astype(int).rename("market_level")
