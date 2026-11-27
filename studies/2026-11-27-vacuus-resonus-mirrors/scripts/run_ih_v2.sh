#!/bin/bash
# Step 11b (27 Nov 2026): rerun with the full-rank realisation LP: cube control, five symmetry runs, merge, centre of mass.
cd "$(dirname "$0")"; PY=~/venvs/indep/bin/python; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
rm -f ../fairdice_icosidodecahedron_C*.json ../fairdice_icosidodecahedron_symmetric.json ../fairdice_centroid_icosi_shard*.json
cp ../fairdice_cube.json ../fairdice_cube.json.keep
PAIR="cube|octahedron" AS=2 TLIM=1800 $PY -u fairsearch_any.py > ../logs/fairsearch_cube_v2.log 2>&1
mv ../fairdice_cube.json.keep ../fairdice_cube.json
grep -E "realised" ../logs/fairsearch_cube_v2.log || { tail -3 ../logs/fairsearch_cube_v2.log; echo "FINAL FAIL cube control"; exit 1; }
printf '%s\n' C2 C3 C5 Cs Ci | xargs -P 5 -I{} sh -c "PAIR='icosidodecahedron|rhombic triacontahedron' SUB={} AS=2 TLIM=7200 CAP=3000000 $PY -u fairsearch_any.py > ../logs/fairsearch_ih_{}.log 2>&1"
for S in C2 C3 C5 Cs Ci; do grep -E "partitions found|realised" ../logs/fairsearch_ih_$S.log | tr '\n' ' '; echo " $S"; test -f ../fairdice_icosidodecahedron_$S.json || { echo "FINAL FAIL run $S"; exit 1; }; done
PAIR="icosidodecahedron|rhombic triacontahedron" MERGE=1 $PY -u fairsearch_any.py 2>&1 | grep -vE "^      size|^piece|^pieces|^  OK|^PROGRESS|^control|^  [a-z]|^the eleven|^FINAL" > ../logs/fairsearch_ih_merge.log
cat ../logs/fairsearch_ih_merge.log
gzip -9f ../fairdice_icosidodecahedron_symmetric.json; rm -f ../fairdice_icosidodecahedron_C*.json
rm -f ../fairdice_centroid_icosi_shard*.json
seq 0 21 | xargs -P 22 -I{} sh -c "PAIR='icosidodecahedron|rhombic triacontahedron' SHARD={}/22 $PY -u fair_centroid.py > ../logs/fair_centroid_ih_{}.log 2>&1"
$PY -u fair_centroid_merge.py 22 icosi auto | tee ../logs/fair_centroid_ih_merge.log | cut -c1-400
