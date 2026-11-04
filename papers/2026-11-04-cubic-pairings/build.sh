#!/bin/sh
# paper.src.html -> paper.html, then figcheck and print on dicto-big-brother (~/kres-tmp/cw-print), PDF back here
set -e
cd "$(dirname "$0")"
mkdir -p figures
cp ../../studies/2026-11-04-cubic-pairings/figures/*.png figures/
cp paper.src.html paper.html
ssh dicto-big-brother 'mkdir -p ~/kres-tmp/cw-print/cubic-pairings-93'
rsync -a --delete --exclude '*.pdf' ./ dicto-big-brother:kres-tmp/cw-print/cubic-pairings-93/
ssh dicto-big-brother "cd ~/kres-tmp/cw-print && node figcheck.mjs cubic-pairings-93 && node print.mjs cubic-pairings-93 DRAFT-93-cubic-pairings.pdf 'One Double Pyramid, Two Splits' 'reserved on publication' 1"
rsync -a dicto-big-brother:kres-tmp/cw-print/cubic-pairings-93/DRAFT-93-cubic-pairings.pdf ./
