# Macroscopic-count pilot: unit tests, sphere control (short span), foam rung 1 (first 200 frames), Earth (full, small), in parallel.
S=~/k-research/studies/2026-11-15-event-logger; PY=~/venvs/sun/bin/python
cd $S/scripts || exit 1
$PY test_macro.py | tail -1 && $PY test_pairing.py | tail -1 && $PY test_eventlog.py | tail -1 || { echo "FINAL FAIL (unit tests)"; exit 1; }
R=$S/macro/results/pilot; mkdir -p $R; cd $S/macro
timeout 280 $PY scripts/sphere_macro.py voronoi 100 1 0.02 $R/sphere_v1.json 1e-4 1e-5 > $R/sphere_v1.log 2>&1 &
P1=$!
timeout 280 $PY scripts/foam_macro.py $S/pairing/results/foam_s1_frames.jsonl.gz $R/foam_s1.json 200 > $R/foam_s1.log 2>&1 &
P2=$!
timeout 280 $PY scripts/earth_macro.py $R/earth.json > $R/earth.log 2>&1 &
P3=$!
( while sleep 20; do echo "PROGRESS $(find $R -name "*.json" | wc -l)/3 parts done"; done ) &
HB=$!
wait $P1 $P2 $P3
kill $HB
for f in $R/*.log; do echo "== $f"; grep -v PROGRESS $f | tail -14; done
grep -q '^SPHERE_MACRO_OK' $R/sphere_v1.log && grep -q '^FOAM_MACRO_OK' $R/foam_s1.log && grep -q '^EARTH_MACRO_OK' $R/earth.log && echo "FINAL ok" || echo "FINAL FAIL"
