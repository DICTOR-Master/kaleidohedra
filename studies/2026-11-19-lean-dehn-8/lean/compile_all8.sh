#!/bin/bash
# Compile studies 1-8 in dependency order inside the Lean workspace (folder DehnCanon/); write the log to stdout.
# Usage from the workspace root: bash DehnCanon/compile_all8.sh [part]   (part 1, 2, 3, 4 or check; no argument = all)
# The parts exist only so that each run stays short; together they are the whole chain.
export PATH=$HOME/.elan/bin:$PATH
P1="DehnCanon1 Dehn2Poly Dehn2Local Dehn2Sum Dehn2Cut Dehn2Motion DehnCanon2 Dehn2Edges Dehn2R3 Dehn3Sector Dehn3Solids"
P2="Dehn4Similar Dehn4Rational Dehn4Simplex Dehn4Words Dehn5Angles Dehn5Edges Dehn5Fuji Dehn5Pairs Dehn6Indep Dehn6Pairs"
P3="Dehn7Gold Dehn7Octa Dehn7CubeOct Dehn7Dodeca Dehn7Icosa Dehn7Table"
P4="Dehn8Indep Dehn8Cross"
CHAIN="$P1 $P2 $P3 $P4"
case "$1" in 1) RUN="$P1";; 2) RUN="$P2";; 3) RUN="$P3";; 4) RUN="$P4";; check) RUN="";; *) RUN="$CHAIN";; esac
if [ "$1" != "2" ] && [ "$1" != "3" ] && [ "$1" != "4" ] && [ "$1" != "check" ]; then
  echo "toolchain: $(cat lean-toolchain); Mathlib rev: $(grep -B10 '"name": "mathlib"' lake-manifest.json | grep '"rev"' | tr -d ' ,')"
fi
for f in $RUN; do
  echo "== $f.lean"
  timeout 250 lake env lean -o .lake/build/lib/lean/DehnCanon/$f.olean DehnCanon/$f.lean 2>&1
  echo "exit=$?"
done
if [ -z "$1" ] || [ "$1" = "check" ]; then
  echo "== Axioms8.lean"
  timeout 100 lake env lean DehnCanon/Axioms8.lean 2>&1
  echo "exit=$?"
  echo "== grep sorry (the twenty-nine files of the chain and Axioms8)"
  grep -n "sorry" $(for f in $CHAIN Axioms8; do echo DehnCanon/$f.lean; done)
  echo "grep exit=$? (0 = matches listed above; they must all be header lines saying: No \`sorry\`)"
  echo "== grep native_decide / axiom declarations"
  grep -n "native_decide\|^axiom " $(for f in $CHAIN Axioms8; do echo DehnCanon/$f.lean; done)
  echo "grep exit=$? (1 = no match)"
fi
