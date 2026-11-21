#!/bin/sh
# paper.html -> DRAFT PDF on compute-host with the house pipeline (number audit first, then figcheck.mjs and print.mjs)
set -e
cd "$(dirname "$0")"
D=2026-11-22-amber-ammann
rsync -a --delete --exclude '*.pdf' ./ compute-host:kaleidohedra-papers/$D/
rsync -a ../paper.css ../dicto-logo.png ../print.mjs ../figcheck.mjs ../edgecheck.py ../edgecheck-allow.txt compute-host:kaleidohedra-papers/
rsync -a --relative --exclude 'logs/runs' --exclude 'data/ammann_*' --exclude '*.png' --exclude '*.pdf' ../../studies/./2026-11-21-amber-ammann compute-host:kres-audit/studies/
ssh compute-host "cd ~/kaleidohedra-papers/$D/scripts && export STUDIES=~/kres-audit/studies && python3 audit.py | tee /dev/stderr | grep -q '^AUDIT OK'"
ssh compute-host "cd ~/kaleidohedra-papers && node figcheck.mjs $D && node print.mjs $D DRAFT-amber-ammann.pdf 'Icosahedral Cores in the 3D Penrose Tiling' draft"
rsync -a compute-host:kaleidohedra-papers/$D/DRAFT-amber-ammann.pdf ./
