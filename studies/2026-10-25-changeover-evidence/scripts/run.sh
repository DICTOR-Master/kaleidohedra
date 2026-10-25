#!/bin/bash
# Changeover evidence study: geometry (sympy) and compound placements on dicto-big-brother; crossref check on the Pi (network).
# geometry.py imports ../../2026-10-25-relay-census/scripts/networks.py and reads its relay-summary.json.
set -e; cd "$(dirname "$0")"
python3 parse_shannon.py > /dev/null
ssh dicto-big-brother 'mkdir -p ~/runs'
rsync -a ../../2026-10-25-changeover-evidence ../../2026-10-25-relay-census dicto-big-brother:runs/
ssh dicto-big-brother 'uptime; cd ~/runs/2026-10-25-changeover-evidence/scripts && nice -n 10 ~/geom/bin/python geometry.py && nice -n 10 ~/geom/bin/python compounds.py'
rsync -a dicto-big-brother:runs/2026-10-25-changeover-evidence/data/ ../data/
