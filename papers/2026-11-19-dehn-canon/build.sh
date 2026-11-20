#!/bin/sh
# paper.html -> DRAFT PDF on compute-host with the house pipeline (figures and number audit first, then edgecheck, figcheck.mjs and print.mjs)
set -e
cd "$(dirname "$0")"
D=2026-11-19-dehn-canon
PY="${GEOM_PY:-python3}"   # the host's geometry Python (set GEOM_PY)
rsync -a --delete --exclude '*.pdf' ./ compute-host:kaleidohedra-papers/$D/
rsync -a ../paper.css ../dicto-logo.png ../print.mjs ../figcheck.mjs ../edgecheck.py ../edgecheck-allow.txt compute-host:kaleidohedra-papers/
rsync -a --relative ../../studies/./2026-11-19-lean-dehn-1 ../../studies/./2026-11-19-lean-dehn-2 ../../studies/./2026-11-19-lean-dehn-3 ../../studies/./2026-11-19-lean-dehn-4 ../../studies/./2026-11-19-lean-dehn-5 ../../studies/./2026-11-19-lean-dehn-6 ../../studies/./2026-11-19-lean-dehn-7 ../../studies/./2026-11-19-lean-dehn-8 ../../studies/./2026-11-19-lean-dehn-9 ../../studies/./2026-11-19-lean-dehn-10 ../../studies/./2026-11-19-dehn-atoms/README.md compute-host:kres-audit/studies/
ssh compute-host "cd ~/kaleidohedra-papers/$D/scripts && $PY fig_wedge.py && $PY fig_canon.py && $PY fig_scenes.py && $PY fig_pieces.py && for f in canon pairs line words pieces; do node shots.mjs renders/\$f.html renders/\$f; done && $PY fig_compose.py && STUDIES=~/kres-audit/studies $PY audit.py | tee /dev/stderr | grep -q '^AUDIT OK'"
ssh compute-host "cd ~/kaleidohedra-papers && python3 edgecheck.py $D/figures/*.png && node figcheck.mjs $D && node print.mjs $D DRAFT-dehn-canon.pdf 'Dehn Canon' draft"
rsync -a compute-host:kaleidohedra-papers/$D/DRAFT-dehn-canon.pdf compute-host:kaleidohedra-papers/$D/figures ./
