#!/bin/bash
# Local comparator run (after the Yantra study 2026-11-15 and the GET study 2026-11-17): the template's
# verify-comparator.sh, unchanged except that con-ron is given --jobs=$CJ (con-ron's verdict is the same at every
# worker count, per its --help). Palomar itself runs the unmodified script. One foreground run: a time limit of
# TMO seconds (default 280) and a memory cap of 14 GB with no swap; /usr/bin/time records wall time and the largest single-process peak; the scope's
# cgroup memory.peak records the peak of the whole run.
# CJ=default runs the template script unchanged (con-ron with its own worker count).
# Usage (from the entry root): CJ=4 [TMO=280] [LOG=logs/comparator.log] bash scripts/run_comparator_lowmem.sh
# FINAL ok iff the comparator exits 0.
CJ=${CJ:-4}; TMO=${TMO:-280}; ENTRY=$(cd "$(dirname "$0")/.." && pwd); cd "$ENTRY" || exit 1
mkdir -p logs; LOG=${LOG:-logs/comparator.log}
export PATH=$HOME/.elan/bin:$PATH
if [ "$CJ" = default ]; then cp scripts/verify-comparator.sh scripts/verify-comparator-lowmem.sh; else
sed "s#\"con-ron\": \[f\"{prefix}/bin/con-ron\"\]#\"con-ron\": [f\"{prefix}/bin/con-ron\", \"--jobs=$CJ\"]#" \
  scripts/verify-comparator.sh > scripts/verify-comparator-lowmem.sh
grep -q -- "--jobs=$CJ" scripts/verify-comparator-lowmem.sh || { echo "FINAL FAIL (could not set con-ron jobs)"; exit 1; }; fi
timeout $TMO systemd-run --user --scope -q -p MemoryMax=14G -p MemorySwapMax=0 bash -c \
  '/usr/bin/time -v bash scripts/verify-comparator-lowmem.sh; s=$?
   echo "cgroup memory.peak (bytes, whole run): $(cat /sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)/memory.peak)"
   exit $s' > $LOG 2>&1; cs=$?
rm -f scripts/verify-comparator-lowmem.sh
grep -aE "Maximum resident|Elapsed \(wall|memory.peak" $LOG
grep -av "linter\|^warning\|^Note\|^$" $LOG | grep -av "^	" | tail -14
[ $cs -eq 0 ] && echo "FINAL ok" || echo "FINAL FAIL (comparator exit $cs)"
