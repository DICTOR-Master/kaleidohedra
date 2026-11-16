#!/bin/bash
# Regenerate every generated Lean file of the study in module form (Palomar source rule, 16 Nov 2026) and prove that
# nothing but the header changed: each regenerated file must equal lean_module.modulize(<the file before>), byte for byte.
# Generators in dependency order (budget 1.2e5 for c1, as in section 7 of the README):
#   c1 (Data/*), c2 (KBoxData), c5 (Deriv core), c8 (Deriv/KR*), c11 (Deriv/KEx*), c6 (GeomSteps), c9 (Unique1),
#   c10 (Unique2), c12 (Exist), c13 (ExistFinal).
# Deriv/KKBox.lean (17 lines) has no generator and is converted with the hand-written files (scripts/lean_module.py FILE);
# lean/bench/ (scripts/c0_bench.py, not in git) is left out of the comparison.
# Then rewrites data/lean-generated.sha256 and data/lean-deriv-generated.sha256 for the new files.
# Usage: PY=<python with sage, mpmath> [ONLYGEN="c5 c8"] run_module_regen.sh      FINAL ok iff every generator ends well and
# every comparison holds.
PY=${PY:-python3}; ONLYGEN=${ONLYGEN:-"c1 c2 c5 c8 c11 c6 c9 c10 c12 c13"}
ST=$(cd "$(dirname "$0")/.." && pwd); LOG=$ST/logs/module-regen; mkdir -p $LOG; cd $ST || exit 1
OLD=$LOG/old; rm -rf $OLD $LOG/data-before; cp -a lean $OLD; cp -a data $LOG/data-before; export ST
st=0; n=$(echo $ONLYGEN | wc -w); k=0
for g in $ONLYGEN; do
  k=$((k+1)); f=$(ls scripts/${g}_*.py); echo "PROGRESS $(python3 -c "print(round(0.9*($k-1)/$n,3))") $f"
  arg=; [ $g = c1 ] && arg=1.2e5
  /usr/bin/time -f "$g %e s %M KB" $PY $f $arg > $LOG/$g.log 2>&1; ec=$?
  tail -2 $LOG/$g.log
  [ $ec -eq 0 ] || { echo "GENERATOR $g exit $ec"; st=1; }
done
echo "PROGRESS 0.92 compare"
$PY - "$OLD" "$ST/lean" <<'PY' | tee $LOG/compare.out
import os, sys, hashlib
sys.path.insert(0, os.path.join(os.environ.get('ST', '.'), 'scripts'))
from lean_module import modulize, is_module
old, new = sys.argv[1], sys.argv[2]
def files(root):
    out = set()
    for r, d, fs in os.walk(root):
        for x in fs:
            p = os.path.relpath(os.path.join(r, x), root)
            if x.endswith('.lean') and not p.startswith('bench/'): out.add(p)
    return out
O, N = files(old), files(new)
bad = []
same = changed = 0
for p in sorted(O | N):
    if p not in N: bad.append(f'missing after regeneration: {p}'); continue
    if p not in O: bad.append(f'new file: {p}'); continue
    a = open(os.path.join(old, p)).read(); b = open(os.path.join(new, p)).read()
    if not is_module(b): bad.append(f'not in module form: {p}')
    if b == modulize(a): same += 1; changed += (a != b)
    else: bad.append(f'body differs: {p}')
print(f'files {len(N)}; equal to modulize(before) {same} (header added to {changed}); problems {len(bad)}')
for b in bad[:40]: print('  ' + b)
print('COMPARE ok' if not bad else 'COMPARE FAIL')
PY
grep -q '^COMPARE ok' $LOG/compare.out || st=1
echo "PROGRESS 0.97 hashes"
(cd lean && LC_ALL=C sha256sum $(awk '{print $2}' ../data/lean-generated.sha256) > ../data/lean-generated.sha256.new && \
 LC_ALL=C sha256sum $(awk '{print $2}' ../data/lean-deriv-generated.sha256) > ../data/lean-deriv-generated.sha256.new) || st=1
mv data/lean-generated.sha256.new data/lean-generated.sha256; mv data/lean-deriv-generated.sha256.new data/lean-deriv-generated.sha256
for j in data/lean-cert-files.json data/lean-kbox.json data/lean-deriv-index.json data/lean-exist.json data/lean-exist-certs.json; do
  echo "data file $j: $(cmp -s $j $LOG/data-before/$(basename $j) && echo unchanged || echo changed)"
done
# the manifest of c1 may change only in the per-file sha256 and bytes (the header)
$PY - $LOG/data-before/lean-cert-files.json data/lean-cert-files.json <<'PY' || st=1
import json, sys
a, b = (json.load(open(x)) for x in sys.argv[1:])
def strip(m):
    if isinstance(m, dict): return {k: strip(v) for k, v in m.items() if k not in ('sha256', 'bytes')}
    if isinstance(m, list): return [strip(v) for v in m]
    return m
ok = strip(a) == strip(b); print('lean-cert-files.json: equal apart from sha256/bytes:', ok); sys.exit(0 if ok else 1)
PY
echo "PROGRESS 1.0 done"
[ $st -eq 0 ] && echo "FINAL ok" || echo "FINAL FAIL"
