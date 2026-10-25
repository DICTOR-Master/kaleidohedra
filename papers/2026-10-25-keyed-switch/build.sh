#!/bin/sh
# paper.src.html -> paper.html (commit $1; DOI $2, else "reserved on publication"; paper number $5, default "56"), then print on
# dicto-big-brother in ~/kres-tmp/keyed-switch (node_modules -> ~/kaleidohedra-check/node_modules, as for #52/#53).
#   sh build.sh <commit> [DOI] [pdf name] [version] [number]
set -e
cd "$(dirname "$0")"
python3 - "$1" "${2:-}" "${5:-56}" <<'P'
import sys
s = open('paper.src.html').read()
doi = ('DICTO DOI: ' + sys.argv[2]) if sys.argv[2] else 'DICTO DOI: reserved on publication'
s = s.replace('__DOI__', doi).replace('__COMMIT__', sys.argv[1]).replace('__NUM__', sys.argv[3])
open('paper.html', 'w').write(s)
P
rsync -a --delete --exclude pg ./ ${PRINT_NODE:-dicto-big-brother}:kres-tmp/keyed-switch/2026-10-25-keyed-switch/
rsync -a ../paper.css ../dicto-logo.png ../print.mjs ${PRINT_NODE:-dicto-big-brother}:kres-tmp/keyed-switch/
ssh ${PRINT_NODE:-dicto-big-brother} "cd ~/kres-tmp/keyed-switch && ln -sfn ~/kaleidohedra-check/node_modules node_modules && nice -n 10 node print.mjs 2026-10-25-keyed-switch ${3:-keyed-switch-draft.pdf} 'Sonsam and Lahdeli' '${2:-reserved}' ${4:-1}"
rsync -a ${PRINT_NODE:-dicto-big-brother}:kres-tmp/keyed-switch/2026-10-25-keyed-switch/${3:-keyed-switch-draft.pdf} ./
