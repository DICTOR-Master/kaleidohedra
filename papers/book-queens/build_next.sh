#!/bin/sh
# Next-version DRAFT of Alicia in Wonderland (Book Ten of The Five Orders of Space) -> PDF on compute-host-2 (print.mjs).
# Remote folder nv-book-queens, so the published book's folder there is not touched.
set -e
cd "$(dirname "$0")"
D=nv-book-queens
PDF=DRAFT-book-queens-v6.pdf
rsync -a --delete --exclude '*.pdf' --exclude '*.zip' ./ compute-host-2:kaleidohedra-papers/$D/
rsync -a ../paper.css ../dicto-logo.png ../print.mjs ../figcheck.mjs compute-host-2:kaleidohedra-papers/
ssh compute-host-2 "cd ~/kaleidohedra-papers && (node figcheck.mjs $D || true) && node print.mjs $D $PDF 'Alicia in Wonderland, v6 draft' draft"
timeout 900 rsync -a --partial compute-host-2:kaleidohedra-papers/$D/$PDF ./
mkdir -p "$HOME/Documents/papers-to-read/next-versions"
cp $PDF "$HOME/Documents/papers-to-read/next-versions/"
