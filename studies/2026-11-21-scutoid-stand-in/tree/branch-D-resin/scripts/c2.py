"""Branch D lead 3: the resin solution for C2 = truncated dodecahedron (edge 1) with an icosahedron centre pyramid on each of its 20 triangles
(apex at the icosahedron's centre height phi^2/(2 sqrt3) above the triangle, lateral edges = icosahedron circumradius, checked exactly).
Mould = Voronoi cell of sc / bcc / fcc at the smallest scale holding C2 (exact, Q(sqrt5)); division R1 central (cone from the centre over
each face).  Valid when C2 is star-shaped from its centre with all face planes at positive offset (checked exactly); the volume identity
sum(pieces) = mould - C2 is checked exactly.  Kinds: T_h face orbits, merged when congruent.  Usage: python c2.py out.json"""
import itertools, json, sys
from fractions import Fraction as Fr
import numpy as np
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from resin import Q, PHI, dot, cross, vsub, vadd, vsc, det3, TH, act, polytope, analyse, congruent
def pr(*a): print(*a, flush=True)
half = PHI*Fr(1, 2)            # scale factor phi/2 takes the standard edge 2/phi to 1
base = [(Q(0), (PHI - 1), 2+PHI), ((PHI - 1), PHI, 2*PHI), (PHI, Q(2), PHI+1)]
TV, seen = [], set()
for b in base:
    for sg in itertools.product((1, -1), repeat=3):
        t = [b[i]*sg[i]*half for i in range(3)]
        for c in ([t[0], t[1], t[2]], [t[2], t[0], t[1]], [t[1], t[2], t[0]]):
            k = tuple(x.key() for x in c)
            if k not in seen: seen.add(k); TV.append(c)
assert len(TV) == 60
one = Q(1)
d2 = lambda a, b: dot(vsub(a, b), vsub(a, b))
nb = {i: [j for j in range(60) if j != i and (d2(TV[i], TV[j]) - one).sign() == 0] for i in range(60)}
assert all(len(v) == 3 for v in nb.values()), "edge length 1 check"
dd = []
for a, b in itertools.product((1, -1), repeat=2):
    t = [Q(0), PHI*a, Q(b)]; dd += [[t[0], t[1], t[2]], [t[2], t[0], t[1]], [t[1], t[2], t[0]]]
td = [[Q(a), Q(b), Q(c)] for a, b, c in itertools.product((1, -1), repeat=3)]
for a, b in itertools.product((1, -1), repeat=2):
    t = [Q(0), (PHI-1)*a, PHI*b]; td += [[t[0], t[1], t[2]], [t[2], t[0], t[1]], [t[1], t[2], t[0]]]
def face(d):
    vals = [dot(d, v) for v in TV]; m = vals[0]
    for x in vals:
        if (x - m).sign() > 0: m = x
    idx = [i for i in range(60) if (vals[i] - m).sign() == 0]
    cyc = [idx[0]]
    while len(cyc) < len(idx): cyc.append([j for j in nb[cyc[-1]] if j in idx and j not in cyc][0])
    return cyc
decs = [face(d) for d in dd]; tris = [face(d) for d in td]
assert all(len(f) == 10 for f in decs) and all(len(f) == 3 for f in tris)
R2 = (PHI + 2)*Fr(1, 4)
apex = []
for d, f in zip(td, tris):
    cen = [sum((TV[i][j] for i in f), Q(0))*Fr(1, 3) for j in range(3)]
    A = vadd(cen, vsc(PHI*PHI*Fr(1, 6), d))
    for i in f: assert (d2(A, TV[i]) - R2).sign() == 0, "lateral edge = icosahedron circumradius"
    apex.append(A)
V = TV + apex
faces = [(f, "dec") for f in decs]
for p, f in enumerate(tris):
    for i in range(3): faces.append(([f[i], f[(i+1) % 3], 60+p], "tri"))
planes = []
for f, kind in faces:
    P = [V[i] for i in f]; n = cross(vsub(P[1], P[0]), vsub(P[2], P[0]))
    if kind == "dec": inner = [Q(0)]*3
    else:
        p = f[2] - 60; cp = [sum((TV[i][j] for i in tris[p]), Q(0))*Fr(1, 3) for j in range(3)]; inner = vsc(Fr(1, 2), vadd(cp, apex[p]))
    if dot(n, vsub(inner, P[0])).sign() > 0: n = vsc(-1, n)
    planes.append((n, dot(n, P[0])))
pr(f"C2: 60 truncated-dodecahedron vertices (edge 1 exact), 20 apices (lateral edges^2 = (phi+2)/4 exact); faces 12 decagons + 60 triangles")
star = all(c.sign() > 0 for n, c in planes)
pr(f"star check (all 72 face planes at positive offset from the centre, exact): {star}")
volC2 = Q(0)
for (f, kind) in faces:
    P = [V[i] for i in f]
    for q in range(1, len(P) - 1):
        d = det3(P[0], P[q], P[q+1]); volC2 = volC2 + (d if d.sign() > 0 else -d)
volC2 = volC2/6
pr(f"vol C2 = {volC2} = {float(volC2):.10f}")
edge_face = {}
for fi, (f, kind) in enumerate(faces):
    for i in range(len(f)): edge_face.setdefault(frozenset((f[i], f[(i+1) % len(f)])), []).append(fi)
assert all(len(v) == 2 for v in edge_face.values())
keyv = {tuple(x.key() for x in v): i for i, v in enumerate(V)}
fid = {frozenset(f): i for i, (f, k) in enumerate(faces)}
def gface(g, fi): return fid[frozenset(keyv[tuple(x.key() for x in act(g, V[i]))] for i in faces[fi][0])]
orbits, done = [], set()
for fi in range(len(faces)):
    if fi in done: continue
    o = sorted({gface(g, fi) for g in TH}); done |= set(o); orbits.append(o)
pr("T_h face orbits:", [(faces[o[0]][1], len(o)) for o in orbits])
def shell(lat, s):
    H = []
    if lat in ("sc", "bcc"):
        for i in range(3):
            for sg in (1, -1):
                n = [Q(0)]*3; n[i] = Q(sg); H.append((n, s*Fr(1, 2), ("shell", f"e{i}{sg}")))
    if lat == "bcc":
        for sg in itertools.product((1, -1), repeat=3): H.append(([Q(x) for x in sg], s*Fr(3, 4), ("shell", f"111{sg}")))
    if lat == "fcc":
        for i, j in ((0, 1), (1, 2), (0, 2)):
            for a, b in itertools.product((1, -1), repeat=2):
                n = [Q(0)]*3; n[i] = Q(a); n[j] = Q(b); H.append((n, s*Fr(1, 2), ("shell", f"{i}{j}{a}{b}")))
    return H
cellvol = {"sc": Fr(1), "bcc": Fr(1, 2), "fcc": Fr(1, 4)}
out = dict(volC2=str(volC2), star=star, arrangements=[]); allok = star
for lat in ("sc", "bcc", "fcc"):
    s = None
    for n, c, _ in shell(lat, Q(1)):
        for v in V:
            r = dot(n, v)/c
            if s is None or (r - s).sign() > 0: s = r
    Hs = shell(lat, s)
    reps, total = [], Q(0)
    for o in orbits:
        fi = o[0]; f, kind = faces[fi]; n, c = planes[fi]
        H = [(vsc(-1, n), -c, ("bottom", fi))]
        cen = [sum((V[i][j] for i in f), Q(0))/len(f) for j in range(3)]
        for i in range(len(f)):
            a, b = V[f[i]], V[f[(i+1) % len(f)]]; m = cross(a, b)
            if dot(m, cen).sign() < 0: m = vsc(-1, m)
            G = [g for g in edge_face[frozenset((f[i], f[(i+1) % len(f)]))] if g != fi][0]
            H.append((vsc(-1, m), Q(0), ("lat", G)))
        H += Hs
        P = polytope(H); A = analyse(P, H, False)
        total = total + P["vol"]*len(o)
        fl = np.array([[float(x) for x in v] for v in P["verts"]])
        reps.append(dict(face=fi, kind=kind, orbit=len(o), vol=float(P["vol"]), volx=str(P["vol"]), verts=fl.tolist(), **A))
    gap = total - (s*s*s*cellvol[lat] - volC2)
    ok = gap.sign() == 0 and star; allok = allok and ok
    kinds = []
    for r in reps:
        for k in kinds:
            if abs(k["vol"] - r["vol"]) < 1e-9 and congruent(np.array(k["verts"]), np.array(r["verts"])): k["members"].append(r["face"]); break
        else: kinds.append(dict(r, members=[r["face"]]))
    pr(f"\n=== {lat}: s0 = {s} = {float(s):.6f}; cell {float(s*s*s*cellvol[lat]):.4f}, resin {float(s*s*s*cellvol[lat] - volC2):.4f}, "
       f"C2 share {float(volC2/(s*s*s*cellvol[lat])):.4f}; volume sum - resin = {gap} => {'VALID (exact)' if ok else 'NOT valid'}")
    for k in kinds:
        pr(f"   kind {k['kind']} face {k['face']} ({sum(len(o) for o in orbits if o[0] in k['members'])} per cell): F={k['nF']} V={k['nV']} "
           f"faces {k['face_sizes']} top facets {k['n_top']} Y={k['Y']} scutoid={k['scutoid']} vol={k['vol']:.6f}")
        pr("      dihedrals: " + "; ".join(f"{a['deg']:.4f} {a['pair']} [{a['basis'] or 'not in basis'}]" for a in k["angles"]))
    pr(f"   SUMMARY C2 {lat} s0 R1: kinds {len(kinds)}, scutoid kinds {sum(1 for k in kinds if k['scutoid'])}, valid {ok}")
    out["arrangements"].append(dict(lattice=lat, s=str(s), valid=ok, n_kinds=len(kinds), kinds=kinds))
json.dump(out, open(sys.argv[1] if len(sys.argv) > 1 else "c2.json", "w"), indent=1, default=str)
pr("FINAL ok" if allok else "FINAL FAIL: a C2 division failed its exact check")
