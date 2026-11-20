#!/bin/sh
# paper.html -> DRAFT PDF, printed on compute-host-2 with the house pipeline (print.mjs, figcheck.mjs)
set -e
cd "$(dirname "$0")"
D=queen-stages
rsync -a --delete --exclude '*.pdf' ./ compute-host-2:kaleidohedra-papers/$D/
rsync -a ../paper.css ../dicto-logo.png ../print.mjs ../figcheck.mjs ../edgecheck.py ../edgecheck-allow.txt compute-host-2:kaleidohedra-papers/
ssh compute-host-2 "cd ~/kaleidohedra-papers && node figcheck.mjs $D && node print.mjs $D DRAFT-76-between-the-queens-v2.pdf 'Between the Queens' draft"
rsync -a compute-host-2:kaleidohedra-papers/$D/DRAFT-76-between-the-queens-v2.pdf ./
