# Scaling-froth pilot (5 min or less): unit tests; 1024^2 froth 200 MCS with frames 100-200 + forced count (blocks of 50);
# 2048^2 froth 30 MCS (sweep and frame timing).
S=$(cd "$(dirname "$0")/../.." && pwd); PY=${PY:-python3}   # PY: the Python environment with numpy, scipy, scikit-image
cd $S/scripts || exit 1
$PY test_rm_count.py | tail -1 && $PY test_pairing.py | tail -1 && $PY test_eventlog.py | tail -1 || { echo "FINAL FAIL (unit tests)"; exit 1; }
R=$S/scaling/results/pilot; mkdir -p $R; cd $S/scaling
( timeout 270 $PY scripts/froth_scaling.py $R/p1024 L=1024 N0=65536 mcs=200 stats=10 win0=100 win1=200 seed=1 > $R/p1024.log 2>&1 && \
  timeout 120 $PY scripts/count_scaling.py $R/p1024 $R/p1024_count.json block=50 force=1 >> $R/p1024.log 2>&1 ) &
P1=$!
timeout 270 $PY scripts/froth_scaling.py $R/p2048 L=2048 N0=262144 mcs=30 stats=10 win0=20 win1=30 seed=1 > $R/p2048.log 2>&1 &
P2=$!
( while sleep 20; do echo "PROGRESS $(grep -l '^FROTH_OK' $R/*.log 2>/dev/null | wc -l)/2 froths done"; done ) &
HB=$!
wait $P1 $P2
kill $HB
for f in $R/*.log; do echo "== $f"; grep -v PROGRESS $f | tail -8; grep PROGRESS $f | tail -2; done
grep -q '^FROTH_OK' $R/p1024.log && grep -q '^COUNT_FORCED_PILOT' $R/p1024.log && grep -q '^FROTH_OK' $R/p2048.log && echo "FINAL ok" || echo "FINAL FAIL"
