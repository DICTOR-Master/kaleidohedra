"""Step 9b: for every F4 (polytope, direction) whose section has the golden-cut-RD signature {3: 8, 4: 6, 8: 12} (s9), follow
the section over its whole stage: square side s(h), triangle side t(h), octagon-octagon side b(h). A golden cut RD needs
s = t (= a, all corner sides equal) AND b/a = phi or 1/phi at the same h. Floating point scan (2000 heights per stage) with
root bracketing; the nearest approach is reported.
usage: python3 s9b_rhombic_ratios.py F4|H4 -> ../data/s9b-rhombic-ratios-<g>.json
(H4: golden cut RT, signature {3: 20, 5: 12, 8: 30}, needs triangle side = pentagon side = a and b/a = phi^+-1.)
"""
import json, os, itertools, numpy as np
from scipy.spatial import ConvexHull, cKDTree
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, '..', 'data')
import importlib.util, sys
G = (1 + 5 ** .5) / 2
S = np.array([[0, 1, -1, 0], [0, 0, 1, -1], [0, 0, 0, 1], [.5, -.5, -.5, -.5]], float)
def refl(v, a): return v - 2 * (v @ a) / (a @ a) * a
def orbit(p):
    pts = {tuple(np.round(p, 9)): p}; fr = [p]
    while fr:
        nf = []
        for q in fr:
            for a in S:
                r = refl(q, a); k = tuple(np.round(r, 9))
                if k not in pts: pts[k] = r; nf.append(r)
        fr = nf
    return np.array(list(pts.values()))
grp = sys.argv[1]
hits = json.load(open(os.path.join(DATA, f's9-golden-rhombic-{grp}.json')))['hits']
Q4 = 4 if grp == 'F4' else 5
NT = {3: 8, 4: 6, 8: 12} if grp == 'F4' else {3: 20, 5: 12, 8: 30}
if grp == 'H4':
    import itertools as it
    from scipy.optimize import nnls
    V6 = [np.eye(4)[i] * s_ for i in range(4) for s_ in (1, -1)] + [np.array(x) / 2 for x in it.product((1, -1), repeat=4)]
    base = np.array([G / 2, .5, 1 / (2 * G), 0])
    ev = [p for p in it.permutations(range(4)) if sum(1 for a in range(4) for b in range(a + 1, 4) if p[a] > p[b]) % 2 == 0]
    for p in ev:
        for s_ in it.product((1, -1), repeat=4):
            v = np.array([base[p[i]] * s_[i] for i in range(4)])
            if not any(np.allclose(v, w) for w in V6): V6.append(v)
    R = np.array(V6); f = np.array([1, 0.1, 0.01, 0.001]); pos = R[R @ f > 0]
    S = np.array([r for i, r in enumerate(pos) if nnls(np.delete(pos, i, axis=0).T, r)[1] > 1e-9])
    dirs = {'600-cell corner direction (H3)': np.array([1, 0, 0, 0.])}
dirs = {'e1 (root, B3)': np.array([1, 0, 0, 0.]), '(1,1,0,0) (root, B3)': np.array([1, 1, 0, 0.]) / 2 ** .5, '(1,1,1,1)/2 (root, B3)': np.array([1, 1, 1, 1.]) / 2}
if grp == 'H4': dirs = {'600-cell corner direction (H3)': np.array([1, 0, 0, 0.])}
def section(V, E, dv, h, B):
    hv = V @ dv; a, b = hv[E[:, 0]], hv[E[:, 1]]; m = (a - h) * (b - h) < 0
    t = (h - a[m]) / (b[m] - a[m]); P = V[E[m, 0]] + t[:, None] * (V[E[m, 1]] - V[E[m, 0]]); Q = P @ B.T
    Q = Q[np.unique(np.round(Q, 9), axis=0, return_index=True)[1]]
    hl = ConvexHull(Q); groups = {}
    for eq, s in zip(np.round(hl.equations, 6), hl.simplices): groups.setdefault(tuple(eq), set()).update(s)
    faces = []
    for eq, g in groups.items():
        g = list(g); c = Q[g].mean(0); n = np.array(eq[:3]); u = Q[g[0]] - c; u /= np.linalg.norm(u); w = np.cross(n, u)
        g.sort(key=lambda i: np.arctan2((Q[i] - c) @ w, (Q[i] - c) @ u)); faces.append(g)
    return Q, faces
out = []
for hrec in hits:
    rings = tuple(hrec['rings']); p = np.linalg.solve(S, np.array(rings, float)); V = orbit(p)
    d = cKDTree(V).query(V, k=2)[0][:, 1].min(); E = np.array(list(cKDTree(V).query_pairs(d * (1 + 1e-7))))
    dv = dirs[hrec['direction']]; dv = dv / np.linalg.norm(dv); B = np.linalg.svd(dv[None])[2][1:]
    hmax = (V @ dv).max(); rows = []
    for h in np.linspace(1e-6, hmax - 1e-6, 2000 if grp == 'F4' else 400):
        try: Q, F = section(V, E, dv, h, B)
        except Exception: continue
        sig = sorted(len(f) for f in F)
        if any(sig.count(k) != v for k, v in NT.items()) or len(F) != sum(NT.values()): continue
        L = lambda f: [np.linalg.norm(Q[f[i]] - Q[f[(i + 1) % len(f)]]) for i in range(len(f))]
        s = np.mean([np.mean(L(f)) for f in F if len(f) == Q4]); t = np.mean([np.mean(L(f)) for f in F if len(f) == 3])
        oc = [f for f in F if len(f) == 8][0]; ls = L(oc)
        corner = set()
        for f in F:
            if len(f) in (3, Q4):
                for i in range(len(f)): corner.add(frozenset((f[i], f[(i + 1) % len(f)])))
        bs = [l for i, l in enumerate(ls) if frozenset((oc[i], oc[(i + 1) % 8])) not in corner]
        b = np.mean(bs) if bs else float('nan')
        rows.append((h, s, t, b))
    if not rows: continue
    R = np.array(rows)
    st = R[:, 1] - R[:, 2]; idx = np.where(np.sign(st[:-1]) != np.sign(st[1:]))[0]
    eq_pts = [{'h': float(R[i, 0]), 'b_over_a': float(R[i, 3] / R[i, 1])} for i in idx]
    near = min(abs(np.log(R[:, 3] / R[:, 1]) - s_ * np.log(G)).min() for s_ in (1, -1))
    rec = {'rings': rings, 'direction': hrec['direction'], 'stage_h': [float(R[0, 0]), float(R[-1, 0])],
           's_minus_t_range': [float(st.min()), float(st.max())], 'points_s_eq_t': eq_pts,
           'b_over_s_range': [float((R[:, 3] / R[:, 1]).min()), float((R[:, 3] / R[:, 1]).max())],
           'b_over_t_range': [float((R[:, 3] / R[:, 2]).min()), float((R[:, 3] / R[:, 2]).max())]}
    out.append(rec); print(rec, flush=True)
golden = [r for r in out for e in r['points_s_eq_t'] if min(abs(e['b_over_a'] - G), abs(e['b_over_a'] - 1 / G)) < 1e-3]
json.dump({'stages': out, 'golden_candidates': golden}, open(os.path.join(DATA, f's9b-rhombic-ratios-{grp}.json'), 'w'), indent=1)
print('golden candidates (s = t and b/a = phi^+-1 within 1e-3):', len(golden))
