#!/bin/bash
# pilot for leads 1 and 2 of the hopeful-piece hunt (13 Nov 2026): parts in parallel, each capped at 270 s
cd ~/k-research/studies/2026-11-12-hopeful-piece/scripts; D=../data/pilot2; mkdir -p $D; PY="$HOME/geom/bin/python -W ignore -u"
(timeout 270 $PY poly8.py ctl 5 4 > $D/ctl5.log 2>&1; echo "[exit $?]" >> $D/ctl5.log) &
(timeout 150 $PY poly8.py gen 7 $D/p7.json > $D/gen7.log 2>&1; echo "[exit $?]" >> $D/gen7.log; \
 timeout 110 $PY poly8.py run $D/p7.json 1 4 4 0/200 $D/r7.json > $D/r7.log 2>&1; echo "[exit $?]" >> $D/r7.log) &
(timeout 270 $PY keysearch.py ctl 1 2 16 > $D/kctl.log 2>&1; echo "[exit $?]" >> $D/kctl.log) &
(timeout 270 $PY keysearch.py run 1 2 16 4 4 0/16 0.06 $D/ks0.json > $D/ks0.log 2>&1; echo "[exit $?]" >> $D/ks0.log) &
for i in $(seq 1 9); do sleep 30; echo "PROGRESS $(echo "scale=2; $i/9" | bc) pilot2"; done; wait
for f in ctl5 gen7 r7 kctl ks0; do echo "== $f"; grep -v "^PROGRESS" $D/$f.log | tail -12 | cut -c1-400; grep "^PROGRESS" $D/$f.log | tail -1 | cut -c1-400; done
grep -q "FINAL ok" $D/ctl5.log && grep -q "FINAL ok" $D/kctl.log && grep -q "FINAL ok" $D/gen7.log
