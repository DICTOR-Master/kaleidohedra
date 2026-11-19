#!/usr/bin/env python3
"""Assemble the local Palomar entry for candidate D1 (nothing is pushed or submitted) in the directory OUTDIR:
  Challenge.lean, Solution.lean      the two files written by gen_challenge.py (Challenge/ and Solution/ here);
  DehnCanon/*.lean                   the library: exactly the import closure of DehnCanon.Dehn10Hilbert and
                                     DehnCanon.Dehn10Edges, from the study folders 2026-11-19-lean-dehn-1 ... -10,
                                     put in Palomar's module layout (`module`, `public import`, `@[expose] public
                                     section`; the leading comment and the rest of each file unchanged);
  lakefile.toml, lean-toolchain, lake-manifest.json, comparator.json, LICENSE, README.md, formalization.yaml,
  scripts/ (Palomar template scripts, as carried by the 2026-11-17-get-palomar entry, and this package's build.sh,
  run_comparator_lowmem.sh and run_negative_controls.sh).
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


def src(module):
    hits = sorted(STUDIES.glob(f"2026-11-19-lean-dehn-*/lean/{module}.lean"))
    assert len(hits) == 1, (module, hits)
    return hits[0]


def modulize(text):
    """leading plain comment kept; then `module`, the imports made public, `@[expose] public section`, the rest"""
    lines = text.split("\n")
    i = 0
    if lines[0].startswith("/-") and not lines[0].startswith(("/--", "/-!")):
        while not lines[i].rstrip().endswith("-/"):
            i += 1
        i += 1
    head, rest = lines[:i], lines[i:]
    k = 0
    imports = []
    while k < len(rest) and (rest[k].startswith("import ") or not rest[k].strip()):
        if rest[k].startswith("import "):
            imports.append("public " + rest[k])
        k += 1
    assert not any(l.startswith("import ") for l in rest[k:]), "an import after the leading block"
    return "\n".join(head + ["module", ""] + imports + ["", "@[expose] public section", ""] + rest[k:])


# library: the import closure of the two top files
todo, keep = ["Dehn10Hilbert", "Dehn10Edges"], set()
while todo:
    m = todo.pop()
    if m in keep:
        continue
    keep.add(m)
    deps = re.findall(r"^import DehnCanon\.(\S+)", src(m).read_text(encoding="utf-8"), re.M)
    assert not re.search(r"^import (?!Mathlib$|DehnCanon\.)", src(m).read_text(encoding="utf-8"), re.M), m
    todo += deps
(OUT / "DehnCanon").mkdir(exist_ok=True)
for m in sorted(keep):
    (OUT / "DehnCanon" / f"{m}.lean").write_text(modulize(src(m).read_text(encoding="utf-8")), encoding="utf-8")

shutil.copy(PKG / "Challenge" / "HilbertThird.lean", OUT / "Challenge.lean")
shutil.copy(PKG / "Solution" / "HilbertThird.lean", OUT / "Solution.lean")
shutil.copy(PKG / "comparator.json", OUT / "comparator.json")
shutil.copy(PKG / "palomar" / "formalization.yaml", OUT / "formalization.yaml")
shutil.copy(PKG / "palomar" / "README.md", OUT / "README.md")
shutil.copy(GET / "LICENSE", OUT / "LICENSE")
shutil.copy(GET / "lean-toolchain", OUT / "lean-toolchain")
manifest = json.loads((GET / "lake-manifest.json").read_text(encoding="utf-8"))
manifest["name"] = "HilbertThird"
(OUT / "lake-manifest.json").write_text(json.dumps(manifest, indent=1) + "\n", encoding="utf-8")
(OUT / "lakefile.toml").write_text("""name = "HilbertThird"
version = "0.1.0"
defaultTargets = ["DehnCanon", "Challenge", "Solution"]

[[require]]
name = "mathlib"
git = "https://github.com/leanprover-community/mathlib4.git"
rev = "v4.35.0-rc2"

[[lean_lib]]
name = "DehnCanon"
globs = ["DehnCanon.+"]

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
for f in ["run_comparator_lowmem.sh", "run_negative_controls.sh", "build.sh"]:
    shutil.copy(PKG / "scripts" / f, OUT / "scripts" / f)
(OUT / ".gitignore").write_text("/.lake\n/logs\n", encoding="utf-8")

sums = []
for p in sorted(OUT.rglob("*")):
    if p.is_file() and ".lake" not in p.parts and "logs" not in p.parts and p.name != "SHA256SUMS":
        sums.append(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(OUT)}")
(OUT / "SHA256SUMS").write_text("\n".join(sums) + "\n", encoding="utf-8")
lines = sum((OUT / "DehnCanon" / f"{m}.lean").read_text(encoding="utf-8").count("\n") for m in keep)
print(f"library: {len(keep)} modules, {lines} lines; files: {len(sums)}")
