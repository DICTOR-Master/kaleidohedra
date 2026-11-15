#!/bin/bash
# full run: named stackings (cycles + SP rings to l = 24, NB loops to 20, King/Guttman, strong check, ice series to order 18),
# every c/h word of 11 letters (l <= 20, 12 chunks), Fibonacci (l <= 20), ice control, negative controls. 26 parts, 23 at once.
cd "$(dirname "$0")" && D=../data/full && mkdir -p $D || exit 1
gcc -O2 -o rings_core rings_core.c || exit 1
{
  for n in 3C 2H 4H 6H 8H 9R 10H 15R 12R 21R '10H*'; do echo "env NAMED_ONLY=$n python3 rings.py named 24 20 > $D/named-${n/\*/s}.txt 2>&1"; done
  for c in $(seq 0 11); do echo "python3 rings.py local 20 5 $c 12 > $D/local-$c.txt 2>&1"; done
  echo "python3 rings.py fib 20 > $D/fib.txt 2>&1"
  echo "python3 rings.py icecontrol > $D/icecontrol.txt 2>&1"
  echo "python3 rings.py negative > $D/negative.txt 2>&1"
} > $D/parts.list
NP=$(wc -l < $D/parts.list)
# heartbeat: fraction of parts finished (each part ends with an ALLCHECKS line); xargs returns only when every part has ended
( while sleep 120; do k=$(grep -l '^ALLCHECKS' $D/*.txt 2>/dev/null | wc -l); echo "PROGRESS $(python3 -c "print(round($k/$NP,3))") parts finished $k/$NP"; [ "$k" -ge "$NP" ] && break; done ) &
HB=$!
xargs -P 23 -I CMD bash -c CMD < $D/parts.list
kill $HB 2>/dev/null
python3 rings.py analyze $D/local-*.txt > $D/analyze.txt 2>&1
ok=$(grep -l '^ALLCHECKS ok' $D/*.txt | wc -l); bad=$(grep -l 'ALLCHECKS FAIL\|Traceback' $D/*.txt | wc -l)
echo "PROGRESS 1.0 parts with ALLCHECKS ok: $ok of $((NP + 1)); failing: $bad"
[ "$ok" -eq $((NP + 1)) ] && [ "$bad" -eq 0 ]
