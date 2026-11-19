#!/bin/bash
# run.sh PY NPROC OUT "ci:m ci:m ..."   -- each pair in turn, stop before ~270 s (resumable: rerun to continue)
PY=$1; NP=$2; OUT=$3; shift 3
cd /tmp/aequi-complete; start=$(date +%s)
for cm in $@; do
  ci=${cm%%:*}; m=${cm##*:}
  left=$(( 150 - ($(date +%s) - start) )); [ $left -lt 15 ] && { echo "TIME: stopped before $cm"; exit 0; }
  timeout $left $PY scripts/solve.py data/classes.json $ci $m 0 1 $NP $OUT 2>&1 | grep -v Warning | grep -v "cu = " | tail -2
done
echo "ALL DONE"
