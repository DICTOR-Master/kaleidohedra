"""Pentakis dodecahedron core inside Minana #377 (26 Nov 2026). DICTO's plan: build the 60-face Th die Minana #377 (RD12 + D12 + I12' + RT24',
12 squares at the dodecahedron's sites) round a fullerene-based core with 60 faces to match Minana's 60 (DICTO: "no star, just fullerene core", "it has to have 60 sides",
"yes option 1 pentakis"): the pentakis dodecahedron, the dual of C60 (one triangle per C60 corner); resin cut into Scutoid-Frusta. With Claude (Anthropic).
Method: exactly amber_aequus.py (seeds, walls, Y vertices, all checks: closed oriented pieces, embedded, positive exact volume, volumes
add to mould - core exactly), with the inner solid = the pentakis dodecahedron (polar of the truncated icosahedron of resin.build_C1) and the mould = Minana #377's own
face planes, scaled by FACTOR x s0 (s0 = smallest scale holding the core). The core is turned (90 degrees about z, inside T_h if needed)
so its 12 five-fold corners point at Minana's 12 squares; this is checked exactly.
Usage: python pentakis_in_minana.py FACTOR SEED   (e.g. 6/5 cen)"""
import sys
from fractions import Fraction as Fr
argv = list(sys.argv); sys.argv = sys.argv[:1]
import amber_aequus as A
from resin import Q, dot, cross, det3, build_C1
sys.argv = argv

D = A.build("aequus-377")                       # the die, face planes (u, c): u.x <= c
C1 = build_C1()
TV = C1["TV"]; TIf = [(f, "pent") for f in C1["pents"]] + [(f, "hex") for f in C1["hexes"]]
def plane(f):
    P = [TV[i] for i in f]; n = cross([P[1][j] - P[0][j] for j in range(3)], [P[2][j] - P[0][j] for j in range(3)])
    if dot(n, P[0]).sign() < 0: n = [-x for x in n]
    return (n, dot(n, P[0]))
PL = [plane(f) for f, k in TIf]
PV = [[x / c for x in n] for n, c in PL]          # pentakis corners: polar of the TI faces (12 five-fold, 20 six-fold)
PF = []                                           # one triangle per TI corner v: the three TI faces at v, in turn
import itertools
for i in range(len(TV)):
    fs = [k for k, (f, kind) in enumerate(TIf) if i in f]; assert len(fs) == 3
    a, b, c = fs
    if det3(PV[a], PV[b], PV[c]).sign() < 0: b, c = c, b
    PF.append(([a, b, c], "tri"))
C1 = dict(C1, V=PV, faces=PF, planes=[(TV[i], Q(1)) for i in range(len(TV))])
assert all(all((dot(TV[i], PV[k]) - 1).sign() == 0 for k in PF[i][0]) for i in range(len(TV))), "pentakis face planes v.x = 1"

squares = [D["planes"][t][0] for t, (vs, k) in enumerate(D["faces"]) if len(vs) == 4]
assert len(squares) == 12, len(squares)
par = lambda a, b: all(x.sign() == 0 for x in cross(a, b))
def aligned(pd): return all(any(par(q, d) for d in pd) for q in squares)
if not aligned(C1["pd"]):
    turn = lambda v: [v[1], -v[0], v[2]]        # 90 degrees about z
    C1 = dict(C1, V=[turn(v) for v in C1["V"]], planes=[(turn(n), c) for n, c in C1["planes"]], pd=[turn(d) for d in C1["pd"]])
    assert aligned(C1["pd"]), "no T_h turn puts the pentagons on Minana's squares"
    print("core turned 90 degrees about z", flush=True)
print("CHECK the 12 five-fold corners point at Minana's 12 squares (exact): ok", flush=True)
# orbits under T_h (exact): core faces vs Minana's faces
from resin import TH, act
def orbits(dirs):
    seen, out = set(), []
    for i, d in enumerate(dirs):
        if i in seen: continue
        o = {j for g in TH for j, e in enumerate(dirs) if par(act(g, d), e) and dot(act(g, d), e).sign() > 0}
        seen |= o; out.append(len(o))
    return sorted(out)
print("T_h orbits of faces: core", orbits([n for n, c in C1["planes"]]), " Minana", orbits([u for u, c in D["planes"]]), flush=True)

H1 = [(u, c) for (u, c) in D["planes"]]
def shell(lat, s): return [(u, s * c) for (u, c) in H1]
Z = Q(0); vol = Z
for mi, poly in A.mould_faces(H1):
    for q in range(1, len(poly) - 1):
        d = det3(poly[0], poly[q], poly[q + 1]); vol = vol + (d if d.sign() > 0 else -d)
A.CELLVOL["minana"] = vol / 6
A.shell = shell
A.build = lambda name: dict(V=C1["V"], faces=C1["faces"], planes=C1["planes"], name=name)
sys.argv = [argv[0], "pentakis", "minana", argv[1], argv[2]]
A.main()
