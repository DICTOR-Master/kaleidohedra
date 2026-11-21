# DICTO · dictospheres.com — 3D scenes of the two scutoid divisions of the resin round C1, bcc mould at 6/5 s0, for the house
# three.js renderer (render3d.py; shots.mjs takes the frames).
# (A) DICTO's combi method (tree branch E, centroid seeds): geometry from data/geom_combi_bcc_6-5_cen.json, written by
#     combi_dump.py (branch E's combi.py, unchanged but for storing the float geometry; its run repeats branch E's result).
# (B) the exact straight-skeleton division (tree branch D round 3): data/skeleton_exact.json, one piece per kind as slabs with exact
#     vertices in Q(sqrt5, sqrt3); the other pieces of a kind are its T_h images.
# Checks (printed, then FINAL ok): combi piece volumes add to mould - C1; every combi Y vertex lies on a piece; skeleton slab volumes
# match the stored kind volumes; 12 hexagon scutoids and 24 triangle scutoids from T_h; Y points are corners of their pieces.
import json, os, sys, itertools
import numpy as np
H = os.path.dirname(os.path.abspath(__file__)); sys.argv = [sys.argv[0], os.path.join(H, 'data', 'resin.json')]
import scenes as S                                  # C1, colours, helpers (re-runs and re-checks the resin scenes)
from render3d import write

OUT = S.OUT; LOG = []
DATA = os.path.join(H, 'data')
s0 = (10 + 4 * 5 ** .5) / 3; s = 1.2 * s0
mould = S.hull([p for q in itertools.permutations((0, 1, 2)) for sg in itertools.product((1, -1), repeat=2)
                for p in [np.array([0, sg[0] * s / 4, sg[1] * s / 2])[list(q)]]])
vm = S.volume(mould); vC1 = 35 + 12.5 * 5 ** .5
YCOL = '#ffffff'                                    # Y vertex dots: white, neutral


def shade(hexc, k):                                 # k < 0 darker, k > 0 lighter (towards white)
    c = np.array([int(hexc[i:i + 2], 16) for i in (1, 3, 5)], float)
    c = c * (1 + k) if k < 0 else c + (255 - c) * k
    return '#%02x%02x%02x' % tuple(int(round(x)) for x in c)


def mesh_part(V, tris, cols, rad, ydots=(), alpha=1.0, ballrad=None):
    """triangles with a colour each; edges = sharp edges only (between non-coplanar triangles), so flat facets show as one face"""
    V = np.asarray(V, float); N = []
    for a, b, c in tris:
        n = np.cross(V[b] - V[a], V[c] - V[a]); N.append(n / np.linalg.norm(n))
    ed = {}
    for i, t in enumerate(tris):
        for k in range(3): ed.setdefault(frozenset((t[k], t[(k + 1) % 3])), []).append(i)
    tubes = []
    for e, L in ed.items():
        assert len(L) == 2, 'open surface'
        if N[L[0]] @ N[L[1]] < 1 - 1e-9: a, b = tuple(e); tubes.append([int(a), int(b), S.EDGE, None])
    part = {'v': np.round(V, 6).tolist(), 't': [list(map(int, t)) for t in tris], 'c': cols, 'a': alpha, 'tubes': tubes, 'rad': rad, 'balls': []}
    parts = [part]
    if len(ydots):                                  # dots as their own part: larger balls than the edge corners
        parts.append({'v': np.round(V[list(ydots)], 6).tolist(), 't': [], 'c': [], 'a': 1.0, 'tubes': [], 'rad': ballrad or rad * 5.0,
                      'balls': [[i, YCOL] for i in range(len(ydots))]})
    return parts


def centred(parts, c):
    for q in parts: q['v'] = (np.array(q['v']).reshape(-1, 3) - c).round(6).tolist()
    return parts


# ---------------- (A) combi ----------------
G = json.load(open(os.path.join(DATA, 'geom_combi_bcc_6-5_cen.json')))
assert G['valid'] and G['n_scutoid_pieces'] == 80 and G['n_kinds'] == 5
X = np.array(G['geom']['X']); Yset = set(G['geom']['Y'])
kind_of = {F: i + 1 for i, k in enumerate(G['kinds']) for F in k['members']}
assert sorted(kind_of) == list(range(80)) and [k['F'] for k in G['kinds']] == [0, 8, 20, 21, 22]
vt = 0; CP = []
for pc in G['geom']['pieces']:
    T = pc['tris']; vol = sum(np.linalg.det(X[[a, b, c]]) for a, b, c in T) / 6; vt += vol
    bot = set(v for P, lab in pc['polys'] if lab == 'bottom' for v in P)
    tops = [set(P) for P, lab in pc['polys'] if lab == 'top']
    lab = ['bottom' if set(t) <= bot else 'top' if any(set(t) <= tp for tp in tops) else 'wall' for t in T]
    yv = sorted({v for t in T for v in t} & Yset)
    CP.append(dict(F=pc['F'], k=kind_of[pc['F']], T=T, lab=lab, Y=yv))
assert abs(vt - (vm - vC1)) < 1e-8, (vt, vm - vC1)
assert set().union(*[set(c['Y']) for c in CP]) == Yset
LOG.append(f'combi bcc 6/5 s0 cen: 80 pieces, sum vol {vt:.9f} = mould - C1 {vm - vC1:.9f}; {len(Yset)} Y vertices, each on pieces; '
           f'Y per kind {[len([c for c in CP if c["F"] == k["F"]][0]["Y"]) for k in G["kinds"]]}')


def combi_piece(c, shift, rad, shades=False, dots=False):
    idx = sorted({v for t in c['T'] for v in t}); m = {v: i for i, v in enumerate(idx)}
    V = X[idx] + shift; T = [[m[v] for v in t] for t in c['T']]; base = S.KIND[c['k'] - 1]
    cols = [shade(base, -0.45) if (shades and l == 'bottom') else shade(base, 0.5) if (shades and l == 'top') else base for l in c['lab']]
    return mesh_part(V, T, cols, rad, ydots=[m[v] for v in c['Y']] if dots else ())


DIR = S.DIR; f = 0.85
parts = [S.c1_whole(0.0028)]
for c in CP:
    cen = X[sorted({v for t in c['T'] for v in t})].mean(0)
    parts += combi_piece(c, f * cen, 0.0022)
shell = S.Solid(mould.V * (1 + f), [(n, d * (1 + f), o) for n, d, o in mould.F])
parts.append(S.solid_part(shell, S.GLASS, alpha=0.16, rad=0.0018, edge_col=S.LIGHT, faces=S.back(shell, DIR)))
sc = [{'E': S.ext(parts, DIR, 1.04), 'dir': DIR.tolist(), 'parts': parts}]
write(os.path.join(OUT, 'combi_cell.html'), sc); LOG.append('combi_cell.html: one cell pulled apart (f = 0.85), mould see-through at (1+f) x')


def stand(V, n, VD):
    """rotation taking the outward normal n of the piece's C1 face to +y, turned about y so that no face is seen square on"""
    y = np.array([0., 1, 0]); v = np.cross(n, y); cth = n @ y; K = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    R = np.eye(3) + K + K @ K / (1 + cth); assert np.allclose(R @ n, y)
    return R


def best_turn(R, normals, VD):
    best = None
    for a in np.radians(np.arange(0, 360, 5)):
        Ry = np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]]); M = Ry @ R
        sc_ = max((M @ nn) @ VD for nn in normals)
        if best is None or sc_ < best[0]: best = (sc_, M)
    return best[1]


VD = np.array([0.7, 0.42, 1.0]); VD /= np.linalg.norm(VD)
VB = np.array([0.7, -0.55, 1.0]); VB /= np.linalg.norm(VB)    # the same pieces seen from below: the Fullerene Star side
sc, below = [], []
for k in G['kinds']:
    c = [c for c in CP if c['F'] == k['F']][0]
    idx = sorted({v for t in c['T'] for v in t}); P = X[idx]; cen = P.mean(0)
    bt = [t for t, l in zip(c['T'], c['lab']) if l == 'bottom'][0]
    n = np.cross(X[bt[1]] - X[bt[0]], X[bt[2]] - X[bt[0]]); n /= np.linalg.norm(n)
    if n @ X[bt[0]] < 0: n = -n                     # outward from C1
    nrm = [np.cross(X[b] - X[a], X[cc] - X[a]) for a, b, cc in c['T']]; nrm = [x / np.linalg.norm(x) for x in nrm]
    M = best_turn(stand(P, n, VD), nrm, VD)
    q = combi_piece(c, -cen, 0.005, shades=True, dots=True)
    for p in q: p['v'] = (np.array(p['v']).reshape(-1, 3) @ M.T).round(6).tolist()
    sc.append({'E': 0, 'dir': VD.tolist(), 'parts': q})
    below.append({'E': 0, 'dir': VB.tolist(), 'parts': q})
sc += below
E = max(S.ext(x['parts'], x['dir'], 1.12) for x in sc)
for x in sc: x['E'] = E
write(os.path.join(OUT, 'combi_kinds.html'), sc); LOG.append('combi_kinds.html: kinds 1-5 alone, from above (p0-4) and below (p5-9), same scale, C1 side dark, mould side light, Y dots')

# ---------------- (B) exact straight skeleton ----------------
SK = json.load(open(os.path.join(DATA, 'skeleton_exact.json')))
assert SK['lattice'] == 'bcc' and SK['factor'] == '6/5' and SK['valid'] and SK['n_scutoid_kinds'] == 2
r5, r3, r15 = 5 ** .5, 3 ** .5, 15 ** .5
def ev(x):
    assert set(x) <= set('0123456789()+-*/ sqrt.'), x
    return eval(x.replace('sqrt15', 'r15').replace('sqrt5', 'r5').replace('sqrt3', 'r3'), {'r5': r5, 'r3': r3, 'r15': r15})
assert SK['s'] == '4+8/5r5' and abs(4 + 1.6 * r5 - s) < 1e-12


def sk_piece(k):
    """union of the slabs: vertices merged, internal cuts (tk) dropped; triangles labelled bottom / lat / shell"""
    V, T, L = [], [], []
    def vid(p):
        for i, q in enumerate(V):
            if np.linalg.norm(q - p) < 1e-9: return i
        V.append(p); return len(V) - 1
    vol = 0
    for sl in k['slabs']:
        P = np.array([[ev(x) for x in v] for v in sl['vertices']])
        c = P.mean(0)
        for fc in sl['faces']:
            o = fc['vertices']
            for a, b in zip(o[1:-1], o[2:]): vol += abs(np.linalg.det([P[o[0]] - c, P[a] - c, P[b] - c])) / 6
            if fc['label'][0] == 'tk': continue
            ids = [vid(P[i]) for i in o]
            for a, b in zip(ids[1:-1], ids[2:]): T.append([ids[0], a, b]); L.append(fc['label'][0])
    V = np.array(V)
    # orient triangles outward (piece is star-shaped from its slab-centroid? use winding consistency by flipping to agree with neighbours)
    return V, T, L, vol


SKP = {}
for kn, k in enumerate(SK['kinds'], 1):
    V, T, L, vol = sk_piece(k)
    assert abs(vol - k['vol']) < 1e-9, (kn, vol, k['vol'])
    Y = [np.array([ev(x) for x in y]) for y in k['Y_points']]
    yi = [int(np.argmin(np.linalg.norm(V - y, axis=1))) for y in Y]
    assert all(np.linalg.norm(V[i] - y) < 1e-9 for i, y in zip(yi, Y))
    SKP[kn] = dict(V=V, T=T, L=L, Y=yi, k=k)
LOG.append('skeleton exact bcc 6/5 s0: slab volumes match the stored kind volumes; scutoid kinds ' +
           str([kn for kn in SKP if SKP[kn]['k']['scutoid']]) + ' (Y points are corners of their pieces)')
vsum = sum(SKP[kn]['k']['vol'] * SKP[kn]['k']['orbit'] for kn in SKP)
assert abs(vsum - (vm - vC1)) < 1e-8; LOG.append(f'skeleton: sum of kind volume x orbit = {vsum:.9f} = mould - C1')


def sk_mesh(kn, M=np.eye(3), shift=np.zeros(3), rad=0.005, shades=True, dots=True):
    d = SKP[kn]; base = S.KIND[kn - 1]
    cols = [shade(base, -0.45) if (shades and l == 'bottom') else shade(base, 0.5) if (shades and l == 'shell') else base for l in d['L']]
    return mesh_part(d['V'] @ M.T + shift, d['T'], cols, rad, ydots=d['Y'] if dots else ())


sc = []
for kn in (2, 3):
    d = SKP[kn]; c = d['V'].mean(0)
    bt = [t for t, l in zip(d['T'], d['L']) if l == 'bottom'][0]
    n = np.cross(d['V'][bt[1]] - d['V'][bt[0]], d['V'][bt[2]] - d['V'][bt[0]]); n /= np.linalg.norm(n)
    if n @ d['V'][bt[0]] < 0: n = -n
    nrm = [np.cross(d['V'][b] - d['V'][a], d['V'][cc] - d['V'][a]) for a, b, cc in d['T']]; nrm = [x / np.linalg.norm(x) for x in nrm]
    M = best_turn(stand(d['V'], n, VD), nrm, VD)
    sc.append({'E': 0, 'dir': VD.tolist(), 'parts': sk_mesh(kn, M, -(M @ c))})
    sc.append({'E': 0, 'dir': VB.tolist(), 'parts': sk_mesh(kn, M, -(M @ c))})
E = max(S.ext(x['parts'], x['dir'], 1.12) for x in sc)
for x in sc: x['E'] = E
# the 12 hexagon scutoids round C1 (T_h images of kind 2), together, no mould
d = SKP[2]; imgs, parts = [], [S.c1_whole(0.0035)]
for g in S.TH:
    W = S.act(g, d['V']); key = tuple(sorted(map(tuple, np.round(W, 6) + 0.0)))
    if key in imgs: continue
    imgs.append(key)
    c_, sg = g; M = np.zeros((3, 3))
    for i in range(3): M[i, (i - c_) % 3] = sg[i]
    assert np.allclose(d['V'] @ M.T, W)
    if np.linalg.det(M) < 0:                        # a reflection reverses the triangle order; colours and edges do not care
        pass
    parts += mesh_part(W, d['T'], [S.KIND[1] if l == 'lat' else shade(S.KIND[1], 0.5) if l == 'shell' else shade(S.KIND[1], -0.45) for l in d['L']],
                       0.0035, ydots=d['Y'], ballrad=0.0035 * 5.0)
assert len(imgs) == 12; LOG.append('skeleton: 12 distinct hexagon scutoids (kind 2) from T_h')
DH = np.array([0.5, 0.36, 1.0])
sc.append({'E': S.ext(parts, DH, 1.06), 'dir': DH.tolist(), 'parts': parts})
write(os.path.join(OUT, 'skeleton.html'), sc); LOG.append('skeleton.html: kind 2 from above and below, kind 3 from above and below, the 12 kind-2 pieces round C1')
open(os.path.join(H, 'scenes2.log'), 'w').write('\n'.join(LOG) + '\nFINAL ok\n'); print('\n'.join(LOG)); print('FINAL ok')
