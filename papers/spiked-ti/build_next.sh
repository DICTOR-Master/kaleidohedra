#!/bin/sh
# paper.html -> DRAFT PDF of Version 4 on compute-host-2 with the house pipeline (figcheck.mjs, print.mjs).
# Remote folder nv-paper-78, so the copy built from research-fig3 is never overwritten.
set -e
H=${BUILD_HOST:-compute-host-2}   # BUILD_HOST=compute-host when the second host cannot be reached
cd "$(dirname "$0")"
D=nv-paper-78
PDF=DRAFT-paper-78-ti-star-v4.pdf
rsync -a --delete --exclude '*.pdf' --exclude '*.zip' ./ $H:kaleidohedra-papers/$D/
rsync -a ../paper.css ../dicto-logo.png ../print.mjs ../figcheck.mjs $H:kaleidohedra-papers/
ssh $H "cd ~/kaleidohedra-papers && (node figcheck.mjs $D || true) && node print.mjs $D $PDF 'TI Star, v4 draft' draft"
rsync -a $H:kaleidohedra-papers/$D/$PDF ./
mkdir -p "$HOME/Documents/papers-to-read/next-versions/papers"
cp $PDF "$HOME/Documents/papers-to-read/next-versions/papers/"
