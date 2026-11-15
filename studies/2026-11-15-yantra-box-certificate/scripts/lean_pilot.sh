#!/bin/bash
# Lean pilot (Lean 4 + Mathlib, the toolchain of the local Palomar project): (1) the evaluator file with its soundness proofs compiles;
# (2) PROVED part: 1000 leaves of the main certificate checked by the kernel (decide +kernel, no native_decide) with the proved
#     monotone-split evaluator, and the corollary "G~ has no zero in these leaves" follows from the soundness theorem;
# (3) TIMING part: the Nat-only slope checker (its soundness lemma is the next step) on 10 x 50 leaves closed by H1~ (522 terms),
#     two files at a time, to measure kernel time and memory per leaf.
# Writes logs/lean-*.log and data/lean-pilot.json.  FINAL ok iff every file compiles without error.
cd "$(dirname "$0")/.." || exit 1
PY=${PY:-~/geom/bin/python}
LP=${LEANPROJ:-$HOME/lean/palomar-dicto}
OUT=${LEANOUT:-$HOME/lean/yantra-box-pilot}
mkdir -p "$OUT"; export PATH=$HOME/.elan/bin:$PATH
st=0
run() {  # file tag
  /usr/bin/time -f "TIME $2 %e s %M KB" timeout 1500 bash -c "cd $LP && lake env lean $1" > logs/lean-$2.log 2>&1
  local rc=$?; grep -q "error" logs/lean-$2.log && rc=1
  echo "$2 rc=$rc $(grep '^TIME' logs/lean-$2.log)"; [ $rc -eq 0 ] || st=1
}
echo "PROGRESS 0.05 core"
cp lean/BoxCheck.lean "$OUT/BoxCheck.lean"; run "$OUT/BoxCheck.lean" core
echo "PROGRESS 0.15 proved 1000 leaves"
$PY scripts/b6_lean_export.py data/polys-utr.json data/bnb-main.json G 1000 "$OUT/ProvedG1000.lean" mono > logs/lean-export-G.log 2>&1 || st=1
run "$OUT/ProvedG1000.lean" provedG1000
for k in 0 1 2 3 4 5 6 7 8 9; do
  $PY scripts/b6_lean_export.py data/polys-utr.json data/bnb-main.json H1 50 "$OUT/SlopeH1_$k.lean" slope $((50 * k)) > logs/lean-export-H1-$k.log 2>&1 || st=1
done
for pair in "0 1" "2 3" "4 5" "6 7" "8 9"; do
  set -- $pair
  echo "PROGRESS 0.$((2 + $1)) slope files $1 $2"
  run "$OUT/SlopeH1_$1.lean" slopeH1_$1 & p1=$!
  run "$OUT/SlopeH1_$2.lean" slopeH1_$2 & p2=$!
  wait $p1 $p2
done
for f in logs/lean-core.log logs/lean-provedG1000.log logs/lean-slopeH1_*.log; do grep -q "error" "$f" && { echo "error in $f"; st=1; }; grep -q '^TIME' "$f" || st=1; done
grep -h '^TIME' logs/lean-*.log | sort
$PY - <<'EOF'
import json, re, glob
rows = {}
for f in glob.glob('logs/lean-*.log'):
    for l in open(f):
        m = re.match(r'TIME (\S+) ([\d.]+) s (\d+) KB', l)
        if m: rows[m.group(1)] = {'seconds': float(m.group(2)), 'max_rss_gb': int(m.group(3)) / 1e6}
json.dump(rows, open('data/lean-pilot.json', 'w'), indent=1)
print(json.dumps(rows, indent=1))
EOF
[ $st -eq 0 ] && echo "FINAL ok" || echo "FINAL FAIL"
