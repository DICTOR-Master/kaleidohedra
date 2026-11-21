"""RENDER COPY (renders/scripts): ammann_cell.py unchanged except that it also stores the float geometry (X, pieces, Y) and writes to ../data/geom_*.json.
Amber-Ammann study (21 Nov 2026): DICTO's combined method in a golden-rhombohedron mould.
This file is the amber-cell sweep's amber.py (2026-11-21-amber-cell-sweep/scripts) with ONLY these changes:
 - mould = the golden rhombohedron spanned by e_a/3, e_b/3, e_c/3 (a,b,c = a triple of the six 5-fold vectors of tiling.py), centred at
   the origin = the solid's centre, scaled by s; LATTICE argument = the triple, e.g. 012 (oblate) or 023 (prolate);
 - orbits of faces under the stabiliser of the mould in I_h (D3d, order 12; computed exactly) instead of T_h;
 - sampling box = the mould's circumscribed cube; kinds keep their vertex coordinates (for congruence across cells); solids from the amber-cell sweep's solids.py; data to this study's data folder.
Everything else (seeds, outer pattern, Y rule, fins, triangulation, all checks) is unchanged.  Usage: python ammann_cell.py SOLID abc FACTOR cen
The original docstring follows.
Amber-cell sweep (21 Nov 2026): DICTO's combined method ("fill the ends in 2D, then cut the resin to fit"), generalised from
branch E's combi.py (scutoid stand-in study) to any solid of solids.py (star-shaped from its centre, T_h axes on the cube axes).
Method and checks exactly as in combi.py (its docstring follows); changes: solid from solids.build(NAME); s0 computed exactly
(smallest s with the solid inside its Voronoi cell); a persistent wall whose outer chain IS the inner edge (an edge lying on the mould)
is dropped (zero area: bottom and top meet along that edge); counts general.  Usage: python amber.py SOLID LATTICE FACTOR SEED [TAU]
writes ../data/amber_<solid>_<lat>_<fac>_<seed>.json.
Branch E, DICTO's combi method (scutoid + resin), 21 Nov 2026: "fill the ends in 2D, then cut the resin to fit".
Inner pattern = C1's 80 faces. Outer pattern = 3D Voronoi diagram of 80 seeds (one per C1 face) intersected with the mould surface
(this is the definition used throughout; for seeds on the mould it equals the restricted Voronoi of the surface).
Seeds: cen   = face centroid;
       cproj = centroid projected centrally (ray from C1's centre) onto the mould;
       nproj = centroid pushed out along the face normal until it meets the mould.
All in Q(sqrt5), exact.  Pieces: one per C1 face, bottom = the face, top = its outer cell, lateral walls join matching boundaries:
 - an inner edge F|G whose outer boundary F|G is one chain with matching ends is "persistent": wall = polygon (inner edge, up-paths, chain);
 - otherwise the vertices are merged into a cluster with one interior vertex m (the Y vertex) at the midpoint between the mean of the
   cluster's inner vertices and the mean of its outer vertices; an inner edge inside a cluster pinches to m (triangle), an outer chain
   inside a cluster grows from m (fan).  Walls that are not flat are split into flat triangles (ear clipping), facet counts honest.
Checks (rigorous): (1) every piece surface is a closed oriented 2-manifold and every wall triangle is used by exactly two pieces with
opposite orientation (combinatorial); (2) every piece surface is embedded (pairwise triangle tests, float64 with margin 1e-9, exact
Q(sqrt5) when within margin); (3) every piece has positive exact volume; (4) volumes add exactly to mould - C1.  (1)-(3) make each piece
the indicator of its inside and the oriented boundaries add to (mould - C1), so the pieces partition the resin; (4) is the exact
cross-check.  Usage: python combi.py LATTICE FACTOR SEED [TAU]   (e.g. bcc 1 cproj), writes ../data/combi_<lat>_<fac>_<seed>.json."""
import itertools, json, math, os, sys, time
from collections import Counter
from fractions import Fraction as Fr
import numpy as np
import mpmath as mp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.environ.get("RESIN_DIR", os.path.join(HERE, "../../../2026-11-21-scutoid-stand-in/tree/branch-D-resin/scripts")))
sys.path.insert(0, os.path.join(HERE, "../../../2026-11-21-amber-cell-sweep/scripts"))
sys.path.insert(0, os.path.join(HERE, "../../scripts"))
from resin import Q, PHI, dot, cross, vsub, vadd, vsc, det3, congruent, ident, LAMBDA
from tiling import E as E5
mp.mp.dps = 40
from solids import build
T0 = time.time()
def pr(*a): print(*a, flush=True)
def key(v): return tuple(x.key() for x in v)
def fl(v): return np.array([float(x) for x in v])
Z = Q(0)

def shell(lat, s):
    """golden rhombohedron spanned by e_a/3, e_b/3, e_c/3, centred at the origin, scaled by s: n.x <= c"""
    A = [int(ch) for ch in lat]; V3 = [vsc(Fr(1, 3), E5[a]) for a in A]
    H = []
    for k in range(3):
        n = cross(V3[(k+1) % 3], V3[(k+2) % 3]); h = dot(n, V3[k])
        if h.sign() < 0: n = vsc(-1, n); h = -h
        H.append((n, s*h/2)); H.append((vsc(-1, n), s*h/2))
    return H
class _CV(dict):
    def __missing__(self, lat):
        A = [int(ch) for ch in lat]; d = det3(*[vsc(Fr(1, 3), E5[a]) for a in A]); return d if d.sign() > 0 else -d
CELLVOL = _CV()
def _ih():
    """I_h exactly: all linear maps taking the 12 icosahedron vertices onto themselves"""
    Vt = E5 + [vsc(-1, v) for v in E5]
    b = [Vt[0], Vt[2], Vt[4]]
    D = det3(*b); inv = [vsc(Q(1)/D, cross(b[1], b[2])), vsc(Q(1)/D, cross(b[2], b[0])), vsc(Q(1)/D, cross(b[0], b[1]))]   # rows: dual basis
    keys = {key(v) for v in Vt}; G = []
    for t in itertools.permutations(range(12), 3):
        im = [Vt[i] for i in t]
        if any((dot(im[i], im[j]) - dot(b[i], b[j])).sign() != 0 for i in range(3) for j in range(3)): continue
        M = [[sum((im[k][r]*inv[k][c] for k in range(3)), Q(0)) for c in range(3)] for r in range(3)]
        if all(key([dot(M[r], v) for r in range(3)]) in keys for v in Vt): G.append(M)
    assert len(G) == 120
    return G
IH = _ih()
def act(g, x): return [dot(g[r], x) for r in range(3)]
def stabiliser(H):
    hk = {(key(n), c.key() if isinstance(c, Q) else Q(c).key()) for n, c in H}
    return [g for g in IH if all((key(act(g, n)), c.key() if isinstance(c, Q) else Q(c).key()) in hk for n, c in H)]

def mould_faces(H):
    out = []
    for i, (n, c) in enumerate(H):
        pts = {}
        for j, k in itertools.combinations([t for t in range(len(H)) if t != i], 2):
            a, b, cc = n, H[j][0], H[k][0]
            D = det3(a, b, cc)
            if D.sign() == 0: continue
            cx, cy, cz = cross(b, cc), cross(cc, a), cross(a, b)
            X = [(c*cx[t] + H[j][1]*cy[t] + H[k][1]*cz[t])/D for t in range(3)]
            if all((dot(h[0], X) - h[1]).sign() <= 0 for h in H): pts[key(X)] = X
        P = list(pts.values())
        if len(P) < 3: continue
        out.append((i, order_poly(P, n)))
    return out

def order_poly(P, n):
    nf = fl(n); C = sum(fl(p) for p in P)/len(P); u = fl(P[0]) - C; u /= np.linalg.norm(u); w = np.cross(nf/np.linalg.norm(nf), u)
    return sorted(P, key=lambda p: math.atan2(np.dot(fl(p)-C, w), np.dot(fl(p)-C, u)))

def clip(poly, a, b):
    """keep a.x <= b, exact"""
    out = []
    m = len(poly)
    for i in range(m):
        p, q = poly[i], poly[(i+1) % m]
        fp, fq = dot(a, p) - b, dot(a, q) - b
        sp, sq = fp.sign(), fq.sign()
        if sp <= 0: out.append(p)
        if sp*sq < 0:
            t = fp/(fp - fq); out.append(vadd(p, vsc(t, vsub(q, p))))
    ded = []
    for p in out:
        if not ded or key(ded[-1]) != key(p): ded.append(p)
    if len(ded) > 1 and key(ded[0]) == key(ded[-1]): ded.pop()
    return ded

def area2(poly):
    s = [Z, Z, Z]
    for i in range(1, len(poly) - 1): s = vadd(s, cross(vsub(poly[i], poly[0]), vsub(poly[i+1], poly[0])))
    return s

# ---------- triangle intersection (float with margin, exact fallback) ----------
EPS = 1e-9
def orient(a, b, c, d):  # exact sign of det(b-a, c-a, d-a)
    return det3(vsub(b, a), vsub(c, a), vsub(d, a)).sign()
def forient(a, b, c, d):
    v = np.dot(np.cross(b - a, c - a), d - a)
    return 0 if abs(v) < EPS else (1 if v > 0 else -1)
def seg_tri(P, Qv, A, B, C, o):
    """does the closed segment PQ meet the closed triangle ABC (o = orient function)? general, includes coplanar case"""
    s1, s2 = o(A, B, C, P), o(A, B, C, Qv)
    if s1*s2 > 0: return False
    if s1 == 0 and s2 == 0: return None  # coplanar: decided separately
    t1, t2, t3 = o(P, Qv, A, B), o(P, Qv, B, C), o(P, Qv, C, A)
    return (t1 >= 0 and t2 >= 0 and t3 >= 0) or (t1 <= 0 and t2 <= 0 and t3 <= 0)

def tri_pair_ok(T1, T2, X, F):
    """T1, T2 vertex-index triples of one piece surface; True if they meet only in their shared vertices/edge."""
    sh = set(T1) & set(T2)
    if len(sh) == 2:
        a, b = sh; c = [v for v in T1 if v not in sh][0]; d = [v for v in T2 if v not in sh][0]
        # fold-back: coplanar and on the same side of the shared edge
        if orient(X[a], X[b], X[c], X[d]) != 0: return True
        n = cross(vsub(X[b], X[a]), vsub(X[c], X[a]))
        s1 = dot(cross(vsub(X[b], X[a]), vsub(X[c], X[a])), n).sign(); s2 = dot(cross(vsub(X[b], X[a]), vsub(X[d], X[a])), n).sign()
        return s1*s2 < 0
    for fast in (True, False):
        o = (lambda a, b, c, d: forient(a, b, c, d)) if fast else orient
        P = F if fast else X
        hit, amb = False, False
        for U, V in ((T1, T2), (T2, T1)):
            for i in range(3):
                p, q = U[i], U[(i+1) % 3]
                if p in sh and q in sh: continue
                r = seg_tri(P[p], P[q], P[V[0]], P[V[1]], P[V[2]], o)
                if r is None: amb = True; continue
                if r:
                    # touching only at a shared vertex is allowed
                    if p in sh or q in sh:
                        w = q if p in sh else p
                        if o(P[V[0]], P[V[1]], P[V[2]], P[w]) != 0: continue
                        amb = True; continue
                    hit = True
        if fast:
            # decide quickly only if clearly apart (no float hits, no ambiguity with zero orientations)
            if not hit and not amb and not any(forient(F[V[0]], F[V[1]], F[V[2]], F[w]) == 0 for U, V in ((T1, T2), (T2, T1)) for w in U if w not in sh):
                return True
            continue
        if hit: return False
        if amb: return coplanar_ok(T1, T2, X, sh)
        return True

def coplanar_ok(T1, T2, X, sh):
    """exact: both triangles in one plane (or touching in a vertex in plane): test 2D overlap of interiors"""
    n = cross(vsub(X[T1[1]], X[T1[0]]), vsub(X[T1[2]], X[T1[0]]))
    if any(dot(n, vsub(X[w], X[T1[0]])).sign() != 0 for w in T2): return True  # touches plane at a vertex/edge only
    # separating axis in the plane with exact arithmetic
    for U in (T1, T2):
        for i in range(3):
            a, b = X[U[i]], X[U[(i+1) % 3]]; ax = cross(n, vsub(b, a))
            p1 = [dot(ax, X[w]) for w in T1]; p2 = [dot(ax, X[w]) for w in T2]
            def mx(L):
                m = L[0]
                for x in L:
                    if (x - m).sign() > 0: m = x
                return m
            def mn(L):
                m = L[0]
                for x in L:
                    if (x - m).sign() < 0: m = x
                return m
            if (mx(p1) - mn(p2)).sign() <= 0 or (mx(p2) - mn(p1)).sign() <= 0: return True
    return False

def earclip(idx, X):
    """triangulate a (possibly non-planar) simple polygon given by vertex indices; projection on the best-fit plane"""
    if len(idx) == 3: return [tuple(idx)]
    P = np.array([fl(X[i]) for i in idx]); C = P.mean(0)
    nrm = np.zeros(3)
    for i in range(len(P)): nrm += np.cross(P[i] - C, P[(i+1) % len(P)] - C)
    nrm /= np.linalg.norm(nrm); u = np.cross(nrm, [1, 0, 0] if abs(nrm[0]) < .9 else [0, 1, 0]); u /= np.linalg.norm(u); w = np.cross(nrm, u)
    pts = {i: np.array([np.dot(p - C, u), np.dot(p - C, w)]) for i, p in zip(idx, P)}
    L = list(idx); tris = []
    def cr(a, b, c): return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])
    guard = 0
    while len(L) > 3 and guard < 1000:
        guard += 1
        best = None
        for k in range(len(L)):
            a, b, c = L[k-1], L[k], L[(k+1) % len(L)]
            if cr(pts[a], pts[b], pts[c]) <= 1e-12: continue
            if any(cr(pts[a], pts[b], pts[x]) >= 0 and cr(pts[b], pts[c], pts[x]) >= 0 and cr(pts[c], pts[a], pts[x]) >= 0 for x in L if x not in (a, b, c)): continue
            # prefer the ear with the best minimal angle
            q = min(abs(cr(pts[a], pts[b], pts[c]))/(np.linalg.norm(pts[a]-pts[b])*np.linalg.norm(pts[c]-pts[b]) + 1e-300), 1)
            if best is None or q > best[0]: best = (q, k)
        if best is None: return None
        k = best[1]; tris.append((L[k-1], L[k], L[(k+1) % len(L)])); L.pop(k)
    tris.append(tuple(L))
    return tris

def triangulations(L):
    if len(L) < 3: yield []; return
    if len(L) == 3: yield [tuple(L)]; return
    a, b = L[0], L[-1]
    for k in range(1, len(L) - 1):
        for t1 in triangulations(L[:k+1]):
            for t2 in triangulations(L[k:]):
                yield t1 + t2 + [(a, L[k], b)]

def min_area_tri(poly, X):
    """non-flat wall: the triangulation of least total area (isometry-invariant); exact ties -> 'centre'"""
    P = {i: fl(X[i]) for i in poly}
    best = []
    for T in triangulations(list(poly)):
        A = sum(np.linalg.norm(np.cross(P[b] - P[a], P[c] - P[a]))/2 for a, b, c in T)
        if any(np.linalg.norm(np.cross(P[b] - P[a], P[c] - P[a])) < 1e-12 for a, b, c in T): continue
        best.append((A, T))
    if not best: return None
    best.sort(key=lambda x: x[0])
    if len(best) > 1 and best[1][0] - best[0][0] < 1e-9: return "centre"
    return best[0][1]

def main():
    solid, lat, fac, seedmode = sys.argv[1], sys.argv[2], Fr(sys.argv[3]), sys.argv[4]
    tau = Fr(sys.argv[5]) if len(sys.argv) > 5 else Fr(1, 2)
    from aligned import aligned
    C = aligned(solid, IH, act); pr(f"solid orientation: {C['aligned']}"); V, faces, planes = C["V"], C["faces"], C["planes"]
    NV, NF = len(V), len(faces)
    assert all(c.sign() > 0 for n, c in planes), "every face plane at positive offset from the centre (star-shaped)"
    s0 = None
    for n, c in shell(lat, Q(1)):
        for v in V:
            r = dot(n, v)/c
            if s0 is None or (r - s0).sign() > 0: s0 = r
    s = s0*fac
    if os.environ.get("AMBER_S"):          # absolute scale a,b -> s = a + b sqrt5 (mixed bcc cell: both solids at one common s)
        a_, b_ = os.environ["AMBER_S"].split(","); s = Q(Fr(a_), Fr(b_)); assert (s - s0).sign() >= 0, "s below s0"; fac = "S" + str(s).replace("/", "|")
    if os.environ.get("AMBER_TAG"): fac = os.environ["AMBER_TAG"]
    H = shell(lat, s)
    STAB = stabiliser(H); pr(f"stabiliser of the mould in I_h: order {len(STAB)}")
    pr(f"=== amber  {solid}  {lat}  s0 = {s0} = {float(s0):.6f}  s = {fac} s0 = {float(s):.6f}  seeds {seedmode}  tau {tau}")
    volC1 = Q(0)
    for (f, kind) in faces:
        P = [V[i] for i in f]
        for q in range(1, len(P) - 1):
            d = det3(P[0], P[q], P[q+1]); volC1 = volC1 + (d if d.sign() > 0 else -d)
    volC1 = volC1/6; volres = s*s*s*CELLVOL[lat] - volC1
    # contact of C1 with the mould
    contact = [i for i, v in enumerate(V) if any((dot(n, v) - c).sign() == 0 for n, c in H)]
    def onplane(idx): return any(all((dot(n, V[i]) - c).sign() == 0 for i in idx) for n, c in H)
    cedges = sum(1 for f, k in faces for i in range(len(f)) if onplane([f[i], f[(i+1) % len(f)]]))//2
    cfaces = sum(1 for f, k in faces if onplane(f))
    pr(f"solid vertices on the mould surface: {len(contact)}; edges on it {cedges}; faces on it {cfaces}")
    # seeds
    cent = [[sum((V[i][j] for i in f), Z)/len(f) for j in range(3)] for f, k in faces]
    seeds = []
    for F in range(NF):
        c0 = cent[F]
        if seedmode == "cen": seeds.append(c0)
        elif seedmode == "cproj":
            t = None
            for n, c in H:
                d = dot(n, c0)
                if d.sign() > 0:
                    r = c/d
                    if t is None or (r - t).sign() < 0: t = r
            seeds.append(vsc(t, c0))
        elif seedmode == "nproj":
            nF = planes[F][0]; t = None
            for n, c in H:
                d = dot(n, nF)
                if d.sign() > 0:
                    r = (c - dot(n, c0))/d
                    if t is None or (r - t).sign() < 0: t = r
            seeds.append(vadd(c0, vsc(t, nF)))
    sq = [dot(p, p) for p in seeds]
    def cellset(x):
        d = [dot(vsub(x, p), vsub(x, p)) for p in seeds]; m = d[0]
        for y in d:
            if (y - m).sign() < 0: m = y
        return frozenset(F for F in range(NF) if (d[F] - m).sign() == 0)
    # outer pattern: clip every mould face by the Voronoi halfspaces of every seed
    MF = mould_faces(H)
    pr(f"mould faces {len(MF)}  ({time.time()-T0:.1f}s)")
    sf = np.array([fl(p) for p in seeds])
    cells = {F: [] for F in range(NF)}          # F -> list of (mould face index, polygon)
    for mi, poly in MF:
        pf = np.array([fl(p) for p in poly]); cen_f = pf.mean(0); rad = np.linalg.norm(pf - cen_f, axis=1).max()
        for F in range(NF):
            P = poly
            # cull: other seeds ordered by distance
            order = sorted(range(NF), key=lambda G: np.linalg.norm(sf[G] - sf[F]))
            for G in order:
                if G == F: continue
                # skip G whose bisector cannot cut the face disc (float test with margin)
                a = 2*(sf[G] - sf[F]); b = sf[G] @ sf[G] - sf[F] @ sf[F]
                if a @ cen_f + np.linalg.norm(a)*rad < b - 1e-7: continue
                P = clip(P, vsc(2, vsub(seeds[G], seeds[F])), sq[G] - sq[F])
                if len(P) < 3: break
            if len(P) >= 3:
                A = area2(P)
                if any(x.sign() != 0 for x in A): cells[F].append((mi, P))
    empty = [F for F in range(NF) if not cells[F]]
    pr(f"outer pattern computed ({time.time()-T0:.1f}s); faces with an empty outer cell: {empty}")
    res = dict(solid=solid, s0=str(s0), s0_float=float(s0), n_faces=NF, contact_edges=cedges, contact_faces=cfaces, lattice=lat, factor=str(fac), s=float(s), seeds=seedmode, tau=str(tau), contact_vertices=contact)
    def finish(ok, why):
        res["valid"] = ok; res["why"] = why
        json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"../data/geom_{solid}_{lat}_{str(fac).replace('/', '-')}_{seedmode}.json"), "w"), indent=1, default=str)
        pr(f"RESULT {lat} {fac} {seedmode}: valid={ok}  {why}")
        pr(f"({time.time()-T0:.1f}s)")
    if empty: return finish(False, f"empty outer cells {empty}")
    # vertex registry
    X, kid = [], {}
    def vid(p):
        k = key(p)
        if k not in kid: kid[k] = len(X); X.append(p)
        return kid[k]
    for v in V: vid(v)                           # inner vertices 0..71
    TS = {}
    topp = {F: [[vid(p) for p in P] for mi, P in cells[F]] for F in range(NF)}
    for F in range(NF):
        for P in topp[F]:
            for v in P:
                if v not in TS: TS[v] = cellset(X[v])
    # connectivity of each outer cell (polygons joined along shared edges)
    disc = []
    for F in range(NF):
        polys = topp[F]; comp = list(range(len(polys)))
        def fnd(a):
            while comp[a] != a: a = comp[a]
            return a
        E = [{frozenset((P[i], P[(i+1) % len(P)])) for i in range(len(P))} for P in polys]
        for a, b in itertools.combinations(range(len(polys)), 2):
            if E[a] & E[b]: comp[fnd(a)] = fnd(b)
        if len({fnd(a) for a in range(len(polys))}) > 1: disc.append(F)
    if disc: return finish(False, f"disconnected outer cells {disc}")
    # outer segments F|G
    seg = {}
    for F in range(NF):
        for P in topp[F]:
            for i in range(len(P)):
                a, b = P[i], P[(i+1) % len(P)]
                T = cellset(vsc(Fr(1, 2), vadd(X[a], X[b])))
                if len(T) == 2: seg.setdefault(frozenset(T), set()).add(frozenset((a, b)))
                elif len(T) > 2: return finish(False, f"segment with {len(T)} cells")
    # chains per pair
    chains = {}
    for pair, S in seg.items():
        adj = {}
        for e in S:
            a, b = tuple(e); adj.setdefault(a, []).append(b); adj.setdefault(b, []).append(a)
        ends = [v for v in adj if len(TS[v]) >= 3]
        if any(len(adj[v]) > 2 for v in adj) or any(len(adj[v]) != 1 for v in ends) or any(len(TS[v]) == 2 and len(adj[v]) != 2 for v in adj):
            return finish(False, f"irregular outer boundary for pair {sorted(pair)}")
        used, L = set(), []
        for e0 in sorted(ends):
            if e0 in used: continue
            ch = [e0]; used.add(e0)
            while True:
                nx = [w for w in adj[ch[-1]] if w not in used]
                if not nx: break
                ch.append(nx[0]); used.add(nx[0])
                if len(TS[ch[-1]]) >= 3: break
            L.append(ch)
        if len(used) != len(adj): return finish(False, f"closed outer loop for pair {sorted(pair)}")
        chains[pair] = L
    # inner pattern
    edge_face = {}
    for fi, (f, kind) in enumerate(faces):
        for i in range(len(f)): edge_face.setdefault(frozenset((f[i], f[(i+1) % len(f)])), []).append(fi)
    inner_pairs = {frozenset(F): e for e, F in edge_face.items()}
    SV = {v: frozenset(fi for fi, (f, k) in enumerate(faces) if v in f) for v in range(NV)}
    Nin = {F: set() for F in range(NF)}; Nout = {F: set() for F in range(NF)}
    for p in inner_pairs:
        a, b = tuple(p); Nin[a].add(b); Nin[b].add(a)
    for p in chains:
        a, b = tuple(p); Nout[a].add(b); Nout[b].add(a)
    shared = sum(1 for p in inner_pairs if p in chains); extra = sum(1 for p in chains if p not in inner_pairs)
    pr(f"adjacency: inner pairs {len(inner_pairs)}, outer pairs {len(chains)}, shared {shared}, outer-only {extra}, inner-only {len(inner_pairs) - shared}")
    res.update(inner_pairs=len(inner_pairs), outer_pairs=len(chains), shared_pairs=shared)
    # persistence and clusters
    par = {}
    def fnd(a):
        par.setdefault(a, a)
        while par[a] != a: par[a] = par[par[a]]; a = par[a]
        return a
    def uni(a, b): par[fnd(a)] = fnd(b)
    persistent = {}
    # inner clusters first: an inner edge with no single matching outer chain pinches; repeat with cluster face sets until stable
    ip = {v: v for v in range(NV)}
    def ifn(v):
        while ip[v] != v: ip[v] = ip[ip[v]]; v = ip[v]
        return v
    pinched = set(); fails = []; pinched_phase1_done = False
    changed = True
    while changed:
        changed = False
        SK = {}
        for v in range(NV): SK[ifn(v)] = SK.get(ifn(v), frozenset()) | SV[v]
        for p, e in inner_pairs.items():
            if p in pinched: continue
            v, w = tuple(e); L = chains.get(p, [])
            ok = False
            if len(L) == 1 and ifn(v) != ifn(w):
                c, c2 = L[0][0], L[0][-1]
                ok = (TS[c] <= SK[ifn(v)] and TS[c2] <= SK[ifn(w)]) or (TS[c2] <= SK[ifn(v)] and TS[c] <= SK[ifn(w)])
            if not ok:
                if len(L) != 1 or not pinched_phase1_done:
                    if len(L) != 1: pinched.add(p); ip[ifn(v)] = ifn(w); changed = True
                    continue
                fails.append((p, v, w))
        if not pinched_phase1_done:
            pinched_phase1_done = True; changed = True; continue
        for p, v, w in fails:
            pinched.add(p); ip[ifn(v)] = ifn(w); changed = True
        fails = []
    SK = {}
    for v in range(NV): SK[ifn(v)] = SK.get(ifn(v), frozenset()) | SV[v]
    pr("pinched inner edges:", sorted(tuple(sorted(faces[f][1] for f in p)) for p in pinched).__len__(), dict(Counter(tuple(sorted(faces[f][1] for f in p)) for p in pinched)))
    for p, e in inner_pairs.items():
        v, w = tuple(e); fnd(("i", v)); fnd(("i", w))
        if p in pinched: uni(("i", v), ("i", w)); continue
        ch = chains[p][0]; c, c2 = ch[0], ch[-1]
        if TS[c] <= SK[ifn(v)] and TS[c2] <= SK[ifn(w)]: persistent[p] = (v, w, ch); uni(("i", v), ("o", c)); uni(("i", w), ("o", c2))
        else: persistent[p] = (v, w, ch[::-1]); uni(("i", v), ("o", c2)); uni(("i", w), ("o", c))
    for p, L in chains.items():
        for ch in L:
            fnd(("o", ch[0])); fnd(("o", ch[-1]))
            if p in persistent and persistent[p][2] in (ch, ch[::-1]): continue
            uni(("o", ch[0]), ("o", ch[-1]))
    clusters = {}
    for n in list(par): clusters.setdefault(fnd(n), []).append(n)
    mvert = {}
    nY = 0
    for r, mem in clusters.items():
        I = [n[1] for n in mem if n[0] == "i"]; O = [n[1] for n in mem if n[0] == "o"]
        if not I or not O: return finish(False, f"cluster without inner or outer vertices ({len(I)} inner, {len(O)} outer); persistent inner edges {len(persistent)}/{len(inner_pairs)}")
        fi_ = frozenset().union(*[SV[v] for v in I]); fo_ = frozenset().union(*[TS[c] for c in O])
        if fi_ != fo_: return finish(False, f"cluster face sets differ inner {sorted(fi_)} outer {sorted(fo_)}")
        if len(I) == 1 and len(O) == 1 and SV[I[0]] == TS[O[0]]: mvert[r] = None; continue
        mi_ = [sum((X[v][j] for v in I), Z)/len(I) for j in range(3)]; mo_ = [sum((X[c][j] for c in O), Z)/len(O) for j in range(3)]
        # Y vertex: on the ray from C1's centre through the mean of the cluster's vertices, at fraction tau between C1 and the mould
        d = [sum((X[v][j] for v in I), Z) + sum((X[c][j] for c in O), Z) for j in range(3)]
        t_in = None
        for fi, (nF, cF) in enumerate(planes):
            f = faces[fi][0]
            # direction inside the cone of face fi (central cone; C1 is star-shaped from the centre)
            if all(det3(V[f[i]], V[f[(i+1) % len(f)]], d).sign() * det3(V[f[0]], V[f[1]], cent[fi]).sign() >= 0 for i in range(len(f))):
                t_in = cF/dot(nF, d); break
        t_out = None
        for n, c in H:
            dd = dot(n, d)
            if dd.sign() > 0:
                rr = c/dd
                if t_out is None or (rr - t_out).sign() < 0: t_out = rr
        if t_in is None or (t_out - t_in).sign() <= 0: return finish(False, "Y vertex direction meets the mould at C1")
        mvert[r] = vid(vsc((1 - tau)*t_in + tau*t_out, d)); nY += 1
    Yset = {m for m in mvert.values() if m is not None}
    csize = sorted((sum(1 for n in mem if n[0] == "i"), sum(1 for n in mem if n[0] == "o")) for mem in clusters.values())
    pr(f"clusters {len(clusters)}: (inner, outer) vertex counts {dict(Counter(csize))}; Y vertices {nY}; persistent inner edges {len(persistent)}/{len(inner_pairs)}")
    def up(n):
        """vertex path from node n=('i',v) or ('o',c) to its cluster centre and the matched partner"""
        return mvert[fnd(n)]
    # walls
    walls = []   # (F, G, polygon) orientation arbitrary
    for p, (v, w, ch) in persistent.items():
        mv, mw = up(("i", v)), up(("i", w))
        if w == ch[-1]: mw = None          # C1 vertex on the mould = its own outer vertex: no vertical edge
        if v == ch[0]: mv = None
        if len(ch) == 2 and v == ch[0] and w == ch[-1]: continue   # inner edge lies on the mould: zero-area wall, bottom meets top
        poly = [v, w] + ([mw] if mw is not None else []) + ch[::-1] + ([mv] if mv is not None else [])
        walls.append((p, poly, "persistent"))
    for p, e in inner_pairs.items():
        if p in persistent: continue
        v, w = tuple(e); m = up(("i", v))
        walls.append((p, [v, w, m], "pinch"))
    for p, L in chains.items():
        for ch in L:
            if p in persistent and persistent[p][2] in (ch, ch[::-1]): continue
            m = up(("o", ch[0]))
            walls.append((p, [m] + ch, "grow"))
    # triangulate walls; flat test
    wtris, wflat = [], []
    for wi, (p, poly, kind) in enumerate(walls):
        # a C1 vertex lying on the mould is its own outer vertex: drop the zero-length vertical edge
        poly = [q for i, q in enumerate(poly) if q != poly[i-1]]; walls[wi] = (p, poly, kind)
        if len(set(poly)) != len(poly): return finish(False, f"degenerate wall {sorted(p)} {kind} {poly} TS {[sorted(TS.get(q, [])) for q in poly]}")
        n = None; flat = True
        for i in range(1, len(poly) - 1):
            nn = cross(vsub(X[poly[i]], X[poly[0]]), vsub(X[poly[i+1]], X[poly[0]]))
            if any(x.sign() for x in nn): n = nn; break
        if n is None: return finish(False, f"collinear wall {sorted(p)}")
        flat = all(dot(n, vsub(X[q], X[poly[0]])).sign() == 0 for q in poly)
        T = earclip(poly, X) if flat else min_area_tri(poly, X)
        if T is None: return finish(False, f"wall {sorted(p)} cannot be triangulated")
        if T == "centre":   # tie between mirror triangulations: fan from the wall's vertex centroid (keeps the symmetry)
            cpt = vid([sum((X[q][j] for q in poly), Z)/len(poly) for j in range(3)])
            T = [(cpt, poly[i], poly[(i+1) % len(poly)]) for i in range(len(poly))]
        wtris.append(T); wflat.append(flat)
    # piece surfaces
    pieces = []
    total = Q(0); allok = True; bad = []; nbt = [0]; nfin = [0]
    for F in range(NF):
        polys = [(list(faces[F][0]), "bottom")] + [(P, "top") for P in topp[F]] + [(walls[k][1], ("wall", k)) for k in range(len(walls)) if F in walls[k][0]]
        # orient consistently by BFS on directed edges
        de = {}
        for idx, (P, lab) in enumerate(polys):
            for i in range(len(P)): de.setdefault(frozenset((P[i], P[(i+1) % len(P)])), []).append(idx)
        man = all(len(x) == 2 for x in de.values())
        if not man:
            bad.append((F, "not a closed 2-manifold")); allok = False; continue
        def draw(idx, e):
            P = polys[idx][0]
            for i in range(len(P)):
                if frozenset((P[i], P[(i+1) % len(P)])) == e: return (P[i], P[(i+1) % len(P)])
        sign = {0: 1}; stack = [0]; orientable = True
        while stack:
            a = stack.pop(); P = polys[a][0]
            for i in range(len(P)):
                e = frozenset((P[i], P[(i+1) % len(P)]))
                for b in de[e]:
                    if b == a: continue
                    sb = -sign[a] if draw(b, e) == draw(a, e) else sign[a]
                    if b in sign:
                        if sign[b] != sb: orientable = False
                    else: sign[b] = sb; stack.append(b)
        if len(sign) != len(polys) or not orientable:
            bad.append((F, "not orientable / not connected")); allok = False; continue
        # triangles with orientation
        tris = []
        for idx, (P, lab) in enumerate(polys):
            if lab in ("bottom", "top"):
                T = [(P[0], P[i], P[i+1]) for i in range(1, len(P) - 1) if any(x.sign() for x in cross(vsub(X[P[i]], X[P[0]]), vsub(X[P[i+1]], X[P[0]])))]
                nbt[0] += len(T)
            else:
                T = wtris[lab[1]]
                # orient wall triangles to agree with the polygon's direction
                Pd = {(P[i], P[(i+1) % len(P)]) for i in range(len(P))}
                ok_dir = any(((t[i], t[(i+1) % 3]) in Pd) for t in T for i in range(3))
                if not ok_dir: T = [t[::-1] for t in T]
            if sign[idx] < 0: T = [t[::-1] for t in T]
            tris += T
        # a fin: two walls of this piece that share the triangle (v, m, c) with opposite orientation (a face meeting only one outer
        # vertex of a cluster): the pair cancels, the piece's corner edge is v-c, and the two neighbours meet across (v, m, c)
        cnt = {}
        for t in tris: cnt.setdefault(frozenset(t), []).append(t)
        drop = set()
        for k_, L in cnt.items():
            if len(L) == 2 and {(L[0][i], L[0][(i+1) % 3]) for i in range(3)} == {(L[1][(i+1) % 3], L[1][i]) for i in range(3)}: drop.add(k_)
        if drop: tris = [t for t in tris if frozenset(t) not in drop]; nfin[0] += len(drop)
        vol = sum((det3(X[a], X[b], X[c]) for a, b, c in tris), Q(0))/6
        if vol.sign() < 0: vol = -vol; tris = [t[::-1] for t in tris]
        # embedding: pairwise triangle tests within the piece
        Fl = {i: fl(X[i]) for t in tris for i in t}
        bb = [(np.min([Fl[i] for i in t], 0) - 1e-9, np.max([Fl[i] for i in t], 0) + 1e-9) for t in tris]
        emb = True
        for i, j in itertools.combinations(range(len(tris)), 2):
            if np.any(bb[i][1] < bb[j][0]) or np.any(bb[j][1] < bb[i][0]): continue
            if not tri_pair_ok(tris[i], tris[j], X, Fl): emb = False; break
        if not emb or vol.sign() <= 0:
            bad.append((F, "self-intersecting surface" if not emb else "non-positive volume")); allok = False
        total = total + vol
        pieces.append(dict(F=F, kind=faces[F][1], polys=polys, tris=tris, vol=vol))
    # global cancellation: every wall triangle used by exactly two pieces with opposite orientation
    if allok:
        use = {}
        for pc in pieces:
            for t in pc["tris"]:
                k = frozenset(t); use.setdefault(k, []).append((pc["F"], t))
        canc = True
        for k, L in use.items():
            if len(L) == 1: continue
            if len(L) != 2: canc = False; break
            (F1, t1), (F2, t2) = L
            r1 = {(t1[i], t1[(i+1) % 3]) for i in range(3)}; r2 = {(t2[(i+1) % 3], t2[i]) for i in range(3)}
            if r1 != r2: canc = False; break
        single = [k for k, L in use.items() if len(L) == 1]
        # singles must be exactly C1-surface and mould-surface triangles
        bottomtops = nbt[0]
        canc = canc and len(single) == bottomtops
        if not canc:
            multi = [(k, [F for F, t in L]) for k, L in use.items() if len(L) > 2][:3]
            bad.append((-1, f"wall triangles do not cancel in pairs (singles {len(single)} vs C1+mould {bottomtops}; used >2: {multi})")); allok = False
    # independent cross-check (float, sampling): winding number of every piece at random points of the mould
    mc = None
    if allok:
        rng = np.random.default_rng(1)
        Hn = np.array([fl(n) for n, c in H]); Hc = np.array([float(c) for n, c in H])
        R = 1.0001*float(s)*max(abs(float(sum((sg[q]*E5[int(lat[q])][r]/6 for q in range(3)), Q(0)))) for sg in itertools.product((1, -1), repeat=3) for r in range(3))   # circumscribed cube of the mould
        pts = rng.uniform(-R, R, size=(60000, 3)); pts = pts[np.all(pts @ Hn.T <= Hc, axis=1)][:6000]
        Pn = np.array([fl(n) for n, c in planes]); Pc = np.array([float(c) for n, c in planes])
        Vf = np.array([fl(v) for v in V])
        inC1 = np.zeros(len(pts), bool)
        for fi, (f, kind) in enumerate(faces):
            A = Vf[f]
            cone = np.ones(len(pts), bool)
            for i in range(len(f)):
                nn = np.cross(A[i], A[(i+1) % len(f)])
                if nn @ A.mean(0) < 0: nn = -nn
                cone &= pts @ nn >= 0
            inC1 |= cone & (pts @ Pn[fi] < Pc[fi])
        W = np.zeros(len(pts))
        worst = 0.0
        for pc in pieces:
            w = np.zeros(len(pts))
            for a, b, c in pc["tris"]:
                A = fl(X[a]) - pts; B = fl(X[b]) - pts; Cc = fl(X[c]) - pts
                la, lb, lc = np.linalg.norm(A, axis=1), np.linalg.norm(B, axis=1), np.linalg.norm(Cc, axis=1)
                num = np.einsum("ij,ij->i", A, np.cross(B, Cc))
                den = la*lb*lc + np.einsum("ij,ij->i", A, B)*lc + np.einsum("ij,ij->i", A, Cc)*lb + np.einsum("ij,ij->i", B, Cc)*la
                w += 2*np.arctan2(num, den)
            w /= 4*np.pi
            worst = max(worst, float(np.abs(w - np.round(w)).max()))
            if np.any(np.round(w) < 0) or np.any(np.round(w) > 1): worst = max(worst, 9)
            W += np.round(w)
        err = int(np.sum(W != np.where(inC1, 0, 1)))
        mc = dict(points=len(pts), in_resin=int((~inC1).sum()), miscounted=err, max_rounding=worst)
        pr(f"sampling cross-check: {len(pts)} points ({int((~inC1).sum())} in the resin), points not covered exactly once: {err}, max winding rounding {worst:.2e}")
        res["sampling"] = mc
        if err: bad.append((-1, f"sampling: {err} points not covered exactly once")); allok = False
    res["fins_cancelled"] = nfin[0]
    gap = total - volres
    volok = gap.sign() == 0
    pr(f"volume sum - resin = {gap} ({'exact 0' if volok else 'NONZERO'}); resin = {float(volres):.6f}; problems {len(bad)}: {bad}")
    valid = allok and volok
    res.update(volume_gap=str(gap), resin=float(volres), n_Y=nY, persistent=len(persistent), clusters=dict(Counter(csize)) and [list(c) for c in csize],
               problems=[list(b) for b in bad])
    if not valid: return finish(False, f"partition checks failed: {bad[:4]}, volume ok {volok}")
    # analysis per piece
    keyv = {key(v): i for i, v in enumerate(V)}
    fid = {frozenset(f): i for i, (f, k) in enumerate(faces)}
    def gface(g, fi): return fid[frozenset(keyv[key(act(g, V[i]))] for i in faces[fi][0])]
    orbits, done = [], set()
    for fi in range(NF):
        if fi in done: continue
        orb = sorted({gface(g, fi) for g in STAB}); done |= set(orb); orbits.append(orb)
    def nrm(t): return cross(vsub(X[t[1]], X[t[0]]), vsub(X[t[2]], X[t[0]]))
    lam_any = False; recs = []
    for pc in pieces:
        F = pc["F"]
        # merge coplanar adjacent triangles into facets (exact)
        tris = pc["tris"]; parent = list(range(len(tris)))
        def fd(a):
            while parent[a] != a: a = parent[a]
            return a
        N = [nrm(t) for t in tris]
        ed = {}
        for i, t in enumerate(tris):
            for k in range(3): ed.setdefault(frozenset((t[k], t[(k+1) % 3])), []).append(i)
        for e, L in ed.items():
            i, j = L
            c = cross(N[i], N[j])
            if all(x.sign() == 0 for x in c) and dot(N[i], N[j]).sign() > 0: parent[fd(i)] = fd(j)
        facets = {}
        for i in range(len(tris)): facets.setdefault(fd(i), []).append(i)
        verts = sorted({v for t in tris for v in t})
        # true vertices: where >= 3 facets meet
        vf = {v: {fd(i) for i, t in enumerate(tris) if v in t} for v in verts}
        tv = [v for v in verts if len(vf[v]) >= 3]
        # dihedrals between facets (exact cos, mp)
        angs = {}
        c1side = []
        for e, (i, j) in ed.items():
            if fd(i) == fd(j): continue
            n1, n2 = N[i], N[j]
            # interior dihedral: pi - angle between outward normals
            cth = -(dot(n1, n2)).mpf()/mp.sqrt((dot(n1, n1)*dot(n2, n2)).mpf())
            th = mp.acos(cth)
            # reflex test: is the edge convex? third vertex of j relative to plane of i
            a, b = tuple(e); d = [v for v in tris[j] if v not in e][0]
            if dot(n1, vsub(X[d], X[a])).sign() > 0: th = 2*mp.pi - th
            k_ = mp.nstr(th*180/mp.pi, 12)
            oncl = a < NV and b < NV
            if k_ not in angs: angs[k_] = th
            if oncl: c1side.append(float(th*180/mp.pi))
            if abs(th - LAMBDA) < mp.mpf(10)**-25: lam_any = True
        Yp = [v for v in tv if v in Yset]
        nf = len(facets)
        recs.append(dict(F=F, kind=pc["kind"], vol=float(pc["vol"]), volx=str(pc["vol"]), n_facets=nf, n_vertices=len(tv), n_edges=len(tv) + nf - 2,
                         Nin=sorted(Nin[F]), Nout=sorted(Nout[F]), Y=len(Yp), scutoid=bool(Yp) and Nin[F] != Nout[F],
                         c1_edge_angles=sorted(set(round(x, 4) for x in c1side)), angles=sorted(round(float(t*180/mp.pi), 4) for t in angs.values()),
                         angle_basis={mp.nstr(t*180/mp.pi, 10): ident(t) for t in angs.values()} if F in [o[0] for o in orbits] else None,
                         verts=[[float(x) for x in X[v]] for v in tv]))
    # kinds: congruence among orbit representatives (and check orbit members are congruent to their representative)
    kinds = []
    for o in orbits:
        r = recs[o[0]]
        for k in kinds:
            if abs(k["vol"] - r["vol"]) < 1e-9 and congruent(np.array(k["verts"]), np.array(r["verts"])): k["members"] += o; break
        else: kinds.append(dict(r, members=list(o)))
    orbit_ok = all(abs(recs[f]["vol"] - recs[o[0]]["vol"]) < 1e-9 and congruent(np.array(recs[f]["verts"]), np.array(recs[o[0]]["verts"])) for o in orbits for f in o[:3])
    nsc = sum(1 for r in recs if r["scutoid"])
    pr(f"PARTITION (manifold, embedded, cancelling, exact volume).  pieces {NF}, scutoid pieces {nsc}, kinds {len(kinds)} (stabiliser orbit members congruent: {orbit_ok}); 157.7612 present: {lam_any}")
    for k in kinds:
        pr(f"  kind {k['kind']} face {k['F']} ({len(k['members'])} per cell): facets {k['n_facets']} vertices {k['n_vertices']} Y {k['Y']} scutoid {k['scutoid']} "
           f"vol {k['vol']:.6f}  C1-side neighbours {k['Nin']} mould-side {k['Nout']}")
        pr(f"     angles at C1 edges: {k['c1_edge_angles']}")
        pr(f"     all dihedrals: " + "; ".join(f"{d} [{b or 'not in basis'}]" for d, b in sorted(k['angle_basis'].items(), key=lambda x: float(x[0]))))
    res.update(n_scutoid_pieces=nsc, n_kinds=len(kinds), lambda_present=lam_any, orbit_members_congruent=orbit_ok,
               kinds=[dict(k) for k in kinds], pieces=[{x: r[x] for x in r if x not in ("verts", "angle_basis")} for r in recs])
    res["geom"] = dict(X=[fl(x).tolist() for x in X], pieces=[dict(F=pc["F"], tris=[list(map(int, tr)) for tr in pc["tris"]], polys=[[list(map(int, P)), lab if isinstance(lab, str) else "wall"] for P, lab in pc["polys"]]) for pc in pieces], Y=sorted(int(v) for v in Yset), nC1=len(V))
    finish(True, f"partition; scutoid pieces {nsc}; kinds {len(kinds)}; Y vertices {nY}; 157.7612 present {lam_any}")

if __name__ == "__main__":
    main()
