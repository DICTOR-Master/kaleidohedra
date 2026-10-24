#!/bin/bash
# Physical anchors study: parse the saved Shannon pages (Pi), then A (sympy) and B (exact cells) on dicto-big-brother.
# B imports lib.py and samples.py from the web-of-bonds study (../../2026-10-25-web-of-bonds/scripts).
# crossref_check.py needs network access (it rewrites ../data/raw/crossref.json).
set -e; cd "$(dirname "$0")"
python3 parse_shannon.py > /dev/null
rsync -a ../../2026-10-25-physical-anchors ../../2026-10-25-web-of-bonds dicto-big-brother:runs/
ssh dicto-big-brother 'cd ~/runs/2026-10-25-physical-anchors/scripts && uptime && nice -n 10 ~/geom/bin/python symbolic.py && nice -n 10 ~/geom/bin/python compounds.py'
rsync -a dicto-big-brother:runs/2026-10-25-physical-anchors/data/ ../data/
