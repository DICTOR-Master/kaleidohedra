#!/bin/sh
# pattern/paper.html -> HexOct-crochet-pattern.pdf on the print host with the house pipeline (edge guard, figcheck, print.mjs).
# Figures and core templates come from make_pattern.py (run on the compute host: python3 make_pattern.py <hex scripts> <mark>).
set -e
cd "$(dirname "$0")"
cp ../fig/block-4H.png fig/
D=hexoct-crochet-pattern; H=compute-host-2
rsync -a --delete --exclude '*.pdf' --exclude '*.py' --exclude build.sh --exclude data ./ $H:kaleidohedra-papers/$D/
rsync -a ../../../papers/paper.css ../../../papers/dicto-logo.png ../../../papers/print.mjs ../../../papers/figcheck.mjs ../../../papers/edgecheck.py ../../../papers/edgecheck-allow.txt $H:kaleidohedra-papers/
ssh $H "cd ~/kaleidohedra-papers && python3 edgecheck.py $D/fig/*.png && node figcheck.mjs $D && node print.mjs $D HexOct-crochet-pattern.pdf 'HexOct crochet pattern' draft"
rsync -a $H:kaleidohedra-papers/$D/HexOct-crochet-pattern.pdf ./
