#!/bin/bash
# Job sun-tilt-poly (16 Nov 2026; control 4 of the full space-time run, README "Space-time slicing at a tilt"): the #104 polytope
# sweeps (120-cell, truncated 120-cell, bitruncated 600-cell), logged by the shared event logger (event-logger study,
# scripts/sweep_tilings.py, unchanged; corners of the 600-cell from studies/2026-10-30-queen-stages/scripts/stages.py, as in job elog-sweep) in three more
# generic directions (seeds 13, 17, 19; seeds 7 and 11 were run on 15 Nov). Known answer: the h-vectors of #104, births / swaps /
# deaths 116/366/116, 716/966/716, 716/2166/716, nothing else, every frame passing. FINAL ok only if all 9 sweeps give them exactly.
S=$(cd "$(dirname "$0")/.." && pwd); PY=${PY:-python3}
EL=$S/../2026-11-15-event-logger/scripts; T6=$S/../2026-10-30-queen-stages/scripts/stages.py
R=$S/results/tilt/polytopes; mkdir -p $R; cd $R || exit 1
for st in red trunc120 bitruncated; do for sd in 13 17 19; do echo "$st $sd"; done; done | \
  xargs -P 3 -L 1 bash -c "timeout 3000 $PY $EL/sweep_tilings.py $T6 \$0 \$1 1 2>&1 | tee $R/\$0_\$1.log | grep -E '^(step|PROGRESS 1)'" | \
  while read x; do n=$((n+1)); echo "PROGRESS $(python3 -c "print(f'{$n / 18:.3f}')") $x"; done
$PY $S/scripts/tilt_polytopes_check.py $R | tee $R/check.log
[ "$(tail -1 $R/check.log)" = "MATCH 9" ] && echo "FINAL ok" || echo "FINAL FAIL (exact h-vectors: $(tail -1 $R/check.log) of 9 sweeps)"
