# The ten golden truncations (DICTO 11-02): each Platonic solid (edge 1) cut equally at every corner, distance x along each edge,
# so that each original face becomes a truncated polygon with its two side lengths in the golden ratio (either way).
# Builds each solid as the convex hull of the cut points, checks every face (regular corner polygon / truncated polygon ratio phi),
# volume, and renders all ten in DICTO order. Usage: golden_cuts.py <star-cores scripts dir> <out dir>
import sys, os, itertools, json, numpy as np
SC, OUT = [os.path.abspath(a) for a in sys.argv[1:3]]; sys.path.insert(0, SC)
sys.argv = [sys.argv[0], '.', OUT, os.path.expanduser('~/kres-tmp/book/dicto-logo.png')]
import figs_paper_a as A
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
g = (1 + 5 ** .5) / 2
def plat(name):
    if name == 'tetrahedron': P = [[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]]
    elif name == 'cube': P = [[x, y, z] for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]
    elif name == 'octahedron': P = [[s * (i == k) for i in range(3)] for k in range(3) for s in (1, -1)]
    elif name == 'icosahedron': P = [p for a in (-1, 1) for b in (-1, 1) for p in ([0, a, b * g], [a, b * g, 0], [b * g, 0, a])]
    else: P = [[x, y, z] for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)] + [p for a in (-1, 1) for b in (-1, 1) for p in ([0, a / g, b * g], [a / g, b * g, 0], [b * g, 0, a / g])]
    P = np.array(P, float); D = np.linalg.norm(P[:, None] - P[None], axis=2); e = D[D > 1e-9].min(); P /= e
    E = [(i, j) for i, j in itertools.combinations(range(len(P)), 2) if abs(np.linalg.norm(P[i] - P[j]) - 1) < 1e-9]
    return P, E
CORNER = {'tetrahedron': 1, 'octahedron': 1, 'icosahedron': 1, 'cube': 2 ** .5, 'dodecahedron': g}   # corner-polygon side per unit cut
ORDER = ['dodecahedron', 'icosahedron', 'cube', 'tetrahedron', 'octahedron']
def cuts(k):  # x with k*x/(1-2x) = phi  (corner sides long)  and (1-2x)/(k*x) = phi (original sides long)
    return [g / (k + 2 * g), 1 / (g * k + 2)]
def faces(Q):
    out = []
    for P, n in A.hull_faces(Q):
        L = [np.linalg.norm(P[(i + 1) % len(P)] - P[i]) for i in range(len(P))]; out.append((len(P), sorted(set(np.round(L, 9)))))
    return out
rep = []; fig, axs = plt.subplots(2, 5, figsize=(14, 6.6), gridspec_kw=dict(wspace=0.02, hspace=0.25)); M = A.rot(*A.VIEW)
for col, name in enumerate(ORDER):
    P, E = plat(name)
    for row, x in enumerate(cuts(CORNER[name])):
        Q = np.array([P[i] + x * (P[j] - P[i]) for i, j in E] + [P[j] + x * (P[i] - P[j]) for i, j in E])
        h = ConvexHull(Q); F = faces(Q); kinds = {}
        for n, L in F: kinds[(n, tuple(L))] = kinds.get((n, tuple(L)), 0) + 1
        ok = all((len(L) == 1) or abs(max(L) / min(L) - g) < 1e-9 for n, L in F)
        side = 'corner sides long' if row == 0 else 'original sides long'
        rep.append(dict(solid=name, x=x, side=side, faces={f'{n}-gon sides {list(L)}': c for (n, L), c in kinds.items()}, volume=h.volume, golden_ok=ok))
        S = A.Scene(M)
        for Pf, n in A.hull_faces(Q):
            S.convex(np.vstack([Pf, Pf.mean(0) * 0.999]), A.GOLD if len(Pf) in (3, 4, 5) and len(set(np.round([np.linalg.norm(Pf[(i+1)%len(Pf)]-Pf[i]) for i in range(len(Pf))], 9))) == 1 else A.VIOLET)
        S.draw(axs[row, col], 1.05 * np.linalg.norm(Q, axis=1).max())
        nm = ({'octahedron': 'Icosaxes'} if row == 0 else {'octahedron': 'Unborn Axes'}).get(name, f"{'Greater' if row == 0 else 'Lesser'} Golden Cut {name.capitalize()}")
        axs[row, col].set_title(f'{nm}\nx = {x:.4f}', fontsize=8.5)
fig.suptitle('The ten DICTO-Kepler golden truncations. Top: Greater Golden Cut (deeper cut); bottom: Lesser Golden Cut (lighter cut). Gold: regular corner cuts', fontsize=10.5)
A.mark(fig); fig.savefig(os.path.join(OUT, 'golden-truncations-ten.png'), dpi=200, facecolor='white')
json.dump(rep, open(os.path.join(OUT, 'golden-truncations-ten.json'), 'w'), indent=1)
for r in rep: print(f"{r['solid']:13s} x={r['x']:.6f} {r['side']:20s} golden={r['golden_ok']} vol={r['volume']:.6f} faces={r['faces']}")
