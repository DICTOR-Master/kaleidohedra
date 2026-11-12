#!/bin/bash
# keyed_cutdown.sh, 12 Nov 2026 (aim 3, cutting the 90 keyed RDs down): the certified marking sets smaller than 90 (H02 87, H05 83,
# H07 83) and the 90-type H01, H03 as shapes. Per scheme: keyed_rd.py (bumps/dents; must admit every allowed pair: FINAL ok),
# registration_check.py (lattice + mirrors), contact_test.py (chair contacts vs Kamenetsky's P*), integrity_test.py (whole chairs, R 2
# then 3). Controls: keyed_rd FINAL ok and registration FINAL ok for every scheme, integrity positive control true; else FINAL FAIL.
cd "$(dirname "$0")"; D=../data; PY=${PY:-python3};   # the job sets PY to the study environment S="H02 H05 H07 H01 H03"
run() {
  s=$1; K=$D/keyed-$s-K1.json; L=$D/keyed-cut-$s.log; : > $L
  $PY -W ignore -u keyed_rd.py 4 $s 1 $K >> $L 2>&1
  $PY -W ignore -u registration_check.py $K 2>&1 | grep -v PROGRESS >> $L
  RULES=$K $PY -W ignore -u contact_test.py 4 $s encl 2>&1 | grep -E "allowed by|survive|VERDICT|control" >> $L
  for R in 2 3; do
    RULES=$K $PY -W ignore -u integrity_test.py 4 $s $R 2>&1 | grep -E "\(G\)|control|\(C\)|VERDICT" | sed "s/^/R$R /" >> $L
    grep -q "R$R VERDICT WHOLE CHAIRS FORCED" $L && break
  done
  echo "DONE $s" >> $L
}
rm -f $D/keyed-cut-*.log
for s in $S; do run $s & done
while [ $(grep -l "^DONE" $D/keyed-cut-*.log 2>/dev/null | wc -l) -lt 5 ]; do
  sleep 30; echo "PROGRESS $(echo "scale=2; $(grep -l '^DONE' $D/keyed-cut-*.log 2>/dev/null | wc -l)/5" | bc) schemes"
done
wait
bad=0
for s in $S; do
  L=$D/keyed-cut-$s.log; echo "== $s"; grep -E "types|pairs that fit|VERDICT|allowed by|^FAIL|R[23] " $L
  [ $(grep -c "^FINAL ok" $L) -ge 2 ] || { echo "CONTROL FAIL $s (keyed_rd or registration)"; bad=1; }
  grep -q "control (1): rule-obeying filling with a whole chair round c0 exists: True" $L || { echo "CONTROL FAIL $s (integrity positive control)"; bad=1; }
done
[ $bad = 0 ] && echo "FINAL ok" || echo "FINAL FAIL"
