#!/bin/bash
# second deep check (13 Nov 2026): the keyed-RD survivors of hp-ksdeep (no torus to index 48, fill R5), one per congruence class,
# on balls R6..R8 first, then tori of index 49..64. 8 parts.
cd ~/k-research/studies/2026-11-12-hopeful-piece/scripts; E=../data/ksdeep; PY="$HOME/geom/bin/python -W ignore -u"
J=$(ls $E/d_*_deep48.json | paste -sd,)
for k in $(seq 0 7); do $PY keysearch.py deep2 $J 48 64 8 $k/8 > $E/e_$k.log 2>&1 & done
while [ $(jobs -r | wc -l) -gt 0 ]; do
  sleep 60; tot=0; for f in $E/e_*.log; do p=$(grep "^PROGRESS" $f | tail -1 | awk '{print $2}'); tot=$(echo "$tot + ${p:-0}" | bc); done
  echo "PROGRESS $(echo "scale=3; $tot / 8" | bc) deep2 parts"
done
grep -h "survivors, \|^survivor" $E/e_*.log | cut -c1-200
[ $(grep -l '^FINAL ok' $E/e_*.log | wc -l) = 8 ]
