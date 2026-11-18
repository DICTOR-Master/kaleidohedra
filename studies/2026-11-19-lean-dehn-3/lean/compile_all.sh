#!/bin/bash
# Compile studies 1-3 in dependency order inside the Lean workspace (folder DehnCanon/); write the log to stdout.
export PATH=$HOME/.elan/bin:$PATH
echo "toolchain: $(cat lean-toolchain); Mathlib rev: $(grep -B10 '"name": "mathlib"' lake-manifest.json | grep '"rev"' | tr -d ' ,')"
for f in DehnCanon1 Dehn2Poly Dehn2Local Dehn2Sum Dehn2Cut Dehn2Motion DehnCanon2 Dehn2Edges Dehn2R3 Dehn3Sector Dehn3Solids; do
  echo "== $f.lean"
  timeout 250 lake env lean -o .lake/build/lib/lean/DehnCanon/$f.olean DehnCanon/$f.lean 2>&1
  echo "exit=$?"
done
echo "== Axioms3.lean"
timeout 60 lake env lean DehnCanon/Axioms3.lean 2>&1
echo "exit=$?"
echo "== grep sorry (study 3 files and every file they import)"
grep -n "sorry" DehnCanon/DehnCanon1.lean DehnCanon/Dehn2Poly.lean DehnCanon/Dehn2Local.lean DehnCanon/Dehn2Sum.lean DehnCanon/Dehn2Cut.lean DehnCanon/Dehn2Motion.lean DehnCanon/DehnCanon2.lean DehnCanon/Dehn2Edges.lean DehnCanon/Dehn2R3.lean DehnCanon/Dehn3Sector.lean DehnCanon/Dehn3Solids.lean DehnCanon/Axioms3.lean
echo "grep exit=$? (1 = no match)"
