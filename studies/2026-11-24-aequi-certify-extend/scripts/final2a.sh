#!/bin/bash
# Part 2(a) after the search: classify, split off repeats, certify the new Aequi (arb Krawczyk; split box where the type changes).
cd "$(dirname "$0")/.."; PY=${PY:-$HOME/venvs/arb/bin/python}
python3 -c "print([[int(a), int(b)] for a, b in (x.split(':') for x in open('data/plan2a-stages.txt').read().split())])" > data/plan2a.json
NPROC=20 $PY scripts/collect.py data/classes2a.json data/plan2a.json data/collected2a.json data/raw/sol-2a.jsonl 2>&1 | grep -v Warn > logs/collect2a.log
$PY scripts/post2a.py data/collected2a.json > logs/post2a.log 2>&1
rm -f data/certify2a.jsonl; DICE=data/dice2a-new.json $PY scripts/certify.py data/certify2a.jsonl 20 > logs/certify2a.log 2>&1
DICE=data/dice2a-new.json CERT=data/certify2a.jsonl $PY scripts/accidental.py data/accidental2a.json > logs/accidental2a.log 2>&1
tail -2 logs/collect2a.log; tail -1 logs/post2a.log; tail -1 logs/accidental2a.log
