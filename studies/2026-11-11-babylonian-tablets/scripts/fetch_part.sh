#!/bin/bash
# fetch one HeiCuBeDa part from heiDATA (resumable), check its size against the dataset listing, list its PLY files
set -u; id=$1; dir=~/kres-tmp/tablets; cd $dir
want=$(curl -s "https://heidata.uni-heidelberg.de/api/datasets/:persistentId/?persistentId=doi:10.11588/data/IE8CCN" | python3 -c "import json,sys;print([f['dataFile']['filesize'] for f in json.load(sys.stdin)['data']['latestVersion']['files'] if f['dataFile']['id']==$id][0])")
( while sleep 120; do echo "PROGRESS $(stat -c %s part_$id.zip 2>/dev/null || echo 0) of $want bytes"; done ) & HB=$!   # heartbeat (11-11: a silent curl looked stalled)
for t in 1 2 3; do curl -s -L -C - -o part_$id.zip "https://heidata.uni-heidelberg.de/api/access/datafile/$id" -H "User-Agent: dicto-research" && break; echo "retry $t"; done
kill $HB 2>/dev/null; got=$(stat -c %s part_$id.zip); echo "size $got want $want"
[ "$got" = "$want" ] || { echo "FINAL FAIL size mismatch"; exit 1; }
unzip -l part_$id.zip | grep -c -i "\.ply$" | sed 's/^/ply files: /'
echo "FINAL ok"
