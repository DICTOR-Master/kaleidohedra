#!/bin/sh
# copy the script to compute-host, render there (foreground), fetch the pictures. Optional: QG_ONLY=wg,rg  QG_CFG='{"w_sink":0.2}'
set -e
D=$(dirname "$0")/..
scp -q "$D/scripts/queen_geodes.py" compute-host:work/queen-geodes/
ssh compute-host "cd ~/work/queen-geodes && uptime && QG_ONLY='${QG_ONLY:-wg,wd,rg,rd}' QG_CFG='${QG_CFG:-{\}}' python3 queen_geodes.py ~/work/4d/data/600cell-source.json ~/work/alicia-plates/dicto-logo.png out"
scp -q 'compute-host:work/queen-geodes/out/*' "$D/out/"
