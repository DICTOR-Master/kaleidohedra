#!/bin/bash
# full run: setup (exact) -> enumeration -> atoms -> exact analysis. Each step must succeed.
set -e
cd "$(dirname "$0")/.."
D=${1:-data/raw}
PY=${PY:-python3}
mkdir -p $D
gcc -O2 -Wall -o scripts/gp_enum scripts/gp_enum.c
$PY scripts/gp_setup.py $D
for s in A3 B3 H3; do
  ./scripts/gp_enum enum $D/$s.in 0 1 $D/$s.reps
  grep '^R' $D/$s.reps | awk '{print $4}' > $D/$s.repbits
  ./scripts/gp_enum sub $D/$s.in $D/$s.repbits 3 $D/$s.sub
  echo "PROGRESS 0.2 $s enumerated"
done
$PY scripts/gp_analyse.py $D ${NPROC:-8}
