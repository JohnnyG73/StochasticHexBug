"""
Step 5: Monte Carlo. 1000 fake experiments from the urn model, with the same N's and run lengths as the
real ones, analyzed like the real data. Their spread is the error bar on k.
Output: results/monte_carlo.csv, monte_carlo.png, monte_carlo_paths.png
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from urn import RESULTS, DT, load_logs, count_k, pooled_fraction

rng = np.random.default_rng(1)  # fixed seed so results repeat


def simulate_run(N, k, run_time):
    """Fake crossing log: N bugs, each crossing independently at rate k."""
    time, n_left, rows = 0, N, []
    while True:
        time += rng.exponential(1 / (N * k))  # wait for the next crossing
        if time > run_time:
            break
        if rng.random() < n_left / N:  # the bug that crossed was on the left
            n_left -= 1
            rows.append([time, "R"])
        else:
            n_left += 1
            rows.append([time, "L"])

    if len(rows) < 2:  # rarely almost nothing crosses; try again
        return simulate_run(N, k, run_time)
    return pd.DataFrame(rows, columns=["time", "direction"])


def k_by_N(logs):
    """Counting k for each N."""
    Ns = sorted({N for N, log in logs})
    return pd.Series([count_k([(n, log) for n, log in logs if n == N]) for N in Ns], index=Ns)


logs = list(load_logs().values())
k_all = count_k(logs)

# 1000 fake experiments, each with the same N's and run lengths as the real one
fakes = []
for _ in range(1000):
    fake_logs = [(N, simulate_run(N, k_all, log["time"].iloc[-1])) for N, log in logs]
    fakes.append(k_by_N(fake_logs))
fakes = pd.DataFrame(fakes)

result = pd.DataFrame({"k": k_by_N(logs), "k_err": fakes.std()})
result.to_csv(RESULTS / "monte_carlo.csv", index_label="N")

plt.errorbar(result.index, result["k"], yerr=result["k_err"], fmt="o")
plt.axhline(k_all, color="gray")  # urn model: same k for every N
plt.xlabel("N")
plt.ylabel("k (1/s)")
plt.savefig(RESULTS / "monte_carlo.png")

# Paths: 200 fake experiments (all runs pooled) for 600 s, real data in black
plt.figure()
for _ in range(200):
    fake_logs = [(N, simulate_run(N, k_all, 600)) for N, log in logs]
    fraction = pooled_fraction(fake_logs, 600)
    plt.plot(np.arange(len(fraction)) * DT, fraction, lw=0.5)

fraction = pooled_fraction(logs, min(log["time"].iloc[-1] for N, log in logs))
plt.plot(np.arange(len(fraction)) * DT, fraction, "k", lw=2)
plt.xlabel("time since release (s)")
plt.ylabel("fraction of all bugs on the left")
plt.savefig(RESULTS / "monte_carlo_paths.png")
