# Step 20 (DICTO: "try the envelopes in the five-fold chorus arrangement"). Float.
# Envelopes (golden rhombic triacontahedra) on every copy of the spatial five-fold chorus, each cut at the joints it actually has
# (a neighbour at 2h along a hexagon normal). Overlaps between envelopes; then the canonical golden cut of the golden region
# around the central copy (its Voronoi cell among the chorus sites), pieces compared with the five Bodhi shapes.
import json, itertools, numpy as np, sys
from scipy.spatial import ConvexHull, HalfspaceIntersection
from scipy.optimize import linprog
sys.path.insert(0, '../_lib'); import geomcheck as gc
N = json.load(open('data/network.json')); O = np.array(N['ocd']); r = np.linalg.norm(O, axis=1)
ax = gc.icosa_axes(O[np.abs(r - r.max()) < 1e-9]); D2 = np.vstack([ax['2'], -ax['2']])
S = np.array(json.load(open('data/chorus-space.json'))['sites'])
pl = []
for e in ConvexHull(O).equations:
    if not any(np.allclose(e, q, atol=1e-7) for q in pl): pl.append(e)
hexn = [e for e in pl if np.sum(np.abs(O @ e[:3] + e[3]) < 1e-7) == 6]
HU = np.array([e[:3] / np.linalg.norm(e[:3]) for e in hexn]); h = -hexn[0][3] / np.linalg.norm(hexn[0][:3])
base = np.array([np.r_[u, -np.max(O @ u)] for u in D2])
def poly(H):
    H = np.array(H); nrm = np.linalg.norm(H[:, :3], axis=1)
    rr = linprog([0, 0, 0, -1], A_ub=np.c_[H[:, :3], nrm], b_ub=-H[:, 3], bounds=[(None, None)] * 3 + [(0, None)])
    if rr.status != 0 or rr.x[3] < 1e-7: return None
    X = np.unique(np.round(HalfspaceIntersection(H, rr.x[:3]).intersections, 10), axis=0)
    return (H, X) if len(X) >= 4 and ConvexHull(X).volume > 1e-10 else None
envs = []
for s in S:
    cuts = []
    for u in HU:
        if np.min(np.linalg.norm(S - (s + 2 * h * u), axis=1)) < 1e-6: cuts.append(np.r_[u, -(u @ s) - h])   # joint: cut at the hexagon plane
    H = np.vstack([base - np.c_[np.zeros((len(base), 3)), base[:, :3] @ s]] + ([np.array(cuts)] if cuts else []))
    P = poly(H); envs.append(ConvexHull(P[1]).equations if P else None)
def overlap(E1, E2): return poly(list(E1) + list(E2)) is not None
centre = int(np.argmin(np.linalg.norm(S, axis=1)))
near = [i for i in range(len(S)) if np.linalg.norm(S[i] - S[centre]) < 2.0 and i != centre]
ov = sum(overlap(envs[i], envs[j]) for i, j in itertools.combinations([centre] + near, 2))
out = [f'chorus: {len(S)} copies; envelopes cut at their actual joints; overlapping envelope pairs around the centre: {ov}']
# the golden region around the central copy: its Voronoi cell among the chorus sites, minus every nearby envelope
cell = [np.r_[S[j] - S[centre], -((S[j] @ S[j]) - (S[centre] @ S[centre])) / 2] for j in range(len(S)) if j != centre]
envN = [envs[i] for i in [centre] + near]
def uniq(E):
    o = []
    for e in E:
        e = e / np.linalg.norm(e[:3])
        if not any(np.allclose(e, q, atol=1e-9) for q in o): o.append(e)
    return np.array(o)
planes = uniq(np.vstack(envN))
pieces, stack = [], [cell]
while stack:
    H = stack.pop(); P = poly(H)
    if P is None: continue
    H, X = P
    if any(np.all(X @ E[:, :3].T + E[:, 3] <= 1e-9) for E in envN): continue
    if not any(poly(list(H) + list(E)) is not None for E in envN): pieces.append(X); continue
    for e in planes:
        s_ = X @ e[:3] + e[3]
        if s_.max() > 1e-8 and s_.min() < -1e-8: stack.append(list(H) + [e]); stack.append(list(H) + [-e]); break
    else: pieces.append(X)
def sig(P):
    P = np.unique(np.round(P, 9), axis=0); E = sorted(np.linalg.norm(a - b) for a, b in itertools.combinations(P, 2)); return len(P), tuple(np.round(np.array(E) / E[-1], 4))
bodhi = {}
for b, nm in [('B1', 'Vajra (fine)'), ('B2', 'Chatra'), ('B3', 'Mudra'), ('B4', 'Crown Jewel'), ('B5', 'Diadem')]:
    bodhi[sig(np.array(json.load(open(f'../2026-10-12-bodhi-pieces/data/bodhi-{b}-unit.json'))['vertices']))] = nm
kinds = gc.kinds(pieces, gc.group(ax)) if len(pieces) < 3000 else []
golden_only = sum(1 for X in pieces if all(np.max(D2 @ e[:3]) > 1 - 1e-7 for e in ConvexHull(X).equations))
match = {}
for X in pieces:
    nm = bodhi.get(sig(X))
    if nm: match[nm] = match.get(nm, 0) + 1
vol = sum(ConvexHull(X).volume for X in pieces)
out += [f'golden region in the central copy\'s cell: volume {vol:.6f}; {len(pieces)} pieces, {len(kinds)} kinds; purely golden-walled {golden_only}',
        f'Bodhi pieces among them: {match if match else "none"}  (the cubic packing gave 1624 pieces, 751 kinds, 6 Diadems)']
print('\n'.join(out)); open('data/chorus-golden.txt', 'w').write('\n'.join(out) + '\n')
