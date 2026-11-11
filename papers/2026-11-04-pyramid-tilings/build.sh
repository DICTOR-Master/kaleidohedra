#!/bin/sh
# paper.src.html -> paper.html, then figcheck and print on compute-host (~/work/cw-print), PDF back here
set -e
cd "$(dirname "$0")"
cp paper.src.html paper.html
ssh compute-host 'mkdir -p ~/work/cw-print/pyramid-tilings-92'
rsync -a --delete --exclude '*.pdf' ./ compute-host:work/cw-print/pyramid-tilings-92/
ssh compute-host "cd ~/work/cw-print && node figcheck.mjs pyramid-tilings-92 && node print.mjs pyramid-tilings-92 aristotles-pyramid-in-layers.pdf \"Aristotle's Pyramid in Layers\" '10.5281/zenodo.23931608' 2"
rsync -a compute-host:work/cw-print/pyramid-tilings-92/aristotles-pyramid-in-layers.pdf ./
