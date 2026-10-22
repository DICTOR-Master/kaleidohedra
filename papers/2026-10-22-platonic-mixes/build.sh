#!/bin/sh
# paper.src.html -> paper.html (DOI reserved or given as $2, commit $1), then print on dicto-node
set -e
cd "$(dirname "$0")"
python3 - "$1" "${2:-}" <<'P'
import sys
s = open('paper.src.html').read()
doi = ('DICTO DOI: ' + sys.argv[2]) if sys.argv[2] else 'DICTO DOI: reserved on publication'
s = s.replace('__DOI__', doi).replace('__COMMIT__', sys.argv[1])
open('paper.html', 'w').write(s)
P
rsync -a --delete --exclude pg ./ 192.168.0.7:kaleidohedra-papers/2026-10-22-platonic-mixes/
rsync -a ../paper.css ../dicto-logo.png ../print.mjs 192.168.0.7:kaleidohedra-papers/
ssh 192.168.0.7 "cd ~/kaleidohedra-papers && node print.mjs 2026-10-22-platonic-mixes ${3:-platonic-mixes-draft.pdf} 'Every Mix of the Platonic Solids Fills Space' '${2:-reserved}' ${4:-1}"
rsync -a 192.168.0.7:kaleidohedra-papers/2026-10-22-platonic-mixes/${3:-platonic-mixes-draft.pdf} ./
