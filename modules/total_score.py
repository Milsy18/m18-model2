import pandas as pd  # ✅ Required for pd.isna()

def compute_total_score(row):
    required_fields = ["trend_score", "mom_score", "vty_score", "vol_score"]
    if any(pd.isna(row[col]) for col in required_fields):
        return None  # or 0.0 depending on how you want to handle it

    return (
        row["trend_score"] +
        row["mom_score"] +
        row["vty_score"] +
        row["vol_score"]
    )


