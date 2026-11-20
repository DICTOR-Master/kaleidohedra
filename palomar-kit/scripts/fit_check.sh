#!/bin/bash
# Fit check: does the entry fit Palomar's runners? Emulated on a larger compute host, one step per call, each step in
# the foreground under TMO (280 s), with CPUs pinned (taskset, LEAN_NUM_THREADS) and a memory cap without swap.
#
# Profiles (PalomarSubmission 14aa8d6: execution-profiles.json and verification-profile.json):
#   PROFILE=namespace  palomar-namespace-16x32-v1: 16 CPUs, 32 GB (minimum host memory 28 GiB). This is the profile
#                      Palomar actually ran the Dehn Canon submission on (its mechanical report: 16 CPUs, 31.4 GiB).
#                      Emulated as CPUs 0-15, cap 30G.
#   PROFILE=standard   palomar-standard-v1: GitHub-hosted ubuntu-24.04, 4 CPUs, 16 GB (minimum host memory 14 GiB).
#                      The workflow's execution_profile; emulated as CPUs 0-3, cap 14G. If an entry fits here it fits
#                      everywhere. Record both.
# con-ron runs with 2 workers in both (Palomar's --jobs=2), with a 1800 s budget in Palomar; a con-ron capacity failure
# is recorded by Palomar as "declined" with a warning after the mandatory Lean and NanoDa checks pass, not a rejection.
#
# Steps (ENTRY = the assembled entry; default the current folder):
#   STEP=clean                     remove the entry's own build folder (.lake/build), keep the Mathlib packages
#   STEP=build T="<targets>"       lake build; split a long build into calls on library targets, lake resumes; the last
#                                  call is Palomar's `lake build Solution`
#   STEP=comparator                the template comparator in one run (run_comparator_full.sh, con-ron --jobs=2)
#   STEP=export | STEP=judge K=none | STEP=kernel K=lean|nanoda|con-ron    the split judge (run_comparator_split.sh)
# Each call appends one line to $ENTRY/logs/fit/SUMMARY.tsv: date, profile, step, exit, wall time, peak memory
# (cgroup, whole step), most Lean processes at once. Prints FINAL ok iff the step exits 0 within the limit.
PROFILE=${PROFILE:?PROFILE=namespace|standard}; STEP=${STEP:?}; TMO=${TMO:-280}; CJ=${CJ:-2}
KIT=$(cd "$(dirname "$0")" && pwd); ENTRY=$(cd "${ENTRY:-.}" && pwd); cd "$ENTRY" || exit 1
case $PROFILE in
  namespace) CPUS=0-15; MEM=${MEM:-30G}; NAME=palomar-namespace-16x32-v1 ;;
  standard)  CPUS=0-3;  MEM=${MEM:-14G}; NAME=palomar-standard-v1 ;;
  *) echo "PROFILE must be namespace or standard"; exit 1 ;;
esac
NCPU=$(nproc --all); [ "${CPUS#*-}" -ge "$NCPU" ] && { echo "this host has $NCPU CPUs: cannot emulate $NAME"; exit 1; }
LOG=logs/fit/$PROFILE; mkdir -p "$LOG"; export PATH=$HOME/.elan/bin:$PATH
export LEAN_NUM_THREADS=$(( ${CPUS#*-} + 1 ))
( mx=0; while sleep 2; do c=$(pgrep -c -x lean); [ "$c" -gt "$mx" ] && mx=$c && echo $mx > "$LOG/maxlean-$STEP"; done ) & smp=$!
rm -f "$LOG/maxlean-$STEP"
case $STEP in
  clean) kill $smp; rm -rf .lake/build; echo "removed .lake/build"; echo "FINAL ok"; exit 0 ;;
  build) OUT=$LOG/build-last.log
    timeout "$TMO" systemd-run --user --scope -q -p MemoryMax="$MEM" -p MemorySwapMax=0 taskset -c $CPUS bash -c \
      "/usr/bin/time -v lake build ${T:-Solution}; s=\$?
       echo \"cgroup memory.peak (bytes, whole step): \$(cat /sys/fs/cgroup\$(cut -d: -f3 /proc/self/cgroup)/memory.peak)\"
       exit \$s" > "$OUT" 2>&1; cs=$?
    cat "$OUT" >> "$LOG/build.log" ;;
  comparator) OUT=$LOG/comparator.log
    ENTRY=$ENTRY CPUS=$CPUS MEM=$MEM CJ=$CJ TMO=$TMO LOG=$OUT bash "$KIT/run_comparator_full.sh" > "$LOG/comparator-summary.txt" 2>&1; cs=$?
    grep -q "^FINAL ok" "$LOG/comparator-summary.txt" || cs=1 ;;
  export|judge|kernel) OUT=$LOG/$STEP-${K:-all}.log
    ENTRY=$ENTRY STEP=$STEP K=$K CPUS=$CPUS MEM=$MEM CJ=$CJ TMO=$TMO LOG=$OUT bash "$KIT/run_comparator_split.sh" > "$LOG/$STEP-${K:-all}-summary.txt" 2>&1; cs=$?
    grep -q "^FINAL ok" "$LOG/$STEP-${K:-all}-summary.txt" || cs=1 ;;
  *) kill $smp; echo "unknown STEP"; exit 1 ;;
esac
kill $smp 2>/dev/null
WALL=$(grep -aoE "Elapsed \(wall clock\) time \(h:mm:ss or m:ss\): \S+" "$OUT" | tail -1 | awk '{print $NF}')
PEAK=$(grep -aoE "memory.peak \(bytes, whole (step|run)\): [0-9]+" "$OUT" | tail -1 | awk '{printf "%.2f GiB", $NF/2^30}')
MAXL=$(cat "$LOG/maxlean-$STEP" 2>/dev/null || echo 0)
printf '%s\t%s\t%s %s\texit %s\twall %s\tpeak %s\tlean procs %s\n' "$(date -u +%FT%TZ)" "$NAME" "$STEP" "${K:-${T:-}}" \
  "$cs" "${WALL:-?}" "${PEAK:-?}" "$MAXL" | tee -a logs/fit/SUMMARY.tsv
grep -aE "^error|kernel accepts|okay|Illegal|do not match|Build completed|CUT OFF" "$OUT" | grep -v "^Exporting" | tail -6 | cut -c1-300
[ $cs -eq 0 ] && echo "FINAL ok" || echo "FINAL FAIL (exit $cs)"
