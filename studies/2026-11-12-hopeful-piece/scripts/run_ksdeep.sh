#!/bin/bash
# deep check (13 Nov 2026) of the keyed-RD survivors that hp-ks has logged so far (no torus <= 32, fill R4): tori to index 48, ball R5.
# Uses the 8 cores freed by hp-n8. Survivors are read from the shard logs (SURVIVOR lines), split over 8 processes.
cd ~/k-research/studies/2026-11-12-hopeful-piece/scripts; D=../data/ks; E=../data/ksdeep; mkdir -p $E; PY="$HOME/geom/bin/python -W ignore -u"
$PY -c "
import json, glob, ast
S = []; seen = set()
for f in sorted(glob.glob('$D/s_*.log')):
    for l in open(f):
        if l.startswith('SURVIVOR keyed RD'):
            H = ast.literal_eval(l[len('SURVIVOR keyed RD '):l.rindex(']') + 1])
            if tuple(H) not in seen: seen.add(tuple(H)); S.append(H)
for k in range(8): json.dump(dict(survivors=S[k::8]), open('$E/d_%d.json' % k, 'w'))
print('survivors so far', len(S))"
for k in $(seq 0 7); do $PY keysearch.py deep $E/d_$k.json 48 > $E/d_$k.log 2>&1 & done
while [ $(jobs -r | wc -l) -gt 0 ]; do
  sleep 60; tot=0; for f in $E/d_*.log; do p=$(grep "^PROGRESS" $f | tail -1 | awk '{print $2}'); tot=$(echo "$tot + ${p:-0}" | bc); done
  echo "PROGRESS $(echo "scale=3; $tot / 8" | bc) deep parts"
done
grep -ho "killed [0-9]*\|untileable R[0-9]\|: SURVIVOR" $E/d_*.log | sort | uniq -c
[ $(grep -l '^FINAL ok' $E/d_*.log | wc -l) = 8 ]
