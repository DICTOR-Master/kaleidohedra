#!/bin/sh
# paper.html -> DRAFT PDF, printed on compute-host-2 with the house pipeline (print.mjs, figcheck.mjs)
set -e
cd "$(dirname "$0")"
D=2026-11-12-geometry-gives-laws
rsync -a --delete --exclude '*.pdf' ./ compute-host-2:kaleidohedra-papers/$D/
rsync -a ../paper.css ../dicto-logo.png ../print.mjs ../figcheck.mjs compute-host-2:kaleidohedra-papers/
ssh compute-host-2 "cd ~/kaleidohedra-papers && node figcheck.mjs $D && node print.mjs $D DRAFT-geometry-gives-laws.pdf 'Geometry Gives Laws' draft"
rsync -a compute-host-2:kaleidohedra-papers/$D/DRAFT-geometry-gives-laws.pdf ./
