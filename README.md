# StochasticHexBug
Phys 2210 Lab: Hexbugs spreading between two chambers, compared to the Ehrenfest urn model.

## Setup
```
sh setup.sh                  # once: makes .venv with the packages in requirements.txt
source .venv/bin/activate    # every new terminal
```

## Run
From this folder, e.g. `python analysis/rates.py`. Each script saves its output to `results/`.

## Files
- `data/crossings/N{N}_run{R}.csv`: hand-logged crossings (`time,direction`, time from release, all bugs start left)
- `analysis/urn.py`: shared functions used by the scripts below (not run on its own)
- `analysis/plot_runs.py`: fraction of bugs on the left vs time for every run
- `analysis/rates.py`: crossing rate per bug, k, for each run by counting
- `analysis/fit_curve.py`: fits the exponential to all runs pooled together
- `analysis/steady_state.py`: compares the settled counts to the binomial
- `analysis/monte_carlo.py`: fake experiments from the urn model, for error bars on k and the paths plot
- `analysis/clean.py`, `data/bugs_*.csv`: earlier tracker data from the first experiment
