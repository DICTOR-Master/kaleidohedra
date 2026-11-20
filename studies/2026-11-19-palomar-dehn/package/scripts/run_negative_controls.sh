#!/bin/bash
# Negative controls for the local comparator run (after the Yantra study's run_negative_controls.sh): an altered copy
# of the built entry, in its own scratch directory outside the entry, which must be REJECTED.
#   a  one constant in a Challenge statement changed: the first volume 1/6 of hilbert_third_problem becomes 1/7
#   b  one Challenge definition changed: wedgeAngle measures with π instead of 2π (no theorem text is touched)
#   c  one Solution proof (dehnSet_eq_edge_sum) replaced by `sorry`
# Each control runs the template comparator unchanged (CJ=default) under the same 280 s limit and 14 GB cap.
# Usage (from the entry root): V=a SCRATCH=<dir> bash scripts/run_negative_controls.sh   (one control per call)
# FINAL ok iff the control is rejected (comparator exit not 0, no "Your solution is okay", no time-out).
V=${V:?}; SCRATCH=${SCRATCH:?}; ENTRY=$(cd "$(dirname "$0")/.." && pwd); LOG=$ENTRY/logs/negative; mkdir -p $LOG
export PATH=$HOME/.elan/bin:$PATH
D=$SCRATCH/neg-$V; rm -rf $D; mkdir -p $D/.lake
(cd $ENTRY && tar --exclude=./.lake --exclude=./logs -cf - .) | (cd $D && tar -xf -)
cp -a $ENTRY/.lake/build $D/.lake/; cp -al $ENTRY/.lake/packages $D/.lake/
case $V in
  a) sed -i '0,/volume (convexHull ℝ ({A, B, C, D} : Set R3)) = ENNReal.ofReal (1 \/ 6)/s//volume (convexHull ℝ ({A, B, C, D} : Set R3)) = ENNReal.ofReal (1 \/ 7)/' $D/Challenge.lean
     grep -q "ENNReal.ofReal (1 / 7)" $D/Challenge.lean || { echo "control a: edit failed"; exit 1; } ;;
  b) sed -i 's/^  2 \* Real.pi \* ((volume (wedgeSet T K)).toReal/  Real.pi * ((volume (wedgeSet T K)).toReal/' $D/Challenge.lean
     grep -q "^  Real.pi \* ((volume (wedgeSet T K))" $D/Challenge.lean || { echo "control b: edit failed"; exit 1; } ;;
  c) sed -i 's/^  exact DehnCanon.Library.dehnSet_eq_edge_sum hP hint$/  sorry/' $D/Solution.lean
     grep -q "^  sorry" $D/Solution.lean || { echo "control c: edit failed"; exit 1; } ;;
esac
diff $ENTRY/Challenge.lean $D/Challenge.lean > $LOG/$V.diff; diff $ENTRY/Solution.lean $D/Solution.lean >> $LOG/$V.diff
cat $LOG/$V.diff
cd $D
timeout 200 lake build Challenge Solution > $LOG/$V-build.log 2>&1; echo "control $V: build exit $?"
printf 'import Solution\n#print axioms DehnCanon.dehnSet_eq_edge_sum\n' > AxiomsCheck.lean
timeout 120 lake env lean AxiomsCheck.lean > $LOG/$V-axioms.log 2>&1; rm -f AxiomsCheck.lean
echo "control $V: sorryAx in axioms of dehnSet_eq_edge_sum: $(grep -c sorryAx $LOG/$V-axioms.log)"
CJ=default TMO=280 LOG=$LOG/$V-comparator.log bash scripts/run_comparator_lowmem.sh > $LOG/$V-summary.log 2>&1
cs=$(grep -c "^FINAL ok" $LOG/$V-summary.log)
grep -aE "Elapsed|memory.peak" $LOG/$V-summary.log | head -2
grep -aiE "^error|uncaught|do not match|mismatch|illegal|axiom|okay" $LOG/$V-comparator.log | grep -v "^Exporting" | tail -4 | cut -c1-300
cd /; rm -rf $D
if grep -q "Your solution is okay" $LOG/$V-comparator.log || [ $cs -ne 0 ]; then echo "control $V: NOT REJECTED"; echo "FINAL FAIL"
elif grep -q "comparator exit 124" $LOG/$V-summary.log; then echo "control $V: TIMEOUT (no verdict)"; echo "FINAL FAIL"
else echo "control $V: REJECTED"; echo "FINAL ok"; fi
