"""Step 1: fraction of bugs on the left vs time, every run. Output: results/runs.png"""

import matplotlib.pyplot as plt
from urn import RESULTS, load_logs, n_left_from_log

for name, (N, log) in load_logs().items():
    times, n_left = n_left_from_log(log, N)
    plt.plot(times, n_left / N, label=name)

plt.xlabel("time since release (s)")
plt.ylabel("fraction on left")
plt.legend()
plt.savefig(RESULTS / "runs.png")
