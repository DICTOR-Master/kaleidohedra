#!/bin/bash
# run_r7.sh -- item R7, end to end, on the compute host, from the study folder (foreground, about 1 minute):
#   build_dataset.py -> census.py (unchanged, one call per solid) -> collect.py (unchanged) -> exact_census.py -> r7_table.py
# Python: ~/venvs/indep (numpy, scipy, sympy, mpmath); collect.py needs matplotlib for its thumbnails: ~/venvs/plates.
# (~/venvs/voids, named in the brief, has no sympy on this host.) Work files (dataset, per-shape census JSON, DICTO Solids v7) in work/.
set -u
PY=~/venvs/indep/bin/python; PYM=~/venvs/plates/bin/python
cd "$(dirname "$0")/.."
$PY -u scripts/build_dataset.py work/ds > logs/build_dataset.log 2>&1
ls work/ds/solids | sed 's/.json//' > data/slugs.txt
rm -rf work/census; mkdir -p work/census; cp data/classical-krp.json work/census/
: > logs/census.log; n=0
for s in $(cat data/slugs.txt); do timeout 120 $PY -u scripts/census.py work/ds $s work/census >> logs/census.log 2>&1 && n=$((n+1)); done
[ "$n" = 31 ] && [ "$(ls work/census/shapes | wc -l)" = 31 ] && echo "census.py ran for 31 of 31 solids" >> logs/census.log && echo "FINAL ok" >> logs/census.log || echo "FINAL FAIL" >> logs/census.log
# collect.py matches against the classical registry and a dataset folder: DICTO Solids v7 + the 31 solids built here
rm -rf work/dsall; mkdir -p work/dsall/solids
[ -d work/v7 ] || unzip -q -o work/dicto-solids-exact-geometry-v7-ffbfa013.zip -d work/v7
for f in work/v7/dicto-solids-exact-geometry/solids/*.json work/ds/solids/*.json; do ln -sf "$(realpath "$f")" work/dsall/solids/; done
$PYM -u scripts/collect.py work/dsall work/census > logs/collect.log 2>&1
[ "$(grep -c ' | ' logs/collect.log)" = 124 ] && grep -q '^done 124' logs/collect.log && echo "collect.py classified 124 of 124 objects" >> logs/collect.log && echo "FINAL ok" >> logs/collect.log || echo "FINAL FAIL" >> logs/collect.log
cp work/census/census.json data/collect_census.json; mkdir -p data/thumbs; cp work/census/thumbs/*.png data/thumbs/ 2>/dev/null
$PY -u scripts/exact_census.py work data/exact_census.json > logs/exact_census.log 2>&1
$PY -u scripts/r7_table.py work data/exact_census.json data/r7_table.csv > logs/r7_table.log 2>&1
tail -n1 logs/build_dataset.log logs/census.log logs/collect.log logs/exact_census.log logs/r7_table.log
