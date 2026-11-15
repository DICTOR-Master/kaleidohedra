#!/bin/bash
# Build the existence direction and the final theorem, then print the axioms of the main theorems.
# FINAL ok iff every module builds and every axioms line lists only propext, Classical.choice, Quot.sound.
LP=${LEANPROJ:?set LEANPROJ}
ST=$(cd "$(dirname "$0")/.." && pwd); LOG=$ST/logs/lean-exist; mkdir -p $LOG
L=${LAKE:-lake}; cd $LP || exit 1
st=0; i=0
echo "PROGRESS 0.02 KEx"
$L build YantraCert.Deriv.KEx > $LOG/kex.log 2>&1 || { echo "FAILED KEx"; tail -20 $LOG/kex.log; st=1; }
TT=$ST/data/lean-exist-times.tsv; export L LOG TT
xargs -P ${J:-2} -I{} sh -c '/usr/bin/time -f "{}	%e	%M" -a -o $TT timeout 3600 $L build {} > $LOG/{}.log 2>&1 || echo "FAILED {}"; echo "PROGRESS 0.3 {}"' < $ST/lean/YantraCert/Deriv/order-kex.txt | tee $LOG/kex.out
grep -q FAILED $LOG/kex.out && st=1
for m in YantraCert.ExistBase YantraCert.Exist YantraCert.ExistFinal YantraCert.Main; do
  [ $st -eq 0 ] || break
  i=$((i + 1)); echo "PROGRESS $(python3 -c "print(round($i / 6, 3))") $m"
  /usr/bin/time -f "$m	%e	%M" -a -o $ST/data/lean-exist-times.tsv $L build $m > $LOG/$m.log 2>&1 || { echo "FAILED $m"; grep -A8 "error" $LOG/$m.log | head -40; st=1; break; }
done
AX=YantraCert/AxiomsMain.lean
printf 'import YantraCert.Main\n#print axioms YantraCert.Y.kulaichev_unique\n#print axioms YantraCert.Y.kulaichev_slope\n' > $AX
[ $st -eq 0 ] && { $L env lean $AX > $LOG/axioms.log 2>&1 || st=1; cat $LOG/axioms.log; }
n=$(grep -c "depends on axioms: \[propext, Classical.choice, Quot.sound\]" $LOG/axioms.log 2>/dev/null)
echo "PROGRESS 1.00 done"
[ $st -eq 0 ] && [ "$n" = 2 ] && echo "FINAL ok" || echo "FINAL FAIL"
