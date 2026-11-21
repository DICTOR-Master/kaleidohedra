#!/bin/bash
# usage: run_cases.sh TMIN TMAX PARALLEL [GP or GPc]  (from scripts/): runs amber.py on every case, one log per case in ../logs;
# prints "PROGRESS <fraction> <case>" after each case (denominator = number of cases).  One BLAS thread per process (parallel runs).
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python=~/venvs/indep/bin/python
tag=$4_$1_$2; rm -rf ../logs/.done_$tag; mkdir -p ../logs/.done_$tag
export N=$($python cases.py $1 $2 ${4:-GP} | wc -l) TAG=$tag
$python cases.py $1 $2 ${4:-GP} | xargs -P ${3:-20} -L 1 sh -c 'f=$(echo $2|tr / -); '$python' amber.py $0 $1 $2 cen > ../logs/run_$0_$1_${f}_cen.log 2>&1; touch ../logs/.done_$TAG/$0_$1_$f; k=$(ls ../logs/.done_$TAG | wc -l); echo "PROGRESS $(awk "BEGIN{printf \"%.3f\", $k/$N}") $0 $1 $2: $(grep -h "^RESULT" ../logs/run_$0_$1_${f}_cen.log | cut -c1-120)"'
