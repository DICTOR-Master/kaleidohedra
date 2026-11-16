#!/bin/sh
# paper.html -> DRAFT PDF on compute-host-2 with the house pipeline (checks and figures first, then figcheck.mjs and print.mjs)
set -e
cd "$(dirname "$0")"
D=2026-11-16-walls-of-silence
rsync -a --delete --exclude '*.pdf' ./ compute-host-2:kaleidohedra-papers/$D/
rsync -a ../paper.css ../dicto-logo.png ../print.mjs ../figcheck.mjs ../edgecheck.py ../edgecheck-allow.txt compute-host-2:kaleidohedra-papers/
ssh compute-host-2 "cd ~/kaleidohedra-papers && python3 edgecheck.py $D/figures/*.png && node figcheck.mjs $D && node print.mjs $D DRAFT-walls-of-silence.pdf 'Walls of Silence' draft"
rsync -a compute-host-2:kaleidohedra-papers/$D/DRAFT-walls-of-silence.pdf ./
