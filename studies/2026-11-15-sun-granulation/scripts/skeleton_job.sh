#!/bin/bash
# Job sun-skeleton (README section "The skeleton: persistence or reappearance", 16 Nov 2026): features per frame at three depths
# of en024048_hion (census label maps of the depth trace) and at 0.1 Mm of qs024048_by3363 (segmented here), the analysis in
# real, time-reversed and shuffled frame order at steps 10, 20, 40, 80 s, and the moving-Voronoi control (speeds 1 and 2,
# texture 0 and 1). Ends FINAL ok only when every task passed.
S=$(cd "$(dirname "$0")/.." && pwd); PY=${PY:-python3}; T=scripts/skeleton.py
cd $S || exit 1
D=data/skeleton; R=results/skeleton; mkdir -p $D $R/logs $R/anal $R/voro
# 1. features (4)
{ for dz in 0.0 0.1 0.2; do echo "en024048_hion $dz data/trace3d/seg_dz$dz.npy"; done; echo "qs024048_by3363 0.1 -"; } > $D/feat_tasks.txt
cat $D/feat_tasks.txt | xargs -P 4 -L 1 bash -c "$PY $T feat data/bifrost \$0 \$1 \$2 $D/feat_\$0_dz\$1.pkl > $R/logs/feat_\$0_\$1.log 2>&1"
nf=$(cat $R/logs/feat_*.log | grep -c '^FEAT_OK'); echo "PROGRESS 0.10 features ($nf of 4)"; grep -h '^FEAT_OK' $R/logs/feat_*.log
# 2. analysis (4 planes x 3 orders x 4 steps = 48) and the control (4), one queue
: > $D/tasks.txt
for p in "en024048_hion 0.0" "en024048_hion 0.1" "en024048_hion 0.2" "qs024048_by3363 0.1"; do set -- $p
  seg=data/trace3d/seg_dz$2.npy; [ $1 = qs024048_by3363 ] && seg=-
  for o in shuf:7 real rev; do for s in 1 2 4 8; do echo "anal $D/feat_$1_dz$2.pkl $seg data/bifrost $1 $2 $o $s $R/anal/$1_dz$2_${o/:/}_s$s.json" >> $D/tasks.txt; done; done; done
for v in 1 2; do for z in 0 1; do echo "voro data/control-s1 voronoi_n500_v$v.0_z$z.0_s1 $v 1 $R/voro/v${v}_z$z.json" >> $D/tasks.txt; done; done
tot=$(wc -l < $D/tasks.txt); n=0
cat $D/tasks.txt | xargs -P 20 -L 1 bash -c "log=$R/logs/\$(basename \${@: -1} .json)_\$0.log; $PY $T \$0 \"\$@\" > \$log 2>&1; echo done" | while read x; do n=$((n+1)); echo "PROGRESS $(python3 -c "print(f'{0.10 + 0.88 * $n / $tot:.4f}')") tasks $n/$tot"; done
na=$(cat $R/logs/*_anal.log 2>/dev/null | grep -c '^ANAL_OK'); nv=$(cat $R/logs/*_voro.log 2>/dev/null | grep -c '^VORO_OK')
echo "PROGRESS 0.99 analysis $na of 48, control $nv of 4"
grep -L '^FINAL ok' $R/logs/*_anal.log $R/logs/*_voro.log | head -5
[ "$nf" = 4 ] && [ "$na" = 48 ] && [ "$nv" = 4 ] && echo "FINAL ok" || echo "FINAL FAIL (features $nf/4 analysis $na/48 control $nv/4)"
