#!/bin/sh
# paper.html -> PLAN PDF on compute-host-2 with the house pipeline (print.mjs)
set -e
cd "$(dirname "$0")"
D=plan-fable-handoff
rsync -a --delete --exclude '*.pdf' ./ compute-host-2:kaleidohedra-papers/$D/
rsync -a ../paper.css ../dicto-logo.png ../print.mjs ../figcheck.mjs compute-host-2:kaleidohedra-papers/
ssh compute-host-2 "cd ~/kaleidohedra-papers && node print.mjs $D PLAN-fable-handoff.pdf 'Implementation plan: the Fable handoff' draft"
rsync -a compute-host-2:kaleidohedra-papers/$D/PLAN-fable-handoff.pdf ./
