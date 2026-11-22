#!/usr/bin/env python3
"""Collect the library of the DehnPackets entry into one folder, ready for the kit's assemble_entry.py.

The library is the prepared Packets project at its last building commit (ddb5f59), Packets/*.lean, plus the import
closure, in the registered Dehn Canon (github.com/DICTOR-Master/dehn-canon-lean at 9ea20f6, PALOMAR-2026-11-20-000003),
of the Canon modules it imports. The Canon modules go unchanged to Packets/Canon/<name>.lean and every
`import DehnCanon.X` line becomes `import Packets.Canon.X`; nothing else changes (the Lean namespaces stay
`DehnCanon.Library`, `Packets` and `PacketsGen`). This is the layout of the Dehn-Hadwiger 4D entry (its
prep_library.py). It replaces the Git dependency of the prepared project: the Canon repository has its own root
modules `Challenge` and `Solution`, which Palomar refuses as a shadowed Challenge root (challenge.module_root_shadowed).
One layout change in the generated files Packets/Gen*.lean: the list of face normals `XN` is put four to a line, as the
entry's gen_pieces.py now writes it (whitespace only, checked here), so that the Challenge, which copies these
definitions, stays near 300 lines.

Usage: prep_library.py PACKETS_REPO CANON_REPO OUTDIR     (git repositories; OUTDIR is created and must not exist)
"""
import re
import subprocess
import sys
from pathlib import Path

PACKETS_REV = "ddb5f59"
CANON_REV = "9ea20f6dfd64fc3f10f64b1fb59a754a77e5cf57"
packets, canon, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
out.mkdir(parents=True)


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, check=True).stdout


def files(repo, rev, folder):
    return [f for f in git(repo, "ls-tree", "--name-only", rev, folder + "/").split() if f.endswith(".lean")]


src = {}
for f in files(packets, PACKETS_REV, "Packets"):
    src["Packets." + Path(f).stem] = (packets, PACKETS_REV, f)
for f in files(canon, CANON_REV, "DehnCanon"):
    src["DehnCanon." + Path(f).stem] = (canon, CANON_REV, f)
text = {m: git(r, "show", f"{rev}:{f}") for m, (r, rev, f) in src.items()}
todo = [m for m in src if m.startswith("Packets.")]
seen = set()
while todo:
    m = todo.pop()
    if m in seen:
        continue
    seen.add(m)
    for mm in re.finditer(r"^(?:public )?import (\S+)", text[m], re.M):
        if not mm.group(1).startswith("Mathlib"):
            todo.append(mm.group(1))


def group_normals(t):
    """the `noncomputable def XN : Fin F → R3 :=` list, four vectors to a line (whitespace only)"""
    m = re.search(r"(noncomputable def \w+N : Fin \d+ → R3 :=\n  !\[)(.*?)\]\n", t, re.S)
    if not m:
        return t
    vecs = m.group(2).split(",\n    ")
    assert all(v.startswith("!₂[") and v.endswith("]") for v in vecs), "unexpected normal list layout"
    body = ",\n    ".join(", ".join(vecs[i:i + 4]) for i in range(0, len(vecs), 4))
    new = t[:m.start(2)] + body + t[m.end(2):]
    assert re.sub(r"\s", "", new) == re.sub(r"\s", "", t)
    return new


lines = 0
for m in sorted(seen):
    t = re.sub(r"^((?:public )?import )DehnCanon\.", r"\1Packets.Canon.", text[m], flags=re.M)
    if m.startswith("Packets.Gen"):
        t = group_normals(t)
    rel = Path("Canon", m.split(".", 1)[1] + ".lean") if m.startswith("DehnCanon.") else Path(m.split(".", 1)[1] + ".lean")
    (out / rel).parent.mkdir(parents=True, exist_ok=True)
    (out / rel).write_text(t, encoding="utf-8")
    lines += t.count("\n")
n_canon = sum(1 for m in seen if m.startswith("DehnCanon."))
print(f"{len(seen)} modules ({len(seen) - n_canon} Packets, {n_canon} Canon), {lines} lines -> {out}")
