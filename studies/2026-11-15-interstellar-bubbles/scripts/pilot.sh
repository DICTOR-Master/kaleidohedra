# Foam ladder pilot: every rung once (rung 1 also with a second seed and at T = 0), the bubble toy at two time steps,
# a second threshold, a larger marker size and a second seed.
S=~/k-research/studies/2026-11-15-interstellar-bubbles; PY=~/venvs/sun/bin/python
cd $S || exit 1; mkdir -p results/pilot; R=results/pilot
run() { name=$1; shift; timeout 280 $PY scripts/ladder.py "$@" > $R/$name.log 2>&1; }
run r1_dry2d_s1 dry2d $R/r1_dry2d_s1.json seed=1 mcs=1500 rec=1 &
P1=$!
run r1_dry2d_s2 dry2d $R/r1_dry2d_s2.json seed=2 mcs=1500 rec=1 &
P2=$!
run r1_dry2d_T0 dry2d $R/r1_dry2d_T0.json seed=1 mcs=1500 rec=1 T=0 &
P3=$!
run r2_wet2d wet2d $R/r2_wet2d.json seed=1 mcs=1500 rec=1 &
P4=$!
run r3_dry3d dry3d $R/r3_dry3d.json seed=1 L=40 N=600 mcs=300 rec=1 &
P5=$!
run r4_births2d births2d $R/r4_births2d.json seed=1 mcs=1500 rec=1 nuc_rate=0.5 &
P6=$!
run r5_ism_dt1 ism2d $R/r5_ism_dt1.json seed=1 dt=1 &
P7=$!
run r5_ism_dt025 ism2d $R/r5_ism_dt025.json seed=1 dt=0.25 &
P8=$!
run r5_ism_theta02 ism2d $R/r5_ism_theta02.json seed=1 dt=0.25 theta=0.2 &
P9=$!
run r5_ism_amin16 ism2d $R/r5_ism_amin16.json seed=1 dt=0.25 amin=16 &
P10=$!
run r5_ism_s2 ism2d $R/r5_ism_s2.json seed=2 dt=0.25 &
P11=$!
( while sleep 20; do echo "PROGRESS $(ls $R/*.json 2>/dev/null | wc -l)/11 runs done"; done ) &
HB=$!
wait $P1 $P2 $P3 $P4 $P5 $P6 $P7 $P8 $P9 $P10 $P11
kill $HB 2>/dev/null
n_ok=$(grep -l '^LADDER_OK' $R/*.log | wc -l); echo "runs LADDER_OK: $n_ok / 11"
for f in $R/*.log; do echo "== $f"; grep -v PROGRESS $f | tail -3; done
[ "$n_ok" -eq 11 ] && echo "FINAL ok" || echo "FINAL FAIL"
