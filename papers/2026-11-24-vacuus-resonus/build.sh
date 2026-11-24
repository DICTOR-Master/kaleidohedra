#!/bin/sh
# paper.src.html -> paper.html (catalogue figure + Appendix A from the catalogue CSV), then figcheck and the DRAFT print on the print host (PRINT_HOST)
set -e
cd "$(dirname "$0")"
python3 scripts/make_parts.py
D=2026-11-24-vacuus-resonus
H=${PRINT_HOST:?set PRINT_HOST to the print host}
R=${PRINT_DIR:-kaleidohedra-papers}
rsync -a --delete --exclude '*.pdf' ./ $H:$R/$D/
rsync -a ../paper.css ../dicto-logo.png ../print.mjs ../figcheck.mjs $H:$R/
ssh $H "cd ~/$R && node figcheck.mjs $D && node print.mjs $D DRAFT-vacuus-resonus-v0.pdf 'The Vacuus and the Resonus' draft"
rsync -a $H:$R/$D/DRAFT-vacuus-resonus-v0.pdf ./
