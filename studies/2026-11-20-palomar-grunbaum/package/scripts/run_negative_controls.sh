#!/bin/bash
# Negative controls for the local comparator run (after the Dehn entry's run_negative_controls.sh): an altered copy of
# the built entry, in its own scratch directory outside the entry, which must be REJECTED.
#   a  one constant in a Challenge statement changed: in grunbaum_k10, `EveryZoneHas F 10` becomes `EveryZoneHas F 12`
#   b  one Challenge definition changed: IsRhombus asks ‖u‖ ≤ ‖v‖ instead of ‖u‖ = ‖v‖ (no theorem text is touched)
#   c  one Solution proof (grunbaum_k10) replaced by `sorry`
# Each control runs the template comparator unchanged (CJ=default) under the same limit TMO (default 280 s) and 14 GB
# cap. Usage (from the entry root): V=a SCRATCH=<dir> bash scripts/run_negative_controls.sh   (one control per call)
# FINAL ok iff the control is rejected (comparator exit not 0, no "Your solution is okay", no time-out).
V=${V:?}; SCRATCH=${SCRATCH:?}; TMO=${TMO:-280}; ENTRY=$(cd "$(dirname "$0")/.." && pwd); LOG=$ENTRY/logs/negative
mkdir -p $LOG; export PATH=$HOME/.elan/bin:$PATH
D=$SCRATCH/neg-$V; rm -rf $D; mkdir -p $D/.lake
(cd $ENTRY && tar --exclude=./.lake --exclude=./logs --exclude=./.git -cf - .) | (cd $D && tar -xf -)
cp -a $ENTRY/.lake/build $D/.lake/; cp -al $ENTRY/.lake/packages $D/.lake/
case $V in
  a) sed -i 's/^      EveryZoneHas F 10 ∧ LinearIndependent ℝ b ∧/      EveryZoneHas F 12 ∧ LinearIndependent ℝ b ∧/' $D/Challenge.lean
     grep -q "^      EveryZoneHas F 12 ∧" $D/Challenge.lean || { echo "control a: edit failed"; exit 1; } ;;
  b) sed -i 's/^def IsRhombus (F : Parallelogram) : Prop := F.Nondegenerate ∧ ‖F.u‖ = ‖F.v‖$/def IsRhombus (F : Parallelogram) : Prop := F.Nondegenerate ∧ ‖F.u‖ ≤ ‖F.v‖/' $D/Challenge.lean
     grep -q "‖F.u‖ ≤ ‖F.v‖$" $D/Challenge.lean || { echo "control b: edit failed"; exit 1; } ;;
  c) python3 - $D/Solution.lean <<'PY' || { echo "control c: edit failed"; exit 1; }
import sys, pathlib
p = pathlib.Path(sys.argv[1]); t = p.read_text(encoding="utf-8")
old = ("  ⟨GET.PB, GET.FB, GET.bB, GET.PB_spherical, GET.FB_rhombicMonohedral, GET.FB_golden, GET.FB_zones, GET.bB_li,\n"
       "    GET.PB_tiles, GET.FB_faceToFace⟩\n")
assert t.count(old) == 1
p.write_text(t.replace(old, "  sorry\n"), encoding="utf-8")
PY
     ;;
esac
diff $ENTRY/Challenge.lean $D/Challenge.lean > $LOG/$V.diff; diff $ENTRY/Solution.lean $D/Solution.lean >> $LOG/$V.diff
cat $LOG/$V.diff
cd $D
timeout 200 lake build Challenge Solution > $LOG/$V-build.log 2>&1; echo "control $V: build exit $?"
printf 'import Solution\n#print axioms GrunbaumK10.grunbaum_k10\n' > AxiomsCheck.lean
timeout 120 lake env lean AxiomsCheck.lean > $LOG/$V-axioms.log 2>&1; rm -f AxiomsCheck.lean
echo "control $V: sorryAx in axioms of grunbaum_k10: $(grep -c sorryAx $LOG/$V-axioms.log)"
CJ=default TMO=$TMO LOG=$LOG/$V-comparator.log bash scripts/run_comparator_lowmem.sh > $LOG/$V-summary.log 2>&1
cs=$(grep -c "^FINAL ok" $LOG/$V-summary.log)
grep -aE "Elapsed|memory.peak" $LOG/$V-summary.log | head -2
grep -aiE "^error|uncaught|do not match|mismatch|illegal|axiom|okay" $LOG/$V-comparator.log | grep -v "^Exporting" | tail -4 | cut -c1-300
cd /; rm -rf $D
if grep -q "Your solution is okay" $LOG/$V-comparator.log || [ $cs -ne 0 ]; then echo "control $V: NOT REJECTED"; echo "FINAL FAIL"
elif grep -q "comparator exit 124" $LOG/$V-summary.log; then echo "control $V: TIMEOUT (no verdict)"; echo "FINAL FAIL"
else echo "control $V: REJECTED"; echo "FINAL ok"; fi
