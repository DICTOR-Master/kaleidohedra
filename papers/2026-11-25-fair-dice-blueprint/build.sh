#!/bin/sh
# paper.html -> DRAFT PDF on compute-host with the house pipeline (statement audit first, then figcheck.mjs and print.mjs)
set -e
cd "$(dirname "$0")"
D=2026-11-25-fair-dice-blueprint
rsync -a --delete --exclude '*.pdf' ./ compute-host:kaleidohedra-papers/$D/
rsync -a ../paper.css ../dicto-logo.png ../print.mjs ../figcheck.mjs ../edgecheck.py ../edgecheck-allow.txt compute-host:kaleidohedra-papers/
ssh compute-host "cd ~/kaleidohedra-papers && node figcheck.mjs $D && node print.mjs $D DRAFT-fair-dice-blueprint.pdf 'Fair Dice from Curvature' draft"
rsync -a compute-host:kaleidohedra-papers/$D/DRAFT-fair-dice-blueprint.pdf ./
