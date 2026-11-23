#!/usr/bin/env python3
"""Vacuus enumeration, exact (24 Nov 2026).

Definition used (Walls of Silence #110, Section 2, widening #87 and #105): for a convex
polytope X with centre O, each edge (ridge, in 3D) spans with O a plane through O, its
plate; the Vacuus is the set of plates, each with the edges on it. A plate is a full sheet
if with each edge it carries the opposite edge -e, a shared sheet if it carries >= 2 edges
but is not full, a single fin if it carries one. Kind: heart (all full), non-heart (all
single), inherited heart (otherwise).

Also reported (the reading on DICTO's V SF A page, "one plate for each pair of parallel
faces (or each face)"): the face-parallel central planes ("face plates").

All arithmetic is exact in a number field (sympy AlgebraicField); signs of nonzero elements
are read from an 80-digit evaluation of the exact element (a sign is only taken when the
element is exactly nonzero). Floats choose orderings and the convex-hull combinatorics,
which are then checked exactly (coplanarity, strict support, Euler).
"""
import sys, json, itertools, time
import sympy as sp
import mpmath as mp
from sympy import QQ
import numpy as np
from scipy.spatial import ConvexHull, cKDTree

mp.mp.dps = 80

class Fld:
    def __init__(self, *gens):
        self.K = QQ.algebraic_field(*gens) if gens else QQ.algebraic_field(sp.Integer(1))
        self.alpha = mp.mpf(str(sp.N(self.K.ext.as_expr(), 90)))
        self.zero = self.K.zero; self.one = self.K.one
        self._vc = {}
    def c(self, x):
        if isinstance(x, int): return self.K.convert(x)
        return self.K.from_sympy(sp.sympify(x))
    def key(self, a): return tuple(a.to_list())
    def val(self, a):
        k = self.key(a)
        v = self._vc.get(k)
        if v is None:
            v = mp.mpf(0)
            for co in k:
                v = v * self.alpha + mp.mpf(int(co.numerator)) / int(co.denominator)
            self._vc[k] = v
        return v
    def sign(self, a):
        if not a: return 0
        v = self.val(a)
        assert abs(v) > mp.mpf(10) ** -60, "sign not certified"
        return 1 if v > 0 else -1

def vadd(a, b): return tuple(x + y for x, y in zip(a, b))
def vsub(a, b): return tuple(x - y for x, y in zip(a, b))
def vneg(a): return tuple(-x for x in a)
def dot(a, b): return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]
def cross(a, b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def scal(s, a): return tuple(s * x for x in a)

def canon(F, n):
    for x in n:
        if x: return tuple(y / x for y in n)
    raise ValueError("zero normal")

def vkey(F, v): return tuple(F.key(x) for x in v)

def fl(F, v): return [float(F.val(x)) for x in v]

def analyse(name, F, V, uniform=True, extra=None, check_centre=True):
    t0 = time.time()
    n = len(V)
    keys = {vkey(F, v): i for i, v in enumerate(V)}
    assert len(keys) == n, "repeated vertex"
    # centre: corner centroid, must be the origin here
    cen = tuple(sum((v[i] for v in V), F.zero) for i in range(3))
    centred = all(not x for x in cen)
    assert centred or not check_centre, name + ": centroid not at origin"
    P = np.array([fl(F, v) for v in V])
    hull = ConvexHull(P)
    # group facets by plane
    groups = {}
    for simp, eq in zip(hull.simplices, hull.equations):
        k = tuple(np.round(eq, 7))
        groups.setdefault(k, set()).update(int(i) for i in simp)
    faces = []
    for idx in groups.values():
        idx = sorted(idx)
        a, b = V[idx[0]], V[idx[1]]
        Nn = None
        for c in idx[2:]:
            Nn = cross(vsub(b, a), vsub(V[c], a))
            if any(Nn): break
        d = dot(Nn, a)
        # orient outward: d > 0 (origin inside)
        if F.sign(d) < 0: Nn = vneg(Nn); d = -d
        assert F.sign(d) > 0
        on = [i for i in range(n) if not (dot(Nn, V[i]) - d)]
        assert sorted(on) == idx, name + ": face set mismatch"
        assert all(F.sign(dot(Nn, V[i]) - d) < 0 for i in range(n) if i not in on), "not supporting"
        # order polygon by angle (float) around centre of face
        cf = P[idx].mean(0); nf = np.array(fl(F, Nn)); nf /= np.linalg.norm(nf)
        u = P[idx[0]] - cf; u /= np.linalg.norm(u); w = np.cross(nf, u)
        ang = [np.arctan2((P[i]-cf) @ w, (P[i]-cf) @ u) for i in idx]
        poly = [i for _, i in sorted(zip(ang, idx))]
        faces.append({"verts": poly, "N": Nn, "d": d})
    edges = set()
    for f in faces:
        p = f["verts"]
        for j in range(len(p)):
            a, b = p[j], p[(j+1) % len(p)]
            edges.add((min(a, b), max(a, b)))
    edges = sorted(edges)
    nE, nF = len(edges), len(faces)
    assert n - nE + nF == 2, "Euler"
    if uniform:
        for f in faces:
            p = f["verts"]; k = len(p)
            cf = tuple(sum((V[i][t] for i in p), F.zero) / k for t in range(3))
            assert len({F.key(dot(vsub(V[i], cf), vsub(V[i], cf))) for i in p}) == 1, name + ": face not cyclic"
        L = {F.key(dot(vsub(V[a], V[b]), vsub(V[a], V[b]))) for a, b in edges}
        assert len(L) == 1, name + ": edges not all equal"
    ekeys = {(min(a, b), max(a, b)) for a, b in edges}
    neg = {i: keys.get(vkey(F, vneg(V[i]))) for i in range(n)}
    cs = all(neg[i] is not None for i in range(n))

    def reflect_ok(m):
        mm = dot(m, m)
        for v in V:
            r = vsub(v, scal(2 * dot(m, v) / mm, m))
            if vkey(F, r) not in keys: return False
        return True

    # mirrors of the full symmetry group
    cand = {}
    nrm = [F.key(dot(v, v)) for v in V]
    for i in range(n):
        for j in range(i+1, n):
            if nrm[i] == nrm[j]:
                mf = P[i] - P[j]; mf = mf / np.linalg.norm(mf)
                R_ = P - 2 * np.outer(P @ mf, mf)
                if cKDTree(P).query(R_)[0].max() > 1e-6:
                    continue
                m = canon(F, vsub(V[i], V[j]))
                cand.setdefault(vkey(F, m), m)
    mirrors = {k: m for k, m in cand.items() if reflect_ok(m)}

    def section(m):
        s = [F.sign(dot(m, v)) for v in V]
        on = [i for i in range(n) if s[i] == 0]
        pts = [V[i] for i in on]
        cr = 0
        for a, b in edges:
            if s[a] * s[b] < 0:
                cr += 1
                da, db = dot(m, V[a]), dot(m, V[b])
                pts.append(tuple((db * x - da * y) / (db - da) for x, y in zip(V[a], V[b])))
        k = len(pts)
        Q = np.array([fl(F, p) for p in pts]); mf = np.array(fl(F, m)); mf /= np.linalg.norm(mf)
        u = Q[0] / (np.linalg.norm(Q[0]) or 1); w = np.cross(mf, u)
        order = [p for _, p in sorted(zip([np.arctan2(q @ w, q @ u) for q in Q], range(k)))]
        sides = {F.key(dot(vsub(pts[order[j]], pts[order[(j+1) % k]]), vsub(pts[order[j]], pts[order[(j+1) % k]]))) for j in range(k)}
        radii = {F.key(dot(p, p)) for p in pts}
        reg = len(sides) == 1 and len(radii) == 1
        desc = ("regular " if reg else "") + f"{k}-gon"
        if not reg: desc += f" ({len(sides)} side length{'s' if len(sides) > 1 else ''})"
        return {"sides": k, "corners_on": len(on), "crossings": cr, "shape": desc, "regular": reg}

    # edge plates
    plates = {}
    for a, b in edges:
        m = canon(F, cross(V[a], V[b]))
        plates.setdefault(vkey(F, m), {"m": m, "edges": []})["edges"].append((a, b))
    prows = []
    for k, p in plates.items():
        es = p["edges"]; eset = set(es)
        full = all(neg[a] is not None and neg[b] is not None and (min(neg[a], neg[b]), max(neg[a], neg[b])) in eset for a, b in es)
        kind = "full" if (full and len(es) >= 2) else ("shared" if len(es) >= 2 else "single")
        sec = section(p["m"])
        prows.append({"edges": len(es), "sheet": kind, "mirror": k in mirrors, **sec, "key": k})
    sheets = {r["sheet"] for r in prows}
    vkind = "heart" if sheets == {"full"} else ("non-heart" if sheets == {"single"} else "inherited heart")
    # face plates (central planes parallel to faces)
    fpl = {}
    for f in faces:
        m = canon(F, f["N"])
        fpl.setdefault(vkey(F, m), {"m": m, "faces": []})["faces"].append(len(f["verts"]))
    frows = []
    for k, p in fpl.items():
        sec = section(p["m"])
        frows.append({"faces": len(p["faces"]), "face_sides": sorted(p["faces"]), "mirror": k in mirrors, **sec, "key": k})

    def summ(rows, cnt):
        c = {}
        for r in rows:
            sig = (r[cnt], r.get("sheet", ""), r["shape"], r["mirror"]) if cnt == "edges" else (tuple(r["face_sides"]), r["shape"], r["mirror"])
            c[sig] = c.get(sig, 0) + 1
        return sorted(c.items(), key=lambda kv: (-kv[1], str(kv[0])))
    out = {"name": name, "V": n, "E": nE, "F": nF, "centrally_symmetric": cs, "mirrors": len(mirrors),
           "plates": len(prows), "kind": vkind,
           "plate_classes": [{"count": c, "edges_per_plate": s[0], "sheet": s[1], "slice": s[2], "mirror": s[3]} for s, c in summ(prows, "edges")],
           "plates_on_mirrors": sum(r["mirror"] for r in prows),
           "face_plates": len(frows),
           "face_plate_classes": [{"count": c, "faces": list(s[0]), "slice": s[1], "mirror": s[2]} for s, c in summ(frows, "faces")],
           "face_plates_on_mirrors": sum(r["mirror"] for r in frows),
           "_plate_keys": sorted(str(r["key"]) for r in prows),
           "_face_plate_keys": sorted(str(r["key"]) for r in frows),
           "_plate_float": sorted(tuple(round(x, 12) for x in fl(F, canon_unit(F, r["key"], plates))) for r in prows),
           "_face_plate_float": sorted(tuple(round(x, 12) for x in fl(F, fpl[r["key"]]["m"])) for r in frows),
           "secs": round(time.time() - t0, 1)}
    if extra:
        out.update(extra(F, V, edges, faces, mirrors, keys))
    return out, faces

def canon_unit(F, k, plates):
    m = plates[k]["m"]
    return m


def det3(M):
    return (M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1]) - M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])
            + M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0]))

def inv3(M):
    d = det3(M)
    C = [[M[(j+1)%3][(i+1)%3]*M[(j+2)%3][(i+2)%3] - M[(j+1)%3][(i+2)%3]*M[(j+2)%3][(i+1)%3] for j in range(3)] for i in range(3)]
    return tuple(tuple(C[i][j] / d for j in range(3)) for i in range(3))

def apply3(A, v): return tuple(A[i][0]*v[0] + A[i][1]*v[1] + A[i][2]*v[2] for i in range(3))

def rotations_permuting(F, P):
    """All rotations mapping the point set P (an icosahedron) onto itself, exact."""
    kset = {vkey(F, v) for v in P}
    u = P[0]; w = next(v for v in P[1:] if any(cross(u, v)) and F.key(dot(vsub(u, v), vsub(u, v))) == min_d(F, P))
    B = (u, w, cross(u, w)); Bm = tuple(tuple(B[j][i] for j in range(3)) for i in range(3)); Bi = inv3(Bm)
    out = []
    for u2 in P:
        for w2 in P:
            if F.key(dot(u2, w2)) != F.key(dot(u, w)): continue
            if not any(cross(u2, w2)): continue
            C = (u2, w2, cross(u2, w2)); Cm = tuple(tuple(C[j][i] for j in range(3)) for i in range(3))
            A = tuple(tuple(sum((Cm[i][k]*Bi[k][j] for k in range(3)), F.zero) for j in range(3)) for i in range(3))
            if all(vkey(F, apply3(A, v)) in kset for v in P): out.append(A)
    return out

def min_d(F, P):
    ds = [dot(vsub(P[0], v), vsub(P[0], v)) for v in P[1:]]
    m = ds[0]
    for d in ds[1:]:
        if F.sign(d - m) < 0: m = d
    return F.key(m)

def dual_vertices(F, faces):
    return [tuple(x / f["d"] for x in f["N"]) for f in faces]

# ---------- coordinate builders ----------
def perms_all(t): return set(itertools.permutations(t))
def even_perms(t): return {(t[0], t[1], t[2]), (t[1], t[2], t[0]), (t[2], t[0], t[1])}
def odd_perms(t): return {(t[1], t[0], t[2]), (t[0], t[2], t[1]), (t[2], t[1], t[0])}
def signs(t, cond=None):
    out = []
    for s in itertools.product((1, -1), repeat=3):
        if cond and not cond(s): continue
        if any(t[i] == 0 and s[i] == -1 for i in range(3)): continue
        out.append(tuple(si * ti for si, ti in zip(s, t)))
    return out

def build_set(F, gen):
    seen = {}
    for v in gen:
        v = tuple(F.c(x) if not hasattr(x, "to_list") else x for x in v)
        seen.setdefault(vkey(F, v), v)
    return list(seen.values())

def uniform_solids():
    s2, s5 = sp.sqrt(2), sp.sqrt(5)
    phi = (1 + s5) / 2
    Q = Fld()
    R2 = Fld(s2)
    R5 = Fld(s5)
    S = {}
    S["tetrahedron"] = (R2, [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)], "Td")
    S["cube"] = (R2, signs((1, 1, 1)), "Oh")
    S["octahedron"] = (R2, [p for t in perms_all((1, 0, 0)) for p in signs(t)], "Oh")
    S["dodecahedron"] = (R5, signs((1, 1, 1)) + [p for t in even_perms((0, 1/phi, phi)) for p in signs(t)], "Ih")
    S["icosahedron"] = (R5, [p for t in even_perms((0, 1, phi)) for p in signs(t)], "Ih")
    S["truncated tetrahedron"] = (R2, [p for t in perms_all((3, 1, 1)) for p in signs(t, lambda s: s.count(-1) % 2 == 0)], "Td")
    S["cuboctahedron"] = (R2, [p for t in perms_all((1, 1, 0)) for p in signs(t)], "Oh")
    S["truncated cube"] = (R2, [p for t in perms_all((s2 - 1, 1, 1)) for p in signs(t)], "Oh")
    S["truncated octahedron"] = (R2, [p for t in perms_all((0, 1, 2)) for p in signs(t)], "Oh")
    S["rhombicuboctahedron"] = (R2, [p for t in perms_all((1, 1, 1 + s2)) for p in signs(t)], "Oh")
    S["truncated cuboctahedron"] = (R2, [p for t in perms_all((1, 1 + s2, 1 + 2*s2)) for p in signs(t)], "Oh")
    S["icosidodecahedron"] = (R5, [p for t in even_perms((0, 0, phi)) for p in signs(t)] + [p for t in even_perms((sp.Rational(1, 2), phi/2, phi**2/2)) for p in signs(t)], "Ih")
    S["truncated icosahedron"] = (R5, [p for tt in [(0, 1, 3*phi), (1, 2 + phi, 2*phi), (phi, 2, phi**3)] for t in even_perms(tt) for p in signs(t)], "Ih")
    S["truncated dodecahedron"] = (R5, [p for tt in [(0, 1/phi, 2 + phi), (1/phi, phi, 2*phi), (phi, 2, phi + 1)] for t in even_perms(tt) for p in signs(t)], "Ih")
    S["rhombicosidodecahedron"] = (R5, [p for tt in [(1, 1, phi**3), (phi**2, phi, 2*phi), (2 + phi, 0, phi**2)] for t in even_perms(tt) for p in signs(t)], "Ih")
    S["truncated icosidodecahedron"] = (R5, [p for tt in [(1/phi, 1/phi, 3 + phi), (2/phi, phi, 1 + 2*phi), (1/phi, phi**2, -1 + 3*phi), (2*phi - 1, 2, 2 + phi), (phi, 3, 2*phi)] for t in even_perms(tt) for p in signs(t)], "Ih")
    # snub cube: tribonacci t
    x = sp.Symbol("x")
    T = Fld(sp.CRootOf(x**3 - x**2 - x - 1, 0))
    t = T.c(sp.CRootOf(x**3 - x**2 - x - 1, 0)); one = T.one
    base = (one, one / t, t)
    sc = []
    for p in even_perms(base):
        sc += signs(p, lambda s: s.count(1) % 2 == 0)
    for p in odd_perms(base):
        sc += signs(p, lambda s: s.count(1) % 2 == 1)
    S["snub cube"] = (T, sc, "O")
    # snub dodecahedron: xi real root of xi^3 - 2 xi = phi (phi = xi^3 - 2 xi); one vertex q = -(2a, 2, 2b)
    # (Wikipedia's list); the 60 vertices = the orbit of q under the icosahedral rotation group, built exactly
    # as all rotations permuting an icosahedron's 12 corners (both golden orientations tried; the one giving
    # 60 corners with 150 equal edges is kept).
    X = Fld(sp.CRootOf(x**6 - 4*x**4 - x**3 + 4*x**2 + 2*x - 1, 3))
    xi = X.c(sp.CRootOf(x**6 - 4*x**4 - x**3 + 4*x**2 + 2*x - 1, 3)); o = X.one; z0 = X.zero
    ph = xi**3 - 2*xi
    al = xi - o / xi; be = xi*ph + ph*ph + ph / xi
    q = (-2*al, -2*o, -2*be)
    cands = []
    for orient in ((z0, o, ph), (z0, ph, o)):
        ico = []
        for t in even_perms(orient):
            for sg in itertools.product((1, -1), repeat=3):
                v = tuple(si * ti for si, ti in zip(sg, t))
                if v not in ico and all(not (ti == z0 and si == -1) for si, ti in zip(sg, t)): ico.append(v)
        rots = rotations_permuting(X, ico)
        cands.append([apply3(A, q) for A in rots])
    S["snub dodecahedron"] = (X, cands, "I")
    return S

def prism_family(n):
    g = sp.cos(sp.pi / (2*n)); h = sp.sqrt(2*sp.cos(sp.pi/n) - 2*sp.cos(2*sp.pi/n))
    F = Fld(g, h)
    G = F.c(g); H = F.c(h)
    T = [F.one, G]
    for k in range(2, 4*n + 1): T.append(2*G*T[-1] - T[-2])
    def C(j):  # cos(j*pi/n)
        return T[(2*j) % (4*n)]
    def Sn(j):  # sin(j*pi/n) = cos(pi/2 - j pi/n) = cos((n - 2j) pi/(2n))
        k = (n - 2*j) % (4*n)
        return T[k]
    # T[k] for k up to 4n: cos(k*pi/(2n)) via Chebyshev, valid for all k
    e = 2 * Sn(1)  # edge of unit-circumradius n-gon
    pr = [(C(2*j), Sn(2*j), s * e / 2) for j in range(n) for s in (1, -1)]
    ap = [(C(2*j), Sn(2*j), H / 2) for j in range(n)] + [(C(2*j + 1), Sn(2*j + 1), -H / 2) for j in range(n)]
    return F, pr, ap

if __name__ == "__main__":
    import csv
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    results = []
    perm_extra = None
    if which in ("all", "uniform"):
        from perm_checks import perm_extra
        S = uniform_solids()
        catalan = {"tetrahedron": "tetrahedron (self-dual)", "cube": "octahedron", "octahedron": "cube",
                   "dodecahedron": "icosahedron", "icosahedron": "dodecahedron",
                   "truncated tetrahedron": "triakis tetrahedron", "cuboctahedron": "rhombic dodecahedron",
                   "truncated cube": "triakis octahedron", "truncated octahedron": "tetrakis hexahedron",
                   "rhombicuboctahedron": "deltoidal icositetrahedron", "truncated cuboctahedron": "disdyakis dodecahedron",
                   "snub cube": "pentagonal icositetrahedron", "icosidodecahedron": "rhombic triacontahedron",
                   "truncated icosahedron": "pentakis dodecahedron", "truncated dodecahedron": "triakis icosahedron",
                   "rhombicosidodecahedron": "deltoidal hexecontahedron", "truncated icosidodecahedron": "disdyakis triacontahedron",
                   "snub dodecahedron": "pentagonal hexecontahedron"}
        for nm, (F, gen, grp) in S.items():
            if nm == "snub dodecahedron":
                V = None
                for cand in gen:
                    Vc = build_set(F, cand)
                    try:
                        if len(Vc) == 60: analyse("probe", F, Vc, True); V = Vc; break
                    except AssertionError as e:
                        print("snub orientation rejected:", e, flush=True)
                assert V is not None
            else:
                V = build_set(F, gen)
            ex = perm_extra if nm in ("truncated octahedron", "truncated cuboctahedron", "truncated icosidodecahedron") else None
            r, faces = analyse(nm, F, V, True, ex)
            r["family"] = "Platonic" if nm in ("tetrahedron", "cube", "octahedron", "dodecahedron", "icosahedron") else "Archimedean"
            r["group"] = grp; r["frame"] = {"Td": "cube", "Oh": "cube", "O": "cube", "Ih": "ico", "I": "ico"}[grp]
            results.append(r); print(json.dumps({k: v for k, v in r.items() if not k.startswith("_")}), flush=True)
            if nm in ("tetrahedron", "cube", "octahedron", "dodecahedron", "icosahedron"):
                continue
            D = dual_vertices(F, faces)
            dn = catalan[nm]
            dex = None
            if nm in ("truncated octahedron", "truncated cuboctahedron", "truncated icosidodecahedron"):
                from perm_checks import dual_extra
                dex = dual_extra
            r2, _ = analyse(dn, F, D, False, dex)
            r2["family"] = "Catalan"; r2["group"] = grp; r2["frame"] = r["frame"]; r2["dual_of"] = nm
            results.append(r2); print(json.dumps({k: v for k, v in r2.items() if not k.startswith("_")}), flush=True)
    if which in ("all", "prisms"):
        for n in range(3, 13):
            F, pr, ap = prism_family(n)
            for nm, V0, fam in ((f"{n}-gonal prism", pr, "prism"), (f"{n}-gonal antiprism", ap, "antiprism")):
                V = build_set(F, V0)
                r, faces = analyse(nm, F, V, True)
                r["family"] = fam; r["n"] = n; r["frame"] = f"axis-{n}"
                results.append(r); print(json.dumps({k: v for k, v in r.items() if not k.startswith("_")}), flush=True)
                D = dual_vertices(F, faces)
                dn = f"{n}-gonal bipyramid" if fam == "prism" else f"{n}-gonal trapezohedron"
                r2, _ = analyse(dn, F, D, False)
                r2["family"] = "bipyramid" if fam == "prism" else "trapezohedron"; r2["n"] = n; r2["frame"] = f"axis-{n}"; r2["dual_of"] = nm
                results.append(r2); print(json.dumps({k: v for k, v in r2.items() if not k.startswith("_")}), flush=True)
    json.dump(results, open(f"data/exact-{which}.json", "w"), indent=1, default=str)
    print("FINAL ok", len(results), flush=True)
