#!/bin/bash
# The main census (steps 1-3) in one job: each step must end FINAL ok; the job's FINAL line depends on all three.
cd "$(dirname "$0")/.." || exit 1
PY=${PY:-python3}
st=0
for s in s1_system s2_isolate s3_backsolve; do
  echo "PROGRESS step $s"
  $PY -u scripts/$s.py > logs/$s.log 2>&1
  tail -n 1 logs/$s.log | grep -q '^FINAL ok' && echo "$s FINAL ok" || { echo "$s did not end FINAL ok:"; tail -n 3 logs/$s.log; st=1; break; }
done
[ $st -eq 0 ] && echo "FINAL ok" || echo "FINAL FAIL"
