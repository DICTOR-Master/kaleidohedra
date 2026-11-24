"""Task 3: Vacuus and Resonus of the gap hits (data/gapcheck.json), and whether they join the cycle
(Vacuus inside the 15 mirror planes; Resonus inside the 31 planes = 15 two-fold + 10 three-fold + 6 five-fold).
  - the D5d station die (study 2026-11-19 sid 77) at its exact station size (Theorem 8): EXACT in Q(sqrt5);
  - the regular octahedron |x| + |y| + |z| <= 3 (gap d): EXACT;
  - Yo (No.4) and Goi (No.51) (gap a; depths certified, not algebraic): an edge lies in a mirror exactly when its two faces are
    mirror images of each other (equal depth) -- decided exactly from the face directions; other edges are tested in double
    precision against the mirrors with the margin printed.
Vacuus = the planes through the centre and each edge; Resonus = the planes through the centre parallel to the faces.
-> data/vacres.json"""
import json, os, sys, itertools, glob
import numpy as np
from scipy.spatial import HalfspaceIntersection
HERE = os.path.dirname(os.path.abspath(__file__)); ST = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(ST, '2026-11-24-aequi-exact-dice', 'scripts'))
from groups import DIRS, DFAM
src = open(os.path.join(HERE, 'exact42.py')).read().split('\nco = json.load(')[0]
ex = {'__file__': os.path.join(HERE, 'exact42.py')}; exec(compile(src, 'exact42-helpers', 'exec'), ex)
EX, H, solve3, K, dot, cross, PHI = ex['EX'], ex['H'], ex['solve3'], ex['K'], ex['dot'], ex['cross'], ex['PHI']
MIR = [EX[i] for i, f in enumerate(DFAM) if f in ('C6', 'RT24')]
def pkey(n):
    f = np.array([float(t) for t in n]); f /= np.linalg.norm(f); s = np.sign(f[np.argmax(np.abs(f) > 1e-9)]); return tuple((f * s).round(9))
MIRK = {pkey(m) for m in MIR}; assert len(MIRK) == 15
AX31 = {pkey(EX[i]) for i in EX}; assert len(AX31) == 31
def exact_poly(q, h):
    C = []
    for a, b, c in itertools.combinations(range(len(q)), 3):
        x = solve3([q[a], q[b], q[c]], [h[a], h[b], h[c]])
        if x is not None and all((h[k] - dot(q[k], x)).sign() >= 0 for k in range(len(q))) and x not in C: C.append(x)
    inc = [{k for k in range(len(q)) if (h[k] - dot(q[k], x)).sign() == 0} for x in C]
    E = [(i, j) for i, j in itertools.combinations(range(len(C)), 2) if len(inc[i] & inc[j]) >= 2]
    # keep true edges: no third corner between on the same two planes
    E2 = []
    for i, j in E:
        common = inc[i] & inc[j]
        mid = [k for k in range(len(C)) if k not in (i, j) and common <= inc[k] and 0 < float(dot(ex['sub'](C[k], C[i]), ex['sub'](C[j], C[i]))) < float(dot(ex['sub'](C[j], C[i]), ex['sub'](C[j], C[i])))]
        if not mid: E2.append((i, j))
    return C, E2
def exact_report(name, q, h):
    C, E = exact_poly(q, h)
    vac = {}
    for i, j in E:
        n = cross(C[i], C[j])
        if all(t.sign() == 0 for t in n): continue
        in_mirror = any(all(t.sign() == 0 for t in cross(n, m)) for m in MIR)
        vac[pkey(n)] = in_mirror
    res = {pkey(qq) for qq in q}
    r = dict(polyhedron=name, corners=len(C), edges=len(E), vacuus_planes=len(vac), vacuus_in_15_mirrors=sum(vac.values()),
             vacuus_inside_15=all(vac.values()), resonus_planes=len(res), resonus_inside_31=res <= AX31)
    print(r, flush=True); return r
out = []
d77 = json.load(open(glob.glob(os.path.join(ST, '2026-11-19-aequi-complete', 'data', 'dice', '0077-*.json'))[0]))
out.append(exact_report('D5d station die (4553 sid 77) at its station size', [EX[i] for i in d77['face_directions']], [H[DFAM[i]] for i in d77['face_directions']]))
o8 = [EX[i] for i, f in enumerate(DFAM) if f == 'O8']
out.append(exact_report('regular octahedron |x|+|y|+|z| <= 3', o8, [K(3)] * 8))
for sid, name in (('6', 'Yo (No.4)'), ('63', 'Goi (No.51)')):
    d = json.load(open(glob.glob(os.path.join(ST, '2026-11-19-aequi-complete', 'data', 'dice', '%04d-*.json' % int(sid)))[0]))
    idx = d['face_directions']; U = DIRS[idx]; Dd = np.repeat([float(x) for x in d['depths_60_digits']], d['orbit_sizes'])
    orb = np.repeat(np.arange(len(d['orbit_sizes'])), d['orbit_sizes'])
    V = []
    for v in HalfspaceIntersection(np.hstack([U, -Dd[:, None]]), np.zeros(3)).intersections:
        if not any(np.abs(v - w).max() < 1e-9 for w in V): V.append(v)
    inc = [set(np.where(np.abs(U @ v - Dd) < 1e-9)[0]) for v in V]
    vac = {}; worst = 1
    for i, j in itertools.combinations(range(len(V)), 2):
        com = sorted(inc[i] & inc[j])
        if len(com) < 2: continue
        a, b = com[0], com[1]
        n = np.cross(V[i], V[j]); n /= np.linalg.norm(n); s = np.sign(n[np.argmax(np.abs(n) > 1e-9)]); key = tuple((n * s).round(7))
        # exact: faces a, b mirror images (same orbit, U[a] - U[b] along a two-fold axis) => the edge lies in that mirror
        exact_mirror = orb[a] == orb[b] and pkey(tuple(x - y for x, y in zip(EX[idx[a]], EX[idx[b]]))) in MIRK and dot(EX[idx[a]], EX[idx[a]]) == dot(EX[idx[b]], EX[idx[b]])
        near = min(np.linalg.norm(np.cross(n, np.array(m, float))) for m in MIRK)
        if not exact_mirror: worst = min(worst, near)
        vac[key] = vac.get(key, False) or bool(exact_mirror)
    r = dict(polyhedron=name + ' (4553 sid %s)' % sid, corners=len(V), vacuus_planes=len(vac), vacuus_in_15_mirrors_exact=sum(vac.values()),
             smallest_distance_of_another_vacuus_plane_from_a_mirror=float(worst), resonus_planes=len({pkey(EX[i]) for i in idx}), resonus_inside_31=True)
    print(r, flush=True); out.append(r)
json.dump(out, open(os.path.join(HERE, '..', 'data', 'vacres.json'), 'w'), indent=1)
print('FINAL ok' if len(out) == 4 and out[1]['vacuus_inside_15'] and out[1]['resonus_inside_31'] and out[0]['resonus_inside_31'] else 'FINAL FAIL')
