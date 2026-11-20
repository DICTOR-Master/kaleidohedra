#!/usr/bin/env bash
# Build lake targets of the assembled entry on the compute host, each call under a 280 s limit and a 14 GB memory cap
# (no swap); prints errors, wall time and peak memory. Usage (from the entry root): bash build.sh TARGET...
cd "$(dirname "$0")/.." && mkdir -p logs && export PATH=$HOME/.elan/bin:$PATH
timeout 280 systemd-run --user --scope -q -p MemoryMax=14G -p MemorySwapMax=0 /usr/bin/time -v lake build "$@" > logs/last.log 2>&1
echo "EXIT $?" >> logs/last.log
cat logs/last.log >> logs/build-all.log
grep -E 'error|declaration uses|Built|Elapsed|Maximum resident|EXIT' logs/last.log | grep -v "^✔" | tail -40
