#!/bin/sh
# plan/paper.html -> DRAFT PDF on the print host with the house pipeline (figcheck first, then print.mjs)
set -e
cd "$(dirname "$0")"
mkdir -p plan/fig && cp fig/*.png plan/fig/
D=hexoct-crochet-plan
rsync -a --delete --exclude '*.pdf' plan/ compute-host-2:kaleidohedra-papers/$D/
rsync -a ../../papers/paper.css ../../papers/dicto-logo.png ../../papers/print.mjs ../../papers/figcheck.mjs ../../papers/edgecheck.py ../../papers/edgecheck-allow.txt compute-host-2:kaleidohedra-papers/
ssh compute-host-2 "cd ~/kaleidohedra-papers && node figcheck.mjs $D && node print.mjs $D DRAFT-hexoct-crochet-plan.pdf 'HexOct in Crochet' draft"
rsync -a compute-host-2:kaleidohedra-papers/$D/DRAFT-hexoct-crochet-plan.pdf plan/
