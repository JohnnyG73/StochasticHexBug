"""
Step 3: pool all runs into one curve (fraction of all bugs on the left) and fit p + (1 - p) e^(-2kt).
The band is the expected scatter, treating each bug as a trial: sqrt(P(1-P) / bugs).
Output: results/fit_curve.png
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from urn import RESULTS, DT, load_logs, pooled_fraction

logs = list(load_logs().values())
end = min(log["time"].iloc[-1] for N, log in logs)  # shortest run
fraction = pooled_fraction(logs, end)
t = np.arange(len(fraction)) * DT


def model(t, k, p):
    return p + (1 - p) * np.exp(-2 * k * t)


(k, p), _ = curve_fit(model, t, fraction, p0=[0.05, 0.5])
P = model(t, k, p)
error = np.sqrt(P * (1 - P) / sum(N for N, log in logs))

plt.plot(t, fraction, label="data")
plt.plot(t, P, label=f"fit: k = {k:.3f} /s, p = {p:.2f}")
plt.fill_between(t, P - error, P + error, alpha=0.3)
plt.xlabel("time since release (s)")
plt.ylabel("fraction on left")
plt.legend()
plt.savefig(RESULTS / "fit_curve.png")
