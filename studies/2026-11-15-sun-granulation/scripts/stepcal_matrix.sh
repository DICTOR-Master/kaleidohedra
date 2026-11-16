#!/bin/bash
# Step calibration (README section "Swap rate at step 0", 16 Nov 2026): every Sun setting and every moving-Voronoi control at steps
# 10, 20, 30, 40, 60, 80 s (persistence windows P = 20, 30, 60, 120, 240 s come out of census.py in one pass), plus the frame-order
# controls (time-reversed and shuffled frames) for the primary Sun setting and the Sun-like control. census.py, tiles.py and the
# event logger are used unchanged. The control sequences are regenerated from their seed and must reproduce the exact totals of the
# 15 Nov run (results/control/data_*.log) before they are used.
S=$(cd "$(dirname "$0")/.." && pwd); PY=${PY:-python3}   # PY: a Python with numpy, scipy, scikit-image
cd $S || exit 1
mkdir -p data/control-s1 data/stepcal results/stepcal/sun results/stepcal/control results/stepcal/order results/stepcal/logs
STEPS='[1, 2, 3, 4, 6, 8]'
# 1. control sequences, seed 1 (as 15 Nov), six in parallel
printf '%s\n' "1 0" "1 1" "2 0" "2 1" "4 0" "4 1" | xargs -P 6 -L 1 bash -c \
  "$PY scripts/control_voronoi.py data/control-s1 500 120 \$0 \$1 1 | grep -v PROGRESS > results/stepcal/logs/data_v\$0_z\$1.log 2>&1"
echo "PROGRESS 0.20 control sequences written"
rep=0
for V in 1 2 4; do for Z in 0 1; do
  a=$(grep '^EXACT' results/control/data_v${V}_z${Z}.log | awk '{print $3}'); b=$(grep '^EXACT' results/stepcal/logs/data_v${V}_z${Z}.log | awk '{print $3}')
  echo "REPRO v$V z$Z exact 15 Nov $a now $b"; [ -n "$a" ] && [ "$a" = "$b" ] && rep=$((rep+1))
done; done
# 2. frame-order controls
$PY scripts/stepcal_prep.py data/bifrost en024048_hion uz 0.1 data/stepcal rev 0 | grep -v PROGRESS > results/stepcal/logs/prep_sun_rev.log
$PY scripts/stepcal_prep.py data/bifrost en024048_hion uz 0.1 data/stepcal shuf 7 | grep -v PROGRESS > results/stepcal/logs/prep_sun_shuf.log
$PY scripts/stepcal_prep.py data/control-s1 voronoi_n500_v1.0_z0.0_s1 img 0.0 data/stepcal rev 0 | grep -v PROGRESS > results/stepcal/logs/prep_ctl_rev.log
$PY scripts/stepcal_prep.py data/control-s1 voronoi_n500_v1.0_z0.0_s1 img 0.0 data/stepcal shuf 7 | grep -v PROGRESS > results/stepcal/logs/prep_ctl_shuf.log
prep=$(grep -l '^FINAL ok' results/stepcal/logs/prep_*.log | wc -l)
echo "PROGRESS 0.25 frame-order copies written ($prep of 4 ok)"
# 3. configurations
C=results/stepcal/configs.jsonl
$PY - "$STEPS" > $C <<'EOF'
import json, sys
steps = json.loads(sys.argv[1])
for l in open('scripts/sun_matrix.jsonl'):
    if not l.strip(): continue
    c = json.loads(l); c['steps'] = steps; c['out'] = c['out'].replace('results/census/', 'results/stepcal/sun/'); print(json.dumps(c))
for v in (1, 2, 4):
    for z in (0, 1):
        name = f'voronoi_n500_v{v}.0_z{z}.0_s1'
        sg, h = (0, 'hmax:0.01') if z == 0 else (1.5, 'hmax:0.5')
        print(json.dumps(dict(data='data/control-s1', run=name, var='img', dz=0.0, sigma=sg, h=h, steps=steps, W=60, out=f'results/stepcal/control/{name}.json')))
for m in ('rev', 'shuf'):
    print(json.dumps(dict(data='data/stepcal', run=f'en024048_hion-{m}', var='uz', dz=0.1, sigma=1.5, h='thr:0.25', steps=steps, W=60, out=f'results/stepcal/order/en_uz0.1_s1.5_thr0.25-{m}.json')))
    print(json.dumps(dict(data='data/stepcal', run=f'voronoi_n500_v1.0_z0.0_s1-{m}', var='img', dz=0.0, sigma=0, h='hmax:0.01', steps=steps, W=60, out=f'results/stepcal/order/voronoi_n500_v1.0_z0.0_s1-{m}.json')))
EOF
n=$(wc -l < $C); echo "PROGRESS 0.30 $n configurations"
# 4. census of every configuration
$PY scripts/run_matrix.py $C 22 2>&1 | tee results/stepcal/matrix.log | grep --line-buffered -E "PROGRESS|Error"
grep -q MATRIX_OK results/stepcal/matrix.log && [ $rep = 6 ] && [ $prep = 4 ] && [ $n = 27 ] && echo "FINAL ok" || echo "FINAL FAIL (repro $rep/6, prep $prep/4, configs $n/27)"
