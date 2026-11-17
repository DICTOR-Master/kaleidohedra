#!/bin/bash
# Jobs of this study, each a foreground stage under 5 minutes:
#   jobs.sh pilot  primary setting, 80 snapshots, steps 10 and 80 s, tau 80 and 160 s; null (main, V2) and calibration with N = 2000
#   jobs.sh gen    shuffled-frame copies (the 17 Nov permutation, seed 7) of the six fields used, into work/order
#   jobs.sh real   the 16 settings, real frame order, steps 10 and 80 s -> data/lin/TAG.json
#   jobs.sh shuf   the 16 settings, shuffled frames, step 10 s         -> data/lin/TAG-shuf.json
#   jobs.sh null   16 settings x (main, V1, V2) + calibration, N = 20 000, 4 repetitions -> data/null/
#   jobs.sh fit    tables, criteria, figure (lin_fit.py)
# PY: a Python with numpy, scipy, scikit-image, matplotlib. Bifrost planes are read from the 15 Nov study's data folder.
S=$(cd "$(dirname "$0")/.." && pwd); PY=${PY:-python3}; cd $S || exit 1
OLD=../2026-11-15-sun-granulation/data/bifrost; PAR=../2026-11-18-sun-net-change/data/net; NW=${NW:-16}
mkdir -p data/lin data/null results/logs results/pilot work/order
case "$1" in
pilot)
  $PY scripts/lin_sun.py $OLD en024048_hion uz 0.1 1.5 thr:0.25 results/pilot/lin_primary.json $PAR/en_uz0.1_s1.5_thr0.25.json 80 steps=1,8 tauf=8,16 | tee results/pilot/lin.log
  $PY scripts/lin_null.py en_uz0.1_s1.5_thr0.25 main results/pilot/null_main.json 2000 1 | tee results/pilot/null_main.log
  $PY scripts/lin_null.py en_uz0.1_s1.5_thr0.25 V2 results/pilot/null_V2.json 2000 1 | tee results/pilot/null_V2.log
  $PY scripts/lin_null.py calib calib results/pilot/null_calib.json 2000 2 | tee results/pilot/null_calib.log
  grep -q 'FINAL ok' results/pilot/lin.log && grep -q 'FINAL ok' results/pilot/null_main.log && grep -q 'FINAL ok' results/pilot/null_V2.log \
    && grep -q "'lineage_equals_plain': True" results/pilot/null_calib.log && echo "FINAL ok" || echo "FINAL FAIL (pilot)";;
gen)
  n=0
  for f in "en024048_hion uz 0.1" "en024048_hion uz 0.0" "en024048_hion uz 0.2" "en024048_hion lgtg 0.0" "qs024048_by3363 uz 0.1" "qs024048_by3363 uz 0.2"; do
    set -- $f
    $PY ../2026-11-17-sun-step-zero/scripts/prep_order.py $OLD $1 $2 $3 work/order shuf 7 | grep -v PROGRESS > results/logs/prep_$1_$2_$3.log
    grep -q 'FINAL ok' results/logs/prep_$1_$2_$3.log && n=$((n+1))
  done
  [ $n = 6 ] && echo "FINAL ok" || echo "FINAL FAIL (prep $n of 6)";;
real|shuf)
  if [ $1 = real ]; then D=$OLD; SUF=""; ST=1,8; else D=work/order; SUF="-shuf"; ST=1; fi
  cat scripts/settings.txt | xargs -P $NW -L 1 bash -c \
    "$PY scripts/lin_sun.py $D \$1$SUF \$2 \$3 \$4 \$5 data/lin/\$0$SUF.json $PAR/\$0$SUF.json all steps=$ST > results/logs/lin_\$0$SUF.log 2>&1"
  n=$(for t in $(awk '{print $1}' scripts/settings.txt); do grep -l 'FINAL ok' results/logs/lin_$t$SUF.log; done | wc -l)
  [ $n = 16 ] && echo "FINAL ok ($1: 16 of 16)" || echo "FINAL FAIL ($1: $n of 16)";;
null)
  { awk '{print NR-1, $1, "main"; print NR-1, $1, "V1"; print NR-1, $1, "V2"}' scripts/settings.txt; echo "0 calib calib"; } | \
    xargs -P ${NW} -L 1 bash -c "$PY scripts/lin_null.py \$1 \$2 data/null/\$1_\$2.json 20000 4 \$0 > results/logs/null_\$1_\$2.log 2>&1"
  n=$(grep -l 'FINAL ok' results/logs/null_*.log | wc -l)
  [ $n = 49 ] && echo "FINAL ok (null: 49 of 49)" || echo "FINAL FAIL (null: $n of 49)";;
fit)
  $PY scripts/lin_fit.py | tee results/logs/fit.log | tail -4;;
*) echo "usage: jobs.sh pilot|gen|real|shuf|null|fit"; exit 1;;
esac
