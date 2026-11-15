#!/bin/bash
# Negative controls for the local Palomar preflight: three altered copies of the entry, each in its own scratch
# directory outside the entry, each of which must be REJECTED by the comparator or the axiom check.
#   a  one numeric constant in the Challenge statement changed (kulaichev_slope lower bound, last digit +1)
#   b  the Challenge conclusion weakened (exists unique -> exists), so Solution's statement no longer matches
#   c  one Solution proof replaced by `sorry`
# Usage: ENTRY=<built entry> SCRATCH=<dir> CJ=4 [ONLY="a"] [TMO=<s per comparator>] run_negative_controls.sh
# FINAL ok iff every control run is rejected for the intended reason (statement mismatch for a, b; sorryAx for c).
ENTRY=${ENTRY:?}; SCRATCH=${SCRATCH:?}; CJ=${CJ:-4}; ONLY=${ONLY:-"a b c"}; TMO=${TMO:-7200}
ST=$(cd "$(dirname "$0")/.." && pwd); LOG=$ST/logs/palomar/negative; mkdir -p $LOG
export PATH=$HOME/.elan/bin:$PATH
ok=1; k=0; n=$(echo $ONLY | wc -w)
for v in $ONLY; do
  k=$((k+1)); D=$SCRATCH/neg-$v; rm -rf $D; mkdir -p $D/.lake
  echo "PROGRESS $(python3 -c "print(round(($k-1)/$n,2))") control $v: copy"
  (cd $ENTRY && tar --exclude=./.lake -cf - .) | (cd $D && tar -xf -)
  cp -a $ENTRY/.lake/build $D/.lake/; cp -al $ENTRY/.lake/packages $D/.lake/
  case $v in
    a) sed -i 's/(3379673547380287 : ℝ)/(3379673547380288 : ℝ)/' $D/Challenge.lean; grep -q 3379673547380288 $D/Challenge.lean || { echo "control a: edit failed"; ok=0; continue; } ;;
    b) sed -i 's/theorem kulaichev_unique : ∃! y : Yantra/theorem kulaichev_unique : ∃ y : Yantra/' $D/Challenge.lean; grep -q "kulaichev_unique : ∃ y" $D/Challenge.lean || { echo "control b: edit failed"; ok=0; continue; } ;;
    c) sed -i 's/^  exact YantraCert.Y.kulaichev_slope ⟨y.b, y.w, y.a⟩ h$/  sorry/' $D/Solution.lean; grep -q "^  sorry" $D/Solution.lean || { echo "control c: edit failed"; ok=0; continue; } ;;
  esac
  diff <(cd $ENTRY && cat Challenge.lean Solution.lean) <(cd $D && cat Challenge.lean Solution.lean) | head -6 > $LOG/$v.diff
  cd $D
  lake build Challenge Solution > $LOG/$v-build.log 2>&1; echo "control $v: build exit $?"
  printf 'import Solution\n#print axioms KulaichevYantra.kulaichev_unique\n#print axioms KulaichevYantra.kulaichev_slope\n' > AxiomsCheck.lean
  lake env lean AxiomsCheck.lean > $LOG/$v-axioms.log 2>&1; rm -f AxiomsCheck.lean
  ax=$(grep -c sorryAx $LOG/$v-axioms.log); echo "control $v: sorryAx in axioms: $ax"
  sed "s#\"con-ron\": \[f\"{prefix}/bin/con-ron\"\]#\"con-ron\": [f\"{prefix}/bin/con-ron\", \"--jobs=$CJ\"]#" scripts/verify-comparator.sh > scripts/verify-comparator-lowmem.sh
  echo "PROGRESS $(python3 -c "print(round(($k-0.5)/$n,2))") control $v: comparator"
  timeout $TMO bash scripts/verify-comparator-lowmem.sh > $LOG/$v-comparator.log 2>&1; cs=$?
  verdict=$(grep -aE "^error|rejects|disallowed|not allowed|sorry|okay" $LOG/$v-comparator.log | grep -v "^warning" | tail -3 | tr '\n' ' ' | cut -c1-400)
  echo "control $v: comparator exit $cs :: $verdict"
  if grep -q "Your solution is okay" $LOG/$v-comparator.log || [ $cs -eq 0 ]; then echo "control $v: NOT REJECTED"; ok=0
  elif [ $cs -eq 124 ]; then echo "control $v: TIMEOUT (no verdict)"; ok=0
  else echo "control $v: REJECTED"; fi
  cd /; rm -rf $D
done
echo "PROGRESS 1.0 done"
[ $ok -eq 1 ] && echo "FINAL ok (every control rejected)" || echo "FINAL FAIL"
