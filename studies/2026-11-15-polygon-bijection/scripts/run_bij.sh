#!/bin/bash
# exhaustive surgery test (bij.c) on finite windows: 3C/2H to l = 20 at every flip, every c/h word of 7 bilayers to l = 16,
# every word of 5 bilayers to l = 18, wrong twists (negative controls); then the local half-structure count (halves.py) to l = 20.
cd "$(dirname "$0")" && D=../data/full && mkdir -p $D || exit 1
gcc -O2 -o bij bij.c || exit 1
{
  echo "python3 bij.py named 18 > $D/named18.txt 2>&1"
  echo "python3 bij.py named 20 > $D/named20.txt 2>&1"
  echo "python3 bij.py negative 16 > $D/negative.txt 2>&1"
  echo "python3 halves.py 18 > $D/halves18.txt 2>&1"
  for b in 0 1 2 3; do echo "python3 halves.py 20 $b > $D/halves20-$b.txt 2>&1"; done
  for c in $(seq 0 9); do echo "python3 bij.py words 16 3 $c 10 > $D/words16-$c.txt 2>&1"; done
  for c in $(seq 0 5); do echo "python3 bij.py words 18 2 $c 6 > $D/words18-$c.txt 2>&1"; done
} > $D/parts.list
NP=$(wc -l < $D/parts.list)
( while sleep 120; do k=$(grep -l '^ALLCHECKS' $D/*.txt 2>/dev/null | wc -l); echo "PROGRESS $(python3 -c "print(round($k/$NP,3))") parts finished $k/$NP"; [ "$k" -ge "$NP" ] && break; done ) &
HB=$!
xargs -P 20 -I CMD bash -c CMD < $D/parts.list
kill $HB 2>/dev/null
# count only this run's part outputs (15 Nov: a file from another job in the same folder made "25 of 24" read as a failure)
OUTS=$(sed -n 's/.*> \([^ ]*\) 2>&1.*/\1/p' $D/parts.list)
ok=$(grep -l '^ALLCHECKS ok' $OUTS | wc -l); bad=$(grep -l 'ALLCHECKS FAIL\|Traceback' $OUTS | wc -l)
echo "PROGRESS 1.0 parts with ALLCHECKS ok: $ok of $NP; failing: $bad"
[ "$ok" -eq "$NP" ] && [ "$bad" -eq 0 ]
