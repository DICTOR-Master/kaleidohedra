#!/bin/bash
# Palomar's template comparator (scripts/verify-comparator.sh of the entry) in one foreground run, unchanged except that
# con-ron gets --jobs=$CJ (CJ=default: the template exactly). For entries whose whole judge fits the time limit, and for
# the negative controls. Time limit TMO (default 280 s), memory cap MEM (default 14G) without swap, CPUs CPUS (empty =
# all). /usr/bin/time gives wall time and the largest process; the cgroup's memory.peak the peak of the whole run.
#   ENTRY=<entry> [CJ=2] [LOG=logs/comparator.log] bash run_comparator_full.sh       FINAL ok iff the comparator exits 0
CJ=${CJ:-2}; TMO=${TMO:-280}; MEM=${MEM:-14G}; CPUS=${CPUS:-}
ENTRY=$(cd "${ENTRY:-.}" && pwd); cd "$ENTRY" || exit 1; mkdir -p logs; LOG=${LOG:-logs/comparator.log}
export PATH=$HOME/.elan/bin:$PATH
PIN=""; if [ -n "$CPUS" ]; then PIN="taskset -c $CPUS"
  export LEAN_NUM_THREADS=$(python3 -c 'import sys; print(sum(int(r.split("-")[-1]) - int(r.split("-")[0]) + 1 for r in sys.argv[1].split(",")))' "$CPUS"); fi
V=scripts/verify-comparator-kit.sh
if [ "$CJ" = default ]; then cp scripts/verify-comparator.sh $V; else
  sed "s#\"con-ron\": \[f\"{prefix}/bin/con-ron\"\]#\"con-ron\": [f\"{prefix}/bin/con-ron\", \"--jobs=$CJ\"]#" scripts/verify-comparator.sh > $V
  grep -q -- "--jobs=$CJ" $V || { rm -f $V; echo "FINAL FAIL (could not set con-ron jobs)"; exit 1; }; fi
timeout "$TMO" systemd-run --user --scope -q -p MemoryMax="$MEM" -p MemorySwapMax=0 $PIN bash -c \
  "/usr/bin/time -v bash $V; s=\$?
   echo \"cgroup memory.peak (bytes, whole run): \$(cat /sys/fs/cgroup\$(cut -d: -f3 /proc/self/cgroup)/memory.peak)\"
   exit \$s" > "$LOG" 2>&1; cs=$?
rm -f $V
echo "comparator exit $cs; CPUS=${CPUS:-all} MEM=$MEM CJ=$CJ; log $LOG"
grep -aE "Maximum resident|Elapsed \(wall|memory.peak" "$LOG"
grep -av "linter\|^warning\|^Note\|^$\|^Exporting" "$LOG" | grep -av "^	" | tail -10 | cut -c1-300
[ $cs -eq 0 ] && echo "FINAL ok" || echo "FINAL FAIL (comparator exit $cs)"
