#!/bin/bash
# Part 2(b) wide-box re-search driver (resumable).  usage: run2b.sh PY NP OUT "ci:m ..."
cd "$(dirname "$0")/.."; PY=$1; NP=$2; OUT=$3; STAGES=$4; n=0; tot=$(echo $STAGES | wc -w)
for cm in $STAGES; do
  IFS=: read ci m <<< "$cm"
  $PY scripts/solve_wide.py data/classes-study1.json $ci $m 0 1 $NP $OUT 2>&1 | grep -E "^class|^done"
  n=$((n+1)); echo "PROGRESS $(python3 -c "print(round($n/$tot,3))") $cm"
done
$PY scripts/plan_check2.py data/classes-study1.json $OUT "$STAGES"
