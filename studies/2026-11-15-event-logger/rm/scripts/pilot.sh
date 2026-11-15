# Rutenberg-McCurdy count pilot: unit tests, sphere control (short span), foam rung 1 seed 1 regenerated for 200 MCS (identity with the saved frames + counts).
S=$(cd "$(dirname "$0")/../.." && pwd); PY=${PY:-python3}   # PY: the Python environment with numpy and scipy
cd $S/scripts || exit 1
$PY test_rm_count.py | tail -1 && $PY test_macro.py | tail -1 && $PY test_pairing.py | tail -1 && $PY test_eventlog.py | tail -1 || { echo "FINAL FAIL (unit tests)"; exit 1; }
$PY test_rm_count.py | grep -v '^PASS'
R=$S/rm/results/pilot; mkdir -p $R; cd $S/rm
timeout 280 $PY scripts/rm_sphere.py voronoi 100 1 0.02 $R/sphere_v1.json 1e-4 1e-5 > $R/sphere_v1.log 2>&1 &
P1=$!
timeout 280 $PY scripts/rm_sphere.py power 100 1 0.02 $R/sphere_p1.json 1e-4 1e-5 > $R/sphere_p1.log 2>&1 &
P2=$!
timeout 280 $PY scripts/rm_foam.py $S/pairing/results/foam_s1_frames.jsonl.gz $R/foam_s1.json seed=1 mcs=200 > $R/foam_s1.log 2>&1 &
P3=$!
( while sleep 20; do echo "PROGRESS $(find $R -name "*.json" | wc -l)/3 parts done"; done ) &
HB=$!
wait $P1 $P2 $P3
kill $HB
for f in $R/*.log; do echo "== $f"; grep -v PROGRESS $f | tail -16; done
grep -q '^RM_SPHERE_OK' $R/sphere_v1.log && grep -q '^RM_SPHERE_OK' $R/sphere_p1.log && grep -q '^RM_FOAM_OK' $R/foam_s1.log && echo "FINAL ok" || echo "FINAL FAIL"
