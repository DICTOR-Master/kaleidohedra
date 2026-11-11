#!/bin/sh
# paper.src.html -> paper.html (DOI reserved or given as $2, commit $1), then print on Compute-host (PRINT_NODE=compute-host for compute-host-2)
set -e
cd "$(dirname "$0")"
python3 - "$1" "${2:-}" <<'P'
import sys
s = open('paper.src.html').read().replace('__LIBROWS__', open('lib-rows.html').read().strip())
doi = ('DICTO DOI: ' + sys.argv[2]) if sys.argv[2] else 'DICTO DOI: reserved on publication'
s = s.replace('__DOI__', doi).replace('__COMMIT__', sys.argv[1])
open('paper.html', 'w').write(s)
P
rsync -a --delete --exclude pg ./ ${PRINT_NODE:-compute-host}:kaleidohedra-papers/2026-10-23-exact-vs-dissection/
rsync -a ../paper.css ../dicto-logo.png ../print.mjs ${PRINT_NODE:-compute-host}:kaleidohedra-papers/
ssh ${PRINT_NODE:-compute-host} "cd ~/kaleidohedra-papers && node print.mjs 2026-10-23-exact-vs-dissection ${3:-exact-vs-dissection-draft.pdf} 'One Move Each' '${2:-reserved}' ${4:-1}"
rsync -a ${PRINT_NODE:-compute-host}:kaleidohedra-papers/2026-10-23-exact-vs-dissection/${3:-exact-vs-dissection-draft.pdf} ./
