#!/bin/bash
# Compile studies 1-6 in dependency order inside the Lean workspace (folder DehnCanon/); write the log to stdout.
export PATH=$HOME/.elan/bin:$PATH
CHAIN="DehnCanon1 Dehn2Poly Dehn2Local Dehn2Sum Dehn2Cut Dehn2Motion DehnCanon2 Dehn2Edges Dehn2R3 Dehn3Sector Dehn3Solids Dehn4Similar Dehn4Rational Dehn4Simplex Dehn4Words Dehn5Angles Dehn5Edges Dehn5Fuji Dehn5Pairs Dehn6Indep Dehn6Pairs"
echo "toolchain: $(cat lean-toolchain); Mathlib rev: $(grep -B10 '"name": "mathlib"' lake-manifest.json | grep '"rev"' | tr -d ' ,')"
for f in $CHAIN; do
  echo "== $f.lean"
  timeout 200 lake env lean -o .lake/build/lib/lean/DehnCanon/$f.olean DehnCanon/$f.lean 2>&1
  echo "exit=$?"
done
echo "== Axioms6.lean"
timeout 60 lake env lean DehnCanon/Axioms6.lean 2>&1
echo "exit=$?"
echo "== grep sorry (the twenty-one files of the chain and Axioms6)"
grep -n "sorry" $(for f in $CHAIN Axioms6; do echo DehnCanon/$f.lean; done)
echo "grep exit=$? (0 = matches listed above; they must all be header lines saying: No \`sorry\`)"
echo "== grep native_decide / axiom declarations"
grep -n "native_decide\|^axiom " $(for f in $CHAIN Axioms6; do echo DehnCanon/$f.lean; done)
echo "grep exit=$? (1 = no match)"
