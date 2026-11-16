#!/bin/sh
# Next-version DRAFT of Alicia in Wonderland (Book Ten of The Five Orders of Space) -> PDF on the compute host (house pipeline:
# edgecheck.py, figcheck.mjs, print.mjs with its guards). Remote folder nv-book-queens, so the published book's folder there is not touched.
set -e
cd "$(dirname "$0")"
D=nv-book-queens
PDF=DRAFT-alicia-next.pdf
rsync -a --delete --exclude '*.pdf' --exclude '*.zip' --exclude '__pycache__' ./ compute-host-2:kaleidohedra-papers/$D/
rsync -a ../paper.css ../dicto-logo.png ../print.mjs ../figcheck.mjs ../edgecheck.py ../edgecheck-allow.txt compute-host-2:kaleidohedra-papers/
ssh compute-host-2 "cd ~/kaleidohedra-papers && python3 edgecheck.py $D/figures/ch*/*.png && node figcheck.mjs $D && node print.mjs $D $PDF 'Alicia in Wonderland, next version' draft"
timeout 900 rsync -a --partial compute-host-2:kaleidohedra-papers/$D/$PDF ./
cp $PDF "$HOME/Documents/papers-to-read/$PDF"
