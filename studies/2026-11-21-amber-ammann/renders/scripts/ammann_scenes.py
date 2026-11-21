# DICTO · dictospheres.com — three scenes of the Amber-Ammann study (Rollerball-Amber Cells in the 3D Penrose tiling), for the house three.js
# renderer (render3d.py, shots.mjs of the scutoid stand-in renders). Geometry: ../../data/patch.json (exact patch, floats here) and
# data/geom_C2_<triple>_S0_cen.json (written by ammann_dump.py = ammann_cell.py + float geometry; C2 = Rollerball, S0, centroid seeds).
# Checks printed, then FINAL ok.
import json, os, math
import numpy as np
from render3d import write, solid_part, basis
H = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(H, '..', 'data'); OUT = os.path.join(H, '..', 'html'); os.makedirs(OUT, exist_ok=True)
PHI = (1 + 5 ** .5) / 2
E6 = np.array([(0, 1, PHI), (0, -1, PHI), (1, PHI, 0), (-1, PHI, 0), (PHI, 0, 1), (-PHI, 0, 1)])
PEARL, BLUE, EDGE, LIGHT, GLASS = '#e2ded6', '#3a70cd', '#2b261e', '#efe6d0', '#cfd8dc'
SAND, SLATE = '#d6b46a', '#7f93a8'                                   # prolate / oblate: neutral tints
KIND = ['#d6b46a', '#9c7448', '#7f93a8', '#c99e95', '#8f8a80', '#b9b08a', '#a39cb0', '#8aa39a']   # kinds: neutral labels only
YCOL = '#ffffff'; LOG = []
P = json.load(open(os.path.join(D, '..', '..', 'data', 'patch.json'))); T = P['tiles']
G = {t: json.load(open(os.path.join(D, f'geom_C2_{t}_S0_cen.json'))) for t in ('012', '023', '024')}
for t, g in G.items(): assert g['valid'] and g['n_scutoid_pieces'] == 72 and g['n_Y'] == 30 and g['factor'] == 'S0' and g['seeds'] == 'cen'
S_ = G['012']['s']; assert all(abs(g['s'] - S_) < 1e-12 for g in G.values())
SC = 3 / S_                                                           # mould (edge s/3 |e|) -> patch cell (edge |e|)
def Ecorner(A, c): return [np.asarray(c) + 0.5 * sum(sg[i] * E6[a] for i, a in enumerate(A)) for sg in __import__('itertools').product((1, -1), repeat=3)]
for t, g in G.items():                                                 # every cell's geometry sits in the patch cell of its triple
    A = [int(ch) for ch in t]; M = np.array([E6[a] for a in A]).T; X = np.array(g['geom']['X']) * SC
    b = np.linalg.solve(M, X.T); assert abs(b).max() < 0.5 + 1e-9 and abs(abs(b).max() - 0.5) < 1e-9, (t, abs(b).max())
LOG.append(f'cells 012 (oblate), 023, 024 (prolate): all piece corners inside the golden rhombohedron of their triple, touching its walls; scale 3/s = {SC:.6f}')
def mesh_part(V, tris, cols, rad, ydots=(), alpha=1.0, ballrad=None):
    V = np.asarray(V, float); N = []
    for a, b, c in tris:
        n = np.cross(V[b] - V[a], V[c] - V[a]); N.append(n / np.linalg.norm(n))
    ed = {}
    for i, t in enumerate(tris):
        for k in range(3): ed.setdefault(frozenset((t[k], t[(k + 1) % 3])), []).append(i)
    tubes = []
    for e, L in ed.items():
        assert len(L) == 2, 'open surface'
        if N[L[0]] @ N[L[1]] < 1 - 1e-9: a, b = tuple(e); tubes.append([int(a), int(b), EDGE, None])
    parts = [{'v': np.round(V, 6).tolist(), 't': [list(map(int, t)) for t in tris], 'c': cols, 'a': alpha, 'tubes': tubes, 'rad': rad, 'balls': []}]
    if len(ydots): parts.append({'v': np.round(V[list(ydots)], 6).tolist(), 't': [], 'c': [], 'a': 1.0, 'tubes': [], 'rad': ballrad or rad * 5.0, 'balls': [[i, YCOL] for i in range(len(ydots))]})
    return parts
def ext(parts, dirv, pad=1.07):
    x, y, _ = basis(dirv); Pp = np.vstack([np.array(p['v']).reshape(-1, 3) for p in parts])
    return float(max(np.abs(Pp @ x).max(), np.abs(Pp @ y).max()) * pad)
def core_part(g, scale, shift, rad):
    """the Rollerball: 12 decagons pearl, 60 pyramid triangles blue (they are the icosahedron centre pyramids' faces)"""
    X = np.array(g['geom']['X'][:g['geom']['nC1']]) * scale + shift; V, T_, C = X, [], []
    for pc in g['geom']['pieces']:
        for poly, lab in pc['polys']:
            if lab != 'bottom': continue
            for a, b in zip(poly[1:-1], poly[2:]): T_.append([poly[0], a, b]); C.append(PEARL if len(poly) == 10 else BLUE)
    # orient each triangle outward
    for t in T_:
        n = np.cross(V[t[1]] - V[t[0]], V[t[2]] - V[t[0]])
        if n @ V[t[0]] < 0: t[1], t[2] = t[2], t[1]
    return mesh_part(V, T_, C, rad)
def kind_of(g): return {F: i for i, k in enumerate(g['kinds']) for F in k['members']}
def piece(g, pc, KO, scale, shift, rad, dots=True):
    X = np.array(g['geom']['X']) * scale; idx = sorted({v for t in pc['tris'] for v in t}); m = {v: i for i, v in enumerate(idx)}
    Y = set(g['geom']['Y']); cols = [KIND[KO[pc['F']]]] * len(pc['tris'])
    return mesh_part(X[idx] + shift, [[m[v] for v in t] for t in pc['tris']], cols, rad, ydots=[m[v] for v in idx if v in Y] if dots else ())
class Sol:
    def __init__(s, V, F):
        s.V = np.asarray(V, float); s.F = F; E = set()
        for _, _, o in F:
            for a, b in zip(o, o[1:] + o[:1]): E.add((min(a, b), max(a, b)))
        s.E = sorted(E)
    def vf(s): return s.V
def rhombo(A, centre, scale=1.0):
    """golden rhombohedron on e_A as a Sol: corners centre + scale*(+-e_a +-e_b +-e_c)/2, 6 parallelogram faces"""
    import itertools
    Ea = [E6[a] for a in A]; V = []; idx = {}
    for sg in itertools.product((1, -1), repeat=3): idx[sg] = len(V); V.append(np.asarray(centre) + scale * 0.5 * sum(s * e for s, e in zip(sg, Ea)))
    F = []
    for k in range(3):
        n = np.cross(Ea[(k + 1) % 3], Ea[(k + 2) % 3]); n /= np.linalg.norm(n)
        if n @ Ea[k] < 0: n = -n
        for s in (1, -1):
            pts = [sg for sg in idx if sg[k] == s]; c = np.mean([V[idx[q]] for q in pts], 0); a0 = V[idx[pts[0]]] - c; b0 = np.cross(n, a0)
            pts.sort(key=lambda q: math.atan2((V[idx[q]] - c) @ b0, (V[idx[q]] - c) @ a0)); F.append((s * n, (s * n) @ V[idx[pts[0]]], [idx[q] for q in pts]))
    return Sol(V, F)
# ---------------- 1. the patch ----------------
cen = np.array([t['centre'] for t in T]); order = np.argsort(np.linalg.norm(cen - cen[33], axis=1))[:30]   # 30 cells round tile 33 (a mixed patch: P : O close to phi)
pick = [T[i] for i in order]; nP = sum(t['kind'] == 'P' for t in pick); nO = 30 - nP
parts = []
for t in pick:
    A = t['A']; c = np.array(t['centre']); parts.append(solid_part(rhombo(A, c, 0.90), '#000000', faces=[], edge_col=SAND if t['kind'] == 'P' else SLATE, rad=0.0042))
    # a Rollerball at the centre (one orientation, one size; its scale in this patch cell)
    parts += core_part(G['023'] if t['kind'] == 'P' else G['012'], SC, c, 0.0016)
DIR1 = np.array([0.50, 0.38, 1.0]); E1 = ext(parts, DIR1, 1.05)
write(os.path.join(OUT, 'patch.html'), [{'E': E1, 'dir': DIR1.tolist(), 'parts': parts}])
LOG.append(f'patch.html: the 30 cells nearest tile 33: {nP} prolate + {nO} oblate, one Rollerball each (all one orientation, one size)')
# ---------------- 2. two cells ----------------
f = 0.85; DIR2 = np.array([0.36, 0.30, 1.0]); sc2 = []; cells = []; dirs = []
for t in ('023', '012'):
    g = G[t]; KO = kind_of(g); A = [int(ch) for ch in t]; assert len(g['kinds']) == 8
    ax = sum(E6[a] for a in A); ax /= np.linalg.norm(ax); tt = np.cross(ax, [0, 1, 0]); tt /= np.linalg.norm(tt); DIRc = ax * math.cos(math.radians(72)) + tt * math.sin(math.radians(72)); dirs.append(DIRc)   # nearly side-on to the 3-fold axis (72 deg), so the cell shapes differ
    Ssol = rhombo(A, np.zeros(3), g['s'] / 3 * (1 + f))
    ps = list(core_part(g, 1.0, 0.0, 0.0028))
    vt = 0
    for pc in g['geom']['pieces']:
        X = np.array(g['geom']['X']); idx = sorted({v for tr in pc['tris'] for v in tr}); cc = X[idx].mean(0)
        ps += piece(g, pc, KO, 1.0, f * cc, 0.0022)
    glass = solid_part(Ssol, GLASS, alpha=0.16, rad=0.0018, edge_col=LIGHT, faces=[k for k, (n, d, o) in enumerate(Ssol.F) if n @ DIRc < 0])
    ps.append(glass); cells.append(ps)
    assert {v for pc in g['geom']['pieces'] for tr in pc['tris'] for v in tr} >= set(g['geom']['Y']) and len(g['geom']['Y']) == 30
E2 = max(ext(ps, d_, 1.03) for ps, d_ in zip(cells, dirs))
write(os.path.join(OUT, 'cells.html'), [{'E': E2, 'dir': d_.tolist(), 'parts': ps} for ps, d_ in zip(cells, dirs)])
LOG.append('cells.html: prolate (023) and oblate (012) cell, Rollerball + 72 pieces moved out by 0.85 x their centres, 30 Y dots each, mould far side see-through')
# ---------------- 3. seams ----------------
def pos(n): return sum(n[k] * E6[k] for k in range(6))
def wall_pattern(g, c, plane_n, plane_d):
    """top polygons of the cell (patch units, centre c) lying on the plane: list of polygons (arrays of corner points)"""
    X = np.array(g['geom']['X']) * SC + c; out = []
    for pc in g['geom']['pieces']:
        for poly, lab in pc['polys']:
            if lab == 'top' and np.all(np.abs(X[poly] @ plane_n - plane_d) < 1e-7): out.append(X[poly])
    return out
def pick_pair(kinds, ta, tb):
    for i, j, corners in P['shared']:
        a, b = T[i], T[j]
        if a['kind'] + b['kind'] == kinds and tuple(a['A']) == ta and tuple(b['A']) == tb: return a, b, corners
    raise SystemExit('no pair')
def seam_scene(a, b, corners, DIRs, label):
    W = np.array([pos(n) for n in corners]); n = np.cross(W[1] - W[0], W[2] - W[0]); n /= np.linalg.norm(n); d = n @ W[0]; C0 = W.mean(0)
    ca, cb = np.array(a['centre']), np.array(b['centre']); assert (ca @ n - d) * (cb @ n - d) < 0                 # the two cells lie on opposite sides of the wall
    ga = G[''.join(map(str, a['A']))]; gb = G[''.join(map(str, b['A']))]
    pa, pb = wall_pattern(ga, ca, n, d), wall_pattern(gb, cb, n, d)
    pa = [q - C0 for q in pa]; pb = [q - C0 for q in pb]; W = W - C0
    area = lambda polys: sum(0.5 * np.linalg.norm(np.cross(q[1:-1] - q[0], q[2:] - q[0]).sum(0)) for q in polys)
    wallA = np.linalg.norm(np.cross(W[1] - W[0], W[3] - W[0])) if len(W) == 4 else 0
    ar = [area(pa), area(pb), wallA]
    v = DIRs / np.linalg.norm(DIRs); v = v if v @ n > 0 else -v
    def keyset(polys): return {tuple(sorted(tuple(np.round(p, 5)) for p in q)) for q in polys}
    match = keyset(pa) == keyset(pb)
    def sheet(polys, off, col, alpha, ecol, erad, eoff, sort=True):
        Vs, Ts, Es, ids = [], [], set(), {}
        def vid(p):
            k = tuple(np.round(p, 5))
            if k not in ids: ids[k] = len(Vs); Vs.append(np.asarray(p) + off * v)
            return ids[k]
        for q in polys:
            ii = [vid(p) for p in q]
            for x, y in zip(ii[1:-1], ii[2:]): Ts.append([ii[0], x, y])
            for x, y in zip(ii, ii[1:] + ii[:1]): Es.add((min(x, y), max(x, y)))
        parts = [{'v': np.round(Vs, 6).tolist(), 't': Ts, 'c': [col] * len(Ts), 'a': alpha, 'tubes': [], 'rad': erad, 'balls': []}]
        Ve = [np.asarray(p) + eoff * v for p in Vs]; Ve = [np.asarray(p) - off * v + eoff * v for p in Vs]
        parts.append({'v': np.round(Ve, 6).tolist(), 't': [], 'c': [], 'a': 1.0, 'tubes': [[int(x), int(y), ecol, None] for x, y in sorted(Es)], 'rad': erad, 'balls': []})
        return parts
    rim = {'v': np.round(W + 0.045 * v, 6).tolist(), 't': [], 'c': [], 'a': 1.0, 'tubes': [[0, 1, LIGHT, None], [1, 2, LIGHT, None], [2, 3, LIGHT, None], [3, 0, LIGHT, None]], 'rad': 0.0030, 'balls': []}
    sa = sheet(pa, 0.0, '#4a4339', 1.0, SAND, 0.0072, 0.030); sb = sheet(pb, 0.0, '#4a4339', 1.0, '#a9bccd', 0.0036, 0.062)
    pp = [sa[0], sa[1], sb[1], rim]
    # the tubes of B drawn thicker/lighter so that, where the patterns agree, both lines show together
    return pp, match, (len(pa), len(pb), ar), n
def find(kinds, A1, A2):
    for i, j, corners in P['shared']:
        a, b = T[i], T[j]
        if {tuple(a['A']), tuple(b['A'])} == {A1, A2} and a['kind'] + b['kind'] in kinds: return a, b, corners
    raise SystemExit('no pair')
sA = find(('OP', 'PO'), (0, 1, 2), (0, 2, 3)); sB = find(('PP',), (0, 2, 3), (0, 2, 4))
scen = []; info = []
for a, b, corners in (sA, sB):
    W = np.array([pos(nn) for nn in corners]); n = np.cross(W[1] - W[0], W[2] - W[0]); n /= np.linalg.norm(n)
    up = np.array([0.0, 1.0, 0.0]); t1 = np.cross(up, n); t1 /= np.linalg.norm(t1); t2 = np.cross(n, t1)
    view = n * math.cos(math.radians(22)) + t1 * math.sin(math.radians(22)) * 0.8 + t2 * math.sin(math.radians(22)) * 0.6
    pp, match, st, n = seam_scene(a, b, corners, view, '')
    scen.append((pp, view, match, st, a, b)); info.append((a['kind'] + b['kind'], match, st))
E3 = max(ext(pp, view, 1.07) for pp, view, *_ in scen)
write(os.path.join(OUT, 'seam.html'), [{'E': E3, 'dir': (v / np.linalg.norm(v)).tolist(), 'parts': pp} for pp, v, *_ in scen])
for (kk, match, st) in info: LOG.append(f'seam.html wall {kk}: patterns agree exactly = {match}; regions on the wall: cell A {st[0]}, cell B {st[1]}; area A {st[2][0]:.6f}, B {st[2][1]:.6f}, wall {st[2][2]:.6f}')
assert info[0][1] is False and info[1][1] is True
assert abs(info[0][2][2][0] - info[0][2][2][2]) < 1e-6 and abs(info[0][2][2][1] - info[0][2][2][2]) < 1e-6, 'tops do not cover the wall'
assert abs(info[1][2][2][0] - info[1][2][2][2]) < 1e-6 and abs(info[1][2][2][1] - info[1][2][2][2]) < 1e-6
json.dump({'pick': [[t['kind'], t['A']] for t in pick], 'nP': nP, 'nO': nO, 'seams': [[k, bool(m), s[0], s[1]] for k, m, s in info]}, open(os.path.join(OUT, 'info.json'), 'w'))
open(os.path.join(H, 'ammann_scenes.log'), 'w').write('\n'.join(LOG) + '\nFINAL ok\n'); print('\n'.join(LOG)); print('FINAL ok')
