#!/bin/bash
# Study 2: amber cells (A) for five Aequi x three cubic moulds (sc, bcc, fcc) at 6/5 s0, centroid seeds.  PROGRESS per finished run.
# FINAL ok only if all runs print RESULT with valid=True, exact volume gap 0 and sampling 0 miscounted.
cd "$(dirname "$0")"; PY=${PY:-python3}; mkdir -p ../logs/cells ../data/cells/stand
runs=(); for n in ${NONHEART:-377 1 5 236 61}; do for L in sc bcc fcc; do runs+=("$n $L"); done; done
total=${#runs[@]}
printf '%s\n' "${runs[@]}" | xargs -P 15 -L 1 bash -c 'timeout 1200 '"$PY"' amber_aequus.py aequus-$0 $1 6/5 cen > ../logs/cells/aequus-$0_$1_6-5.log 2>&1; n=$(ls ../logs/cells/*.log | xargs grep -l "^RESULT\|Traceback" | wc -l); echo "PROGRESS $n/'"$total"' runs finished (aequus-$0 $1)"'
ok=1
for r in "${runs[@]}"; do set -- $r; f=../logs/cells/aequus-$1_$2_6-5.log
  echo "$1 $2: $(grep -E '^SCUTOID|^RESULT' $f | tr '\n' ' ')"
  grep -q 'RESULT.*valid=True' $f && grep -q 'exact 0' $f && grep -q 'not covered exactly once: 0' $f || ok=0
done
[ $ok = 1 ] && echo "FINAL ok" || echo "FINAL FAIL (see logs/cells)"
