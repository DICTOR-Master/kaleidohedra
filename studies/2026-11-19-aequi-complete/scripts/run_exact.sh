#!/bin/bash
# run_exact.sh PY NPROC "si/sn ..."  -- refine slices in turn, stop before ~150 s (resumable)
PY=$1; NP=$2; shift 2
cd /tmp/aequi-complete; start=$(date +%s)
for s in $@; do
  si=${s%%/*}; sn=${s##*/}
  left=$(( 150 - ($(date +%s) - start) )); [ $left -lt 15 ] && { echo "TIME: stopped before $s"; exit 0; }
  timeout $left $PY scripts/exact.py data/dice.json $si $sn $NP data/exact-$si-$sn.jsonl 2>&1 | grep -v Warn | tail -2
done
echo "ALL DONE"
