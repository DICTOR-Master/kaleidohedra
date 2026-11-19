#!/bin/bash
# run.sh PY NPROC OUT BUDGET "ci:m:si:sn ..."  -- each slice in turn, stop before BUDGET seconds (resumable: rerun to continue)
PY=$1; NP=$2; OUT=$3; BUDGET=$4; shift 4
cd /tmp/aequi-two; start=$(date +%s)
for cm in $@; do
  IFS=: read ci m si sn <<< "$cm"
  left=$(( BUDGET - ($(date +%s) - start) )); [ $left -lt 15 ] && { echo "TIME: stopped before $cm"; exit 0; }
  timeout $left $PY scripts/solve.py data/classes.json $ci $m ${si:-0} ${sn:-1} $NP $OUT 2>&1 | grep -v Warning | grep -v "cu = " | tail -2
done
echo "ALL DONE"
