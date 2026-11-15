#!/bin/bash
# Pilot of the yew / conifer cambium stream: synthetic controls + all 300 CoLuS patches (image and manual-mask modes).
# Ends with FINAL ok only if every check in pilot_batch.py passes. PY: a Python with numpy, scipy, scikit-image, Pillow.
S=$(cd "$(dirname "$0")/.." && pwd); PY=${PY:-python3}
cd $S || exit 1
mkdir -p results/pilot
$PY -I scripts/pilot_batch.py data/raw/colus/x/CoLuS_Dataset results/pilot 300 16 | tee results/pilot/pilot.log | grep -E "PROGRESS|CHECK|PILOT" ; grep -q '^PILOT_OK' results/pilot/pilot.log && echo "FINAL ok" || echo "FINAL FAIL"
