#!/bin/bash
# Independent re-check of every leaf of every chart with FLINT/Arb (b5_arb.py), on the second compute machine.
cd "$(dirname "$0")/.." || exit 1
PY=${PY:-~/geom/bin/python}
st=0
for c in main A B C1 C2 W Wt+ Wt- Wr+ Wr-; do
  p=data/polys-utr-$c.json; h=-; [ $c = main ] && { p=data/polys-utr.json; h=data/holes-main.json; }; [ $c = C1 ] && h=data/holes-C1.json
  echo "PROGRESS chart $c"
  $PY scripts/b5_arb.py $p data/bnb-$c.json $h 4 > logs/b5-$c.log 2>&1
  if tail -n 1 logs/b5-$c.log | grep -q '^FINAL ok'; then echo "b5 $c FINAL ok: $(grep 'Arb: confirmed' logs/b5-$c.log | cut -c12-)"
  else echo "b5 $c did not end FINAL ok:"; tail -n 3 logs/b5-$c.log; st=1; fi
done
[ $st -eq 0 ] && echo "FINAL ok" || echo "FINAL FAIL"
