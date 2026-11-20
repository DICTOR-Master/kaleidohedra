# DICTO · dictospheres.com — scenes for the rendered figures of the paper on Grünbaum's zone question at k = 10.
# Every solid is drawn from the exact data checked by get_exact.py (../data/get-exact.json, from the 2026-11-15 study's
# tile12.json and search6.json); every scene re-asserts what it shows, exactly in Z[φ] / Z^6, before any float is made:
#   tri.html    T, and GET A, GET B and the Hall/Inchbald solid with their four removed oblate cells (see-through) and the
#               inscribed cube that carries the four dimpled corners;
#   apart.html  GET A and GET B whole (back view) and pulled apart into their 16 golden rhombohedra (10 prolate, 6 oblate);
#   zones.html  the six zones of GET A and of GET B, each zone's 10 faces coloured, the rest see-through, the axis drawn;
#   tiling.html eight lattice translates of GET A and of GET B (a 2 × 2 × 2 block on a basis of face-neighbour vectors),
#               together and pulled apart.
#   Version 2 (20 Nov): lines behind any face are hidden (render3d.py), and GET B pulled apart is turned slightly so that no
#   face is seen nearly edge-on (two thin bright slivers in Version 1).
import json, os, itertools
import numpy as np
from getlib import *
from render3d import write

OUT = os.path.join(HERE, 'renders'); os.makedirs(OUT, exist_ok=True)
X = json.load(open(os.path.join(HERE, '..', 'data', 'get-exact.json')))
S6, T12 = load(); cands = S6['candidates_rank_le_3']
NM = {0: 'GET A', 1: 'GET B', 2: 'candidate 2'}
FO = {i: faces_from_json(cands[i]['faces']) for i in (0, 1, 2)}
COL = {0: '#c8952a', 1: '#9ea4ad', 2: '#9a8f7e'}          # GET A gold (DICTO's), GET B silver, Hall/Inchbald solid stone: labels only
OBL = {0: '#ecd9a0', 1: '#d9dce1'}                         # oblate cells in the pulled-apart views: a paler tint of the same colour
GLASS, EDGE, LOG = '#efe9dc', '#2b261e', []
B = X['basis']

def surf(Fo, col, shift=np.zeros(3), alpha=1.0, rad=0.004, edge=EDGE, fcols=None):
    """a surface (oriented face dict) as a render part: two triangles per rhombus, every side as a tube"""
    pts = sorted({c for f in Fo for c in corners(*f)}); ix = {p: i for i, p in enumerate(pts)}
    V = np.array([posf(p) for p in pts]) + shift
    tris, cols = [], []
    for f in Fo:
        c = [ix[x] for x in corners(*f)]; cc = fcols[f] if fcols else col
        tris += [[c[0], c[1], c[2]], [c[0], c[2], c[3]]]; cols += [cc, cc]
    E = sorted({(min(ix[e[0]], ix[padd(e[0], unit(e[1]))]), max(ix[e[0]], ix[padd(e[0], unit(e[1]))])) for f in Fo for e in edges_of(*f)})
    return {'v': np.round(V, 6).tolist(), 't': tris, 'c': cols, 'a': alpha, 'tubes': [[a, b, edge, None] for a, b in E], 'rad': rad, 'balls': []}

def lines(P, pairs, col, rad=0.003):
    return {'v': np.round(np.array(P), 6).tolist(), 't': [], 'c': [], 'a': 1.0, 'tubes': [[a, b, col, None] for a, b in pairs], 'rad': rad, 'balls': []}

def centre(Fo): return np.array([posf(c) for c in {c for f in Fo for c in corners(*f)}]).mean(0)

def unitv(v): v = np.asarray(v, float); return v / np.linalg.norm(v)

def tilt(d, k=0.35):
    d = unitv(d); o = np.cross(d, [0.3, 1, 0.2]); return unitv(d + k * unitv(o))

def ext(parts, c): return max(np.linalg.norm(np.array(p['v']) - c, axis=1).max() for p in parts if p['v']) * 1.06

def cells_of(i): return [(tuple(p), tuple(t)) for p, t in X[NM[i]]['cells']]

# ---------- Figure 1: T, and the three dimpled triacontahedra with their removed cells and the cube of the dimples ----------
sc = []
TF = None; VIEW = {}
for i in (0, 1, 2):
    r = X[NM[i]]; Fo = FO[i]; rem = [(tuple(p), tuple(t)) for p, t in r['removed']]
    # exact: solid ∪ four removed cells = T + t (oriented boundary of the solid plus the cells' faces, interior faces cancelling)
    acc = dict(Fo)
    for f, s in boundary(rem).items(): acc[f] = acc.get(f, 0) + s
    acc = {f: s for f, s in acc.items() if s}
    assert len(acc) == 30 and len(zones(acc)) == 6 and all(z[0] == 10 for z in zones(acc).values())
    assert surface_stats(acc)['valence'] == [3, 5]                  # it is the triacontahedron: 20 three-valent, 12 five-valent corners
    if i == 0: TF = acc; c0 = centre(acc)
    c = centre(acc); dm = np.array([posf(tuple(p)) for p in r['dimples']])
    cube = [tuple(p) for p in r['cube']]; cp = [posf(p) for p in cube]
    cpairs = [(a, b) for a, b in itertools.combinations(range(8), 2) if vdot(pos(psub(cube[a], cube[b])), pos(psub(cube[a], cube[b]))) == (4, 4)]
    assert len(cpairs) == 12 and all(tuple(p) in cube for p in r['dimples'])
    m = dm.mean(0) - c
    d = tilt(m if np.linalg.norm(m) > 0.5 else dm[0] - c, 0.45)
    R0 = np.linalg.norm(np.array([posf(q) for q in {x for f in Fo for x in corners(*f)}]) - c, axis=1).max()
    parts = [surf(Fo, COL[i], -c)]
    for cl, dp in zip(rem, dm):                       # each removed cell drawn pulled out of its dimple, see-through
        parts.append(surf(boundary([cl]), GLASS, -c + 0.42 * R0 * unitv(dp - c), alpha=0.38, rad=0.0025, edge='#8a8070'))
    sc.append({'E': ext(parts, np.zeros(3)), 'dir': d.tolist(), 'parts': parts, 'name': NM[i]}); VIEW[i] = d.tolist()
    LOG.append(f'{NM[i]}: solid + 4 removed oblate cells = T exactly (30 faces, six zones of 10, corners of valence 3 and 5); dimples on one inscribed cube ({r["dimple_kind"]})')
# T itself, first panel, same view as GET A
partsT = [surf(TF, '#7d7568', -c0)]
sc.insert(0, {'E': sc[0]['E'], 'dir': sc[0]['dir'], 'parts': partsT, 'name': 'T'})
write(os.path.join(OUT, 'tri.html'), sc); LOG.append(f'tri.html: {len(sc)} scenes')

# ---------- Figure 2: whole (back) and pulled apart into 16 golden rhombohedra ----------
sc = []
pro = X['T']['prolate_volume']
for i in (0, 1):
    cl = cells_of(i); Fo = FO[i]
    assert boundary(cl) == Fo and len(cl) == 16
    c = centre(Fo); d = -np.array(VIEW[i])
    if i == 1:   # Version 2: GET B turned by at most 10 degrees so that no face of the pulled-apart cells is seen nearly edge-on
        nrm = [unitv(np.cross(np.subtract(posf(corners(*f)[1]), posf(corners(*f)[0])), np.subtract(posf(corners(*f)[3]), posf(corners(*f)[0]))))
               for p, t in cl for f in boundary([(p, t)])]
        mc = lambda v: min(abs(n @ unitv(v)) for n in nrm)
        e1 = unitv(np.cross(d, [0, 1, 0])); e2 = unitv(np.cross(d, e1)); m0 = mc(d)
        d = max((unitv(unitv(d) + np.tan(np.radians(a)) * (np.cos(np.radians(b)) * e1 + np.sin(np.radians(b)) * e2))
                 for a in (0, 2, 4, 6, 8, 10) for b in range(0, 360, 10)), key=mc)
        assert mc(d) > 0.12, mc(d)
        LOG.append(f'GET B pulled apart: view turned so the most edge-on face has |cos| {mc(d):.3f} (was {m0:.3f})')
    whole = [surf(Fo, COL[i], -c)]
    apart = []
    for p, t in cl:
        cc = np.array(posf(p)) + 0.5 * sum(np.array(posf(unit(k))) for k in t)
        sh = -c + 0.55 * (cc - c)
        isp = tuple(cell_volume(t)) == tuple(pro)
        apart.append(surf(boundary([(p, t)]), COL[i] if isp else OBL[i], sh, rad=0.0032))
    E = ext(apart, np.zeros(3))
    sc.append({'E': E, 'dir': d.tolist(), 'parts': whole}); sc.append({'E': E, 'dir': d.tolist(), 'parts': apart})
    LOG.append(f'{NM[i]}: 16 cells, boundary = the 30 faces exactly; {sum(tuple(cell_volume(t)) == tuple(pro) for _, t in cl)} prolate drawn {COL[i]}, the rest oblate {OBL[i]}')
write(os.path.join(OUT, 'apart.html'), sc); LOG.append(f'apart.html: {len(sc)} scenes')

# ---------- Figure 3: the six zones ----------
sc = []
for i in (0, 1):
    Fo = FO[i]; z = zones(Fo); c = centre(Fo)
    for dd in range(N):
        n, cyc, Z = z[dd]; assert n == 10 and cyc
        ax = unitv(posf(unit(dd)))
        side = unitv(np.cross(ax, [0.2, 0.9, 0.4])); d = unitv(side + 0.55 * ax)
        on = surf({f: s for f, s in Fo.items() if f in Z}, COL[i], -c)
        off = surf({f: s for f, s in Fo.items() if f not in Z}, '#5d574d', -c, alpha=0.22, rad=0.0025, edge='#6d6455')
        R = np.linalg.norm(np.array(on['v']), axis=1).max()
        axl = lines([(-1.25 * R * ax).tolist(), (1.25 * R * ax).tolist()], [(0, 1)], '#e9e2d0', 0.004)
        sc.append({'E': R * 1.3, 'dir': d.tolist(), 'parts': [off, on, axl]})
    LOG.append(f'{NM[i]}: six zones, each one closed belt of 10 faces')
write(os.path.join(OUT, 'zones.html'), sc); LOG.append(f'zones.html: {len(sc)} scenes')

# ---------- Figure 4: a 2 x 2 x 2 block of lattice translates ----------
TONES = {0: ['#c8952a', '#9c7424', '#e0b75a', '#7f6230', '#d6a646', '#a8854a', '#ebcf86', '#6e5426'],
         1: ['#9ea4ad', '#757b86', '#c3c7cd', '#5f6570', '#8b919b', '#b2b6bd', '#828893', '#d3d6db']}
sc = []
for i in (0, 1):
    Fo = FO[i]; nb = [tuple(v) for v in X[NM[i]]['neighbour_vectors']]
    assert len(nb) == 14 and all(lattice_member(B, v) is not None for v in nb)
    # three face-neighbour vectors that form a basis of the lattice (index 1), as short as possible in space
    best = None
    for tri in itertools.combinations(nb, 3):
        cs = [lattice_member(B, v) for v in tri]
        dt = abs(cs[0][0] * (cs[1][1] * cs[2][2] - cs[1][2] * cs[2][1]) - cs[0][1] * (cs[1][0] * cs[2][2] - cs[1][2] * cs[2][0]) + cs[0][2] * (cs[1][0] * cs[2][1] - cs[1][1] * cs[2][0]))
        if dt != 1: continue
        L = sum(np.linalg.norm(posf(v)) for v in tri)
        if best is None or L < best[0] - 1e-9: best = (L, tri)
    tri = best[1]
    # each of the three shares faces with the solid, face to face (exact): a face of P is the opposite face of P + v
    for v in tri:
        sh = sum(1 for (q, a, b), s in Fo.items() if Fo.get((psub(q, v), a, b)) == -s)
        assert sh >= 1, v
    offs = [tuple(sum(n[k] * tri[k][j] for k in range(3)) for j in range(N)) for n in itertools.product((0, 1), repeat=3)]
    # no two tiles of the block share a face with the same outward side (they would overlap)
    for u, w in itertools.combinations(offs, 2):
        dv = psub(w, u); assert not any(Fo.get((psub(q, dv), a, b)) == s for (q, a, b), s in Fo.items())
    c0 = centre(Fo); m = np.mean([posf(o) for o in offs], axis=0)
    d = tilt([0.42, 0.55, 0.72], 0.0)
    for k in (0.0, 0.42):
        parts = []
        for j, o in enumerate(offs):
            sh = (np.array(posf(o)) - m) * (1 + k) - c0
            parts.append(surf(Fo, TONES[i][j], sh, rad=0.0026))
        sc.append({'E': ext(parts, np.zeros(3)), 'dir': d.tolist(), 'parts': parts})
    LOG.append(f'{NM[i]}: block on the face-neighbour basis {tri} (lattice index 1), each basis vector a face contact, no two tiles with a common face on the same side')
write(os.path.join(OUT, 'tiling.html'), sc); LOG.append(f'tiling.html: {len(sc)} scenes')
open(os.path.join(HERE, '..', 'data', 'fig-scenes.log'), 'w').write('\n'.join(LOG) + '\nFINAL ok\n'); print('\n'.join(LOG)); print('FINAL ok')
