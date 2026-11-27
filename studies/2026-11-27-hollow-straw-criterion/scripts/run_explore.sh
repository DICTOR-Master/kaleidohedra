#!/bin/bash
# Hollow-straw criterion step 1: C60 in parallel with C80 then C140 (27 Nov 2026)
cd ~/k-research/studies/2026-11-27-hollow-straw-criterion/scripts
export NST=150 NG=300 RHO=0.5,0.7,0.9 TAG=sample PY=~/venvs/arb/bin/python
CORE=GPc_1_1 DICE=1,18,27,28,89,90,91,152,153,204,242,329,515,516 $PY -u hs_general.py >> ../logs/hs_C60.log 2>&1 &
P60=$!
CORE=GPc_2_0 DICE=2,31,32,42,112,113,114,164,165,209,251,333,334,347,348,349,553,554,555,556,557,558,559,560,561,562,563,564 $PY -u hs_general.py >> ../logs/hs_C80.log 2>&1
CORE=GP_2_1 DICE=160,161,217,262,384,385,386,387,420,421,422,423,424,902,903,904,905,906,907,908,909,910,911,912,913,914,915,916 $PY -u hs_general.py >> ../logs/hs_C140.log 2>&1
wait $P60
for c in C60 C80 C140; do echo "$c: $(grep -c 'nested True' ../logs/hs_$c.log) nested, $(grep -c 'nested False' ../logs/hs_$c.log) not nested"; done
n=$(for c in C60 C80 C140; do tail -1 ../logs/hs_$c.log; done | grep -c '^FINAL ok')
[ "$n" = 3 ] && echo "FINAL ok" || echo "FINAL FAIL ($n of 3 cores finished)"
