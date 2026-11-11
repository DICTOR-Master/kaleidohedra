#!/bin/bash
# Scale-anomalies study: crossref (Pi, network) then the analysis on compute-host (uses ../../2026-10-25-physical-anchors data).
set -e; cd "$(dirname "$0")"
python3 crossref_check.py > /dev/null
rsync -a ../../2026-10-25-scale-anomalies ../../2026-10-25-physical-anchors compute-host:runs/
ssh compute-host 'cd ~/runs/2026-10-25-scale-anomalies/scripts && uptime && nice -n 10 python3 anomalies.py'
rsync -a compute-host:runs/2026-10-25-scale-anomalies/data/ ../data/
