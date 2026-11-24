"""Exact renders of the RVCMG adapter pieces (house renderer render3d.write; frames by shots.mjs).
Coordinates: data/exact_pieces.json (the exact model of scripts/rvcmg_exact.py, evaluated to 60 digits, then to float for drawing).
Hexagon end pale silver, target end cream, lateral faces neutral blue-grey; every edge of the flat solid drawn (two wall triangles in one
plane are drawn as one face); gold balls = target corners with four edges in the bent-wall reading (one face per hexagon edge) (where Y-corners sit merged into the end).
Hexagon end at the bottom. Usage: python pieces_render.py <study dir> <out.html>"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../2026-11-21-scutoid-stand-in/renders/scripts"))
from render3d import write
ST, OUT = sys.argv[1:3]
EX = json.load(open(os.path.join(ST, 'data/exact_pieces.json')))
VD = json.load(open(os.path.join(ST, 'data/verdicts.json')))['verdicts']
ORDER = ['RVCMG_V2_TRIANGLE_TO_UHEX', 'RVCMG_V2_SQUARE_TO_UHEX', 'RVCMG_V2_PENTAGON_TO_UHEX', 'RVCMG_V2_GOLDEN_RHOMBUS_TO_UHEX',
         'RVCMG_V2_RD_NATIVE_RHOMBUS_TO_UHEX', 'RVCMG_V2_DI_KITE_TO_UHEX', 'RVCMG_V2_DH_KITE_TO_UHEX', 'RVCMG_V2_REGULAR_HEX_TO_UHEX',
         'RVCMG_TRIANGLE_TO_RDH', 'RVCMG_SQUARE_TO_RDH', 'RVCMG_PENTAGON_TO_RDH', 'RVCMG_GOLDEN_RHOMBUS_TO_RDH',
         'RVCMG_DI_KITE_TO_RDH', 'RVCMG_DH_KITE_TO_RDH', 'RVCMG_REGULAR_HEX_TO_RDH', 'RVCMG_RD_HEMI']
HEXC, TOPC, LATC, EDGE, OUTL, GOLD = '#d9dde3', '#efe3c2', '#9fb1c4', '#2a3340', '#11161f', '#e0b84a'
scenes = []
for pid in ORDER:
    P = np.array(EX[pid]['vertices_float']); F = EX[pid]['faces']
    ends = EX[pid].get('ends', [0, 1])
    n0 = np.cross(P[F[ends[0]][1]] - P[F[ends[0]][0]], P[F[ends[0]][2]] - P[F[ends[0]][0]]); n0 /= np.linalg.norm(n0)
    if np.dot(P.mean(0) - P[F[ends[0]]].mean(0), n0) < 0: n0 = -n0        # n0 points from the hexagon end into the solid
    # frame: n0 -> screen up (y)
    a = np.cross(n0, [1, 0, 0]); a = a if np.linalg.norm(a) > 1e-6 else np.cross(n0, [0, 1, 0]); a /= np.linalg.norm(a); b = np.cross(a, n0)
    Q = (P - P.mean(0)) @ np.array([a, n0, b]).T
    Q = Q / np.abs(Q).max() * 0.82
    T, C = [], []
    for fi, f in enumerate(F):
        col = HEXC if fi == ends[0] else TOPC if fi == ends[1] else LATC
        for k in range(1, len(f) - 1): T.append([f[0], f[k], f[k + 1]]); C.append(col)
    def normal(f):
        v = np.cross(Q[f[1]] - Q[f[0]], Q[f[2]] - Q[f[0]]); return v / np.linalg.norm(v)
    ef = {}
    for fi, f in enumerate(F):
        for k in range(len(f)): ef.setdefault(tuple(sorted((f[k], f[(k + 1) % len(f)]))), []).append(fi)
    tubes = [[e[0], e[1], EDGE, OUTL] for e, fs in ef.items() if abs(abs(np.dot(normal(F[fs[0]]), normal(F[fs[1]]))) - 1) > 1e-9]
    deg = VD[pid].get('bent', VD[pid]['flat'])['degrees']; top = set(F[ends[1]])   # merged corners: four edges in the bent-wall reading
    balls = [[i, GOLD] for i in range(len(Q)) if i in top and deg[i] >= 4]
    part = {'v': np.round(Q, 6).tolist(), 't': T, 'c': C, 'a': 1, 'tubes': tubes, 'rad': 0.012, 'balls': []}
    gold = {'v': np.round(Q, 6).tolist(), 't': [], 'c': [], 'a': 1, 'tubes': [], 'rad': 0.03, 'balls': balls}
    scenes.append({'E': 1.18, 'dir': [0.55, 0.62, 1.0], 'parts': [part, gold]})
write(OUT, scenes)
print('scenes', len(scenes), 'FINAL ok' if len(scenes) == 16 else 'FINAL FAIL')
