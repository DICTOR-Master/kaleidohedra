#!/bin/bash
# comfort proxies for every sequence (compute-host); outputs data/therm/<seq>_h<h>_r<r>.json and therm-summary.md
cd "$(dirname "$0")"; mkdir -p ../data/therm; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1; PY=python3; T=()
for s in 3C 2H 4H 6H Fibonacci "Graded c-top/h-bottom" "Graded h-top/c-bottom"; do T+=("$s|0.025|0.05" "$s|0.025|0.1"); done
T+=("3C|0.0167|0.05" "2H|0.0167|0.05")
printf '%s\n' "${T[@]}" | xargs -P 8 -I{} sh -c 'IFS="|" read s h r <<X
{}
X
f=$(echo "$s" | tr "/ " "_-")_h${h}_r${r}; '"$PY"' therm.py "$s" $h $r ../data/therm/$f.json > ../data/therm/$f.log 2>&1 || echo "FAIL {}"'
$PY - <<'EOF' > ../data/therm-summary.md
import json, glob
rows = [json.load(open(f)) for f in sorted(glob.glob('../data/therm/*.json'))]
print('# HexOct comfort proxies (therm.py)\n\n| seq | h | r | porosity | D_eff/D_air | tortuosity factor | k_yarn_eff | direct radiation | cg |')
print('|---|---|---|---|---|---|---|---|---|')
for x in sorted(rows, key=lambda x: (x['r'], x['h'], x['seq'])):
    print('| %s | %s | %s | %.4f | %.4f | %.3f | %.5f | %.4f | %d/%d |' % (x['seq'], x['h'], x['r'], x['porosity'], x['D_eff_air'],
          x['tortuosity_factor'], x['k_eff_yarn'], x['radiation_direct'], x['cg_info_air'], x['cg_info_yarn']))
EOF
echo "therm done: $(ls ../data/therm/*.json | wc -l) json"
