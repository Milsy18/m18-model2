import pandas as pd

class Thresholds:
    """
    Loads indicator_thresholds.csv and provides lookups for
    (metric, offset, market_level) → (yellow_thresh, green_thresh).
    """
    def __init__(self, path="data/processed/indicator_thresholds.csv"):
        self.df = pd.read_csv(path)
        self._map = {
            (r.metric, r.offset, int(r.market_level)): 
                (r.yellow_thresh, r.green_thresh)
            for r in self.df.itertuples()
        }

    def get(self, metric: str, offset: str, level: int):
        key = (metric, offset, level)
        if key not in self._map:
            raise KeyError(f"No thresholds defined for {key}")
        return self._map[key]
