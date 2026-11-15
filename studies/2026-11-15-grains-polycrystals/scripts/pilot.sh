# GRAINS pilot: 2D vertex model variants (von Neumann accuracy vs K, straight-short threshold, eps) and a 3D MBO smoke run.
S=~/k-research/studies/2026-11-15-grains-polycrystals; PY=~/venvs/sun/bin/python
cd $S || exit 1; R=results/pilot; mkdir -p $R
v() { name=$1; shift; timeout 290 $PY scripts/vertex2d.py $R/$name "$@" maxwall=200 > $R/$name.log 2>&1 && timeout 80 $PY scripts/census2d.py $R/$name $R/$name.census.json >> $R/$name.log 2>&1; }
v k3 N0=2000 Nend=600 K=3 seed=1 & P1=$!
v k6 N0=2000 Nend=600 K=6 seed=1 & P2=$!
v k6l2 N0=2000 Nend=600 K=6 lamf=2 seed=1 & P3=$!
v k6e025 N0=2000 Nend=600 K=6 eps=0.025 seed=1 & P4=$!
v k10l2 N0=2000 Nend=600 K=10 lamf=2 seed=1 & P5=$!
timeout 290 $PY scripts/mbo3d.py $R/m3 n=64 N0=600 Nend=200 maxwall=200 > $R/m3.log 2>&1 & P6=$!
( while sleep 20; do echo "PROGRESS $(ls $R/*/final.json 2>/dev/null | wc -l)/6 runs done"; done ) & HB=$!
wait $P1 $P2 $P3 $P4 $P5 $P6; kill $HB
n=$(grep -l CENSUS2D_OK $R/*.log | wc -l); m=$(grep -c MBO3D $R/m3.log)
echo "census ok $n/5, mbo $m/1"
[ "$n" = 5 ] && [ "$m" = 1 ] && echo "FINAL ok" || echo "FINAL FAIL"
