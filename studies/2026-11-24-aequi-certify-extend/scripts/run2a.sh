#!/bin/bash
# Part 2(a) search driver: each (class:m) in turn on NP cores (resumable: rerun to continue); then the completeness check.
# usage: run2a.sh PY NP OUT "ci:m ..."
cd "$(dirname "$0")/.."; PY=$1; NP=$2; OUT=$3; STAGES=$4; n=0; tot=$(echo $STAGES | wc -w)
for cm in $STAGES; do
  IFS=: read ci m <<< "$cm"
  $PY scripts/solve.py data/classes2a.json $ci $m 0 1 $NP $OUT 2>&1 | grep -E "^class|^done"
  n=$((n+1)); echo "PROGRESS $(python3 -c "print(round($n/$tot,3))") $cm"
done
$PY scripts/plan_check.py data/classes2a.json $OUT "$STAGES"
