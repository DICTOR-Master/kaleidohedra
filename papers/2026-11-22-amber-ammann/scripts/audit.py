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
# --- fresh review F1, F2 (24 Nov): bound "more than 0.0805"; own scales: two core sizes, none shared with the factor phi^-3 (core_sizes.py)
ok(m and float(m[6]) > 0.0805, "F1 gap above 0.0805"); intext("by more than 0.0805"); ok("at least 0.0806" not in text, "F1 old bound left")
cs = rd("logs/core_sizes.log")
ok(cs.strip().splitlines()[-1] == "FINAL ok" and "Table 2 own-scale settings passing: 3/3" in cs and cs.count("= phi^-3: True") == 3
   and cs.count("shared with the oblate volumes times phi^-3: 0") == 3, "core_sizes.log")
for core, n in [("Rollerball", 8), ("icosahedron", 3), ("dodecahedron", 2)]:
    ok(f"{core} own cen: s0 P" in cs and f"prolate {n}, oblate {n}; pairs compared {n * n}" in cs.split(f"{core} own cen:")[1].split("closest")[0], "core_sizes " + core)
for s in ["the two sizes differ by a factor of φ", "Rollerball 8 × 8, icosahedron 3 × 3, dodecahedron 2 × 2 pairs", "scripts/core_sizes.py, logs/core_sizes.log", "φ−3 = √5 − 2"]: intext(s)
# --- fresh review F3-F8: symmetry scope, criterion, local isomorphism, figure 2 label, public citations, power-diagram credit, labels
for s in ["Every tiling of the class has no period; the tiling built here has no symmetry other than the identity",
          "exactly when t = π(k) with π′(k) = γ − g′γ", "neither has its 402-cell patch", "the full symmetry group of three such lines is the stabiliser D3d",
          "Moody [9], §6, Theorems 8 to 10", "every generic 3D Penrose tiling of the class", "credited there to Aurenhammer and Imai 1988 [14]",
          "agree up to one common positive factor", "At S0, centroid seeds, let the pattern", "the scripts count from 0 and call it 023",
          "orientation 134", "reference cell 134 (123)", "share some segments but no region",
          "the cores cannot be placed as mirror images of their neighbours across all walls (Theorem 3 (iv))"]: intext(s)
ok(not re.search(r"REFEREE|referee|repetitive|Y-corner|moving the cores cannot", re.sub(r"<[^>]+>", "", paper.split('<div class="abstract">')[1])), "F: private file, repetitivity, Y-corners or old §5 lead left")
ok(rd("renders/scripts/ammann_compose.py").count("'never-repeating setting', 'no period')") == 1, "Figure 2 label 'no period'")
# Theorem 3 (iv) holds for the 120 elements: sym_check A2 density and A4 criterion are in the log
sc = rd("logs/sym_check.log")
ok("is an integer combination of e_1',...,e_6' for every i" in sc and "g with integral coordinates: 1 (the identity, k = 0)" in sc and "isometries of the patch: 1 (identity only)" in sc, "sym_check A2, A4, B")
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
# --- wall configurations (Theorem 3 (v)): every face-to-face tiling, 8 common-scale settings
wc = rd("logs/wall_configs.log")
ok("{'OO': 60, 'OP': 120, 'PP': 60}; total 240" in wc and wc.count("FINAL ok") == 8 and wc.count("OO 30/60, OP 0/120, PP 30/60") == 8, "wall_configs.log 120 walls, 8 settings")
for s in ["120 possible prolate–oblate walls", "scripts/wall_configs.py, logs/wall_configs.log", "(1, φ, φ) or (1/φ, 1/φ, 1)"]: intext(s)
# --- Theorem 3 (v): no common region on prolate-oblate walls (wall_disjoint.py), stacked pairs never in cut and project (stacked_pairs.py)
wd = rd("logs/wall_disjoint.log")
ok(wd.strip().splitlines()[-1] == "FINAL ok" and wd.count("prolate-oblate configurations 120, common polygons per configuration {0: 120}") == 8
   and wd.count("OO 30/30, PP 30/30; ok") == 8 and "settings passing: 8/8" in wd, "wall_disjoint.log: 0 common polygons, 8 settings")
for st in [l.split(":")[0] for l in wc.splitlines() if "per configuration, outer patterns agree" in l]:
    ok(st + ": prolate-oblate configurations 120, common polygons per configuration {0: 120}" in wd, "wall_disjoint setting " + st)
sp_ = rd("logs/stacked_pairs.log")
ok(sp_.strip().splitlines()[-1] == "FINAL ok" and "nonzero: True" in sp_ and "{'(1, phi, phi)': 30, '(1/phi, 1/phi, 1)': 30}; a coefficient exactly 1 in 60/60" in sp_
   and "between two tiles of one triple (stacked): 0" in sp_ and sp_.count("inside open set: False") == 60, "stacked_pairs.log: 60/60 on the boundary")
for s in ["scripts/wall_disjoint.py, logs/wall_disjoint.log", "scripts/stacked_pairs.py, logs/stacked_pairs.log", "share no region", "for all 60 choices of A and l"]: intext(s)
# --- seams (Theorem 3 (iv), Remark 6)
sl = rd("logs/seams_mirror.log")
for s in ["2-fold axis of the core: True", "cells reached 402/402", "{'identity': 428, 'improper': 368, 'proper': 202}", "rank 3, EMPTY"]:
    ok(s in sl, "seams_mirror.log: " + s)
ok(364 + 239 + 156 + 13 + 30 + 10 + 2 == 814 and 364 + 156 + 30 + 2 == 552 and 428 + 368 + 202 == 998 and 27 + 368 + 202 == 597 == 998 - 401, "edge and loop sums")
# --- Version 2 (decisions of 24 Nov): odd edges alone (items 1-3), symmetries (item 5), buried hexagons (item 6), Figure 3 dots (item 7)
oe = rd("logs/odd_edges.log")
for s in ["tree walls 401 (holonomy kinds {'identity': 401}); loops (non-tree walls) 597: {'improper': 368, 'proper': 202, 'identity': 27}", "odd interior edges 552",
          "(a) ODD EDGES ALONE: rank 3, EMPTY (inconsistent)", "distinct mirror planes among the odd edges: 96", "cells 5 plane", "cells 3 plane [0, 0, -2, 1+1r5]", "FINAL ok"]:
    ok(s in oe, "odd_edges.log: " + s)
for f in ("logs/sym_check.log", "logs/sym_check_cores.log", "logs/buried_hex.log"): ok("FINAL ok" in rd(f), f + " FINAL ok")
bh = rd("logs/buried_hex.log"); ok("sigma = -83/4+55/4r5" in bh and "15/2+3/2r5" in bh, "buried_hex sigma (-83+55r5)/4 below s0")
G = {t: json.load(open(os.path.join(A, f"renders/data/geom_C2_{t}_S0_cen.json"))) for t in ("023", "012")}
for t, g in G.items():
    Y = set(g["geom"]["Y"]); ok(len(Y) == 30 and sum(len({v for tr in pc["tris"] for v in tr} & Y) for pc in g["geom"]["pieces"]) == 180, "Figure 3 dots " + t)
for s in ["96 distinct planes", "180 separate dots", "(−83 + 55√5)/4", "597 holonomies", "AmberMirror.no_mirror_placement"]: intext(s)
for s in ["552 of the 814", "27 identity, 368 improper and 202 proper", "3 at 364 edges, 4 at 239, 5 at 156, 6 at 13, 7 at 30, 8 at 10, 9 at 2", "401 form a spanning tree"]: intext(s)
import glob
sw = sorted(glob.glob(os.path.join(A, "logs/exact/seam_*.log")))
ok(len(sw) == 30 and all("RESULT" in open(f).read() and "valid=False" in open(f).read() for f in sw), "wall-cast 30/30 fail (exact)")
# --- renders log
rl = rd("renders/scripts/ammann_scenes.log")
for s in ["19 prolate + 11 oblate", "wall OP: patterns agree exactly = False", "wall PP: patterns agree exactly = True", "cells 012 (oblate), 023, 024 (prolate)"]:
    ok(s in rl, "ammann_scenes.log: " + s)
for s in ["19 prolate", "11 oblate", "600 runs", "319 prolate–prolate", "61 oblate–oblate", "618 prolate–oblate", "all 380", "30 cases"]: intext(s)
# --- Version 2, 25 Nov: four new figures (ammann_scenes2.py, info2.json) and the RVCMG sentence
r2 = rd("renders/scripts/ammann_scenes2.log"); I2 = json.loads(rd("renders/html/info2.json"))
ok(r2.strip().splitlines()[-1] == "FINAL ok", "ammann_scenes2.log FINAL ok")
for s_ in ["all 20 orientations valid, 72 Scutoid-Frusta, 30 Y-vertices, 8 kinds each", "all 402 cells, 278 prolate + 124 oblate, 20 orientations",
           "Rollerball 72/72 Scutoid-Frusta, 30 Y; Fullerene Star 66/80 Scutoid-Frusta, 48 Y; icosidodecahedron 20/32 Scutoid-Frusta, 30 Y; icosahedron 18/20 Scutoid-Frusta, 12 Y; dodecahedron 0/12 Scutoid-Frusta, 0 Y",
           "centre |z| < 0.9, distance from the z axis < 6.2: 42 cells, 24 prolate + 18 oblate, 16 orientations, 3024 pieces",
           "bottom decagon, top pentagon, 10 neighbours on the core side, 5 on the mould side, 5 Y-vertices, 21 vertices, 48 edges, 29 flat faces"]:
    ok(s_ in r2, "ammann_scenes2.log: " + s_)
ok(I2["A"] == [402, 278, 124, 20] and I2["C"] == [42, 24, 18, 16, 3024] and I2["D"][:6] == [10, 5, 5, 21, 48, 29], "info2.json A, C, D")
ok([b[:4] for b in I2["B"]] == [["Rollerball", 72, 72, 30], ["Fullerene Star", 66, 80, 48], ["icosidodecahedron", 20, 32, 30], ["icosahedron", 18, 20, 12], ["dodecahedron", 0, 12, 0]], "info2.json B")
for core, (a, b_, y) in zip(["Rollerball", "Fullerene Star", "icosidodecahedron", "icosahedron", "dodecahedron"], [(72, 72, 30), (66, 80, 48), (20, 32, 30), (18, 20, 12), (0, 12, 0)]):
    r = es(core, "S65", "cproj").splitlines()[0]; ok(f"scutoids/cell P {a}/{b_}" in r and f"Y/cell P {y} " in r, "Figure 7 vs exact S65 cproj " + core)
ok(K[0][:2] == ("P", "dec") and K[0][4] == "5" and K[0][5] == "29" and K[0][7] == f"{I2['D'][6]:.6f}" == "43.253088", "Figure 3 piece = first kind of Table A1")
for s_ in ["278 prolate (sand) and 124 oblate (slate), in all 20 orientations", "all 20 orientations present (Figure 2)",
           "the first kind of Table A1, volume 43.253088", "Its face on the core is the decagon (pearl), with 10 neighbours", "its face on the mould is a pentagon (pale grey), with 5 neighbours",
           "its 5 Y-vertices", "21 vertices, 48 edges and 29 flat faces",
           "the 42 cells whose centres lie within 0.9 of one plane and within 6.2 of an axis normal to it", "√(2 + φ) ≈ 1.902", "24 prolate (sand) and 18 oblate (slate), in 16 of the 20 orientations", "3024 pieces in all",
           "72 of 72 pieces Scutoid-Frusta, 30 Y-vertices", "66 of 80, 48", "20 of 32, 30", "18 of 20, 12", "0 of 12, 0",
           "DICTO first made side-changing pieces in September 2026, the RVCMG adapters of Polyhedraverse, which join triangle, square and pentagon faces to a common hexagon by merging corners; they are degenerate Scutoid-Frusta, with the change of side count at the end rather than at Y-vertices (study rvcmg-scutoid-frusta"]: intext(s_)
ok(abs((2 + (1 + 5 ** .5) / 2) ** .5 - 1.902) < 5e-4, "cell edge sqrt(2 + phi)")
RV = os.path.join(S, "2026-11-24-rvcmg-scutoid-frusta", "data")
V_ = json.load(open(os.path.join(RV, "verdicts.json")))["verdicts"]
ok(len(V_) == 16 and all(v["flat"]["k"] == 0 for v in V_.values()) and [k for k, v in V_.items() if v["flat"]["simple"]] == ["RVCMG_V2_REGULAR_HEX_TO_UHEX"], "RVCMG: 16 pieces, no Y-vertex, 15 degenerate, 1 plain frustum")
ok(open(os.path.join(RV, "rvcmg_exact.log")).read().strip().splitlines()[-1] == "FINAL ok", "rvcmg_exact.log FINAL ok")
# figures: numbered 1-8 in order, every one full width, each referenced in the text
fn = re.findall(r"<figcaption><b>Figure (\d+)\.</b>", paper); ok(fn == [str(i) for i in range(1, 9)], "figure order " + str(fn))
ok(paper.count("<figure><img") == 8 and paper.count('<figure><img src="figures/') == paper.count('style="width:100%;margin:0 auto"'), "every figure full width")
body_ = paper.split('<div class="abstract">')[1]
for i in range(2, 9): ok(len(re.findall(rf"Figure {i}\b", body_)) >= 2, f"Figure {i} referenced outside its own caption")
# --- no floating-point wording left in claims
body = re.sub(r"<[^>]+>", "", paper.split('<div class="abstract">')[1].split("<h2>Data and reproducibility")[0])
ok(not re.search(r"floating|float\b|numerical|margin|sampling|computed\b", body, re.I), "float wording in the claims: " + str(re.findall(r".{30}(?:floating|float\b|numerical|margin|sampling|computed\b).{30}", body, re.I)[:3]))
# --- text consistency
for s in ["10.5281/zenodo.24411660", "10.5281/zenodo.24384789", "10.5281/zenodo.24111864", "Paper #118 · Version 2", "10.5281/zenodo.24491405"]: intext(s)
ok(not re.search(r"signature thread|Winston|house style|DICTO asked", text, re.I), "banned wording")
print("\n".join("FAIL " + f for f in fails) if fails else "AUDIT OK")
