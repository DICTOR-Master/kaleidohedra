#!/usr/bin/env python3
"""Best twin pattern of the Admiral Cap network (frustrated Ising model): each octahedron c of the octet takes golden twin t_c in {0,1};
a shared octahedron edge is matched when both icosahedra put their corner at the same golden point: t_c xor t_c' = k_e.
Maximise matched edges on periodic boxes of side 2N (exhaustive for N = 1, simulated annealing with restarts for N = 2, 3, 4).
Local bound: at most 8 of the 12 shared edges round each octet corner (exhaustive, 64 cases), so at most 2/3 overall."""
import itertools, sys, json, os
import numpy as np
phi = (1 + 5**.5)/2; a, b = 1/phi**2, 1/phi
def ico(t):
    p, q = (a, b) if t == 0 else (b, a); out = []
    for k in range(3):
        for s1, s2 in itertools.product((1, -1), repeat=2):
            v = [0, 0, 0]; v[(k+1) % 3] = s1*p; v[(k+2) % 3] = s2*q; out.append(v)
    return np.array(out)
def pt(c, t, u, w):
    for v in ico(t) + c:
        if abs(np.linalg.norm(v-u) + np.linalg.norm(v-w) - np.linalg.norm(u-w)) < 1e-9: return v
def build(N):
    M = 2*N; octs = [c for c in itertools.product(range(M), repeat=3) if sum(c) % 2 == 1]; idx = {c: i for i, c in enumerate(octs)}
    E = []
    for c in octs:
        C = np.array(c)
        for d in [(1, 1, 0), (1, -1, 0), (1, 0, 1), (1, 0, -1), (0, 1, 1), (0, 1, -1)]:
            D = np.array(d); nz = [i for i in range(3) if d[i]]
            e1 = np.zeros(3); e1[nz[0]] = d[nz[0]]; e2 = np.zeros(3); e2[nz[1]] = d[nz[1]]
            k = 0 if np.allclose(pt(C, 0, C+e1, C+e2), pt(C+D, 0, C+e1, C+e2)) else 1
            E.append((idx[c], idx[tuple((C+D) % M)], k))
    return octs, np.array(E)
def score(t, E): return int(np.sum((t[E[:, 0]] ^ t[E[:, 1]]) == E[:, 2]))
rng = np.random.default_rng(7); res = {}
for N in (1, 2, 3, 4):
    octs, E = build(N); n = len(octs); m = len(E)
    if n <= 16:
        best = max((score(np.array(ts), E), ts) for ts in itertools.product((0, 1), repeat=n))
        bs, bt = best[0], np.array(best[1])
    else:
        nbr = [[] for _ in range(n)]
        for i, j, k in E: nbr[i].append((j, k)); nbr[j].append((i, k))
        bs, bt = -1, None
        for rep in range(20):
            t = rng.integers(0, 2, n); s = score(t, E)
            for T in np.geomspace(2.0, 0.02, 4000):
                i = rng.integers(n); d = sum((1 if (t[i] ^ t[j]) == k else -1) for j, k in nbr[i])   # matches lost by flipping i
                if d <= 0 or rng.random() < np.exp(-2*d/T): t[i] ^= 1; s -= d - (len(nbr[i]) - d) if False else 0
            s = score(t, E)
            if s > bs: bs, bt = s, t.copy()
    res[N] = {'octahedra': n, 'shared_edges': m, 'best_matched': bs, 'fraction': round(bs/m, 4), 'pattern': {str(octs[i]): int(bt[i]) for i in range(n)} if n <= 32 else None}
    print(f'box side {2*N}: {n} octahedra, {m} shared edges, best matched {bs} = {bs/m:.4f} (bound 2/3 = {2*m/3:.1f})', flush=True)
os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data'), exist_ok=True)
json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'twin-ground-state.json'), 'w'), indent=1)
