#!/bin/bash
# par_tests.sh, 12 Nov 2026 (aim 3 exact keying; coordinator: use the idle cores). Runs, for every scheme that exact_key.py hands over
# (data/exact/work/DEFER-<scheme>.json, written while data/exact/PARTESTS exists), the three tests AT ONCE: contact_test (chair
# contacts vs P*), integrity_test R = 2 and R = 3 (whole chairs); outputs data/exact/tests/<scheme>.{contact,R2,R3}; then marks
# data/exact/work/TESTS-DONE-<scheme>, and the waiting exact_key.py prints them into its own log as before.
# POSITIVE CONTROL first: H00's exact set (spec/json of round 2) at R = 2 must give WHOLE CHAIRS FORCED (as in job rd-exactA).
# Ends when no exact_all.sh job is left running and every handed-over scheme is done.
# FINAL ok only if the control held and every handed-over scheme got three outputs that each end in a VERDICT line (no crash).
cd "$(dirname "$0")"; D=../data/exact; W=$D/work; T=$D/tests; mkdir -p $T; PY=${PY:-python3}
test3() {   # scheme kj sp
  s=$1; e="REFINE_SPEC=$3 RULES=$2"
  env REFINE_SPEC=$3 RULES=$2 $PY -W ignore -u contact_test.py 4 $s encl > $T/$s.contact 2>&1 &
  env REFINE_SPEC=$3 RULES=$2 $PY -W ignore -u integrity_test.py 4 $s 2 > $T/$s.R2 2>&1 &
  env REFINE_SPEC=$3 RULES=$2 $PY -W ignore -u integrity_test.py 4 $s 3 > $T/$s.R3 2>&1 &
  wait; touch $W/TESTS-DONE-$s
}
env REFINE_SPEC=$W/spec-H00-r2.json RULES=$W/exact-H00-r2.json $PY -W ignore -u integrity_test.py 4 H00 2 > $T/CONTROL-H00.R2 2>&1
if grep -q "VERDICT WHOLE CHAIRS FORCED" $T/CONTROL-H00.R2; then echo "POSITIVE CONTROL H00 R2 (parallel mode): WHOLE CHAIRS FORCED"; ctl=1
else echo "CONTROL FAIL: H00 R2 in parallel mode"; tail -n 3 $T/CONTROL-H00.R2; ctl=0; fi
touch $D/PARTESTS; started=""
while :; do
  for f in $W/DEFER-*.json; do
    [ -e "$f" ] || continue; s=$(basename $f .json); s=${s#DEFER-}
    case " $started " in *" $s "*) continue;; esac
    kj=$($PY -c "import json;print(json.load(open('$f'))['kj'])"); sp=$($PY -c "import json;print(json.load(open('$f'))['sp'])")
    echo "start tests $s"; started="$started $s"; test3 $s $kj $sp &
  done
  n=$(echo $started | wc -w); dn=0; for s in $started; do [ -e $W/TESTS-DONE-$s ] && dn=$((dn+1)); done
  echo "PROGRESS $( [ $n -gt 0 ] && echo "scale=2; $dn/$n" | bc || echo 0) handed-over schemes tested ($dn of $n)"
  if ! pgrep -f "exact_all.sh" >/dev/null && [ $dn -ge $n ]; then break; fi
  sleep 30
done
wait; rm -f $D/PARTESTS
bad=0
for s in $started; do
  for x in contact R2 R3; do grep -q "VERDICT" $T/$s.$x || { echo "CONTROL FAIL $s $x: no verdict (crash?)"; tail -n 2 $T/$s.$x; bad=1; }; done
  echo "== $s: $(grep -h VERDICT $T/$s.contact $T/$s.R2 $T/$s.R3 | tr '\n' ' ')"
done
[ $ctl = 1 ] && [ $bad = 0 ] && echo "FINAL ok" || echo "FINAL FAIL"
