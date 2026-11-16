#!/bin/sh
# paper.html -> DRAFT PDF on compute-host-2 with the house pipeline (print.mjs)
set -e
cd "$(dirname "$0")"
D=plan-alicia-v2
rsync -a --delete --exclude '*.pdf' ./ compute-host-2:kaleidohedra-papers/$D/
rsync -a ../paper.css ../dicto-logo.png ../print.mjs ../figcheck.mjs ../edgecheck.py ../edgecheck-allow.txt compute-host-2:kaleidohedra-papers/
ssh compute-host-2 "cd ~/kaleidohedra-papers && node print.mjs $D DRAFT-plan-alicia-v2.pdf 'Plan: Alicia in Wonderland, next version' draft"
rsync -a compute-host-2:kaleidohedra-papers/$D/DRAFT-plan-alicia-v2.pdf ./
