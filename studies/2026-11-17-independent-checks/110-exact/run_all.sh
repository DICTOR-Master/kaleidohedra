#!/bin/sh
# Rerun every check from a clean checkout of this folder.
# Needs Python 3 with numpy, scipy, ortools, highspy, python-sat.
# Each step runs well under 5 minutes on a 24-core machine.
set -e
cd "$(dirname "$0")"
PY=${PY:-python3}
mkdir -p logs data cache
$PY scripts/s0_base.py          # 600-cell, W(H4), 120-cell, walls       -> logs/s0_base.log
$PY scripts/s1_crosswalls.py    # item 1                                  -> logs/s1_crosswalls.log
$PY scripts/s2_theoremA.py      # item 2
$PY scripts/s3_lemma3.py        # item 3
$PY scripts/s4_theoremB.py      # item 4 (writes data/thmB.npz)
$PY scripts/s5_prop5.py         # item 5 (writes data/prop5_*)
for f in A B C3; do $PY scripts/s6_duals.py $f; done    # item 6, coverage
$PY scripts/s6b_instance.py     # data/dual_cover_instance.json
# item 6: explicit covers, then proofs that no smaller cover exists
$PY scripts/s7_cover.py A  find 16 60
$PY scripts/s7_cover.py B  find 16 60
$PY scripts/s7_cover.py C3 find 22 60
for s in highs cpsatmin; do
  $PY scripts/s7_cover.py A  $s 15 270
  $PY scripts/s7_cover.py B  $s 15 270
  $PY scripts/s7_cover.py C3 $s 21 270
done
# third solver (CaDiCaL); see README for its outcome
$PY scripts/s7_cover.py A sat 15 260 fix0 || true
$PY scripts/s9_lowerbound.py    # item 6, short lower bounds
$PY scripts/s8_exactcover.py    # item 7
grep -h '^FINAL' logs/*.log | sort | uniq -c
