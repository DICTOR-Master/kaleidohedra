#!/bin/sh
# paper.src.html -> paper.html -> DRAFT PDF of Version 4 on compute-host-2 with the house pipeline (figcheck.mjs, print.mjs).
# Remote folder nv-paper-43, so the copy built from research-fig3 is never overwritten. $1 = study commit (default: the draft's base).
set -e
H=${BUILD_HOST:-compute-host-2}   # BUILD_HOST=compute-host when the second host cannot be reached
cd "$(dirname "$0")"
python3 - "${1:-2f750b1e}" <<'Q'
import sys
s = open('paper.src.html').read().replace('__LIBROWS__', open('lib-rows.html').read().strip())
s = s.replace('__DOI__', 'DICTO DOI: 10.5281/zenodo.23532013').replace('__COMMIT__', sys.argv[1])
open('paper.html', 'w').write(s)
Q
D=nv-paper-43
PDF=DRAFT-paper-43-kyushindo-cores-v4.pdf
rsync -a --delete --exclude '*.pdf' --exclude '*.zip' ./ $H:kaleidohedra-papers/$D/
rsync -a ../paper.css ../dicto-logo.png ../print.mjs ../figcheck.mjs $H:kaleidohedra-papers/
ssh $H "cd ~/kaleidohedra-papers && (node figcheck.mjs $D || true) && node print.mjs $D $PDF 'DICTO Kyushindo Cores, v4 draft' draft"
rsync -a $H:kaleidohedra-papers/$D/$PDF ./
mkdir -p "$HOME/Documents/papers-to-read/next-versions/papers"
cp $PDF "$HOME/Documents/papers-to-read/next-versions/papers/"
