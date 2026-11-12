#!/bin/sh
# paper.html -> DRAFT PDF, printed on compute-host-2 with the house pipeline (figcheck.mjs, then print.mjs), through the job gate
set -e
cd "$(dirname "$0")"
D=2026-11-12-permutohedron-family
rsync -a --delete --exclude '*.pdf' ./ compute-host-2:kaleidohedra-papers/$D/
rsync -a ../paper.css ../dicto-logo.png ../print.mjs ../figcheck.mjs compute-host-2:kaleidohedra-papers/
JOBHOST=dicto-node "$HOME/dicto-alerts/dbbjob.sh" gperm-pdf 0.2 "cd ~/kaleidohedra-papers && node figcheck.mjs $D && node print.mjs $D DRAFT-permutohedron-family.pdf 'The Permutohedron Family' draft && echo FINAL ok"
rsync -a compute-host-2:kaleidohedra-papers/$D/DRAFT-permutohedron-family.pdf ./
