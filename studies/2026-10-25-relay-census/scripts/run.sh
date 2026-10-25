#!/bin/bash
# Relay census: everything runs on dicto-big-brother (~/geom/bin/python: sympy, numpy, scipy), one job at a time, nice 10.
set -e; cd "$(dirname "$0")"
rsync -a --exclude data ../ dicto-big-brother:runs/relay-census/
ssh dicto-big-brother 'cd ~/runs/relay-census/scripts && uptime && mkdir -p ../data/raw ../data/checks &&
  for n in square honeycomb kagome bcc delian nacl zincblende hcpholes a15 c15; do nice -n 10 ~/geom/bin/python census.py $n | tail -1; done &&
  nice -n 10 ~/geom/bin/python relay.py > ../data/raw/relay-stdout.txt && tail -1 ../data/raw/relay-stdout.txt &&
  nice -n 10 ~/geom/bin/python perovskite.py > ../data/raw/perovskite-stdout.txt && tail -1 ../data/raw/perovskite-stdout.txt &&
  nice -n 10 ~/geom/bin/python crosscheck.py | tail -1 && nice -n 10 ~/geom/bin/python walls.py | tail -1 && python3 tables.py > ../data/raw/tables.md'
rsync -a dicto-big-brother:runs/relay-census/data/ ../data/
