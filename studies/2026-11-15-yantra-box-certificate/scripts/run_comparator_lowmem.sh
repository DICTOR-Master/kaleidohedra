#!/bin/bash
# Local comparator run for a machine with less memory than con-ron's default 16 workers need:
# the template's verify-comparator.sh, with con-ron given --jobs=$CJ (con-ron's verdict is the same at
# every worker count, per its --help). Palomar itself runs the unmodified script.
# Usage: ENTRY=<entry dir> CJ=2 run_comparator_lowmem.sh      FINAL ok iff the comparator exits 0.
ENTRY=${ENTRY:?}; CJ=${CJ:-2}; ST=$(cd "$(dirname "$0")/.." && pwd); LOG=$ST/logs/palomar; mkdir -p $LOG
export PATH=$HOME/.elan/bin:$PATH
cd "$ENTRY" || exit 1
sed "s#\"con-ron\": \[f\"{prefix}/bin/con-ron\"\]#\"con-ron\": [f\"{prefix}/bin/con-ron\", \"--jobs=$CJ\", \"--progress=500\"]#" scripts/verify-comparator.sh > $LOG/verify-comparator-lowmem.sh
grep -q -- "--jobs=$CJ" $LOG/verify-comparator-lowmem.sh || { echo "FINAL FAIL (could not set con-ron jobs)"; exit 1; }
cp $LOG/verify-comparator-lowmem.sh scripts/verify-comparator-lowmem.sh
echo "PROGRESS 0.1 comparator (con-ron --jobs=$CJ)"
( while sleep 300; do echo "PROGRESS 0.5 heartbeat $(grep -a 'con-ron: check\|Running' $LOG/comparator2.log | tail -1 | cut -c1-150)"; done ) & hb=$!
/usr/bin/time -v bash scripts/verify-comparator-lowmem.sh > $LOG/comparator2.log 2>&1; cs=$?; kill $hb 2>/dev/null
rm -f scripts/verify-comparator-lowmem.sh
grep -E "Maximum resident|Elapsed \(wall" $LOG/comparator2.log
grep -v "linter\|^warning\|^Note\|^$" $LOG/comparator2.log | grep -v "^	" | tail -12
echo "PROGRESS 1.0 done"
[ $cs -eq 0 ] && echo "FINAL ok" || echo "FINAL FAIL (comparator exit $cs)"
