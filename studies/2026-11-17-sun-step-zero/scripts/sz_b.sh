#!/bin/bash
# Job sz-b: census of the 13 Sun settings in shuffled frame order, the four held-out seed-2 controls and the shuffled speed-1 control.
S=$(cd "$(dirname "$0")/.." && pwd); PY=${PY:-python3}; cd $S || exit 1
$PY scripts/run_matrix.py data/configs_b.jsonl 22 2>&1 | tee results/logs/matrix_b.log | grep --line-buffered -E "PROGRESS|Error"
grep -q MATRIX_OK results/logs/matrix_b.log && echo "FINAL ok" || echo "FINAL FAIL (matrix b)"
