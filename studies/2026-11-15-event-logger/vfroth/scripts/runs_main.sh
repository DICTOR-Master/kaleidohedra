#!/bin/bash
# Production runs of the law-built froth (plan and predictions in the event-logger README, section "Law-built froth").
# Main runs (compute machine 1): N0 = 2500 seeds 1-8, N0 = 1000 seeds 1-8 (N0 = 6400 was dropped after 12 min: about 20 h at the shared machine's load); then vf_count.py per size. The side runs (rc x 4,
# law=wrong) are runs_side.sh. Last line FINAL ok only if every run ended 'done' and every count passed its own checks.
cd "$(dirname "$0")/.." || exit 1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
PY=~/geom/bin/python3
mkdir -p results
pids=()
for s in 1 2 3 4 5 6 7 8; do $PY scripts/vfroth.py results/n2500_s$s N0=2500 Nend=50 seed=$s maxwall=37000 > results/n2500_s$s.log 2>&1 & pids+=($!); done
for s in 1 2 3 4 5 6 7 8; do $PY scripts/vfroth.py results/n1000_s$s N0=1000 Nend=50 seed=$s maxwall=37000 > results/n1000_s$s.log 2>&1 & pids+=($!); done
total=${#pids[@]}
while :; do
  left=0; for p in "${pids[@]}"; do kill -0 $p 2>/dev/null && left=$((left+1)); done
  echo "PROGRESS $(awk -v a=$((total-left)) -v b=$total 'BEGIN{printf "%.3f", a/b}') runs finished; N now: $(for f in results/n1000_s1.log results/n2500_s1.log; do grep PROGRESS $f | tail -1 | grep -o 'N=[0-9]*'; done | tr '\n' ' ')"
  [ $left -eq 0 ] && break
  sleep 300
done
for p in "${pids[@]}"; do wait $p; done
ok=1
for f in results/n2500_s?.log results/n1000_s?.log; do tail -1 $f | grep -q '^FINAL ok' || { echo "RUN NOT OK: $f: $(tail -1 $f)"; ok=0; }; done
$PY scripts/vf_count.py results/count_n2500.json results/n2500_s? > results/count_n2500.log 2>&1 || ok=0
$PY scripts/vf_count.py results/count_n1000.json results/n1000_s? > results/count_n1000.log 2>&1 || ok=0
tail -2 results/count_n2500.log results/count_n1000.log
for f in results/count_n2500.log results/count_n1000.log; do tail -1 $f | grep -q '^FINAL ok' || ok=0; done
[ $ok -eq 1 ] && echo "FINAL ok" || echo "FINAL FAIL"
