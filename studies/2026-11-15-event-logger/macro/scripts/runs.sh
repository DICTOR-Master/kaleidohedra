# Macroscopic-count runs: sphere control (4 runs), foam rung 1 (2 seeds, full), Earth Muller 2016 (both readings), in parallel.
S=~/k-research/studies/2026-11-15-event-logger; PY=~/venvs/sun/bin/python
cd $S/scripts || exit 1
$PY test_macro.py | tail -1 && $PY test_pairing.py | tail -1 && $PY test_eventlog.py | tail -1 || { echo "FINAL FAIL (unit tests)"; exit 1; }
R=$S/macro/results; cd $S/macro
run() { name=$1; shift; timeout 3000 $PY "$@" > $R/$name.log 2>&1; }
run sphere_voronoi_1 scripts/sphere_macro.py voronoi 100 1 0.5 $R/sphere_voronoi_1.json 1e-4 1e-5 &
P1=$!
run sphere_voronoi_2 scripts/sphere_macro.py voronoi 100 2 0.5 $R/sphere_voronoi_2.json 1e-4 1e-5 &
P2=$!
run sphere_power_1 scripts/sphere_macro.py power 100 1 0.5 $R/sphere_power_1.json 1e-4 1e-5 &
P3=$!
run sphere_power_2 scripts/sphere_macro.py power 100 2 0.5 $R/sphere_power_2.json 1e-4 1e-5 &
P4=$!
run foam_s1 scripts/foam_macro.py $S/pairing/results/foam_s1_frames.jsonl.gz $R/foam_s1.json &
P5=$!
run foam_s2 scripts/foam_macro.py $S/pairing/results/foam_s2_frames.jsonl.gz $R/foam_s2.json &
P6=$!
run earth scripts/earth_macro.py $R/earth.json &
P7=$!
( while sleep 30; do echo "PROGRESS $(find $R -maxdepth 1 -name "*.json" | wc -l)/7 runs done"; done ) &
HB=$!
wait $P1 $P2 $P3 $P4 $P5 $P6 $P7
kill $HB
for f in $R/*.log; do echo "== $f"; grep -v PROGRESS $f | tail -22; done
n=$(cat $R/sphere_*.log | grep -c '^SPHERE_MACRO_OK'); f=$(cat $R/foam_s*.log | grep -c '^FOAM_MACRO_OK'); e=$(grep -c '^EARTH_MACRO_OK' $R/earth.log)
echo "sphere ok $n/4, foam ok $f/2, earth ok $e/1"
[ "$n" -eq 4 ] && [ "$f" -eq 2 ] && [ "$e" -eq 1 ] && echo "FINAL ok" || echo "FINAL FAIL"
