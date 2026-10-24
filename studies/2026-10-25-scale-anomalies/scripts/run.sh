#!/bin/bash
# Scale-anomalies study: crossref (Pi, network) then the analysis on dicto-big-brother (uses ../../2026-10-25-physical-anchors data).
set -e; cd "$(dirname "$0")"
python3 crossref_check.py > /dev/null
rsync -a ../../2026-10-25-scale-anomalies ../../2026-10-25-physical-anchors dicto-big-brother:runs/
ssh dicto-big-brother 'cd ~/runs/2026-10-25-scale-anomalies/scripts && uptime && nice -n 10 ~/geom/bin/python anomalies.py'
rsync -a dicto-big-brother:runs/2026-10-25-scale-anomalies/data/ ../data/
