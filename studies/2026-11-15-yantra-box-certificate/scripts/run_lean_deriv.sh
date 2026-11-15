#!/bin/bash
# Kernel checks of the derivation identities (step 2): every module in lean/YantraCert/Deriv/mods.txt (or $MODS), J at a time,
# each `by decide +kernel` on ZP.eqv statements (Lean core only, no native_decide).  Writes data/lean-deriv-times-$TAG.tsv and
# logs/lean-deriv-$TAG/.  FINAL ok iff every listed module builds.
LP=${LEANPROJ:?set LEANPROJ}; J=${J:-3}; TAG=${TAG:-a}
ST=$(cd "$(dirname "$0")/.." && pwd); LOG=$ST/logs/lean-deriv-$TAG; mkdir -p $LOG
L=${LAKE:-lake}; cd $LP || exit 1
LIST=${MODS:-$ST/lean/YantraCert/Deriv/mods.txt}
echo "PROGRESS 0.00 data module"
$L build YantraCert.Deriv.Data > $LOG/data.log 2>&1 || { echo "data build failed"; tail -20 $LOG/data.log; echo "FINAL FAIL"; exit 1; }
N=$(wc -l < $LIST); echo "modules: $N"
TT=$ST/data/lean-deriv-times-$TAG.tsv; : > $TT
export L LOG TT N
xargs -P $J -I{} sh -c '/usr/bin/time -f "{}	%e	%M" -a -o $TT timeout 3600 $L build {} > $LOG/{}.log 2>&1 || echo "FAILED {}"; n=$(wc -l < $TT); echo "PROGRESS $(python3 -c "print(round(0.05 + 0.95 * $n / $N, 3))") module $n/$N {}"' < $LIST | tee $LOG/xargs.out
grep -q FAILED $LOG/xargs.out && st=1 || st=0
awk -F'\t' '{s+=$2; if ($3>m) m=$3} END {printf "modules: %d, total %.0f s, max RSS %.2f GB\n", NR, s, m/1e6}' $TT
sort -t'	' -k2 -n -r $TT | head -5
echo "PROGRESS 1.00 done"
[ $st -eq 0 ] && [ "$(wc -l < $TT)" = "$N" ] && echo "FINAL ok" || echo "FINAL FAIL"
