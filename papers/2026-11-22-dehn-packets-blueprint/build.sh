#!/bin/sh
# paper.html -> DRAFT PDF on compute-host with the house pipeline (statement audit first, then figcheck.mjs and print.mjs)
set -e
cd "$(dirname "$0")"
D=2026-11-22-dehn-packets-blueprint
LEAN=72e20c97   # research-branch commit of the last completed Lean build; the grey boxes are checked against it
rsync -a --delete --exclude '*.pdf' ./ compute-host:kaleidohedra-papers/$D/
rsync -a ../paper.css ../dicto-logo.png ../print.mjs ../figcheck.mjs ../edgecheck.py ../edgecheck-allow.txt compute-host:kaleidohedra-papers/
T=$(mktemp -d); (cd ../.. && git archive $LEAN studies/2026-11-22-lean-packets | tar -x -C "$T")
rsync -a --delete "$T/studies/2026-11-22-lean-packets/" compute-host:kres-audit/lean119/packets/
rsync -a --delete ../../studies/2026-11-19-lean-dehn-2/lean/ compute-host:kres-audit/lean119/canon/
rm -rf "$T"
ssh compute-host "cd ~/kaleidohedra-papers/$D && python3 scripts/audit.py ~/kres-audit/lean119/packets ~/kres-audit/lean119/canon | tee /dev/stderr | grep -q '^AUDIT OK'"
ssh compute-host "cd ~/kaleidohedra-papers && node figcheck.mjs $D && node print.mjs $D DRAFT-dehn-packets-blueprint.pdf 'Cancelling Packets in Lean' draft"
rsync -a compute-host:kaleidohedra-papers/$D/DRAFT-dehn-packets-blueprint.pdf ./
