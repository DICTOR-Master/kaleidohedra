#!/bin/bash
# lead 2 (13 Nov 2026): directed (counterexample-guided) search among keyed RDs, heights -1..1, no symmetry assumed.
# Control first (keysearch ctl must agree on 31 pieces), then 8 shards over the 81 cubes (heights of points 1-4), tori to index 32
# (the pilot's survivors of index 16 were all periodic at 24 or 32), balls to R4, each shard capped at 2.5 h; then every survivor on
# tori to index 48 and the ball R5.
cd ~/k-research/studies/2026-11-12-hopeful-piece/scripts; D=../data/ks; mkdir -p $D; PY="$HOME/geom/bin/python -W ignore -u"
$PY keysearch.py ctl 1 2 16 > $D/ctl.log 2>&1; grep -q "^FINAL ok" $D/ctl.log || { echo "keysearch control failed"; exit 1; }
echo "PROGRESS 0.03 control ok"; grep "^controls" $D/ctl.log
for k in $(seq 0 7); do $PY keysearch.py run 1 2 32 4 4 $k/8 2.5 $D/s_$k.json > $D/s_$k.log 2>&1 & done
t0=$(date +%s)
while [ $(jobs -r | wc -l) -gt 0 ]; do
  sleep 60; el=$(( $(date +%s) - t0 ))
  c=$(for f in $D/s_*.log; do grep "^PROGRESS" $f | tail -1 | awk '{print $6}' | cut -d/ -f1; done | paste -sd+ | bc)
  echo "PROGRESS $(echo "scale=3; 0.03 + 0.8 * $el / 9000" | bc) shards running, cubes exhausted ${c:-0}/81"
done
[ $(grep -l '^FINAL ok' $D/s_*.log | wc -l) = 8 ] || { echo "a shard failed"; grep -h "^FINAL" $D/s_*.log; exit 1; }
$PY -c "
import json, glob; C = {}; S = []; ex = 0; n = 0
for f in sorted(glob.glob('$D/s_*.json')):
    r = json.load(open(f)); S += r['survivors']; ex += len(r['cubes_exhausted']); n += r['candidates']
    for k, v in r['counts'].items(): C[k] = C.get(k, 0) + v
json.dump(dict(survivors=S), open('$D/surv.json', 'w')); json.dump(dict(counts=C, cubes_exhausted=ex, candidates=n), open('$D/summary.json', 'w'))
print('SUMMARY candidates', n, 'cubes exhausted', ex, '/81', C, 'survivors', len(S))"
echo "PROGRESS 0.85 shards done"
if grep -q '\[\[' $D/surv.json; then timeout 2400 $PY keysearch.py deep $D/surv.json 48 > $D/deep48.log 2>&1; grep -o "killed [0-9]*\|untileable R[0-9]\|SURVIVOR" $D/deep48.log | sort | uniq -c; grep -q "^FINAL ok" $D/deep48.log || echo "deep check did not finish (timeout); partial verdicts in deep48.log"; fi
echo "PROGRESS 1.000 done"
