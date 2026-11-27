#!/bin/bash
# Hollow-straw criterion step 2: facing count and largest nested core size (bisection) for C60 and C80 (27 Nov 2026)
cd ~/k-research/studies/2026-11-27-hollow-straw-criterion/scripts
export NST=150 NG=200 RHO=0.5 TAG=facing BISECT=1 PY=~/venvs/arb/bin/python
CORE=GPc_1_1 DICE=1,18,27,28,89,90,91,152,153,204,242,329,515,516 $PY -u hs_general.py >> ../logs/facing_C60.log 2>&1 &
P1=$!
CORE=GPc_2_0 DICE=2,31,32,42,112,113,114,164,165,209,251,333,334,347,348,349,553,554,555,556,557,558,559,560,561,562,563,564 $PY -u hs_general.py >> ../logs/facing_C80.log 2>&1
wait $P1
n=$(for c in C60 C80; do tail -1 ../logs/facing_$c.log; done | grep -c '^FINAL ok')
[ "$n" = 2 ] && echo "FINAL ok" || echo "FINAL FAIL ($n of 2)"
