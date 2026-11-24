#!/bin/bash
# Certify the 4404 with the method and scripts of study 2026-11-24-aequi-certify-extend (Part 1 method; no Newton step:
# the 60-digit depths of study 2026-11-19-aequi-complete are used as they are). Usage: run.sh NPROC [sid list for a pilot]
cd "$(dirname "$0")/.."; PY=${PY:-$HOME/venvs/arb/bin/python}; X=../2026-11-24-aequi-certify-extend/scripts
NP=${1:-16}; ONLY=$2; SUF=${ONLY:+-pilot}
$PY scripts/make_dice.py > logs/make_dice$SUF.log 2>&1 && echo "PROGRESS 0.02 dice list" &&
DICE=data/dice4404.json $PY $X/certify.py data/certify4404$SUF.jsonl $NP $ONLY > logs/certify4404$SUF.log 2>&1 && echo "PROGRESS 0.8 certify" &&
DICE=data/dice4404.json CERT=data/certify4404$SUF.jsonl $PY $X/accidental.py data/accidental4404$SUF.json > logs/accidental4404$SUF.log 2>&1; tail -1 logs/accidental4404$SUF.log
$PY $X/structural.py data/certify4404$SUF.jsonl data/structural4404$SUF.json > logs/structural4404$SUF.log 2>&1; tail -1 logs/structural4404$SUF.log
gzip -f data/certify4404$SUF.jsonl   # summarize.py reads the .gz
