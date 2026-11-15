S=~/k-research/studies/2026-11-15-atmosphere-seaice; PY=~/venvs/sun/bin/python
cd $S || exit 1; mkdir -p data/atm1 data/ice1 results/pilot
echo "PROGRESS 0.00 fetch"
$PY scripts/fetch.py data/atm1 20250205 0000 0100 2.5 B03 R05 2420 4460 1000 4800 2 | grep -v PROGRESS | tee results/pilot/fetch_atm.log
$PY scripts/fetch.py data/ice1 20250227 0000 0300 10 B03 R05 350 750 4700 5250 1 | grep -v PROGRESS | tee results/pilot/fetch_ice.log
echo "PROGRESS 0.30 census"
$PY scripts/control.py data/atm1 0 2 3 0 12 data/ctl_rigid | tee results/pilot/ctl.log
$PY scripts/control.py data/atm1 0 2 3 0.02 12 data/ctl_noise | tee -a results/pilot/ctl.log
$PY scripts/cellcensus.py data/ctl_rigid open 1.5 0.03 1 5,10 300 100 100 results/pilot/ctl_rigid.json | grep -v PROGRESS | tee results/pilot/ctl_rigid.log
$PY scripts/cellcensus.py data/ctl_noise open 1.5 0.03 1 5,10 300 100 100 results/pilot/ctl_noise.json | grep -v PROGRESS | tee results/pilot/ctl_noise.log
echo "PROGRESS 0.50 atm"
for h in 0.03 0.06; do $PY scripts/cellcensus.py data/atm1 open 1.5 $h 1,2,4 5,10,20 400 300 700 results/pilot/atm_h$h.json | grep -v PROGRESS | tee results/pilot/atm_h$h.log; done
echo "PROGRESS 0.80 ice"
for h in 0.35 0.5; do $PY scripts/cellcensus.py data/ice1 floe 0.7 $h 1,2,3 20,30,60 300 50 120 results/pilot/ice_h$h.json all 6 | grep -v PROGRESS | tee results/pilot/ice_h$h.log; done
$PY scripts/render.py data/atm1 open 1.5 0.03 400 300 700 results/pilot/atm_frame0.png
$PY scripts/render.py data/ice1 floe 0.7 0.35 300 50 120 results/pilot/ice_frame0.png
n=$(grep -c CENSUS_OK results/pilot/*.log | awk -F: '{s+=$2} END {print s}')
rig=$(python3 -c "import json;d=json.load(open('results/pilot/ctl_rigid.json'));print(sum(sum(v['counts_interior'].values()) for v in d['steps'].values()))")
echo "census ok: $n of 6; rigid-drift control interior events: $rig (expect 0)"
grep -q FETCH_OK results/pilot/fetch_atm.log && grep -q FETCH_OK results/pilot/fetch_ice.log && [ "$n" = 6 ] && [ "$rig" = 0 ] && echo "FINAL ok" || echo "FINAL FAIL"
