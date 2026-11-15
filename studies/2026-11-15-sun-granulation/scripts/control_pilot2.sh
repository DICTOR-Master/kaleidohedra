S=$(cd "$(dirname "$0")/.." && pwd); PY=${PY:-python3}   # PY: a Python with numpy, scipy, scikit-image, matplotlib
mkdir -p $S/data/control-pilot $S/results/control-pilot && cd $S || exit 1
$PY scripts/control_voronoi.py data/control-pilot 500 12 2 0 1 2>&1 | tee results/control-pilot/data_v2.log | grep -q CONTROL_DATA_OK && \
$PY scripts/census.py data/control-pilot voronoi_n500_v2.0_z0.0_s1 img 0.0 0 hmax:0.1 1,2 60 results/control-pilot/c_v2.json 2>&1 | tee results/control-pilot/c_v2.log | grep -q CENSUS_OK && echo "FINAL ok" || echo "FINAL FAIL"
