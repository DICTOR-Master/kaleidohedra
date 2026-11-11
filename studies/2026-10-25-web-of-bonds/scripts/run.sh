#!/bin/bash
# web-of-bonds study: A (symbolic) and B (exact samples) on compute-host (python3: sympy, numpy, scipy);
# C (app dump + float cross-check) on the Pi, where the app checkout ~/k-dshells (branch dictonic-shells) lives.
set -e; cd "$(dirname "$0")"
node --import ./reg.mjs app_dump.mjs > ../data/raw/app-dump.json
python3 check_app.py
rsync -a ../ compute-host:runs/web-of-bonds/
ssh compute-host 'cd ~/runs/web-of-bonds/scripts && uptime && nice -n 10 python3 symbolic.py && nice -n 10 python3 samples.py'
rsync -a compute-host:runs/web-of-bonds/data/ ../data/
