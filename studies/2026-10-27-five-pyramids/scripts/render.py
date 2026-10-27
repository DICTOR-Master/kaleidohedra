# Five pyramids study (DICTO, 2026-10-27): renders (matplotlib, dark background, gold DICTO mark).
#  1. renders/shared-bipyramids.png: the only face-to-face meetings of two different face pyramids: base to base
#     (tetrahedron's Q, octahedron's, icosahedron's Cleo-Icos; equal equilateral bases).
#  2. renders/small-deltahedra.png: the distinct non-convex deltahedra of 3 and 4 regular tetrahedra found by the search.
import sys, os, json
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pieces import build, fl

GOLD, PURPLE, CYAN, BG = '#d4af37', '#8e5bd6', '#3fb8c9', '#0d0d12'
L = build()

def draw(ax, polys, colors, title):
    allp = np.vstack([np.vstack(p) for p in polys]); c = allp.mean(0); r = np.abs(allp - c).max()
    for P, col in zip(polys, colors):
        ax.add_collection3d(Poly3DCollection(P, facecolor=col, edgecolor='#f5f0dc', linewidths=0.8, alpha=0.82))
    for s in 'xyz': getattr(ax, 'set_%slim' % s)(c['xyz'.index(s)] - r, c['xyz'.index(s)] + r)
    ax.set_box_aspect((1, 1, 1)); ax.set_axis_off(); ax.set_facecolor(BG); ax.set_title(title, color='#e8e2cc', fontsize=10)

def faces_of(V, F): return [V[f] for f in F]

def mark(fig):
    fig.text(0.985, 0.02, 'DICTO', color=GOLD, ha='right', va='bottom', fontsize=11, fontweight='bold', family='serif')

def pyramid(nm):
    P = L[nm]; V = fl(P['V']); apex = V[-1]
    base = [f for f in P['F'] if len(V) - 1 not in f][0]
    B = V[base]; c = B.mean(0); n = np.cross(B[1] - B[0], B[2] - B[0]); n /= np.linalg.norm(n)
    # frame: base centred at origin in the plane z = 0, apex above (z > 0)
    if np.dot(apex - c, n) < 0: n = -n
    u = B[0] - c; u /= np.linalg.norm(u); w = np.cross(n, u); R = np.array([u, w, n])
    return (V - c) @ R.T, P['F']

def bipyramid(a, b):
    Va, Fa = pyramid(a); Vb, Fb = pyramid(b)
    Vb = Vb * np.array([1, -1, -1])  # turn b under the shared base (base vertex 0 kept, orientation reversed)
    Fb = [list(reversed(f)) for f in Fb]
    return [faces_of(Va, Fa), faces_of(Vb, Fb)]

fig = plt.figure(figsize=(12, 4.4), facecolor=BG)
pairs = [('Q (tetrahedron face pyramid)', 'Octahedron face pyramid', 'Q + octahedron pyramid\n(the octet\'s shared face)'),
         ('Q (tetrahedron face pyramid)', 'Cleo-Icos', 'Q + Cleo-Icos\n(finite cluster only)'),
         ('Octahedron face pyramid', 'Cleo-Icos', 'Octahedron pyramid + Cleo-Icos\n(finite cluster only)')]
col = {'Q (tetrahedron face pyramid)': GOLD, 'Octahedron face pyramid': PURPLE, 'Cleo-Icos': CYAN}
for k, (a, b, t) in enumerate(pairs):
    ax = fig.add_subplot(1, 3, k + 1, projection='3d'); ax.view_init(elev=12, azim=35 + 10 * k)
    draw(ax, bipyramid(a, b), [col[a], col[b]], t)
fig.suptitle('Different Platonic face pyramids meet face to face only base to base', color='#e8e2cc', fontsize=12)
mark(fig); os.makedirs('renders', exist_ok=True)
fig.savefig('renders/shared-bipyramids.png', dpi=160, facecolor=BG); plt.close(fig)

# 2: small non-convex deltahedra from regular tetrahedra (from data/q2-deltahedra.json)
D = json.load(open('data/q2-deltahedra.json'))
pick = [d for d in D if d['builds'] and all(p == 'Tetrahedron' for p in d['builds'][0].split(' + ')) and d['vertices'] in (6, 7)]
fig = plt.figure(figsize=(4 * len(pick), 4.4), facecolor=BG)
for k, d in enumerate(pick):
    V = np.array(d['corners']); ax = fig.add_subplot(1, len(pick), k + 1, projection='3d'); ax.view_init(elev=18, azim=30)
    draw(ax, [faces_of(V, d['face_list'])], [GOLD], '%d faces, %d corners\ndegrees %s' % (d['faces'], d['vertices'], ''.join(map(str, d['degrees']))))
fig.suptitle('Equilateral-surfaced gluings of 3 and 4 regular tetrahedra (non-convex deltahedra, class c)', color='#e8e2cc', fontsize=12)
mark(fig); fig.savefig('renders/small-deltahedra.png', dpi=160, facecolor=BG); plt.close(fig)
print('rendered', len(pick), 'tetrahedron gluings')
