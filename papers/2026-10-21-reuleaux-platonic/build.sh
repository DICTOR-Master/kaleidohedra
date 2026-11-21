#!/bin/sh
# paper.src.html -> paper.html (library rows; draft: DOI reserved, commit given as $1), then figcheck and the DRAFT print on the compute host
set -e
cd "$(dirname "$0")"
python3 - "$1" <<'P'
import sys
s = open('paper.src.html').read().replace('__LIBROWS__', open('lib-rows.html').read().strip())
s = s.replace('__DOI__', 'DICTO DOI: reserved on publication').replace('__COMMIT__', sys.argv[1])
open('paper.html', 'w').write(s)
P
rsync -a --delete --exclude pg --exclude '*.zip' --exclude '*.pdf' ./ compute-host:kaleidohedra-papers/2026-10-21-reuleaux-platonic/
rsync -a ../paper.css ../dicto-logo.png ../print.mjs ../figcheck.mjs compute-host:kaleidohedra-papers/
ssh compute-host 'cd ~/kaleidohedra-papers && node figcheck.mjs 2026-10-21-reuleaux-platonic && node print.mjs 2026-10-21-reuleaux-platonic DRAFT-reuleaux-platonic.pdf "The Reuleaux Platonic Solids" "reserved" 3'
rsync -a compute-host:kaleidohedra-papers/2026-10-21-reuleaux-platonic/DRAFT-reuleaux-platonic.pdf ./
