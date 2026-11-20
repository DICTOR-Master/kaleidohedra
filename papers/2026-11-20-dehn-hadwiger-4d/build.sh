#!/bin/sh
# paper.html -> DRAFT PDF on compute-host with the house pipeline (exact checks, figures and number audit first, then edgecheck, figcheck.mjs and print.mjs)
set -e
cd "$(dirname "$0")"
D=2026-11-20-dehn-hadwiger-4d
PY="${GEOM_PY:-python3}"   # the host's geometry Python with numpy, scipy, matplotlib and PIL (set GEOM_PY)
rsync -a --delete --exclude '*.pdf' --exclude renders ./ compute-host:kaleidohedra-papers/$D/
rsync -a ../paper.css ../dicto-logo.png ../print.mjs ../figcheck.mjs ../edgecheck.py ../edgecheck-allow.txt compute-host:kaleidohedra-papers/
rsync -a --relative ../../studies/./2026-11-20-palomar-dehn4d ../../studies/./2026-11-20-600cell-5cell-zero ../../studies/./2026-11-20-palomar-next-prescore compute-host:kres-audit/studies/
ssh compute-host "cd ~/kaleidohedra-papers/$D/scripts && export STUDIES=~/kres-audit/studies && $PY fig_scenes.py && for f in six caps; do node shots.mjs renders/\$f.html renders/\$f; done && $PY fig_angles.py && $PY fig_compose.py && $PY audit.py | tee /dev/stderr | grep -q '^AUDIT OK'"
ssh compute-host "cd ~/kaleidohedra-papers && python3 edgecheck.py $D/figures/*.png && node figcheck.mjs $D && node print.mjs $D DRAFT-dehn-hadwiger-4d.pdf 'Dehn–Hadwiger 4D' draft"
rsync -a compute-host:kaleidohedra-papers/$D/DRAFT-dehn-hadwiger-4d.pdf compute-host:kaleidohedra-papers/$D/figures compute-host:kaleidohedra-papers/$D/data ./
