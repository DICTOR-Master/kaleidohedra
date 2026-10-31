# Mock-up of DICTO's ring double pyramid (two tetrahedra face to face) in the style of the first ring mock-ups (DICTO 2026-10-31: "your
# first 2d drawings were much more accurate"): every big face of 4 rings (double scale, central ring the other way up), zip ties at
# 1/4 and 3/4 of each shared side. Closed = 24 rings; open = the 6 central rings left out (18 rings: a mini tetrahedron at each tip,
# a mini square pyramid at each waist corner).
# Usage (dicto-big-brother): LOGO=<dicto-logo.png> ~/geom/bin/python bipyramid_mockup.py  -> ../out/bipyramid-mockup.png
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import mockup as M
import matplotlib.pyplot as plt

W = [np.array([np.cos(a), np.sin(a), 0.0]) for a in np.radians([90, 210, 330])]
TOP, BOT = np.array([0, 0, 2 ** .5]), np.array([0, 0, -2 ** .5])
FACES = [(TOP, W[i], W[(i + 1) % 3]) for i in range(3)] + [(BOT, W[(i + 1) % 3], W[i]) for i in range(3)]

def model(open_):
    rings, ties = [], {}
    for A, Bc, C in FACES:
        n = np.cross(Bc - A, C - A); n /= np.linalg.norm(n)
        if n @ (A + Bc + C) < 0: n = -n
        ab, bc, ca = (A + Bc) / 2, (Bc + C) / 2, (C + A) / 2
        sub = [(A, ab, ca), (ab, Bc, bc), (ca, bc, C)] + ([] if open_ else [(bc, ca, ab)])
        for X in sub:
            o, i = M.ring_band(X); c = np.mean(X, 0)
            rings.append(dict(outer=o, inner=i, n=n, c=c))
            for k in range(3):
                for s in (.25, .75):
                    p = X[k] + (X[(k + 1) % 3] - X[k]) * s
                    ties.setdefault(tuple(np.round(p, 6)), []).append((c, n))
    bars = []
    for p, cs in ties.items():
        if len(cs) != 2: continue                      # an open side: no tie
        p = np.array(p); a, b = [p + (c - p) / np.linalg.norm(c - p) * 0.07 for c, n in cs]
        bars.append((np.array([a, p, b]), cs[0][1] + cs[1][1]))
    return rings, bars, []

if __name__ == '__main__':
    BG = '#f4f4f2'; V = [('three-quarter view', M.View(22, -58)), ('side view', M.View(0.5, -90)), ('top view', M.View(89.5, -90))]
    fig = plt.figure(figsize=(15, 10.5), facecolor=BG)
    for j, (open_, nm) in enumerate([(False, 'closed · 24 rings'), (True, 'open · 18 rings (central rings left out)')]):
        mdl = model(open_); nt = len(mdl[1])
        for k, (vn, v) in enumerate(V):
            ax = fig.add_axes([0.01 + k * 0.33, 0.52 - j * 0.47, 0.32, 0.40])
            M.draw(ax, 'c', mdl, v, f'{nm} · {nt} zip ties · {vn}' if k == 0 else vn, lw_tie=1.3)
    fig.suptitle('Ring double pyramid (two tetrahedra face to face) · each big triangle = 4 rings, the central one the other way up',
                 fontsize=14, color='#222', y=0.975)
    M.logo(fig, 0.945, 0.045)
    fig.savefig(os.path.join(M.OUT, 'bipyramid-mockup.png'), dpi=150, facecolor=BG); print('saved')
