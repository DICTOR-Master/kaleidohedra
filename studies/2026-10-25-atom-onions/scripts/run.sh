#!/bin/bash
# atom-onions study: C (app dump + float check) on the Pi, where ~/k-dshells (branch dictonic-shells) lives; the exact part, the
# geometry, the Blender renders and the figures on dicto-big-brother (~/geom/bin/python: sympy, numpy, scipy, matplotlib; blender 5.0.1).
# Needs the sibling study 2026-10-25-web-of-bonds (its lib.py and samples.py are imported). Wait for uptime load < 6 between renders.
set -e; cd "$(dirname "$0")"
node --import ./reg.mjs app_dump.mjs > ../data/raw/app-dump.json && python3 check_app.py
python3 geom.py
rsync -a ../../2026-10-25-web-of-bonds ../../2026-10-25-atom-onions dicto-big-brother:runs/studies/
scp -q ~/k-research/papers/dicto-logo.png dicto-big-brother:runs/studies/dicto-logo.png
ssh dicto-big-brother 'cd ~/runs/studies/2026-10-25-atom-onions && nice -n 10 ~/geom/bin/python scripts/onions_exact.py > /dev/null && mkdir -p renders &&
  for k in golden-onion delian-tet-onion delian-oct-onion golden-meshing delian-meshing; do
    nice -n 10 blender -b -P scripts/blender_render.py -- data/raw/scene-$k.json renders/$k.png renders/$k.json 1400 > /dev/null; done &&
  cd scripts && ONION_LOGO=~/runs/studies/dicto-logo.png ONION_READ=~/runs/studies/atom-onions-read nice -n 10 ~/geom/bin/python compose.py'
rsync -a dicto-big-brother:runs/studies/2026-10-25-atom-onions/{data,renders,figures} ../
cp ../figures/fig*.png ~/Documents/papers-to-read/atom-onions/
