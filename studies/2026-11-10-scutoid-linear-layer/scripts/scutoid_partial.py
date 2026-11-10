"""Partial scutoid move on the truncated icosahedron shell (DICTO 10 Nov: "whether a more irregular solid might form"). Only a SUBSET
of the 30 hexagon-hexagon edges shrink to a point (middle) and reopen across (outer). LP (linear): every middle edge parallel to its
core edge, every outer edge parallel to the core edge it came from -> every side face a flat trapezoid / triangle, and every top
polygon flat (all its edges parallel to its core face's plane). Objective: stay close to the radial scalings 1.18 (middle), 1.42
(outer). Checks: flatness, every cell volume > 0, sum = V(inside the outer surface) - V(TI), outer surface faces = 32.
Usage: python scutoid_partial.py all|six|one|<k random>"""
import sys, itertools, json, numpy as np
from scipy.optimize import linprog
from scipy.spatial import ConvexHull
phi = (1 + 5 ** .5) / 2
def evenperm(v):
    return np.unique(np.round(np.array([(s0 * v[a], s1 * v[b], s2 * v[c]) for a, b, c in [(0, 1, 2), (1, 2, 0), (2, 0, 1)]
                                        for s0, s1, s2 in itertools.product([1, -1], repeat=3)], float), 12), axis=0)
P = np.vstack([evenperm((0, 1, 3 * phi)), evenperm((1, 2 + phi, 2 * phi)), evenperm((phi, 2, phi ** 3))]); P /= np.linalg.norm(P[0]); n = 60
h = ConvexHull(P); G = {}
for simp, eq in zip(h.simplices, h.equations): G.setdefault(tuple(np.round(eq, 7)), set()).update(simp)
faces = []
for eq, vs in G.items():
    nn = np.array(eq[:3]); vs = list(vs); c = P[vs].mean(0); e1 = P[vs[0]] - c; e1 /= np.linalg.norm(e1); e2 = np.cross(nn, e1)
    vs.sort(key=lambda v: np.arctan2((P[v] - c) @ e2, (P[v] - c) @ e1)); faces.append(vs)
edges = {}
for fi, f in enumerate(faces):
    for k in range(len(f)): edges.setdefault(frozenset((f[k], f[(k + 1) % len(f)])), []).append(fi)
hh = [e for e, fs in edges.items() if all(len(faces[x]) == 6 for x in fs)]; assert len(hh) == 30
mode = sys.argv[1] if len(sys.argv) > 1 else 'six'
mid = lambda e: P[list(e)].mean(0)
if mode == 'all': C = hh
elif mode == 'six': C = [e for e in hh if np.sum(np.abs(mid(e) / np.linalg.norm(mid(e))) > 0.999) == 1]
elif mode == 'one': C = [max(hh, key=lambda e: mid(e)[2])]
else: rng = np.random.default_rng(int(mode)); C = [hh[i] for i in rng.choice(30, size=int(mode), replace=False)]
print(f'mode {mode}: {len(C)} edges move')
# ---- outer face lists after the T1 moves; source core edge of every outer edge
outer = [list(f) for f in faces]; src = {}
for e in C:
    u, w = tuple(e); A, B = edges[e]
    Cf = next(fi for fi, f in enumerate(faces) if u in f and len(f) == 5); Df = next(fi for fi, f in enumerate(faces) if w in f and len(f) == 5)
    fa = faces[A]; k = fa.index(u); p = fa[(k + 1) % 6] if fa[(k - 1) % 6] == w else fa[(k - 1) % 6]
    fb = faces[B]; k = fb.index(u); q = fb[(k + 1) % 6] if fb[(k - 1) % 6] == w else fb[(k - 1) % 6]
    k = fa.index(w); r = fa[(k + 1) % 6] if fa[(k - 1) % 6] == u else fa[(k - 1) % 6]
    k = fb.index(w); s_ = fb[(k + 1) % 6] if fb[(k - 1) % 6] == u else fb[(k - 1) % 6]
    L = outer[A]; L.remove(w); L = outer[B]; L.remove(u)
    L = outer[Cf]; k = L.index(u); L.insert(k + 1 if L[(k + 1) % len(L)] == q else k, w)
    L = outer[Df]; k = L.index(w); L.insert(k if L[(k - 1) % len(L)] == r else k + 1, u)
    src[frozenset((u, r))] = (w, r); src[frozenset((w, q))] = (u, q); src[frozenset((u, w))] = None
oedges = {}
for fi, f in enumerate(outer):
    for k in range(len(f)): oedges.setdefault(frozenset((f[k], f[(k + 1) % len(f)])), []).append(fi)
assert all(len(v) == 2 for v in oedges.values()), 'outer surface not closed'
# ---- LP: x = [M (3n), O (3n), |M - 1.18P| (3n), |O - 1.42P| (3n), t (edges), s (outer edges)]
Cs = set(C); kept = [e for e in edges if e not in Cs]; oe = list(oedges)
N = 3 * n; nt = len(kept); ns = len(oe); nv = 4 * N + nt + ns
Aeq, beq, Aub, bub = [], [], [], []
def row(): return np.zeros(nv)
for e in Cs:
    a, b = tuple(e)
    for d in range(3): r_ = row(); r_[3 * a + d] = 1; r_[3 * b + d] = -1; Aeq.append(r_); beq.append(0)
for i, e in enumerate(kept):
    a, b = sorted(e); dv = P[b] - P[a]
    for d in range(3): r_ = row(); r_[3 * b + d] = 1; r_[3 * a + d] = -1; r_[4 * N + i] = -dv[d]; Aeq.append(r_); beq.append(0)
for i, e in enumerate(oe):
    a, b = sorted(e); sc = src.get(e, (a, b))
    if sc is None: continue                                   # the new edge: free
    a0, b0 = sc; dv = P[b0] - P[a0]
    # orientation: outer edge a -> b corresponds to core a0 -> b0 where a sits where a0 was (same id) or swapped partner
    same = (a == a0) or (b == b0)
    if not same: dv = -dv
    for d in range(3): r_ = row(); r_[N + 3 * b + d] = 1; r_[N + 3 * a + d] = -1; r_[4 * N + nt + i] = -dv[d]; Aeq.append(r_); beq.append(0)
for k in range(N):
    for blk, tgt, sc in ((0, 2, 1.18), (1, 3, 1.42)):
        r_ = row(); r_[blk * N + k] = 1; r_[tgt * N + k] = -1; Aub.append(r_); bub.append(sc * P.ravel()[k])
        r_ = row(); r_[blk * N + k] = -1; r_[tgt * N + k] = -1; Aub.append(r_); bub.append(-sc * P.ravel()[k])
cost = np.zeros(nv); cost[2 * N:4 * N] = 1
bounds = [(None, None)] * (2 * N) + [(0, None)] * (2 * N) + [(0.25, None)] * nt + [(0.25, None)] * ns
res = linprog(cost, A_ub=np.array(Aub), b_ub=bub, A_eq=np.array(Aeq), b_eq=beq, bounds=bounds, method='highs')
print('LP:', res.message)
M = res.x[:N].reshape(-1, 3); O = res.x[N:2 * N].reshape(-1, 3)
# ---- cells as solids
def svol(V, F): return sum(np.dot(V[f[0]], np.cross(V[f[k]], V[f[k + 1]])) for f in F for k in range(1, len(f) - 1)) / 6
cells, worst, tot = [], 0.0, 0.0
for fi, f in enumerate(faces):
    pts, F = [], []
    def idx(p):
        for q_, v in enumerate(pts):
            if np.allclose(v, p, atol=1e-10): return q_
        pts.append(p); return len(pts) - 1
    F.append([idx(P[u]) for u in f][::-1])
    for k in range(len(f)):
        u, w = f[k], f[(k + 1) % len(f)]; F.append(list(dict.fromkeys([idx(P[u]), idx(P[w]), idx(M[w]), idx(M[u])])))
    g = outer[fi]
    for k in range(len(g)):
        u, w = g[k], g[(k + 1) % len(g)]; F.append(list(dict.fromkeys([idx(M[u]), idx(M[w]), idx(O[w]), idx(O[u])])))
    F.append([idx(O[u]) for u in g])
    V = np.array(pts)
    for ff in F:
        if len(ff) > 3:
            Q = V[ff]; nr = np.cross(Q[1] - Q[0], Q[2] - Q[0]); nr /= np.linalg.norm(nr); worst = max(worst, float(abs((Q - Q[0]) @ nr).max()))
    v = svol(V, F); tot += v; cells.append({'V': V.tolist(), 'F': F, 'kind': f'{len(f)}-{len({tuple(np.round(M[u], 9)) for u in f})}-{len(g)}', 'vol': v})
vin = svol(O, outer); vti = h.volume
from collections import Counter
print('cells:', dict(Counter(c['kind'] for c in cells)))
# distinct shapes up to rotation/reflection: compare sorted pairwise-distance spectra
def spec(c): V = np.array(c['V']); D = np.sort(np.round(np.linalg.norm(V[:, None] - V[None], axis=2).ravel(), 6)); return tuple(D)
print('distinct cell shapes:', len({spec(c) for c in cells}))
print(f'every face flat: {worst:.1e}; volumes {min(c["vol"] for c in cells):.4f} .. {max(c["vol"] for c in cells):.4f}; sum {tot:.10f}; V(outer) - V(TI) {vin - vti:.10f}')
json.dump(cells, open(f'scutoid-partial-{mode}.json', 'w'))
print('FINAL ok' if res.status == 0 and worst < 1e-8 and min(c['vol'] for c in cells) > 0 and abs(tot - (vin - vti)) < 1e-8 else 'FINAL FAIL')
