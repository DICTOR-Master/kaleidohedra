#!/bin/sh
# data/results.json -> paper/paper.html -> DRAFT PDF on the print host with the house pipeline (figcheck, print.mjs guards)
# Usage: sh build.sh
set -e
cd "$(dirname "$0")"
python3 scripts/make_html.py
D=scutoid-interactions
rsync -a --delete --exclude '*.pdf' paper/ compute-host-2:kaleidohedra-papers/$D/
rsync -a ../../papers/paper.css ../../papers/dicto-logo.png ../../papers/print.mjs ../../papers/figcheck.mjs ../../papers/edgecheck.py ../../papers/edgecheck-allow.txt compute-host-2:kaleidohedra-papers/
ssh compute-host-2 "cd kaleidohedra-papers && node figcheck.mjs $D && node print.mjs $D DRAFT-scutoid-interactions.pdf 'Microcosm and Macrocosm' draft"
rsync -a compute-host-2:kaleidohedra-papers/$D/DRAFT-scutoid-interactions.pdf paper/
