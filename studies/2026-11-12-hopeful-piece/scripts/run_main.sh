#!/bin/bash
# main run of the hopeful-piece hunt (12 Nov 2026): 20 processes in parallel.
#  A  keyed RD, every symmetry class |G| = 4, 3, heights -1..1, exhaustive (10 shards)
#  B  keyed RD, every symmetry class |G| >= 6, heights -2..2, exhaustive (2 shards)
#  C  poly-RD, every free polyform n <= 7, no keys (5 shards)
#  D  keyed RD, no symmetry, paired random faces, 2 x 20000 (2 shards)
#  E  controls through the same engine, tori to index 16 (1 process)
cd ~/k-research/studies/2026-11-12-hopeful-piece/scripts; D=../data/main; mkdir -p $D; PY="$HOME/geom/bin/python -W ignore -u"
for k in $(seq 0 9); do $PY hunt.py K classes:4,3:1 16 4 $k/10 $D/A_$k.json > $D/A_$k.log 2>&1 & done
for k in 0 1; do $PY hunt.py K classes:48,24,16,12,8,6:2 16 4 $k/2 $D/B_$k.json > $D/B_$k.log 2>&1 & done
for k in $(seq 0 4); do $PY hunt.py P 7 24 4 $k/5 $D/C_$k.json > $D/C_$k.log 2>&1 & done
for k in 0 1; do $PY hunt.py K pair:1:20000:$((11 + k)) 16 4 0/1 $D/D_$k.json > $D/D_$k.log 2>&1 & done
$PY hunt.py control ../data/rules.json 16 > $D/E_control.log 2>&1 &
while [ $(jobs -r | wc -l) -gt 0 ]; do
  sleep 120
  tot=0; for f in $D/*.log; do p=$(grep "^PROGRESS" $f | tail -1 | awk '{print $2}'); grep -q "^FINAL" $f && p=1; tot=$(echo "$tot + ${p:-0}" | bc); done
  echo "PROGRESS $(echo "scale=3; $tot / 20" | bc) parts (finished $(grep -l '^FINAL' $D/*.log | wc -l)/20)"
done
echo "parts with FINAL ok: $(grep -l '^FINAL ok' $D/*.log | wc -l)/20"; grep -h "^control\|^tori\|^torus" $D/E_control.log
$PY merge.py $D
[ $(grep -l '^FINAL ok' $D/*.log | wc -l) = 20 ]
