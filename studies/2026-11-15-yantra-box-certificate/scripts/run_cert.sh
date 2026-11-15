#!/bin/bash
# The whole box certificate for Kulaichev's yantra in one job: build, generate, check exactly, semantic control, negative controls.
# Every step must end FINAL ok (the negative controls must end FAIL); the job's FINAL line depends on all of them.
cd "$(dirname "$0")/.." || exit 1
PY=${PY:-python3}   # a Python with sage (passagemath), python-flint, mpmath, numpy
CENSUS=${CENSUS:-../2026-11-15-yantra-uniqueness/data/census-K.json}
st=0
step() {  # name, log, command...
  local nm=$1 lg=$2; shift 2
  echo "PROGRESS step $nm"
  "$@" > "logs/$lg" 2>&1
  if tail -n 1 "logs/$lg" | grep -q '^FINAL ok'; then echo "$nm FINAL ok"; else echo "$nm did not end FINAL ok:"; tail -n 3 "logs/$lg"; st=1; fi
}
step b1 b1_polys.log $PY scripts/b1_polys.py
step b1c b1_charts.log $PY scripts/b1_charts.py utr
step b3 b3_krawczyk.log $PY scripts/b3_krawczyk.py data/polys-utr.json "$CENSUS" data/kbox-K.json 22
$PY -c "
import json; k = json.load(open('data/kbox-K.json')); assert k['inside']
json.dump({'holes': [{'name': 'Krawczyk', 'box': k['box']}, {'name': 'corner0', 'box': [[0, '1/4'], [0, '1/16'], [0, 6]]},
           {'name': 'corner1', 'box': [['7/8', 1], ['7/8', 1], [0, 6]]}]}, open('data/holes-main.json', 'w'))
json.dump({'holes': [{'name': 'N1', 'box': [[0, '1/16'], ['1/2', '3/2'], ['1/2', '3/2']]}]}, open('data/holes-C1.json', 'w'))" || st=1
CH="main A B C1 C2 W Wt+ Wt- Wr+ Wr-"
for c in $CH; do
  p=data/polys-utr-$c.json; h=-; [ $c = main ] && { p=data/polys-utr.json; h=data/holes-main.json; }; [ $c = C1 ] && h=data/holes-C1.json
  step "b2 $c" b2-$c.log env MAXOPEN=4000000 $PY scripts/b2_bnb.py $p data/bnb-$c.json 40 $h
  step "b4 $c" b4-$c.log $PY scripts/b4_check.py $p data/bnb-$c.json $h 20
  step "b4b $c" b4b-$c.log $PY scripts/b4b_semantic.py $p data/bnb-$c.json inputs/system-K.txt 400
done
# negative control (a): the main certificate checked against G + 2^-20 must FAIL
echo "PROGRESS control a"
PERTURB='F:G:1/1048576' $PY scripts/b4_check.py data/polys-utr.json data/bnb-main.json data/holes-main.json 20 > logs/control-perturbed.log 2>&1
tail -n 1 logs/control-perturbed.log | grep -q '^FINAL FAIL' && echo "control a: perturbed system rejected (as it must be)" || { echo "control a: perturbed system NOT rejected"; st=1; }
# negative control (b): equations only, no admissibility tests: the cover must stay open exactly at the census's non-admissible
# solution (u, tau, rho) = (0.668656, 0.188437, 2.7808)
echo "PROGRESS control b"
NOTESTS=1 MAXOPEN=2000000 $PY scripts/b2_bnb.py data/polys-utr.json data/bnb-control-notests.json 30 data/holes-main.json > logs/control-notests.log 2>&1
$PY - <<'EOF' >> logs/control-notests.log 2>&1 && echo "control b: equations alone leave the box open only at the non-admissible solution (as they must)" || { echo "control b: unexpected"; st=1; }
import json, sys
c = json.load(open('data/bnb-control-notests.json')); op = c['open']
u0, t0, S0 = 0.668656315401935, 0.12600012263503690807, 0.97571625261253856290
R = 1 / (1 + u0 * u0); x0 = (u0, t0 / u0, (S0 - R) / ((1 - R) * (1 - u0)))
W = [1, 1, 6]
far = [o for o in op if max(abs(W[j] * (o[2 * j + 1] + 0.5) / 2**o[2 * j] - x0[j]) for j in range(3)) > 1e-3]
print('open boxes', len(op), '; farther than 1e-3 from', x0, ':', len(far))
sys.exit(0 if op and not far else 1)
EOF
[ $st -eq 0 ] || echo "a step failed: see above"
$PY - <<'EOF'
import json, glob
tot = {'leaves': 0, 'evaluations': 0, 'term_evaluations': 0, 'max_endpoint_digits': 0}
rows = []
for f in ['data/bnb-%s.check.json' % c for c in 'main A B C1 C2 W Wt+ Wt- Wr+ Wr-'.split()]:
    d = json.load(open(f)); rows.append((f, d['leaves'], d['evaluations'], d['term_evaluations'], d['max_endpoint_digits'], d['passed'] == d['leaves'] and d['coverage']))
    for k in tot: tot[k] = max(tot[k], d[k]) if k == 'max_endpoint_digits' else tot[k] + d[k]
for r in rows: print('SIZE', *r)
print('SIZE total', tot)
json.dump({'charts': rows, 'total': tot}, open('data/certificate-size.json', 'w'), indent=1)
EOF
[ $st -eq 0 ] && echo "FINAL ok" || echo "FINAL FAIL"
