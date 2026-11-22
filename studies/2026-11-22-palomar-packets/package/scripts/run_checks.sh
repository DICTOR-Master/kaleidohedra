#!/bin/bash
# Compute-host checks of the DehnPackets entry (kit README step 3), as one logged job: fit-check build at the namespace
# profile from a clean build folder, #print axioms, the template comparator at the namespace profile, the three
# negative controls, then the standard profile (clean build and comparator). Logs in the entry's logs/.
# Usage: run_checks.sh ENTRY_DIR CONFIG_TOML     Ends with FINAL ok iff build, axioms, comparator and controls pass.
E=$1; CFG=$2; KIT=$HOME/k-research/palomar-kit/scripts; cd "$E" || exit 1; export PATH=$HOME/.elan/bin:$PATH
ok=1; mkdir -p logs
echo "PROGRESS 0.02 start"
ENTRY=$E PROFILE=namespace STEP=clean bash $KIT/fit_check.sh
ENTRY=$E PROFILE=namespace STEP=build T="Packets Challenge Solution" TMO=10800 bash $KIT/fit_check.sh || ok=0
echo "build warnings (other than the Challenge's sorry):"
grep -a "^warning" logs/fit/namespace/build-last.log | grep -v "declaration uses 'sorry'" | sort | uniq -c | head -20
echo "PROGRESS 0.4 built"
printf 'import Solution\n#print axioms DehnPackets.lemma3\n#print axioms DehnPackets.lemma2\n#print axioms DehnPackets.theorem4a_copies\n#print axioms DehnPackets.theorem4b_copies\n' > AxiomsCheck.lean
timeout 600 lake env lean AxiomsCheck.lean > logs/axioms.log 2>&1; rm -f AxiomsCheck.lean; cat logs/axioms.log
[ "$(grep -c "depends on axioms: \[propext, Classical.choice, Quot.sound\]" logs/axioms.log)" = 4 ] || { echo "AXIOMS FAIL"; ok=0; }
echo "PROGRESS 0.45 axioms"
ENTRY=$E PROFILE=namespace STEP=comparator TMO=5400 bash $KIT/fit_check.sh || ok=0
echo "PROGRESS 0.6 comparator"
for V in a b c; do
  ENTRY=$E V=$V SCRATCH=$HOME/lean/packets-neg CONFIG=$CFG TMO=3600 bash $KIT/run_negative_controls.sh || ok=0
done
echo "PROGRESS 0.7 controls"
st=1
ENTRY=$E PROFILE=standard STEP=clean bash $KIT/fit_check.sh
ENTRY=$E PROFILE=standard STEP=build T="Packets Challenge Solution" TMO=14400 bash $KIT/fit_check.sh || st=0
echo "PROGRESS 0.9 standard build"
if [ $st = 1 ]; then ENTRY=$E PROFILE=standard STEP=comparator TMO=5400 bash $KIT/fit_check.sh || st=0; fi
if [ $st = 1 ]; then echo "STANDARD PROFILE ok"; else echo "STANDARD PROFILE FAIL"; fi
cat logs/fit/SUMMARY.tsv
echo "PROGRESS 1 done"
if [ $ok = 1 ]; then echo "FINAL ok"; else echo "FINAL FAIL"; fi
