#!/bin/bash
# Lean kernel check of the whole box certificate (Lean 4 v4.35.0-rc2 + Mathlib, the Palomar toolchain).
# 1. core modules YantraCert.Check (Lean core only), Sound and Cover (soundness proofs, Mathlib);
# 2. the 10 chart polynomial modules (core only; `C_deg` by decide +kernel);
# 3. every subtree module P<k> (core only; `ok` by decide +kernel, no native_decide), J at a time, heaviest first;
# 4. the 10 assemblies (`covered : C.Covered root` for each chart) and #print axioms for each.
# Writes logs/lean-cert/*.log and data/lean-cert-times.tsv.  FINAL ok iff every module builds, no sorry or native_decide occurs in
# the sources, and every axioms line lists only propext, Classical.choice, Quot.sound.
LP=${LEANPROJ:?set LEANPROJ}; J=${J:-5}
ST=$(cd "$(dirname "$0")/.." && pwd); LOG=$ST/logs/lean-cert; mkdir -p $LOG
L=${LAKE:-lake}; cd $LP || exit 1
st=0
echo "PROGRESS 0.00 core"
$L build YantraCert.Check YantraCert.Sound YantraCert.Cover > $LOG/core.log 2>&1 || { echo "core build failed"; tail -20 $LOG/core.log; st=1; }
echo "PROGRESS 0.02 polys"
$L build $(ls -d YantraCert/Data/*/ | sed 's#/$##; s#/#.#g; s#$#.Polys#') > $LOG/polys.log 2>&1 || { echo "polys build failed"; tail -20 $LOG/polys.log; st=1; }
python3 - "$ST/data/lean-cert-files.json" > $LOG/order.txt <<'PY'
import json, sys
m = json.load(open(sys.argv[1])); fs = [f for c in m['charts'].values() for f in c['files']]
for f in sorted(fs, key=lambda f: -f['cost']): print(f['module'])
PY
N=$(wc -l < $LOG/order.txt); echo "subtree modules: $N"
TT=$ST/data/lean-cert-times.tsv; : > $TT
export L LOG TT N
xargs -P $J -I{} sh -c '/usr/bin/time -f "{}	%e	%M" -a -o $TT timeout 1800 $L build {} > $LOG/{}.log 2>&1 || echo "FAILED {}"; n=$(wc -l < $TT); [ $((n % 50)) -eq 0 ] && echo "PROGRESS $(python3 -c "print(round(0.05 + 0.85 * $n / $N, 3))") subtree $n/$N"' < $LOG/order.txt | tee $LOG/xargs.out
grep -q FAILED $LOG/xargs.out && { grep FAILED $LOG/xargs.out | head; st=1; }
echo "PROGRESS 0.92 assemblies"
$L build YantraCert.Data.All > $LOG/assembly.log 2>&1 || { echo "assembly failed"; tail -30 $LOG/assembly.log; st=1; }
AX=YantraCert/AxiomsCert.lean
{ echo "import YantraCert.Data.All"; for c in $(ls YantraCert/Data/ | grep -v All.lean); do echo "#print axioms YantraCert.Data.$c.covered"; done
  echo "#print axioms YantraCert.checkTree_sound"; } > $AX
$L env lean $AX > $LOG/axioms.log 2>&1 || st=1
cat $LOG/axioms.log
n=$(grep -c "depends on axioms: \[propext, Classical.choice, Quot.sound\]" $LOG/axioms.log)
want=$(( $(ls YantraCert/Data/ | grep -vc All.lean) + 1 ))
bad=$(grep -rlE "sorry|native_decide" YantraCert/Check.lean YantraCert/Sound.lean YantraCert/Cover.lean YantraCert/Data | wc -l)
echo "axioms lines ok: $n of $want; files with sorry/native_decide: $bad"
awk -F'\t' '{s+=$2; if ($3>m) m=$3} END {printf "subtree modules: %d, total %.0f s, max RSS %.2f GB\n", NR, s, m/1e6}' $TT
echo "PROGRESS 1.00 done"
[ $st -eq 0 ] && [ "$n" = "$want" ] && [ "$bad" = 0 ] && echo "FINAL ok" || echo "FINAL FAIL"
