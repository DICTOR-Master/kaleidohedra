#!/bin/sh
# paper.src.html -> paper.html, then figcheck and print on compute-host (~/work/cw-print), PDF back here
set -e
cd "$(dirname "$0")"
mkdir -p figures
cp ../../studies/2026-11-04-cubic-pairings/figures/*.png figures/
cp paper.src.html paper.html
ssh compute-host 'mkdir -p ~/work/cw-print/cubic-pairings-93'
rsync -a --delete --exclude '*.pdf' ./ compute-host:work/cw-print/cubic-pairings-93/
ssh compute-host "cd ~/work/cw-print && node figcheck.mjs cubic-pairings-93 && node print.mjs cubic-pairings-93 one-double-pyramid-two-splits.pdf 'One Double Pyramid, Two Splits' '10.5281/zenodo.23933666' 1"
rsync -a compute-host:work/cw-print/cubic-pairings-93/one-double-pyramid-two-splits.pdf ./
