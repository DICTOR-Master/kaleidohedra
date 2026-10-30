#!/bin/sh
# copy the script to dicto-big-brother, render there (foreground), fetch the pictures. Optional: QG_ONLY=wg,rg  QG_CFG='{"w_sink":0.2}'
set -e
D=$(dirname "$0")/..
scp -q "$D/scripts/queen_geodes.py" dicto-big-brother:kres-tmp/queen-geodes/
ssh dicto-big-brother "cd ~/kres-tmp/queen-geodes && uptime && QG_ONLY='${QG_ONLY:-wg,wd,rg,rd}' QG_CFG='${QG_CFG:-{\}}' ~/geom/bin/python queen_geodes.py ~/kres-tmp/4d/data/600cell-source.json ~/kres-tmp/alicia-plates/dicto-logo.png out"
scp -q 'dicto-big-brother:kres-tmp/queen-geodes/out/*' "$D/out/"
