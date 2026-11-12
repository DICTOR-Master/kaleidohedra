#!/bin/sh
# paper.html -> DRAFT PDF on compute-host-2 with the house pipeline (checks and figures first, then figcheck.mjs and print.mjs)
set -e
cd "$(dirname "$0")"
D=2026-11-13-turn-law
rsync -a --delete --exclude '*.pdf' ./ compute-host-2:kaleidohedra-papers/$D/
rsync -a ../paper.css ../dicto-logo.png ../print.mjs ../figcheck.mjs compute-host-2:kaleidohedra-papers/
ssh compute-host-2 "cd ~/kaleidohedra-papers && node figcheck.mjs $D && node print.mjs $D DRAFT-turn-law.pdf 'The Turn Law' draft"
rsync -a compute-host-2:kaleidohedra-papers/$D/DRAFT-turn-law.pdf ./
