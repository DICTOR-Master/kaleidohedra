#!/usr/bin/env python3
"""Network fingerprint (DICTO 4 Nov 2026: "start the network fingerprint with admiral caps ... and identify new potential solids").
Input: data/admiral-network-pieces.json, the I world of paper #47 as built by the Kaleidohedra engine (platonic-mix-geometry.js, slabPieces('I')):
icosahedra I in Pacioli's position in octahedra, six Admiral Caps A per octahedron, the octet's tetrahedra as face pyramids Q'.
For every complete node (pieces fill a small sphere round it): edge-neighbour fingerprint Q4, Q6, Q8, W6-hat (Steinhardt et al.; #94),
the kinds of piece round it, and its vertex star (union of the pieces at the node): convex or not, hull faces. Convex stars are
candidate solids. Nodes are grouped into types. Run on compute-host with python3."""
import json, math, os, sys, itertools
import numpy as np
from scipy.special import sph_harm_y
from scipy.spatial import ConvexHull
from sympy.physics.wigner import wigner_3j
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, '..', 'data')
src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(D, 'admiral-network-pieces.json')
pieces = json.load(open(src))
R = lambda p: tuple(round(x, 6) for x in p)
for p in pieces:
    p['V'] = np.unique(np.array([c for f in p['faces'] for c in f] if 'faces' in p else p['V'], float).round(9), axis=0)
    h = ConvexHull(p['V']); p['H'] = h.equations; p['vol'] = h.volume
    if 'faces' not in p:   # true edges: hull simplex edges whose two facets are not coplanar
        inc = {}
        for si, simp in enumerate(h.simplices):
            for e in itertools.combinations(sorted(simp), 2): inc.setdefault(e, []).append(si)
        p['edges'] = [(p['V'][i], p['V'][j]) for (i, j), ss in inc.items() if len(ss) == 2 and np.linalg.norm(h.equations[ss[0]][:3] - h.equations[ss[1]][:3]) > 1e-6]
nodes = {}
edges = set()
for k, p in enumerate(pieces):
    for v in p['V']: nodes.setdefault(R(v), set()).add(k)
    for a, b in (p['edges'] if 'edges' in p else [(a, b) for f in p['faces'] for a, b in zip(f, f[1:] + f[:1])]):
        e = tuple(sorted((R(a), R(b)))); edges.add(e)
nb = {}
for a, b in edges:
    nb.setdefault(a, set()).add(b); nb.setdefault(b, set()).add(a)
inside = lambda p, x: np.all(p['H'][:, :3] @ x + p['H'][:, 3] <= 1e-9)
rng = np.random.default_rng(1); S = rng.normal(size=(600, 3)); S /= np.linalg.norm(S, axis=1)[:, None]
W3 = {}
def fp(U):
    u = U / np.linalg.norm(U, axis=1)[:, None]; th = np.arccos(np.clip(u[:, 2], -1, 1)); ph = np.arctan2(u[:, 1], u[:, 0]); out = {}
    for l in (4, 6, 8):
        q = np.array([sph_harm_y(l, m, th, ph).mean() for m in range(-l, l+1)]); s = float(np.sum(np.abs(q)**2))
        out[f'Q{l}'] = round(math.sqrt(4*math.pi/(2*l+1)*s), 4)
        if l == 6:
            if 6 not in W3: W3[6] = [(a, b, -a-b, float(wigner_3j(6, 6, 6, a, b, -a-b))) for a in range(-6, 7) for b in range(-6, 7) if abs(a+b) <= 6]
            w = sum(c*q[a+6]*q[b+6]*q[cc+6] for a, b, cc, c in W3[6]); out['W6'] = round(float(np.real(w))/s**1.5, 4) if s > 1e-14 else 0.0
    return out
cent = np.array([p['V'].mean(0) for p in pieces]); rad = np.array([np.max(np.linalg.norm(p['V'] - p['V'].mean(0), axis=1)) for p in pieces])
types = {}
tj = 0
for v, ks0 in nodes.items():
    x = np.array(v)
    near = np.where(np.linalg.norm(cent - x, axis=1) <= rad + 1e-6)[0]
    ks = {int(k) for k in near if np.all(pieces[k]['H'][:, :3] @ x + pieces[k]['H'][:, 3] <= 1e-7)}
    if ks - set(ks0): tj += 1
    eps = 0.04
    if not all(any(inside(pieces[k], x + eps*d) for k in ks) for d in S): continue   # incomplete (block boundary)
    U = np.array([np.array(w) - x for w in nb[v]])
    f = fp(U)
    comp = tuple(sorted((kind, sum(1 for k in ks if pieces[k]['kind'] == kind)) for kind in {pieces[k]['kind'] for k in ks}))
    allV = np.vstack([pieces[k]['V'] for k in ks]); hull = ConvexHull(allV)
    star_vol = sum(pieces[k]['vol'] for k in ks); convex = abs(hull.volume - star_vol) < 1e-7
    fs = {}
    for eq in hull.equations: fs.setdefault(tuple(np.round(eq[:3], 6)), eq)
    census = {}
    hv = allV[hull.vertices]
    for eq in fs.values():
        n = sum(1 for p in hv if abs(p @ eq[:3] + eq[3]) < 1e-7); census[n] = census.get(n, 0) + 1
    key = (comp, len(nb[v]), f['Q4'], f['Q6'], f['Q8'], f['W6'])
    t = types.setdefault(key, {'composition': dict(comp), 'edge_neighbours': len(nb[v]), 'fingerprint': f, 'count': 0,
                               'star_convex': convex, 'star_volume': round(star_vol, 6), 'star_faces': dict(sorted(census.items())),
                               'star_corners': int(len(hull.vertices)), 'example': v})
    t['count'] += 1
out = sorted(types.values(), key=lambda t: -t['count'])
print('nodes lying inside an edge or face of another piece (T-junctions):', tj)
for t in out:
    print(t['count'], 'nodes |', t['composition'], '| edges', t['edge_neighbours'], '|', t['fingerprint'], '| star convex' if t['star_convex'] else '| star not convex',
          t['star_corners'], 'corners, faces', t['star_faces'], 'vol', t['star_volume'])
json.dump(out, open(os.path.join(D, os.path.basename(src).replace('-pieces.json', '-fingerprint.json')), 'w'), indent=1, default=str)
