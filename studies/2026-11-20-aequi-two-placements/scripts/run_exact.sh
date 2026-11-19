#!/bin/bash
# run_exact.sh PY NPROC BUDGET SLICES SN  -- refine the dice whose index mod SN is in SLICES (comma list), stop at
# BUDGET seconds (resumable: rerun to continue; writes data/exact-<host-free tag SLICES>.jsonl)
PY=$1; NP=$2; BUDGET=$3; SL=$4; SN=$5
cd /tmp/aequi-two
timeout $BUDGET $PY scripts/exact.py data/dice.json $SL $SN $NP data/exact-${SL//,/_}-$SN.jsonl 2>&1 | grep -v Warn | tail -1
echo "ROUND DONE"
