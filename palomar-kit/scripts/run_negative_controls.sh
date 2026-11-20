#!/bin/bash
# Negative controls (generalised from the Yantra, Dehn and Grünbaum entries): an altered copy of the built entry, in its
# own scratch folder, which the comparator must REJECT. Run on the compute host, one control per call:
#   ENTRY=<entry> V=a|b|c SCRATCH=<dir> [CONFIG=entry.toml] bash run_negative_controls.sh
#     a  a numeral in a theorem statement of Challenge.lean changed      expected: "theorem statement do not match"
#     b  a definition of Challenge.lean weakened (Prop body -> True)      expected: "Const does not match" (the name can
#                                                                         be another constant sharing an auxiliary term)
#     c  a proof in Solution.lean replaced by `sorry`                     expected: "Illegal axiom detected: 'sorryAx'"
# The mutation is chosen by mutate.py (automatically, or exactly from entry.toml [negative]). The copy reuses the
# entry's .lake (build copied, packages hard-linked), builds Challenge and Solution (200 s), prints #print axioms of the
# checked theorem, then runs the template comparator unchanged (run_comparator_full.sh, CJ=default) under TMO (280 s)
# and MEM (14G). Logs: $ENTRY/logs/negative/<V>-*.log and <V>.diff.
# FINAL ok and exit 0 iff the control is rejected: run_comparator_full.sh exits neither 0 nor 124, there is no "Your
# solution is okay", and the comparator gives a rejection reason (a statement or constant mismatch, or an illegal
# axiom); a comparator that fails for another reason (a build or git error) is no verdict. Otherwise FINAL FAIL, exit 1.
# SCRATCH must be on the same filesystem as the entry (the packages are hard-linked).
V=${V:?V=a|b|c}; SCRATCH=${SCRATCH:?}; TMO=${TMO:-280}; KIT=$(cd "$(dirname "$0")" && pwd)
ENTRY=$(cd "${ENTRY:-.}" && pwd); LOG=$ENTRY/logs/negative; mkdir -p "$LOG"; export PATH=$HOME/.elan/bin:$PATH
CFGARG=(); [ -n "$CONFIG" ] && CFGARG=(--config "$(cd "$(dirname "$CONFIG")" && pwd)/$(basename "$CONFIG")")
D=$SCRATCH/neg-$V; rm -rf "$D"; mkdir -p "$D/.lake"
(cd "$ENTRY" && tar --exclude=./.lake --exclude=./logs --exclude=./.git -cf - .) | (cd "$D" && tar -xf -)
cp -a "$ENTRY/.lake/build" "$D/.lake/"; cp -al "$ENTRY/.lake/packages" "$D/.lake/"
python3 -I "$KIT/mutate.py" "$D" "$V" "${CFGARG[@]}" > "$LOG/$V-mutate.log" || { cat "$LOG/$V-mutate.log"; echo "FINAL FAIL (mutation)"; exit 1; }
CHECK=$(sed -n 's/^CHECK //p' "$LOG/$V-mutate.log"); grep -v "^CHECK" "$LOG/$V-mutate.log"
{ diff "$ENTRY/Challenge.lean" "$D/Challenge.lean"; diff "$ENTRY/Solution.lean" "$D/Solution.lean"; } > "$LOG/$V.diff"
[ -s "$LOG/$V.diff" ] || { echo "FINAL FAIL (the mutation changed nothing)"; exit 1; }
cat "$LOG/$V.diff"
cd "$D" || exit 1
timeout 200 lake build Challenge Solution > "$LOG/$V-build.log" 2>&1; echo "control $V: build exit $?"
printf 'import Solution\n#print axioms %s\n' "$CHECK" > AxiomsCheck.lean
timeout 120 lake env lean AxiomsCheck.lean > "$LOG/$V-axioms.log" 2>&1; rm -f AxiomsCheck.lean
echo "control $V: sorryAx in the axioms of $CHECK: $(grep -c sorryAx "$LOG/$V-axioms.log")"
ENTRY=$D CJ=default TMO=$TMO LOG=$LOG/$V-comparator.log bash "$KIT/run_comparator_full.sh" > "$LOG/$V-summary.log" 2>&1; cs=$?
grep -aE "Elapsed|memory.peak" "$LOG/$V-summary.log" | head -2
grep -aiE "^error|uncaught|do not match|mismatch|illegal|axiom|okay" "$LOG/$V-comparator.log" | grep -v "^Exporting" | tail -4 | cut -c1-300
cd / && rm -rf "$D"
if grep -q "Your solution is okay" "$LOG/$V-comparator.log" || [ "$cs" -eq 0 ]; then echo "control $V: NOT REJECTED"; echo "FINAL FAIL"; exit 1
elif [ "$cs" -eq 124 ]; then echo "control $V: TIMEOUT (no verdict)"; echo "FINAL FAIL"; exit 1
elif ! grep -aqiE "do not match|does not match|mismatch|Illegal axiom" "$LOG/$V-comparator.log"; then
  echo "control $V: the comparator failed without a rejection message (no verdict; see $V-comparator.log)"; echo "FINAL FAIL"; exit 1
else echo "control $V: REJECTED"; echo "FINAL ok"; exit 0; fi
