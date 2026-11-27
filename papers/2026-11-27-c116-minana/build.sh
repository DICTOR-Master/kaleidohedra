#!/bin/sh
# paper.html -> DRAFT PDF on the print host (PRINT_HOST): figcheck then print.mjs
set -e
cd "$(dirname "$0")"
D=2026-11-27-c116-minana
H=${PRINT_HOST:?set PRINT_HOST to the print host}
R=${PRINT_DIR:-kaleidohedra-papers}
rsync -a --delete --exclude '*.pdf' ./ $H:$R/$D/
rsync -a ../paper.css ../dicto-logo.png ../print.mjs ../figcheck.mjs $H:$R/
ssh $H "cd ~/$R && node figcheck.mjs $D && LIGHT_DPI=${LIGHT_DPI:-200} node print.mjs $D DRAFT-c116-minana.pdf 'From a Fullerene to a Fair Die' draft"
rsync -a $H:$R/$D/DRAFT-c116-minana.pdf ./
