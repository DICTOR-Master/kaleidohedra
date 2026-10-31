# All views of the ring h-tile (DICTO 2026-10-31 "i need all views of 3D object"), drawn with the first mock-up's rings, coloured by
# part: the double pyramid's 18 outside rings (gold), the two half-octahedra's 15 rings each (blue, violet). Same scale as DICTO's
# build (a tetrahedron = 16 rings). Usage (dicto-big-brother): LOGO=<dicto-logo.png> ~/geom/bin/python htile_views.py
import os, sys, inspect
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import mockup as M, build as B, exactfaces as E
from tiles import tile
import matplotlib.pyplot as plt
M.TINT.update(bp=np.array([0.93, 0.80, 0.45]), o1=np.array([0.55, 0.72, 0.93]), o2=np.array([0.72, 0.60, 0.93]))
src = inspect.getsource(M.draw).replace("base = 0.55 * np.ones(3) + 0.45 * tint", "base = 0.55 * np.ones(3) + 0.45 * TINT[obj.get('k', t)]")
exec(src, M.__dict__)
P = tile('AB', 0, B.LAM)[0]
def keys(faces): return {tuple(np.round(np.mean([B.cart(p) for p in T], 0), 6)) for f in B.split_edges(faces) for T in B.rings_of(f)}
part = {}
for k, p in enumerate(P):
    for c in keys(E.union_faces([p[3]])): part.setdefault(c, 'bp' if p[0] == 'tet' else ('o1' if k == 0 else 'o2'))
mdl = M.model('h', 'AB', 0)
for r in mdl[0]: r['k'] = part[tuple(np.round(r['c'], 6))]
n = {k: sum(r['k'] == k for r in mdl[0]) for k in ('bp', 'o1', 'o2')}
V = [('three-quarter, front', M.View(22, -58)), ('three-quarter, back', M.View(22, 122)), ('top', M.View(89.5, -90)),
     ('bottom', M.View(-89.5, -90)), ('front', M.View(0.5, -90)), ('back', M.View(0.5, 90)),
     ('left side', M.View(0.5, 180)), ('right side', M.View(0.5, 0))]
BG = '#f4f4f2'; fig = plt.figure(figsize=(16, 16), facecolor=BG)
for i, (nm, v) in enumerate(V):
    ax = fig.add_axes([0.01 + (i % 3) * 0.33, 0.66 - (i // 3) * 0.32, 0.31, 0.27]); M.draw(ax, 'h', mdl, v, nm, lw_tie=1.2)
fig.suptitle(f"h-tile · {len(mdl[0])} rings · {len(mdl[1])} zip ties · gold: your double pyramid's {n['bp']} outside rings · "
             f"blue and violet: the two half-octahedra, {n['o1']} + {n['o2']} rings", fontsize=13, color='#222', y=0.985)
M.logo(fig, 0.945, 0.04)
fig.savefig(os.path.join(M.OUT, 'htile-views.png'), dpi=140, facecolor=BG); print('saved', n)
