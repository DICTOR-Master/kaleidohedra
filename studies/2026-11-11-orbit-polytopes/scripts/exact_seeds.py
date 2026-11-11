"""Exact seed labels (DICTO 11 Nov: "go on with the exact labels and Dogstar check"). For each orbit polytope: the simple roots of its
reflection group, put in Coxeter-chain order (end to end along the graph), the corner's labels in that order, scaled so the smallest
nonzero label is 1, recognised exactly in Q(sqrt2, sqrt5); then PROOF of exactness: the orbit of the exact seed (the point whose inner
products with the simple roots are the exact labels times one scale) is rebuilt with the group and compared with the corners (1e-9).
For a non-convex solid: its corners split into kinds (orbits of its full symmetry group), counted with their distances from the centre."""
import itertools, json, sys
import numpy as np, sympy as sp
from scipy.spatial import cKDTree
sys.argv_saved = sys.argv; sys.argv = ['x', 'none']
exec(open('orbit4d.py').read().split("if __name__ == '__main__':")[0])
sys.argv = sys.argv_saved
SQ = [sp.sqrt(2), sp.sqrt(5)]
def chamber_and_roots(V, mats):
    d = V.shape[1]; R = []
    for M in mats:
        if np.allclose(M, M.T, atol=1e-7) and np.isclose(np.linalg.det(M), -1):
            ev, vec = np.linalg.eigh(M)
            if np.sum(np.isclose(ev, -1, atol=1e-6)) == 1: R.append(vec[:, np.argmin(ev)])
    Rs = []
    for r in R:
        r = r / np.linalg.norm(r)
        if not any(abs(abs(r @ s) - 1) < 1e-6 for s in Rs): Rs.append(r)
    p = np.array([1.0, 0.31, 0.073, 0.0119][:d]) + 1e-3; Rs = [r if r @ p > 0 else -r for r in Rs]
    x = V[0].copy()
    for _ in range(1000):
        bad = [r for r in Rs if r @ x < -1e-9]
        if not bad: break
        x = x - 2 * (bad[0] @ x) * bad[0]
    # simple roots: the positive roots that are not a non-negative combination of the other positive roots (robust, no chamber LP)
    from scipy.optimize import nnls
    simple = []
    for r in Rs:
        A = np.array([s for s in Rs if not np.allclose(s, r)]).T
        coef, res = nnls(A, r)
        if res > 1e-6: simple.append(r)
    assert len(simple) == d, f'{len(simple)} simple roots in dimension {d}'
    return x, simple, Rs
def chain_order(simple):
    n = len(simple); m = [[round(np.pi / np.arccos(min(1, abs(a @ b)))) if i != j else 1 for j, b in enumerate(simple)] for i, a in enumerate(simple)]
    adjl = {i: [j for j in range(n) if j != i and m[i][j] > 2] for i in range(n)}
    ends = [i for i in range(n) if len(adjl[i]) <= 1]
    # start at the end carrying the largest bond (5 or 4), else any end
    start = max(ends, key=lambda i: max([m[i][j] for j in adjl[i]] or [0]))
    order = [start]
    while len(order) < n:
        nxt = [j for j in adjl[order[-1]] if j not in order]
        if not nxt: order += [j for j in range(n) if j not in order]; break
        order.append(nxt[0])
    bonds = [m[order[k]][order[k + 1]] for k in range(n - 1)]
    return order, bonds
def recognise(v):
    for c in [sp.nsimplify(v, SQ, tolerance=1e-9, rational=False)]:
        if abs(float(c) - v) < 1e-9 and len(str(c)) < 40: return sp.radsimp(c)
    return None
def exact_seed(name, V):
    V = np.array(V, float); V = V - V.mean(0); mats = sym_group(V)
    x, simple, Rs = chamber_and_roots(V, mats); order, bonds = chain_order(simple)
    lab = np.array([simple[i] @ x for i in order]); nz = lab[np.abs(lab) > 1e-9]
    if not len(nz): return {'name': name, 'error': 'no labels'}
    sc = nz.min(); rel = lab / sc
    ex = [sp.Integer(0) if abs(v) < 1e-9 else recognise(float(v)) for v in rel]
    ok = all(e is not None for e in ex)
    proof = False
    if ok:
        A = np.array([simple[i] for i in order]); xs = np.linalg.solve(A, np.array([float(e) for e in ex]) * sc)
        S = [np.eye(len(x)) - 2 * np.outer(r, r) for r in Rs]; t = cKDTree(V); orb = [xs]; seen = {tuple(np.round(xs, 7))}; fr = [xs]
        while fr:
            nf = []
            for y in fr:
                for M in S:
                    z = M @ y; k = tuple(np.round(z, 7))
                    if k not in seen: seen.add(k); orb.append(z); nf.append(z)
            fr = nf
        orb = np.array(orb); proof = len(orb) == len(V) and np.all(t.query(orb)[0] < 1e-8)
    rec = {'name': name, 'chain_bonds': bonds, 'labels_exact': [str(e) for e in ex], 'rebuilt_from_exact_seed': bool(proof)}
    print(f"{name}: chain {'-'.join(map(str, bonds))}, seed ({', '.join(map(str, ex))}) {'PROOF: orbit of the exact seed = the corners' if proof else 'NOT confirmed'}", flush=True)
    return rec
def kinds(name, V):
    V = np.array(V, float); V = V - V.mean(0); mats = sym_group(V); t = cKDTree(V)
    seen = set(); orbits = []
    for i in range(len(V)):
        if i in seen: continue
        o = {int(t.query(M @ V[i])[1]) for M in mats}; seen |= o; orbits.append((len(o), round(float(np.linalg.norm(V[i])), 5)))
    print(f'{name}: {len(V)} corners, symmetry group {len(mats)}, {len(orbits)} kinds of corner (size, distance): {sorted(orbits, key=lambda z: z[1])}', flush=True)
    return {'name': name, 'sym': len(mats), 'kinds': orbits}
if __name__ == '__main__':
    out = {'seeds': [], 'kinds': []}
    S = {s['id']: s for s in json.load(open('solids.json'))}
    tau = (1 + 5 ** .5) / 2
    def T(x): return sorted({tuple(s * c for s, c in zip(sg, p)) for p in itertools.permutations((1 + x, x, 0)) for sg in itertools.product((1, -1), repeat=3)})
    items = [('Kelvin T(1)', T(1)), ('DICTO 1:2 = T(1/2)', T(0.5)), ('DICTO 2:1 = T(2)', T(2.0))]
    for k in ['DICTO_ICOSAXES', 'DICTO_UNBORN_AXES', 'DICTO_DELILAH']: items.append((S[k]['name'], np.unique(np.round(np.array(S[k]['corners'], float), 9), axis=0)))
    items.append(('4D permutohedron', perm4()))
    exec(open('stages.py').read().split('keys = ')[0])
    V6 = V.copy(); adj = {i: set(j for j in range(120) if abs(D[i, j] - e0) < 1e-9) for i in range(120)}
    E = [(i, j) for i in range(120) for j in adj[i] if j > i]; Tr = [(i, j, k) for i, j in E for k in adj[i] & adj[j] if k > j]
    C = [(i, j, k, l) for i, j, k in Tr for l in adj[i] & adj[j] & adj[k] if l > k]; cen = lambda q: V6[list(q)].mean(0)
    s_ = (5 - 5 ** .5) / 10; byf = {}
    for ci, c in enumerate(C):
        for f in itertools.combinations(sorted(c), 3): byf.setdefault(f, []).append(ci)
    items += [('600-cell', V6), ('truncated 600-cell', np.array([(2 * V6[a] + V6[b]) / 3 for a in range(120) for b in adj[a]])),
              ('bitruncated 600-cell', np.array([0.4 * (V6[a] + V6[b]) / 2 + 0.6 * cen(t) for t in Tr for a, b in itertools.combinations(t, 2)])),
              ('truncated 120-cell', np.array([(1 - s_) * cen(C[a]) + s_ * cen(C[b]) for f, (a, b) in byf.items() for (a, b) in [(a, b), (b, a)]])),
              ('120-cell', np.array([cen(c) for c in C]))]
    for name, Vx in items: out['seeds'].append(exact_seed(name, Vx))
    for k in ['DOGSTAR', 'DICTO_HEXA_KEY', 'DICTO_LOTUS_JEWEL_AXES', 'DICTO_DODECA13']:
        out['kinds'].append(kinds(S[k]['name'], np.unique(np.round(np.array(S[k]['corners'], float), 9), axis=0)))
    json.dump(out, open('exact_seeds.json', 'w'), indent=1, default=str)
    ok = all(r.get('rebuilt_from_exact_seed') for r in out['seeds'])
    print('FINAL ok' if ok else 'FINAL FAIL (a seed not confirmed)')
