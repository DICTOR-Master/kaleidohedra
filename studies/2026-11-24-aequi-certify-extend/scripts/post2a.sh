#!/bin/bash
# Part 2(a) post-processing after collect: split repeats/new, certify the new dice, split box where needed.
cd "$(dirname "$0")/.."; PY=${PY:-$HOME/venvs/arb/bin/python}
$PY scripts/post2a.py data/collected2a.json > logs/post2a.log 2>&1 && echo "PROGRESS 0.4 post2a" &&
rm -f data/certify2a.jsonl && DICE=data/dice2a-new.json $PY scripts/certify.py data/certify2a.jsonl 20 > logs/certify2a.log 2>&1 && echo "PROGRESS 0.8 certify" &&
DICE=data/dice2a-new.json CERT=data/certify2a.jsonl $PY scripts/accidental.py data/accidental2a.json > logs/accidental2a.log 2>&1
tail -1 logs/post2a.log; tail -1 logs/accidental2a.log
grep -q "^FINAL ok" logs/post2a.log && grep -q "^FINAL ok" logs/accidental2a.log
