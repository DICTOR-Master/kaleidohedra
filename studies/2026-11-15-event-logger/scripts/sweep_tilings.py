"""Validation (a): slicing sweeps of the Queen-stage 4-polytopes of #104 as tiling sequences, logged by eventlog.py.
The polytope and its cells are built exactly as in studies/2026-11-10-t600-scutoid/scripts/t600_scutoid.py (copied, not changed);
the slice at height h is a tiling of a 2-sphere: cells = 3D cells crossing h, boundaries = shared 2D faces crossing h (one segment
each), junctions = polytope edges crossing h (the cells round that edge). Frames sit midway between consecutive corner heights
(step 1 = every corner gap: exact; step s = every s-th gap: a coarser time step).
Usage: python sweep_tilings.py STAGES_PY STAGE SEED STEP [STEP ...]  -> sweep_STAGE_SEED.json (counts per step)."""
import numpy as np, itertools, sys, json, os
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from eventlog import Tiling, run, rebalance_log
exec(open(sys.argv[1]).read().split('keys = ')[0])                 # V (120 corners of the 600-cell), D, e0
STAGE, SEED, STEPS = sys.argv[2], int(sys.argv[3]), [int(s) for s in sys.argv[4:]]
adj = {i: set(j for j in range(120) if abs(D[i, j] - e0) < 1e-9) for i in range(120)}
E = [(i, j) for i in range(120) for j in adj[i] if j > i]
T = [(i, j, k) for i, j in E for k in adj[i] & adj[j] if k > j]
C = [(i, j, k, l) for i, j, k in T for l in adj[i] & adj[j] & adj[k] if l > k]
assert (len(E), len(T), len(C)) == (720, 1200, 600)
cen = lambda q: V[list(q)].mean(0)
pt = {}; X = []
if STAGE == 'truncated':
    def P(a, b):
        if (a, b) not in pt: pt[(a, b)] = len(X); X.append((2 * V[a] + V[b]) / 3)
        return pt[(a, b)]
    cells = [('ico', frozenset(P(v, w) for w in adj[v])) for v in range(120)] + [('tt', frozenset(P(a, b) for a in c for b in c if a != b)) for c in C]
    NV, NC = 1440, 720
elif STAGE == 'red':
    X = [cen(c) for c in C]
    cells = [('D', frozenset(ci for ci, c in enumerate(C) if v in c)) for v in range(120)]
    NV, NC = 600, 120
elif STAGE == 'trunc120':
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
else:
    def P(t, a, b):
        key = (t, frozenset((a, b)))
        if key not in pt: pt[key] = len(X); X.append(0.4 * (V[a] + V[b]) / 2 + 0.6 * cen(t))
        return pt[key]
    for t in T:
        for a, b in itertools.combinations(t, 2): P(t, a, b)
    cells = [('TI', frozenset(idx for (t, e), idx in pt.items() if v in e)) for v in range(120)] + \
            [('tt', frozenset(idx for (t, e), idx in pt.items() if set(t) <= set(c))) for c in C]
    NV, NC = 3600, 720
X = np.array(X); assert len(X) == NV and len(cells) == NC
by_pt = {}
for ci, (_, S) in enumerate(cells):
    for p in S: by_pt.setdefault(p, set()).add(ci)
pairs, seen = [], set()
for p, cs in by_pt.items():
    for a, b in itertools.combinations(sorted(cs), 2):
        if (a, b) in seen: continue
        sh = cells[a][1] & cells[b][1]
        if len(sh) >= 3: pairs.append((a, b, tuple(sorted(sh)))); seen.add((a, b))
from scipy.spatial import cKDTree
tree = cKDTree(X); dmin = min(tree.query(X, 2)[0][:, 1])
edges = [(i, j, tuple(sorted(by_pt[i] & by_pt[j]))) for i, j in sorted(tree.query_pairs(dmin * (1 + 1e-6)))]
assert all(len(c) >= 3 for _, _, c in edges), 'an edge in fewer than three cells'
print(f'START {STAGE}: {NV} corners, {NC} cells, {len(pairs)} faces, {len(edges)} edges; cells per edge {dict(Counter(len(c) for *_, c in edges))}', flush=True)
d = np.random.default_rng(SEED).normal(size=4); d /= np.linalg.norm(d); H = X @ d
hs = np.unique(np.round(H, 9)); assert len(hs) == NV, 'direction not generic: two corners at one height'
lo = np.array([H[list(S)].min() for _, S in cells]); hi = np.array([H[list(S)].max() for _, S in cells])
flo = np.array([H[list(f)].min() for *_, f in pairs]); fhi = np.array([H[list(f)].max() for *_, f in pairs])
elo = np.array([min(H[i], H[j]) for i, j, _ in edges]); ehi = np.array([max(H[i], H[j]) for i, j, _ in edges])
def frame(h, t):
    alive = np.nonzero((lo < h) & (h < hi))[0]
    seg = [(a, b) for k, (a, b, _) in enumerate(pairs) if flo[k] < h < fhi[k]]
    jun = [c for k, (_, _, c) in enumerate(edges) if elo[k] < h < ehi[k]]
    return Tiling([int(c) for c in alive], seg, jun, 2, 'sphere', t)
mids = (hs[:-1] + hs[1:]) / 2
frames1 = []
for k, h in enumerate(mids):
    frames1.append(frame(h, k))
    if k % 300 == 0: print(f'PROGRESS {k / len(mids) * 0.5:.3f} frames {k}/{len(mids)}', flush=True)
out = dict(stage=STAGE, seed=SEED, corners=NV, cells=NC, faces=len(pairs), edges=len(edges), steps={})
for s in STEPS:
    fr = frames1[::s] if (len(frames1) - 1) % s == 0 else frames1[::s] + [frames1[-1]]
    rows, summ = run(fr)
    out['steps'][s] = summ; print(f'step {s}: {len(fr)} frames; counts {summ["counts"]}; ok {summ["ok"]}; triple formulas {summ["triple_formulas"]}; '
                                  f'clump patterns {dict(list(summ["clump_patterns"].items())[:6])}', flush=True)
    if s == 1:                                                     # NEGATIVE CONTROL on real data: one event retyped
        i = next(i for i, r in enumerate(rows) if r['type'] in ('birth', 'death', 'clump') and r['net'] != 0)
        bad = [dict(r) for r in rows]; bad[i]['type'] = 'swap'
        out['neg_control_caught'] = len(rebalance_log(fr, bad)) == 1
        print(f'NEG control (event {i} retyped {rows[i]["type"]} -> swap) caught: {out["neg_control_caught"]}', flush=True)
        json.dump(rows, open(f'sweep_{STAGE}_{SEED}_events.json', 'w'))
json.dump(out, open(f'sweep_{STAGE}_{SEED}.json', 'w'), indent=1)
print('PROGRESS 1.000 done', flush=True)
