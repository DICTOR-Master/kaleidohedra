#!/bin/bash
# Plan-B cover of The Platonic Solids: the nest in its cube of the octet (packing_cover.py) composed with the series lettering
# (compose_planb.py). Run from this folder (PY = the Python with numpy, scipy, Pillow).
set -o pipefail
cd "$(dirname "$0")"
${PY:-python3} packing_cover.py ../data/packing-cover.png 2400 2200 | tee ../data/packing-cover.log | tail -1 | grep -q '^FINAL ok' || { echo "FINAL FAIL: picture"; exit 1; }
${PY:-python3} compose_planb.py ../data/packing-cover.png ../platonic-cover-planB.png
