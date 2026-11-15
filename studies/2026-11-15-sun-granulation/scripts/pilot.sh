S=$(cd "$(dirname "$0")/.." && pwd); PY=${PY:-python3}   # PY: a Python with numpy, scipy, scikit-image, matplotlib
mkdir -p $S/data/pilot $S/results/pilot && cd $S || exit 1
$PY scripts/fetch_bifrost.py en024048_hion 303 308 data/pilot | tail -3 | tee results/pilot/fetch.log | grep -q FETCH_OK && \
$PY scripts/render_pilot.py data/pilot en024048_hion results/pilot | tee results/pilot/render.log && \
$PY scripts/census.py data/pilot en024048_hion lgtg 0.0 1.5 300 1,2 60 results/pilot/census_pilot.json | grep -v PROGRESS | tee results/pilot/census.log | grep -q CENSUS_OK && echo "FINAL ok" || echo "FINAL FAIL"
