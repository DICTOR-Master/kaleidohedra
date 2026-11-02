#!/bin/bash
# runs every mechanics task in parallel on dicto-big-brother (one thread each); outputs data/mech/<task>.json
cd "$(dirname "$0")"; mkdir -p ../data/mech; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
PY=~/geom/bin/python; T=()
for s in 3C 2H 4H 6H; do for j in pin frame; do for v in links stiff full; do T+=("periodic:$s:$j:$v"); done; done; done
for s in 3C 2H 4H 6H Fibonacci "Graded c-top/h-bottom" "Graded h-top/c-bottom"; do
  for j in pin frame; do for v in links stiff full; do T+=("block:$s:$j:$v"); done; done
  for v in links full; do T+=("rigidity:$s:$v"); done
  for v in links stiff full; do for m in compress compress_free shear13 shear23; do T+=("energy:$s:$v:$m"); done; done
done
T+=("size:3C" "size:2H")
for f in 0.0001 0.001 0.003 0.01 0.03 0.1 0.3 1 3 10 100; do for s in 3C 2H; do for j in pin frame; do T+=("periodic:$s:$j:sheet$f"); done; done; done
for m in 0 1 2 3 4 5 6 7 8 9 10; do lab=$(head -c $m < /dev/zero | tr '\0' c)$(head -c $((10-m)) < /dev/zero | tr '\0' h)  # m c sheets at the bottom, then h
  for v in links full; do T+=("blockL:$lab:frame:$v" "blockL:$lab:pin:$v"); done; done
for lab in chchchchch cchcchcchc ccchccchcc cccchcccch ccccchcccc; do for v in links full; do T+=("blockL:$lab:frame:$v"); done; done
printf '%s\n' "${T[@]}" | xargs -P 20 -I{} sh -c 'f=$(echo "{}" | tr ":/ " "__-"); '"$PY"' mech.py "{}" ../data/mech/$f.json > ../data/mech/$f.log 2>&1 || echo "FAIL {}"'
$PY check_octet.py > ../data/check_octet.out
echo "all done: $(ls ../data/mech/*.json | wc -l) json"
