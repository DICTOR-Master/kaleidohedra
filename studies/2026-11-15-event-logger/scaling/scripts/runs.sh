# Scaling-state froth runs (parameters fixed before the runs, README section "Scaling-state froth").
# Usage: runs.sh big   -> 2048^2, seeds 1 and 2, in parallel;   runs.sh small -> 1024^2 seed 1 (finite-size check).
S=$(cd "$(dirname "$0")/../.." && pwd); PY=${PY:-python3}   # PY: the Python environment with numpy, scipy, scikit-image
cd $S/scripts || exit 1
$PY test_rm_count.py | tail -1 && $PY test_pairing.py | tail -1 && $PY test_eventlog.py | tail -1 || { echo "FINAL FAIL (unit tests)"; exit 1; }
R=$S/scaling/results; mkdir -p $R; cd $S/scaling
one() { name=$1; shift; $PY scripts/froth_scaling.py $R/$name "$@" > $R/$name.log 2>&1 && \
        $PY scripts/count_scaling.py $R/$name $R/${name}_count.json >> $R/$name.log 2>&1; }
if [ "$1" = big ]; then
  one L2048_s1 L=2048 N0=262144 T=0.3 mcs=4000 stats=10 win0=1000 win1=4000 seed=1 &
  P1=$!
  one L2048_s2 L=2048 N0=262144 T=0.3 mcs=4000 stats=10 win0=1000 win1=4000 seed=2 &
  P2=$!
  NAMES="L2048_s1 L2048_s2"
  ( while sleep 60; do echo "PROGRESS $(cat $R/L2048_s1.log $R/L2048_s2.log 2>/dev/null | grep -cE '^(FROTH_OK|COUNT_OK|COUNT_NOT_STATIONARY)')/4 parts done"; done ) &
  HB=$!
  wait $P1 $P2
else
  one L1024_s1 L=1024 N0=65536 T=0.3 mcs=4000 stats=10 win0=1000 win1=4000 seed=1 &
  P1=$!
  NAMES="L1024_s1"
  ( while sleep 60; do echo "PROGRESS $(cat $R/L1024_s1.log 2>/dev/null | grep -cE '^(FROTH_OK|COUNT_OK|COUNT_NOT_STATIONARY)')/2 parts done"; done ) &
  HB=$!
  wait $P1
fi
kill $HB
n=0; k=0
for nm in $NAMES; do echo "== $nm"; grep -v PROGRESS $R/$nm.log | tail -12; k=$((k+1))
  grep -q '^FROTH_OK' $R/$nm.log && grep -qE '^(COUNT_OK|COUNT_NOT_STATIONARY)' $R/$nm.log && n=$((n+1)); done
gzip -t $R/*/frames.jsonl.gz && echo "frames gzip ok"
echo "runs finished with froth + analysis: $n / $k"
[ "$n" -eq "$k" ] && echo "FINAL ok" || echo "FINAL FAIL"
