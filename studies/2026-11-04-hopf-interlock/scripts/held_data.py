#!/usr/bin/env python3
"""Geometry and lock status for the figures of paper #101 (Held by Shape Alone), 7 Nov 2026.
Rebuilds the four layers of the study with its own code (interlock_pieces.py / interlock_rot.py, run by exec as interlock_rot.py does):
  (1) one (111) layer of the octet, edge 1;  (2) the #47 Admiral layer from admiral-network-pieces.json (engine data);
  (3) Dyskin's tetrahedron layer;  (4) a layer of upright unit cubes.
Every tested piece gets the slides+twists verdict of interlock_rot.rot_locked (LP in R^6 on exact contact polygons).
Writes out/held-data.json (faces of every piece, kind, verdict) for render_held.py, and prints the tallies (to compare with the study and Ch. 4)."""
import os, json, math, itertools, time
import numpy as np
from scipy.spatial import ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__)); STUDY = os.path.dirname(HERE)
src = open(os.path.join(STUDY, 'interlock_rot.py')).read()
g = {'__file__': os.path.join(STUDY, 'interlock_rot.py'), '__name__': 'held'}
exec(src.split('# calibration: Dyskin tetrahedra')[0], g)
faces, touching, clip, rot_locked = g['faces'], g['touching'], g['clip'], g['rot_locked']
t0 = time.time()

def near_of(bodies):
    cent = np.array([np.mean(np.vstack(b), 0) for b in bodies])
    rad = np.array([np.max(np.linalg.norm(np.vstack(b) - cent[k], axis=1)) for k, b in enumerate(bodies)])
    return cent, (lambda i: [j for j in range(len(bodies)) if j != i and np.linalg.norm(cent[j] - cent[i]) < rad[i] + rad[j] + 1e-6])

def contacts(bodies, i, near):
    """exact contact polygons of body i with its neighbours, with the outward normal of body i"""
    out = []
    for part in bodies[i]:
        for fa in faces(np.array(part, float)):
            for j in near:
                for pj in bodies[j]:
                    for fb in faces(np.array(pj, float)):
                        if touching(fa, fb):
                            poly = clip(fa[2], fb[2], fa[0])
                            if len(poly) >= 3: out.append({'n': fa[0].tolist(), 'poly': np.array(poly).tolist(), 'with': j})
    return out

def hull_faces(V):
    return [F.tolist() for n_, d_, F in faces(np.array(V, float))]

def case(name, bodies, kinds, ids, show_faces=None):
    cent, near = near_of(bodies); verdict = {}; tally = {}
    for i in ids:
        r = rot_locked(bodies, i, near(i)); verdict[i] = r
        tally.setdefault(kinds[i], {}).setdefault(r, 0); tally[kinds[i]][r] += 1
    print(f'{name}: {tally}  ({time.time() - t0:.0f} s)', flush=True)
    pieces = []
    for k, b in enumerate(bodies):
        fs = show_faces[k] if show_faces else [f for part in b for f in hull_faces(part)]
        pieces.append({'kind': kinds[k], 'faces': fs, 'centre': cent[k].tolist(), 'verdict': verdict.get(k)})
    return {'pieces': pieces, 'tally': tally}, near

OUT = {}
# (1) octet (111) layer, edge 1, layer planes A (z = 0) and B (z = H)
H = math.sqrt(2/3); POS = {'A': (0, 0), 'B': (.5, math.sqrt(3)/6)}
pts = np.array([[POS[L][0] + a + b/2, POS[L][1] + b*math.sqrt(3)/2, z*H] for z, L in enumerate('AB') for a in range(-6, 7) for b in range(-6, 7)])
n = len(pts); nbm = np.abs(np.linalg.norm(pts[:, None] - pts[None], axis=2) - 1) < 1e-9
adj = [np.where(nbm[i])[0].tolist() for i in range(n)]
tets = sorted({tuple(sorted(q)) for i in range(n) for q in itertools.combinations([i] + adj[i], 4) if all(nbm[a, b] for a, b in itertools.combinations(q, 2))})
octs = set()
for i in range(n):
    for q in itertools.combinations(adj[i], 4):
        if sum(nbm[a, b] for a, b in itertools.combinations(q, 2)) != 4: continue
        for o in set.intersection(*[set(adj[x]) for x in q]) - {i}:
            if not nbm[i, o]: octs.add(tuple(sorted((i, o) + q)))
octs = sorted(octs)
bodies = [[pts[list(t)]] for t in tets] + [[pts[list(o)]] for o in octs]
kinds = ['tetrahedron'] * len(tets) + ['octahedron'] * len(octs)
cent = [np.mean(b[0], 0) for b in bodies]
keep = [k for k, c in enumerate(cent) if np.linalg.norm(c[:2] - [0.5, 0.29]) < 4.2]
bodies = [bodies[k] for k in keep]; kinds = [kinds[k] for k in keep]
cent = [np.mean(b[0], 0) for b in bodies]
ids = [k for k, c in enumerate(cent) if np.linalg.norm(c[:2] - [0.5, 0.29]) < 2.0]
OUT['octet'], near = case('octet (111) layer', bodies, kinds, ids)
# contact polygons of the most central octahedron, and the most central tetrahedron with a face on the top plane
oc = min([k for k in ids if kinds[k] == 'octahedron'], key=lambda k: np.linalg.norm(cent[k][:2] - [0.5, 0.29]))
tt = min([k for k in ids if kinds[k] == 'tetrahedron' and sum(abs(v[2] - H) < 1e-9 for v in bodies[k][0]) == 3 and np.linalg.norm(cent[k][:2] - cent[oc][:2]) > 0.9],
         key=lambda k: np.linalg.norm(cent[k][:2] - cent[oc][:2]))
OUT['octet']['oct'] = oc; OUT['octet']['tet'] = tt
OUT['octet']['oct_contacts'] = contacts(bodies, oc, near(oc)); OUT['octet']['tet_contacts'] = contacts(bodies, tt, near(tt))
print('central octahedron', oc, 'contact polygons', len(OUT['octet']['oct_contacts']), '; lifted tetrahedron', tt, OUT['octet']['pieces'][tt]['verdict'], flush=True)

# (2) the #47 Admiral layer, exactly as interlock_rot.py builds it
P = json.load(open(os.path.join(STUDY, 'admiral-network-pieces.json'))); bodies = []; kinds = []; shown = []
for p in P:
    V = np.unique(np.round(np.array([cc for f in p['faces'] for cc in f], float), 9), axis=0)
    if p['kind'] == 'A':
        eqf = [np.array(f, float) for f in p['faces'] if len(f) == 3 and all(abs(np.linalg.norm(np.array(f[k]) - np.array(f[(k+1) % 3])) - 1) < 1e-6 for k in range(3))]
        A1 = {tuple(np.round(v, 9)) for v in eqf[0]}; A2 = {tuple(np.round(v, 9)) for v in eqf[1]}
        e = [np.array(v) for v in A1 & A2]; v1 = [np.array(v) for v in A1 - A2][0]; v2 = [np.array(v) for v in A2 - A1][0]
        apex = [v for v in V if not any(np.allclose(v, q) for q in e + [v1, v2])][0]
        bodies.append([np.array([apex, e[0], e[1], v1]), np.array([apex, e[0], e[1], v2])]); kinds.append('Admiral Cap')
    else:
        bodies.append([V]); kinds.append({'I': 'icosahedron', 'Q′': 'face pyramid'}.get(p['kind'], p['kind']))
    shown.append(p['faces'])
cent = np.array([np.mean(np.vstack(b), 0) for b in bodies]); c0 = cent.mean(0)
ids = [i for i, cc in enumerate(cent) if np.linalg.norm((cc - c0)[:2]) < 1.8]
OUT['admiral'], _ = case('#47 Admiral layer', bodies, kinds, ids, show_faces=shown)
zmin = min(v[2] for b in bodies for part in b for v in part); zmax = max(v[2] for b in bodies for part in b for v in part)
for k in ids:
    if kinds[k] == 'face pyramid':
        V = bodies[k][0]; onlow = sum(abs(v[2] - zmin) < 1e-7 for v in V); onhigh = sum(abs(v[2] - zmax) < 1e-7 for v in V)
        OUT['admiral']['pieces'][k]['base'] = 'low' if onlow == 3 else 'high' if onhigh == 3 else 'inside'
print('free face pyramids and their bases:', [(k, OUT['admiral']['pieces'][k]['base']) for k in ids if OUT['admiral']['pieces'][k]['verdict'] == 'free'], flush=True)
print('locked face pyramids and their bases:', sorted({OUT['admiral']['pieces'][k]['base'] for k in ids if kinds[k] == 'face pyramid' and OUT['admiral']['pieces'][k]['verdict'] == 'locked'}), flush=True)
OUT['admiral']['zrange'] = [zmin, zmax]

# (3) Dyskin's tetrahedron layer (as in interlock_rot.py)
h = 1/math.sqrt(2)
def tet(x, y, turn):
    V = np.array([(1, 0, h), (-1, 0, h), (0, 1, -h), (0, -1, -h)], float)/2
    if turn: V = V[:, [1, 0, 2]]
    return V + [x, y, 0]
bodies = []; kinds = []
for a in range(-4, 5):
    for b in range(-4, 5): bodies.append([tet(0.5*a, 0.5*b, (a + b) % 2)]); kinds.append('tetrahedron')
cent = [np.mean(b[0], 0) for b in bodies]; ids = [i for i, cc in enumerate(cent) if np.linalg.norm(cc[:2]) < 1.2]
OUT['dyskin'], _ = case('Dyskin tetrahedron layer', bodies, kinds, ids)
# (4) a layer of upright unit cubes
bodies = []; kinds = []
for a in range(-3, 4):
    for b in range(-3, 4): bodies.append([np.array(list(itertools.product((0, 1), repeat=3)), float) + [a - .5, b - .5, -.5]]); kinds.append('cube')
cent = [np.mean(b[0], 0) for b in bodies]; ids = [i for i, cc in enumerate(cent) if np.linalg.norm(cc[:2]) < 1.6]
OUT['cubes'], _ = case('cube layer', bodies, kinds, ids)
os.makedirs(os.path.join(HERE, '..', 'out'), exist_ok=True)
json.dump(OUT, open(os.path.join(os.path.dirname(HERE), 'out', 'held-data.json'), 'w'))
print(f'OK held_data.py {time.time() - t0:.0f} s', flush=True)
