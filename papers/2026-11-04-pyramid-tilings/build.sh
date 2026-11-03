#!/bin/sh
# paper.src.html -> paper.html, then figcheck and print on dicto-big-brother (~/kres-tmp/cw-print), PDF back here
set -e
cd "$(dirname "$0")"
cp paper.src.html paper.html
ssh dicto-big-brother 'mkdir -p ~/kres-tmp/cw-print/pyramid-tilings-92'
rsync -a --delete --exclude '*.pdf' ./ dicto-big-brother:kres-tmp/cw-print/pyramid-tilings-92/
ssh dicto-big-brother "cd ~/kres-tmp/cw-print && node figcheck.mjs pyramid-tilings-92 && node print.mjs pyramid-tilings-92 DRAFT-92-pyramid-tilings.pdf \"Aristotle's Pyramid in Layers\" 'reserved on publication' 1"
rsync -a dicto-big-brother:kres-tmp/cw-print/pyramid-tilings-92/DRAFT-92-pyramid-tilings.pdf ./
