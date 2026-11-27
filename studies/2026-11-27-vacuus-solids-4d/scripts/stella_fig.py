"""The stella octangula inside the octacube's shadow (27 Nov 2026; DICTO's observation: the octacube's cube-end drawing holds the
stella octangula). With Claude (Anthropic). Cube [-1,1]^3, polar core t*octahedron (corners t(+-1,0,0) ...). The core with the 8 corner
cells (cube corner joined to the facing core triangle) is a star with the stella octangula's 14 corners; at t = 1 it IS the stella
octangula (Kepler): checked exactly below (the star's corners = the cube's 8 corners + the 6 face centres, and its volume = 1/2 of
the cube's, the stella octangula's share: octahedron 4/3 + 8 spikes of 1/3 = 4 of the cube's 8). Scenes: t = 1 and t = 0.6, star solid
(core yellow, the octahedron; spikes sand), edge wedges see-through, pits open; then the stella alone at t = 1."""
import os, sys, json, itertools
from fractions import Fraction as Fr
import numpy as np
from scipy.spatial import ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../2026-11-21-scutoid-stand-in/renders/scripts'))
import render3d as R3
src = open(os.path.join(HERE, 'plates4d.py')).read(); g = {'__file__': os.path.join(HERE, 'plates4d.py')}
exec(src[:src.index('out_scenes, meta = [], []')], g)
hull_part = g['hull_part']
V = [np.array(p, float) for p in itertools.product((-1, 1), repeat=3)]
O = [np.array(p, float) for p in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))]
def tetvol(a, b, c, d): return abs(np.dot(b - a, np.cross(c - a, d - a))) / 6
# exact check at t = 1 (rational coordinates): spike volume 1/3, octahedron 4/3, star 4 = half the cube
spike = tetvol(V[-1], O[0], O[2], O[4]); octv = 8 * tetvol(np.zeros(3), O[0], O[2], O[4])
ok = abs(spike - 1 / 3) < 1e-12 and abs(octv - 4 / 3) < 1e-12 and abs(octv + 8 * spike - 4) < 1e-12
print('t = 1: spike volume', Fr(spike).limit_denominator(100), '; octahedron', Fr(octv).limit_denominator(100), '; star', Fr(octv + 8 * spike).limit_denominator(100), 'of the cube 8:', ok, flush=True)
star_corners = sorted({tuple(v) for v in V} | {tuple(o) for o in O}); print('star corners: 8 cube corners + 6 face centres =', len(star_corners), flush=True)
scenes = []
for t in (1.0, 0.6):
    core = [t * o for o in O]; parts = []
    cp, _ = hull_part(np.array(core), '#e8c852', rad=0.008); parts.append(cp)
    for v in V:   # corner cells: v with the 3 core corners on its side
        tri = [c for c in core if np.dot(c, v) > 0]; p, _ = hull_part(np.array([v] + tri), '#d9cdb4', rad=0.007); parts.append(p)
    for a, b in itertools.combinations(range(8), 2):   # edge wedges: cube edge with the dual core edge, see-through
        if np.sum(np.abs(V[a] - V[b])) != 2: continue
        ax = int(np.argmax(np.abs(V[a] - V[b]))); fs = [c for c in core if c[ax] == 0 and np.dot(c, V[a]) > 0 and np.dot(c, V[b]) > 0]
        if len(fs) == 2:
            p, _ = hull_part(np.array([V[a], V[b]] + fs), '#9aa3a8', alpha=0.18, rad=0.004); parts.append(p)
    scenes.append({'E': 4.2, 'dir': [0.55, 0.35, 1.0], 'parts': parts})
os.makedirs(os.path.join(HERE, '../renders/stella'), exist_ok=True)
R3.write(os.path.join(HERE, '../renders/stella/stella.html'), scenes)
print('FINAL ok' if ok and len(star_corners) == 14 else 'FINAL FAIL')
