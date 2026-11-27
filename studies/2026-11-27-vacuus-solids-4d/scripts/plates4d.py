"""Figures for Section 8 of the Vacuus-Solids draft (27 Nov 2026; DICTO: "I would like masses of beautiful figs for these shapes").
With Claude (Anthropic). For each Platonic solid P with its polar core c P* (c = 0.6 of the largest core that fits inside P; the pieces are the same for every c below that): the
Schlegel picture of the 4D hull conv(P x {0} u P* x {1}) (Proposition 3) drawn directly in 3D:
  pits     : face f of P joined to the core corner over f (pyramid on f),
  wedges   : edge e of P joined to its dual edge of the core (tetrahedron),
  corners  : corner v of P joined to its dual face of the core (pyramid onto a core face),
  core     : c P*.
Scenes per P: (0) assembled, outer shell see-through, core solid; (1) all pieces pulled apart (each moved out along its centre);
(2) one piece of each kind, side by side. Colours: P's and the core's app colours (they ARE those Platonic solids: D violet, I blue,
C green, T red, O yellow); the three kinds of join in neutral tones (abstract labels). Exact corners (floats of exact coordinates).
Every piece is checked to be convex with positive volume, and the volumes add up to P's volume (the pieces tile P)."""
import os, sys, itertools, json
import numpy as np
from scipy.spatial import ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../2026-11-21-scutoid-stand-in/renders/scripts'))
import render3d as R3
src = open(os.path.join(HERE, 'cayley4d.py')).read(); g = {'__file__': os.path.join(HERE, 'cayley4d.py')}
exec(src[:src.index('def hyper')], g)
solid, faces_all = g['solid'], g['faces_all']
APP = {'dodecahedron': '#8a5cc4', 'icosahedron': '#3a70cd', 'cube': '#488e48', 'tetrahedron': '#cd3e28', 'octahedron': '#e8c852'}
DUAL = {'dodecahedron': 'icosahedron', 'icosahedron': 'dodecahedron', 'cube': 'octahedron', 'octahedron': 'cube', 'tetrahedron': 'tetrahedron'}
KIND = {'pit': '#d9cdb4', 'wedge': '#9aa3a8', 'corner': '#c4b49a'}
EDGE = '#2b261e'; C = 0.42
def hull_part(P, col, alpha=1.0, rad=0.006):
    h = ConvexHull(P); eq = [tuple(np.round(q, 6)) for q in h.equations]; own = {}
    T = []
    for k, sm in enumerate(h.simplices):
        a, b, c = map(int, sm)
        if np.cross(P[b] - P[a], P[c] - P[a]) @ (P[a] - P.mean(0)) < 0: b, c = c, b
        T.append([a, b, c])
        for x, y in ((a, b), (b, c), (c, a)): own.setdefault(tuple(sorted((x, y))), set()).add(eq[k])
    tubes = [[x, y, EDGE, None] for (x, y), qs in own.items() if len(qs) > 1]
    return {'v': np.round(P, 6).tolist(), 't': T, 'c': [col] * len(T), 'a': alpha, 'tubes': tubes, 'rad': rad, 'balls': []}, h.volume
out_scenes, meta = [], []
for name in ('tetrahedron', 'cube', 'octahedron', 'dodecahedron', 'icosahedron'):
    V, F, D = solid(name)
    Vf = np.array([[float(x) for x in v] for v in V]); D0 = np.array([[float(x) for x in d] for d in D])
    # core corner c d is inside P iff u . (c d) <= 1 for every plane u of P (u runs over the polar corners): c <= 1 / max_u u . d
    cmax = min(1.0 / float((D0 @ d).max()) for d in D0)
    Df = 0.6 * cmax * D0
    pieces = []
    for S_, ks in faces_all(V, F):
        pts = np.vstack([Vf[sorted(S_)], Df[sorted(ks)]])
        kind = {1: 'corner', 2: 'wedge'}.get(len(S_), 'pit')
        pieces.append((kind, pts))
    vols = []; parts = []
    for kind, pts in pieces:
        p, vol = hull_part(pts, KIND[kind]); vols.append(vol); parts.append((kind, pts, p))
    core, vcore = hull_part(Df, APP[DUAL[name]], rad=0.007)
    shell, vP = hull_part(Vf, APP[name], alpha=0.22, rad=0.008)
    ok = abs(sum(vols) + vcore - vP) < 1e-9 * vP and min(vols) > 0
    R = np.linalg.norm(Vf, axis=1).max(); E = float(1.75 * R); dirv = [0.55, 0.35, 1.0]
        # (0) the Vacuus-Solid itself: the material between the pits (edge wedges and corner pyramids) half see-through, the core solid,
    #     the pits left open (they are the empty pits of the solid)
    asm = [core] + [dict(p, a=0.3) for k, _, p in parts if k != 'pit']
    # (1) pulled apart
    pulled = [dict(core)]
    for kind, pts, p in parts:
        c0 = pts.mean(0); sh = 1.8 * c0
        pulled.append(dict(p, v=np.round(np.array(p['v']) + sh, 6).tolist()))
    # (2) one of each kind, side by side
    one = []; xo = {'pit': -1.4 * R, 'wedge': 0.0, 'corner': 1.4 * R}
    for kind in ('pit', 'wedge', 'corner'):
        kind_pts = next(pts for k, pts in pieces if k == kind); c0 = kind_pts.mean(0)
        p, _ = hull_part(kind_pts - c0 + np.array([xo[kind], 0, 0]), KIND[kind], rad=0.01)
        one.append(p)
    out_scenes += [{'E': E, 'dir': dirv, 'parts': asm}, {'E': float(2.0 * E), 'dir': dirv, 'parts': pulled}, {'E': float(2.4 * R), 'dir': [0.2, 0.3, 1.0], 'parts': one}]
    cnt = {k: sum(1 for kk, _ in pieces if kk == k) for k in KIND}
    meta.append(dict(P=name, core=DUAL[name], core_scale=float(0.6 * cmax), pieces=cnt, volumes_add_up=bool(ok)))
    print(name, cnt, 'core', DUAL[name], '; pieces + core tile P exactly (volumes):', ok, flush=True)
os.makedirs(os.path.join(HERE, '../renders'), exist_ok=True)
R3.write(os.path.join(HERE, '../renders/plates4d.html'), out_scenes)
json.dump(meta, open(os.path.join(HERE, '../renders/plates4d.json'), 'w'), indent=1)
print('FINAL ok' if all(m['volumes_add_up'] for m in meta) and len(meta) == 5 else 'FINAL FAIL')
