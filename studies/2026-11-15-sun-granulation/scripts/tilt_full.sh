#!/bin/bash
# Job sun-tilt (16 Nov 2026, approved by DICTO): the full space-time run. README sections "Space-time slicing at a tilt" (Part A) and
# "Granule tubes in space-time: prisms and scutoids" (Part B). Definitions, predictions and verdict rules were written in the README
# before this job ran.
# Part A: 153 blocks (Sun labellings B, A at 0.5/1.0/1.5 std, A2; 4 quadrants; depths 0, 0.1, 0.2 Mm; real and shuffled frames;
# quiet-Sun run; Poisson-Voronoi 5 seeds x 3 time scales; moving Voronoi 2 seeds), each cut in 15 directions; time-reversed and
# half-step runs on three blocks. Part B: granule tubes (time step 10-80 s, depths, quiet Sun, tracking tolerance, shuffled, reversed),
# Poisson-Voronoi and moving-Voronoi nulls, the figure. Then tilt_full_summary.py.
# FINAL ok only if every block, slice, tube run, the figure and the summary ended with their OK lines.
S=$(cd "$(dirname "$0")/.." && pwd); PY=${PY:-python3}; T=scripts/spacetime_tilt.py; U=scripts/spacetime_scutoids.py
cd $S || exit 1
D=data/tilt-full; R=results/tilt; mkdir -p $D $R/logs $R/slices $R/tubes
rm -f $D/*.npz $R/logs/*.log $R/slices/*.json $R/tubes/*.json   # this job's own folders only
B=data/bifrost; QS=data/skeleton/feat_qs024048_by3363_dz0.1_seg.npy
# ---------------- blocks
{
for dz in 0.0 0.1 0.2; do for q in 0 1 2 3; do for o in real shuf:7; do
  echo "sunB seg=data/trace3d/seg_dz$dz.npy dz=$dz q=$q order=$o"
  echo "sunA2 data=$B dz=$dz q=$q order=$o"
  for thr in 0.5 1.0 1.5; do echo "sunA data=$B dz=$dz q=$q order=$o thr=$thr"; done
done; done; done
for q in 0 1 2 3; do
  echo "sunB seg=data/trace3d/seg_dz0.1.npy dz=0.1 q=$q order=shuf:8"
  echo "sunA2 data=$B dz=0.1 q=$q order=shuf:8"
  echo "sunB seg=$QS run=qs024048_by3363 dz=0.1 q=$q order=real"
  echo "sunA2 data=$B run=qs024048_by3363 dz=0.1 q=$q order=real"
done
for vc in 1.5 3.0 6.0; do for s in 1 2 3 4 5; do echo "pv vc=$vc seed=$s"; done; done
echo "mv seed=1"; echo "mv seed=2"
} > $R/block_tasks.txt
NB=$(wc -l < $R/block_tasks.txt)
cat $R/block_tasks.txt | xargs -P 20 -I{} bash -c "set -- {}; h=\$(echo '{}' | md5sum | cut -c1-8); timeout 900 $PY $T block \$1 $D \${@:2} 2>&1 | tee $R/logs/block_\$h.log | grep -E '^BLOCK_OK'" | \
  while read x; do n=$((n+1)); echo "PROGRESS $(python3 -c "print(f'{0.15 * $n / $NB:.4f}')") blocks $n/$NB $x"; done
nb=$(cat $R/logs/block_*.log | grep -c '^BLOCK_OK'); echo "blocks ok $nb of $NB"
grep -h '^BLOCK ' $R/logs/block_*.log > $R/blocks.jsonl
# ---------------- slices (15 directions; reversal and half step on three blocks)
DIRS="0,3,+x 10,3,+x 10,3,-x 10,3,+y 20,3,+x 20,3,-x 20,3,+y 30,3,+x 30,3,-x 30,3,+y 45,3,+x 45,3,-x 45,3,+y 30,1.5,+x 30,6,+x"
{
for f in $D/*.npz; do b=$(basename $f .npz); for d in $DIRS; do IFS=, read th v az <<< "$d"; echo "$f $th $v $az $R/slices/${b}_t${th}_v${v}_${az}.json"; done; done
for b in sunB_en_dz0.1_q0_real pv_vc3.0_s1 mv_s1; do for d in $DIRS; do IFS=, read th v az <<< "$d"; echo "$D/$b.npz $th $v $az $R/slices/${b}_t${th}_v${v}_${az}_rev.json rev=1"; done; done
for b in sunB_en_dz0.1_q0_real pv_vc3.0_s1; do for d in $DIRS; do IFS=, read th v az <<< "$d"; echo "$D/$b.npz $th $v $az $R/slices/${b}_t${th}_v${v}_${az}_half.json half=1"; done; done
} > $R/slice_tasks.txt
NS=$(wc -l < $R/slice_tasks.txt)
cat $R/slice_tasks.txt | xargs -P 22 -L 1 bash -c "h=\$(echo \"\$@\" | md5sum | cut -c1-8); timeout 1200 $PY $T slice \"\$@\" 2>&1 | tee $R/logs/slice_\$h.log | grep -E '^SLICE_OK'" _ | \
  while read x; do n=$((n+1)); echo "PROGRESS $(python3 -c "print(f'{0.15 + 0.7 * $n / $NS:.4f}')") slices $n/$NS"; done
ns=$(cat $R/logs/slice_*.log | grep -c '^SLICE_OK'); echo "slices ok $ns of $NS"
# ---------------- Part B: granule tubes
{
for dz in 0.0 0.1 0.2; do for st in 1 2 4 8; do echo "sun data/trace3d/seg_dz$dz.npy $R/tubes/sun_en_dz${dz}_step$st.json step=$st tag=en_dz${dz}_step$st"; done; done
for st in 1 2 4 8; do echo "sun $QS $R/tubes/sun_qs_dz0.1_step$st.json step=$st tag=qs_dz0.1_step$st"; done
for tol in 0.3 0.5 0.7; do echo "sun data/trace3d/seg_dz0.1.npy $R/tubes/sun_en_dz0.1_step1_tol$tol.json tol=$tol tag=en_dz0.1_step1_tol$tol"; done
for o in shuf:7 shuf:8; do echo "sun data/trace3d/seg_dz0.1.npy $R/tubes/sun_en_dz0.1_step1_${o/:/}.json order=$o tag=en_dz0.1_step1_${o/:/}"; done
echo "sun data/trace3d/seg_dz0.1.npy $R/tubes/sun_en_dz0.1_step1_rev.json rev=1 tag=en_dz0.1_step1_rev"
for vc in 1.5 3.0 6.0; do for s in 1 2 3 4 5; do echo "pv $s $vc $R/tubes/pv_vc${vc}_s$s.json"; done; done
echo "mv 1 $R/tubes/mv_s1.json"; echo "mv 2 $R/tubes/mv_s2.json"
echo "fig $S data/trace3d/seg_dz0.1.npy"
} > $R/tube_tasks.txt
NT=$(wc -l < $R/tube_tasks.txt)
cat $R/tube_tasks.txt | xargs -P 12 -L 1 bash -c "h=\$(echo \"\$@\" | md5sum | cut -c1-8); timeout 900 $PY $U \"\$@\" 2>&1 | tee $R/logs/tube_\$h.log | grep -E '^(TUBES_OK|FIG_OK|FIG_FAIL)'" _ | \
  while read x; do n=$((n+1)); echo "PROGRESS $(python3 -c "print(f'{0.85 + 0.13 * $n / $NT:.4f}')") tubes $n/$NT $x"; done
nt=$(cat $R/logs/tube_*.log | grep -cE '^(TUBES_OK|FIG_OK)'); echo "tube runs and figure ok $nt of $NT"
# ---------------- summary
$PY scripts/tilt_full_summary.py $R 2>&1 | tee $R/logs/summary.log | tail -60
sm=$(grep -c '^FINAL-SUMMARY ok' $R/logs/summary.log)
echo "PROGRESS 1.0 done"
[ "$nb" = "$NB" ] && [ "$ns" = "$NS" ] && [ "$nt" = "$NT" ] && [ "$sm" = 1 ] && echo "FINAL ok" || echo "FINAL FAIL (blocks $nb/$NB slices $ns/$NS tubes $nt/$NT summary $sm)"
