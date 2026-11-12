#!/bin/sh
# paper.html -> DRAFT PDF, printed on compute-host-2 with the house pipeline (figcheck.mjs, then print.mjs)
set -e
cd "$(dirname "$0")"
D=paradigm-ch13
rsync -a --delete --exclude '*.pdf' --exclude build.sh ./ compute-host-2:kaleidohedra-papers/$D/
rsync -a ../paper.css ../dicto-logo.png ../print.mjs ../figcheck.mjs compute-host-2:kaleidohedra-papers/
ssh compute-host-2 "cd ~/kaleidohedra-papers && node figcheck.mjs $D && node print.mjs $D DRAFT-paradigm-ch13-change-ringing.pdf 'Change, Rhythm, Harmony' draft"
rsync -a compute-host-2:kaleidohedra-papers/$D/DRAFT-paradigm-ch13-change-ringing.pdf ./
