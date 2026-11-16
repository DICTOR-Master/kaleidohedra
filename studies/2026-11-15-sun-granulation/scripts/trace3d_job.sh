#!/bin/bash
# Job sun-3d-trace (README section "Swaps traced through depth", 16 Nov 2026): fetch the extra uz planes (0.05, 0.15, 0.3 Mm),
# segment every depth, link adjacent depths, track every depth in real and shuffled frame order at six steps, combine.
# Ends FINAL ok only when every stage passed and the 0.1 Mm counts reproduce the census (733, 626, 484, 305; shuffled 767).
S=$(cd "$(dirname "$0")/.." && pwd); PY=${PY:-python3}; T=scripts/trace3d.py
cd $S || exit 1
D=data/trace3d; R=results/trace3d; mkdir -p $D $R/logs
DEPTHS="0.0 0.05 0.1 0.15 0.2 0.3 0.4"; STEPS="1 2 3 4 6 8"
# 1. planes
if [ ! -f data/bifrost/en024048_hion_depths_meta.json ]; then
  $PY scripts/fetch_depths.py en024048_hion 303 544 data/bifrost 0.05,0.15,0.3 > $R/logs/fetch.log 2>&1
fi
grep -q '^FINAL ok' $R/logs/fetch.log && fetch=1 || fetch=0
grep -v PROGRESS $R/logs/fetch.log | head -3
echo "PROGRESS 0.25 planes fetched (ok=$fetch)"
# 2. segmentation, one process per depth
printf '%s\n' $DEPTHS | xargs -P 7 -I{} bash -c "$PY $T seg data/bifrost en024048_hion {} $D > $R/logs/seg_{}.log 2>&1"
seg=$(cat $R/logs/seg_*.log | grep -c '^SEG_OK'); echo "PROGRESS 0.35 segmented ($seg of 7)"
# 3. links between adjacent depths
set -- $DEPTHS; prev=$1; shift; pairs=""
for d in "$@"; do pairs="$pairs $prev:$d"; prev=$d; done
printf '%s\n' $pairs | xargs -P 6 -I{} bash -c 'a=${0%%:*}; b=${0##*:}; '"$PY $T"' link '"$D"' $a $b > '"$R"'/logs/link_$a-$b.log 2>&1' {}
lnk=$(cat $R/logs/link_*.log | grep -c '^LINK_OK'); echo "PROGRESS 0.45 linked ($lnk of 6)"
# 4. tracks: 7 depths x 2 orders x 6 steps = 84
for o in real shuf:7; do for s in $STEPS; do for d in $DEPTHS; do echo "$d $o $s"; done; done; done > $D/tasks.txt
n=0; tot=$(wc -l < $D/tasks.txt)
cat $D/tasks.txt | xargs -P 20 -L 1 bash -c "$PY $T track data/bifrost en024048_hion $D \$0 \$1 \$2 60 > $R/logs/track_\${1/:/}_\$0_s\$2.log 2>&1; echo done" | while read x; do n=$((n+1)); echo "PROGRESS $(python3 -c "print(f'{0.45 + 0.45 * $n / $tot:.4f}')") tracks $n/$tot"; done
trk=$(cat $R/logs/track_*.log | grep -c '^TRACK_OK'); echo "PROGRESS 0.90 tracked ($trk of 84)"
grep -h '^TRACK ' $R/logs/track_*.log > $R/tracks.jsonl
# 5. reproduction of the census at 0.1 Mm
rep=$($PY - $R/tracks.jsonl <<'PYEOF'
import json, sys
want = {('real', 1): 733, ('real', 2): 626, ('real', 4): 484, ('real', 8): 305, ('shuf:7', 1): 767}
got = {}
for l in open(sys.argv[1]):
    r = json.loads(l[6:])
    if r['dz'] == 0.1: got[(r['order'], r['step'])] = r['swaps_persistent']
ok = sum(got.get(k) == v for k, v in want.items())
print(ok, ' '.join(f'{k[0]}/{k[1]}:{got.get(k)}(census {v})' for k, v in want.items()))
PYEOF
)
echo "REPRO $rep"
# 6. combine
$PY $T combine $D 0.0,0.05,0.1,0.15,0.2,0.3,0.4 1,2,3,4,6,8 $R . > $R/logs/combine.log 2>&1
grep -v PROGRESS $R/logs/combine.log | tail -3
cmb=$(grep -c '^COMBINE_OK' $R/logs/combine.log)
[ $fetch = 1 ] && [ $seg = 7 ] && [ $lnk = 6 ] && [ $trk = 84 ] && [ "${rep%% *}" = 5 ] && [ $cmb = 1 ] && echo "FINAL ok" || echo "FINAL FAIL (fetch $fetch seg $seg/7 link $lnk/6 track $trk/84 repro ${rep%% *}/5 combine $cmb)"
