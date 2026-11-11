#!/bin/bash
# Changeover evidence study: geometry (sympy) and compound placements on compute-host; crossref check on the Pi (network).
# geometry.py imports ../../2026-10-25-relay-census/scripts/networks.py and reads its relay-summary.json.
set -e; cd "$(dirname "$0")"
python3 parse_shannon.py > /dev/null
ssh compute-host 'mkdir -p ~/runs'
rsync -a ../../2026-10-25-changeover-evidence ../../2026-10-25-relay-census compute-host:runs/
ssh compute-host 'uptime; cd ~/runs/2026-10-25-changeover-evidence/scripts && nice -n 10 python3 geometry.py && nice -n 10 python3 compounds.py'
rsync -a compute-host:runs/2026-10-25-changeover-evidence/data/ ../data/
