# GRAINS full 2D runs (curved vertex model) + census; frames deleted after the census except seed 1 (gzipped).
S=~/k-research/studies/2026-11-15-grains-polycrystals; PY=~/venvs/sun/bin/python
cd $S || exit 1; R=results/v2d; mkdir -p $R
v() { name=$1; shift; $PY scripts/vertex2d.py $R/$name "$@" rec_frac=0.002 maxwall=16000 > $R/$name.log 2>&1 && \
      $PY scripts/census2d.py $R/$name $R/$name.census.json >> $R/$name.log 2>&1; \
      if [ "$name" = k3e05s1 ]; then gzip -f $R/$name/frames.jsonl; else rm -f $R/$name/frames.jsonl; fi; }
v k3e05s1 N0=20000 Nend=1500 K=3 eps=0.05 seed=1 & P1=$!
v k3e05s2 N0=20000 Nend=1500 K=3 eps=0.05 seed=2 & P2=$!
v k3e05s3 N0=20000 Nend=1500 K=3 eps=0.05 seed=3 & P3=$!
v k3e025s1 N0=20000 Nend=1500 K=3 eps=0.025 seed=1 & P4=$!
v k3e10s1 N0=20000 Nend=1500 K=3 eps=0.1 seed=1 & P5=$!
v k6e05s1 N0=8000 Nend=800 K=6 eps=0.05 seed=1 & P6=$!
( while sleep 60; do echo "PROGRESS $(ls $R/*.census.json 2>/dev/null | wc -l)/6 runs censused"; done ) & HB=$!
wait $P1 $P2 $P3 $P4 $P5 $P6; kill $HB
n=$(grep -l CENSUS2D_OK $R/*.log | wc -l); echo "census ok $n/6"
[ "$n" = 6 ] && echo "FINAL ok" || echo "FINAL FAIL"
