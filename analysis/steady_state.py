"""Step 4: after settling, how often each n_L occurs, vs the binomial Bin(N, 1/2). Output: results/steady_state.png"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom
from urn import RESULTS, load_logs, settled_counts

logs = list(load_logs().values())
Ns = sorted({N for N, log in logs})

fig, axes = plt.subplots(1, len(Ns), figsize=(3 * len(Ns), 3))
for ax, N in zip(axes, Ns):
    values = settled_counts(logs, N)
    n = np.arange(N + 1)
    ax.bar(n, [np.mean(values == i) for i in n], label="data")
    ax.plot(n, binom.pmf(n, N, 0.5), "ko", label="binomial")
    ax.set_title(f"N = {N}")

axes[0].legend()
fig.savefig(RESULTS / "steady_state.png")
