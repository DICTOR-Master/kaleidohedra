#!/bin/bash
# Depth-box certification of the 15 amber cells: for each die x mould, one run at the box centre with ball enclosures (AEQ_MODE=box)
# and two runs at random exact points of the box (pt:1, pt:2).  PROGRESS per finished run.
# FINAL ok only if every run is a valid partition with exact volume gap 0, every nonzero sign of the box run is certified over the box,
# and the three runs of each cell made the same sign sequence (same sha256) with the same counts.
# run with PY set to a python with numpy, scipy, mpmath, python-flint
cd "$(dirname "$0")"; PY=${PY:-python3}; mkdir -p ../logs/certify ../data/cells/box ../data/cells/pt1 ../data/cells/pt2
runs=(); for n in 377 1 5 236 61; do for L in sc bcc fcc; do for M in box pt:1 pt:2; do runs+=("$n $L $M"); done; done; done
total=${#runs[@]}
printf '%s\n' "${runs[@]}" | xargs -P 22 -L 1 bash -c 'AEQ_MODE=$2 timeout 3000 '"$PY"' amber_aequus.py aequus-$0 $1 6/5 cen > ../logs/certify/aequus-$0_$1_${2/:/}.log 2>&1; n=$(ls ../logs/certify/*.log | xargs grep -l "^SIGNS\|Traceback" | wc -l); echo "PROGRESS $n/'"$total"' runs finished (aequus-$0 $1 $2)"'
ok=1
for n in 377 1 5 236 61; do for L in sc bcc fcc; do
  b=../logs/certify/aequus-${n}_${L}_box.log; h=$(grep -o 'sha256 [0-9a-f]*' $b)
  line="$n $L: $(grep -E '^SCUTOID' $b) | $(grep -E '^SIGNS' $b)"
  for M in pt1 pt2; do f=../logs/certify/aequus-${n}_${L}_$M.log
    [ "$(grep -o 'sha256 [0-9a-f]*' $f)" = "$h" ] && [ "$(grep '^SCUTOID' $f)" = "$(grep '^SCUTOID' $b)" ] || { ok=0; line="$line | $M DIFFERS"; }
    grep -q 'RESULT.*valid=True' $f && grep -q 'exact 0' $f || ok=0
  done
  grep -q 'RESULT.*valid=True' $b && grep -q 'exact 0' $b && grep -q 'nonzero NOT certified 0;' $b && [ -n "$h" ] || ok=0
  echo "$line"
done; done
[ $ok = 1 ] && echo "FINAL ok" || echo "FINAL FAIL (see logs/certify)"
