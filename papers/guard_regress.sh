#!/bin/bash
# Run on dicto-big-brother after ANY change to print.mjs (11-07: a guard edit once disabled bracket stripping and flagged every book).
# Prints each translated book once, on a copy, without its status box, as a final edition would be printed; every line must say "written".
cd ~/kaleidohedra-check/papers || exit 1
for b in book-quanta-ja book-dictonary-ja book-quanta-zh book-dictonary-zh book-quanta-fa book-dictonary-fa book-quanta-ar book-dictonary-ar; do
  [ -d "$b" ] || continue
  rm -rf zz-g && cp -r "$b" zz-g && python3 -c "
import re;p='zz-g/paper.html';s=open(p).read();s=re.sub(r'<div class=.status.[^>]*>.*?</div>','',s,count=1,flags=re.S);open(p,'w').write(s)"
  printf '%s: ' "$b"; node print.mjs zz-g g.pdf T x 1 2>&1 | tail -1
done; rm -rf zz-g
