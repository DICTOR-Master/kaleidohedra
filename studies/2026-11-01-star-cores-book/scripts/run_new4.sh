#!/bin/bash
# runs on dicto-big-brother in ~/kres-tmp/star-cores-book: treatment, polar fill, valley rule and exact core cycle for D106-D109
set -x
B=~/kres-tmp/star-cores-book; DS=~/kres-tmp/dataset-v7; S=~/kres-tmp/star-cores/scripts; PY=~/geom/bin/python
cd $B && mkdir -p data && cp $DS/build/exactlib.py $B/ 2>/dev/null
$PY scripts/new4.py $DS $B/data $S > data/new4.log 2>&1
cd $B && $PY $S/polar_spikes.py $DS data/star-cores-new4.json > data/polar-new4.log 2>&1 && mv data/polar-spikes.json data/polar-spikes-new4.json
$PY $S/star_valley.py $DS data/star-cores-new4.json data/valley-new4 4 > data/valley-new4.log 2>&1 &
STUDY2B_LIMIT=1500 $PY ~/kres-tmp/star-cores-exact/scripts/study2b.py $DS/solids $DS/build data/star-cores-new4.json data/study2b-new4.json 0 4 > data/study2b-new4.log 2>&1 &
wait
echo ALLDONE
