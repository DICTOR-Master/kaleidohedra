#!/bin/bash
cd ~/kres-tmp/star-cores-book
PY=~/geom/bin/python; DS=~/kres-tmp/dataset-v7
for s in hamlet:D108 ophelia:D109; do for T in phi 2; do
  WORKERS=5 nohup $PY scripts/valley_fast.py $DS dicto-${s%%:*} ${s##*:} $T $HOME/kres-tmp/star-cores-book/data/gaps/valleyfast-${s%%:*}-$T.json > logs/valleyfast-${s%%:*}-$T.log 2>&1 < /dev/null &
done; done
