#!/bin/bash
# Exact follow-up (22 Nov 2026): the 600 runs of run_all.sh (same job list ../logs/joblist.txt) with exact_cell.py (make_exact.py).
# Runs whose log already has a RESULT line are skipped, so the script can be re-run in parts.  Logs ../logs/exact/, data ../data/exact/.
cd "$(dirname "$0")"; mkdir -p ../logs/exact ../data/exact
run1() { set -- $1; solid=$1 t=$2 seed=$3 sc=$4 S=$5
  log=../logs/exact/${solid}_${t}_${sc}_${seed}.log
  grep -q "^RESULT" $log 2>/dev/null && return
  if [ "$sc" = own ]; then timeout 1200 ~/venvs/indep/bin/python exact_cell.py $solid $t 1 $seed > $log 2>&1
  else AMBER_S=$S AMBER_TAG=$sc timeout 1200 ~/venvs/indep/bin/python exact_cell.py $solid $t 1 $seed > $log 2>&1; fi
  echo "done ${solid}_${t}_${sc}_${seed} exit $?"; }
export -f run1
xargs -P ${P:-20} -I{} bash -c 'run1 "{}"' < ../logs/joblist.txt | awk '{c++} END {print "runs finished this call:", c+0}'
echo "runs with a RESULT line: $(grep -l '^RESULT' ../logs/exact/*.log 2>/dev/null | wc -l) / $(wc -l < ../logs/joblist.txt)"
