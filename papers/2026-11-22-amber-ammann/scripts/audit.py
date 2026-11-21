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
for p, end in [("logs/tiling.log", "PATCH OK"), ("logs/summary.txt", "SUMMARY OK"), ("logs/job.log", "[exit 0]"),
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
for s in ["faces 1414: shared 998", "boundary 416, bad 0", "dihedral sum != 360 deg at 0", "difference 0 (exact 0)", "P 10/10, O 10/10", "3.55e-15", "1856.899327"]:
    ok(s in tl, "tiling.log: " + s)
ok(len({(t["kind"], tuple(t["A"])) for t in T}) == 20, "20 orientations")
for s in ["402 rhombohedra, 278 prolate and 124 oblate", "1414 faces", "998 shared", "416 on the boundary", "814 interior edges",
          "1856.899327", "217 interior vertices", "3.6·10", "1234/10007", "−567/10009", "891/10037"]: intext(s)
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
# --- summary rows (Theorem 1, Proposition 4, Table 2)
sm = rd("logs/summary.txt")
rows = {}
for l in sm.splitlines():
    m = re.match(r"(Fullerene Star|Rollerball|dodecahedron|icosahedron|icosidodecahedron)\s+(own|S0|S65)\s+(cen|cproj)\s+(.*)", l)
    if m: rows[(m[1], m[2], m[3])] = m[4]
def row(core, sc, sd, kP, kO, scP, scO, nP_, nO_, yP, yO):
    r = rows.get((core, sc, sd), "")
    exp = (f"valid P 10/10 O 10/10  kinds P {kP} O {kO} patch {kP + kO} (shared 0)  scutoids/cell P {scP}/{nP_} O {scO}/{nO_}"
           f"  Y/cell P {yP} O {yO}")
    ok(r.startswith(exp) and "irrational kind frequencies True" in r, f"summary row {core} {sc} {sd}: {r[:120]}")
for sc, sd in [("S0", "cen"), ("S65", "cen"), ("S65", "cproj"), ("own", "cen")]: row("Rollerball", sc, sd, 8, 8, 72, 72, 72, 72, 30, 30)
for sc in ("S0", "S65"): row("Fullerene Star", sc, "cproj", 9, 9, 66, 72, 80, 80, 48, 42)
for sd in ("cen", "cproj"): row("icosidodecahedron", "S65", sd, 5, 5, 20, 18, 32, 32, 30, 30)
for sc in ("S0", "S65"): row("icosahedron", sc, "cproj", 3, 3, 18, 18, 20, 20, 12, 12)
for sc in ("S0", "S65", "own"): row("icosahedron", sc, "cen", 3, 3, 0, 0, 20, 20, 0, 0)
for sc in ("S0", "S65", "own"): row("dodecahedron", sc, "cen", 2, 2, 0, 0, 12, 12, 0, 0)
row("dodecahedron", "S65", "cproj", 2, 2, 0, 0, 12, 12, 0, 0)
ok(rows[("Rollerball", "S0", "cproj")].startswith("valid P 10/10 O 0/10") and "self-intersecting" in rows[("Rollerball", "S0", "cproj")], "Rollerball S0 cproj near miss")
ok("empty outer cells" in rows[("Fullerene Star", "S0", "cen")] and "valid P 0/10 O 10/10" in rows[("Fullerene Star", "S0", "cen")], "FS cen near miss")
ok("Y vertex direction meets the mould" in rows[("icosidodecahedron", "S0", "cen")] and "valid P 10/10 O 0/10" in rows[("icosidodecahedron", "S0", "cen")], "ID S0 near miss")
# kinds: per block; P and O volumes disjoint (Theorem 1 (b), Proposition 4), Table A1
blocks = {}
cur = None
for l in sm.splitlines():
    m = re.match(r"--- (.+) (\S+) (\S+): kinds", l)
    if m: cur = (m[1], m[2], m[3]); blocks[cur] = []; continue
    m = re.match(r"\s+(\w+)\s+mP\s+(\d+) mO\s+(\d+) scutoid (\w+)\s+Y (\d+) facets (\d+) vol ([\d.]+)", l)
    if m and cur: blocks[cur].append((m[1], int(m[2]), int(m[3]), m[4] == "True", int(m[5]), int(m[6]), m[7]))
for key, K in blocks.items():
    vp = [float(k[6]) for k in K if k[1]]; vo = [float(k[6]) for k in K if k[2]]
    ok(all(not (k[1] and k[2]) for k in K), "kind in both types " + str(key))
    ok(min(abs(a - b) for a in vp for b in vo) > 1e-4, "volumes not separated " + str(key))
R = blocks[("Rollerball", "S0", "cen")]
gap = min((abs(float(a[6]) - float(b[6])), a[6], b[6]) for a in R if a[1] for b in R if b[2])
ok(f"{gap[0]:.4f}" == "0.0806" and gap[1:] == ("7.571397", "7.490844"), "closest pair " + str(gap)); intext("0.0806"); intext("7.571397"); intext("7.490844")
ok(sum(k[1] for k in R) == 72 and sum(k[2] for k in R) == 72 and all(k[3] for k in R), "72 + 72 scutoids")
ok(sum(k[1] for k in R if k[0] == "dec") == 12 and sum(k[2] for k in R if k[0] == "dec") == 12, "decagon pieces 6 + 6")
app = paper.split("Appendix: Table A1")[1].split("</table>")[0]
arows = re.findall(r"<td>(prolate|oblate)</td><td>(decagon|triangle)</td><td class=\"n\">(\d+)</td><td class=\"n\">(\d+)</td><td class=\"n\">(\d+)</td><td class=\"n\">([\d.]+)</td>", app)
exp = [("prolate" if k[1] else "oblate", {"dec": "decagon", "tri": "triangle"}[k[0]], str(k[1] or k[2]), str(k[4]), str(k[5]), k[6]) for k in R]
ok(arows == exp, "Table A1 differs from summary.txt")
# --- wall patterns (Theorem 3 (iii))
fm = [l for l in rd("logs/facematch.log").splitlines() if l.strip()]
ok(len(fm) == 8 and all("OO 61/61, OP 0/618, PP 319/319; all 380/998" in l for l in fm), "facematch 8 settings")
for s in ["C2 S0 cen", "C2 S65 cen", "C1 S0 cproj", "C1 S65 cproj", "icosahedron S0 cen", "icosahedron S0 cproj", "dodecahedron S0 cen", "icosidodecahedron S65 cen"]:
    ok(any(l.startswith(s + ":") for l in fm), "facematch setting " + s)
# mirror relation (computed): same-type neighbours are mirror images in the wall, prolate-oblate ones are not
p = (1 + 5 ** .5) / 2
E = [(0, 1, p), (0, -1, p), (1, p, 0), (-1, p, 0), (p, 0, 1), (-p, 0, 1)]
def add(u, v): return tuple(x + y for x, y in zip(u, v))
def sub(u, v): return tuple(x - y for x, y in zip(u, v))
def sc(k, u): return tuple(k * x for x in u)
def dot(u, v): return sum(x * y for x, y in zip(u, v))
def cross(u, v): return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
def dist(u, v): return dot(sub(u, v), sub(u, v)) ** .5
def P3(v6): return tuple(sum(v6[i] * E[i][r] for i in range(6)) for r in range(3))
def corners(t):
    out = []
    for s in itertools.product((1, -1), repeat=3):
        v = tuple(t["centre"])
        for i in range(3): v = add(v, sc(0.5 * s[i], E[t["A"][i]]))
        out.append(v)
    return out
def refl(x, X0, n): return sub(x, sc(2 * dot(sub(x, X0), n), n))
mc = Counter()
for a, b, pts in P["shared"]:
    X = [P3(q) for q in pts]; n = cross(sub(X[1], X[0]), sub(X[3], X[0])); n = sc(1 / dot(n, n) ** .5, n)
    Vb = corners(T[b])
    mir = all(min(dist(refl(v, X[0], n), w) for w in Vb) < 1e-9 for v in corners(T[a])) and dist(refl(tuple(T[a]["centre"]), X[0], n), tuple(T[b]["centre"])) < 1e-9
    mc[("".join(sorted(T[a]["kind"] + T[b]["kind"])), mir)] += 1
ok(mc == Counter({("OP", False): 618, ("PP", True): 319, ("OO", True): 61}), "mirror relation " + str(mc))
# --- seams (Theorem 3 (iv), Remark 6)
sl = rd("logs/seams_mirror.log")
for s in ["2-fold axis of the core: True", "cells reached 402/402", "{'identity': 428, 'improper': 368, 'proper': 202}", "rank 3, EMPTY",
          "interior edges 814 by number of cells round them: {3: 364, 4: 239, 5: 156, 6: 13, 7: 30, 8: 10, 9: 2}; odd: 552"]:
    ok(s in sl, "seams_mirror.log: " + s)
ok(364 + 239 + 156 + 13 + 30 + 10 + 2 == 814 and 364 + 156 + 30 + 2 == 552 and 428 + 368 + 202 == 998, "edge and loop sums")
for s in ["552 of the 814", "428 identity, 368 improper and 202 proper", "3 at 364 edges, 4 at 239, 5 at 156, 6 at 13, 7 at 30, 8 at 10, 9 at 2", "401 form a spanning tree"]: intext(s)
sw = [l for l in rd("logs/seams_wall.log").splitlines() if "RESULT" in l]
ok(len(sw) == 30 and all("valid=False" in l for l in sw), "wall-cast 30/30 fail")
# --- renders log
rl = rd("renders/scripts/ammann_scenes.log")
for s in ["19 prolate + 11 oblate", "wall OP: patterns agree exactly = False; regions on the wall: cell A 16, cell B 16; area A 3.236068",
          "wall PP: patterns agree exactly = True; regions on the wall: cell A 16, cell B 16", "cells 012 (oblate), 023, 024 (prolate)"]:
    ok(s in rl, "ammann_scenes.log: " + s)
for s in ["19 prolate", "11 oblate", "3.236068", "600 runs", "319 prolate–prolate", "61 oblate–oblate", "618 prolate–oblate", "all 380", "30 cases"]: intext(s)
# --- text consistency
for s in ["10.5281/zenodo.24411660", "10.5281/zenodo.24384789", "10.5281/zenodo.24111864", "#118 (proposed)"]: intext(s)
ok(not re.search(r"signature thread|Winston|house style|DICTO asked", text, re.I), "banned wording")
print("\n".join("FAIL " + f for f in fails) if fails else "AUDIT OK")
