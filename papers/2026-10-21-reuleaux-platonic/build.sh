#!/bin/sh
# paper.src.html -> paper.html (library rows; draft: DOI reserved, commit given as $1), then print on dicto-node
set -e
cd "$(dirname "$0")"
python3 - "$1" <<'P'
import sys
s = open('paper.src.html').read().replace('__LIBROWS__', open('lib-rows.html').read().strip())
s = s.replace('__DOI__', 'DICTO DOI: reserved on publication').replace('__COMMIT__', sys.argv[1])
open('paper.html', 'w').write(s)
P
rsync -a --delete --exclude pg ./ 192.168.0.7:kaleidohedra-papers/2026-10-21-reuleaux-platonic/
rsync -a ../paper.css ../dicto-logo.png ../print.mjs 192.168.0.7:kaleidohedra-papers/
ssh 192.168.0.7 'cd ~/kaleidohedra-papers && node print.mjs 2026-10-21-reuleaux-platonic reuleaux-platonic-draft.pdf "The Reuleaux Platonic Solids" "reserved" 1'
rsync -a 192.168.0.7:kaleidohedra-papers/2026-10-21-reuleaux-platonic/reuleaux-platonic-draft.pdf ./
