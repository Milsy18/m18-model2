import pandas as pd

def compute_market_level(df: pd.DataFrame) -> pd.Series:
    """
    Compute market level from TOTAL3, TOTAL, USDT.D, BTC.D using:
    - 14-period rolling percentile thresholds
    - raw composite score (1/5/9)
    - single EMA smoothing with span=2
    """
    window = 14
    smooth_len = 2

    # Extract
    s_t3  = df['total3']
    s_tc  = df['totalCap']
    s_ud  = df['usdtD']
    s_bd  = df['btcD']

    # Rolling pos
    min_t3, max_t3 = s_t3.rolling(window,1).min(), s_t3.rolling(window,1).max()
    total3_pos  = (s_t3  - min_t3) / (max_t3  - min_t3)

    min_tc, max_tc = s_tc.rolling(window,1).min(), s_tc.rolling(window,1).max()
    totalCap_pos = (s_tc  - min_tc) / (max_tc  - min_tc)

    min_ud, max_ud = s_ud.rolling(window,1).min(), s_ud.rolling(window,1).max()
    usdtD_pos   = (s_ud   - min_ud) / (max_ud   - min_ud)

    min_bd, max_bd = s_bd.rolling(window,1).min(), s_bd.rolling(window,1).max()
    btcD_pos    = (s_bd   - min_bd) / (max_bd    - min_bd)

    # Component scores
    total3_score   = pd.Series(5, index=df.index).mask(total3_pos  > 0.7, 9).mask(total3_pos  < 0.3, 1)
    totalCap_score = pd.Series(5, index=df.index).mask(totalCap_pos > 0.7, 9).mask(totalCap_pos < 0.3, 1)
    usdtD_score    = pd.Series(5, index=df.index).mask(usdtD_pos   < 0.3, 9).mask(usdtD_pos   > 0.7, 1)
    btcD_score     = pd.Series(5, index=df.index).mask(btcD_pos    < 0.3, 9).mask(btcD_pos    > 0.7, 1)

    # Composite raw
    mktScore = (total3_score + totalCap_score + usdtD_score + btcD_score) / 4.0

    # Single EMA smoothing
    mktScoreEma = mktScore.ewm(span=smooth_len, adjust=False).mean()

    # Round to int levels
    return mktScoreEma.round().astype(int).rename("market_level")
