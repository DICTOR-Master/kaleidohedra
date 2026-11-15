S=~/k-research/studies/2026-11-15-atmosphere-seaice; PY=~/venvs/sun/bin/python
cd $S || exit 1; mkdir -p data/atm6 results/run2
echo "PROGRESS 0.00 fetch"
$PY scripts/fetch.py data/atm6 20250205 0000 0600 2.5 B03 R05 2420 4460 1000 4800 2 | grep -v PROGRESS | tee results/run2/fetch.log
grep -q FETCH_OK results/run2/fetch.log || { echo "FINAL FAIL fetch"; exit 1; }
echo "PROGRESS 0.40 controls"
$PY scripts/control.py data/atm6 0 1 2 0 24 data/c2_rigid > results/run2/ctl.log
$PY scripts/control.py data/atm6 0 1 2 0.02 24 data/c2_noise >> results/run2/ctl.log
$PY scripts/cellcensus.py data/c2_rigid open 3 0.05 1 10,20 400 250 500 results/run2/ctl_rigid.json | grep -v PROGRESS > results/run2/ctl_rigid.log
$PY scripts/cellcensus.py data/c2_noise open 3 0.05 1 10,20 400 250 500 results/run2/ctl_noise.json | grep -v PROGRESS > results/run2/ctl_noise.log
echo "PROGRESS 0.50 census (6 settings in parallel)"
pids=""
for sg in 1.5 3; do for h in 0.03 0.05 0.08; do
  ( $PY scripts/cellcensus.py data/atm6 open $sg $h 1,2,4,8 10,20,40 400 250 500 results/run2/atm_s${sg}_h$h.json | grep -v PROGRESS > results/run2/atm_s${sg}_h$h.log ) &
  pids="$pids $!"
done; done
for p in $pids; do wait $p; done
echo "PROGRESS 0.95 render"
$PY scripts/render.py data/atm6 open 3 0.05 400 250 500 results/run2/atm_s3_frame0.png
rm -rf data/c2_rigid data/c2_noise
n=$(cat results/run2/atm_*.log results/run2/ctl_*.log | grep -c CENSUS_OK)
rig=$(python3 -c "import json;d=json.load(open('results/run2/ctl_rigid.json'));print(sum(sum(v['counts_interior'].values()) for v in d['steps'].values()))")
echo "census ok: $n of 8; rigid control interior events: $rig (expect 0)"
[ "$n" = 8 ] && [ "$rig" = 0 ] && echo "FINAL ok" || echo "FINAL FAIL"
