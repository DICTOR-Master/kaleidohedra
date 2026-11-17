#!/bin/bash
# Jobs of this study, each a foreground stage under 5 minutes:
#   jobs.sh pilot  primary setting, 80 snapshots, steps 10 and 80 s, tau 80 and 160 s; null with N = 2000
#   jobs.sh gen    shuffled-frame copies (the 17 Nov permutation, seed 7) of the five fields used, into work/order
#   jobs.sh real   the 16 settings, real frame order        -> data/net/TAG.json
#   jobs.sh shuf   the 16 settings, shuffled frames         -> data/net/TAG-shuf.json
#   jobs.sh null   the null curve, N = 20 000, 4 repetitions -> data/null/null_net.json
# PY: a Python with numpy, scipy, scikit-image. The Bifrost planes are read from the 15 Nov study's data folder.
S=$(cd "$(dirname "$0")/.." && pwd); PY=${PY:-python3}; cd $S || exit 1
OLD=../2026-11-15-sun-granulation/data/bifrost; NW=${NW:-16}
mkdir -p data/net data/null results/logs results/pilot work/order
case "$1" in
pilot)
  $PY scripts/net_sz.py $OLD en024048_hion uz 0.1 1.5 thr:0.25 results/pilot/net_primary.json 80 steps=1,8 tauf=8,16 | tee results/pilot/net.log
  $PY scripts/null_net.py results/pilot/null.json 2000 2 | tee results/pilot/null.log
  grep -q 'FINAL ok' results/pilot/net.log && echo "FINAL ok" || echo "FINAL FAIL (pilot net)";;
gen)
  n=0
  for f in "en024048_hion uz 0.1" "en024048_hion uz 0.0" "en024048_hion uz 0.2" "en024048_hion lgtg 0.0" "qs024048_by3363 uz 0.1" "qs024048_by3363 uz 0.2"; do
    set -- $f
    $PY ../2026-11-17-sun-step-zero/scripts/prep_order.py $OLD $1 $2 $3 work/order shuf 7 | grep -v PROGRESS > results/logs/prep_$1_$2_$3.log
    grep -q 'FINAL ok' results/logs/prep_$1_$2_$3.log && n=$((n+1))
  done
  [ $n = 6 ] && echo "FINAL ok" || echo "FINAL FAIL (prep $n of 6)";;
real|shuf)
  if [ $1 = real ]; then D=$OLD; SUF=""; else D=work/order; SUF="-shuf"; fi
  cat scripts/settings.txt | xargs -P $NW -L 1 bash -c \
    "$PY scripts/net_sz.py $D \$1$SUF \$2 \$3 \$4 \$5 data/net/\$0$SUF.json > results/logs/net_\$0$SUF.log 2>&1"
  [ $1 = real ] && n=$(for t in $(awk '{print $1}' scripts/settings.txt); do grep -l 'FINAL ok' results/logs/net_$t.log; done | wc -l)
  [ $1 = shuf ] && n=$(for t in $(awk '{print $1}' scripts/settings.txt); do grep -l 'FINAL ok' results/logs/net_$t-shuf.log; done | wc -l)
  [ $n = 16 ] && echo "FINAL ok ($1: 16 of 16)" || echo "FINAL FAIL ($1: $n of 16)";;
null)
  $PY scripts/null_net.py data/null/null_net.json 20000 4 | tee results/logs/null.log | grep -v PROGRESS | tail -3;;
*) echo "usage: jobs.sh pilot|gen|real|shuf|null"; exit 1;;
esac
