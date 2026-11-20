#!/usr/bin/env python3
"""Assemble the local Palomar entry GrunbaumK10 (Grünbaum's zone question at k = 10) in the directory OUTDIR; nothing is
pushed or submitted. The witness is GET B (DICTO, 20 November 2026).
  Challenge.lean, Solution.lean   copies of Challenge/GrunbaumK10.lean and Solution/GrunbaumK10.lean here (= lean-B/);
  GET/*.lean                      the library: the 23 modules of lean-B/GET, written by make_witness_b.py from the GET A
                                  development of studies/2026-11-17-get-palomar (Lean core only: no classification, no
                                  second solid), unchanged;
  lakefile.toml, lean-toolchain, lake-manifest.json (from the GET study), comparator.json, LICENSE, README.md,
  formalization.yaml, scripts/ (Palomar template scripts check-lean-sources.py and verify-comparator.sh, as carried by
  the GET study, and this package's build.sh, run_comparator_lowmem.sh, run_comparator_split.sh,
  run_negative_controls.sh, run_fit_check.sh).
Usage: assemble_entry.py OUTDIR     (prints the sha256 of every assembled file to OUTDIR/SHA256SUMS)"""
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent
STUDIES = PKG.parent.parent
GET = STUDIES / "2026-11-17-get-palomar" / "lean"
OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)


LIB = PKG / "lean-B" / "GET"
keep = sorted(p.stem for p in LIB.glob("*.lean"))
assert len(keep) == 23 and "SphereB" in keep, keep
(OUT / "GET").mkdir(exist_ok=True)
for m in keep:
    t = (LIB / f"{m}.lean").read_text(encoding="utf-8")
    assert not re.search(r"^(public )?import (?!Mathlib$|GET\.)", t, re.M), m
    shutil.copy(LIB / f"{m}.lean", OUT / "GET" / f"{m}.lean")
assert (PKG / "lean-B" / "Challenge.lean").read_bytes() == (PKG / "Challenge" / "GrunbaumK10.lean").read_bytes()
assert (PKG / "lean-B" / "Solution.lean").read_bytes() == (PKG / "Solution" / "GrunbaumK10.lean").read_bytes()

shutil.copy(PKG / "Challenge" / "GrunbaumK10.lean", OUT / "Challenge.lean")
shutil.copy(PKG / "Solution" / "GrunbaumK10.lean", OUT / "Solution.lean")
shutil.copy(PKG / "comparator.json", OUT / "comparator.json")
shutil.copy(PKG / "palomar" / "formalization.yaml", OUT / "formalization.yaml")
shutil.copy(PKG / "palomar" / "README.md", OUT / "README.md")
for f in ["LICENSE", "lean-toolchain", "lake-manifest.json"]:
    shutil.copy(GET / f, OUT / f)
assert json.loads((OUT / "lake-manifest.json").read_text(encoding="utf-8"))["name"] == "GrunbaumK10"
(OUT / "lakefile.toml").write_text("""name = "GrunbaumK10"
version = "0.1.0"
defaultTargets = ["GET", "Challenge", "Solution"]

[[require]]
name = "mathlib"
git = "https://github.com/leanprover-community/mathlib4.git"
rev = "v4.35.0-rc2"

[[lean_lib]]
name = "GET"
globs = ["GET.+"]

[[lean_lib]]
name = "Challenge"
roots = ["Challenge"]

[[lean_lib]]
name = "Solution"
roots = ["Solution"]
""", encoding="utf-8")
(OUT / "scripts").mkdir(exist_ok=True)
for f in ["check-lean-sources.py", "verify-comparator.sh"]:
    shutil.copy(GET / "scripts" / f, OUT / "scripts" / f)
for f in ["run_comparator_lowmem.sh", "run_comparator_split.sh", "run_negative_controls.sh", "run_fit_check.sh",
          "build.sh"]:
    shutil.copy(PKG / "scripts" / f, OUT / "scripts" / f)
(OUT / ".gitignore").write_text("/.lake\n/logs\n", encoding="utf-8")

sums = []
for p in sorted(OUT.rglob("*")):
    if p.is_file() and ".lake" not in p.parts and "logs" not in p.parts and ".git" not in p.parts \
            and p.name != "SHA256SUMS":
        sums.append(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(OUT)}")
(OUT / "SHA256SUMS").write_text("\n".join(sums) + "\n", encoding="utf-8")
lines = sum((OUT / "GET" / f"{m}.lean").read_text(encoding="utf-8").count("\n") for m in keep)
print(f"library: {len(keep)} modules, {lines} lines; files: {len(sums)}")
