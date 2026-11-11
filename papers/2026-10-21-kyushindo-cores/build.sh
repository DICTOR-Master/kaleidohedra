#!/bin/sh
# paper.src.html -> paper.html (library rows; draft: DOI reserved, commit given as $1), then print on compute-host-2
set -e
cd "$(dirname "$0")"
python3 - "$1" <<'P'
import sys
s = open('paper.src.html').read().replace('__LIBROWS__', open('lib-rows.html').read().strip())
s = s.replace('__DOI__', 'DICTO DOI: reserved on publication').replace('__COMMIT__', sys.argv[1])
open('paper.html', 'w').write(s)
P
rsync -a --delete --exclude pg ./ compute-host:kaleidohedra-papers/2026-10-21-kyushindo-cores/
rsync -a ../paper.css ../dicto-logo.png ../print.mjs compute-host:kaleidohedra-papers/
ssh compute-host 'cd ~/kaleidohedra-papers && node print.mjs 2026-10-21-kyushindo-cores kyushindo-cores-draft.pdf "DICTO Kyushindo Cores" "reserved" 3'
rsync -a compute-host:kaleidohedra-papers/2026-10-21-kyushindo-cores/kyushindo-cores-draft.pdf ./
