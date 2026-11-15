S=~/k-research/studies/2026-11-15-event-logger/pairing; PY=~/venvs/sun/bin/python; R=$S/results
cd $S || exit 1
timeout 1200 $PY scripts/diag_lost_swaps.py $R/foam_s1_frames.jsonl.gz 8 8 4 > $R/diag_foam_s1.log 2>&1 &
P1=$!
timeout 1200 $PY scripts/diag_lost_swaps.py $R/foam_s2_frames.jsonl.gz 8 8 4 > $R/diag_foam_s2.log 2>&1 &
P2=$!
( while sleep 20; do echo "PROGRESS $(grep -l DIAG_OK $R/diag_*.log 2>/dev/null | wc -l)/2 done"; done ) &
HB=$!
wait $P1 $P2
kill $HB 2>/dev/null
cat $R/diag_foam_s1.log $R/diag_foam_s2.log | grep -v PROGRESS
[ "$(cat $R/diag_foam_s*.log | grep -c '^DIAG_OK')" -eq 2 ] && echo "FINAL ok" || echo "FINAL FAIL"
