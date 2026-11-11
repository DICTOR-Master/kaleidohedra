#!/bin/sh
# RT pyramids, edge-to-edge search, no node cap, deeper targets; controls first (C6 must reach, RD must not collapse)
cd "$(dirname "$0")"
mkdir -p data
python3 scripts/rt_pyramids.py 31 100000000 C6 > data/night-C6.log 2>&1
for d in 60 100 150; do timeout 14400 python3 scripts/rt_pyramids.py $d 100000000 RT > data/night-RT-$d.log 2>&1; done
{ echo "# RT pyramids overnight"; for f in data/night-*.log; do echo "## $f"; tail -1 "$f"; done; } > night-summary.md
