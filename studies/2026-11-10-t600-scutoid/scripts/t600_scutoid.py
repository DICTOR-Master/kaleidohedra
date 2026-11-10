"""Is the truncated 600-cell a scutoid build? (DICTO 10 Nov: "looking at the truncated 600 cell it could be a scutoid build by
appearance"; "lets move to the scutoid build test of truncated 600"). Built as in the queen-stages atlas (corners at 1/3 along every
600-cell edge): 1440 corners, 120 icosahedra, 600 truncated tetrahedra. Slice along a direction d: the slice's surface is tiled by the
cross-sections of the 3D cells that cross the hyperplane; two cells are neighbours in the slice iff their shared 2D face crosses it.
At every corner height compare the tiling just below and just above: cells appearing / disappearing; SWAPS (same cells, one pair stops
touching and one starts: the scutoid move); larger changes. Directions: the four main ones of #63 and a generic one."""
import numpy as np, itertools, sys, json
from collections import Counter
exec(open(sys.argv[1]).read().split('keys = ')[0]) if len(sys.argv) > 1 else None   # stages.py: V (120 corners of the 600-cell), D, e0
adj = {i: set(j for j in range(120) if abs(D[i, j] - e0) < 1e-9) for i in range(120)}
E = [(i, j) for i in range(120) for j in adj[i] if j > i]
T = [(i, j, k) for i, j in E for k in adj[i] & adj[j] if k > j]
C = [(i, j, k, l) for i, j, k in T for l in adj[i] & adj[j] & adj[k] if l > k]
assert (len(E), len(T), len(C)) == (720, 1200, 600)
cen = lambda q: V[list(q)].mean(0)
STAGE = sys.argv[2] if len(sys.argv) > 2 else 'truncated'
pt = {}; X = []
if STAGE == 'truncated':
    def P(a, b):                                         # the corner at 1/3 along the edge from a towards b
        if (a, b) not in pt: pt[(a, b)] = len(X); X.append((2 * V[a] + V[b]) / 3)
        return pt[(a, b)]
    cells = [('ico', frozenset(P(v, w) for w in adj[v])) for v in range(120)] + [('tt', frozenset(P(a, b) for a in c for b in c if a != b)) for c in C]
    NV, NC = 1440, 720
elif STAGE == 'red':                                     # the 120-cell: corners = 600-cell cell centres; one dodecahedron per 600-cell corner
    X = [cen(c) for c in C]
    cells = [('D', frozenset(ci for ci, c in enumerate(C) if v in c)) for v in range(120)]
    NV, NC = 600, 120
elif STAGE == 'trunc120':                                # truncated 120-cell: on each Red Queen edge (two 600-cell cells sharing a triangle)
    s_ = (5 - 5 ** .5) / 10; byf = {}
    for ci, c in enumerate(C):
        for f in itertools.combinations(sorted(c), 3): byf.setdefault(f, []).append(ci)
    def P(a, b):
        if (a, b) not in pt: pt[(a, b)] = len(X); X.append((1 - s_) * cen(C[a]) + s_ * cen(C[b]))
        return pt[(a, b)]
    tri_of = {}
    for f, (a, b) in byf.items(): P(a, b); P(b, a); tri_of[(a, b)] = f; tri_of[(b, a)] = f
    cells = [('TD', frozenset(idx for (a, b), idx in pt.items() if v in tri_of[(a, b)])) for v in range(120)] + \
            [('tet', frozenset(idx for (a, b), idx in pt.items() if a == ci)) for ci in range(600)]
    NV, NC = 2400, 720
else:                                                    # bitruncated (atlas: 3/5 of the way from an edge's middle to its triangle's centre)
    def P(t, a, b):
        key = (t, frozenset((a, b)))
        if key not in pt: pt[key] = len(X); X.append(0.4 * (V[a] + V[b]) / 2 + 0.6 * cen(t))
        return pt[key]
    for t in T:
        for a, b in itertools.combinations(t, 2): P(t, a, b)
    cells = [('TI', frozenset(idx for (t, e), idx in pt.items() if v in e)) for v in range(120)] + \
            [('tt', frozenset(idx for (t, e), idx in pt.items() if set(t) <= set(c))) for c in C]
    NV, NC = 3600, 720
X = np.array(X); assert len(X) == NV and len(cells) == NC, (len(X), len(cells))
cnt = Counter(); [cnt.update(S) for _, S in cells]; print('cells per corner:', Counter(cnt.values()), flush=True)
pairs = []                                               # neighbouring cells and their shared 2D face (corner set)
by_pt = {}
for ci, (_, S) in enumerate(cells):
    for p in S: by_pt.setdefault(p, []).append(ci)
seen = set()
for p, cs in by_pt.items():
    for a, b in itertools.combinations(cs, 2):
        if (a, b) in seen: continue
        sh = cells[a][1] & cells[b][1]
        if len(sh) >= 3: pairs.append((a, b, tuple(sorted(sh)))); seen.add((a, b))
print(f'START {STAGE} 600-cell: {len(X)} corners, {len(cells)} cells, {len(pairs)} shared faces '
      f'({Counter((cells[a][0], cells[b][0], len(f)) for a, b, f in pairs)})', flush=True)
c0 = C[0]; t0 = c0[:3]; rng = np.random.default_rng(7)
DIRS = {'vertex-first': V[c0[0]], 'edge-first': (V[c0[0]] + V[c0[1]]) / 2, 'face-first': V[list(t0)].mean(0), 'cell-first': V[list(c0)].mean(0),
        'generic': rng.normal(size=4)}
def tiling(H, h):
    lo = {ci: H[list(S)].min() for ci, (_, S) in enumerate(cells)}; hi = {ci: H[list(S)].max() for ci, (_, S) in enumerate(cells)}
    alive = {ci for ci in lo if lo[ci] < h < hi[ci]}
    edges = {(a, b) for a, b, f in pairs if H[list(f)].min() < h < H[list(f)].max()}
    return alive, edges
results = {}
for name, d in DIRS.items():
    d = d / np.linalg.norm(d); H = X @ d; hs = np.unique(np.round(H, 9)); ev = Counter(); swaps = []
    prev = tiling(H, (hs[0] + hs[1]) / 2)
    for k in range(1, len(hs) - 1):
        cur = tiling(H, (hs[k] + hs[k + 1]) / 2)
        born, died = cur[0] - prev[0], prev[0] - cur[0]
        lost = {e for e in prev[1] - cur[1] if e[0] in cur[0] and e[1] in cur[0]}; gained = {e for e in cur[1] - prev[1] if e[0] in prev[0] and e[1] in prev[0]}
        if born: ev['cells appear'] += len(born)
        if died: ev['cells disappear'] += len(died)
        if lost or gained:
            q = (len(lost), len(gained))
            if q == (1, 1) and len({*next(iter(lost)), *next(iter(gained))}) == 4: ev['SWAP (scutoid move)'] += 1; swaps.append(float(hs[k]))
            else: ev[f'neighbour change {q[0]} lost / {q[1]} gained among surviving cells'] += 1
        prev = cur
    results[name] = dict(ev); print(f'{name}: {len(hs)} corner heights; events {dict(ev)}', flush=True)
json.dump(results, open(f't600_scutoid_{STAGE}.json', 'w'), indent=1)
anyswap = sum(r.get('SWAP (scutoid move)', 0) for r in results.values())
print(f'scutoid moves (swaps among surviving cells) over all directions: {anyswap}')
print('FINAL ok' if all(results.values()) else 'FINAL FAIL: a direction produced no events')
