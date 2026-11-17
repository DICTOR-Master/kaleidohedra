#!/bin/bash
# Job sz-a: seed-2 control sequences regenerated (must reproduce the 16 Nov exact totals), shuffled copies (seed 7, the 16 Nov
# permutation rule), census of the 13 Sun settings (real frame order) and the four seed-1 Sun-like controls at six steps.
# Run in two foreground stages, each under 5 minutes: sz_a.sh gen, then sz_a.sh census (FINAL line from the census stage).
S=$(cd "$(dirname "$0")/.." && pwd); PY=${PY:-python3}; cd $S || exit 1
OLD=../2026-11-15-sun-granulation
if [ "$1" = gen ]; then
mkdir -p work/control-s2 work/order data/sun data/control data/holdout data/order results/logs
printf '%s\n' "1 0" "1 1" "2 0" "2 1" | xargs -P 4 -L 1 bash -c \
  "$PY scripts/control_voronoi.py work/control-s2 500 120 \$0 \$1 2 | grep -v PROGRESS > results/logs/data_s2_v\$0_z\$1.log 2>&1"
rep=0
for V in 1 2; do for Z in 0 1; do
  a=$($PY -c "import json;print(json.load(open('$OLD/data/control-s2/voronoi_n500_v$V.0_z$Z.0_s2_exact.json'))['exact_swaps_total'])")
  b=$(grep '^EXACT' results/logs/data_s2_v${V}_z${Z}.log | awk '{print $3}')
  echo "REPRO seed2 v$V z$Z exact 16 Nov $a now $b"; [ -n "$b" ] && [ "$a" = "$b" ] && rep=$((rep+1))
done; done
echo "PROGRESS 0.20 seed-2 sequences ($rep of 4 reproduce)"
$PY scripts/prep_order.py $OLD/data/bifrost en024048_hion uz 0.1 work/order shuf 7 | grep -v PROGRESS > results/logs/prep_en_uz.log
$PY scripts/prep_order.py $OLD/data/bifrost en024048_hion lgtg 0.0 work/order shuf 7 | grep -v PROGRESS > results/logs/prep_en_T.log
$PY scripts/prep_order.py $OLD/data/bifrost qs024048_by3363 uz 0.1 work/order shuf 7 | grep -v PROGRESS > results/logs/prep_qs_uz.log
$PY scripts/prep_order.py $OLD/data/control-s1 voronoi_n500_v1.0_z0.0_s1 img 0.0 work/order shuf 7 | grep -v PROGRESS > results/logs/prep_ctl.log
prep=$(grep -l '^FINAL ok' results/logs/prep_*.log | wc -l); echo "PROGRESS 0.30 shuffled copies ($prep of 4 ok)"
echo "GEN seed2 $rep prep $prep" > results/logs/gen.status
[ $rep = 4 ] && [ $prep = 4 ] && echo "GEN ok" || echo "GEN FAIL"; exit 0
fi
read _ _ rep _ prep < results/logs/gen.status
$PY scripts/run_matrix.py data/configs_a.jsonl 22 2>&1 | tee results/logs/matrix_a.log | grep --line-buffered -E "PROGRESS|Error"
grep -q MATRIX_OK results/logs/matrix_a.log && [ $rep = 4 ] && [ $prep = 4 ] && echo "FINAL ok" || echo "FINAL FAIL (seed2 repro $rep/4, prep $prep/4)"
