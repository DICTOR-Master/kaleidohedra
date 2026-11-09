#!/bin/bash
# Rerun every certificate of the audit from scratch.
# usage: bash run_all.sh <study folder 2026-11-08-sri-yantra> <python with sympy, mpmath, cypari2, passagemath-singular>
# Makes a fresh work folder ./work, copies the inputs (model.py, natural.py, the two polynomial files, golden_family.json),
# runs the stages in order and writes the logs into thm9/, thm10/ and piece_counts/. Each step ends with a FINAL line.
# Total time about 6 minutes on a 24-core machine (single-threaded steps).
set -u
STUDY=${1:?study folder}; PY=${2:-python3}
HERE=$(cd "$(dirname "$0")" && pwd)
W=$HERE/work; rm -rf "$W"; mkdir -p "$W"
cp "$STUDY"/scripts/model.py "$STUDY"/scripts/natural.py "$STUDY"/figures/golden_family.json \
   "$STUDY"/figures/dicto-yantra-exact-u.txt "$STUDY"/figures/kulaichev-minpoly-u.txt "$W"/
cp "$HERE"/common/*.py "$HERE"/piece_counts/certified_counts.py "$W"/
cd "$W"
run() { local log=$1; shift; timeout 1200 "$PY" -u "$@" > "$log" 2>&1; echo "$(basename "$log"): $(grep -E '^FINAL' "$log" | tail -1)"; }
for c in D K; do
  dir=$HERE/thm9; [ $c = K ] && dir=$HERE/thm10
  run "$dir/stage1-$c-log.txt" stage1_poly.py $c
  [ $c = D ] && run "$dir/stage1b-D-log.txt" stage1b_sqrt5_check.py
  run "$dir/stage2-$c-log.txt" stage2_symbolic.py $c
  run "$dir/stage4-$c-log.txt" stage4_elim.py $c
  run "$dir/stage5-$c-log.txt" stage5_certify.py $c 520
  run "$HERE/piece_counts/counts-$c-log.txt" certified_counts.py $c
done
run "$HERE/thm9/stage2-G-log.txt" stage2_symbolic.py G
cp stage1-*.json stage4-*.txt stage5-*.json counts-*.json stage1-D-g-over-Qsqrt5.txt "$HERE"/work-outputs/ 2>/dev/null || { mkdir -p "$HERE"/work-outputs; cp stage1-*.json stage4-*.txt stage5-*.json counts-*.json stage1-D-g-over-Qsqrt5.txt "$HERE"/work-outputs/; }
