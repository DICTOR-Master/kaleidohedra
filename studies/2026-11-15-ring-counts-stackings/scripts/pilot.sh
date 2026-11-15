#!/bin/bash
# pilot (<= 5 min): compile, negative controls, named 3C/2H to l = 20 (no ice), local words l = 14, W = 3, analysis
cd "$(dirname "$0")" && mkdir -p ../data/pilot || exit 1
gcc -O2 -o rings_core rings_core.c || exit 1
echo "PROGRESS 0.1 compiled"
python3 rings.py negative > ../data/pilot/negative.txt; a=$?
echo "PROGRESS 0.2 negative exit $a"
NAMED_ONLY=3C,2H ICE=0 python3 rings.py named 20 14 > ../data/pilot/named.txt; b=$?
echo "PROGRESS 0.6 named exit $b"
python3 rings.py local 14 3 0 1 > ../data/pilot/local.txt; c=$?
echo "PROGRESS 0.9 local exit $c"
python3 rings.py analyze ../data/pilot/local.txt > ../data/pilot/analyze.txt; d=$?
echo "PROGRESS 1.0 analyze exit $d"
tail -n 2 ../data/pilot/*.txt
[ $a = 0 ] && [ $b = 0 ] && [ $c = 0 ] && [ $d = 0 ] && grep -q 'ALLCHECKS ok' ../data/pilot/negative.txt
