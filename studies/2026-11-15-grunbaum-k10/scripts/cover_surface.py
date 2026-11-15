#!/usr/bin/env python3
"""Coverage test straight from the surface (no cell decomposition needed), for candidates the exact check left undecided.
For each rank-3 candidate: lattice from the face pairs; 20,000 random points of a fundamental parallelepiped; for each point the number
of translates P + l containing it, by ray parity (a random ray direction, Moller-Trumbore on the 60 triangles of the 30 rhombi).
A tiling needs every count = 1. A count of 0 or 2 at a point far (> 1e-6) from every face is a witness against tiling; the witness
point is printed so that it can be re-checked exactly. Floating point: evidence, not proof, unless a witness is re-checked.
Usage: cover_surface.py search_or_gnomon.json out.json"""
import sys, json, itertools
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from zsurf import Geo, analyse, face_pair_vectors, int_rank_basis, lattice_det, volume3, zsign
PHI = (1 + 5**0.5)/2
E = np.array([(1, PHI, 0), (-1, PHI, 0), (0, 1, PHI), (0, -1, PHI), (PHI, 0, 1), (-PHI, 0, 1)], float)
d = json.load(open(sys.argv[1])); OUT = sys.argv[2]
cands = [c['faces'] for c in d['candidates_rank_le_3']] if 'candidates_rank_le_3' in d else d['rank_le_3_surfaces']
G = Geo(6); rng = np.random.default_rng(7); res = []
for ci, faces in enumerate(cands):
    S = {(tuple(f[0]), f[1], f[2]): f[3] for f in faces}
    info, _ = analyse(G, S); lam = face_pair_vectors(G, S, info)
    if lam is None: res.append({'index': ci, 'why': 'a pair faces the same way: no translation tiling'}); continue
    B = int_rank_basis([list(v) for v in lam.values()]); Bf = np.array(B, float) @ E
    det = lattice_det(G, B)
    if len(B) != 3 or det == (0, 0):
        r = {'index': ci, 'basis': B, 'why': 'face-pair vectors do not span a lattice in R^3 (exact det 0): no face-to-face lattice tiling'}
        print(r, flush=True); res.append(r); continue
    v3 = volume3(G, S); det = det if zsign(det) > 0 else (-det[0], -det[1])
    if (3*det[0], 3*det[1]) != v3:
        r = {'index': ci, 'basis': B, 'why': f'covolume {det} != volume {v3}/3 (exact)'}
        print(r, flush=True); res.append(r); continue
    tri = []
    for (p, a, b), s in S.items():
        P0 = np.array(p, float) @ E; A = E[a]; Bv = E[b]
        tri += [(P0, A, A + Bv), (P0, A + Bv, Bv)]
    V0 = np.array([t[0] for t in tri]); e1 = np.array([t[1] for t in tri]); e2 = np.array([t[2] for t in tri])
    verts = np.vstack([V0, V0 + e1, V0 + e2]); ctr = verts.mean(0); R = np.linalg.norm(verts - ctr, axis=1).max()
    nrm = np.cross(e1, e2); nrm /= np.linalg.norm(nrm, axis=1)[:, None]
    def inside(X):
        D = rng.normal(size=3); D /= np.linalg.norm(D)
        h = np.cross(D, e2); a = np.einsum('ij,ij->i', e1, h); f = 1/a
        s = X[:, None, :] - V0[None]; u = f*np.einsum('pij,ij->pi', s, h)
        q = np.cross(s, e1[None]); v = f*np.einsum('j,pij->pi', D, q); t = f*np.einsum('pij,ij->pi', q, e2)
        hit = (u > 0) & (v > 0) & (u + v < 1) & (t > 0)
        return hit.sum(1) % 2 == 1
    N = 20000; X = ctr + (rng.random((N, 3)) - 0.5) @ Bf
    dist = np.min(np.abs(np.einsum('pij,ij->pi', X[:, None, :] - V0[None], nrm)), axis=1)   # distance to face planes (lower bound proxy)
    keep = dist > 1e-6; X = X[keep]
    dual = np.linalg.inv(Bf).T; bound = [int(2*R*np.linalg.norm(dual[k])) + 2 for k in range(3)]
    cnt = np.zeros(len(X), int)
    for co in itertools.product(*[range(-b, b + 1) for b in bound]):
        l = np.array(co) @ Bf
        if np.linalg.norm(l) > 2*R + 1: continue
        cnt += inside(X - l)
    hist = {int(k): int(v) for k, v in zip(*np.unique(cnt, return_counts=True))}
    bad = np.nonzero(cnt != 1)[0]
    r = {'index': ci, 'basis': B, 'points': int(len(X)), 'count_histogram': hist, 'all_once': bool(len(bad) == 0),
         'witness': X[bad[0]].tolist() if len(bad) else None}
    print(r, flush=True); res.append(r)
json.dump(res, open(OUT, 'w'), indent=1)
print('RESULT covered exactly once:', [r['index'] for r in res if r.get('all_once')], 'of', len(res))
print('FINAL ok' if len(res) == len(cands) else 'FINAL FAIL: not every candidate processed')
