#!/bin/bash
# deep check of the hp-main poly survivors, one process per survivor (12 Nov 2026)
cd ~/k-research/studies/2026-11-12-hopeful-piece/scripts; D=../data/deep; mkdir -p $D; PY="$HOME/geom/bin/python -W ignore -u"
for k in 0 1 2 3 4 5; do
  $PY -c "import json; s=json.load(open('../data/main/summary.json'))['survivors']; json.dump({'survivors': [s[$k]]}, open('$D/s$k.json','w'))"
  $PY deep_check.py $D/s$k.json 28 56 4 > $D/s$k.log 2>&1 &
done
while [ $(jobs -r | wc -l) -gt 0 ]; do sleep 60; echo "PROGRESS $(echo "scale=3; $(grep -l '^FINAL' $D/s*.log 2>/dev/null | wc -l) / 6" | bc) survivors done"; done
grep -h "^survivor" $D/s*.log
[ $(grep -l '^FINAL ok' $D/s*.log | wc -l) = 6 ]
