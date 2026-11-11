# Golden truncated triangles (DICTO 11-02): each dataset solid that has them, rendered with those faces gold, others grey; ratio in title.
# Same renderer as the Star Cores / #87 figures. Usage: tt_figs.py <dataset dir> <star-cores scripts dir> <out dir>
import sys, os, glob, numpy as np
DS, SC, OUT = [os.path.abspath(x) for x in sys.argv[1:4]]; sys.path.insert(0, SC)
sys.argv = [sys.argv[0], DS, OUT, os.path.expanduser('~/work/book/dicto-logo.png')]
import figs_paper_a as A
from star_core import load
import matplotlib.pyplot as plt
SOL = [('dicto-icosaxes-hexa.json', 'Icosaxes Hexa', 'φ'), ('dicto-white-knight.json', 'White Knight', 'φ'), ('dicto-icosaxes.json', 'Icosaxes', 'φ'),
       ('dicto-unborn-axes.json', 'Unborn Axes', 'φ'), ('dicto-ti-star-core.json', 'TI Star core', '√5'), ('dicto-gti.json', 'GTI', '1 + 3√5/5'),
       ('dicto-golden-clasp.json', 'Golden Clasp', 'φ⁴/2'), ('dicto-haigha.json', 'Haigha', '(1 + 2√5)/5'), ('dicto-hatta.json', 'Hatta', '(5 + 4√5)/11')]
def is_tt(P):
    L = [np.linalg.norm(P[(i + 1) % 6] - P[i]) for i in range(6)]
    ang = [np.degrees(np.arccos(np.clip(np.dot(P[i - 1] - P[i], P[(i + 1) % 6] - P[i]) / (np.linalg.norm(P[i - 1] - P[i]) * np.linalg.norm(P[(i + 1) % 6] - P[i])), -1, 1))) for i in range(6)]
    t = 1e-6 * max(L)
    return all(abs(a - 120) < 1e-6 for a in ang) and all(abs(L[i] - L[(i + 2) % 6]) < t for i in range(6)) and abs(L[0] - L[1]) > t
fig, axs = plt.subplots(3, 3, figsize=(10, 10.6), gridspec_kw=dict(wspace=0.02, hspace=0.14)); M = A.rot(*A.VIEW)
for ax, (fn, nm, r) in zip(axs.flat, SOL):
    _, V, F = load(os.path.join(DS, 'solids', fn)); V = np.array(V, float); V -= V.mean(0)
    cols = []; n_tt = 0; tt_n = None
    for f in F:
        t = len(f) == 6 and is_tt(V[f]); n_tt += t; cols.append(A.GOLD if t else '#c9ccd3')
        if t and tt_n is None: c = V[f].mean(0); tt_n = c / np.linalg.norm(c)
    Mv = M
    if n_tt <= 4 and tt_n is not None:   # few golden faces: turn the solid so one looks at the viewer, slightly tilted
        z = tt_n; xa = np.cross([0.3, 0.5, 0.81], z); xa /= np.linalg.norm(xa); ya = np.cross(z, xa)
        Rt = np.array([xa, ya, z]); a = np.radians(20); Tilt = np.array([[1, 0, 0], [0, np.cos(a), -np.sin(a)], [0, np.sin(a), np.cos(a)]])
        Mv = Tilt @ Rt
    S = A.Scene(Mv); S.tris(V, [list(f) for f in F], cols); S.draw(ax, 1.08 * np.linalg.norm(V, axis=1).max())
    ax.set_title(f'{nm}\n{n_tt} faces, long/short = {r}', fontsize=9)
fig.suptitle("Golden truncated triangles in DICTO's solids (gold): every 3-fold hexagonal face in the dataset", fontsize=11)
A.mark(fig); fig.savefig(os.path.join(OUT, 'golden-truncated-triangles.png'), dpi=220, facecolor='white'); print('written')
