#!/bin/bash
# Job sun-tilt-pilot2 (16 Nov 2026, at most 5 min): pilot of the full-run code (scripts/spacetime_tilt.py with quadrants, azimuths,
# reversal, labelling A2) and of Part B (scripts/spacetime_scutoids.py, granule tubes: prisms and scutoids). Measures times;
# FINAL ok only if every task ended with its OK line (the reversal comparison is printed, not gated: see the plan).
S=$(cd "$(dirname "$0")/.." && pwd); PY=${PY:-python3}; T=scripts/spacetime_tilt.py; U=scripts/spacetime_scutoids.py
cd $S || exit 1
D=data/tilt-p2; R=results/tilt-pilot2; mkdir -p $D $R/logs
B=data/bifrost
printf '%s\n' "sunB seg=data/trace3d/seg_dz0.0.npy dz=0.0 q=1" "sunA2 data=$B dz=0.1 q=2" "sunA data=$B dz=0.1 q=0 thr=1.0" \
  "pv vc=1.5 seed=2" "mv seed=2" | \
  xargs -P 5 -I{} bash -c "set -- {}; timeout 150 $PY $T block \$1 $D \${@:2} 2>&1 | tee $R/logs/block_\$1_\$3.log | grep -E '^(PROGRESS|BLOCK_OK)'"
nb=$(cat $R/logs/block_*.log | grep -c '^BLOCK_OK'); echo "PROGRESS 0.40 blocks ok $nb of 5"
grep -h '^BLOCK ' $R/logs/block_*.log > $R/blocks.jsonl
b1=$(ls $D/sunB_*.npz | head -1); b2=$(ls $D/sunA2_*.npz | head -1); b3=$(ls $D/sunA_*.npz | head -1); bp=$(ls $D/pv_*.npz | head -1); bm=$(ls $D/mv_*.npz | head -1)
cat > $R/tasks.txt <<EOF
$T slice $b1 20 3 -x $R/sunB_t20_-x.json
$T slice $b1 20 3 +y $R/sunB_t20_+y.json
$T slice $b2 30 3 +x $R/sunA2_t30_+x.json
$T slice $b3 30 3 +x $R/sunA_t30_+x.json
$T slice $bp 30 3 +x $R/pv_t30_+x.json
$T slice $bp 30 3 +x $R/pv_t30_+x_rev.json rev=1
$T slice $bm 10 3 +y $R/mv_t10_+y.json
$U sun data/trace3d/seg_dz0.1.npy $R/tubes_sun_step4.json step=4 tag=pilot
$U pv 1 3.0 $R/tubes_pv.json
$U mv 1 $R/tubes_mv.json
$U fig $S data/trace3d/seg_dz0.1.npy
$U sun data/trace3d/seg_dz0.1.npy $R/tubes_sun_shuf7.json order=shuf:7 tag=pilot-shuf
EOF
n=0; cat $R/tasks.txt | xargs -P 12 -L 1 bash -c "timeout 140 $PY \"\$@\" 2>&1 | tee $R/logs/task_\$(echo \"\$@\" | md5sum | cut -c1-8).log | grep -E '^(SLICE_OK|TUBES_OK|TUBES |FIG)'" _ | \
  while read x; do n=$((n+1)); echo "PROGRESS $(python3 -c "print(f'{0.4 + 0.6 * $n / 22:.3f}')") $x"; done
ok=$(cat $R/logs/task_*.log | grep -cE '^(SLICE_OK|TUBES_OK|FIG_OK)')
same=$($PY -c "import json; a=json.load(open('$R/pv_t30_+x.json')); b=json.load(open('$R/pv_t30_+x_rev.json')); print(int(a['core_swaps_all']==b['core_swaps_all'] and a['core_events'].get('birth',0)==b['core_events'].get('death',0)))" 2>&1)
echo "tasks ok $ok of 12; reversal check $same (pilot 1: the shared logger is not exactly mirror-symmetric; reported, not gated)"
[ "$nb" = 5 ] && [ "$ok" = 12 ] && echo "FINAL ok" || echo "FINAL FAIL (blocks $nb/5 tasks $ok/12)"
