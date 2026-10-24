#!/bin/bash
# web-of-bonds study: A (symbolic) and B (exact samples) on dicto-big-brother (~/geom/bin/python: sympy, numpy, scipy);
# C (app dump + float cross-check) on the Pi, where the app checkout ~/k-dshells (branch dictonic-shells) lives.
set -e; cd "$(dirname "$0")"
node --import ./reg.mjs app_dump.mjs > ../data/raw/app-dump.json
python3 check_app.py
rsync -a ../ dicto-big-brother:runs/web-of-bonds/
ssh dicto-big-brother 'cd ~/runs/web-of-bonds/scripts && uptime && nice -n 10 ~/geom/bin/python symbolic.py && nice -n 10 ~/geom/bin/python samples.py'
rsync -a dicto-big-brother:runs/web-of-bonds/data/ ../data/
