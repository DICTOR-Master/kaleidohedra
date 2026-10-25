#!/bin/sh
# paper.src.html -> paper.html (commit $1, DOI $2 or reserved), then print on dicto-big-brother in ~/kres-tmp/gnomon-polar-print (node_modules -> ~/kaleidohedra-check/node_modules)
set -e
cd "$(dirname "$0")"
python3 - "$1" "${2:-}" <<'P'
import sys
s = open('paper.src.html').read()
doi = ('DICTO DOI: ' + sys.argv[2]) if sys.argv[2] else 'DICTO DOI: reserved on publication'
s = s.replace('__DOI__', doi).replace('__COMMIT__', sys.argv[1])
open('paper.html', 'w').write(s)
P
ssh ${PRINT_NODE:-dicto-big-brother} 'mkdir -p ~/kres-tmp/gnomon-polar-print && ln -sfn ~/kaleidohedra-check/node_modules ~/kres-tmp/gnomon-polar-print/node_modules'
rsync -a --delete ./ ${PRINT_NODE:-dicto-big-brother}:kres-tmp/gnomon-polar-print/2026-10-25-gnomon-polar/
rsync -a ../paper.css ../dicto-logo.png ../print.mjs ${PRINT_NODE:-dicto-big-brother}:kres-tmp/gnomon-polar-print/
ssh ${PRINT_NODE:-dicto-big-brother} "cd ~/kres-tmp/gnomon-polar-print && nice -n 10 node print.mjs 2026-10-25-gnomon-polar ${3:-gnomon-polar-draft.pdf} 'One Turn Is a Gnomon' '${2:-reserved}' ${4:-1}"
rsync -a ${PRINT_NODE:-dicto-big-brother}:kres-tmp/gnomon-polar-print/2026-10-25-gnomon-polar/${3:-gnomon-polar-draft.pdf} ./
