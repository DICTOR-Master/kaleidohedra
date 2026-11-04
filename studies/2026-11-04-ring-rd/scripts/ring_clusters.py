#!/usr/bin/env python3
"""DICTO's PET-ring RD cells in clusters (brief pet-ring-tetra-cluster.md, photos 4 Nov 2026). Elements stated explicitly:
RING = one per RD FACE (12 per cell), centred on the face direction (±1,±1,0) and permutations; TIE = one per RD EDGE (24 per cell), where two face-rings touch;
GAP = at each RD CORNER (14 per cell: 8 three-ring gaps, 6 four-ring gaps).
Sphere model: rings are circles on the cell's sphere (radius R); neighbouring face directions are 60 deg apart, so each ring covers 30 deg:
ring radius r = R sin 30 = R/2, ring plane at R cos 30 = (√3/2) R from the centre. Cells sit on the fcc lattice with centre distance d = √3 R,
so the ring towards a neighbour lies exactly in the shared RD face (option 1, SHARED ring) — or two rings tied face to face (option 2, d slightly larger).
Counts for clusters of 1, 4 (tetrahedral), 6 (octahedral), 14 (fcc cube: 8 corners + 6 face centres); figure of the 4-cell tetrapod."""
import itertools, math, os, json
import numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'); os.makedirs(os.path.join(OUT, 'figures'), exist_ok=True)
FACE = [np.array(v, float) for v in {tuple(s*x for s, x in zip(sg, p)) for p in itertools.permutations((1, 1, 0)) for sg in itertools.product((1, -1), repeat=3)}]
assert len(FACE) == 12
R = 1.0; r = R/2; h = R*math.sqrt(3)/2; d = math.sqrt(3)*R
# ring-to-ring contact angle check: neighbouring face directions at 60 deg
nb = [(i, j) for i, j in itertools.combinations(range(12), 2) if abs(FACE[i] @ FACE[j] / 2 - 0.5) < 1e-9]
assert len(nb) == 24
ROTG = np.eye(3)
def cell_rings(c):   # centre of each ring (in its plane) and its unit normal
    return [(c + h*(ROTG @ f)/np.linalg.norm(f), (ROTG @ f)/np.linalg.norm(f)) for f in FACE]
def ties_of(c):      # tangency points of neighbouring rings, on the sphere
    return [c + R*(FACE[i] + FACE[j])/np.linalg.norm(FACE[i] + FACE[j]) * 1.0 for i, j in nb]
def cluster(name):
    s = d / math.sqrt(2)   # fcc: centres = s*(even-sum integer points)... use nearest-neighbour distance d
    if name == '1': C = [(0, 0, 0)]
    elif name == '4 tetrahedral': C = [(0, 0, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1)]
    elif name == '6 octahedral': C = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]; C = [tuple(np.array(c) + np.array((0, 0, 0))) for c in C]
    elif name == '14 fcc cube': C = [c for c in itertools.product((0, 2), repeat=3)] + [(1, 1, 0), (1, 1, 2), (1, 0, 1), (1, 2, 1), (0, 1, 1), (2, 1, 1)]
    return [np.array(c, float) * d / math.sqrt(2) for c in C]
rows = []
for name in ('1', '4 tetrahedral', '6 octahedral', '14 fcc cube'):
    C = cluster(name); N = len(C)
    contacts = sum(1 for a, b in itertools.combinations(C, 2) if abs(np.linalg.norm(a - b) - d) < 1e-9)
    # option 1: shared rings (one ring per distinct face position), ties at distinct tangency points, rings meeting at each tie
    ringpos = {tuple(np.round(p, 6)) for c in C for p, _ in cell_rings(c)}
    tiepts = {}
    for c in C:
        for i, j in nb:
            t = tuple(np.round(c + R*(FACE[i] + FACE[j])/np.linalg.norm(FACE[i] + FACE[j]), 6))
            tiepts.setdefault(t, set()).update({tuple(np.round(c + h*FACE[i]/math.sqrt(2), 6)), tuple(np.round(c + h*FACE[j]/math.sqrt(2), 6))})
    multi = {}
    for t, rs in tiepts.items(): multi[len(rs)] = multi.get(len(rs), 0) + 1
    rows.append({'cluster': name, 'cells': N, 'contacts': contacts, 'opt1_rings_shared': len(ringpos), 'opt1_tie_points': len(tiepts),
                 'opt1_rings_per_tie': dict(sorted(multi.items())), 'opt2_rings_separate': 12*N, 'opt2_ties_in_cells': 24*N, 'opt2_extra_ties_per_contact': 'k (2-4, to confirm)'})
for rw in rows: print(rw)
json.dump({'r_over_R': 0.5, 'ring_plane_over_R': h, 'centre_distance_over_R': d, 'clusters': rows}, open(os.path.join(OUT, 'data', 'ring-clusters.json') if os.path.isdir(os.path.join(OUT, 'data')) else os.path.join(OUT, 'ring-clusters.json'), 'w'), indent=1)
# figure: 4-cell tetrapod, shared contact rings gold
fig = plt.figure(figsize=(12, 6.2))
for k, (elev, azim, ttl) in enumerate([(12, -60, 'side: three cells on the base, one on top; shared rings gold'), (89, -90, 'from above (apex cell on top): a rounded triangle')]):
    ax = fig.add_subplot(1, 2, k+1, projection='3d'); ax.set_axis_off(); ax.set_box_aspect((1, 1, 1)); ax.view_init(elev, azim); ax.computed_zorder = False
    _z = -np.ones(3)/math.sqrt(3); _x = np.array([1., -1, 0])/math.sqrt(2); _y = np.cross(_z, _x); ROT = np.array([_x, _y, _z])
    C = [ROT @ c for c in cluster('4 tetrahedral')]; ctr = np.mean(C, 0)
    CELLCOL = [(0.80, 0.86, 0.95), (0.95, 0.85, 0.80), (0.82, 0.93, 0.84), (0.92, 0.88, 0.95)]
    view = np.array([math.cos(math.radians(elev))*math.cos(math.radians(azim)), math.cos(math.radians(elev))*math.sin(math.radians(azim)), math.sin(math.radians(elev))])
    ROTG = ROT
    shared = {tuple(np.round(p, 6)) for a, b in itertools.combinations(C, 2) for p, _ in cell_rings(a) if np.linalg.norm(a - b) - d < 1e-9 and abs(np.linalg.norm(p - (a+b)/2)) < 1e-6}
    polys, cols = [], []
    done = set()
    for ci, c in enumerate(C):
        for p, n in cell_rings(c):
            key = tuple(np.round(p, 6))
            if key in done: continue
            done.add(key)
            u = np.cross(n, [0.3, 0.5, 0.8]); u /= np.linalg.norm(u); v = np.cross(n, u)
            th = np.linspace(0, 2*math.pi, 73)
            out = [p + r*(math.cos(t)*u + math.sin(t)*v) for t in th]; inn = [p + 0.82*r*(math.cos(t)*u + math.sin(t)*v) for t in th]
            front = ((p - ctr)/np.linalg.norm(p - ctr)) @ view
            al = 1.0 if front > -0.2 else 0.18
            col = (0.85, 0.62, 0.18, al) if key in shared else (*CELLCOL[ci], al)
            for m in range(72): polys.append([out[m], out[m+1], inn[m+1], inn[m]]); cols.append(col)
    ax.add_collection3d(Poly3DCollection(polys, facecolors=cols, edgecolors=[(0.3, 0.3, 0.3, 0.25 * c[3]) for c in cols], linewidths=0.2))
    lo, hi = np.min(C, 0) - 1.1, np.max(C, 0) + 1.1; L = max(hi - lo)/2; m0 = (lo + hi)/2
    ax.set_xlim(m0[0]-L, m0[0]+L); ax.set_ylim(m0[1]-L, m0[1]+L); ax.set_zlim(m0[2]-L, m0[2]+L); ax.set_title(ttl, fontsize=11)
fig.suptitle('Four RD ring cells in a tetrapod (the fcc tetrahedral hole): 12 rings per cell (one per RD face), r = R/2; 6 contacts, each a shared ring (gold)', fontsize=10.5)
fig.text(0.99, 0.01, 'DICTO · dictospheres.com', ha='right', fontsize=9, color='#888')
fig.savefig(os.path.join(OUT, 'figures', 'ring-tetrapod.png'), dpi=160, bbox_inches='tight'); print('figure ok')
