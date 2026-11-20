#!/usr/bin/env python3
"""Write the Lean development with GET B as the witness (DICTO, 20 November 2026), into package/lean-B/:
  Challenge.lean, Solution.lean, GET/*.lean (the import closure of GET.Main; the module SphereA becomes SphereB).
Source: the GET A development of studies/2026-11-17-get-palomar (lean/, data/get-data.json, scripts/), which is not
changed. GET B has the same lattice basis and the same covolume 20 + 32 phi as GET A (get-data.json), so the lattice
part (the basis, the dual normals, the covolume) carries over word for word; only the witness data change:
  * Data.lean      the GET A data are removed; the GET B data (cellsB, facesB, basisB, matchB) are kept as generated;
  * Checks.lean    the GET A section of the pilot checks is removed; the GET B section is kept;
  * Certs.lean     regenerated for GET B by the generator of the GET study (gen_certs.py), run here on the B data:
                   the exact faces XB, the zone certificate ZB and the face matching MB (the calibration solids as
                   before);
  * SphereData.lean regenerated for GET B by the generator of the GET study (gen_sphere.py) on the B faces, from the
                   same centre c0 = (0, phi, 1 + phi) = (1/2) sum of the six axes, giving SPB;
  * SphereA.lean -> SphereB.lean: the cell of GET B that holds c0 and the parameters of c0 in it are found here
                   exactly (in Q(phi)) and written in place of `CA 14` and `tc0`;
  * every other module: the names of the witness are renamed from A to B (PA -> PB, FA -> FB, CA -> CB, XA -> XB,
                   MA -> MB, ZA -> ZB, SPA -> SPB, bA -> bB, BA -> BB, mA -> mB, δA -> δB, bbA -> bbB, GA -> GB,
                   cellsA -> cellsB, ..., and the theorem prefixes A_, PA_, FA_, ...), by identifier segments, so that
                   a bare variable `A` and names such as `XAcross` are untouched; "GET A" in comments becomes "GET B";
  * Challenge.lean the docstring of the witness names GET B (no definition or statement changes);
    Solution.lean  the same docstring change and the renamed witness names; GET/Statement.lean is regenerated from the
                   Challenge exactly as gen_statement.py of the GET study does.
All exact facts are then re-decided by the Lean kernel (`decide +kernel`); this script only proposes data.
Usage: make_witness_b.py   (run on the compute host: the sphere certificates take a little computation)"""
import importlib.util
import json
import re
import shutil
import sys
from fractions import Fraction as Fr
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent
STUDIES = PKG.parent.parent
GS = STUDIES / "2026-11-17-get-palomar"
SRC = GS / "lean"
OUT = PKG / "lean-B"
if OUT.exists():
    shutil.rmtree(OUT)
(OUT / "GET").mkdir(parents=True)

# ---------- the import closure of GET.Main in the GET A development ----------
todo, keep = ["Main"], set()
while todo:
    m = todo.pop()
    if m in keep:
        continue
    keep.add(m)
    todo += re.findall(r"^public import GET\.(\S+)", (SRC / "GET" / f"{m}.lean").read_text(encoding="utf-8"), re.M)
text = {m: (SRC / "GET" / f"{m}.lean").read_text(encoding="utf-8") for m in keep}
text["Challenge"] = (SRC / "Challenge.lean").read_text(encoding="utf-8")
text["Solution"] = (SRC / "Solution.lean").read_text(encoding="utf-8")

# ---------- the generators of the GET study, run on GET B ----------
data = json.loads((GS / "data" / "get-data.json").read_text(encoding="utf-8"))
assert data["A"]["basis"] == data["B"]["basis"] and data["A"]["covolume"] == data["B"]["covolume"]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    return spec, mod


# getgeom.py reads the A data at import; load it, then point its tables at B
spec, gg = load("getgeom", GS / "scripts" / "getgeom.py")
spec.loader.exec_module(gg)
gg.D = data["B"]
gg.CELLS = [(tuple(c[0]), tuple(c[1])) for c in gg.D["cells"]]
gg.FACES = [(tuple(f[0]), f[1], f[2], f[3]) for f in gg.D["faces"]]
gg.BA = gg.D["basis"]


def run_generator(path, subst):
    """run a generator of the GET study with textual substitutions (the witness and the output file)"""
    src = path.read_text(encoding="utf-8")
    for old, new in subst:
        assert src.count(old) >= 1, (path.name, old)
        src = src.replace(old, new)
    g = {"__file__": str(path), "__name__": "__main__"}
    exec(compile(src, str(path), "exec"), g)


certs = OUT / "GET" / "Certs.lean"
run_generator(GS / "scripts" / "gen_certs.py", [
    ("json.load(open(os.path.join(ROOT, 'data', 'get-data.json')))['A']",
     "json.load(open(os.path.join(ROOT, 'data', 'get-data.json')))['B']"),
    ('lean_X("XA", XA, "the 30 faces of GET A: corner `posn p`, sides `axis a`, `axis b`")',
     'lean_X("XB", XA, "the 30 faces of GET B: corner `posn p`, sides `axis a`, `axis b`")'),
    ('lean_Z("ZA", 30, zone_cert(XA, 10), "zone certificate of GET A")',
     'lean_Z("ZB", 30, zone_cert(XA, 10), "zone certificate of GET B")'),
    ("def MA : Fin 30", "def MB : Fin 30"),
    ("os.path.join(ROOT, 'lean', 'GET', 'Certs.lean')", repr(str(certs))),
])
sphd = OUT / "GET" / "SphereData.lean"
run_generator(GS / "scripts" / "gen_sphere.py", [
    ("from getgeom import *", "from getgeom import *\nFACES = sys.modules['getgeom'].FACES"),
    ('"def SPA : List', '"def SPB : List'),
    ("os.path.join(ROOT, 'lean', 'GET', 'SphereData.lean')", repr(str(sphd))),
])
for m in ("Certs", "SphereData"):
    text[m] = (OUT / "GET" / f"{m}.lean").read_text(encoding="utf-8")
assert "GET A" not in text["Certs"] and "def XB" in text["Certs"] and "def SPB" in text["SphereData"]

# ---------- the cell of GET B that holds the centre c0, exactly in Q(phi) ----------
# elements x + y phi with rational x, y; phi^2 = phi + 1
def qa(a, b): return (a[0] + b[0], a[1] + b[1])
def qs(a, b): return (a[0] - b[0], a[1] - b[1])
def qm(a, b): return (a[0] * b[0] + a[1] * b[1], a[0] * b[1] + a[1] * b[0] + a[1] * b[1])
def qinv(a):
    n = a[0] * a[0] + a[0] * a[1] - a[1] * a[1]          # norm of x + y phi
    return (Fr(a[0] + a[1]) / n, Fr(-a[1]) / n)
def qsign(a):
    return gg.zsign((a[0], a[1])) if all(Fr(t).denominator == 1 for t in a) else None
def det3(u, v, w):
    return qs(qa(qm(u[0], qs(qm(v[1], w[2]), qm(v[2], w[1]))), qm(u[2], qs(qm(v[0], w[1]), qm(v[1], w[0])))),
              qm(u[1], qs(qm(v[0], w[2]), qm(v[2], w[0]))))
C0 = ((0, 0), (0, 1), (1, 1))
hits = []
for n, (p, (i, j, k)) in enumerate(gg.CELLS):
    r = gg.vsub(C0, gg.posn(p))
    E = [gg.AX[i], gg.AX[j], gg.AX[k]]
    d = det3(*E)
    t = []
    for s in range(3):
        M = list(E); M[s] = r
        t.append(qm(det3(*M), qinv(d)))
    if all(all(Fr(c).denominator == 1 for c in x) for x in t):
        ti = [(int(x[0]), int(x[1])) for x in t]
        if all(gg.zsign(x) >= 0 and gg.zsign(gg.zsub((1, 0), x)) >= 0 for x in ti):
            hits.append((n, ti))
assert hits, "c0 lies in no cell of GET B with integral parameters"
cell, tc0 = hits[0]
print("c0 lies in cell", cell, "of GET B with parameters", tc0, "; all hits:", hits)

# ---------- rename the witness from A to B ----------
SEG = {"PA", "FA", "CA", "XA", "BA", "mA", "bA", "δA", "GA", "MA", "bbA", "SPA", "ZA", "A", "SphereA",
       "cellsA", "facesA", "basisA", "matchA"}
IDENT = re.compile(r"[A-Za-zδ_][A-Za-z0-9δ_'!?]*(?:\.[A-Za-zδ_][A-Za-z0-9δ_'!?]*)*")


def rename_token(tok):
    if tok == "A":
        return tok                                   # a bare variable A is not the witness
    parts = re.split(r"([._])", tok)
    return "".join(p[:-1] + "B" if p in SEG else p for p in parts)


def rename(t):
    t = t.replace("GET A", "GET B")
    return IDENT.sub(lambda mo: rename_token(mo.group(0)), t)


# GET A parts removed before renaming (their B counterparts are already in the files)
t = text["Data"]
i, j = t.index("/-- the 16 cells of GET A"), t.index("/-- the 16 cells of GET B")
text["Data"] = t[:i] + t[j:]
text["Data"] = text["Data"].replace("/-! Exact data of GET A and GET B", "/-! Exact data of GET B")
text["Checks"], n = re.subn(r"\nsection A\n.*?\nend A\n", "\n", text["Checks"], flags=re.S)
assert n == 1
text["Checks"] = text["Checks"].replace("the exact facts of GET A and GET B (pilot)", "the exact facts of GET B (pilot)")

# the centre's cell in SphereA
t = text["SphereA"]
old_tc0 = "def tc0 : Fin 3 → ZPhi := ![⟨2, -1⟩, ⟨2, -1⟩, ⟨-1, 1⟩]"
assert t.count(old_tc0) == 1 and t.count("CA 14") >= 4 and t.count("⟨14, ?_⟩") == 1
t = t.replace(old_tc0, "def tc0 : Fin 3 → ZPhi := ![" + ", ".join(f"⟨{a}, {b}⟩" for a, b in tc0) + "]")
t = t.replace("CA 14", f"CA {cell}").replace("⟨14, ?_⟩", f"⟨{cell}, ?_⟩")
text["SphereA"] = t

for m in list(text):
    if m not in ("Certs", "SphereData"):
        text[m] = rename(text[m])
text["SphereB"] = text.pop("SphereA")

# Statement.lean from the new Challenge, as gen_statement.py does
head = text["Challenge"].split("-- END DEFINITIONS")[0].rstrip() + "\n\nend GrunbaumK10\n"
head = head.replace("/-!\n# Grünbaum's zone question at k = 10\n",
                    "/-!\n# Grünbaum's zone question at k = 10: the definitions (generated from Challenge.lean)\n", 1)
text["Statement"] = head

for m, t in text.items():
    assert not re.search(r"\b(cellsA|facesA|basisA|matchA|PA|FA|CA|XA|MA|SPA|ZA)\b|GET A|SphereA", t), m
    dest = OUT / (f"{m}.lean" if m in ("Challenge", "Solution") else f"GET/{m}.lean")
    dest.write_text(t, encoding="utf-8")
print("wrote", len(text), "files to", OUT)
