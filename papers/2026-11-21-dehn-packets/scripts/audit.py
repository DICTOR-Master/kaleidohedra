#!/usr/bin/env python3
"""Number audit for the Dehn packets draft: recompute every number of the text from exact forms and the study data.
Run from scripts/ with STUDIES pointing at the studies folder. Prints AUDIT OK or each failure."""
import math, json, os, re, glob
here = os.path.dirname(os.path.abspath(__file__))
S = os.environ.get("STUDIES", os.path.join(here, "..", "..", "..", "studies"))
paper = open(os.path.join(here, "..", "paper.html"), encoding="utf-8").read()
fails = []
def ok(cond, msg):
    if not cond: fails.append(msg)
def intext(s): ok(s in paper, "not in text: " + s)
phi = (1 + 5 ** .5) / 2; pi = math.pi
al = math.atan(phi); be = math.acos(1 / 6 ** .5); ga = math.acos((2 / 3) ** .5)
deg = math.degrees
vals = {"58.2825": al, "65.9052": be, "35.2644": ga, "138.1897": 1.5 * pi - 2 * be, "142.6226": .75 * pi - al + be,
        "69.0948": .75 * pi - be, "116.5651": 2 * al, "159.0948": 1.25 * pi - be, "148.2825": pi / 2 + al,
        "125.2644": pi / 2 + ga, "109.4712": pi - 2 * ga, "144.7356": pi - ga, "200.9052": .75 * pi + be,
        "211.7175": 1.5 * pi - al, "221.8103": pi / 2 + 2 * be, "243.4349": 2 * pi - 2 * al, "41.8103": 2 * be - pi / 2,
        "63.4349": pi - 2 * al, "20.9052": be - pi / 4}
for s, v in vals.items():
    ok(f"{deg(v):.4f}" == s, f"{s} recomputes as {deg(v):.6f}"); intext(s)
for s in ["138.19°", "200.91°", "221.81°", "159.09°", "20.91°"]: intext(s)
# exact cross-checks of angle identities (numerical sanity of proved identities)
ok(abs(math.acos(1 / (3 ** .5 * phi)) - (.75 * pi - be)) < 1e-12, "spike base angle")
ok(abs(math.acos(-0.8) - (4 * al - pi / 2)) < 1e-12, "tetrakis relation")
ok(abs(2 * ga - math.acos(1 / 3)) < 1e-12, "2 gamma = arccos 1/3")
ok(abs(2 * al - math.acos(-1 / 5 ** .5)) < 1e-12, "dodecahedron dihedral")
ok(abs(1.5 * pi - 2 * be - math.acos(-5 ** .5 / 3)) < 1e-12, "icosahedron dihedral")
# rings of Theorem 4 (c) and the TID rings
ok(abs(2 * al + 2 * (.75 * pi - al + be) + (1.5 * pi - 2 * be) - 3 * pi) < 1e-12, "ring 1")
ok(abs(2 * (.75 * pi - be) + 2 * (.75 * pi - al + be) + 2 * al - 3 * pi) < 1e-12, "ring 2")
ok(abs((1.25 * pi - be) + (pi / 2 + al) + (.75 * pi - al + be) - 2.5 * pi) < 1e-12, "TID sum 5pi/2")
fr = json.load(open(os.path.join(here, "..", "data", "fig-ring.json")))
for k in ("lead1", "lead2"): ok(abs(sum(x for _, x in fr[k]) - 540) < 1e-9, "figure ring " + k)
# packets
ok(12 * 5 + (60 * (-1) + 30 * 0) == 0 and 60 * (-1 + 1) + 30 * (-2) * 0 == 0, "packet arithmetic lead 1")
ok(5 * 12 - 60 == 0 and -3 * 20 + 60 == 0, "packet proportions")
ok(30 * (-2) + 60 * 1 == 0 and 30 * 2 + 60 * (-1) == 0, "C1, C2 packets")
# spherical areas (Lemma 10)
area = lambda cs: sum(cs) - (len(cs) - 2) * pi
c1 = [1.5 * pi - 2 * be, .75 * pi + be, .75 * pi + be, 2 * pi / 3]
ok(abs(area(c1) - 5 * pi / 3) < 1e-12, "C1 at v 5pi/3")
X = [2 * pi - c for c in c1]
ok(abs(area(X) - 7 * pi / 3) < 1e-12, "X 7pi/3")
ok(abs(5 * 2 * pi / 3 - 3 * pi - pi / 3) < 1e-12, "apex cone")
L = [1.25 * pi - be, 4 * pi / 3, be - pi / 4] * 2
ok(abs(area(L) - 2 * pi / 3) < 1e-12, "L 2pi/3")
ok(1.5 * pi - 2 * be + 2 * (.75 * pi + be) > 2 * pi and 2 * (.75 * pi + be) > 2 * pi, "B1, B3 bounds")
# screen counts
ld = json.load(open(os.path.join(S, "2026-11-21-packet-screen/data/leads.json")))
ok(ld["counts"] == {"zero": 3, "one": 10, "two": 17, "none": 17}, "screen counts " + str(ld["counts"]))
ok(len(ld["leads"]) == 26 and len(ld["two_helper"]) == 71, "26 and 71")
ok(all(x["exact"] for x in ld["leads"]) and all(x["exact"] for x in ld["two_helper"]), "all exact")
pk = json.load(open(os.path.join(S, "2026-11-21-packet-screen/data/packets.json")))
sc = pk["screen"]; ok(len(sc) == 47, "47 pyramids")
def n1(k): return len(sc[k].get("one_helper", []))
def n2(k): return len(sc[k].get("two_helpers", []))
for k, a, b in [("P[tetrahedron|3]", 5, 0), ("P[dodecahedron|5]", 1, 0), ("P[icosahedron|3]", 1, 0), ("P[icosidodecahedron|3]", 0, 21),
                ("P[truncated_dodecahedron|3]", 0, 2), ("P[truncated_dodecahedron|10]", 0, 2), ("P[truncated_icosahedron|5]", 0, 5),
                ("P[truncated_cuboctahedron|8]", 0, 1), ("P[tetrakis_hexahedron|3]", 1, 0)]:
    ok(k in sc and n1(k) == a and n2(k) == b, f"{k}: {n1(k) if k in sc else '-'} {n2(k) if k in sc else '-'}")
ok(sum(n1(k) for k in sc) == 26 and sum(n2(k) for k in sc) == 71, "sums over screen")
ok(sorted(k for k in sc if sc[k]["zero"]) == ["P[cube|4]", "P[rhombic_dodecahedron|4]", "P[rhombic_triacontahedron|4]"], "zero pyramids")
for c, n in [("zero", 3), ("none", 17)]:
    t = paper.split("Appendix: Table A1")[1].split("</table>")[0]
    cnt = sum(len(re.findall(r"\b" + c + r"\b", td)) for td in re.findall(r"<td>([^<]*)</td>\s*</tr>", t))
    ok(cnt == n, f"Table A1 {c}: {cnt}")
# Lemma 9 numbers
rt = json.load(open(os.path.join(S, "2026-11-21-scutoid-stand-in/data/round_trivial.json")))
for key, s in [("zc", "2.8842"), ("rp", "2.3274"), ("zA", "3.4410"), ("W", "7.8819"), ("vol_C1", "62.9508"), ("vol_K", "426.7088")]:
    ok(f"{rt[key]:.4f}" == s, f"{key} {rt[key]}"); intext(s)
ok(abs(rt["W"] - rt["h"]) < 1e-12 and rt["K_per_C1"] == 1, "slab period")
rl = json.load(open(os.path.join(S, "2026-11-21-scutoid-stand-in/data/round_local.json")))
ok(all(v for _, v in rl["checks"]), "round_local checks")
ok(rl["hexagons"] == {"max_shared_with_C1": 8, "min_K_hexagon_faces_per_C1": 12}, "hexagon bound")
# logs
for pat in ["2026-11-21-packet-screen/logs/*.log", "2026-11-21-packet-leads-tiling/logs/*.log"]:
    for f in glob.glob(os.path.join(S, pat)):
        if os.path.basename(f).startswith("relations"): continue
        ok("FINAL ok" in open(f).read().strip().splitlines()[-1], "log " + f.split("studies/")[-1])
for f in ["log.txt", "log_round.txt"]:
    ok("FINAL ok" in open(os.path.join(S, "2026-11-21-scutoid-stand-in", f)).read(), "log " + f)
lt = open(os.path.join(S, "2026-11-21-packet-leads-tiling/logs/angle_test.log")).read()
ok(lt.count("-> lead pieces cannot occur in any tiling") >= 20, "angle test verdicts")
ok("worst" not in paper or "−0.2432" in paper, "overlap number")
pl = open(os.path.join(S, "2026-11-21-scutoid-stand-in/log.txt")).read() + open(os.path.join(S, "2026-11-21-scutoid-stand-in/README.md")).read()
ok("-0.2432" in pl and "512" in pl, "placement numbers in study")
if fails:
    print("AUDIT FAIL"); [print("  " + x) for x in fails]; raise SystemExit(1)
print("AUDIT OK")
