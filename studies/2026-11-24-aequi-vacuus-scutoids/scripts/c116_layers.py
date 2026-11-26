"""C116 -> floor 1 -> floor 2 -> Minana #377: the three Scutoid-Frusta layers (26 Nov 2026; DICTO: pillars and floors, 2-3 stages).
With Claude (Anthropic). Layer L: core = floor L-1 (exact convex solid, data/c116/floors.json; floor 0 = C116), mould = floor L's face
planes (layer 3: Minana #377's own planes), every core face paired with the mould face of the same label (layer 3: label k -> Minana
face sigma(k), the local pairing). Cell by amber_aequus.py with ASSIGN (outer end of each piece = its paired face), all its checks.
Usage: python c116_layers.py LAYER FACTOR   (LAYER 1, 2, 3; e.g. 6/5; LAYER 0 = one layer C116 -> Minana, best alignment)"""
import os, sys, json
sys.set_int_max_str_digits(0)
import numpy as np
from fractions import Fraction as Fr
argv = list(sys.argv); sys.argv = sys.argv[:1]
import amber_aequus as A
from resin import Q, dot, cross, det3
sys.argv = argv
HERE = os.path.dirname(os.path.abspath(__file__))
L, fac = int(argv[1]), argv[2]
F = json.load(open(os.path.join(HERE, '../data/c116/floors.json')))['realised']
byfloor = {r['floor']: r for r in F}
sig = {int(k): v for k, v in json.load(open(os.path.join(HERE, '../data/c116/pairing_local.json'))).items()}
if L == 0:   # 27 Nov: ONE layer, C116 -> Minana directly with the best alignment (data/c116/onefloor.json, c116_onefloor.py)
    sig = {int(k): v for k, v in json.load(open(os.path.join(HERE, '../data/c116/' + os.environ.get('ONEFLOOR', 'onefloor.json'))))['pairing'].items()}
Dm = A.build("aequus-377")
MN = np.array([[float(x) for x in u] for u, c in Dm["planes"]]); MN /= np.linalg.norm(MN, axis=1)[:, None]
def aligned_planes(r):
    # turn the floor so that face k points along Minana's face sigma(k) (least squares rotation), then exact rational planes
    N = np.array([[float(Fr(x)) for x in p] for p in r['planes']])
    Nu = N / np.linalg.norm(N, axis=1)[:, None]; T_ = np.array([MN[sig[k]] for k in range(60)])
    U, _, Vt = np.linalg.svd(Nu.T @ T_); R = (U @ Vt).T   # orthogonal; a reflection is allowed (the mirror image has the same face pattern)
    Nr = N @ R.T
    ang = np.degrees(np.arccos(np.clip(np.sum((Nr / np.linalg.norm(Nr, axis=1)[:, None]) * T_, axis=1), -1, 1)))
    print(f'  floor {r["floor"]} turned onto Minana (mirror {np.linalg.det(R) < 0}): angle between paired face directions max {ang.max():.1f} deg, mean {ang.mean():.1f} deg', flush=True)
    return [[Fr(int(round(x * 10**6)), 10**6) for x in nv] for nv in Nr]
def solid(r):
    planes = [([Q(x) for x in p], Q(1)) for p in aligned_planes(r)]
    tris = sorted({tuple(t) for f in r['faces'] for t in f})
    tid = {t: i for i, t in enumerate(tris)}; V = []
    for t in tris:
        a, b, c = (planes[k][0] for k in t); D = det3(a, b, c)
        cx, cy, cz = cross(b, c), cross(c, a), cross(a, b); V.append([(cx[q] + cy[q] + cz[q]) / D for q in range(3)])
    bad = sum(1 for i, tr in enumerate(tris) for k in range(60) if k not in tr and (dot(planes[k][0], V[i]) - 1).sign() >= 0)
    assert bad == 0, f'turned floor {r["floor"]} not exactly convex ({bad} corner/plane violations)'
    faces = []
    for k, f in enumerate(r['faces']):
        idx = [tid[tuple(t)] for t in f]
        nrm = cross([V[idx[1]][q] - V[idx[0]][q] for q in range(3)], [V[idx[2]][q] - V[idx[0]][q] for q in range(3)])
        faces.append((idx if dot(nrm, V[idx[0]]).sign() > 0 else idx[::-1], f"{len(idx)}-gon"))
    return V, faces, planes
V, faces, planes = solid(byfloor[max(L - 1, 0)])
if 0 < L < 3:
    H1 = [p for p in solid(byfloor[L])[2]]; ASSIGN = {k: k for k in range(60)}
else:
    H1 = [(u, c) for (u, c) in Dm["planes"]]; ASSIGN = {k: sig[k] for k in range(60)}
print(f'layer {L}: core floor {L - 1} ({len(V)} corners), mould {"floor " + str(L) if 0 < L < 3 else "Minana #377"}', flush=True)
def shell(lat, s): return [(u, s * c) for (u, c) in H1]
Z = Q(0); vol = Z
for mi, poly in A.mould_faces(H1):
    for q in range(1, len(poly) - 1):
        d = det3(poly[0], poly[q], poly[q + 1]); vol = vol + (d if d.sign() > 0 else -d)
A.CELLVOL["layer"] = vol / 6; A.shell = shell; A.ASSIGN = ASSIGN
A.build = lambda name: dict(V=V, faces=faces, planes=planes, name=name)
sys.argv = [argv[0], f"c116-layer{L}" + os.environ.get("TAG", ""), "layer", fac, "cen"]
A.main()
