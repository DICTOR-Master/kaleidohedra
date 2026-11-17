#!/bin/bash
# Build the replay trees (shape-kernel pilot, 2026-11-18). For each case two copies of the original study files:
#   orig/  the original scripts and modules, unchanged
#   kern/  the same, except the exact-number module is the kernel shim from replay/shims/ (the scripts themselves unchanged)
# plus the stored outputs (stored/) to compare with. Originals are only read. usage: setup.sh <studies root>
set -e
S=${1:-$HOME/k-research/studies}
R=$(cd "$(dirname "$0")" && pwd)
rm -rf "$R/cases"; mkdir -p "$R/cases"

# A (G1, class Q5): 2026-11-13-paradigm-exact, hemi_exact.py and scutoid_exact.py, module q5.py
for t in orig kern; do
  d="$R/cases/paradigm-exact/$t"; mkdir -p "$d/scripts" "$d/input"
  cp "$S/2026-11-13-paradigm-exact/scripts/"{hemi_exact.py,scutoid_exact.py,q5.py} "$d/scripts/"
  cp "$S/2026-11-11-hemi-rd-build/data/dicto-build-worldpoly.json" "$d/input/"
done
d="$R/cases/paradigm-exact/kern/scripts"
{ cat "$R/shims/paradigm-exact_q5_head.py"; sed -n '/^def facets(P):/,$p' "$S/2026-11-13-paradigm-exact/scripts/q5.py"; } > "$d/q5.py"
mkdir -p "$R/cases/paradigm-exact/stored"
cp "$S/2026-11-13-paradigm-exact/data/"{hemi-exact.log,scutoid-exact.log} "$R/cases/paradigm-exact/stored/"

# B (G2, class QF with class-level field): 2026-11-13-platonic-fans-law, fans_law.py (exec's qf.py)
for t in orig kern; do
  d="$R/cases/fans-law/$t"; mkdir -p "$d/scripts" "$d/input" "$d/data"
  cp "$S/2026-11-13-platonic-fans-law/scripts/"{fans_law.py,qf.py} "$d/scripts/"
  cp "$S/2026-11-13-platonic-disc-ranking/data/"{registry-solids.json,disc-ranking.json} "$d/input/"
done
cp "$R/shims/fans-law_qf.py" "$R/cases/fans-law/kern/scripts/qf.py"
mkdir -p "$R/cases/fans-law/stored"
cp "$S/2026-11-13-platonic-fans-law/data/"{fans-law.log,fans-law.json,fans-pilot.log} "$R/cases/fans-law/stored/"

# C (G3, Fraction pairs): 2026-10-18-ocd-octet, step12_exact_faces.py (imports exactpoly.py, which imports q5.py)
for t in orig kern; do
  d="$R/cases/ocd-octet/$t"; mkdir -p "$d/scripts" "$d/data"
  cp "$S/2026-10-18-ocd-octet/scripts/"{step12_exact_faces.py,exactpoly.py,q5.py} "$d/scripts/"
  cp "$S/2026-10-18-ocd-octet/data/"{step1-ocd-exact.json,step2-octet-frame.json,step5-keyed-octet.json,step10-meshes.json} "$d/data/"
done
cp "$R/shims/ocd-octet_q5.py" "$R/cases/ocd-octet/kern/scripts/q5.py"
mkdir -p "$R/cases/ocd-octet/stored"
cp "$S/2026-10-18-ocd-octet/data/"{step12.log,step12-faces.json} "$R/cases/ocd-octet/stored/"
echo "setup ok: $(find "$R/cases" -type f | wc -l) files"
