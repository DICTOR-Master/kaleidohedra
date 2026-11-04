#!/usr/bin/env python3
"""Second dual sweep (Concordance gap 2) with the harmonic detector: S(mu) = CO ∩ mu·RD, CO = {|x|<=1, |x|+|y|+|z|<=2}, RD = polar(CO) = {|x|+|y|<=1}.
mu = 1: RD; mu = 2: CO. Reports the corner set, face census and Q4 along mu; finds zeros of Q4. dicto-big-brother, ~/geom/bin/python."""
import itertools, json, math, os, sys
import numpy as np
from scipy.spatial import HalfspaceIntersection, ConvexHull
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '2026-11-04-harmonic-fingerprint', 'scripts'))
from scipy.special import sph_harm_y
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data'); os.makedirs(OUT, exist_ok=True)
def Q(P, l):
    u = P / np.linalg.norm(P, axis=1)[:, None]; th = np.arccos(np.clip(u[:, 2], -1, 1)); ph = np.arctan2(u[:, 1], u[:, 0])
    q = np.array([sph_harm_y(l, m, th, ph).mean() for m in range(-l, l+1)]); return math.sqrt(4*math.pi/(2*l+1)*np.sum(np.abs(q)**2))
hs = []
for i in range(3):
    for s in (1, -1): e = [0, 0, 0]; e[i] = s; hs.append([*e, -1.0])
for s in itertools.product((1, -1), repeat=3): hs.append([*s, -2.0])
RDh = []
for i, j in itertools.combinations(range(3), 2):
    for a, b in itertools.product((1, -1), repeat=2): e = [0, 0, 0]; e[i] = a; e[j] = b; RDh.append(e)
def S(mu):
    H = np.array(hs + [[*e, -mu] for e in RDh], float)
    V = np.unique(np.round(HalfspaceIntersection(H, np.zeros(3)).intersections, 9), axis=0)
    hull = ConvexHull(V); fs = {}
    for eq in hull.equations:
        k = tuple(np.round(eq[:3], 6)); fs[k] = eq
    census = {}
    for k, eq in fs.items():
        n = len([p for p in V if abs(p @ eq[:3] + eq[3]) < 1e-7]); census[n] = census.get(n, 0) + 1
    return V, census, hull.volume
log = []
for mu in (1.0, 1.1, 1.25, 4/3, 1.4, 1.5, (1+5**.5)/2, 1.75, 1.9, 2.0):
    V, c, vol = S(mu)
    s = f'mu {mu:.4f}: {len(V)} corners, faces {dict(sorted(c.items()))}, Q4 {Q(V,4):.4f}, Q6 {Q(V,6):.4f}'; print(s); log.append(s)
grid = np.linspace(1.0005, 1.9995, 2000); q4 = np.array([Q(S(m)[0], 4) for m in grid])
mins = [i for i in range(1, len(grid)-1) if q4[i] < q4[i-1] and q4[i] <= q4[i+1]]
s = 'local minima of Q4: ' + str([(round(grid[i], 4), round(q4[i], 4)) for i in mins]); print(s); log.append(s)
open(os.path.join(OUT, 'co-rd-sweep.log'), 'w').write('\n'.join(log) + '\n')
