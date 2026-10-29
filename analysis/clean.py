"""
Usage: python analysis/clean.py <raw file> [start time in seconds]
Ex: python analysis/clean.py data/bugs_1.csv 0.8

The start time is optional, Use it if the raw file wasn't already trimmed to the release.
Output: data/clean/<name>_clean.csv (the raw file is never changed).
"""

import sys
from pathlib import Path
import pandas as pd

# drop bugs tracked less than 80% of the time
MIN_TRACKED = 0.80

raw_path = Path(sys.argv[1])
start_time = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0

data = pd.read_csv(raw_path)

# Cut everything before the release and restart time at 0
data = data[data["timestamp"] >= start_time].copy()
data["time"] = (data["timestamp"] - start_time).round(1)

# Keep well-tracked bugs ("tracked" is True/False, so its mean = fraction of time tracked)
columns = ["time"]
for col in data.columns:
    if col.startswith("tracked_") and data[col].mean() >= MIN_TRACKED:
        bug = col.removeprefix("tracked_")
        columns += [f"center_x_{bug}", f"center_y_{bug}"]


out_path = Path("data/clean") / f"{raw_path.stem}_clean.csv"
data[columns].to_csv(out_path, index=False)