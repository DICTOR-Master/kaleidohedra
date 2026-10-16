# Fable, GBPC pass 4 (2026-10-16): FLOAT check and gap analysis of a search result (gbpc_search.py output).
# Grid of n^3 points in one bcc cell (fractional coordinates, periodic). Each point: inside an RT? inside how many placed bodies
# (all lattice translates)? The gap = points in no RT and no body. Components: periodic flood fill with lattice offsets, so each
# component is unwrapped in space; then voxel volume vs convex-hull volume (ratio near 1 = convex) and wrap test.
# usage: python3 gbpc_gap.py RESULT.json N OUT.txt
import sys, os, json, itertools, numpy as np
from scipy.spatial import ConvexHull
S5 = 5 ** 0.5
qf = lambda s: (lambda a, b: float(eval(a)) + float(eval(b)) * S5)(*s.split('|'))
vf = lambda v: np.array([qf(x) for x in v])
HERE = os.path.dirname(os.path.abspath(__file__)); STUDY = os.path.dirname(HERE)
G = json.load(open(os.path.join(STUDY, 'data', 'gbpc-geom-exact.json'))); R = json.load(open(sys.argv[1])); n = int(sys.argv[2])
L = np.array([vf(v) for v in G['LB']]).T; cv = abs(np.linalg.det(L))
RTH = [(vf(nn), qf(d)) for nn, d in G['RT_H']]; Hn = np.array([h[0] for h in RTH]); Hd = np.array([h[1] for h in RTH])
g = (np.arange(n) + 0.5) / n
F = np.stack(np.meshgrid(g, g, g, indexing='ij'), -1).reshape(-1, 3); X = F @ L.T
shifts = [L @ np.array(m) for m in itertools.product(range(-3, 4), repeat=3)]
shifts = [s for s in shifts if np.linalg.norm(s) < 4.5]
inRT = np.zeros(len(X), bool)
for s in shifts: inRT |= np.all((X - s) @ Hn.T <= Hd + 1e-12, axis=1)
cnt = np.zeros(len(X), np.int16); XMIN, XMAX = X.min(0), X.max(0)
for B in R['bodies']:
    V = np.array([vf(v) for v in B['vertices']]); h = ConvexHull(V); E = h.equations
    lo, hi = V.min(0), V.max(0)
    for s in shifts:
        if np.any(lo + s > XMAX) or np.any(hi + s < XMIN): continue
        m = np.all((X >= lo + s - 1e-9) & (X <= hi + s + 1e-9), axis=1)
        if not m.any(): continue
        idx = np.where(m)[0]
        cnt[idx] += np.all((X[idx] - s) @ E[:, :3].T + E[:, 3] < -1e-12, axis=1)
free = ~inRT; gap = free & (cnt == 0)
lines = ['DICTO · dictospheres.com',
         f"FLOAT grid {n}^3 in one cell, result {os.path.basename(sys.argv[1])} (mode {R['mode']}): free {free.mean():.5f} of the cell; bodies cover {(cnt > 0).mean() / free.mean():.4f} of the free points;"
         f" covered twice {(cnt > 1).sum()} points; body points inside an RT {(inRT & (cnt > 0)).sum()}; gap {gap.mean() / free.mean():.4f} of G'"]
# components of the gap (6-neighbour, periodic, with lattice offsets)
gr = gap.reshape(n, n, n); lab = -np.ones((n, n, n), np.int32); off = np.zeros((n, n, n, 3), np.int16); comps = []
for st in map(tuple, np.argwhere(gr)):
    if lab[st] >= 0: continue
    k = len(comps); lab[st] = k; stack = [st]; pts = []; wraps = False
    while stack:
        p = stack.pop(); pts.append((p, off[p].copy()))
        for ax in range(3):
            for d in (-1, 1):
                qq = list(p); o = off[p].copy(); qq[ax] += d
                if qq[ax] < 0: qq[ax] += n; o[ax] -= 1
                elif qq[ax] >= n: qq[ax] -= n; o[ax] += 1
                qq = tuple(qq)
                if not gr[qq]: continue
                if lab[qq] < 0: lab[qq] = k; off[qq] = o; stack.append(qq)
                elif lab[qq] == k and np.any(off[qq] != o): wraps = True
    P = np.array([((np.array(p) + 0.5) / n + o) @ L.T for p, o in pts])
    hv = ConvexHull(P).volume if len(P) >= 8 and np.linalg.matrix_rank(P - P.mean(0)) == 3 else 0.0
    comps.append((len(pts) * cv / n ** 3, hv, wraps, len(pts)))
comps.sort(key=lambda c: -c[0])
tot = sum(c[0] for c in comps)
lines.append(f'gap components per cell: {len(comps)}; percolating (wrap the cell): {sum(c[2] for c in comps)}; volume (FLOAT) {tot:.6f}')
big = [c for c in comps if c[3] >= 20]
lines.append(f'components with >= 20 voxels: {len(big)}, holding {sum(c[0] for c in big) / tot:.2%} of the gap; the 10 largest: '
             + '; '.join(f'vol {c[0]:.5f}, hull {c[1]:.5f}, vol/hull {c[0] / c[1] if c[1] else 0:.2f}{", wraps" if c[2] else ""}' for c in comps[:10]))
lines.append(f'components below 20 voxels (slivers at grid resolution): {len(comps) - len(big)}, {sum(c[0] for c in comps if c[3] < 20) / tot:.2%} of the gap')
print('\n'.join(lines)); open(sys.argv[3], 'w').write('\n'.join(lines) + '\n')
