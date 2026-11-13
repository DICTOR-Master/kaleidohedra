#!/bin/bash
# deep check of the 73 keyed-RD classes (13 Nov 2026, DICTO's one exception to the paused RD hunt; no search, no keying).
# Tiers, every class through a tier before the next: 0 balls R10, R12, R16; 1 every torus of index 65..72; 2 index 96; 3 index 128.
# Controls first: deep4 ctl (heptomino first torus at 28, orbit counts, plain/all-bump RD) and the known survivor 0.0 on every
# torus of index 49..64 (must stay alive). 2 parts (2 cores); checkpoint per (class, tier) in data/d73/p_K.jsonl (rerun resumes).
cd ~/k-research/studies/2026-11-12-hopeful-piece/scripts; D=../data/d73; mkdir -p $D; PY="$HOME/geom/bin/python -W ignore -u"
[ -s $D/classes.json ] || $PY deep4.py list ../data/ksdeep $D/classes.json > $D/list.log 2>&1 || { echo "list failed"; exit 1; }
$PY deep4.py ctl $D/classes.json ../data/deep/s0.json > $D/ctl.log 2>&1; grep -v PROGRESS $D/ctl.log; grep -q '^FINAL ok' $D/ctl.log || { echo "controls failed"; exit 1; }
echo "PROGRESS 0.01 controls ok"
mk() { [ -s $D/$2.pkl ] || $PY deep4.py tori $1 $D/$2.pkl > $D/$2.log 2>&1; }
mk 49-64 t4964 & mk 65-72 t6572 & wait; mk 96 t96 & mk 128 t128 & wait
for t in t4964 t6572 t96 t128; do [ -s $D/$t.pkl ] || { echo "tori $t failed"; exit 1; }; grep "orbits in all" $D/$t.log; done
echo "PROGRESS 0.03 tori built"
$PY deep4.py run $D/classes.json $D/t4964.pkl 16 0/73 $D/ctl_surv.jsonl > $D/ctl_surv.log 2>&1
grep -v PROGRESS $D/ctl_surv.log | tail -3
grep -q '"tier": 1, "verdict": "alive' $D/ctl_surv.jsonl || { echo "survivor control failed: class 0.0 should have no torus 49..64"; exit 1; }
echo "PROGRESS 0.05 survivor control ok"
for k in 0 1; do $PY deep4.py run $D/classes.json $D/t6572.pkl,$D/t96.pkl,$D/t128.pkl 16 $k/2 $D/p_$k.jsonl > $D/p_$k.log 2>&1 & done
while [ $(jobs -r | wc -l) -gt 0 ]; do
  sleep 60; tot=0; for f in $D/p_*.log; do p=$(grep "^PROGRESS" $f | tail -1 | awk '{print $2}'); tot=$(echo "$tot + ${p:-0}" | bc); done
  echo "PROGRESS $(echo "scale=4; 0.05 + 0.93 * $tot / 2" | bc) parts; checkpoints $(cat $D/p_*.jsonl 2>/dev/null | wc -l)"
done
[ $(grep -l '^FINAL ok' $D/p_*.log | wc -l) = 2 ] || { echo "a part failed"; tail -3 $D/p_*.log; exit 1; }
cat $D/p_*.jsonl | $PY -c "
import sys, json, collections; R = [json.loads(l) for l in sys.stdin]; last = {}
for r in R: last[r['id']] = r if r['id'] not in last or r['tier'] >= last[r['id']]['tier'] else last[r['id']]
print('SUMMARY', len(last), 'classes', collections.Counter(v['verdict'].split(':')[0] if v['verdict'].startswith('alive') else v['verdict'] for v in last.values()))"
$PY deep4.py struct $D/classes.json $D/p_0.jsonl,$D/p_1.jsonl 10 > $D/struct.log 2>&1; grep -v PROGRESS $D/struct.log | tail -80
grep -q '^FINAL ok' $D/struct.log && echo "PROGRESS 1.000 done" && echo "FINAL ok"
