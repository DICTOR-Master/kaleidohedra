#!/bin/bash
# Fit check under Palomar's standard runner (4 cores, 16 GB), emulated on a larger machine (after the Yantra study's
# run_fit_check.sh): every step runs on CPUs 0-3 (taskset, LEAN_NUM_THREADS=4) inside a cgroup capped at $CAP
# (default 14G, under the runner's 16 GB) with no swap, in the foreground under a ${TMO:-280} s limit. A sampler records
# the most lean processes seen at once; the cgroup's memory.peak gives the peak of the whole step.
# Steps (one per call, from the entry root):
#   STEP=build T="<lake targets>"  a lake build from an empty build folder, split into calls that each finish; lake
#                                  resumes where the previous call stopped (Palomar's command is `lake build Solution`)
#   STEP=comparator                the template verify-comparator.sh, unchanged except con-ron --jobs=$CJ (default 2,
#                                  Palomar's worker count)
# FINAL ok iff the step exits 0 within the limit.
STEP=${STEP:?}; CAP=${CAP:-14G}; CJ=${CJ:-2}; TMO=${TMO:-280}
ENTRY=$(cd "$(dirname "$0")/.." && pwd); cd "$ENTRY" || exit 1; LOG=logs/fit; mkdir -p $LOG
export PATH=$HOME/.elan/bin:$PATH LEAN_NUM_THREADS=4
case $STEP in
  build) CMD="lake build $T"; N=build ;;
  comparator)
    sed "s#\"con-ron\": \[f\"{prefix}/bin/con-ron\"\]#\"con-ron\": [f\"{prefix}/bin/con-ron\", \"--jobs=$CJ\"]#" \
      scripts/verify-comparator.sh > scripts/verify-comparator-fit.sh
    grep -q -- "--jobs=$CJ" scripts/verify-comparator-fit.sh || { echo "FINAL FAIL (could not set con-ron jobs)"; exit 1; }
    CMD="bash scripts/verify-comparator-fit.sh"; N=comparator ;;
esac
( mx=0; while sleep 2; do c=$(pgrep -c -x lean); [ "$c" -gt "$mx" ] && mx=$c && echo $mx > $LOG/maxlean-$N; done ) & smp=$!
rm -f $LOG/maxlean-$N
timeout $TMO systemd-run --user --scope -q -p MemoryMax=$CAP -p MemorySwapMax=0 taskset -c 0-3 bash -c \
  "/usr/bin/time -v $CMD; s=\$?
   echo \"cgroup memory.peak (bytes, whole step): \$(cat /sys/fs/cgroup\$(cut -d: -f3 /proc/self/cgroup)/memory.peak)\"
   exit \$s" > $LOG/$N-last.log 2>&1; cs=$?
kill $smp 2>/dev/null; rm -f scripts/verify-comparator-fit.sh
cat $LOG/$N-last.log >> $LOG/$N.log
echo "step $STEP ${T:-}: exit $cs; most lean processes at once: $(cat $LOG/maxlean-$N 2>/dev/null || echo 0)"
grep -aE "Elapsed \(wall|Maximum resident|memory.peak|^error|kernel accepts|okay|Illegal|do not match|Build completed" $LOG/$N-last.log | grep -v "^Exporting" | tail -10
[ $cs -eq 0 ] && echo "FINAL ok" || echo "FINAL FAIL (exit $cs)"
