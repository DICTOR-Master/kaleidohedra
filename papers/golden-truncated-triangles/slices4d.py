# Which of DICTO's solids are cross-sections of a regular 4D polytope? (DICTO 11-03, after White Knight and the golden truncations)
# Polytopes: 5-cell, 8-cell, 16-cell, 24-cell, 600-cell, 120-cell. Directions: vertex-, edge-, face- and cell-first (face/cell via the dual).
# For each direction, slice at N heights; the section = convex hull of edge crossings. Each convex dataset solid (and the ten golden truncations)
# is compared scale-free (same corner count; sorted pairwise squared distances / mean squared radius). Local minima of the mismatch are refined
# by golden-section search; matches below 1e-8 are reported with their height. Output slices4d.json + slices4d.md. Floats; matches are
# candidates for an exact check.
import sys, os, json, itertools, glob, time, numpy as np
from scipy.spatial import ConvexHull
sys.path.insert(0, sys.argv[2]); from star_core import load
g = (1 + 5 ** .5) / 2
def unique(P): return np.unique(np.round(P, 9), axis=0)
def edges(V):
    D = np.linalg.norm(V[:, None] - V[None], axis=2); m = D[D > 1e-9].min()
    return [(i, j) for i, j in zip(*np.where(np.triu(np.abs(D - m) < 1e-7, 1)))]
def cliques(V, E, k):
    adj = {i: set() for i in range(len(V))}
    for i, j in E: adj[i].add(j); adj[j].add(i)
    out = []
    def grow(c, cand):
        if len(c) == k: out.append(c); return
        for v in sorted(cand):
            if v > c[-1]: grow(c + [v], cand & adj[v])
    for v in range(len(V)): grow([v], adj[v])
    return out
evenp = [p for p in itertools.permutations(range(4)) if sum(1 for a in range(4) for b in range(a + 1, 4) if p[a] > p[b]) % 2 == 0]
def signs(v): return [tuple(s * x for s, x in zip(ss, v)) for ss in itertools.product([1, -1], repeat=4)]
def poly(name):
    if name == '8-cell': return np.array(list(itertools.product([1, -1], repeat=4)), float)
    if name == '16-cell': return unique(np.array([s for p in itertools.permutations([1, 0, 0, 0]) for s in signs(p)], float))
    if name == '24-cell': return unique(np.array([s for p in itertools.permutations([1, 1, 0, 0]) for s in signs(p)], float))
    if name == '600-cell':
        P = [s for s in signs((.5, .5, .5, .5))] + [s for p in itertools.permutations([1, 0, 0, 0]) for s in signs(p)]
        base = (g / 2, .5, 1 / (2 * g), 0)
        P += [s for pe in evenp for s in signs(tuple(base[pe[i]] for i in range(4)))]
        return unique(np.array(P, float))
    if name == '120-cell':
        V6 = poly('600-cell'); C = cliques(V6, edges(V6), 4); return unique(np.array([V6[c].mean(0) for c in C]))
    if name == '5-cell':
        E5 = np.eye(5) - 0.2; B = np.linalg.svd(E5)[2][:4]; return E5 @ B.T
DUAL = {'5-cell': '5-cell', '8-cell': '16-cell', '16-cell': '8-cell', '24-cell': '24-cell', '600-cell': '120-cell', '120-cell': '600-cell'}
def directions(name):
    V = poly(name); E = edges(V); W = poly(DUAL[name])
    if name == '24-cell': W = unique(np.array([s for p in itertools.permutations([1, 0, 0, 0]) for s in signs(p)] + [s for s in signs((.5, .5, .5, .5))], float))  # dual 24-cell
    if name == '5-cell': W = -V
    EW = edges(W)
    return {'vertex-first': V[0], 'edge-first': V[E[0][0]] + V[E[0][1]], 'face-first': W[EW[0][0]] + W[EW[0][1]], 'cell-first': W[0]}, V, E
def section(V, E, d, h):
    B = np.linalg.svd(d[None])[2][1:]; H = V @ d; P = [V[i] @ B.T for i in np.where(np.abs(H - h) < 1e-12)[0]]
    for i, j in E:
        a, b = H[i] - h, H[j] - h
        if a * b < -1e-15: t = a / (a - b); P.append((V[i] + t * (V[j] - V[i])) @ B.T)
    if len(P) < 4: return None
    P = unique(np.array(P))
    try: hl = ConvexHull(P)
    except Exception: return None
    return P[hl.vertices]
def inv(P):
    P = P - P.mean(0); R2 = (P ** 2).sum(1).mean()
    return np.sort(((P[:, None] - P[None]) ** 2).sum(-1)[np.triu_indices(len(P), 1)] / R2)
# targets: convex dataset solids + the ten golden truncations
T = {}
for f in sorted(glob.glob(os.path.join(sys.argv[1], 'solids', '*.json'))):
    d = json.load(open(f))
    if not d.get('convex'): continue
    W = np.array([[float(c) for c in v['decimal']] for v in d['vertices']]); T[d['name']] = inv(W)
byn = {}
for k, v in T.items(): byn.setdefault(int(round((1 + (1 + 8 * len(v)) ** .5) / 2)), []).append(k)
N = int(sys.argv[3]) if len(sys.argv) > 3 else 2400
res = []; t0 = time.time()
for name in ['5-cell', '8-cell', '16-cell', '24-cell', '600-cell', '120-cell']:
    D, V, E = directions(name)
    for lab, d in D.items():
        d = d / np.linalg.norm(d); top = (V @ d).max(); hs = np.linspace(0, top, N)[1:-1]
        prev = {}
        def mis(h, key):
            P = section(V, E, d, h)
            if P is None or len(P) not in byn or key not in byn[len(P)]: return 9.0
            a, b = inv(P), T[key]; return float(np.max(np.abs(a - b))) if len(a) == len(b) else 9.0
        cache = []
        for h in hs:
            P = section(V, E, d, h)
            row = {}
            if P is not None and len(P) in byn:
                a = inv(P)
                for key in byn[len(P)]: row[key] = float(np.max(np.abs(a - T[key]))) if len(a) == len(T[key]) else 9.0
            cache.append(row)
        for key in T:
            vals = np.array([c.get(key, 9.0) for c in cache]); flat = vals < 1e-9
            i = 0
            while i < len(vals):          # runs of exact matches = the shape is constant over an interval of heights
                if flat[i]:
                    j = i
                    while j + 1 < len(vals) and flat[j + 1]: j += 1
                    if j > i:
                        res.append(dict(solid=key, polytope=name, direction=lab, height=float(hs[i]), height_to=float(hs[j]), height_over_top=hs[i] / top, mismatch=0.0, interval=True))
                        print(f'MATCH-INTERVAL {key}: {name} {lab} h in [{hs[i]:.6f}, {hs[j]:.6f}]', flush=True)
                        flat[i:j + 1] = False; vals[i:j + 1] = 9.0
                    i = j + 1
                else: i += 1
            for i in range(1, len(vals) - 1):
                if vals[i] < 0.05 and vals[i] <= vals[i - 1] and vals[i] <= vals[i + 1]:
                    lo, hi = hs[i - 1], hs[i + 1]
                    for _ in range(80):
                        m1, m2 = lo + (hi - lo) / g ** 2, hi - (hi - lo) / g ** 2
                        if mis(m1, key) < mis(m2, key): hi = m2
                        else: lo = m1
                    hb = (lo + hi) / 2; e = mis(hb, key)
                    if e < 1e-6: res.append(dict(solid=key, polytope=name, direction=lab, height=hb, height_over_top=hb / top, mismatch=e)); print(f'MATCH {key}: {name} {lab} h={hb:.10f} (h/top {hb/top:.8f}) err {e:.1e}', flush=True)
        print(f'{name} {lab} done ({time.time() - t0:.0f}s)', flush=True)
json.dump(res, open('slices4d.json', 'w'), indent=1)
with open('slices4d.md', 'w') as f:
    f.write('# DICTO solids found as sections of regular 4D polytopes (float search; exact check pending)\n\n')
    for r in res: f.write(f"- {r['solid']}: {r['polytope']} {r['direction']}, height {r['height']:.10f}" + (f" to {r['height_to']:.6f} (constant over the interval)" if r.get('interval') else f" (fraction of tip {r['height_over_top']:.8f}), mismatch {r['mismatch']:.1e}") + "\n")
print('ALL DONE', len(res), 'matches')
