S=$(cd "$(dirname "$0")/.." && pwd); PY=${PY:-python3}   # PY: a Python with numpy, scipy, scikit-image, matplotlib
mkdir -p $S/data/control $S/results/control && cd $S || exit 1
: > results/control/configs.jsonl
n=0
for V in 1 2 4; do for Z in 0 1; do
  $PY scripts/control_voronoi.py data/control 500 120 $V $Z 1 > results/control/data_v${V}_z${Z}.log 2>&1 || echo "data v$V z$Z failed"
  n=$((n+1)); echo "PROGRESS $(echo "scale=3; $n/12" | bc) control data v$V z$Z"
  name=voronoi_n500_v$V.0_z$Z.0_s1
  if [ $Z = 0 ]; then sg=0; h=hmax:0.01; else sg=1.5; h=hmax:0.5; fi
  echo "{\"data\": \"data/control\", \"run\": \"$name\", \"var\": \"img\", \"dz\": 0.0, \"sigma\": $sg, \"h\": \"$h\", \"steps\": [1, 2, 4, 8], \"W\": 60, \"out\": \"results/control/$name.json\"}" >> results/control/configs.jsonl
done; done
$PY scripts/run_matrix.py results/control/configs.jsonl 3 2>&1 | tee results/control/matrix.log | grep --line-buffered PROGRESS
grep -q MATRIX_OK results/control/matrix.log && [ $(grep -c CONTROL_DATA_OK results/control/data_v*.log | grep -c ':1') = 6 ] && echo "FINAL ok" || echo "FINAL FAIL"
