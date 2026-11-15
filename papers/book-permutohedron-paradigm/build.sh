#!/bin/sh
# Assemble the book and print the PDF on compute-host-2 with the house pipeline (figcheck.mjs, then print.mjs)
set -e
cd "$(dirname "$0")"
python3 assemble.py
D=book-permutohedron-paradigm
rsync -a --delete --exclude '*.pdf' --exclude figures-fixed ./ compute-host-2:kaleidohedra-papers/$D/
rsync -a ../paper.css ../dicto-logo.png ../print.mjs ../figcheck.mjs compute-host-2:kaleidohedra-papers/
ssh compute-host-2 "cd ~/kaleidohedra-papers && node figcheck.mjs $D && node print.mjs $D dicto-permutohedron-paradigm.pdf 'The Permutohedron Paradigm' 10.5281/zenodo.24239019 1"
rsync -a compute-host-2:kaleidohedra-papers/$D/dicto-permutohedron-paradigm.pdf ./
