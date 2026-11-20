#!/bin/sh
# paper.html -> DRAFT PDF on compute-host with the house pipeline (exact checks, figures and number audit first, then edgecheck, figcheck.mjs and print.mjs)
set -e
cd "$(dirname "$0")"
D=2026-11-20-grunbaum-k10
PY="${GEOM_PY:-python3}"   # the host's geometry Python (set GEOM_PY)
rsync -a --delete --exclude '*.pdf' ./ compute-host:kaleidohedra-papers/$D/
rsync -a ../paper.css ../dicto-logo.png ../print.mjs ../figcheck.mjs ../edgecheck.py ../edgecheck-allow.txt compute-host:kaleidohedra-papers/
rsync -a --relative ../../studies/./2026-11-15-grunbaum-k10 ../../studies/./2026-11-20-hall-2016-check ../../studies/./2026-11-20-palomar-grunbaum ../../studies/./2026-11-17-get-mixing/README.md ../../studies/./2026-11-17-inchbald-check/README.md ../../studies/./2026-11-15-echo-shapes/README.md compute-host:kres-audit/studies/
ssh compute-host "cd ~/kaleidohedra-papers/$D/scripts && export STUDIES=~/kres-audit/studies && $PY get_exact.py && $PY fig_scenes.py && for f in tri apart zones tiling; do node shots.mjs renders/\$f.html renders/\$f; done && $PY fig_compose.py && $PY audit.py | tee /dev/stderr | grep -q '^AUDIT OK'"
ssh compute-host "cd ~/kaleidohedra-papers && python3 edgecheck.py $D/figures/*.png && node figcheck.mjs $D && node print.mjs $D DRAFT-grunbaum-k10.pdf 'Ten Faces in Every Zone' draft"
rsync -a compute-host:kaleidohedra-papers/$D/DRAFT-grunbaum-k10.pdf compute-host:kaleidohedra-papers/$D/figures compute-host:kaleidohedra-papers/$D/data ./
