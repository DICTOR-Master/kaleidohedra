"""Chapter 11 of the Platonic book (DICTO 11 Nov: "one book"): the residents of the 600-cell and the 120-cell, EXACT.
The 600-cell's 120 corners in exact coordinates over Q(sqrt5) (the 8 + 16 + 96 standard ones); the 120-cell's 600 corners as the
centres of the 600-cell's cells (exact). Through corner 0 every candidate Platonic solid found by the float search (inhabitance.py's
hidden()) is matched to exact corners and kept only if, in exact arithmetic, all its corners are corners and its squared distances
are exactly those of the regular solid (each distance class in the right number). Count = (solids through corner 0) x V / k.
Controls: 600-cell cells 600 T; 120-cell cells 120 D."""
import sys, itertools, json
import numpy as np, sympy as sp
from scipy.spatial import cKDTree
sys.argv = ['x', 'H4']
exec(open('inhabitance.py').read().split('res = {}; t00')[0])
r5 = sp.sqrt(5); ph = (1 + r5) / 2
def v600():
    V = []
    for i in range(4):
        for s in (1, -1):
            e = [sp.Integer(0)] * 4; e[i] = sp.Integer(s * 2); V.append(e)
    for s in itertools.product((1, -1), repeat=4): V.append([sp.Integer(c) for c in s])
    evens = [p for p in itertools.permutations(range(4)) if sum(1 for a in range(4) for b in range(a + 1, 4) if p[a] > p[b]) % 2 == 0]
    for p in evens:
        for s in itertools.product((1, -1), repeat=3):
            base = [s[0] * ph, s[1] * 1, s[2] / ph, 0]
            v = [sp.Integer(0)] * 4
            for i in range(4): v[p[i]] = base[i]
            V.append(v)
    V = [[sp.radsimp(sp.sympify(c)) for c in v] for v in V]
    U = {tuple(sp.radsimp(c) for c in v) for v in V}
    return [list(u) for u in U]
VX = v600(); assert len(VX) == 120, len(VX)
def sq(a, b): return sp.radsimp(sum((x - y) ** 2 for x, y in zip(a, b)))
def canon_exact():
    T = [[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]]
    C = [list(t) for t in itertools.product((1, -1), repeat=3)]
    O = [[s * (1 if k == i else 0) for k in range(3)] for i in range(3) for s in (1, -1)]
    I = [[0, a, b * ph][-c:] + [0, a, b * ph][:-c] if c else [0, a, b * ph] for c in range(3) for a in (1, -1) for b in (1, -1)]
    Dd = C + [[0, a / ph, b * ph][-c:] + [0, a / ph, b * ph][:-c] if c else [0, a / ph, b * ph] for c in range(3) for a in (1, -1) for b in (1, -1)]
    out = {}
    for name, S in (('D', Dd), ('I', I), ('C', C), ('T', T), ('O', O)):
        S = [[sp.sympify(x) for x in v] for v in S]; d2 = [sq(a, b) for a, b in itertools.combinations(S, 2)]
        e2 = min(d2, key=lambda z: float(z)); out[name] = sorted((sp.radsimp(x / e2) for x in d2), key=lambda z: float(z))
    return out
CANX = canon_exact()
def exact_check(EX, S, name):
    Q = [EX[i] for i in S]; d2 = [sq(a, b) for a, b in itertools.combinations(Q, 2)]
    e2 = min(d2, key=lambda z: float(z)); got = sorted((sp.radsimp(x / e2) for x in d2), key=lambda z: float(z))
    return len(got) == len(CANX[name]) and all(sp.simplify(a - b) == 0 for a, b in zip(got, CANX[name]))
out = {}
for poly in ('600-cell', '120-cell'):
    if poly == '600-cell': EX = VX
    else:   # 120-cell corners = centres of the 600-cell's 600 tetrahedra (exact)
        Pf = np.array([[float(c) for c in v] for v in VX]); D = np.linalg.norm(Pf[:, None] - Pf[None], axis=2); e = D[D > 1e-9].min()
        adj = [set(np.where(np.abs(D[i] - e) < 1e-9)[0]) for i in range(120)]
        tets = {frozenset((a, b, c, d)) for a in range(120) for b in adj[a] for c in adj[a] & adj[b] for d in adj[a] & adj[b] & adj[c]}
        EX = [[sp.radsimp(sum(VX[i][k] for i in t) / 4) for k in range(4)] for t in tets]
    P = np.array([[float(c) for c in v] for v in EX]); V = len(P); tree = cKDTree(P)
    H = hidden(P, tree); res = {}
    for name in ('D', 'I', 'C', 'T', 'O'):
        sols = H[name]; good = [S for S in sols if exact_check(EX, S, name)]
        res[name] = {'through_corner': len(sols), 'exact': len(good), 'total': len(good) * V // CAN[name]['k']}
        print(f"{poly}: {name} through corner 0 {len(sols)}, exact {len(good)} -> total {res[name]['total']}", flush=True)
    out[poly] = res
json.dump(out, open('residents_exact.json', 'w'), indent=1)
ok = out['600-cell']['T']['total'] >= 600 and out['120-cell']['D']['total'] >= 120 and all(r[n]['exact'] == r[n]['through_corner'] for r in out.values() for n in r)
print('FINAL ok' if ok else 'FINAL FAIL')
