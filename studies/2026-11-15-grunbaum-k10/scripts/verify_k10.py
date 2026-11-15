#!/usr/bin/env python3
"""Independent re-check of each tiler found by tile_check.py (different code path, floating point, so it cross-checks the exact run):
(a) surface: closed 2-manifold, Euler characteristic 2, every zone exactly k faces, no two edge-adjacent faces coplanar (dihedral angles
    listed: none is 180 degrees), all faces congruent golden rhombi (side lengths and diagonals measured);
(b) embedding: every pair of faces meets only in their common vertices/edge (triangle-triangle intersection tests on the two triangles
    of each rhombus, shrunk by 1e-7 towards the common part);
(c) coverage: 200,000 random points of a fundamental parallelepiped of the lattice, each counted in all translates P + l (point in
    cell): every point must be covered exactly once (points within 1e-9 of a cell boundary are re-drawn);
(d) the face-to-face matching: every face of P coincides with a face of one neighbour P + l, with opposite outward normal.
Usage: verify_k10.py tile4.json search.json out.json"""
import sys, json, itertools
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from zsurf import Geo, analyse, in_class, face_pair_vectors, corners
PHI = (1 + 5**0.5)/2
AX = np.array([(1, PHI, 0), (-1, PHI, 0), (0, 1, PHI), (0, -1, PHI), (PHI, 0, 1), (-PHI, 0, 1)], float)
T, Sj, OUT = json.load(open(sys.argv[1])), json.load(open(sys.argv[2])), sys.argv[3]
if 'candidates_rank_le_3' not in Sj: Sj = {'candidates_rank_le_3': [{'faces': f} for f in Sj['rank_le_3_surfaces']]}
n = T['n']; E = AX[:n]; G = Geo(n); rng = np.random.default_rng(20261115)
def pos(p): return np.asarray(p, float) @ E
report = []
for r in T['results']:
    if not r.get('tiles'): continue
    c = Sj['candidates_rank_le_3'][r['index']]
    S = {(tuple(f[0]), f[1], f[2]): f[3] for f in c['faces']}
    info, why = analyse(G, S); rep = {'index': r['index'], 'faces': len(S), 'vertices': info['V'], 'edges': info['E'], 'chi': info['chi'],
                                      'zones': sorted(z for _, z in info['zones']), 'in_class': in_class(G, info), 'coplanar_adjacent': info['coplanar_adjacent']}
    # (a) faces congruent, dihedral angles
    sides = set(); diags = set(); dih = []
    Eedges = {}
    for f, s in S.items():
        p, a, b = f; P0 = pos(p); A = E[a]; B = E[b]
        sides.update([round(np.linalg.norm(A), 9), round(np.linalg.norm(B), 9)])
        diags.add(tuple(sorted([round(np.linalg.norm(A + B), 9), round(np.linalg.norm(A - B), 9)])))
    for e, fs in [(e, [g for g in S if e in [(q, d) for (q, d) in [(g[0], g[1]), (g[0], g[2]), (tuple(np.add(g[0], np.eye(n, dtype=int)[g[2]])), g[1]), (tuple(np.add(g[0], np.eye(n, dtype=int)[g[1]])), g[2])]]]) for e in set((q, d) for g in S for (q, d) in [(g[0], g[1]), (g[0], g[2]), (tuple(np.add(g[0], np.eye(n, dtype=int)[g[2]])), g[1]), (tuple(np.add(g[0], np.eye(n, dtype=int)[g[1]])), g[2])])]:
        if len(fs) != 2: continue
        nrm = []
        for g in fs:
            v = np.cross(E[g[1]], E[g[2]])*S[g]; nrm.append(v/np.linalg.norm(v))
        dih.append(round(float(np.degrees(np.arccos(np.clip(nrm[0] @ nrm[1], -1, 1)))), 4))   # angle between outward normals
    rep['side_lengths'] = sorted(sides); rep['diagonals'] = sorted(diags)
    rep['normal_angles_deg'] = sorted(set(dih)); rep['min_normal_angle_deg'] = min(dih)
    # (b) embedding: triangle pairs
    tris = []
    for f, s in S.items():
        p, a, b = f; P0 = pos(p); A = E[a]; B = E[b]
        tris.append((f, [P0, P0 + A, P0 + A + B])); tris.append((f, [P0, P0 + A + B, P0 + B]))
    def seg_tri(p, q, t, eps=1e-9):
        u, v = t[1] - t[0], t[2] - t[0]; nn = np.cross(u, v); d0 = (p - t[0]) @ nn; d1 = (q - t[0]) @ nn
        if (d0 > eps and d1 > eps) or (d0 < -eps and d1 < -eps) or abs(d0 - d1) < 1e-15: return False
        x = p + (q - p)*(d0/(d0 - d1)); w = x - t[0]
        uu, uv, vv, wu, wv = u @ u, u @ v, v @ v, w @ u, w @ v; den = uv*uv - uu*vv
        s_ = (uv*wv - vv*wu)/den; t_ = (uv*wu - uu*wv)/den
        return s_ > eps and t_ > eps and s_ + t_ < 1 - eps
    bad = 0
    for (f1, t1), (f2, t2) in itertools.combinations(tris, 2):
        if f1 == f2: continue
        for (A_, B_) in ((t1, t2), (t2, t1)):
            ctr = sum(A_)/3
            sh = [x + (ctr - x)*1e-7 for x in A_]      # shrink so shared edges and corners do not count
            if any(seg_tri(sh[i], sh[(i + 1) % 3], B_) for i in range(3)): bad += 1
    rep['face_crossings'] = bad
    # (c) coverage
    B = np.array([pos(b) for b in r['basis']]); cells = r['cells']
    Minv = []
    for p, t in cells:
        M = np.array([E[d] for d in t]).T; Minv.append((pos(p), np.linalg.inv(M)))
    pts = np.array([pos(p) + sum(E[d]*s for d, s in zip(t, sub)) for p, t in cells for sub in itertools.product((0, 1), repeat=3)])
    ctr = pts.mean(0); Rr = np.linalg.norm(pts - ctr, axis=1).max()
    dual = np.linalg.inv(B).T; bound = [int(2*Rr*np.linalg.norm(dual[k])) + 2 for k in range(3)]
    L = [np.array(co) @ B for co in itertools.product(*[range(-b, b + 1) for b in bound])]
    N = 200000; X = ctr + rng.random((N, 3)) @ B - B.sum(0)/2
    count = np.zeros(N, int); near = np.zeros(N, bool)
    for l in L:
        if np.linalg.norm(l) > 3*Rr: continue
        for base, Mi in Minv:
            co = (X - base - l) @ Mi.T
            inside = np.all((co > 1e-9) & (co < 1 - 1e-9), axis=1)
            nearb = np.all((co > -1e-9) & (co < 1 + 1e-9), axis=1) & ~inside
            count += inside; near |= nearb
    ok = ~near
    rep['coverage_points'] = int(ok.sum()); rep['coverage_counts'] = {int(k): int(v) for k, v in zip(*np.unique(count[ok], return_counts=True))}
    # (d) face-to-face matching
    lam = face_pair_vectors(G, S, info); rep['face_to_face'] = lam is not None
    rep['lattice_basis'] = r['basis']; rep['cell_types'] = r.get('cell_types')
    vol = sum(abs(np.linalg.det(np.array([E[d] for d in t]))) for p, t in cells)
    rep['volume'] = vol; rep['covolume'] = abs(np.linalg.det(B))
    rep['PASS'] = bool(rep['in_class'] and rep['coplanar_adjacent'] == 0 and rep['chi'] == 2 and bad == 0 and rep['coverage_counts'] == {1: int(ok.sum())}
                       and abs(vol - rep['covolume']) < 1e-9 and rep['face_to_face'] and len(rep['side_lengths']) == 1 and len(rep['diagonals']) == 1)
    print(rep, flush=True); report.append(rep)
json.dump(report, open(OUT, 'w'), indent=1, default=str)
print('RESULT verified tilers:', sum(r['PASS'] for r in report), 'of', len(report))
print('FINAL ok' if report and all(r['PASS'] for r in report) else 'FINAL FAIL')
