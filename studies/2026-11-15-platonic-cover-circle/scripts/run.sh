#!/bin/bash
# Render + compose the Platonic series cover (circle design). Usage: bash run.sh TAG SS      PY = a Python with numpy, scipy, Pillow.
# TAG final -> ../platonic-cover-front-series.png and ../platonic-dicto-mark-back.png; any other TAG -> ../pilot-TAG*.png
set -o pipefail
cd "$(dirname "$0")"
tag=$1; ss=$2
SS=$ss "${PY:-python3}" circle_scene.py "../circle-$tag.png" | tee /dev/stderr | grep -q '^FINAL ok' || { echo "FINAL FAIL: render"; exit 1; }
if [ "$tag" = final ]; then out=../platonic-cover-front-series.png; mk=../platonic-dicto-mark-back.png; else out=../pilot-$tag-cover.png; mk=../pilot-$tag-mark.png; fi
"${PY:-python3}" compose.py "../circle-$tag.png" "$out" "$mk"
