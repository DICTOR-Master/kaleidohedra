#!/bin/bash
# Job sun-tilt-pilot (README section "Space-time slicing at a tilt", 16 Nov 2026): build 6 labelled space-time blocks, cut each at
# 5 directions (theta 0, 15, 30 degrees at v = 3 km/s; theta 30 at v = 1.5 and 6 km/s), log events. FINAL ok only if every block
# and every slice run finished and the moving-Voronoi theta = 0 run has no interior births (its known answer).
S=$(cd "$(dirname "$0")/.." && pwd); PY=${PY:-python3}; T=scripts/spacetime_tilt.py
cd $S || exit 1
D=data/tilt; R=results/tilt-pilot; mkdir -p $D $R/logs
B=data/bifrost; SEG=data/trace3d/seg_dz0.1.npy
printf '%s\n' "sunA real 0.25 $B" "sunA shuf:7 0.25 $B" "sunB real $B $SEG" "sunB shuf:7 $B $SEG" "pv 3.0 1" "mv" | \
  xargs -P 6 -I{} bash -c "set -- {}; $PY $T block \$1 $D \${@:2} > $R/logs/block_\$1_\${2//:/}.log 2>&1; echo done" | \
  while read x; do n=$((n+1)); echo "PROGRESS $(python3 -c "print(f'{0.4 * $n / 6:.3f}')") blocks $n/6"; done
nb=$(cat $R/logs/block_*.log | grep -c '^BLOCK_OK'); echo "PROGRESS 0.40 blocks ok $nb of 6"
grep -h '^BLOCK ' $R/logs/block_*.log > $R/blocks.jsonl
for f in $D/*.npz; do for dir in "0 3" "15 3" "30 3" "30 1.5" "30 6"; do echo "$f $dir"; done; done > $R/tasks.txt
tot=$(wc -l < $R/tasks.txt); n=0
cat $R/tasks.txt | xargs -P 20 -L 1 bash -c "b=\$(basename \$0 .npz); $PY $T slice \$0 \$1 \$2 $R/\${b}_t\$1_v\$2.json > $R/logs/slice_\${b}_t\$1_v\$2.log 2>&1; echo done" | \
  while read x; do n=$((n+1)); echo "PROGRESS $(python3 -c "print(f'{0.4 + 0.6 * $n / $tot:.4f}')") slices $n/$tot"; done
ns=$(cat $R/logs/slice_*.log | grep -c '^SLICE_OK')
mvb=$($PY -c "import json; r=json.load(open('$R/mv_s1_t0_v3.json')); print(r['core_events'].get('birth',0)+r['core_events'].get('death',0))" 2>/dev/null)
echo "mv theta=0 core births+deaths: $mvb"
[ "$nb" = 6 ] && [ "$ns" = "$tot" ] && [ "$tot" = 30 ] && [ "$mvb" = 0 ] && echo "FINAL ok" || echo "FINAL FAIL (blocks $nb/6 slices $ns/$tot mv-births $mvb)"
