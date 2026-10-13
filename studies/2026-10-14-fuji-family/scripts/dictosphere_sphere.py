# The dictosphere as a sphere (DICTO, 2026-10-14): 14 ports (6 on the cube axes, 8 on the three-fold axes); each point of the
# surface belongs to its nearest port (spherical Voronoi: even space round every port). Writes a finely divided sphere for the
# renderer, faces tagged square / hex (the region they belong to), port (inside a port: 3 cm across on a sphere 8.8 cm across),
# and seam (near a region boundary). Also measures the curved flat-ended triangles. DICTO · dictospheres.com
import itertools, json, math, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
C = [np.array(v, float) for v in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]] + [np.array(s, float) / 3 ** .5 for s in itertools.product((1,-1), repeat=3)]
KIND = ['square'] * 6 + ['hex'] * 8
Rs = 4.40; port = 1.5 / Rs   # port radius as an angle (sin), sphere radius from DICTO's 8.4 cm arc
t = (1 + 5 ** .5) / 2
V = [np.array(v, float) for v in [(-1,t,0),(1,t,0),(-1,-t,0),(1,-t,0),(0,-1,t),(0,1,t),(0,-1,-t),(0,1,-t),(t,0,-1),(t,0,1),(-t,0,-1),(-t,0,1)]]
V = [v / np.linalg.norm(v) for v in V]
F = [(0,11,5),(0,5,1),(0,1,7),(0,7,10),(0,10,11),(1,5,9),(5,11,4),(11,10,2),(10,7,6),(7,1,8),(3,9,4),(3,4,2),(3,2,6),(3,6,8),(3,8,9),(4,9,5),(2,4,11),(6,2,10),(8,6,7),(9,8,1)]
for _ in range(7):
    mid = {}; NF = []
    def m(a, b):
        k = (min(a, b), max(a, b))
        if k not in mid: p = V[a] + V[b]; V.append(p / np.linalg.norm(p)); mid[k] = len(V) - 1
        return mid[k]
    for a, b, c in F:
        ab, bc, ca = m(a, b), m(b, c), m(c, a); NF += [(a, ab, ca), (b, bc, ab), (c, ca, bc), (ab, bc, ca)]
    F = NF
V = np.array(V); out_t = []
for f in F:
    p = V[list(f)].mean(0); p /= np.linalg.norm(p); d = [math.acos(np.clip(p @ c, -1, 1)) for c in C]; o = np.argsort(d)
    if d[o[0]] < math.asin(port): tag = 'port'
    elif d[o[1]] - d[o[0]] < 0.008: tag = 'seam'
    else: tag = KIND[o[0]]
    out_t.append(tag)
json.dump({'dictosphere_sphere': dict(v=V.tolist(), f=[list(f) for f in F], t=out_t)}, open(os.path.join(ROOT, 'paper', 'figures', 'sphere.json'), 'w'))
# the curved triangle's sides (arcs) on the sphere: Voronoi vertices are the directions of the equal-depth solid's corners
s = 3 ** .5; corner = np.array([1, s - 1, 0]); corner /= np.linalg.norm(corner)
arc = lambda a, b: math.acos(np.clip(a @ b / np.linalg.norm(a) / np.linalg.norm(b), -1, 1))
L = arc(np.array([1, s - 1, 0]), np.array([1, 0, s - 1])); S = arc(np.array([1, s - 1, 0]), np.array([s - 1, 1, 0]))
print(f'faces {len(F)}; along the surface on a sphere of radius {Rs} cm: long side {L*Rs:.2f} cm, short side {S*Rs:.2f} cm, r = {S/L:.3f}')
