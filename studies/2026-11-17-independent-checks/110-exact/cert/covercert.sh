#!/bin/bash
# Machine certificate for the fewest covers of #110 Theorem B' (d) (DICTO 17 Nov: "a machine cert as recommended").
# For each family: CNF "cover with at most K copies" (make_cnf.py, no symmetry breaking), CaDiCaL writes a DRAT proof of
# UNSAT, drat-trim checks it against the CNF. Controls: at K+1 a model is found and verified as a real cover (verify_model.py).
# Runs on the compute host from ~/indep-checks/110-exact; prints PROGRESS lines; ends FINAL ok only if every check passed.
cd ~/indep-checks/110-exact || exit 1
C=~/tools/cadical/build/cadical; D=~/tools/drat-trim/drat-trim; P=python3; L=cert/logs; mkdir -p $L
fail=0
for spec in "A 15" "B 15" "C3 21"; do
  set -- $spec; f=$1; k=$2; k1=$((k+1))
  $P cert/make_cnf.py dual_cover_instance.json $f $k cert/$f$k.cnf | tee -a $L/make.log | grep -q "FINAL ok" || fail=1
  $P cert/make_cnf.py dual_cover_instance.json $f $k1 cert/$f$k1.cnf | tee -a $L/make.log | grep -q "FINAL ok" || fail=1
  timeout 3600 $C -q cert/$f$k1.cnf > $L/$f$k1.out
  $P cert/verify_model.py dual_cover_instance.json $f $k1 $L/$f$k1.out | tee $L/$f$k1-control.log | grep -q "FINAL ok" || fail=1
done
echo "PROGRESS 0.05 controls done (fail=$fail); solving A15, B15, C3-21 in parallel"
for fk in A15 B15 C321; do
  ( /usr/bin/time -v $C --unsat cert/$fk.cnf cert/$fk.drat > $L/$fk-solve.out 2> $L/$fk-solve.time
    echo "exit $?" >> $L/$fk-solve.out
    echo done > $L/$fk.finished ) &
done
start=$(date +%s)
while true; do
  n=$(ls $L/A15.finished $L/B15.finished $L/C321.finished 2>/dev/null | wc -l)   # only the three main runs (17 Nov: race files were counted, "6 of 3")
  sz=$(du -ch cert/*.drat 2>/dev/null | tail -1 | cut -f1)
  el=$(( ($(date +%s) - start) / 60 ))
  echo "PROGRESS $(awk -v n=$n 'BEGIN{printf "%.2f", 0.05+0.95*n/3}') $n of 3 finished after $el min; proofs $sz; free disk $(df -h ~ | tail -1 | awk '{print $4}')"
  [ "$n" -ge 3 ] && break
  sleep 600
done
for fk in A15 B15 C321; do   # proof checks one at a time (memory)
  if grep -q "^s UNSATISFIABLE" $L/$fk-solve.out; then
    echo "PROGRESS 0.90 checking $fk proof with drat-trim"
    /usr/bin/time -v $D cert/$fk.cnf cert/$fk.drat -t 200000 > $L/$fk-check.out 2> $L/$fk-check.time
    echo "exit $?" >> $L/$fk-check.out
  fi
done
for fk in A15 B15 C321; do
  if grep -q "^s UNSATISFIABLE" $L/$fk-solve.out && grep -q "s VERIFIED" $L/$fk-check.out 2>/dev/null; then
    echo "RESULT $fk: UNSAT, DRAT proof VERIFIED by drat-trim"
  else
    echo "RESULT $fk: not certified ($(grep -E '^s ' $L/$fk-solve.out | head -1); check: $(grep -E '^s ' $L/$fk-check.out 2>/dev/null | head -1))"; fail=1
  fi
done
[ $fail -eq 0 ] && echo "FINAL ok" || echo "FINAL FAIL a control or a certificate did not pass"
