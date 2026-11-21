"""Amber-cell sweep: exact solids in Q(sqrt5), T_h axes on the cube axes (vertex sets closed under cyclic permutation x sign changes).
build(name) -> dict(V, faces=[(vertex index list, kind)], planes=[(n, c)] outward n.x = c, name).
C1 (DICTO's Fullerene Star) and C2 (working name) are taken unchanged from the scutoid stand-in study (branch D, resin.py / c2.py).
Convex solids: exact hull (float hull for the candidate faces, then every face plane checked exactly: face vertices on it, all others
strictly inside).  Edge 1 where the edge is in Q(sqrt5); the rhombic triacontahedron is the polar of the icosidodecahedron (inradius 1)."""
import itertools, math, os, sys
from fractions import Fraction as Fr
import numpy as np
sys.path.insert(0, os.environ.get("RESIN_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../2026-11-21-scutoid-stand-in/tree/branch-D-resin/scripts")))
from resin import Q, PHI, build_C1, dot, cross, vsub, vadd, vsc, det3, polytope
from c2 import build_C2

def key(v): return tuple(x.key() for x in v)
def orbit(base, scale=Q(1)):
    out, seen = [], set()
    for b in base:
        b = [x if isinstance(x, Q) else Q(x) for x in b]
        for sg in itertools.product((1, -1), repeat=3):
            t = [b[i]*sg[i]*scale for i in range(3)]
            for c in ([t[0], t[1], t[2]], [t[2], t[0], t[1]], [t[1], t[2], t[0]]):
                if key(c) not in seen: seen.add(key(c)); out.append(c)
    return out

def hull(P, kindname):
    from scipy.spatial import ConvexHull
    F = np.array([[float(x) for x in p] for p in P]); h = ConvexHull(F)
    cand = {}
    for eq in h.equations:
        n = eq[:3]; idx = tuple(sorted(i for i in range(len(P)) if abs(F[i] @ n + eq[3]) < 1e-9))
        cand[idx] = 1
    faces, planes = [], []
    for idx in cand:
        a, b, c = [P[i] for i in idx[:3]]
        n = cross(vsub(b, a), vsub(c, a)); k = 3
        while all(x.sign() == 0 for x in n): n = cross(vsub(b, a), vsub(P[idx[k]], a)); k += 1
        d = dot(n, a)
        if d.sign() < 0: n = vsc(-1, n); d = -d
        assert d.sign() > 0, "origin strictly inside"
        on = [i for i in range(len(P)) if (dot(n, P[i]) - d).sign() == 0]
        assert tuple(on) == idx, "face vertex set exact"
        assert all((dot(n, P[i]) - d).sign() < 0 for i in range(len(P)) if i not in idx), "convexity exact"
        nf = np.array([float(x) for x in n]); C = F[list(idx)].mean(0); u = F[idx[0]] - C; u /= np.linalg.norm(u); w = np.cross(nf/np.linalg.norm(nf), u)
        cyc = sorted(idx, key=lambda i: math.atan2((F[i]-C) @ w, (F[i]-C) @ u))
        faces.append((cyc, kindname.get(len(cyc), f"{len(cyc)}-gon"))); planes.append((n, d))
    return dict(V=P, faces=faces, planes=planes)

KIND = {3: "tri", 4: "quad", 5: "pent", 6: "hex", 10: "dec"}
H = Fr(1, 2)
def build(name):
    if name == "C1":
        C = build_C1(); return dict(V=C["V"], faces=C["faces"], planes=C["planes"], name=name)
    if name == "C2":
        C = build_C2(); return dict(V=C["V"], faces=C["faces"], planes=C["planes"], name=name)
    if name == "dodeca_icosa_compound":
        return compound()
    if name == "dodecahedron":     # edge 2/phi scaled by phi/2 -> 1
        P = orbit([(1, 1, 1), (0, PHI - 1, PHI)], PHI*H)
    elif name == "icosahedron":    # edge 2 scaled by 1/2
        P = orbit([(0, 1, PHI)], Q(H))
    elif name == "icosidodecahedron":
        P = orbit([(0, 0, PHI), (H, PHI*H, PHI*PHI*H)])
    elif name == "truncated_icosahedron":
        P = orbit([(Q(0), Q(1), 3*PHI), (Q(1), 2+PHI, 2*PHI), (PHI, Q(2), 2*PHI+1)], Q(H))
    elif name == "truncated_dodecahedron":
        P = orbit([(Q(0), PHI - 1, 2+PHI), (PHI - 1, PHI, 2*PHI), (PHI, Q(2), PHI+1)], PHI*H)
    elif name == "rhombic_triacontahedron":   # polar of the icosidodecahedron vertex set (unit inradius after scaling below)
        N = orbit([(0, 0, PHI), (H, PHI*H, PHI*PHI*H)])
        Pt = polytope([(n, dot(n, n), "f") for n in N])
        P = Pt["verts"]
    else:
        raise SystemExit(f"unknown solid {name}")
    S = hull(P, KIND); S["name"] = name
    # edge length check (exact) for the edge-1 solids
    if name != "rhombic_triacontahedron":
        for f, k in S["faces"]:
            for i in range(len(f)):
                a, b = S["V"][f[i]], S["V"][f[(i+1) % len(f)]]
                assert (dot(vsub(a, b), vsub(a, b)) - 1).sign() == 0, "edge 1"
    return S

def compound():
    """DICTO's mixed amber core (working name): the dual compound of a dodecahedron D = (+-1,+-1,+-1), cyc(0,+-1/phi,+-phi) and an
    icosahedron I = cyc(0,+-phi,+-1), edges crossing at their common midpoints (radius phi on the 2-fold axes; checked exactly).
    Core = the union D u I (non-convex, star-shaped).  Its surface: 120 triangles, (v, mid(v,a), mid(v,b)) for every vertex v of either
    solid and every face of that solid at v (a, b = v's neighbours in that face): 60 from the icosahedron's faces (the 12 five-sided
    tips), 60 from the dodecahedron's faces (the 20 three-sided tips).  Checked exactly: every edge midpoint of D is an edge midpoint
    of I; each triangle lies in its solid's face plane and outside the other solid; closed oriented surface; vol = vol D + vol I - vol(D n I)."""
    D = hull(orbit([(1, 1, 1), (0, PHI - 1, PHI)]), KIND); I = hull(orbit([(0, PHI, 1)]), KIND)
    def mids(S):
        out = {}
        for f, k in S["faces"]:
            for i in range(len(f)):
                a, b = f[i], f[(i+1) % len(f)]; out[frozenset((a, b))] = vsc(Fr(1, 2), vadd(S["V"][a], S["V"][b]))
        return out
    mD, mI = mids(D), mids(I)
    assert {key(m) for m in mD.values()} == {key(m) for m in mI.values()} and len(mD) == 30, "edges cross at common midpoints"
    V, idx = [], {}
    def vid(p):
        if key(p) not in idx: idx[key(p)] = len(V); V.append(p)
        return idx[key(p)]
    for S in (I, D):
        for p in S["V"]: vid(p)
    for m in mD.values(): vid(m)
    faces, planes = [], []
    for S, other, kn in ((I, D, "I-tri"), (D, I, "D-tri")):
        mm = mids(S)
        for (f, k), (n, c) in zip(S["faces"], S["planes"]):
            for i in range(len(f)):
                v, a, b = f[i], f[i-1], f[(i+1) % len(f)]
                tri = [vid(S["V"][v]), vid(mm[frozenset((v, b))]), vid(mm[frozenset((v, a))])]
                cen = [sum((V[t][j] for t in tri), Q(0))*Fr(1, 3) for j in range(3)]
                assert any((dot(n2, cen) - c2).sign() > 0 for n2, c2 in other["planes"]), "triangle outside the other solid"
                assert all((dot(n, V[t]) - c).sign() == 0 for t in tri)
                P = [V[t] for t in tri]
                if dot(cross(vsub(P[1], P[0]), vsub(P[2], P[0])), n).sign() < 0: tri = tri[::-1]
                faces.append((tri, kn)); planes.append((n, c))
    E = {}
    for t, k in faces:
        for i in range(3): E.setdefault((t[i], t[(i+1) % 3]), 0); E[(t[i], t[(i+1) % 3])] += 1
    assert all(E[e] == 1 and (e[1], e[0]) in E for e in E), "closed oriented surface"
    def vol(S):
        tot = Q(0)
        for f, k in S["faces"]:
            P = [S["V"][i] for i in f]
            for q in range(1, len(P) - 1):
                d = det3(P[0], P[q], P[q+1]); tot = tot + (d if d.sign() > 0 else -d)
        return tot/6
    U = vol(dict(V=V, faces=faces))
    X = polytope([(n, c, "x") for n, c in D["planes"] + I["planes"]])
    assert (U - (vol(D) + vol(I) - X["vol"])).sign() == 0, "union volume exact"
    return dict(V=V, faces=faces, planes=planes, name="dodeca_icosa_compound")

COUNTS = {"dodeca_icosa_compound": (62, 120), "dodecahedron": (20, 12), "icosahedron": (12, 20), "icosidodecahedron": (30, 32), "truncated_icosahedron": (60, 32),
          "truncated_dodecahedron": (60, 32), "rhombic_triacontahedron": (32, 30), "C1": (72, 80), "C2": (80, 72)}
if __name__ == "__main__":
    for nm in COUNTS:
        S = build(nm)
        from collections import Counter
        assert (len(S["V"]), len(S["faces"])) == COUNTS[nm], (nm, len(S["V"]), len(S["faces"]))
        print(nm, len(S["V"]), "vertices", dict(Counter(k for f, k in S["faces"])), "faces: ok")
