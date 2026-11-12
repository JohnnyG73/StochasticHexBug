#!/bin/sh
# One-time setup: makes a private Python environment in .venv with the packages in requirements.txt.
# Usage: sh setup.sh
# Then, in each new terminal: source .venv/bin/activate

set -e  # stop at the first error

python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt

echo "Done. Now run: source .venv/bin/activate"
