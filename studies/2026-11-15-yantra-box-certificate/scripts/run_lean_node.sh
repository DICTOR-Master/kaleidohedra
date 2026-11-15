#!/bin/bash
# Independent re-check of every subtree module of the Lean box certificate on the second compute machine (aarch64 build of the same
# Lean 4 v4.35.0-rc2 kernel, commit 11acb17).  These modules import only Lean core and YantraCert.Check, so no Mathlib is needed.
# FINAL ok iff every subtree module and every chart polynomial module builds (each `ok` and `C_deg` accepted by decide +kernel).
LP=${LEANPROJ:?set LEANPROJ}; J=${J:-4}
ST=$(cd "$(dirname "$0")/.." && pwd); LOG=$ST/logs/lean-node; mkdir -p $LOG
L=${LAKE:-lake}; cd $LP || exit 1
st=0
echo "PROGRESS 0.00 core and polys"
$L build YantraCert.Check $(ls -d YantraCert/Data/*/ | sed 's#/$##; s#/#.#g; s#$#.Polys#') > $LOG/polys.log 2>&1 || { echo "polys build failed"; tail -20 $LOG/polys.log; st=1; }
python3 - "$ST/data/lean-cert-files.json" > $LOG/order.txt <<'PY'
import json, sys
m = json.load(open(sys.argv[1]))
import os
stride = int(os.environ.get('STRIDE', '1'))   # STRIDE=k: every chart but main and C1 in full, and every k-th module of main and C1
sel = [f for c, v in m['charts'].items() for i, f in enumerate(v['files']) if c not in ('main', 'C1') or i % stride == 0]
for f in sorted(sel, key=lambda f: -f['cost']): print(f['module'])
PY
N=$(wc -l < $LOG/order.txt); echo "subtree modules: $N"
TT=$ST/data/lean-node-times.tsv; : > $TT
export L LOG TT N
xargs -P $J -I{} sh -c '/usr/bin/time -f "{}	%e	%M" -a -o $TT timeout 3600 $L build {} > $LOG/{}.log 2>&1 || echo "FAILED {}"; n=$(wc -l < $TT); [ $((n % 25)) -eq 0 ] && echo "PROGRESS $(python3 -c "print(round(0.02 + 0.97 * $n / $N, 3))") subtree $n/$N"' < $LOG/order.txt | tee $LOG/xargs.out
grep -q FAILED $LOG/xargs.out && { grep FAILED $LOG/xargs.out | head; st=1; }
done_n=$(wc -l < $TT)
awk -F'\t' '{s+=$2; if ($3>m) m=$3} END {printf "subtree modules: %d, total %.0f s, max RSS %.2f GB\n", NR, s, m/1e6}' $TT
echo "PROGRESS 1.00 done"
[ $st -eq 0 ] && [ "$done_n" = "$N" ] && echo "FINAL ok" || echo "FINAL FAIL"
