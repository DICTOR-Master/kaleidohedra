#!/bin/sh
# Assemble the book and print the DRAFT PDF on compute-host-2 with the house pipeline (figcheck.mjs, then print.mjs)
set -e
cd "$(dirname "$0")"
python3 assemble.py
D=book-permutohedron-paradigm
rsync -a --delete --exclude '*.pdf' --exclude figures-fixed ./ compute-host-2:kaleidohedra-papers/$D/
rsync -a ../paper.css ../dicto-logo.png ../print.mjs ../figcheck.mjs compute-host-2:kaleidohedra-papers/
ssh compute-host-2 "cd ~/kaleidohedra-papers && node figcheck.mjs $D && node print.mjs $D DRAFT-permutohedron-paradigm-book.pdf 'The Permutohedron Paradigm' draft"
rsync -a compute-host-2:kaleidohedra-papers/$D/DRAFT-permutohedron-paradigm-book.pdf ./
