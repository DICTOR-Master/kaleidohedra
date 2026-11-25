#!/usr/bin/env python3
"""Figures 4 and 5 of the packets blueprint, in the house card style of the gold-standard figures (#118):
Figure 4: the nine pieces of Definition G (the two centre pyramids, the truncated icosahedron and dodecahedron, and the five
          helpers), rendered by the house three.js renderer (render3d.py of study 2026-11-21-amber-ammann);
Figure 5: lead 2 of Theorem 4 as a strip of angles from 0 to 540 degrees, the companion of Figure 3 (lead 1), angles from #117's
          data/fig-ring.json (computed and asserted there from exact values).
Stage A (python, here): writes renders/pieces.html and checks every solid (equal edges; a pyramid = one face + the centre).
Stage B (node shots.mjs renders/pieces.html renders/pieces) then stage C (python fig_pieces.py compose)."""
import os, sys, json, math, itertools
import numpy as np
from scipy.spatial import ConvexHull
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(H, '..'); R = os.path.join(ROOT, 'renders'); os.makedirs(R, exist_ok=True)
AA = os.path.join(H, '..', '..', '..', 'studies', '2026-11-21-amber-ammann', 'renders', 'scripts')
sys.path.insert(0, AA)
from render3d import write, solid_part

PHI = (1 + 5 ** 0.5) / 2
def perms(v): return {tuple(p) for p in itertools.permutations(v)}
def evenp(v): return {(v[0], v[1], v[2]), (v[1], v[2], v[0]), (v[2], v[0], v[1])}
def signs(v): return {tuple(s * x for s, x in zip(sg, v)) for sg in itertools.product((1, -1), repeat=3)}
def pts(*sets): return np.array(sorted({tuple(np.round(q, 12)) for s_ in sets for q in s_}), float)

class Solid:
    """corners, faces (normal, offset, ordered corner indices) and edges from the convex hull"""
    def __init__(self, P):
        self.P = np.asarray(P, float); h = ConvexHull(self.P); g = {}
        for s, e in zip(h.simplices, h.equations): g.setdefault(tuple(np.round(e, 7)), set()).update(int(i) for i in s)
        self.F = []
        for e, idx in g.items():
            n = np.array(e[:3]); idx = sorted(idx); c = self.P[idx].mean(0); u = self.P[idx[0]] - c; u /= np.linalg.norm(u); w = np.cross(n, u)
            o = sorted(idx, key=lambda i: math.atan2((self.P[i] - c) @ w, (self.P[i] - c) @ u))
            self.F.append((n, -e[3], o))
        self.E = sorted({(min(o[j], o[(j + 1) % len(o)]), max(o[j], o[(j + 1) % len(o)])) for _, _, o in self.F for j in range(len(o))})
    def vf(self): return self.P

def uniform(P, name, nE):
    S = Solid(P); L = [float(np.linalg.norm(S.P[a] - S.P[b])) for a, b in S.E]
    assert len(S.E) == nE and max(L) - min(L) < 1e-9, (name, len(S.E), min(L), max(L))
    return S

dod = uniform(pts(signs((1, 1, 1)), *[signs(p) for p in evenp((0, 1 / PHI, PHI))]), 'dodecahedron', 30)
ico = uniform(pts(*[signs(p) for p in evenp((0, 1, PHI))]), 'icosahedron', 30)
ti = uniform(pts(*[signs(p) for v in [(0, 1, 3 * PHI), (1, 2 + PHI, 2 * PHI), (PHI, 2, PHI ** 3)] for p in evenp(v)]), 'truncated icosahedron', 90)
td = uniform(pts(*[signs(p) for v in [(0, 1 / PHI, 2 + PHI), (1 / PHI, PHI, 2 * PHI), (PHI, 2, PHI + 1)] for p in evenp(v)]), 'truncated dodecahedron', 90)
to = uniform(pts(*[signs(p) for p in perms((0, 1, 2))]), 'truncated octahedron', 36)
tco = uniform(pts(*[signs(p) for p in perms((1, 1 + 2 ** 0.5, 1 + 2 * 2 ** 0.5))]), 'truncated cuboctahedron', 72)
tid = uniform(pts(*[signs(p) for v in [(1 / PHI, 1 / PHI, 3 + PHI), (2 / PHI, PHI, 1 + 2 * PHI), (1 / PHI, PHI ** 2, -1 + 3 * PHI),
                                         (2 * PHI - 1, 2, 2 + PHI), (PHI, 3, 2 * PHI)] for p in evenp(v)]), 'truncated icosidodecahedron', 180)

def centre_pyramid(S, k):
    """the centre pyramid of S on a k-gon face: that face and the centre O"""
    o = next(o for _, _, o in S.F if len(o) == k)
    P = np.vstack([S.P[o], np.zeros(3)]); Q = Solid(P); assert len(Q.F) == k + 1
    return Q

pyrD, pyrI = centre_pyramid(dod, 5), centre_pyramid(ico, 3)

def fit(S):   # centre at the corner centroid, circumradius 1
    P = S.P - S.P.mean(0); S.P = P / np.max(np.linalg.norm(P, axis=1)); return S

VIOLET, BLUE, PEARL, SILVER, CREAM, GREEN, RED, GOLD = '#7a50b4', '#3a70cd', '#e2ded6', '#bdb8aa', '#d9c9a3', '#79a86c', '#c0645a', '#c9a14a'
PIECES = [(pyrD, VIOLET, 'dodecahedron centre pyramid', 'pyrDSet'), (ti, PEARL, 'truncated icosahedron', 'tiSet'),
          (pyrI, BLUE, 'icosahedron centre pyramid', 'pyrISet'), (td, SILVER, 'truncated dodecahedron', 'tdSet'),
          (dod, VIOLET, 'dodecahedron (helper)', 'dhSet'), (ico, BLUE, 'icosahedron (helper)', 'ihSet'),
          (to, CREAM, 'truncated octahedron (helper)', 'toSet'), (tco, CREAM, 'truncated cuboctahedron (helper)', 'tcoSet'),
          (tid, SILVER, 'truncated icosidodecahedron (helper)', 'tidSet')]
DIR = np.array([0.55, 0.42, 1.0]); DIR /= np.linalg.norm(DIR)

if __name__ == '__main__' and (len(sys.argv) < 2 or sys.argv[1] == 'scenes'):
    sc = []
    for S, col, nm, lean in PIECES:
        S = fit(S); sc.append({'E': 1.18, 'dir': DIR.tolist(), 'parts': [solid_part(S, col, rad=0.007)]})
    write(os.path.join(R, 'pieces.html'), sc)
    json.dump([[nm, lean, len(S.F), len(S.E), len(S.P)] for S, _, nm, lean in PIECES], open(os.path.join(R, 'pieces.json'), 'w'), indent=1)
    print('pieces', [(nm, len(S.F), len(S.E), len(S.P)) for S, _, nm, _ in PIECES]); print('FINAL ok scenes')

if __name__ == '__main__' and len(sys.argv) > 1 and sys.argv[1] == 'compose':
    SS = os.path.join(H, '..', '..', '..', 'studies', '2026-11-21-scutoid-stand-in', 'renders', 'scripts', 'compose.py')
    src = open(SS).read(); OUTF = os.path.join(ROOT, 'figures')
    exec(src[:src.index("s = lambda sc, i")].replace("H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, 'renders'); OUT = os.path.join(H, 'figures')",
                                                     "R = os.path.join(ROOT, 'renders'); OUT = os.path.join(ROOT, 'figures')"))
    info = json.load(open(os.path.join(R, 'pieces.json')))
    hexc = lambda h: tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
    rows = [[(os.path.join(R, 'pieces', f'p{3 * r + c}.png'), info[3 * r + c][0], f"{info[3 * r + c][1]} · {info[3 * r + c][2]} faces, {info[3 * r + c][3]} edges")
             for c in range(3)] for r in range(3)]
    figure('fig-pieces.png', 'The nine pieces of Theorem 4',
           'Definition G: each piece built from exact coordinates in the Lean files (its Lean set beneath) · the two cancelling pairs on top, the five helpers below · drawn to one size',
           rows, [(hexc(VIOLET), 'dodecahedral family'), (hexc(BLUE), 'icosahedral family'), (hexc(PEARL), 'truncated icosahedron'),
                  (hexc(SILVER), 'truncated (ico)dodecahedra'), (hexc(CREAM), 'octahedral helpers')], cell=640)
    # Figure 5: lead 2 as a strip, the companion of Figure 3
    L2 = json.load(open(os.path.join(ROOT, '..', '2026-11-21-dehn-packets', 'data', 'fig-ring.json')))['lead2']
    tot = sum(a for _, a in L2); assert abs(tot - 540) < 1e-9, tot
    first3 = sum(a for _, a in L2[:3]); gap = 360 - first3
    COL = {'pyramid base': hexc(BLUE), 'TD tri–dec': (189, 184, 170), 'TD dec–dec': (139, 135, 124)}
    Wd, Hd = 2400 * K // 2, 1000 * K // 2
    im = Image.new('RGB', (Wd, Hd), BG); d = ImageDraw.Draw(im); s_ = K / 2
    d.text((80 * s_, 44 * s_), 'Lead 2: also one and a half turns', font=f(64 * s_, True), fill=INK)
    d.text((80 * s_, 126 * s_), 'Theorem 4 (c), ring3pi_lead2: the icosahedron centre pyramid with the truncated dodecahedron · the angles at one edge, laid end to end', font=fit(d, 'x' * 120, f(28 * s_), Wd - 160 * s_), fill=MUTE)
    sx0, sx1, sy = 100 * s_, 2300 * s_, 520 * s_; sc_ = (sx1 - sx0) / 540.0; d0 = 0.0
    RED_ = (214, 88, 72)
    for nm, a in L2:
        d.rectangle((sx0 + d0 * sc_, sy - 90 * s_, sx0 + (d0 + a) * sc_, sy + 20 * s_), fill=COL[nm], outline=(43, 38, 30), width=int(3 * s_))
        ctext(d, sx0 + (d0 + a / 2) * sc_, sy - 62 * s_, f'{a:.2f}°', f(36 * s_, True), (20, 15, 11) if nm != 'pyramid base' else (240, 236, 255), a * sc_)
        d0 += a
    d.rectangle((sx0 + 360 * sc_, sy - 90 * s_, sx1, sy + 20 * s_), outline=RED_, width=int(6 * s_))
    d.line((sx0 + 360 * sc_, sy - 140 * s_, sx0 + 360 * sc_, sy + 60 * s_), fill=RED_, width=int(6 * s_))
    d.text((sx0 + 360 * sc_ - 200 * s_, sy - 190 * s_), 'one full turn, 360°', font=f(32 * s_, True), fill=RED_)
    d.text((sx0, sy - 190 * s_), f'the first three fill {first3:.2f}°, leaving {gap:.2f}°', font=f(32 * s_), fill=INK)
    d.text((sx0, sy + 100 * s_), f'the next two bring {L2[3][1] + L2[4][1]:.2f}°: 180° beyond one turn, so the ring cannot close round an edge', font=f(32 * s_), fill=RED_)
    d.text((sx0, sy + 44 * s_), '0°', font=f(30 * s_), fill=MUTE); d.text((sx1 - 80 * s_, sy + 44 * s_), '540°', font=f(30 * s_), fill=MUTE)
    for k, (col, txt) in enumerate([(COL['pyramid base'], 'icosahedron centre pyramid: base angle'), (COL['TD tri–dec'], 'truncated dodecahedron: triangle–decagon'), (COL['TD dec–dec'], 'truncated dodecahedron: decagon–decagon')]):
        swatch(d, 100 * s_ + (k % 2) * 1100 * s_, (740 + 60 * (k // 2)) * s_, col, txt, f(28 * s_))
    d.text((Wd - 80 * s_ - d.textlength(MARK, font=f(24 * s_)), Hd - 56 * s_), MARK, font=f(24 * s_), fill=MUTE)
    im.save(os.path.join(OUTF, 'fig-lead2-strip.png'), optimize=True)
    print('FINAL ok compose', round(first3, 4), round(gap, 4))
