#!/bin/sh
# paper.html -> DRAFT PDF on the compute host with the house pipeline: the figures (fig_tube.py, 20 exact checks; fig_scenes.py,
# 43 checks; three.js shots; fig_compose.py), the audit of every number against the study data, then edgecheck.py, figcheck.mjs
# and print.mjs. Nothing is computed on this machine. data/sun-faces.npz is cut once from the Sun study's frames (sun_extract.py).
set -e
cd "$(dirname "$0")"
D=2026-11-20-scutoid-tissues
H=compute-host-2
PY=${PY:-python3}   # on the host: a Python 3 with NumPy, SciPy, Matplotlib and Pillow (set PY when running build.sh)
ssh $H "mkdir -p kaleidohedra-papers/$D kaleidohedra-papers/_src-$D/studies"
rsync -a --delete --exclude '*.pdf' ./ $H:kaleidohedra-papers/$D/
rsync -a ../paper.css ../dicto-logo.png ../print.mjs ../figcheck.mjs ../edgecheck.py ../edgecheck-allow.txt $H:kaleidohedra-papers/
# the study files the audit reads (texts and data only)
cd ../../studies
rsync -aR 2026-11-15-tissue-null-models/data/sweep.json 2026-11-15-tissue-null-models/data/sweep.log 2026-11-15-tissue-null-models/THEORY.md \
  2026-11-15-event-logger/README.md 2026-11-15-sun-granulation/README.md 2026-11-15-cosmic-voids/README.md \
  2026-11-15-grains-polycrystals/README.md 2026-11-15-earth-plates/README.md 2026-11-15-atmosphere-seaice/README.md \
  2026-11-17-sun-step-zero/README.md 2026-11-18-sun-net-change/README.md 2026-11-18-sun-net-vs-d/README.md 2026-11-18-sun-lineage/README.md \
  $H:kaleidohedra-papers/_src-$D/studies/
rsync -a ../papers/dicto-concordance/concordance.json $H:kaleidohedra-papers/_src-$D/
cd - >/dev/null
ssh $H "cd ~/kaleidohedra-papers/$D && timeout 200 $PY scripts/fig_tube.py data/fig-tube.json | tail -2 && cd scripts && timeout 200 $PY fig_scenes.py | tail -2"
ssh $H "cd ~/kaleidohedra-papers/$D/scripts && for f in scutoid corners block tube law; do timeout 100 node shots.mjs renders/\$f.html renders/\$f; done"
ssh $H "cd ~/kaleidohedra-papers/$D/scripts && timeout 250 $PY fig_compose.py ../../_src-$D/studies/2026-11-15-tissue-null-models/data/sweep.json | tail -1"
ssh $H "cd ~/kaleidohedra-papers/$D && $PY scripts/audit.py ../_src-$D/studies ../_src-$D/concordance.json > data/audit.log; tail -3 data/audit.log; grep -E 'FAIL|UNMATCHED' data/audit.log || true; tail -1 data/audit.log | grep -q 'FINAL ok' && cd .. && python3 edgecheck.py $D/figures/*.png && node figcheck.mjs $D && node print.mjs $D DRAFT-scutoid-tissues.pdf 'Scutoid Tissues in Space and Time' draft"
rsync -a $H:kaleidohedra-papers/$D/figures $H:kaleidohedra-papers/$D/data ./
# drafts live in papers-to-read, never in git
rsync -a $H:kaleidohedra-papers/$D/DRAFT-scutoid-tissues.pdf ~/Documents/papers-to-read/
