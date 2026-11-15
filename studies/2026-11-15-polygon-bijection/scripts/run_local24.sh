#!/bin/bash
# direct enumeration (rings.py of study 2026-11-15-ring-counts-stackings, unchanged) of the polygons through both atoms of bilayer 0,
# to l = 24, for every c/h word on bilayers -4..4 (512 words, 32 chunks); CHUNKS = the chunk numbers for this host, P = parallel runs.
R=$HOME/k-research/studies/2026-11-15-ring-counts-stackings/scripts
D=$(cd "$(dirname "$0")" && pwd)/../data/law24 && mkdir -p $D || exit 1
cd $R && gcc -O2 -o rings_core rings_core.c || exit 1
for c in $CHUNKS; do echo "python3 rings.py local 24 4 $c 32 > $D/local24-$c.txt 2>&1"; done > $D/parts-local-${CHUNKS// /_}.list
L=$D/parts-local-${CHUNKS// /_}.list; OUTS=$(sed -n 's/.*> \([^ ]*\) 2>&1.*/\1/p' $L); NP=$(wc -l < $L)
( while sleep 120; do k=$(grep -l '^ALLCHECKS' $OUTS 2>/dev/null | wc -l); w=$(cat $OUTS 2>/dev/null | grep -c '^LOCALDATA'); echo "PROGRESS $(python3 -c "print(round($w/(32*$NP),3))") site runs $w/$((32*NP)), chunks finished $k/$NP"; [ "$k" -ge "$NP" ] && break; done ) &
HB=$!
xargs -P $P -I CMD bash -c CMD < $L
kill $HB 2>/dev/null
ok=$(grep -l '^ALLCHECKS ok' $OUTS | wc -l); bad=$(grep -l 'ALLCHECKS FAIL\|Traceback' $OUTS | wc -l)
echo "PROGRESS 1.0 chunks with ALLCHECKS ok: $ok of $NP; failing: $bad"
[ "$ok" -eq "$NP" ] && [ "$bad" -eq 0 ]
