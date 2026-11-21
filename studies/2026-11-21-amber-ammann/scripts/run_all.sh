#!/bin/bash
# Amber-Ammann: every solid x every one of the 20 rhombohedron orientations x scales (S0, 6/5 S0, own s0) x seeds (cen, cproj).
# Logs per run in ../logs/runs/, data in ../data/.  PROGRESS lines from the count of finished runs.  FINAL ok only if every run
# printed a RESULT line and summary.py re-checks pass (its last line SUMMARY OK).
cd "$(dirname "$0")"; PY=~/venvs/indep/bin/python; mkdir -p ../logs/runs
TR="012 013 014 015 023 024 025 034 035 045 123 124 125 134 135 145 234 235 245 345"
$PY s0.py ${SOLIDS:-icosahedron dodecahedron icosidodecahedron C1 C2} > ../data/s0.txt || exit 1
jobs=../logs/joblist.txt; : > $jobs
while read solid a b rest; do
  a6=$($PY -c "from fractions import Fraction as F; print(F('$a')*F(6,5))"); b6=$($PY -c "from fractions import Fraction as F; print(F('$b')*F(6,5))")
  for t in $TR; do for seed in cen cproj; do
    echo "$solid $t $seed S0 $a,$b" >> $jobs; echo "$solid $t $seed S65 $a6,$b6" >> $jobs; echo "$solid $t $seed own -" >> $jobs
  done; done
done < ../data/s0.txt
N=$(wc -l < $jobs); echo "runs: $N"
run1() { set -- $1; solid=$1 t=$2 seed=$3 sc=$4 S=$5
  log=../logs/runs/${solid}_${t}_${sc}_${seed}.log
  if [ "$sc" = own ]; then timeout 1200 ~/venvs/indep/bin/python ammann_cell.py $solid $t 1 $seed > $log 2>&1
  else AMBER_S=$S AMBER_TAG=$sc timeout 1200 ~/venvs/indep/bin/python ammann_cell.py $solid $t 1 $seed > $log 2>&1; fi
  echo "done ${solid}_${t}_${sc}_${seed} exit $?"; }
export -f run1
( xargs -P 20 -I{} bash -c 'run1 "{}"' < $jobs ) | awk -v N=$N '{c++; print; if (c % 20 == 0) printf "PROGRESS %.2f runs %d/%d\n", c/N, c, N; fflush()}'
nres=$(grep -l "^RESULT" ../logs/runs/*.log | wc -l)
echo "runs with a RESULT line: $nres / $N"
if [ "$nres" -eq "$N" ] && $PY summary.py > ../logs/summary.txt; then tail -60 ../logs/summary.txt; grep -q "^SUMMARY OK" ../logs/summary.txt && echo "FINAL ok" || echo "FINAL FAIL (summary)"; else echo "FINAL FAIL (runs)"; fi
