#!/bin/bash
# pilot 2b (13 Nov 2026): keysearch control with fresh models for the blocking tests; deep check of the pilot's keyed-RD survivors
# (no torus <= 16, fill R4) on tori to index 32; each part capped at 270 s
cd ~/k-research/studies/2026-11-12-hopeful-piece/scripts; D=../data/pilot2; PY="$HOME/geom/bin/python -W ignore -u"
(timeout 270 $PY keysearch.py ctl 1 2 16 > $D/kctl2.log 2>&1; echo "[exit $?]" >> $D/kctl2.log) &
(timeout 270 $PY keysearch.py deep $D/ks0.json 32 > $D/deep32.log 2>&1; echo "[exit $?]" >> $D/deep32.log) &
for i in $(seq 1 9); do sleep 30; echo "PROGRESS $(echo "scale=2; $i/9" | bc) pilot2b"; done; wait
for f in kctl2 deep32; do echo "== $f"; grep -v "^PROGRESS" $D/$f.log | tail -20 | cut -c1-300; done
grep -q "FINAL ok" $D/kctl2.log
