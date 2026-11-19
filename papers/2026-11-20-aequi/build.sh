#!/bin/sh
# paper.html -> DRAFT PDF on compute-host-2 with the house pipeline (Figure 1, Table 3 and the number audit first, then edgecheck, figcheck.mjs and print.mjs)
set -e
cd "$(dirname "$0")"
D=2026-11-20-aequi
rsync -a --delete --exclude '*.pdf' ./ compute-host-2:kaleidohedra-papers/$D/
rsync -a ../paper.css ../dicto-logo.png ../print.mjs ../figcheck.mjs ../edgecheck.py ../edgecheck-allow.txt compute-host-2:kaleidohedra-papers/
rsync -a --relative --exclude 'figures/' --exclude 'data/figures/' --exclude 'data/raw/' ../../studies/./2026-11-19-aequi-complete ../../studies/./2026-11-20-aequi-alexandrov ../../studies/./2026-11-20-aequi-catalogue ../../studies/./2026-11-20-aequi-two-placements compute-host-2:kres-audit/studies/
ssh compute-host-2 "cd ~/kaleidohedra-papers/$D/scripts && python3 fig_polar.py && STUDIES=~/kres-audit/studies python3 make_table.py && STUDIES=~/kres-audit/studies python3 audit.py | tee /dev/stderr | grep -q '^AUDIT OK'"
ssh compute-host-2 "cd ~/kaleidohedra-papers && python3 edgecheck.py $D/figures/*.png && node figcheck.mjs $D && node print.mjs $D DRAFT-aequi-enumerating-the-innumerable.pdf 'Fair Dice — The Aequi' draft"
rsync -a compute-host-2:kaleidohedra-papers/$D/DRAFT-aequi-enumerating-the-innumerable.pdf compute-host-2:kaleidohedra-papers/$D/paper.html ./
rsync -a compute-host-2:kaleidohedra-papers/$D/figures/fig-polar.svg ./figures/
