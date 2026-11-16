#!/bin/bash
# Job sun-skeleton2 (README section "The skeleton: persistence or reappearance", second pass written after reading the first
# results, 16 Nov 2026): families of fragmenting granules as time-weighted presence, re-formation of corners and sinks without
# the linking bias (true vanishings only, time-shifted null at the same place), lanes with the gap fix and quadrant errors.
# Same 48 plane x order x step cases as sun-skeleton. Ends FINAL ok only when every task passed.
S=$(cd "$(dirname "$0")/.." && pwd); PY=${PY:-python3}; T=scripts/skeleton.py
cd $S || exit 1
D=data/skeleton; R=results/skeleton; mkdir -p $R/anal2 $R/logs2
: > $D/tasks2.txt
for p in "en024048_hion 0.0" "en024048_hion 0.1" "en024048_hion 0.2" "qs024048_by3363 0.1"; do set -- $p
  seg=data/trace3d/seg_dz$2.npy; [ $1 = qs024048_by3363 ] && seg=-
  for o in shuf:7 real rev; do for s in 1 2 4 8; do echo "anal2 $D/feat_$1_dz$2.pkl $seg data/bifrost $1 $2 $o $s $R/anal2/$1_dz$2_${o/:/}_s$s.json" >> $D/tasks2.txt; done; done; done
tot=$(wc -l < $D/tasks2.txt); n=0
cat $D/tasks2.txt | xargs -P 20 -L 1 bash -c "log=$R/logs2/\$(basename \${@: -1} .json).log; $PY $T \$0 \"\$@\" > \$log 2>&1; echo done" | while read x; do n=$((n+1)); echo "PROGRESS $(python3 -c "print(f'{0.98 * $n / $tot:.4f}')") tasks $n/$tot"; done
na=$(cat $R/logs2/*.log | grep -c '^ANAL2_OK'); echo "PROGRESS 0.99 second pass $na of 48"
grep -L '^FINAL ok' $R/logs2/*.log | head -5
[ "$na" = 48 ] && echo "FINAL ok" || echo "FINAL FAIL (second pass $na/48)"
