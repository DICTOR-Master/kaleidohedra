#!/bin/bash
# section 8: the laws p22, p24 from the tables (law.py), checked against direct enumeration (61 named-polytype sites x 2 atoms and
# 512 local words x 2 atoms), plus two negative controls that must fail: the WRONG=1 tables, and the law without six-crossing terms.
cd "$(dirname "$0")" && D=../data/law24 || exit 1
N=$HOME/k-research/studies/2026-11-15-ring-counts-stackings/data/full
echo "PROGRESS 0.0 law"
python3 law.py $D/halves24.txt $D/six24-kf*.txt --named $N --local $D/local24-*.txt > $D/law.txt 2>&1
echo "PROGRESS 0.4 wrong tables"
python3 law.py $D/halves24-wrong.txt $D/six24-kf*.txt --named $N --local $D/local24-*.txt > $D/law-wrong.txt 2>&1
echo "PROGRESS 0.7 no six-crossing terms"
python3 law.py $D/halves24.txt $D/six24-kf*.txt --drop6 --named $N --local $D/local24-*.txt > $D/law-drop6.txt 2>&1
echo "PROGRESS 1.0 done"
tail -1 $D/law.txt $D/law-wrong.txt $D/law-drop6.txt
grep -q '^ALLCHECKS ok' $D/law.txt && grep -q '^ALLCHECKS FAIL' $D/law-wrong.txt && grep -q '^ALLCHECKS FAIL' $D/law-drop6.txt
