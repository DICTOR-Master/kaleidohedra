#!/bin/bash
# Relay census: everything runs on compute-host (python3: sympy, numpy, scipy), one job at a time, nice 10.
set -e; cd "$(dirname "$0")"
rsync -a --exclude data ../ compute-host:runs/relay-census/
ssh compute-host 'cd ~/runs/relay-census/scripts && uptime && mkdir -p ../data/raw ../data/checks &&
  for n in square honeycomb kagome bcc delian nacl zincblende hcpholes a15 c15; do nice -n 10 python3 census.py $n | tail -1; done &&
  nice -n 10 python3 relay.py > ../data/raw/relay-stdout.txt && tail -1 ../data/raw/relay-stdout.txt &&
  nice -n 10 python3 perovskite.py > ../data/raw/perovskite-stdout.txt && tail -1 ../data/raw/perovskite-stdout.txt &&
  nice -n 10 python3 crosscheck.py | tail -1 && nice -n 10 python3 walls.py | tail -1 && python3 tables.py > ../data/raw/tables.md'
rsync -a compute-host:runs/relay-census/data/ ../data/
