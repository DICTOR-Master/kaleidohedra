#!/bin/sh
# paper.html -> OVERVIEW.pdf of the paper next versions, on compute-host-2 with print.mjs (draft, status box).
set -e
H=${BUILD_HOST:-compute-host-2}
cd "$(dirname "$0")"
D=nv-overview-papers
PDF=DRAFT-OVERVIEW.pdf
rsync -a --delete --exclude '*.pdf' ./ $H:kaleidohedra-papers/$D/
rsync -a ../paper.css ../dicto-logo.png ../print.mjs $H:kaleidohedra-papers/
ssh $H "cd ~/kaleidohedra-papers && node print.mjs $D $PDF 'Next versions of seven papers: overview' draft"
rsync -a $H:kaleidohedra-papers/$D/$PDF ./
mkdir -p "$HOME/Documents/papers-to-read/next-versions/papers"
cp $PDF "$HOME/Documents/papers-to-read/next-versions/papers/OVERVIEW.pdf"
