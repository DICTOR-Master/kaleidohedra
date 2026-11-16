#!/bin/bash
# Does the entry fit Palomar's standard runner (4 cores, 16 GB)? On a larger machine, emulate it:
#   1. a clean `lake build Solution` (Palomar's own build command) on 4 CPUs (taskset, LEAN_NUM_THREADS=4) inside a cgroup
#      with MemoryMax=$CAP and no swap; a sampler records the most lean processes seen at once; the unit reports its
#      memory peak;
#   2. the axioms of the two theorems;
#   3. the comparator (Lean kernel, NanoDa, con-ron with --jobs=$CJ; Palomar uses 2) under the same cap and CPUs.
# Usage: ENTRY=<assembled entry with .lake/packages and no .lake/build> [CAP=14G] [CJ=2] run_fit_check.sh
# FINAL ok iff the build and the comparator succeed under the cap and the axioms are the three standard ones.
ENTRY=${ENTRY:?}; CAP=${CAP:-14G}; CJ=${CJ:-2}
ST=$(cd "$(dirname "$0")/.." && pwd); LOG=$ST/logs/fit; mkdir -p $LOG
export PATH=$HOME/.elan/bin:$PATH
cd "$ENTRY" || exit 1
st=0
echo "clean (no .lake/build): $(test -d .lake/build && echo NO || echo yes)"
python3 scripts/check-lean-sources.py > $LOG/sources.log 2>&1; echo "source check exit $?"; [ -s $LOG/sources.log ] && { cat $LOG/sources.log; st=1; }
lake exe cache get > $LOG/cache.log 2>&1 || { tail -3 $LOG/cache.log; st=1; }
run_capped() {   # name, command...: run in a capped unit on CPUs 0-3; print the unit summary
  n=$1; shift
  systemd-run --user --wait --pipe -p MemoryMax=$CAP -p MemorySwapMax=0 -E PATH=$PATH -E LEAN_NUM_THREADS=4 \
    --working-directory=$ENTRY taskset -c 0-3 "$@" > $LOG/$n.log 2>&1; ec=$?
  grep -E "Finished with result|Memory peak|Service runtime|CPU time" $LOG/$n.log | sed "s/^ */$n: /"
  return $ec
}
echo "PROGRESS 0.05 capped build"
( mx=0; while sleep 5; do c=$(pgrep -c -f "bin/lean $ENTRY"); [ "$c" -gt "$mx" ] && mx=$c && echo $mx > $LOG/maxlean; done ) & smp=$!
( while sleep 300; do echo "PROGRESS 0.3 heartbeat: built $(find .lake/build/lib -name '*.olean' 2>/dev/null | wc -l) oleans"; done ) & hb=$!
run_capped build lake build Solution; bc=$?
kill $smp $hb 2>/dev/null
echo "build exit $bc; most lean processes at once: $(cat $LOG/maxlean 2>/dev/null)"; grep -E "error|Build completed" $LOG/build.log | head -5
[ $bc -eq 0 ] || st=1
echo "PROGRESS 0.5 axioms"
printf 'import Solution\n#print axioms KulaichevYantra.kulaichev_unique\n#print axioms KulaichevYantra.kulaichev_slope\n' > AxiomsCheck.lean
lake env lean AxiomsCheck.lean > $LOG/axioms.log 2>&1; rm -f AxiomsCheck.lean; cat $LOG/axioms.log
[ "$(grep -c 'depends on axioms: \[propext, Classical.choice, Quot.sound\]' $LOG/axioms.log)" = 2 ] || st=1
if [ $st -eq 0 ] && [ -z "$NOCOMP" ]; then
  echo "PROGRESS 0.55 capped comparator (con-ron --jobs=$CJ)"
  sed "s#\"con-ron\": \[f\"{prefix}/bin/con-ron\"\]#\"con-ron\": [f\"{prefix}/bin/con-ron\", \"--jobs=$CJ\", \"--progress=2000\"]#" scripts/verify-comparator.sh > scripts/verify-comparator-fit.sh
  grep -q -- "--jobs=$CJ" scripts/verify-comparator-fit.sh || { echo "could not set con-ron jobs"; st=1; }
  ( while sleep 300; do echo "PROGRESS 0.7 heartbeat $(grep -a 'con-ron: check\|Running' $LOG/comparator.log | tail -1 | cut -c1-120)"; done ) & hb=$!
  run_capped comparator bash scripts/verify-comparator-fit.sh; cc=$?
  kill $hb 2>/dev/null; rm -f scripts/verify-comparator-fit.sh
  grep -aE "kernel accepts|okay|^error|Illegal|do not match" $LOG/comparator.log | tail -6
  echo "comparator exit $cc"; [ $cc -eq 0 ] || st=1
fi
echo "PROGRESS 1.0 done"
[ $st -eq 0 ] && echo "FINAL ok" || echo "FINAL FAIL"
