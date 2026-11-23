#!/bin/bash
cd "$(dirname "$0")/.."; PY=${PY:-python3}
r() { timeout 120 $PY scripts/render.py data/cells/amber_aequus-$1_$2_6-5_cen.json renders/RENDER-aequus-amber-$3-$2.png "$4: amber cell, $2 mould" src/dice.json; }
r 377 bcc Th-RD12-D12-I12p-RT24p-60 "Th die RD12 + D12 + I12′ + RT24′ (60 faces; picker no. 377, not yet named)"
r 1 bcc DI-32-Ih1 "Aequus DI-32, Ih 1"
r 5 bcc CO-14-Oh1 "Aequus CO-14, Oh 1"
r 236 bcc Td-O8-4a-RT24-RT24p-28 "Td die (picker no. 236) O8/4a + RT24+RT24′/24a (28 faces)"
r 61 bcc TRT-16-T3 "Aequus TRT-16, T 3"
r 61 sc TRT-16-T3 "Aequus TRT-16, T 3"
