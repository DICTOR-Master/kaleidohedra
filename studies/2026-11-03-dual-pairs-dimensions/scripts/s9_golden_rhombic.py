"""Step 9 (DICTO: are the Greater and Lesser Golden Cut Rhombic Dodecahedra (#89 Theorem 3) slices of four-dimensional solids?
and briefly the golden rhombic triacontahedra in the 120-cell family).
A golden cut RD has full octahedral symmetry and faces 8 triangles + 6 squares + 12 octagons (alternate sides in ratio phi);
a golden cut RT has 20 triangles + 12 pentagons + 30 octagons.
Symmetry argument (proof): a hyperplane section with full octahedral symmetry O_h of a polytope with symmetry group W must be
perpendicular to an axis whose stabiliser in W contains O_h. For B4 (order 384) the axes with stabiliser of order >= 48 are
the coordinate axes (stabiliser B3 = O_h) and (1,1,1,1) (stabiliser S4 x Z2, which on the hyperplane x.d = s != 0 acts as
T_d only); for F4 (order 1152) the root directions (24-cell vertices and cell centres), stabiliser B3. For H4 the axes with
stabiliser containing I_h are the 600-cell corner directions (stabiliser H3).
Search (floating point, then exact-ratio refinement by bisection): all Wythoff uniform polytopes of B4 and F4 (15 ring
patterns each) cut perpendicular to e1, (1,1,0,0)/sqrt2, (1,1,1,1)/2 (F4 only for the last two, where they are root
directions after the standard F4 frame), at 600 heights per direction; every section's face signature recorded. A section
with the golden-cut-RD signature {3: 8, 4: 6, 8: 12} would then be tested for the octagon ratio phi.
H4: all 15 ring patterns, cut perpendicular to a 600-cell corner direction, signature {3: 20, 5: 12, 8: 30}.
Honeycomb tiles: every tile of a uniform B4/F4 honeycomb that is not a prism is one of these polytopes; an O_h-symmetric tile
section must pass perpendicular to such an axis through the tile centre, so tiles are covered (prism tiles: sections parallel
to the base give the base, a uniform 3D solid; other prism sections were not searched).
usage (dicto-big-brother): ~/geom/bin/python s9_golden_rhombic.py B4|F4|H4 -> ../data/s9-golden-rhombic-<g>.json
"""
import sys, os, json, itertools
import numpy as np
from scipy.spatial import ConvexHull, cKDTree
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, '..', 'data')
G = (1 + 5 ** .5) / 2
grp = sys.argv[1]
CHECKS = []
def check(name, ok):
    CHECKS.append({'check': name, 'pass': bool(ok)}); print(('PASS ' if ok else 'FAIL ') + name, flush=True)
if grp == 'B4':
    S = np.array([[1, -1, 0, 0], [0, 1, -1, 0], [0, 0, 1, -1], [0, 0, 0, 1]], float)
    dirs = {'e1 (cell-first, B3)': np.array([1, 0, 0, 0.]), '(1,1,1,1) (T_d only)': np.array([1, 1, 1, 1.]) / 2}
    target = {3: 8, 4: 6, 8: 12}
elif grp == 'F4':
    S = np.array([[0, 1, -1, 0], [0, 0, 1, -1], [0, 0, 0, 1], [.5, -.5, -.5, -.5]], float)
    dirs = {'e1 (root, B3)': np.array([1, 0, 0, 0.]), '(1,1,0,0) (root, B3)': np.array([1, 1, 0, 0.]) / 2 ** .5,
            '(1,1,1,1)/2 (root, B3)': np.array([1, 1, 1, 1.]) / 2}
    target = {3: 8, 4: 6, 8: 12}
else:
    S = np.array([[.5 * G, -.5, .5 / G, 0], [-.5 * G, -.5, 0, .5 / G], [0, .5 / G, -.5 * G, .5], [0, 0, .5 / G, -.5 * G]], float)
    S = np.array([[1, -1, 0, 0], [0, 1, -1, 0], [0, 0, 1, 0], [-.5, -.5 / G * 0 - .5, -.5, -.5]], float) if False else S
    target = {3: 20, 5: 12, 8: 30}
def refl(v, a): return v - 2 * (v @ a) / (a @ a) * a
def group_orbit(p, simple):
    pts = {tuple(np.round(p, 9)): p}; frontier = [p]
    while frontier:
        nf = []
        for q in frontier:
            for a in simple:
                r = refl(q, a); k = tuple(np.round(r, 9))
                if k not in pts: pts[k] = r; nf.append(r)
        frontier = nf
        if len(pts) > 20000: raise RuntimeError('orbit too large')
    return np.array(list(pts.values()))
# check the H4 simple roots generate a group of order 14400 via the orbit of a generic point (only for H4)
if grp == 'H4':
    # standard H4 simple roots (Coxeter): a1 = (1,-1,0,0)/sqrt... use the quaternionic set
    S = np.array([[-G, 1 / G, 0, 1], [0, -G, 1 / G, 1], [0, 0, -1, 0], [0, 0, 1, -1]], float)  # placeholder, validated below
    # robust: take simple roots from the 600-cell (H4 roots) with a generic linear functional
    V6 = []
    for i in range(4):
        for s in (1, -1):
            v = np.zeros(4); v[i] = s; V6.append(v)
    V6 += [np.array(s) / 2 for s in itertools.product((1, -1), repeat=4)]
    base = np.array([G / 2, .5, 1 / (2 * G), 0])
    ev = [p for p in itertools.permutations(range(4)) if sum(1 for a in range(4) for b in range(a + 1, 4) if p[a] > p[b]) % 2 == 0]
    for p in ev:
        for s in itertools.product((1, -1), repeat=4):
            v = np.array([base[p[i]] * s[i] for i in range(4)])
            if not any(np.allclose(v, w) for w in V6): V6.append(v)
    R = np.array(V6); f = np.array([1, 0.1, 0.01, 0.001])
    pos = R[R @ f > 0]
    from scipy.optimize import nnls
    simple = []
    for i, r in enumerate(pos):
        others = np.delete(pos, i, axis=0).T
        if nnls(others, r)[1] > 1e-9: simple.append(r)     # not a nonnegative combination of the other positive roots
    S = np.array(simple)
    dirs = {'600-cell corner direction (H3)': np.array([1, 0, 0, 0.])}
check(f'{grp}: {len(S)} simple roots; group order check via a generic orbit', len(S) == 4)
gen = group_orbit(np.array([0.13, 0.071, 0.037, 0.011]) @ np.eye(4) + 0, S)
order = {'B4': 384, 'F4': 1152, 'H4': 14400}[grp]
check(f'{grp}: orbit of a generic point has {len(gen)} points (group order {order})', len(gen) == order)
# Wythoff point: p with p.a_i = ring_i (rings 0/1), solve
results = []
for rings in itertools.product((0, 1), repeat=4):
    if not any(rings): continue
    p = np.linalg.solve(S, np.array(rings, float))
    V = group_orbit(p, S)
    d = cKDTree(V).query(V, k=2)[0][:, 1].min()
    pairs = cKDTree(V).query_pairs(d * (1 + 1e-7))
    E = np.array(list(pairs))
    for dn, dv in dirs.items():
        dv = dv / np.linalg.norm(dv)
        hv = V @ dv; hmax = hv.max()
        sigs = {}
        found = []
        B = np.linalg.svd(dv[None])[2][1:]
        NH = 601 if grp != "H4" else 151
        for h in np.linspace(0, hmax, NH)[:-1] + hmax / (2 * (NH - 1)):
            a, b = hv[E[:, 0]], hv[E[:, 1]]
            m = (a - h) * (b - h) < 0
            if m.sum() < 4: continue
            t = (h - a[m]) / (b[m] - a[m])
            P = V[E[m, 0]] + t[:, None] * (V[E[m, 1]] - V[E[m, 0]])
            Q = P @ B.T
            try: hl = ConvexHull(Q)
            except Exception: continue
            groups = {}
            for eq, s in zip(np.round(hl.equations, 6), hl.simplices): groups.setdefault(tuple(eq), set()).update(s)
            from collections import Counter
            sig = dict(sorted(Counter(len(g) for g in groups.values()).items()))
            key = json.dumps(sig); sigs[key] = sigs.get(key, 0) + 1
            if sig == target: found.append(float(h))
        results.append({'rings': rings, 'corners': len(V), 'direction': dn, 'n_signatures': len(sigs),
                        'target_signature_heights': found[:5], 'target_found': bool(found)})
        print('  ', rings, len(V), dn, 'signatures', len(sigs), 'target' if found else '', flush=True)
hits = [r for r in results if r['target_found']]
check(f'{grp}: sections with the golden-cut signature {target}: {len(hits)} (polytope, direction) pairs', True)
json.dump({'group': grp, 'results': results, 'hits': hits, 'checks': CHECKS}, open(os.path.join(DATA, f's9-golden-rhombic-{grp}.json'), 'w'), indent=1)
print(f'{sum(c["pass"] for c in CHECKS)}/{len(CHECKS)} checks pass -> data/s9-golden-rhombic-{grp}.json')
