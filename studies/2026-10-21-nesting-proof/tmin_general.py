# DICTO Kyushindo Cores (#43), 2026-10-21: the containment constant t_min(S) = least t with S inside t.P(S) for classic solids and
# counterexamples (float, scipy hulls). Checks the theorem  max_v |v|^2/h_P(v) <= t_min(S) <= R/r(P(S)) <= (R/r)^2  and the
# sharpness on the Platonic solids (t_min = (R/r)^2: 9, 3, 3, 15 - 6 sqrt5), and shows that no constant works in general:
# flat bipyramids (centrally symmetric) and spiky icosahedral hulls have t_min as large as you like.  Also probes whether t_min
# falls under the reverse step P (it does not, in general).
import itertools, json, os, numpy as np
from scipy.spatial import ConvexHull
PHI = (1 + 5 ** .5) / 2
def faces(P):
    """outward unit normals and supports of the facets of hull(P) (coplanar hull triangles merged)."""
    h = ConvexHull(P); eq = h.equations; out = {}
    for e in eq:
        n = e[:3] / np.linalg.norm(e[:3]); d = -e[3] / np.linalg.norm(e[:3]); out[tuple(np.round(np.r_[n, d], 7))] = (n, d)
    return [v for v in out.values()], h
def tmin(P):
    P = np.asarray(P, float); fs, h = faces(P); V = P[h.vertices]
    assert all(d > 0 for _, d in fs), 'centre outside'
    foot = np.array([d * n for n, d in fs]); fp, hp = faces(foot)
    g = np.array([max((n @ v) / d for n, d in fp) for v in V]); i = g.argmax()
    R = np.linalg.norm(V, axis=1).max(); r = min(d for _, d in fs); rP = min(d for _, d in fp)
    lower = max(np.dot(v, v) / max(foot @ v) for v in V)
    return dict(t_min=g.max(), lower=lower, R_over_rP=R / rP, R_over_r_sq=(R / r) ** 2, V=len(V), F=len(fs), foot_extreme=len(hp.vertices), foot_points=len(foot)), foot
def rep(name, P, extra=''):
    d, foot = tmin(P); assert d['lower'] - 1e-6 <= d['t_min'] <= d['R_over_rP'] + 1e-6 and d['R_over_rP'] <= d['R_over_r_sq'] + 1e-6, (name, d)
    print(f"{name:34s} t_min {d['t_min']:.6f}  lower {d['lower']:.6f}  R/r(P) {d['R_over_rP']:.6f}  (R/r)^2 {d['R_over_r_sq']:.6f}  V {d['V']} F {d['F']} foot-extreme {d['foot_extreme']}/{d['foot_points']} {extra}")
    return d, foot
signs = lambda k: list(itertools.product(*[(1, -1)] * k))
def perms(v): return list({tuple(np.array(v)[list(p)]) for p in itertools.permutations(range(3))})
def evenperms(v): return [tuple(np.array(v)[list(p)]) for p in [(0, 1, 2), (1, 2, 0), (2, 0, 1)]]
def allsigns(pts): return np.array(list({tuple(s * np.array(p)) for p in pts for s in signs(3)}))
tet = np.array([(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)], float)
cube = allsigns([(1, 1, 1)]); octa = allsigns(perms((1, 0, 0)))
ico = allsigns([p for v in [(0, 1, PHI)] for p in evenperms(v)])
dod = np.vstack([cube, allsigns([p for v in [(0, 1 / PHI, PHI)] for p in evenperms(v)])])
ID = np.vstack([allsigns(evenperms((0, 0, PHI))), allsigns([p for v in [(.5, PHI / 2, PHI ** 2 / 2)] for p in evenperms(v)])])
TI = allsigns([p for v in [(0, 1, 3 * PHI), (1, 2 + PHI, 2 * PHI), (PHI, 2, 2 * PHI + 1)] for p in evenperms(v)])
CO = allsigns(perms((1, 1, 0))); RD = np.vstack([cube, allsigns(perms((2, 0, 0)))]); TO = allsigns(perms((0, 1, 2)))
print('--- Platonic: theorem sharp, t_min = (R/r)^2 ---')
rep('tetrahedron (9)', tet); rep('cube (3)', cube); rep('octahedron (3)', octa); rep(f'dodecahedron (15-6r5={15 - 6 * 5 ** .5:.6f})', dod); rep('icosahedron (15-6r5)', ico)
print('--- other classic solids (below phi? phi = %.6f) ---' % PHI)
for nm, P in [('cuboctahedron', CO), ('rhombic dodecahedron', RD), ('truncated octahedron', TO), ('icosidodecahedron', ID), ('truncated icosahedron', TI)]:
    rep(nm, P)
print('--- counterexamples: no constant for centrally symmetric, nor for icosahedral symmetry ---')
for eps in (1, .3, .1, .03):
    rep(f'square bipyramid, height {eps}', allsigns([(1, 0, 0), (0, 1, 0), (0, 0, eps)]), '(flat -> t_min -> infinity)')
rng = np.random.default_rng(1)
def icosa_group():
    """the 60 rotations as matrices, from the icosahedron's vertex set (float)."""
    from scipy.spatial.transform import Rotation as Ro
    pts = ico / np.linalg.norm(ico[0]); mats = []
    for i in range(12):
        for j in range(12):
            a, b = pts[0], pts[i]
            if abs(a @ pts[1] - pts[i] @ pts[j]) > 1e-9 or i == j: continue
            A = np.array([pts[0], pts[1], np.cross(pts[0], pts[1])]); B = np.array([pts[i], pts[j], np.cross(pts[i], pts[j])])
            M = B.T @ np.linalg.inv(A.T)
            if np.allclose(M @ M.T, np.eye(3)) and np.linalg.det(M) > 0 and all(np.min(np.linalg.norm(pts - (M @ p), axis=1)) < 1e-9 for p in pts):
                if not any(np.allclose(M, N) for N in mats): mats.append(M)
    return mats
Gm = icosa_group(); assert len(Gm) == 60, len(Gm)
ball = np.vstack([np.array([M @ v for M in Gm]) for v in rng.normal(size=(20, 3))]); ball /= np.linalg.norm(ball, axis=1)[:, None]
for rho in (.9, .7, .5, .3):
    rep(f'icosahedron + {rho} x round icosahedral core', np.vstack([ico / np.linalg.norm(ico[0]), rho * ball]), '(spiky icosahedral, centrally symmetric)')
print('--- does t_min fall under P? (P-iterates of classic solids and random centrally symmetric hulls) ---')
for nm, P in [('cube', cube), ('rhombic dodecahedron', RD), ('icosahedron', ico), ('truncated icosahedron', TI), ('icosahedron+0.7 core', np.vstack([ico / np.linalg.norm(ico[0]), .7 * ball]))]:
    seq = []; Q = P
    for k in range(6):
        d, foot = tmin(Q); seq.append(round(d['t_min'], 4)); Q = foot
    print(f'{nm:34s} t_min of P^k, k=0..5: {seq}')
for s in range(4):
    Q = rng.normal(size=(8, 3)); Q = np.vstack([Q, -Q]); seq = []
    for k in range(6):
        d, foot = tmin(Q); seq.append(round(d['t_min'], 4)); Q = foot
    print(f'random centrally symmetric #{s}          t_min of P^k, k=0..5: {seq}')
