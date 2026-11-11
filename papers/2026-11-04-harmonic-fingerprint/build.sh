#!/bin/sh
# paper.src.html -> paper.html, then figcheck and print on compute-host (~/work/cw-print), PDF back here
set -e
cd "$(dirname "$0")"
mkdir -p figures
cp ../../studies/2026-11-04-harmonic-fingerprint/figures/*.png figures/
cp paper.src.html paper.html
ssh compute-host 'mkdir -p ~/work/cw-print/harmonic-fingerprint-94'
rsync -a --delete --exclude '*.pdf' ./ compute-host:work/cw-print/harmonic-fingerprint-94/
ssh compute-host "cd ~/work/cw-print && node figcheck.mjs harmonic-fingerprint-94 && node print.mjs harmonic-fingerprint-94 the-silent-golden-station.pdf 'The Silent Golden Station' '10.5281/zenodo.23934349' 1"
rsync -a compute-host:work/cw-print/harmonic-fingerprint-94/the-silent-golden-station.pdf ./
