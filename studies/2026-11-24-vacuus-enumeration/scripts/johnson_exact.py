#!/usr/bin/env python3
"""Johnson solids, exact (24 Nov 2026).

Each Johnson solid is BUILT exactly in a number field from exact pieces: caps (pyramid,
cupola, rotunda), prisms and antiprisms stacked on an axis; pyramid and cupola augmentations
of exact uniform solids; vertex removals (diminishings); half-turn gyrations of caps.
Every candidate is matched to the app registry's float model by its pairwise-distance
invariant (edge = 1), which names it; then vacuus_exact.analyse checks it exactly (faces
planar, regular and supporting, Euler, all edges equal) and computes its Vacuus about
(a) the corner centroid and (b) the volume centroid, both exact.
J84-J90 are not built here (coordinates are roots of higher-degree systems).
"""
import sys, json, itertools, time
import numpy as np
import sympy as sp
import mpmath as mp
from scipy.spatial import ConvexHull
from vacuus_exact import Fld, analyse, vkey, dot, cross, vsub, vadd, scal, fl, uniform_solids, build_set

reg = json.load(open("data/johnson-float-source.json"))
alias = {"D6": "J12_TRIANGULAR_BIPYRAMID", "D10": "J13_PENTAGONAL_BIPYRAMID", "D16": "J17_GYROELONGATED_SQUARE_BIPYRAMID",
         "D14": "J51_TRIAUGMENTED_TRIANGULAR_PRISM", "D12": "J84_SNUB_DISPHENOID"}

def invariant(P):
    P = np.asarray(P, float)
    d = np.sqrt(((P[:, None] - P[None]) ** 2).sum(-1))[np.triu_indices(len(P), 1)]
    return len(P), np.sort(d / d.min())

REG = {}
for k, v in reg.items():
    if k in ("D4", "D8", "D20"): continue
    REG[alias.get(k, k)] = invariant(v["vertices"])

BUILT = {}   # name -> (F, V, recipe)

def offer(F, V, recipe):
    Pf = np.array([fl(F, v) for v in V])
    n, d = invariant(Pf)
    for name, (n2, d2) in REG.items():
        if n == n2 and np.abs(d - d2).max() < 1e-6:
            if name not in BUILT:
                BUILT[name] = (F, V, recipe)
                print("built", name, "<-", recipe, flush=True)
            return name
    return None

def faces_float(P):
    h = ConvexHull(P); g = {}
    for s, e in zip(h.simplices, h.equations):
        g.setdefault(tuple(np.round(e, 6)), set()).update(int(i) for i in s)
    out = []
    for idx in g.values():
        idx = sorted(idx); cf = P[idx].mean(0)
        nf = np.cross(P[idx[1]] - P[idx[0]], P[idx[2]] - P[idx[0]]); nf /= np.linalg.norm(nf)
        u = P[idx[0]] - cf; u /= np.linalg.norm(u); w = np.cross(nf, u)
        out.append([i for _, i in sorted(zip([np.arctan2((P[i]-cf) @ w, (P[i]-cf) @ u) for i in idx], idx))])
    return out

# ---------------- axial family ----------------
def axial(m):
    g = sp.cos(sp.pi / (2*m)); Rm = 1 / (2*sp.sin(sp.pi/m))
    hs = {}
    if m in (3, 4, 5): hs["pyr"] = sp.sqrt(1 - Rm**2)
    if m in (6, 8, 10):
        Rn = 1 / (2*sp.sin(2*sp.pi/m))
        hs["cup"] = sp.sqrt(1 - Rn**2 - Rm**2 + 2*Rn*Rm*sp.cos(sp.pi/m))
    hs["anti"] = sp.sqrt(1 - 4*Rm**2*sp.sin(sp.pi/(2*m))**2)
    if m == 10:
        phi = (1 + sp.sqrt(5)) / 2; R5 = 1 / (2*sp.sin(sp.pi/5))
        r1 = (2*phi**2 - 1) / (2*phi*sp.cos(sp.pi/10))
        hs["rotH"] = sp.sqrt(phi**2 - R5**2); hs["rotz1"] = sp.sqrt(phi**2 - r1**2)
    t0 = time.time()
    F = Fld(g, *hs.values())
    try: deg = len(F.K.mod.to_list()) - 1
    except Exception: deg = "?"
    print(f"field m={m}: degree {deg} ({time.time()-t0:.1f}s)", flush=True)
    G = F.c(g); T = [F.one, G]
    for k in range(2, 4*m + 1): T.append(2*G*T[-1] - T[-2])
    cu = lambda k: T[(2*k) % (4*m)]
    su = lambda k: T[(m - 2*k) % (4*m)]
    H = {k: F.c(v) for k, v in hs.items()}
    Rm_ = F.one / (2*su(1)); z = F.zero
    def ring(N, R, zz, off):
        st = 2*m // N
        return [(R*cu(j*st + off), R*su(j*st + off), zz) for j in range(N)]
    def chk(name, val):
        assert H[name]*H[name] == val, "height " + name
    caps = {}
    if m in (3, 4, 5):
        chk("pyr", F.one - Rm_*Rm_)
        caps["pyr"] = ring(m, Rm_, z, 0) + [(z, z, H["pyr"])]
    if m in (6, 8, 10):
        Rn = F.one / (2*su(2))
        chk("cup", F.one - Rn*Rn - Rm_*Rm_ + 2*Rn*Rm_*cu(1))
        caps["cup"] = ring(m, Rm_, z, 0) + ring(m // 2, Rn, H["cup"], 1)
    chk("anti", F.one - 2*Rm_*Rm_*(F.one - cu(1)))
    if m == 10:
        phi = 2*cu(2); R5 = F.one / (2*su(2)); r1 = (2*phi*phi - F.one) / (2*phi*cu(1))
        chk("rotH", phi*phi - R5*R5); chk("rotz1", phi*phi - r1*r1)
        for toff in (1, 3):
            for moff in (1, 3):
                caps[f"rot{moff}{toff}"] = ring(10, Rm_, z, 0) + ring(5, r1, H["rotz1"], moff) + ring(5, R5, H["rotH"], toff)
    def rotk(v, k): c, s = cu(k), su(k); return (v[0]*c - v[1]*s, v[0]*s + v[1]*c, v[2])
    def place(piece, k, dz, mirror=False):
        return [rotk((x, y, (-zz if mirror else zz) + dz), k) for x, y, zz in piece]
    mids = {"none": ([], z, 0), "prism": (ring(m, Rm_, z, 0) + ring(m, Rm_, F.one, 0), F.one, 0),
            "anti": (ring(m, Rm_, z, 0) + ring(m, Rm_, H["anti"], 1), H["anti"], 1)}
    for tn, top in caps.items():
        for mn, (mv, hm, toff) in mids.items():
            for bn in [None] + list(caps):
                for b in ([0] if bn is None else [0, 2]):
                    V = place(top, toff, hm) + mv + ([] if bn is None else place(caps[bn], b, z, True))
                    V = build_set(F, V)
                    try:
                        offer(F, V, f"axial m={m}: {tn} / {mn} / {bn} b={b}")
                    except Exception as e:
                        pass

def prisms_augmented():
    for m in (3, 5, 6):
        g = sp.cos(sp.pi/(2*m)); F = Fld(g, sp.sqrt(2))
        G = F.c(g); T = [F.one, G]
        for k in range(2, 4*m + 1): T.append(2*G*T[-1] - T[-2])
        cu = lambda k: T[(2*k) % (4*m)]; su = lambda k: T[(m - 2*k) % (4*m)]
        Rm = F.one / (2*su(1)); half = F.one / 2; s2 = F.c(sp.sqrt(2))
        base = [(Rm*cu(2*j), Rm*su(2*j), s*half) for j in range(m) for s in (1, -1)]
        a = Rm*cu(1)
        for k in (1, 2, 3):
            for S in itertools.combinations(range(m), k):
                V = list(base) + [((a + s2/2)*cu(2*j+1), (a + s2/2)*su(2*j+1), F.zero) for j in S]
                offer(F, build_set(F, V), f"{m}-prism + square pyramids on lateral faces {S}")

def edge(F, V, expr):
    """The exact edge length (given), checked against the shortest corner distance."""
    e = F.c(expr)
    d2 = [dot(vsub(V[0], v), vsub(V[0], v)) for v in V[1:]]
    m = min(d2, key=lambda x: float(F.val(x)))
    assert e * e == m, "edge length"
    return e

def outward(F, V, p, N):
    cen = [sum(x) / len(V) for x in zip(*[fl(F, v) for v in V])]
    A = fl(F, V[p[0]])
    return N if np.dot(fl(F, N), np.array(A) - cen) > 0 else tuple(-x for x in N)

def apex(F, V, p, s, e):
    A, B, C = V[p[0]], V[p[1]], V[p[2]]
    N = outward(F, V, p, cross(vsub(B, A), vsub(C, B)))
    k = len(p); c = tuple(sum((V[i][t] for i in p), F.zero) / k for t in range(3))
    return vadd(c, scal(s / e, N))

def cupola_top(F, V, p, sh, r, t, e):
    A, B, C = V[p[0]], V[p[1]], V[p[2]]
    N = outward(F, V, p, cross(vsub(B, A), vsub(C, B)))
    k = len(p); c = tuple(sum((V[i][q] for i in p), F.zero) / k for q in range(3))
    out = []
    for j in range(k // 2):
        a, b = V[p[(2*j + t) % k]], V[p[(2*j + 1 + t) % k]]
        mj = tuple((x + y) / 2 for x, y in zip(a, b))
        out.append(vadd(vadd(c, scal(sh / e, N)), scal(r, vsub(mj, c))))
    return out

def platonic_archimedean_based():
    S = uniform_solids()
    # dodecahedron + pentagonal pyramids (J58-J61)
    F, gen, _ = S["dodecahedron"]; V = build_set(F, gen); P = np.array([fl(F, v) for v in V]); fcs = faces_float(P)
    s5 = F.c((5 - sp.sqrt(5)) / 5); e = edge(F, V, sp.sqrt(5) - 1)
    for k in (1, 2, 3):
        for Sx in itertools.combinations(range(len(fcs)), k):
            if Sx[0] != 0: continue
            offer(F, build_set(F, list(V) + [apex(F, V, fcs[i], s5, e) for i in Sx]), f"dodecahedron + pentagonal pyramids {Sx}")
    # icosahedron diminished (J62, J63) and J64, in Q(sqrt5, sqrt2)
    F2 = Fld(sp.sqrt(5), sp.sqrt(2)); phi = (1 + sp.sqrt(5)) / 2
    from vacuus_exact import even_perms, signs
    Vi = build_set(F2, [p for t in even_perms((0, 1, phi)) for p in signs(t)])
    s3 = F2.c(2*sp.sqrt(2)/3); e2 = edge(F2, Vi, sp.Integer(2))
    for k in (2, 3):
        for R in itertools.combinations(range(12), k):
            if R[0] != 0: continue
            W = [v for i, v in enumerate(Vi) if i not in R]
            nm = offer(F2, W, f"icosahedron minus corners {R}")
            if nm and nm.startswith("J63") and "J64_AUGMENTED_TRIDIMINISHED_ICOSAHEDRON" not in BUILT:
                Pw = np.array([fl(F2, v) for v in W])
                for p in faces_float(Pw):
                    if len(p) == 3:
                        offer(F2, build_set(F2, W + [apex(F2, W, p, s3, e2)]), f"J63 + tetrahedron on face {p}")
    # cupola augmentations J65-J71
    specs = [("truncated tetrahedron", 6, "2*sqrt(2)/3", "2/3", "2*sqrt(2)"), ("truncated cube", 8, "1", "2-sqrt(2)", "2*sqrt(2)-2"),
             ("truncated dodecahedron", 10, "2*sqrt(5)/5", "(5-sqrt(5))/5", "sqrt(5)-1")]
    for nm0, big, sh, r, ee in specs:
        F, gen, _ = S[nm0]; V = build_set(F, gen); P = np.array([fl(F, v) for v in V])
        fcs = [p for p in faces_float(P) if len(p) == big]
        shv = F.c(sp.sympify(sh)); rv = F.c(sp.sympify(r)); e = edge(F, V, sp.sympify(ee))
        for k in (1, 2, 3):
            for Sx in itertools.combinations(range(len(fcs)), k):
                if Sx[0] != 0: continue
                for ts in itertools.product((0, 1), repeat=k):
                    W = list(V)
                    for i, t in zip(Sx, ts): W += cupola_top(F, V, fcs[i], shv, rv, t, e)
                    offer(F, build_set(F, W), f"{nm0} + cupolas on {Sx} t={ts}")
    # rhombicosidodecahedron: gyrate (half-turn of the pentagon) / diminish caps (J72-J83)
    F, gen, _ = S["rhombicosidodecahedron"]; V = build_set(F, gen); P = np.array([fl(F, v) for v in V])
    fcs = faces_float(P); pents = [p for p in fcs if len(p) == 5]
    nb = {i: set() for i in range(len(V))}
    for p in fcs:
        for j in range(len(p)): a, b = p[j], p[(j+1) % len(p)]; nb[a].add(b); nb[b].add(a)
    caps = []
    for p in pents:
        ring = set().union(*[nb[i] for i in p]) - set(p)
        caps.append((p, set(p) | ring))
    for k in (1, 2, 3):
        for Sx in itertools.combinations(range(12), k):
            if Sx[0] != 0: continue
            if any(caps[a][1] & caps[b][1] for a, b in itertools.combinations(Sx, 2)): continue
            for st in itertools.product("gd", repeat=k):
                W = {i: V[i] for i in range(len(V))}
                for c, s in zip(Sx, st):
                    p = caps[c][0]
                    ax = tuple(sum((V[i][q] for i in p), F.zero) for q in range(3)); aa = dot(ax, ax)
                    for i in p:
                        if s == "d": W.pop(i)
                        else: W[i] = vsub(scal(2*dot(V[i], ax)/aa, ax), V[i])
                offer(F, list(W.values()), f"rhombicosidodecahedron caps {Sx} {''.join(st)}")

def gyrobifastigium():
    F = Fld(sp.sqrt(3)); h = F.c(sp.sqrt(3)/2); a = F.one/2; z = F.zero
    V = [(sx*a, sy*a, z) for sx in (1, -1) for sy in (1, -1)] + [(s*a, z, h) for s in (1, -1)] + [(z, s*a, -h) for s in (1, -1)]
    offer(F, V, "gyrobifastigium: square with two ridges")

def recognise(name, gens, basis):
    """Exact coordinates from the registry floats: frame from symmetry, PSLQ in the given basis."""
    P = frame(np.array(reg_lookup(name), float))
    F = Fld(*gens); bv = [F.c(b) for b in basis]; bf = [float(sp.N(b, 30)) for b in basis]
    V = []
    for v in P:
        cv = []
        for x in v:
            if abs(x) < 1e-12: cv.append(F.zero); continue
            rel = mp.pslq([mp.mpf(x)] + [mp.mpf(b) for b in bf], tol=1e-10, maxcoeff=2000, maxsteps=10**5)
            if rel is None or rel[0] == 0: return None
            cv.append(sum((sp.Rational(-c, rel[0]) * bb for c, bb in zip(rel[1:], basis)), sp.Integer(0)))
        V.append(tuple(c if not isinstance(c, sp.Basic) else F.c(c) for c in cv))
    return offer(F, build_set(F, V), f"{name}: recognised in basis {basis}")

def frame(P):
    """Centre at the corner centroid, edge 1, axes from the symmetry: three mirror normals (D2h),
    or the 3-fold axis plus a mirror normal (C3v)."""
    V = P - P.mean(0); n = len(V)
    d = np.sqrt(((V[:, None] - V[None]) ** 2).sum(-1)); V = V / d[d > 1e-9].min()
    def find(p):
        e = np.linalg.norm(V - p, axis=1); return e.min() < 1e-6
    mir = []
    for i in range(n):
        for j in range(i+1, n):
            if abs(np.linalg.norm(V[i]) - np.linalg.norm(V[j])) > 1e-6: continue
            m = V[i] - V[j]; m /= np.linalg.norm(m)
            if all(find(v - 2*(v @ m)*m) for v in V) and not any(abs(abs(m @ q) - 1) < 1e-6 for q in mir): mir.append(m)
    if len(mir) == 3:
        E = np.array(mir)
    else:
        ax = np.cross(mir[0], mir[1]); ax /= np.linalg.norm(ax)
        e1 = mir[0]; E = np.array([e1, np.cross(ax, e1), ax])
    return V @ E.T

def reg_lookup(name):
    for k, v in reg.items():
        if alias.get(k, k) == name: return v["vertices"]

def centroids(F, V):
    n = len(V); Oc = tuple(sum((v[t] for v in V), F.zero) / n for t in range(3))
    P = np.array([fl(F, v) for v in V]); vol = F.zero; acc = (F.zero, F.zero, F.zero)
    for p in faces_float(P):
        for j in range(1, len(p) - 1):
            a, b, c = vsub(V[p[0]], Oc), vsub(V[p[j]], Oc), vsub(V[p[j+1]], Oc)
            d = dot(a, cross(b, c))
            if F.sign(d) < 0: d = -d
            vol = vol + d
            acc = vadd(acc, scal(d, tuple((x + y + z) / 4 for x, y, z in zip(a, b, c))))
    Ov = vadd(Oc, tuple(x / vol for x in acc))
    return Oc, Ov

def strip(r):
    return {k: v for k, v in r.items() if not k.startswith("_")}

if __name__ == "__main__":
    t0 = time.time()
    for m in (3, 4, 5, 6, 8, 10):
        axial(m)
    prisms_augmented(); gyrobifastigium(); platonic_archimedean_based()
    print("PROGRESS 0.5 built", len(BUILT), "in", round(time.time() - t0), "s", flush=True)
    try:
        recognise("J91_BILUNABIROTUNDA", [sp.sqrt(5)], [sp.Integer(1), sp.sqrt(5)])
    except Exception as e: print("J91 recognition failed:", e, flush=True)
    try:
        recognise("J92_TRIANGULAR_HEBESPHENOROTUNDA", [sp.sqrt(3), sp.sqrt(5)], [sp.Integer(1), sp.sqrt(3), sp.sqrt(5), sp.sqrt(15)])
    except Exception as e: print("J92 recognition failed:", e, flush=True)
    missing = sorted(set(REG) - set(BUILT), key=lambda s: int(s.split("_")[0][1:]))
    print("missing:", missing, flush=True)
    if "--build-only" in sys.argv: sys.exit(0)
    out = []
    names = sorted(BUILT, key=lambda s: int(s.split("_")[0][1:]))
    for i, nm in enumerate(names):
        F, V, recipe = BUILT[nm]
        Oc, Ov = centroids(F, V)
        row = {"name": nm, "J": int(nm.split("_")[0][1:]), "recipe": recipe, "same_centre": all(not (a - b) for a, b in zip(Oc, Ov))}
        for lab, O in (("corner", Oc), ("volume", Ov)):
            W = [vsub(v, O) for v in V]
            r, _ = analyse(nm, F, W, True, None, check_centre=False)
            row[lab] = strip(r)
        a, b = row["corner"], row["volume"]
        row["differ"] = (a["kind"], a["plates"], a["plate_classes"]) != (b["kind"], b["plates"], b["plate_classes"])
        out.append(row)
        print(f"PROGRESS {0.5 + 0.5*(i+1)/len(names):.3f} {nm} corner {a['kind']} {a['plates']} | volume {b['kind']} {b['plates']} | differ {row['differ']}", flush=True)
        json.dump(out, open("data/johnson-exact.json", "w"), indent=1, default=str)
    print("missing:", missing)
    print("FINAL ok", len(out), "exact;", len(missing), "not built")
