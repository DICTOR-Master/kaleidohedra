S=$(cd "$(dirname "$0")/.." && pwd); PY=${PY:-python3}   # PY: a Python with numpy, scipy, scikit-image, matplotlib
mkdir -p $S/data/control-pilot $S/results/control-pilot && cd $S || exit 1
$PY scripts/control_voronoi.py data/control-pilot 500 20 20 0 1 | grep -v PROGRESS | tee results/control-pilot/data0.log | grep -q CONTROL_DATA_OK && \
$PY scripts/control_voronoi.py data/control-pilot 500 20 20 2 1 | grep -v PROGRESS | tee results/control-pilot/data2.log | grep -q CONTROL_DATA_OK && \
$PY scripts/census.py data/control-pilot voronoi_n500_v20.0_z0.0_s1 img 0.0 0 0.5 1,2 60 results/control-pilot/c0.json | grep -v PROGRESS | tee results/control-pilot/c0.log | grep -q CENSUS_OK && \
$PY scripts/census.py data/control-pilot voronoi_n500_v20.0_z2.0_s1 img 0.0 1.5 1 1,2 60 results/control-pilot/c2.json | grep -v PROGRESS | tee results/control-pilot/c2.log | grep -q CENSUS_OK && echo "FINAL ok" || echo "FINAL FAIL"
