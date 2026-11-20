#!/bin/sh
# paper.html -> DRAFT PDF on the compute host with the house pipeline: edgecheck.py on the figures, figcheck.mjs, print.mjs.
# The figures are copied unchanged from the source papers and study (see Appendix B); nothing is computed on this machine.
set -e
cd "$(dirname "$0")"
D=dossier-mathematicians
H=compute-host
ssh $H "mkdir -p kaleidohedra-papers/$D"
rsync -a --delete --exclude '*.pdf' ./ $H:kaleidohedra-papers/$D/
rsync -a ../paper.css ../dicto-logo.png ../print.mjs ../figcheck.mjs ../edgecheck.py ../edgecheck-allow.txt $H:kaleidohedra-papers/
ssh $H "cd ~/kaleidohedra-papers && timeout 60 python3 edgecheck.py $D/figures/*.png && timeout 120 node figcheck.mjs $D && timeout 120 node print.mjs $D DRAFT-dossier-mathematicians.pdf 'DICTO: Selected Results' draft"
# drafts live in papers-to-read, never in git
rsync -a $H:kaleidohedra-papers/$D/DRAFT-dossier-mathematicians.pdf ~/Documents/papers-to-read/
