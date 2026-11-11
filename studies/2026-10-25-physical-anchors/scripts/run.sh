#!/bin/bash
# Physical anchors study: parse the saved Shannon pages (Pi), then A (sympy) and B (exact cells) on compute-host.
# B imports lib.py and samples.py from the web-of-bonds study (../../2026-10-25-web-of-bonds/scripts).
# crossref_check.py needs network access (it rewrites ../data/raw/crossref.json).
set -e; cd "$(dirname "$0")"
python3 parse_shannon.py > /dev/null
rsync -a ../../2026-10-25-physical-anchors ../../2026-10-25-web-of-bonds compute-host:runs/
ssh compute-host 'cd ~/runs/2026-10-25-physical-anchors/scripts && uptime && nice -n 10 python3 symbolic.py && nice -n 10 python3 compounds.py'
rsync -a compute-host:runs/2026-10-25-physical-anchors/data/ ../data/
