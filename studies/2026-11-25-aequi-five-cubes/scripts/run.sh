#!/bin/bash
# Search driver (after run2a.sh of study 2026-11-24-aequi-certify-extend): each (class:m) in turn on NP cores
# (resumable: rerun to continue); then the completeness check.   usage: run.sh PY NP OUT "ci:m ..."
cd "$(dirname "$0")/.."; PY=$1; NP=$2; OUT=$3; STAGES=$4; n=0; tot=$(echo $STAGES | wc -w)
for cm in $STAGES; do
  IFS=: read ci m <<< "$cm"
  $PY scripts/solve.py data/classes.json $ci $m 0 1 $NP $OUT 2>&1 | grep -E "^class|^done"
  n=$((n+1)); echo "PROGRESS $(python3 -c "print(round($n/$tot,3))") $cm"
done
$PY scripts/plan_check.py data/classes.json $OUT "$STAGES" && echo "FINAL ok" || echo "FINAL FAIL: plan_check"
