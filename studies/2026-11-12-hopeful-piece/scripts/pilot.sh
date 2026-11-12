#!/bin/bash
# pilot for the hopeful-piece hunt (12 Nov 2026): four parts in parallel, each capped at 150 s
cd ~/k-research/studies/2026-11-12-hopeful-piece/scripts; D=../data/pilot; mkdir -p $D; PY="$HOME/geom/bin/python -W ignore -u"
(timeout 150 $PY hunt.py control ../data/rules.json 8 > $D/control.log 2>&1; echo "[exit $?]" >> $D/control.log) &
(timeout 150 $PY hunt.py K classes:4,3:1 16 4 0/400 $D/k43.json > $D/k43.log 2>&1; echo "[exit $?]" >> $D/k43.log) &
(timeout 150 $PY hunt.py P 6 24 3 0/10 $D/p6.json > $D/p6.log 2>&1; echo "[exit $?]" >> $D/p6.log) &
(timeout 150 $PY hunt.py K rand:1,2:1:300:7 16 4 0/1 $D/r12.json > $D/r12.log 2>&1; echo "[exit $?]" >> $D/r12.log) &
for i in 1 2 3 4 5 6; do sleep 25; echo "PROGRESS $(echo "scale=2; $i/6" | bc) pilot"; done; wait
for f in control k43 p6 r12; do echo "== $f"; grep -v "^PROGRESS" $D/$f.log | tail -6; grep "^PROGRESS" $D/$f.log | tail -1; done
grep -q "FINAL ok" $D/k43.log && grep -q "FINAL ok" $D/p6.log && grep -q "FINAL ok" $D/r12.log
