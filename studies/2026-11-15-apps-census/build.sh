#!/bin/sh
# data/census.json + the wizard code -> paper/paper.html -> DRAFT PDF on the compute host with the house pipeline (figcheck, print.mjs)
# Usage: sh build.sh <path to the Kaleidohedra repo's src/app/dimension-wizard.js>
set -e
cd "$(dirname "$0")"
python3 scripts/make_html.py "$1"
D=apps-census
rsync -a --delete --exclude '*.pdf' paper/ compute-host-2:kaleidohedra-papers/$D/
rsync -a ../../papers/paper.css ../../papers/dicto-logo.png ../../papers/print.mjs ../../papers/figcheck.mjs ../../papers/edgecheck.py ../../papers/edgecheck-allow.txt compute-host-2:kaleidohedra-papers/
ssh compute-host-2 "cd ~/kaleidohedra-papers && node figcheck.mjs $D && node print.mjs $D DRAFT-apps-five-orders-census.pdf 'Apps and The Five Orders of Space' draft"
rsync -a compute-host-2:kaleidohedra-papers/$D/DRAFT-apps-five-orders-census.pdf paper/
