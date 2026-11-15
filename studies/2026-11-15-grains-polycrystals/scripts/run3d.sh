# GRAINS full 3D run (MBO threshold dynamics) + census. Usage: run3d.sh NAME n N0 Nend
S=~/k-research/studies/2026-11-15-grains-polycrystals; PY=~/venvs/sun/bin/python
cd $S || exit 1; R=results/m3d; mkdir -p $R
( while sleep 60; do echo "PROGRESS $(tail -1 $R/$1/stats.jsonl 2>/dev/null | cut -c1-80)"; done ) & HB=$!
$PY scripts/mbo3d.py $R/$1 n=$2 N0=$3 Nend=$4 c=0.8 sigmin=2.5 rec_frac=0.0 maxwall=${5:-14000} > $R/$1.log 2>&1 && \
$PY scripts/census3d.py $R/$1 $R/$1.census.json >> $R/$1.log 2>&1
kill $HB
grep -q CENSUS3D_OK $R/$1.log && echo "FINAL ok" || echo "FINAL FAIL"
