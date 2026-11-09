# DICTO #43 Conjecture 1 by a gnomon (DICTO proposed a gnomon argument, 9 Nov 2026). Float exploration of the OG's downward family.
# D_0 = OG, D_k = P(D_{k-1}) (hull of the foot points of the face planes). For each k this records the shell ("gnomon") between
# D_k and D_{k+1} in several normalisations and the face structure:
#   s_k = max_u h_{k+1}(u)/h_k(u)   (D_{k+1} inside s_k D_k; unscaled nesting D_{k+1} in D_k <=> s_k <= 1)
#   t_k = t_min(D_k) = max_u h_k(u)/h_{k+1}(u)   (D_k inside t_k D_{k+1}; Conjecture 1 <=> t_k <= 3/phi^2)
#   delta_k = log(s_k t_k) >= 0, = 0 exactly when D_{k+1} is a scaled copy of D_k about O (a classical gnomon step)
#   Lemma G check: h_{k+1}(n) >= h_k(n) at every face normal n of D_k (each face plane of D_k touches D_{k+1})
#   r, R, H, rho_min (nearest corner), theta (normal covering radius) and where it is attained (angle to the 5-, 3-, 2-fold axes)
#   face orbits by size (60/30/20/12), face polygon sizes, the axis rhythm (face or corner on each axis type)
# usage: python -u gnomon_float.py <five-fold-octet dir> <kmax> <out.json>
import sys, os, json, time
import numpy as np
from scipy.spatial import ConvexHull, cKDTree
OUT = os.path.abspath(sys.argv[3])
sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1])
src = open('exact_upward.py').read(); exec(src.split("def kinds(S)")[0])   # OG (exact), G (60 exact rotations)
KMAX = int(sys.argv[2])
OGf = np.array([[x.f() for x in v] for v in OG]); Gf = np.array([[[x.f() for x in row] for row in M] for M in G])
phi = (1 + 5 ** .5) / 2; TARGET = 3 / phi ** 2

def faces(V, tol=1e-9):
    h = ConvexHull(V); E = h.equations; n = len(E); par = np.arange(n)
    def find(i):
        while par[i] != i: par[i] = par[par[i]]; i = par[i]
        return i
    for f in range(n):
        for g in h.neighbors[f]:
            if g > f and np.abs(E[f] - E[g]).max() < tol: par[find(f)] = find(g)
    roots = np.array([find(i) for i in range(n)]); u, inv = np.unique(roots, return_inverse=True)
    M = np.zeros((len(u), 3)); Dd = np.zeros(len(u)); cnt = np.bincount(inv)
    np.add.at(M, inv, E[:, :3]); np.add.at(Dd, inv, -E[:, 3]); M /= np.linalg.norm(M, axis=1)[:, None]; Dd /= cnt
    vs = [set() for _ in range(len(u))]
    for t, s in zip(inv, h.simplices): vs[t].update(s.tolist())
    return M, Dd, np.unique(h.vertices), np.array([len(s) for s in vs])

def symmetrise(W):
    X = np.vstack([W @ g.T for g in Gf]); X = X[np.lexsort(X.T[::-1])]
    t = cKDTree(X); groups = {}
    for i, js in enumerate(t.query_ball_point(X, 1e-8)): groups.setdefault(min(js), []).append(i)
    return np.array([X[g].mean(0) for g in groups.values()])

# rotation axes by order (5, 3, 2), as unit vectors (both signs)
AX = {5: [], 3: [], 2: []}
for g in Gf:
    tr = np.trace(g); c = (tr - 1) / 2
    if c > 1 - 1e-9: continue
    ang = np.degrees(np.arccos(np.clip(c, -1, 1)))
    o = 5 if min(abs(ang - 72), abs(ang - 144)) < 1e-4 else 3 if abs(ang - 120) < 1e-4 else 2 if abs(ang - 180) < 1e-4 else 0
    w, v = np.linalg.eig(g); a = np.real(v[:, np.argmin(np.abs(w - 1))]); a /= np.linalg.norm(a)
    AX[o] += [a, -a]
for o in AX: AX[o] = np.unique(np.round(np.array(AX[o]), 9), axis=0)
NAX = {o: len(AX[o]) for o in AX}
assert NAX == {5: 12, 3: 20, 2: 30}, NAX

def ax_angle(u):
    return {o: float(np.degrees(np.arccos(np.clip(np.abs(AX[o] @ u).max(), -1, 1)))) for o in AX}

def orbit_size(u):   # 60 / stabiliser; stabiliser order from how many rotations fix u
    return 60 // int(sum(np.linalg.norm(g @ u - u) < 1e-7 for g in Gf))

def maxratio(P, M, D, chunk=2000):   # max over points p, faces (m, d): m.p/d
    best = -1.0
    for c0 in range(0, len(P), chunk): best = max(best, float((P[c0:c0 + chunk] @ M.T / D[None, :]).max()))
    return best

def support(P, U, chunk=2000):       # h_P(u) for every u in U
    out = np.full(len(U), -np.inf)
    for c0 in range(0, len(P), chunk): out = np.maximum(out, (U @ P[c0:c0 + chunk].T).max(1))
    return out

res = {'mark': 'DICTO #43 Conjecture 1, gnomon study, float, 2026-11-09 · DICTO · dictospheres.com', 'k': []}
t0 = time.time(); ok = True
V = OGf; FF = faces(V)
for k in range(KMAX + 1):
    M, Dd, cor, psz = FF; Vc = V[cor]
    W = symmetrise(M * Dd[:, None]); FN = faces(W); M2, D2, cor2, psz2 = FN; Wc = W[cor2]
    t = maxratio(Vc, M2, D2)                    # D_k inside t D_{k+1}
    s = maxratio(Wc, M, Dd)                     # D_{k+1} inside s D_k
    hk1_old = support(Wc, M)                    # h_{k+1} at D_k's normals
    lemG = float((hk1_old - Dd).min())          # >= 0 (Lemma G)
    crossed = int((hk1_old - Dd > 1e-9).sum())  # face planes of D_k that D_{k+1} crosses (foot points outside)
    R = float(np.linalg.norm(Vc, axis=1).max()); rho_min = float(np.linalg.norm(Vc, axis=1).min())
    r = float(Dd.min()); H = float(Dd.max())
    hm = ConvexHull(M); th = float(np.arccos((-hm.equations[:, 3]).min()))
    uth = -hm.equations[np.argmin(-hm.equations[:, 3]), :3]; uth /= np.linalg.norm(uth)
    ir = int(np.argmin(Dd)); ur = M[ir]
    # face orbits by size: count distinct orbits of each size
    sizes = {}
    rep = {}
    for i in range(len(M)):
        key = round(float(Dd[i]), 8)
        rep.setdefault(key, []).append(i)
    norb = {60: 0, 30: 0, 20: 0, 12: 0}
    for key, idx in rep.items():
        rest = list(idx)
        while rest:
            i = rest[0]; o = orbit_size(M[i]); norb[o] += 1
            orb = M[i] @ Gf.transpose(0, 2, 1)
            tr = cKDTree(orb); dd, _ = tr.query(M[rest]); rest = [j for j, x in zip(rest, dd) if x > 1e-7]
    rhythm = {o: ('face' if (np.abs(M @ AX[o].T).max(0) > 1 - 1e-9).all() else
                  'corner' if (np.abs((Vc / np.linalg.norm(Vc, axis=1)[:, None]) @ AX[o].T).max(0) > 1 - 1e-9).all() else 'edge')
              for o in AX}
    row = {'k': k, 'corners': len(cor), 'faces': len(M), 'R': R, 'r': r, 'H': H, 'rho_min': rho_min, 'theta_deg': float(np.degrees(th)),
           'theta_at_axis_deg': ax_angle(uth), 'r_at_axis_deg': ax_angle(ur), 'r_orbit': orbit_size(ur), 'r_face_sides': int(psz[ir]),
           't': t, 's': s, 'delta': float(np.log(s * t)), 'lemmaG_min': lemG, 'crossed_planes': crossed,
           'face_orbits': norb, 'polygon_sizes': {int(a): int(b) for a, b in zip(*np.unique(psz, return_counts=True))}, 'axis_rhythm': rhythm,
           'osc_log_H_over_r': float(np.log(H / r)), 'osc_log_R_over_r': float(np.log(R / r))}
    res['k'].append(row)
    ok &= lemG > -1e-9 and t <= TARGET + 1e-9 and s * t >= 1 - 1e-9 and sum(o * n for o, n in norb.items()) == len(M)
    print(f"k {k:2d} F {len(M):6d} r {r:.6f} rho_min {rho_min:.6f} R {R:.6f} t {t:.6f} s {s:.6f} delta {row['delta']:.6f} "
          f"lemG {lemG:+.1e} crossed {crossed:5d} th {row['theta_deg']:.3f} (ax5 {row['theta_at_axis_deg'][5]:.2f} ax3 {row['theta_at_axis_deg'][3]:.2f} ax2 {row['theta_at_axis_deg'][2]:.2f}) "
          f"r@orbit {row['r_orbit']} sides {row['r_face_sides']} (ax5 {row['r_at_axis_deg'][5]:.2f} ax3 {row['r_at_axis_deg'][3]:.2f} ax2 {row['r_at_axis_deg'][2]:.2f}) "
          f"orbits {norb} rhythm {rhythm} ({time.time() - t0:.0f}s)", flush=True)
    V, FF = W, FN
    json.dump(res, open(OUT, 'w'))
print('FINAL ok' if ok else 'FINAL FAIL: Lemma G, the bound, s*t >= 1 or the orbit count failed')
