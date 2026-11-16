#!/bin/bash
# Side runs (compute machine 2): rc four times larger (N0 = 2500, seeds 1-2) for Rutenberg-McCurdy's statement that results do not
# depend on rc, and the negative control law=wrong (N0 = 400), which must FAIL the flux check. Last line FINAL ok only if both rc x 4
# runs ended done, their count passed its checks, and the wrong-law run failed the flux check as required.
cd "$(dirname "$0")/.." || exit 1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
PY="${PYTHON:-python3}"   # set PYTHON to the interpreter with numpy/scipy
mkdir -p results
pids=()
for s in 1 2; do $PY scripts/vfroth.py results/n2500_rc4_s$s N0=2500 Nend=50 seed=$s rc=1.2648e-3 > results/n2500_rc4_s$s.log 2>&1 & pids+=($!); done
$PY scripts/vfroth.py results/wrong_n400 N0=400 Nend=40 seed=1 law=wrong > results/wrong_n400.log 2>&1 & pids+=($!)
total=${#pids[@]}
while :; do
  left=0; for p in "${pids[@]}"; do kill -0 $p 2>/dev/null && left=$((left+1)); done
  echo "PROGRESS $(awk -v a=$((total-left)) -v b=$total 'BEGIN{printf "%.3f", a/b}') runs finished; N now: $(grep PROGRESS results/n2500_rc4_s1.log | tail -1 | grep -o 'N=[0-9]*')"
  [ $left -eq 0 ] && break
  sleep 300
done
for p in "${pids[@]}"; do wait $p; done
ok=1
for f in results/n2500_rc4_s?.log results/wrong_n400.log; do tail -1 $f | grep -q '^FINAL ok' || { echo "RUN NOT OK: $f: $(tail -1 $f)"; ok=0; }; done
$PY scripts/vf_count.py results/count_n2500_rc4.json results/n2500_rc4_s? > results/count_n2500_rc4.log 2>&1 || ok=0
tail -2 results/count_n2500_rc4.log
tail -1 results/count_n2500_rc4.log | grep -q '^FINAL ok' || ok=0
[ $ok -eq 1 ] && echo "FINAL ok" || echo "FINAL FAIL"
