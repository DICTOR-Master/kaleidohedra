#!/bin/bash
# Reruns the bond-physics study. Part G is the heavier one (about 155 s on dicto-big-brother): run it there with nice -n 10.
set -e
cd "$(dirname "$0")"
nice -n 10 python3 geom.py      # needs ../../2026-10-25-web-of-bonds/scripts and ../../2026-10-25-physical-anchors/data/raw/compounds.json
python3 links.py
python3 crossref_check.py > /dev/null
