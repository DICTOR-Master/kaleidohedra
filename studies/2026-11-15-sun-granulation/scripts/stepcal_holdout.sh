#!/bin/bash
# Held-out control for the step calibration (README section "Swap rate at step 0", 16 Nov 2026): new moving-Voronoi sequences with
# seed 2 at the Sun-like speeds 1 and 2, texture 0 and 1, through the same chain at the same steps. They are NOT used to calibrate;
# stepcal_fit.py corrects them with the seed-1 detection fractions and compares with their exact counts.
S=$(cd "$(dirname "$0")/.." && pwd); PY=${PY:-python3}
cd $S || exit 1
mkdir -p data/control-s2 results/stepcal/holdout results/stepcal/logs
printf '%s\n' "1 0" "1 1" "2 0" "2 1" | xargs -P 4 -L 1 bash -c \
  "$PY scripts/control_voronoi.py data/control-s2 500 120 \$0 \$1 2 | grep -v PROGRESS > results/stepcal/logs/data_s2_v\$0_z\$1.log 2>&1"
ok=$(grep -l CONTROL_DATA_OK results/stepcal/logs/data_s2_*.log | wc -l); echo "PROGRESS 0.25 seed-2 sequences ($ok of 4 ok)"
C=results/stepcal/holdout/configs.jsonl; : > $C
for V in 1 2; do for Z in 0 1; do
  name=voronoi_n500_v$V.0_z$Z.0_s2
  if [ $Z = 0 ]; then sg=0; h=hmax:0.01; else sg=1.5; h=hmax:0.5; fi
  echo "{\"data\": \"data/control-s2\", \"run\": \"$name\", \"var\": \"img\", \"dz\": 0.0, \"sigma\": $sg, \"h\": \"$h\", \"steps\": [1, 2, 3, 4, 6, 8], \"W\": 60, \"out\": \"results/stepcal/holdout/$name.json\"}" >> $C
done; done
$PY scripts/run_matrix.py $C 4 2>&1 | tee results/stepcal/holdout/matrix.log | grep --line-buffered -E "PROGRESS|Error"
grep -q MATRIX_OK results/stepcal/holdout/matrix.log && [ $ok = 4 ] && echo "FINAL ok" || echo "FINAL FAIL (data $ok/4)"
