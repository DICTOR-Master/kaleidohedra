#!/usr/bin/env python3
"""Collect the library of the DehnHadwiger4D entry into one folder, ready for the kit's assemble_entry.py.

The library is the import closure of DehnHadwiger.DH15Results600: the modules DehnHadwiger.* of this study
(lean/DehnHadwiger) and the modules DehnCanon.* of studies 2026-11-19-lean-dehn-1 to -10 that they import. All are put
under one module prefix, `DehnHadwiger`: the Canon modules as DehnHadwiger/Canon/<name>.lean, and every
`import DehnCanon.X` line becomes `import DehnHadwiger.Canon.X`. Nothing else changes (the Lean namespaces stay
`DehnCanon` and `DehnHadwiger`).

Usage: prep_library.py OUTDIR      (OUTDIR is created; it must not exist)
"""
import re
import sys
from pathlib import Path

STUDY = Path(__file__).resolve().parents[2]
STUDIES = STUDY.parent
out = Path(sys.argv[1])
out.mkdir(parents=True)
src = {}
for f in STUDIES.glob("2026-11-19-lean-dehn-*/lean/*.lean"):
    src["DehnCanon." + f.stem] = f
for f in (STUDY / "lean" / "DehnHadwiger").glob("DH*.lean"):
    src["DehnHadwiger." + f.stem] = f
todo, seen = ["DehnHadwiger.DH15Results600"], set()
while todo:
    m = todo.pop()
    if m in seen:
        continue
    seen.add(m)
    for line in src[m].read_text(encoding="utf-8").split("\n"):
        mm = re.match(r"import (\S+)", line)
        if mm and not mm.group(1).startswith("Mathlib"):
            todo.append(mm.group(1))
lines = 0
for m in sorted(seen):
    t = src[m].read_text(encoding="utf-8")
    t = re.sub(r"^import DehnCanon\.", "import DehnHadwiger.Canon.", t, flags=re.M)
    rel = Path("Canon", src[m].name) if m.startswith("DehnCanon.") else Path(src[m].name)
    (out / rel).parent.mkdir(parents=True, exist_ok=True)
    (out / rel).write_text(t, encoding="utf-8")
    lines += t.count("\n")
print(f"{len(seen)} modules, {lines} lines -> {out}")
