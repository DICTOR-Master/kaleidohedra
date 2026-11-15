#!/bin/bash
# Render + compose the Platonic series cover (circle design, see-through). Usage: bash run.sh TAG SS
# PY = a Python with numpy, scipy and Pillow (default python3).
# TAG final -> ../platonic-cover-front-series.png and ../platonic-dicto-mark-back.png; any other TAG -> ../pilot-TAG*.png
set -o pipefail
cd "$(dirname "$0")"
tag=$1; ss=$2
SS=$ss "${PY:-python3}" seethrough_circle.py "../circle-$tag.png" | tee ../render-$tag.log
grep -q "^FINAL ok" ../render-$tag.log || { echo "FINAL FAIL: render"; exit 1; }
if [ "$tag" = final ]; then out=../platonic-cover-front-series.png; mk=../platonic-dicto-mark-back.png; else out=../pilot-$tag-cover.png; mk=../pilot-$tag-mark.png; fi
"${PY:-python3}" compose.py "../circle-$tag.png" "$out" "$mk"
