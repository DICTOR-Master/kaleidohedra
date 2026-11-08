"""Does the perfect stella yantra's upper great triangle have a parent solid? Its slope 0.695886431693 (apex half-angle 34.83353
degrees) puts its base corners at alpha = 180 - 2 * 34.83353 = 110.33293 degrees from its tip, measured round the circle; the
stella's lower triangle has 109.47122 (the tetrahedral angle). Search: every angle between two corners of the regular 4D solids
(5-cell, tesseract, 16-cell, 24-cell, 600-cell, 120-cell = centres of the 600-cell's cells), the five Platonic solids, and every
solid of DICTO's dataset v8 whose corners all lie on one sphere. Report the angles nearest to alpha."""
import json, glob, itertools, math, os
import numpy as np
ALPHA = 180 - 2 * math.degrees(math.atan(0.695886431693492822627280681684))
def angles(V):
    V = np.array(V, float); V = V - V.mean(0); r = np.linalg.norm(V, axis=1)
    if r.min() < 1e-9 or (r.max() - r.min()) > 1e-7 * r.max(): return None        # not all on one sphere about the centroid
    U = V / r[:, None]; G = np.clip(U @ U.T, -1, 1)
    return sorted({round(math.degrees(math.acos(g)), 7) for g in G[np.triu_indices(len(U), 1)]})
S = {}
phi = (1 + 5 ** .5) / 2
S['5-cell'] = [list(r) for r in np.vstack([np.eye(5)])]               # in R^5, on the hyperplane sum = 1 (centroid removed in angles())
S['tesseract'] = [list(p) for p in itertools.product((-1, 1), repeat=4)]
S['16-cell'] = [list(s * np.eye(4)[i]) for i in range(4) for s in (1, -1)]
S['24-cell'] = [list(v) for v in {tuple(p) for i, j in itertools.combinations(range(4), 2) for a in (1, -1) for b in (1, -1) for p in [tuple(a if k == i else b if k == j else 0 for k in range(4))]}]
src = json.load(open(os.path.expanduser('~/k-research/studies/2026-10-27-white-queen-600/data/600cell-source.json')))
V600 = np.array(src['vertices'], float); S['600-cell'] = V600.tolist()
E = {tuple(sorted(e)) for e in src['edges']}; nb = {i: set() for i in range(len(V600))}
for i, j in E: nb[i].add(j); nb[j].add(i)
cells = {tuple(sorted((a, b, c, d))) for a in nb for b in nb[a] for c in nb[a] & nb[b] for d in nb[a] & nb[b] & nb[c]}
S['120-cell'] = [list(V600[list(c)].mean(0)) for c in cells]
assert len(cells) == 600, len(cells)
P3 = {'tetrahedron': [(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)], 'cube': list(itertools.product((-1,1), repeat=3)), 'octahedron': [tuple(s*np.eye(3)[i]) for i in range(3) for s in (1,-1)],
      'icosahedron': [p for c in [(0,1,phi),(1,phi,0),(phi,0,1)] for p in itertools.product(*[(x,-x) if x else (0,) for x in c])],
      'dodecahedron': list(itertools.product((-1,1), repeat=3)) + [p for c in [(0,1/phi,phi),(1/phi,phi,0),(phi,0,1/phi)] for p in itertools.product(*[(x,-x) if x else (0,) for x in c])]}
for k, v in P3.items(): S[k] = [list(p) for p in v]
for f in sorted(glob.glob(os.path.expanduser('~/k-mathdata/studies/2026-10-22-math-data-dicto-solids/solids/*.json'))):
    if 'unit-volume' in f: continue
    j = json.load(open(f)); vs = j.get('vertices', {})
    vv = vs.get('decimal') if isinstance(vs, dict) else None
    if vv is None and isinstance(vs, list) and vs and isinstance(vs[0], dict): vv = [x.get('decimal') for x in vs]
    if not vv: continue
    try: S['dataset: ' + j['name']] = [[float(c) for c in p] for p in vv]
    except Exception: pass
hits = []
for name, V in S.items():
    A = angles(V)
    if not A: continue
    for a in A: hits.append((abs(a - ALPHA), a, name))
hits.sort()
print(f'target alpha = {ALPHA:.6f} deg (stella lower: 109.471221 deg); solids searched: {len(S)}, inscribed: {len({h[2] for h in hits})}')
for d, a, n in hits[:15]: print(f'  {a:.6f} deg  (off by {d:.6f})  {n}')
exact = [h for h in hits if h[0] < 1e-5]
print('FINAL ok' if hits else 'FINAL FAIL: nothing searched')
print('exact parent found' if exact else 'no solid has this angle exactly')
