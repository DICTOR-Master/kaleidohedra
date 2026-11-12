#!/bin/bash
# exact_all.sh, 12 Nov 2026 (aim 3, exact keying): run exact_key.py for the given schemes, two at a time; logs data/exact/<scheme>.log.
# usage: exact_all.sh <tag> <scheme> ...      (PY = interpreter)
# FINAL ok only if every scheme ended (DONE), no CONTROL FAIL, every EXACT scheme passed registration (REG FINAL ok) and the
# completeness control (COMPLETE ... SAME), and, when H00 is in the list (positive control), H00 is EXACT, complete, its chair
# contacts stay inside P* and whole chairs are FORCED.
cd "$(dirname "$0")"; TAG=$1; shift; D=${LOGDIR:-../data/exact}; mkdir -p $D; export PY=${PY:-python3}
for s in "$@"; do rm -f "$D/$s.log"; done
printf '%s\n' "$@" | xargs -P "${PAR:-2}" -I{} sh -c "$PY -u exact_key.py {} 6 $D/work > $D/{}.log 2>&1; echo DONE-RUN >> $D/{}.log" &
n=$#
while :; do
  # 12 Nov: fine progress (watcher saw 0 for minutes): 8 units per scheme = rounds + test stages seen so far, 8 when finished
  d=0; u=0
  for s in "$@"; do
    if grep -q "^DONE-RUN" "$D/$s.log" 2>/dev/null; then d=$((d+1)); u=$((u+8))
    else k=$(grep -cE "round [0-9]+:|^EXACT|^COMPLETE|^REG FINAL|^CONTACT VERDICT|^R[23] VERDICT" "$D/$s.log" 2>/dev/null); [ "${k:-0}" -gt 7 ] && k=7; u=$((u+${k:-0})); fi
  done
  echo "PROGRESS $(echo "scale=3; $u/(8*$n)" | bc) stages, $d of $n schemes done ($TAG)"; [ $d -ge $n ] && break; sleep 60
done
wait
bad=0
for s in "$@"; do
  L="$D/$s.log"; echo "== $s"; grep -E "round [0-9]|EXACT|COMPLETE|REG (ok|FAIL)|REG VERDICT|REG FINAL|CONTACT|^R[23] |CONTROL FAIL|Traceback|Error" "$L" | grep -v "PROGRESS"
  grep -q "^DONE$" "$L" || { echo "CONTROL FAIL $s: did not finish"; bad=1; }
  grep -q "CONTROL FAIL\|Traceback" "$L" && bad=1
  if grep -q "^EXACT" "$L"; then
    grep -q "^REG FINAL ok" "$L" || { echo "CONTROL FAIL $s: registration"; bad=1; }
    grep -q "^COMPLETE .*SAME" "$L" || { echo "CONTROL FAIL $s: rules not complete (level 4 != level 5)"; bad=1; }
    grep -q "control (1): rule-obeying filling with a whole chair round c0 exists: True" "$L" || { echo "CONTROL FAIL $s: integrity positive control"; bad=1; }
  fi
done
if printf '%s\n' "$@" | grep -qx H00; then
  L="$D/H00.log"
  grep -q "^EXACT H00" "$L" && grep -q "^COMPLETE H00.*SAME" "$L" && grep -q "allowed outside P\*: 0" "$L" && grep -q "VERDICT WHOLE CHAIRS FORCED" "$L" \
    && echo "POSITIVE CONTROL H00: exact, complete, contacts inside P*, whole chairs forced" || { echo "CONTROL FAIL: H00 positive control"; bad=1; }
fi
[ $bad = 0 ] && echo "FINAL ok" || echo "FINAL FAIL"
