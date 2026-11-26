#!/bin/sh
# paper.html -> DRAFT PDF on the print host (PRINT_HOST): figcheck then print.mjs
set -e
cd "$(dirname "$0")"
D=2026-11-26-vacuus-solids
H=${PRINT_HOST:?set PRINT_HOST to the print host}
R=${PRINT_DIR:-kaleidohedra-papers}
rsync -a --delete --exclude '*.pdf' ./ $H:$R/$D/
rsync -a ../paper.css ../dicto-logo.png ../print.mjs ../figcheck.mjs $H:$R/
ssh $H "cd ~/$R && node figcheck.mjs $D && LIGHT_DPI=${LIGHT_DPI:-200} node print.mjs $D DRAFT-vacuus-solids.pdf 'Building Out the Centre of the Vacuus' draft"
rsync -a $H:$R/$D/DRAFT-vacuus-solids.pdf ./
