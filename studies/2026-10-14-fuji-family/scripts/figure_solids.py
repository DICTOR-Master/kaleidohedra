# Solids for the FUJI family paper's figures (DICTO, 2026-10-14): FUJI(r) for several r, and the dictosphere solid
# (cube ∩ octahedron with an inscribed sphere). Face tags pick the colours in the renderer. Writes paper/figures/solids.json.
# DICTO · dictospheres.com
import itertools, json, math, os
import numpy as np
from scipy.spatial import HalfspaceIntersection, ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
phi = (1 + 5 ** .5) / 2
def fuji(r):
    R = math.sqrt((1 + r + r * r) / 3); h = math.sqrt(max(0, 1 - R * R))
    a = 2 * math.asin(min(1, 1 / (2 * R))); b = 2 * math.pi / 3 - a; ang = 0; P = []
    for i in range(3):
        P.append((R * math.cos(ang), R * math.sin(ang), 0)); ang += a
        P.append((R * math.cos(ang), R * math.sin(ang), 0)); ang += b
    # apex up = +y in the renderer: map (x, y, z) -> (x, z, -y)
    V = [(x, z, -y) for x, y, z in P] + [(0, h, 0)]
    F = [[5, 4, 3, 2, 1, 0]] + [[i, (i + 1) % 6, 6] for i in range(6)]
    T = ['base'] + ['equi' if i % 2 == 0 else 'iso' for i in range(6)]
    if r < 1e-9:  # the tetrahedron: merge the zero-length short sides
        V = [V[0], V[2], V[4], V[6]]; F = [[2, 1, 0], [0, 1, 3], [1, 2, 3], [2, 0, 3]]; T = ['base', 'equi', 'equi', 'equi']
    return dict(v=[list(map(float, p)) for p in V], f=F, t=T)
def dictosphere():
    s = math.sqrt(3)
    H = [list(n) + [-1.0] for n in np.vstack([np.eye(3), -np.eye(3)])] + [list(sg) + [-s] for sg in itertools.product((1, -1), repeat=3)]
    V = HalfspaceIntersection(np.array(H, float), np.zeros(3)).intersections
    h = ConvexHull(V); F = []; T = []
    for e in np.unique(np.round(h.equations, 7), axis=0):
        on = np.where(np.abs(V @ e[:3] + e[3]) < 1e-6)[0]; c = V[on].mean(0); a = V[on[0]] - c; a /= np.linalg.norm(a); b = np.cross(e[:3], a)
        F.append([int(i) for i in on[np.argsort(np.arctan2((V[on] - c) @ b, (V[on] - c) @ a))]]); T.append('square' if len(on) == 4 else 'hex')
    return dict(v=V.tolist(), f=F, t=T)
out = {f'FUJI_{k}': fuji(r) for k, r in [('0', 0), ('q', .25), ('h', .5), ('g', 1 / phi), ('e', .8), ('1', 1e-3 + .999)]}
out['dictosphere'] = dictosphere()
json.dump(out, open(os.path.join(ROOT, 'paper', 'figures', 'solids.json'), 'w'))
print({k: (len(v['v']), len(v['f'])) for k, v in out.items()})
