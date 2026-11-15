#!/bin/bash
# section 8 (l = 22, 24): PART=tables -> four-crossing tables to F = 14 and Delta4 for 512 cases (+ check vs halves.py, + WRONG control);
#                          PART=six    -> six- and eight-crossing Delta by direct chain counts, one shard per flip in KFS (3 at once).
cd "$(dirname "$0")" && D=../data/law24 && mkdir -p $D || exit 1
if [ "$PART" = tables ]; then
  {
    echo "python3 halves24.py dump 24 $D/tables24.txt.gz > $D/halves24.txt 2>&1"
    echo "WRONG=1 python3 halves24.py all 24 > $D/halves24-wrong.txt 2>&1"
    echo "python3 halves24.py check12 > $D/check12.txt 2>&1"
  } > $D/parts-tables.list
  L=$D/parts-tables.list; P=3
else
  for kf in ${KFS:--3 -2 -1 0 1 2}; do echo "python3 six.py 24 $kf > $D/six24-kf$kf.txt 2>&1"; done > $D/parts-six-${KFS// /_}.list
  L=$D/parts-six-${KFS// /_}.list; P=3
fi
OUTS=$(sed -n 's/.*> \([^ ]*\) 2>&1.*/\1/p' $L); NP=$(wc -l < $L)
( while sleep 60; do k=$(grep -l '^ALLCHECKS' $OUTS 2>/dev/null | wc -l); echo "PROGRESS $(python3 -c "print(round($k/$NP,3))") parts finished $k/$NP"; [ "$k" -ge "$NP" ] && break; done ) &
HB=$!
xargs -P $P -I CMD bash -c CMD < $L
kill $HB 2>/dev/null
ok=$(grep -l '^ALLCHECKS ok' $OUTS | wc -l); bad=$(grep -l 'Traceback' $OUTS | wc -l)
echo "PROGRESS 1.0 parts with ALLCHECKS ok: $ok of $NP; tracebacks: $bad"
# the WRONG=1 control must FAIL (ALLCHECKS FAIL) and every other part must pass
if [ "$PART" = tables ]; then
  grep -q '^ALLCHECKS FAIL' $D/halves24-wrong.txt && grep -q '^ALLCHECKS ok' $D/halves24.txt && grep -q '^ALLCHECKS ok' $D/check12.txt && [ "$bad" -eq 0 ]
else
  [ "$ok" -eq "$NP" ] && [ "$bad" -eq 0 ]
fi
