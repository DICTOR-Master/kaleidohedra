#!/bin/bash
# Pilot (job sz-pilot): primary Sun setting and the speed-1 control, first 40 frames, all six steps; checks that census_sz.py runs,
# writes the swap list and that its persistence at P = 60 s equals census.py's own count. Under 5 minutes.
S=$(cd "$(dirname "$0")/.." && pwd); PY=${PY:-python3}; cd $S || exit 1
mkdir -p results/pilot results/logs
$PY scripts/make_configs.py | tee results/logs/configs.log
$PY scripts/run_matrix.py data/configs_pilot.jsonl 2 2>&1 | tee results/pilot/matrix.log
$PY - <<'PYEOF'
import json
ok = True
for f in ('results/pilot/sun_primary.json', 'results/pilot/control_v1_z0.json'):
    J = json.load(open(f))
    for s, r in J['steps'].items():
        L = r['swap_list']; op, fl = {}, 0
        for t, lo, ga, two, sh in L:
            k = (tuple(ga), tuple(lo))
            if k in op and t - op[k] <= 60 + 1e-6: fl += 1; del op[k]
            else: op[(tuple(lo), tuple(ga))] = t
        same = len(L) - 2 * fl == r['swaps_persistent_by_W']['60'] and len(L) == r['swaps_elementary']
        ok &= same
        print(f, 'step', s, 'elementary', len(L), 'persistent(list)', len(L) - 2 * fl, 'census', r['swaps_persistent_by_W']['60'],
              'median share', r['centroid']['median_share'], 'msd', round(r['centroid']['msd_px2_share05'], 2), 'same' if same else 'DIFFERENT')
print('FINAL ok' if ok else 'FINAL FAIL list persistence differs from census')
PYEOF
