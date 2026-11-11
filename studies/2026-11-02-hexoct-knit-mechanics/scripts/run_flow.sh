#!/bin/bash
# airflow proxy for every sequence (compute-host); outputs data/flow/<seq>_h<h>_r<r>.json
cd "$(dirname "$0")"; mkdir -p ../data/flow; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1; PY=python3; T=()
for s in 3C 2H 4H 6H Fibonacci "Graded c-top/h-bottom" "Graded h-top/c-bottom"; do T+=("$s|0.02|0.05" "$s|0.02|0.1"); done
T+=("3C|0.0125|0.05" "2H|0.0125|0.05")
printf '%s\n' "${T[@]}" | xargs -P 10 -I{} sh -c 'IFS="|" read s h r <<X
{}
X
f=$(echo "$s" | tr "/ " "_-")_h${h}_r${r}; '"$PY"' flow.py "$s" $h $r ../data/flow/$f.json > ../data/flow/$f.log 2>&1 || echo "FAIL {}"'
echo "flow done: $(ls ../data/flow/*.json | wc -l) json"
