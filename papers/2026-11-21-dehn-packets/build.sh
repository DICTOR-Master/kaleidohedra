#!/bin/sh
# paper.html -> DRAFT PDF on compute-host with the house pipeline (figure and number audit first, then figcheck.mjs and print.mjs)
set -e
cd "$(dirname "$0")"
D=2026-11-21-dehn-packets
rsync -a --delete --exclude '*.pdf' ./ compute-host:kaleidohedra-papers/$D/
rsync -a ../paper.css ../dicto-logo.png ../print.mjs ../figcheck.mjs ../edgecheck.py ../edgecheck-allow.txt compute-host:kaleidohedra-papers/
rsync -a --relative ../../studies/./2026-11-21-packet-screen ../../studies/./2026-11-21-packet-leads-tiling ../../studies/./2026-11-21-scutoid-stand-in ../../studies/./2026-11-04-rt-pyramids compute-host:kres-audit/studies/
ssh compute-host "cd ~/kaleidohedra-papers/$D/scripts && export STUDIES=~/kres-audit/studies && python3 fig_ring.py && python3 fig_screen.py && python3 audit.py | tee /dev/stderr | grep -q '^AUDIT OK'"
ssh compute-host "cd ~/kaleidohedra-papers && node figcheck.mjs $D && node print.mjs $D DRAFT-dehn-packets.pdf 'From Dehn Packets to Scutoids' draft"
rsync -a compute-host:kaleidohedra-papers/$D/DRAFT-dehn-packets.pdf ./
