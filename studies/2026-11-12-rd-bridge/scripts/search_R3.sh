#!/bin/bash
# search_R3.sh: the schemes of the 12-90 search whose chair contacts are certified (0 outside P*) but whose whole-chair test failed at
# R = 2: retest at R = 3 (a bigger ball only adds constraints); and the rule-completeness check (levels 4 = 5) of the smallest certified
# scheme H18 (62 types). PY = interpreter with pysat.
cd "$(dirname "$0")"; PY=${PY:-python3}
$PY -W ignore -u rule_stability.py H18 4 5 > ../data/searchH-18-stability.log 2>&1 &
for k in 25 26 22 23 24 15 19 17 04 06 08; do echo $k; done | xargs -P 11 -I{} sh -c "$PY -W ignore -u integrity_test.py 4 H{} 3 > ../data/searchH-{}-integrity-R3.log 2>&1; echo H{} done"
wait
echo "== summary"; tail -n 2 ../data/searchH-18-stability.log
for k in 25 26 22 23 24 15 19 17 04 06 08; do echo "H$k R3: $(grep -h '^VERDICT\|(C) ball' ../data/searchH-$k-integrity-R3.log | tr '\n' ' ')"; done
grep -q "FINAL ok" ../data/searchH-18-stability.log && echo "FINAL ok" || echo "FINAL FAIL: H18 rule stability"
