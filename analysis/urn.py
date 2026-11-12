"""
Shared functions for the urn-model analysis. Run the scripts from the repo folder, e.g. python analysis/rates.py
Logs: data/crossings/N{N}_run{R}.csv with columns time,direction (time from release, all bugs start on the left).
"""

from pathlib import Path
import numpy as np
import pandas as pd

DATA = Path("data/crossings")
RESULTS = Path("results")
DT = 0.1     # time step (s)
SETTLE = 45  # time (s) after which every run has settled

RESULTS.mkdir(exist_ok=True)


def load_logs():
    """Every log as name -> (N, log). N comes from the file name."""
    return {p.stem: (int(p.stem.split("_")[0][1:]), pd.read_csv(p)) for p in sorted(DATA.glob("N*_run*.csv"))}


def n_left_from_log(log, N, end=None):
    """Number of bugs on the left every DT seconds, up to `end` (default: the last crossing)."""
    if end is None:
        end = log["time"].iloc[-1]
    times = np.arange(0, end, DT)
    n_left = np.full(len(times), N)
    for time, direction in zip(log["time"], log["direction"]):
        if direction == "R":
            n_left[times >= time] -= 1
        else:
            n_left[times >= time] += 1

    if n_left.min() < 0 or n_left.max() > N:
        raise ValueError(f"N = {N} log: count goes outside 0..{N}, check the log")
    return times, n_left


def count_k(logs):
    """Crossings per bug-second over a list of (N, log). The last crossing only marks the end, so it isn't counted."""
    crossings = sum(len(log) - 1 for N, log in logs)
    bug_seconds = sum(N * log["time"].iloc[-1] for N, log in logs)
    return crossings / bug_seconds


def pooled_fraction(logs, end):
    """Fraction of all bugs on the left every DT seconds up to `end`, over a list of (N, log)."""
    return sum(n_left_from_log(log, N, end)[1] for N, log in logs) / sum(N for N, log in logs)


def settled_counts(logs, N):
    """Every n_L value after SETTLE, from all runs with N bugs, over a list of (N, log)."""
    values = []
    for n, log in logs:
        if n == N:
            times, n_left = n_left_from_log(log, N)
            values.extend(n_left[times > SETTLE])
    return np.array(values)
