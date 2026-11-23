#!/bin/bash
# Part 2(b) driver (resumable): SOLVER=solve_wide.py (wide box, default) or solve1.py (raised caps, study-1 box).  usage: run2b.sh PY NP OUT "ci:m ..."
cd "$(dirname "$0")/.."; PY=$1; NP=$2; OUT=$3; STAGES=$4; n=0; tot=$(echo $STAGES | wc -w)
for cm in $STAGES; do
  IFS=: read ci m <<< "$cm"
  $PY scripts/${SOLVER:-solve_wide.py} data/classes-study1.json $ci $m 0 1 $NP $OUT 2>&1 | grep -E "^class|^done"
  n=$((n+1)); echo "PROGRESS $(python3 -c "print(round($n/$tot,3))") $cm"
done
$PY scripts/plan_check2.py data/classes-study1.json $OUT "$STAGES"
