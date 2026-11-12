#!/bin/bash
# lead 1 (13 Nov 2026): every free unkeyed poly-RD of 8 cells. Control first (poly8 ctl n <= 6 must equal hp-main), then
# generation, then 8 shards on tori of index 8, 16, 24, 32 (1-4 pieces per period, the most any piece n <= 7 needed),
# then every survivor on tori of index 40..64 (5-8 pieces per period, twice the worst seen) and the ball R4.
cd ~/k-research/studies/2026-11-12-hopeful-piece/scripts; D=../data/n8; mkdir -p $D; PY="$HOME/geom/bin/python -W ignore -u"
$PY poly8.py ctl 6 4 > $D/ctl6.log 2>&1 || exit 1; grep -q "^FINAL ok" $D/ctl6.log || { echo "control n <= 6 differs from hp-main"; exit 1; }
echo "PROGRESS 0.05 control ok"; tail -2 $D/ctl6.log
$PY poly8.py gen 8 $D/p8.json > $D/gen8.log 2>&1; grep -q "^FINAL ok" $D/gen8.log || exit 1; grep "free poly" $D/gen8.log
echo "PROGRESS 0.15 generated"
for k in $(seq 0 7); do $PY poly8.py run $D/p8.json 1 4 4 $k/8 $D/m_$k.json > $D/m_$k.log 2>&1 & done
while [ $(jobs -r | wc -l) -gt 0 ]; do
  sleep 60; tot=0; for f in $D/m_*.log; do p=$(grep "^PROGRESS" $f | tail -1 | awk '{print $2}'); tot=$(echo "$tot + ${p:-0}" | bc); done
  echo "PROGRESS $(echo "scale=3; 0.15 + 0.7 * $tot / 8" | bc) main shards"
done
[ $(grep -l '^FINAL ok' $D/m_*.log | wc -l) = 8 ] || { echo "a main shard failed"; exit 1; }
$PY -c "
import json, glob; S = []; C = {}
for f in sorted(glob.glob('$D/m_*.json')):
    r = json.load(open(f)); S += r['survivors']
    for k, v in r['counts'].items(): C[k] = C.get(k, 0) + v
json.dump(S, open('$D/surv.json', 'w')); json.dump(C, open('$D/counts.json', 'w')); print('COUNTS n=8', sum(C.values()), C, 'survivors', len(S))"
if [ "$(cat $D/surv.json)" != "[]" ]; then
  $PY poly8.py run $D/surv.json 5 8 4 0/1 $D/deep.json > $D/deep.log 2>&1 || exit 1; grep "COUNTS\|SURVIVOR" $D/deep.log
fi
echo "PROGRESS 1.000 done"
