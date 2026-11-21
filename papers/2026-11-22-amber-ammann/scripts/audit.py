#!/usr/bin/env python3
"""Number audit for the Amber-Ammann draft: every number of the text checked against the study's exact data and logs.
Run from scripts/ with STUDIES pointing at the studies folder. Prints AUDIT OK or each failure."""
import itertools, json, os, re
from collections import Counter
from fractions import Fraction as Fr
here = os.path.dirname(os.path.abspath(__file__))
S = os.environ.get("STUDIES", os.path.join(here, "..", "..", "..", "studies"))
A = os.path.join(S, "2026-11-21-amber-ammann")
paper = open(os.path.join(here, "..", "paper.html"), encoding="utf-8").read()
text = re.sub(r"<[^>]+>", "", paper)
fails = []
def ok(c, m):
    if not c: fails.append(m)
def intext(s): ok(s in text, "not in text: " + s)
def rd(p): return open(os.path.join(A, p)).read()
# --- logs end as they should
for p, end in [("logs/tiling.log", "PATCH OK"), ("logs/job.log", "[exit 0]"),
               ("renders/scripts/ammann_scenes.log", "FINAL ok")]:
    ok(rd(p).strip().splitlines()[-1].startswith(end), "log end " + p)
ok("FINAL ok" in rd("logs/job.log").strip().splitlines()[-2], "job.log FINAL ok")
# --- patch (Lemma 2)
P = json.load(open(os.path.join(A, "data/patch.json"))); T = P["tiles"]
nP = sum(t["kind"] == "P" for t in T); nO = len(T) - nP
ok((len(T), nP, nO) == (402, 278, 124), f"tiles {len(T)} {nP} {nO}")
ok(P["shared_faces"] == 998 and P["boundary_faces"] == 416 and P["interior_edges"] == 814 and P["interior_vertices"] == 217, "faces/edges")
ok(P["shared_by_pair"] == {"OP": 618, "OO": 61, "PP": 319}, "shared by pair " + str(P["shared_by_pair"]))
ok(P["checks_ok"] and P["freq_ratio_P_O"] == "1/2+1/2r5", "patch checks / frequency")
tl = rd("logs/tiling.log")
for s in ["faces 1414: shared 998", "boundary 416, bad 0", "dihedral sum != 360 deg at 0", "difference 0 (exact 0)", "P 10/10, O 10/10", "1856.899327"]:
    ok(s in tl, "tiling.log: " + s)
ok(len({(t["kind"], tuple(t["A"])) for t in T}) == 20, "20 orientations")
for s in ["402 rhombohedra, 278 prolate and 124 oblate", "1414 faces", "998 shared", "416 on the boundary", "814 interior edges",
          "1856.899327", "1234/10007", "−567/10009", "891/10037"]: intext(s)
ok(abs(278 * (3 + 5 ** .5) + 124 * (1 + 5 ** .5) - 1856.899327) < 1e-5, "volume sum")
# --- scales (Table 1): s0.txt; s0(O) = phi s0(P) exactly (a + b r5 arithmetic in fractions)
phi = (Fr(1, 2), Fr(1, 2))
def mul(x, y): return (x[0] * y[0] + 5 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])
def parse(t):
    t = t.strip()
    if "r5" not in t: return (Fr(t), Fr(0))
    a, b = t[:-2].rsplit("+", 1)
    return (Fr(a), Fr(b))
want = {"C2": ((6, 3), (Fr(21, 2), Fr(9, 2))), "C1": ((Fr(15, 2), Fr(3, 2)), (Fr(15, 2), Fr(9, 2))), "icosidodecahedron": ((6, 0), (3, 3)),
        "icosahedron": ((3, 0), (Fr(3, 2), Fr(3, 2))), "dodecahedron": ((Fr(3, 2), Fr(3, 2)), (Fr(9, 2), Fr(3, 2)))}
for line in rd("data/s0.txt").splitlines():
    w = line.split(); sP = parse(w[3].split("=")[1]); sO = parse(w[4].split("=")[1])
    ok(mul(phi, sP) == sO, f"phi s0P != s0O for {w[0]}")
    ok(tuple(map(Fr, want[w[0]][0])) == sP and tuple(map(Fr, want[w[0]][1])) == sO, f"Table 1 values {w[0]}")
    ok("S0=O" in line, "oblate binds " + w[0])
for s in ["6 + 3√5", "(21 + 9√5)/2", "(15 + 3√5)/2", "(15 + 9√5)/2", "3 + 3√5", "(3 + 3√5)/2", "(9 + 3√5)/2"]: intext(s)
# --- exact runs (Theorem 1, Proposition 4, Table 2): logs/exact/summary/<solid>_<scale>_<seed>.txt from exact_summary.py
NM = {"Rollerball": "C2", "Fullerene Star": "C1"}
def es(core, sc, sd):
    t = rd(f"logs/exact/summary/{NM.get(core, core)}_{ {'own': '1'}.get(sc, sc)}_{sd}.txt")
    ok(t.strip().endswith("EXACT SUMMARY OK"), f"exact summary {core} {sc} {sd}")
    return t
def row(core, sc, sd, kP, kO, scP, scO, nP_, nO_, yP, yO):
    r = es(core, sc, sd).splitlines()[0]
    exp = (f"valid P 10/10 O 10/10  orbit check True  rotation check True  kinds P {kP} O {kO} shared 0  scutoids/cell P {scP}/{nP_} O {scO}/{nO_}"
           f"  Y/cell P {yP} O {yO}")
    ok(r.endswith(exp), f"exact row {core} {sc} {sd}: {r[:160]}")
for sc, sd in [("S0", "cen"), ("S65", "cen"), ("S65", "cproj"), ("own", "cen")]: row("Rollerball", sc, sd, 8, 8, 72, 72, 72, 72, 30, 30)
for sc in ("S0", "S65"): row("Fullerene Star", sc, "cproj", 9, 9, 66, 72, 80, 80, 48, 42)
for sd in ("cen", "cproj"): row("icosidodecahedron", "S65", sd, 5, 5, 20, 18, 32, 32, 30, 30)
for sc in ("S0", "S65"): row("icosahedron", sc, "cproj", 3, 3, 18, 18, 20, 20, 12, 12)
for sc in ("S0", "S65", "own"): row("icosahedron", sc, "cen", 3, 3, 0, 0, 20, 20, 0, 0)
for sc in ("S0", "S65", "own"): row("dodecahedron", sc, "cen", 2, 2, 0, 0, 12, 12, 0, 0)
row("dodecahedron", "S65", "cproj", 2, 2, 0, 0, 12, 12, 0, 0)
r = es("Rollerball", "S0", "cproj"); ok("valid P 10/10 O 0/10" in r and "self-intersecting" in r, "Rollerball S0 cproj near miss")
r = es("Fullerene Star", "S0", "cen"); ok("valid P 0/10 O 10/10" in r and "empty outer cells" in r, "FS cen near miss")
r = es("icosidodecahedron", "S0", "cen"); ok("valid P 10/10 O 0/10" in r and "Y vertex direction meets the mould" in r, "ID S0 near miss")
# kinds of the Rollerball (Theorem 1 (b), Table A1), exact volumes
t = es("Rollerball", "S0", "cen")
K = re.findall(r"  ([PO]) (dec|tri)\s+x\s*(\d+) scutoid (\w+)\s+Y (\d+) facets (\d+) vol (\S+) = ([\d.]+)", t)
ok(len(K) == 16 and all(k[3] == "True" for k in K), "16 kinds, all scutoids")
ok(sum(int(k[2]) for k in K if k[0] == "P") == 72 and sum(int(k[2]) for k in K if k[0] == "O") == 72, "72 + 72")
ok(sum(int(k[2]) for k in K if k[1] == "dec" and k[0] == "P") == 12 and sum(int(k[2]) for k in K if k[1] == "dec" and k[0] == "O") == 12, "decagon 6 + 6")
m = re.search(r"closest prolate/oblate kind volumes: (\S+) = ([\d.]+) and (\S+) = ([\d.]+); exact difference (\S+) = (-?[\d.]+)", t)
ok(m and (m[2], m[4]) == ("7.571397", "7.490844") and m[6] == "0.080553" and m[5] != "0", "closest pair " + (m[0] if m else "none"))
for s in ["0.0806", "7.571397", "7.490844", "13861/3648", "73841/43776"]: intext(s)
app = paper.split("Appendix: Table A1")[1].split("</table>")[0]
arows = re.findall(r"<td>(prolate|oblate)</td><td>(decagon|triangle)</td><td class=\"n\">(\d+)</td><td class=\"n\">(\d+)</td><td class=\"n\">(\d+)</td><td class=\"n\">([\d.]+)</td>", app)
exp = [({"P": "prolate", "O": "oblate"}[k[0]], {"dec": "decagon", "tri": "triangle"}[k[1]], k[2], k[4], k[5], k[7]) for k in K]
ok(arows == exp, "Table A1 differs from the exact summary")
# --- exact patch facts (Theorem 3 (iii), (iv)): mirror relation and odd edges
pe = rd("logs/exact/patch_exact.log")
ok(pe.strip().endswith("PATCH EXACT OK") and "{('OP', False): 618, ('OO', True): 61, ('PP', True): 319}" in pe, "patch_exact mirror")
ok("interior edges 814 by number of cells round them (exact, integer): {3: 364, 4: 239, 5: 156, 6: 13, 7: 30, 8: 10, 9: 2}; odd: 552" in pe, "patch_exact edges")
# --- wall patterns, exact (facematch_exact.py), 8 settings
for s in ["C2 S0 cen", "C2 S65 cen", "C1 S0 cproj", "C1 S65 cproj", "icosahedron S0 cen", "icosahedron S0 cproj", "dodecahedron S0 cen", "icosidodecahedron S65 cen"]:
    l = rd("logs/exact/fm_" + s.replace(" ", "_") + ".log")
    ok(l.startswith(s + ":") and "OO 61/61, OP 0/618, PP 319/319; all 380/998" in l, "facematch exact " + s)
# --- seams (Theorem 3 (iv), Remark 6)
sl = rd("logs/seams_mirror.log")
for s in ["2-fold axis of the core: True", "cells reached 402/402", "{'identity': 428, 'improper': 368, 'proper': 202}", "rank 3, EMPTY"]:
    ok(s in sl, "seams_mirror.log: " + s)
ok(364 + 239 + 156 + 13 + 30 + 10 + 2 == 814 and 364 + 156 + 30 + 2 == 552 and 428 + 368 + 202 == 998, "edge and loop sums")
for s in ["552 of the 814", "428 identity, 368 improper and 202 proper", "3 at 364 edges, 4 at 239, 5 at 156, 6 at 13, 7 at 30, 8 at 10, 9 at 2", "401 form a spanning tree"]: intext(s)
import glob
sw = sorted(glob.glob(os.path.join(A, "logs/exact/seam_*.log")))
ok(len(sw) == 30 and all("RESULT" in open(f).read() and "valid=False" in open(f).read() for f in sw), "wall-cast 30/30 fail (exact)")
# --- renders log
rl = rd("renders/scripts/ammann_scenes.log")
for s in ["19 prolate + 11 oblate", "wall OP: patterns agree exactly = False", "wall PP: patterns agree exactly = True", "cells 012 (oblate), 023, 024 (prolate)"]:
    ok(s in rl, "ammann_scenes.log: " + s)
for s in ["19 prolate", "11 oblate", "600 runs", "319 prolate–prolate", "61 oblate–oblate", "618 prolate–oblate", "all 380", "30 cases"]: intext(s)
# --- no floating-point wording left in claims
body = re.sub(r"<[^>]+>", "", paper.split('<div class="abstract">')[1].split("<h2>Data and reproducibility")[0])
ok(not re.search(r"floating|float\b|numerical|margin|sampling|computed\b", body, re.I), "float wording in the claims: " + str(re.findall(r".{30}(?:floating|float\b|numerical|margin|sampling|computed\b).{30}", body, re.I)[:3]))
# --- text consistency
for s in ["10.5281/zenodo.24411660", "10.5281/zenodo.24384789", "10.5281/zenodo.24111864", "#118 (proposed)"]: intext(s)
ok(not re.search(r"signature thread|Winston|house style|DICTO asked", text, re.I), "banned wording")
print("\n".join("FAIL " + f for f in fails) if fails else "AUDIT OK")
