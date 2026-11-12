"""Step 2: crossing rate per bug, k = crossings / bug-seconds, for each run. Output: results/rates.csv, rates.png"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from urn import RESULTS, load_logs, count_k

logs = load_logs()

rows = [{"run": name, "N": N, "crossings": len(log), "k": count_k([(N, log)])} for name, (N, log) in logs.items()]
rates = pd.DataFrame(rows)
rates["k_err"] = rates["k"] / np.sqrt(rates["crossings"])  # counting error
rates.to_csv(RESULTS / "rates.csv", index=False)

plt.errorbar(rates["N"], rates["k"], yerr=rates["k_err"], fmt="o")
plt.axhline(count_k(logs.values()), color="gray")  # all runs together
plt.xlabel("N")
plt.ylabel("k (1/s)")
plt.savefig(RESULTS / "rates.png")
