#!/bin/bash
# Build job for the truncated icosidodecahedron (dbb job lean-tid). FINAL ok only on a clean build with no sorry.
cd ~/lean/palomar-packets || exit 1
export PATH=$HOME/.elan/bin:$PATH
echo "PROGRESS 0.1 start"
(cd gen && python3 gen_pieces.py tid > /tmp/tid.out 2> tid.err) || { echo "generation failed"; tail -3 gen/tid.err; exit 1; }
grep "wrote" gen/tid.err
wc -l Packets/GenTID*.lean
echo "PROGRESS 0.2 generated"
lake build Packets 2>&1 | tee /tmp/tidbuild.log | grep -a --line-buffered "Built Packets\|^error" | \
  while IFS= read -r line; do echo "PROGRESS 0.5 $line"; done
if grep -aq "^error" /tmp/tidbuild.log; then grep -a "^error" -A8 /tmp/tidbuild.log | head -60; exit 1; fi
lake build Packets > /tmp/tidbuild2.log 2>&1 || { tail -20 /tmp/tidbuild2.log; exit 1; }
echo "PROGRESS 0.9 built"
cat > /tmp/axtid.lean <<'LEAN'
import Packets
#print axioms Packets.theorem4a_copies
#print axioms Packets.theorem4b_copies
#print axioms Packets.tid_edgeAngle
LEAN
lake env lean /tmp/axtid.lean || exit 1
if grep -rn "sorry" Packets/*.lean | grep -v "No .sorry"; then echo "sorry found"; exit 1; fi
echo "PROGRESS 1 checked"
echo "FINAL ok"
