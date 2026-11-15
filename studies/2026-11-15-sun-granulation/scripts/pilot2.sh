S=$(cd "$(dirname "$0")/.." && pwd); PY=${PY:-python3}   # PY: a Python with numpy, scipy, scikit-image, matplotlib
cd $S || exit 1; mkdir -p results/pilot2
ok=1
for H in thr:0.0 thr:0.5 hmax:500; do
  $PY scripts/census.py data/pilot en024048_hion uz 0.1 1.5 $H 1,2 60 results/pilot2/uz_$H.json 2>&1 | grep -v PROGRESS | tee results/pilot2/uz_$H.log | grep -q CENSUS_OK || ok=0
  echo "PROGRESS 0.3 done $H"
done
[ $ok = 1 ] && echo "FINAL ok" || echo "FINAL FAIL"
