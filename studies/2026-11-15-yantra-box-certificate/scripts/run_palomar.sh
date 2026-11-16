#!/bin/bash
# Local Palomar preflight of the Kulaichev entry (nothing is pushed or submitted):
# 1. assemble the entry in $ENTRY (scripts/c14_palomar_entry.py; the library in Palomar's module layout);
# 2. Palomar's source check (scripts/check-lean-sources.py from the template);
# 3. clean build: the kernel-heavy modules first, J at a time, then `lake build`;
# 4. #print axioms of the two compared theorems, as seen from Solution;
# 5. `lake comparator` with the toolchain's bundled kernels (Lean, NanoDa, con-ron), the way Palomar runs it
#    (scripts/verify-comparator.sh from the template).
# FINAL ok iff every step passes.
ENTRY=${ENTRY:?set ENTRY}; LIBDIR=${LIBDIR:?set LIBDIR}; J=${J:-3}
ST=$(cd "$(dirname "$0")/.." && pwd); LOG=$ST/logs/palomar; mkdir -p $LOG
export PATH=$HOME/.elan/bin:$PATH
st=0
echo "PROGRESS 0.01 assemble"
[ -d "$ENTRY" ] && find "$ENTRY" -mindepth 1 -maxdepth 1 ! -name .lake -exec rm -rf {} +  # keep built .lake (lake rebuilds what changed)
python3 $ST/scripts/c14_palomar_entry.py "$ENTRY" "$LIBDIR" > $LOG/assemble.log 2>&1; grep -q "^FINAL ok" $LOG/assemble.log || { cat $LOG/assemble.log; echo "FINAL FAIL"; exit 1; }
cd "$ENTRY" || exit 1
mkdir -p .lake && [ -d .lake/packages ] || cp -r $LIBDIR/../.lake/packages .lake/
echo "PROGRESS 0.03 source check"
python3 scripts/check-lean-sources.py > $LOG/sources.log 2>&1 || { tail -20 $LOG/sources.log; st=1; }
tail -3 $LOG/sources.log
echo "PROGRESS 0.05 cache"
lake exe cache get > $LOG/cache.log 2>&1 || { tail -5 $LOG/cache.log; st=1; }
echo "PROGRESS 0.08 heavy modules"
find YantraCert -name '*.lean' | grep -E 'Data/[^/]+/P[0-9]+\.lean|Deriv/K' | sed 's#\.lean$##; s#/#.#g' | sort > $LOG/heavy.txt
N=$(wc -l < $LOG/heavy.txt); export LOG N
# 16 Nov 2026 (job ymod-palomar, clean build): two parallel `lake build`s raced on a shared dependency's .olean
# (Data.Wtp.Polys). Guard: build every non-heavy module that a heavy module imports first, in one lake process;
# then any heavy module that still fails is retried alone, and only a second failure counts.
deps=$(sed 's#\.#/#g; s#$#.lean#' $LOG/heavy.txt | xargs grep -h '^public import YantraCert' | awk '{print $3}' | sort -u | grep -vxF -f $LOG/heavy.txt)
echo "PROGRESS 0.08 shared dependencies ($(echo $deps | wc -w) modules)"
lake build $deps > $LOG/deps.log 2>&1 || { grep -A5 error $LOG/deps.log | head -20; st=1; }
xargs -P $J -I{} sh -c 'lake build {} > $LOG/b-{}.log 2>&1 || echo "FAILED {}"; n=$(ls $LOG | grep -c "^b-"); [ $((n % 100)) -eq 0 ] && echo "PROGRESS $(python3 -c "print(round(0.08 + 0.6 * $n / $N, 3))") heavy $n/$N"' < $LOG/heavy.txt | tee $LOG/heavy.out
if grep -q FAILED $LOG/heavy.out; then
  grep FAILED $LOG/heavy.out | awk '{print $2}' | while read m; do lake build $m > $LOG/r-$m.log 2>&1 && echo "RETRY ok $m" || echo "FAILED AGAIN $m"; done | tee $LOG/heavy-retry.out
  grep -q "FAILED AGAIN" $LOG/heavy-retry.out && st=1
fi
echo "PROGRESS 0.70 full build"
lake build > $LOG/build.log 2>&1 || { grep -A5 error $LOG/build.log | head -30; st=1; }
tail -2 $LOG/build.log
echo "PROGRESS 0.75 axioms"
printf 'import Solution\n#print axioms KulaichevYantra.kulaichev_unique\n#print axioms KulaichevYantra.kulaichev_slope\n' > ./AxiomsCheck.lean; lake env lean AxiomsCheck.lean > $LOG/axioms.log 2>&1; rm -f AxiomsCheck.lean
cat $LOG/axioms.log
[ "$(grep -c 'depends on axioms: \[propext, Classical.choice, Quot.sound\]' $LOG/axioms.log)" = 2 ] || st=1
grep -c sorry Challenge.lean; grep -lE 'sorry|native_decide' Solution.lean YantraCert -r | grep -v '^$' && st=1
# NOCOMP=1 skips this step (16 Nov 2026: con-ron's default 16 workers exceed the memory cage; run run_comparator_lowmem.sh after)
if [ -z "$NOCOMP" ]; then
echo "PROGRESS 0.80 comparator"
bash scripts/verify-comparator.sh > $LOG/comparator.log 2>&1; cs=$?
tail -8 $LOG/comparator.log
[ $cs -eq 0 ] || st=1
fi
echo "PROGRESS 1.00 done"
[ $st -eq 0 ] && echo "FINAL ok" || echo "FINAL FAIL"
