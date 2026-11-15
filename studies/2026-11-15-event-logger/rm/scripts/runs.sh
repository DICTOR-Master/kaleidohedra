# Rutenberg-McCurdy count runs: sphere control (4 runs, 2 steps), foam rung 1 (2 seeds, full 1500 MCS regenerated), in parallel.
S=$(cd "$(dirname "$0")/../.." && pwd); PY=${PY:-python3}   # PY: the Python environment with numpy and scipy
cd $S/scripts || exit 1
$PY test_rm_count.py | tail -1 && $PY test_macro.py | tail -1 && $PY test_pairing.py | tail -1 && $PY test_eventlog.py | tail -1 || { echo "FINAL FAIL (unit tests)"; exit 1; }
R=$S/rm/results; mkdir -p $R; cd $S/rm
run() { name=$1; shift; timeout 3000 $PY "$@" > $R/$name.log 2>&1; }
run sphere_voronoi_1 scripts/rm_sphere.py voronoi 100 1 0.5 $R/sphere_voronoi_1.json 1e-4 1e-5 &
P1=$!
run sphere_voronoi_2 scripts/rm_sphere.py voronoi 100 2 0.5 $R/sphere_voronoi_2.json 1e-4 1e-5 &
P2=$!
run sphere_power_1 scripts/rm_sphere.py power 100 1 0.5 $R/sphere_power_1.json 1e-4 1e-5 &
P3=$!
run sphere_power_2 scripts/rm_sphere.py power 100 2 0.5 $R/sphere_power_2.json 1e-4 1e-5 &
P4=$!
run foam_s1 scripts/rm_foam.py $S/pairing/results/foam_s1_frames.jsonl.gz $R/foam_s1.json seed=1 &
P5=$!
run foam_s2 scripts/rm_foam.py $S/pairing/results/foam_s2_frames.jsonl.gz $R/foam_s2.json seed=2 &
P6=$!
( while sleep 30; do echo "PROGRESS $(find $R -maxdepth 1 -name "*.json" | wc -l)/6 runs done"; done ) &
HB=$!
wait $P1 $P2 $P3 $P4 $P5 $P6
kill $HB
for f in $R/*.log; do echo "== $f"; grep -v PROGRESS $f | tail -22; done
n=$(cat $R/sphere_*.log | grep -c '^RM_SPHERE_OK'); f=$(cat $R/foam_s*.log | grep -c '^RM_FOAM_OK')
echo "sphere ok $n/4, foam ok $f/2"
[ "$n" -eq 4 ] && [ "$f" -eq 2 ] && echo "FINAL ok" || echo "FINAL FAIL"
