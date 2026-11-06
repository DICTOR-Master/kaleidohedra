"""Football scutoid study, step 3a part 2: the closest stacking, solved at 60 digits from its contacts (gap g = 3/5 exactly).
The optimum of stack_exact.py lies on facets of four Minkowski pieces (ball-ball contacts). Each facet is a plane through three exact
points (differences of football vertices), so each contact gives one linear equation in (h, a, b). Solve them at 60 digits, check every
equation, then look for the minimal polynomials of h, a, b (integer relation search, degree <= 16)."""
import json, itertools, sys, numpy as np, mpmath as mp
from scipy.spatial import ConvexHull
mp.mp.dps = 60
sys.argv = [sys.argv[0], '0.6']
exec(open('grid_layer.py').read().split('# overlap test')[0].replace('print(', '(lambda *a, **k: None)('))
S = json.load(open('../data-stack-exact.json'))
n_ = np.cross(e1, e2); n_ /= np.linalg.norm(n_)
P1n, P2n = 2 * D * e1, D * (e1 + e2)
Tn = S['h'] * n_ + S['a'] * P1n + S['b'] * P2n
# ---- exact (60-digit) geometry, same combinatorics as the float one
phi = (1 + mp.sqrt(5)) / 2
Vm = mp.matrix([[mp.mpf(0)] * 3] * 60)
def mpv(x):  # float vertex -> exact one: coordinates are halves of 0, 1, 2, phi, 2phi, 3phi, 2+phi, phi^3
    cands = [mp.mpf(0), mp.mpf(1), mp.mpf(2), phi, 2 * phi, 3 * phi, 2 + phi, phi ** 3]
    out = []
    for c in x * 2:
        m = min(cands, key=lambda t: abs(float(t) - abs(c))); assert abs(float(m) - abs(c)) < 1e-9; out.append(m / 2 * (1 if c >= 0 else -1))
    return out
VM = [mpv(v) for v in V]
def vec(l): return mp.matrix(l)
def unit(v): return v / mp.norm(v)
fa = [f for f in F if len(f[2]) == 5 and np.allclose(f[0] / np.linalg.norm(f[0]), a)][0]
fc = [f for f in F if len(f[2]) == 6 and np.allclose(f[0] / np.linalg.norm(f[0]), c)][0]
cen = lambda idx: sum((vec(VM[i]) for i in idx), mp.matrix([0, 0, 0])) / len(idx)
A5, C3 = cen(fa[2]), cen(fc[2]); E1, E2 = unit(A5), unit(C3)
H5, H6 = mp.norm(A5), mp.norm(C3); G = mp.mpf(3) / 5; DD = H5 + H6 + G
bis = unit(E1 + E2); RY = 2 * bis * bis.T - mp.eye(3)
N = E1.T * E2  # dot
nrm = unit(mp.matrix([E1[1] * E2[2] - E1[2] * E2[1], E1[2] * E2[0] - E1[0] * E2[2], E1[0] * E2[1] - E1[1] * E2[0]]))
P1, P2 = 2 * DD * E1, DD * (E1 + E2)
def ballm(i, j):
    R = mp.eye(3) if (i + j) % 2 == 0 else RY; c0 = DD * (i * E1 + j * E2)
    return [R * vec(v) + c0 for v in VM]
dev = max(abs(float(x) - y) for i, j in ((0, 0), (1, 0)) for P, Q in zip(ballm(i, j), ball(i, j)[0]) for x, y in zip(P, Q))
print(f'60-digit balls vs float balls (float normals rounded to 1e-7 in football.py): largest difference {dev:.2e}'); assert dev < 1e-5
names = {'ball X': (0, 0), 'ball Y': (1, 0)}
rows, rhs = [], []; planes = []
for ct in S['contacts']:
    iA, iB = names[ct['A']], names[ct['B']]
    A_, B_ = ball(*iA)[0], ball(*iB)[0]; L = ct['p'] * P1n + ct['q'] * P2n
    diff = (A_[:, None, :] - B_[None, :, :]).reshape(-1, 3) - L
    H = ConvexHull(diff)
    for eq, sp in zip(H.equations, H.simplices):
        if abs(eq[:3] @ Tn + eq[3]) < 2e-5:
            AM, BM = ballm(*iA), ballm(*iB); Lm = ct['p'] * P1 + ct['q'] * P2
            pts = [AM[k // 60] - BM[k % 60] - Lm for k in sp]
            u, w = pts[1] - pts[0], pts[2] - pts[0]
            nn = mp.matrix([u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0]])
            if mp.norm(nn) < mp.mpf(10) ** -30: continue
            nn = unit(nn)
            row = [(nn.T * nrm)[0], (nn.T * P1)[0], (nn.T * P2)[0]]
            key = tuple(round(float(x), 9) for x in row + [(nn.T * pts[0])[0]])
            if any(all(abs(x - y) < 1e-8 for x, y in zip(key, k2)) or all(abs(x + y) < 1e-8 for x, y in zip(key, k2)) for k2, _ in rows): continue
            rows.append((key, (row, (nn.T * pts[0])[0]))); planes.append(dict(A=iA, B=iB, p=ct['p'], q=ct['q'], k=[int(x) for x in sp]))
print(f"distinct contact planes: {len(rows)}")
M = mp.matrix([r[1][0] for r in rows]); y = mp.matrix([r[1][1] for r in rows])
sol = mp.lu_solve(M.T * M, M.T * y) if len(rows) > 3 else mp.lu_solve(M, y)
res = max(abs(x) for x in (M * sol - y))
h, aa, bb = sol
print(f"h = {mp.nstr(h, 40)}\na = {mp.nstr(aa, 40)}\nb = {mp.nstr(bb, 40)}\nlargest residual over all contact planes: {mp.nstr(res, 3)}")
print(f"(float search gave h {S['h']:.10f}, a {S['a']:.8f}, b {S['b']:.8f})")
for nm, x in (('h', h), ('h^2', h * h), ('a', aa), ('b', bb)):
    p = None
    for deg in (1, 2, 4, 8, 16):
        p = mp.findpoly(x, deg, maxcoeff=10 ** 7)
        if p: break
    print(f"minimal polynomial of {nm}: {p if p else 'none found up to degree 16, coefficients < 1e7'}")
ok = res < mp.mpf(10) ** -40 and len(rows) >= 3
json.dump(dict(face_a=[int(i) for i in fa[2]], face_c=[int(i) for i in fc[2]], planes=planes), open("../data-stack-planes.json", "w"))
print("FINAL ok" if ok else "FINAL FAIL (contacts do not fix the optimum: residual too big or too few planes)")
