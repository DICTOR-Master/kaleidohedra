# DICTO 2026-11-09 harmonic-gaps study, part A (harmonic half). DICTO proposed solving the open points by 3D waves (harmonics).
# Each shell (core K -> star S -> hull H) gets a scale-free harmonic fingerprint:
#   (a) the l = 6 incidence signature: icosahedral symmetry has exactly one invariant at l = 6, so every symmetric set of directions has
#       q6 = (its value of that invariant) x (one fixed vector); the cosine c6(A, B) between two sets' q6 is +1 when A and B sit on the
#       same kind of axis and -1 otherwise (5-fold and 3-fold have opposite signs). The Cleo pattern of #38a needs: tips over the core's
#       faces and under the hull's corners, valley floors at the core's corners and under the hull's faces: signature (+1, +1, +1, +1).
#   (b) the radial spectrum of the star, p_l = P_l / P_0 of r_S(u) (scale-free), l <= 30.
# Shells: KP-UP turn 1 (GSD, SSD), turn 2 (x phi^3, scale check), the reciprocal stars GD(D1) and GI(I), and the polar shell of GI.
import os, sys, json, itertools, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from radial import *
from scipy.spatial import ConvexHull
DATA = os.path.join(HERE, '..', 'data'); phi = (1 + 5 ** .5) / 2; fails = []; log = {'mark': 'DICTO harmonic gaps, part A harmonic, 2026-11-09'}
def check(c, m):
    print(('PASS ' if c else 'FAIL ') + m, flush=True); log.setdefault('checks', []).append(('PASS ' if c else 'FAIL ') + m)
    if not c: fails.append(m)
def cycp(v):
    out = set()
    for k in range(3):
        p = v[k:] + v[:k]
        for s in itertools.product((1, -1), repeat=3): out.add(tuple(round(a * b, 12) for a, b in zip(p, s)))
    return np.array(sorted(out))
def hull_faces(V):
    h = ConvexHull(V); g = {}
    for simp, eq in zip(h.simplices, h.equations): g.setdefault(tuple(np.round(eq, 8)), set()).update(simp)
    out = []
    for eq, idx in g.items():
        F = V[list(idx)]; c = F.mean(0); n = np.array(eq[:3]); u = F[0] - c; w = np.cross(n, u)
        out.append(F[np.argsort(np.arctan2((F - c) @ w, (F - c) @ u))])
    return out
I = cycp([0, .5, phi / 2]); FI = hull_faces(I)
D1 = np.array([3 * F.mean(0) for F in FI]); FD = hull_faces(D1)
I2 = np.array([5 ** .5 * F.mean(0) for F in FD]); FI2 = hull_faces(I2)
def pyramid_faces(F, tip): return [np.array([F[i], F[(i + 1) % len(F)], tip]) for i in range(len(F))]
def star_cells(core_faces, f):
    faces = list(core_faces)
    for F in core_faces: faces += pyramid_faces(F, f * F.mean(0)) + [F]
    return faces
GSD = star_cells(FI, 3.0); SSD = star_cells(FD, 5 ** .5)
def plane_pts(V, n, d): return V[np.abs(V @ n - d) < 1e-9]
def stell(planes_from, V):
    out = []
    for F in planes_from:
        n = np.cross(F[1] - F[0], F[2] - F[0]); n /= np.linalg.norm(n); d = n @ F[0]
        G = plane_pts(V, n, d); c = G.mean(0); u = G[0] - c; w = np.cross(n, u); out.append(G[np.argsort(np.arctan2((G - c) @ w, (G - c) @ u))])
    return out
GI = stell(FI, I2); GD = stell(FD, I2)
check(all(len(F) == 3 for F in GI) and all(len(F) == 5 for F in GD), 'GI(I): 20 triangles in I\'s planes; GD(D1): 12 pentagons in D1\'s planes, corners I2')
dirs = lambda V: V / np.linalg.norm(V, axis=1)[:, None]
fc = lambda Fs: np.array([F.mean(0) for F in Fs])
def q6(V):
    Y = real_Y(dirs(np.asarray(V, float)), 6)[6]; return Y.mean(1)
def c6(A, B):
    a, b = q6(A), q6(B); return float(a @ b / np.linalg.norm(a) / np.linalg.norm(b))
def landmarks(vis):
    """star tips (farthest visible corners) and valley floors (nearest visible corners on the surface)"""
    P = np.vstack([t for _, _, tris in vis for t in tris]); U = []
    for p in P:                                            # merge float copies of one corner (shapely grid 1e-9)
        if not any(np.linalg.norm(p - q) < 1e-6 for q in U): U.append(p)
    P = np.array(U); r = np.linalg.norm(P, axis=1); order = np.argsort(r); groups = []
    for i in order:
        if groups and abs(r[i] - r[groups[-1][0]]) < 1e-6 * r[i]: groups[-1].append(i)
        else: groups.append([i])
    full = [g for g in groups if len(g) >= 12]             # whole symmetry orbits only (12, 20, 30, 60, ...)
    return P[full[-1]], P[full[0]]
shells = {
    'KP-UP shell 1: I -> GSD -> D1': (I, FI, GSD, D1, FD),
    'KP-UP shell 2: D1 -> SSD -> I2': (D1, FD, SSD, I2, FI2),
    'KP-UP turn 2, shell 1 (x phi^3)': (I * phi ** 3, [F * phi ** 3 for F in FI], [F * phi ** 3 for F in GSD], D1 * phi ** 3, [F * phi ** 3 for F in FD]),
    'reciprocal: D1 -> GD(D1) -> I2': (D1, FD, GD, I2, FI2),
    'reciprocal: I -> GI(I) -> I2': (I, FI, GI, I2, FI2),
}
res = {}
for name, (K, FK, S, Hh, FH) in shells.items():
    vis = visible(S); tips, floors = landmarks(vis)
    sig = [c6(tips, fc(FK)), c6(tips, Hh), c6(floors, K), c6(floors, fc(FH))]
    X, W = quad_points(vis); r = np.linalg.norm(X, axis=1); vol = (W * r ** 3).sum() / 3
    a, Pl = coeffs(X, W, r); p = Pl / Pl[0]
    X2, W2 = quad_points(vis, 32, 0.22); a2, Pl2 = coeffs(X2, W2, np.linalg.norm(X2, axis=1)); conv = float(np.abs(Pl2 / Pl2[0] - p).max())
    res[name] = {'tips': len(tips), 'valley_floors': len(floors), 'signature_c6': [round(x, 9) for x in sig], 'volume_quadrature': vol,
                 'solid_angle': float(W.sum()), 'p_l': {l: float(p[l]) for l in range(31) if p[l] > 1e-18}, 'conv': conv}
    print(f'{name:36s} tips {len(tips):2d} floors {len(floors):2d}  c6 (tips·core faces, tips·hull corners, floors·core corners, floors·hull faces) = '
          + ', '.join(f'{x:+.6f}' for x in sig) + f'   vol {vol:.6f}  p6 {p[6]:.6e} p10 {p[10]:.6e} p12 {p[12]:.6e}  conv {conv:.1e}', flush=True)
R = res
check(abs(R['KP-UP shell 1: I -> GSD -> D1']['volume_quadrature'] - 6.545084971874737) < 1e-9 and abs(R['reciprocal: I -> GI(I) -> I2']['volume_quadrature'] - 47.787730879) < 1e-6
      and abs(R['reciprocal: D1 -> GD(D1) -> I2']['volume_quadrature'] - 117.446784) < 1e-5, 'quadrature volumes = exact volumes (GSD 3·I, GI 95/4 + 43√5/4, GD 235/4 + 105√5/4)')
check(all(abs(v['solid_angle'] - 4 * np.pi) < 1e-10 and v['conv'] < 1e-10 for v in R.values()), 'every star: solid angle 4π; spectra converged to 1e-10 between two quadratures')
ones = lambda s: all(abs(x - 1) < 1e-9 for x in s)
check(ones(R['KP-UP shell 1: I -> GSD -> D1']['signature_c6']) and ones(R['KP-UP shell 2: D1 -> SSD -> I2']['signature_c6']),
      'both KP-UP shells: signature (+1, +1, +1, +1), the Cleo pattern\'s incidences, although their solids differ')
p1, p2, p3 = (R[k]['p_l'] for k in ('KP-UP shell 1: I -> GSD -> D1', 'KP-UP shell 2: D1 -> SSD -> I2', 'KP-UP turn 2, shell 1 (x phi^3)'))
check(max(abs(p1[l] - p3[l]) for l in p1) < 1e-10, 'scaling: the next turn has the same radial spectrum to 1e-10 (similar shells, as expected)')
drift12 = max(abs(p1[l] - p2[l]) for l in set(p1) | set(p2) if l in p1 and l in p2)
check(drift12 > 1e-3, f'the radial spectrum alone differs between the two KP-UP shells (max |Δp_l| = {drift12:.4f}) although #38a proves one pattern: the bare radial fingerprint is not the test; the incidence signature is')
check(ones(R['reciprocal: D1 -> GD(D1) -> I2']['signature_c6']), 'GD(D1): signature (+1, +1, +1, +1), the same as the SSD shell (it is that shell)')
sGI = R['reciprocal: I -> GI(I) -> I2']['signature_c6']
check(not ones(sGI), f'GI(I): signature {sGI}: drifts, so the Cleo pattern cannot be laid in its shell')
log['shells'] = res
json.dump(log, open(os.path.join(DATA, 'a_harmonic.json'), 'w'), indent=1)
print('FINAL ok' if not fails else 'FINAL FAIL: ' + '; '.join(fails))
