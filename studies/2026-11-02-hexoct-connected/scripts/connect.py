# HexOct connected tiles (DICTO 2026-11-02: "really want to sort out HexOct into two true simple pieces").
# Each layer tile of #75 = 4 convex pieces (2 tetrahedral parts, 2 octahedral halves; 2 pieces at the walk's ends). Any piece may
# be replaced by an in-layer lattice translate (u, v integer, z kept): the set of all copies in the layer is unchanged, so the
# result is still a fundamental domain of that layer and the layer slab, hence every stacking, is filled exactly as before.
# This script, per weight λ and tile type (c = tile('ABC',1,λ), h = tile('AB',0,λ) of tiles.py):
#  1. exact facets of every piece; exact face contacts between piece pairs at every relative translate (coplanar facets with
#     opposite normals, overlap polygon of positive area, rational);
#  2. all translate choices with piece 0 fixed and pieces 1..3 at (a, b), -2 <= a, b <= 2 (25^3 = 15625); keep those whose
#     face-contact graph is connected;
#  3. congruent survivors merged (12 lattice symmetries x {z, -z} x translation);
#  4. for each class: exact merged faces (exactfaces.union_faces, coplanar faces merged), surface check (every side used by
#     exactly two faces = no edge/point pinch), exact volume, convex-hull volume ratio (float), neck = least total contact area
#     over all ways to split the pieces in two (in unit-triangle areas sqrt(3)/4), symmetry order.
# Usage: ~/geom/bin/python connect.py <lam> [<lam> ...]  -> data/conn_<lam>.json
import itertools, json, os, sys, math
from fractions import Fraction as Fr
import numpy as np
from scipy.spatial import ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from tiles import tile, SYM
import exactfaces as E

D = math.sqrt(2 / 3); TRI = math.sqrt(3) / 4
def cart(p): return np.array([float(p[0]) + float(p[1]) / 2, float(p[1]) * math.sqrt(3) / 2, float(p[2]) * D])
W = 2                                     # window of translates for pieces 1..3

def shift(X, t): return [(p[0] + t[0], p[1] + t[1], p[2]) for p in X]

def poly2(n, pts):
    k, ax = E.proj_axes(n); return E.hull2([(p[ax[0]], p[ax[1]]) for p in pts]), k, ax

def inter2(P, Q):
    """exact intersection of two convex ccw polygons (lists of 2D points)"""
    R = P
    for i in range(len(Q)):
        a, b = Q[i], Q[(i + 1) % len(Q)]
        L = (b[1] - a[1], a[0] - b[0]); c = L[0] * a[0] + L[1] * a[1]
        # interior of ccw Q is to the left of a->b: L.x - c <= 0 there  -> keep side -1
        R = E.clip(R, (L[0], L[1], c), -1)
        if not R: return None
    return R

def area2(P): return sum(P[i][0] * P[(i + 1) % len(P)][1] - P[(i + 1) % len(P)][0] * P[i][1] for i in range(len(P))) / 2

def real_area(n, poly, k, ax, c):
    def lift(p):
        x = [None] * 3; x[ax[0]], x[ax[1]] = p; x[k] = (c - n[ax[0]] * p[0] - n[ax[1]] * p[1]) / Fr(n[k]); return cart(x)
    Q = [lift(p) for p in poly]; s = np.zeros(3)
    for i in range(1, len(Q) - 1): s += np.cross(Q[i] - Q[0], Q[i + 1] - Q[0])
    return float(np.linalg.norm(s) / 2)

def contact(Fa, Fb, t):
    """face contact between piece a (facets Fa) and piece b translated by t: list of (area in unit triangles) per plane"""
    out = []
    for n, c, pts in Fa:
        m = tuple(-x for x in n)
        for n2, c2, pts2 in Fb:
            if n2 != m: continue
            c2t = c2 + n2[0] * t[0] + n2[1] * t[1]
            if c2t != -c: continue
            P, k, ax = poly2(n, pts); Q, _, _ = poly2(n, shift(pts2, t))
            R = inter2(P, Q)
            if R and area2(R) != 0: out.append(real_area(n, R, k, ax, c) / TRI)
    return sum(out)

def bbox(X): return [min(p[r] for p in X) for r in range(3)], [max(p[r] for p in X) for r in range(3)]

def canon(pieces):
    """canonical form of a set of pieces up to lattice symmetry, z-flip and lattice-free translation (any rational shift)"""
    best = None
    for (a, b, c, d), fl in itertools.product(SYM, (1, -1)):
        Y = [[(a * p[0] + b * p[1], c * p[0] + d * p[1], fl * p[2]) for p in X] for X in pieces]
        o = min(p for X in Y for p in X)
        key = tuple(sorted(tuple(sorted(E.sub(p, o) for p in X)) for X in Y))
        if best is None or key < best: best = key
    return best

def sym_order(pieces):
    """number of motions (lattice symmetry x z-flip, then translation) carrying the union's piece set onto itself"""
    ref = None; cnt = 0
    for (a, b, c, d), fl in itertools.product(SYM, (1, -1)):
        Y = [[(a * p[0] + b * p[1], c * p[0] + d * p[1], fl * p[2]) for p in X] for X in pieces]
        o = min(p for X in Y for p in X)
        key = tuple(sorted(tuple(sorted(E.sub(p, o) for p in X)) for X in Y))
        if ref is None: ref = key
        cnt += key == ref
    return cnt

def analyse(pieces, cont):
    faces = E.union_faces(pieces)
    segs, bad = E.edge_multiplicity(faces)
    vol6 = E.volume6(faces); pv6 = sum(E.piece_volume6(X) for X in pieces)
    pts = np.array([cart(p) for X in pieces for p in X]); hull = ConvexHull(pts)
    vol = float(abs(vol6)) / 6 * (math.sqrt(3) / 2) * D
    sizes = sorted(len(f['loops'][0]) for f in faces)
    holes = sum(len(f['loops']) - 1 for f in faces)
    n = len(pieces); neck = None
    for r in range(1, n):
        for S in itertools.combinations(range(n), r):
            if 0 not in S: continue
            s = sum(cont.get((i, j), 0) for i in S for j in range(n) if j not in S)
            neck = s if neck is None else min(neck, s)
    zs = pts[:, 2]; ext = pts.max(0) - pts.min(0)
    return dict(faces=len(faces), sizes=sizes, holes=holes, manifold=not bad, vol_ok=abs(vol6) == pv6,
                volume=vol, hull_ratio=vol / hull.volume, convex=abs(vol / hull.volume - 1) < 1e-9,
                neck=neck, extent=[float(x) for x in ext], sym=sym_order(pieces))

def run(lam, t):
    w, L = {'c': ('ABC', 1), 'h': ('AB', 0)}[t]
    P = [p[3] for p in tile(w, L, lam)[0]]
    kinds = [f"{p[0]}{'' if p[1] is None else ('-top' if p[1] else '-bottom')}" for p in tile(w, L, lam)[0]]
    r = run_pieces(P); r.update(lam=str(lam), tile=t, pieces=kinds); return r

def run_pieces(P):
    n = len(P); F = [E.facets(X) for X in P]; BB = [bbox(X) for X in P]
    R = range(-2 * W, 2 * W + 1)
    C = {}                                 # (i, j, d) -> area of contact of piece i with piece j shifted by d
    for i, j in itertools.combinations(range(n), 2):
        for d in itertools.product(R, R):
            lo1, hi1 = BB[i]; lo2, hi2 = BB[j]
            if any(lo2[r] + (d[r] if r < 2 else 0) > hi1[r] or hi2[r] + (d[r] if r < 2 else 0) < lo1[r] for r in range(3)): continue
            a = contact(F[i], F[j], d)
            if a > 0: C[(i, j, d)] = a
    T = list(itertools.product(range(-W, W + 1), repeat=2))
    classes = {}
    for ch in itertools.product(T, repeat=n - 1):
        tr = [(0, 0)] + list(ch)
        cont = {}
        for i, j in itertools.combinations(range(n), 2):
            d = (tr[j][0] - tr[i][0], tr[j][1] - tr[i][1]); a = C.get((i, j, d))
            if a: cont[(i, j)] = cont[(j, i)] = a
        seen = {0}; st = [0]
        while st:
            x = st.pop()
            for y in range(n):
                if y not in seen and (x, y) in cont: seen.add(y); st.append(y)
        if len(seen) < n: continue
        pcs = [shift(P[i], tr[i]) for i in range(n)]
        key = canon(pcs)
        if key not in classes: classes[key] = dict(tr=tr, cont=cont, count=0)
        classes[key]['count'] += 1
    out = []
    for key, v in classes.items():
        pcs = [shift(P[i], v['tr'][i]) for i in range(n)]
        a = analyse(pcs, v['cont']); a.update(translates=[list(map(int, x)) for x in v['tr']], choices=v['count'],
                                              contacts={f'{i}-{j}': round(x, 6) for (i, j), x in v['cont'].items() if i < j})
        out.append(a)
    out.sort(key=lambda a: (not a['manifold'], a['faces'], -a['hull_ratio']))
    return dict(n_pieces=n, connected_choices=sum(v['count'] for v in classes.values()),
                total_choices=len(T) ** (n - 1), classes=out)

if __name__ == '__main__':
    os.makedirs(os.path.join(HERE, 'data'), exist_ok=True)
    for s in sys.argv[1:]:
        lam = Fr(s); res = {t: run(lam, t) for t in 'ch'}
        fn = os.path.join(HERE, f"data/conn_{s.replace('/', '_')}.json"); json.dump(res, open(fn, 'w'), indent=1)
        for t in 'ch':
            r = res[t]; good = [a for a in r['classes'] if a['manifold']]
            best = good[0] if good else None
            print(f"λ={s} {t}: {r['connected_choices']}/{r['total_choices']} connected, {len(r['classes'])} classes, "
                  f"{len(good)} manifold; best: " + (f"{best['faces']} faces {best['sizes']} hull {best['hull_ratio']:.4f} "
                  f"neck {best['neck']:.3f} sym {best['sym']} tr {best['translates']}" if best else '-'), flush=True)
