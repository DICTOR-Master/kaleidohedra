#!/bin/sh
# paper.src.html -> paper.html (DOI reserved or given as $2, commit $1), then print on dicto-big-brother in ~/kres-tmp/web-of-bonds (node_modules -> ~/kaleidohedra-check/node_modules)
set -e
cd "$(dirname "$0")"
python3 - "$1" "${2:-}" <<'P'
import sys
s = open('paper.src.html').read().replace('__LIBROWS__', open('lib-rows.html').read().strip())
doi = ('DICTO DOI: ' + sys.argv[2]) if sys.argv[2] else 'DICTO DOI: reserved on publication'
s = s.replace('__DOI__', doi).replace('__COMMIT__', sys.argv[1])
open('paper.html', 'w').write(s)
P
rsync -a --delete --exclude pg ./ ${PRINT_NODE:-dicto-big-brother}:kres-tmp/web-of-bonds/2026-10-25-bond-relay/
rsync -a ../paper.css ../dicto-logo.png ../print.mjs ${PRINT_NODE:-dicto-big-brother}:kres-tmp/web-of-bonds/
ssh ${PRINT_NODE:-dicto-big-brother} "cd ~/kres-tmp/web-of-bonds && node print.mjs 2026-10-25-bond-relay ${3:-web-of-bonds-draft.pdf} 'The Web of Bonds' '${2:-reserved}' ${4:-1}"
rsync -a ${PRINT_NODE:-dicto-big-brother}:kres-tmp/web-of-bonds/2026-10-25-bond-relay/${3:-web-of-bonds-draft.pdf} ./
