#!/bin/bash
# Render + compose the Platonic series cover (circle design, crystal). Usage: bash run.sh TAG WIDTH HEIGHT SAMPLES
# PY = a Python with numpy, scipy and Pillow (default python3).
# TAG final -> ../platonic-cover-front-series.png and ../platonic-dicto-mark-back.png; any other TAG -> ../pilot-TAG*.png
set -o pipefail
cd "$(dirname "$0")"
tag=$1; w=$2; h=$3; spp=$4
blender -b -P crystal_circle.py -- "$PWD/../circle-$tag.png" "$w" "$h" "$spp" 2>&1 | grep -v -E "^Fra:|Path Tracing Sample|Synchroniz|Updating|Loading|Compiling" | tee ../render-$tag.log
grep -q "^FINAL FAIL" ../render-$tag.log && { echo "FINAL FAIL: checks"; exit 1; }
grep -q . "../circle-$tag.png" || { echo "FINAL FAIL: no picture"; exit 1; }
if [ "$tag" = final ]; then out=../platonic-cover-front-series.png; mk=../platonic-dicto-mark-back.png; else out=../pilot-$tag-cover.png; mk=../pilot-$tag-mark.png; fi
"${PY:-python3}" -c "
from PIL import Image; im = Image.open('../circle-$tag.png')
im = im if im.size == (2400, 2200) else im.resize((2400, 2200), Image.LANCZOS); im.save('../circle-$tag-full.png')"
"${PY:-python3}" compose.py "../circle-$tag-full.png" "$out" "$mk"
