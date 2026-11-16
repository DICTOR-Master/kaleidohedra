#!/bin/bash
# The kernel phases as Palomar's verifier runs them (PalomarSubmission scripts/verify_submission.py at 14aa8d6), on 4 CPUs
# inside a cgroup capped at $CAP with no swap:
#   1. `lake comparator` with Lean's kernel and NanoDa only (the mandatory checks; Palomar registers only NanoDa as an
#      external kernel and replays con-ron afterwards);
#   2. the Solution export (`leanexport Solution -- <theorems>`), then con-ron --jobs=2 --verified on it, with Palomar's
#      30-minute replay limit, using the con-ron binary Palomar pins (lean v4.36.0-rc1 release, sha256 checked); a con-ron
#      that runs out of memory or time is "declined" there (a warning), not a failure;
#   3. if con-ron did not accept: con-ron --jobs=1 without the cap, with its resident memory sampled every 2 s beside its
#      progress lines, to find the records that need the memory.
# Usage: ENTRY=<built entry> [CAP=14G] [SKIP_COMPARATOR=1] run_palomar_kernels.sh     FINAL ok iff step 1 accepts.
ENTRY=${ENTRY:?}; CAP=${CAP:-14G}
ST=$(cd "$(dirname "$0")/.." && pwd); LOG=$ST/logs/kernels; mkdir -p $LOG
export PATH=$HOME/.elan/bin:$PATH
cd "$ENTRY" || exit 1
prefix=$(lake env lean --print-prefix)
st=0
capped() { n=$1; shift
  systemd-run --user --wait --pipe -p MemoryMax=$CAP -p MemorySwapMax=0 -E PATH=$PATH -E LEAN_NUM_THREADS=4 \
    --working-directory=$ENTRY taskset -c 0-3 "$@" > $LOG/$n.log 2>&1; ec=$?
  grep -E "Finished with result|Memory peak|Service runtime" $LOG/$n.log | sed "s/^ */$n: /"; return $ec; }
# 1. mandatory comparator (Lean kernel + NanoDa)
if [ -z "$SKIP_COMPARATOR" ]; then
  echo "PROGRESS 0.05 comparator (Lean kernel, NanoDa) under $CAP"
  python3 - comparator.json $LOG/config.json "$prefix" <<'PY'
import json, sys
src, dst, prefix = sys.argv[1:]
c = json.load(open(src)); c.pop('enable_nanoda', None)
c['external_kernels'] = {'nanoda': [f'{prefix}/bin/nanoda_bin']}
json.dump(c, open(dst, 'w'), indent=2)
PY
  ( while sleep 300; do echo "PROGRESS 0.3 heartbeat $(grep -a 'Running' $LOG/comparator.log | tail -1 | cut -c1-100)"; done ) & hb=$!
  capped comparator lake comparator --config $LOG/config.json; cc=$?; kill $hb 2>/dev/null
  grep -aE "kernel accepts|okay|^error|Illegal|do not match" $LOG/comparator.log | tail -5; echo "comparator exit $cc"
  [ $cc -eq 0 ] || st=1
fi
# 2. export and con-ron replay
echo "PROGRESS 0.7 export"
lake env leanexport Solution -- KulaichevYantra.kulaichev_unique KulaichevYantra.kulaichev_slope > $LOG/solution.ndjson 2> $LOG/export.err
echo "export exit $? size $(du -h $LOG/solution.ndjson | cut -f1)"
CR=$HOME/lean/con-ron-4.36.0-rc1/con-ron
if [ ! -x $CR ]; then
  mkdir -p $(dirname $CR); cd $(dirname $CR)
  curl -sL -o l.tar.zst https://github.com/leanprover/lean4/releases/download/v4.36.0-rc1/lean-4.36.0-rc1-linux.tar.zst
  echo "26b3cea1a006ad419215520b8668dcd3f6a9eeba1a123756563a739f9c6274b2  l.tar.zst" | sha256sum -c - || { echo "con-ron archive sha256 mismatch"; st=1; }
  tar --zstd -xOf l.tar.zst lean-4.36.0-rc1-linux/bin/con-ron > con-ron && chmod +x con-ron; rm -f l.tar.zst
  sha256sum con-ron; cd "$ENTRY"
fi
echo "PROGRESS 0.75 con-ron --jobs=2 under $CAP (30 min)"
capped conron timeout 1800 $CR --jobs=2 --verified --progress=1000 $LOG/solution.ndjson; rc=$?
grep -aE "^con-ron: (accepted|rejected|declined|error)" $LOG/conron.log | tail -2; echo "con-ron exit $rc"
if [ $rc -ne 0 ]; then
  echo "PROGRESS 0.85 con-ron --jobs=1, memory sampled"
  ( $CR --jobs=1 --verified --progress=20 $LOG/solution.ndjson > $LOG/conron1.log 2>&1 ) & cp=$!
  : > $LOG/conron1.rss
  while kill -0 $cp 2>/dev/null; do
    p=$(pgrep -n -f "con-ron --jobs=1"); r=$(awk '/VmRSS/{print $2}' /proc/$p/status 2>/dev/null)
    echo "$(date +%s) ${r:-0} $(grep -a 'con-ron: check' $LOG/conron1.log | tail -1 | cut -c1-160)" >> $LOG/conron1.rss; sleep 2
  done
  echo "con-ron --jobs=1: $(grep -aE '^con-ron: (accepted|rejected|declined|error)' $LOG/conron1.log | tail -1)"
  echo "largest resident sets (KB) with the last progress line:"; sort -k2 -n -r $LOG/conron1.rss | head -8 | cut -c1-200
fi
echo "PROGRESS 1.0 done"
[ $st -eq 0 ] && echo "FINAL ok" || echo "FINAL FAIL"
