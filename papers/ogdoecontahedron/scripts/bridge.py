# Is the DICTO Ogdoecontahedron a real periodic <-> aperiodic bridge? (DICTO, queued 2026-10-16; three checks before any Fable work)
#  1  6D lift: its corners written in the primitive icosahedral module (the 6D hypercubic lattice projected along the 6 five-fold
#     axes); their perpendicular-space images (Galois conjugate) tested against the canonical window (the triacontahedron that the
#     6D unit cube projects to, as in the Ammann-Kramer-Neri tiling). Caution: phi-inflation shrinks perp images by phi, so ANY finite
#     golden set fits after enough inflations; the scale k at which it first fits, and the edge directions, are what carry meaning.
#  2  clusters: its corner orbits (12 five-fold, 30 two-fold, 60 on mirrors) against the shells of the Tsai, Bergman and Mackay
#     clusters (standard shell geometry, see README for sources).
#  3  faces: can its hexagon and kite angles be made from tile angles (golden rhombus 63.43/116.57; Penrose rhombi multiples of 36)?
import sys, io, contextlib, itertools, json, numpy as np
from fractions import Fraction as Fr
from scipy.spatial import ConvexHull
from scipy.optimize import linprog
sys.path.insert(0, '/home/dicto/kaleidohedra/studies/_lib'); import geomcheck as gc
PD = '/home/dicto/kaleidohedra/studies/2026-10-16-polar-dharma'
sys.argv = ['polar.py', PD + '/data/dharma_cycle.json']
import os; _cwd = os.getcwd(); os.chdir(PD)
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('scripts/polar.py').read())
os.chdir(_cwd)
St = dict(rev); OG = St['dual of the Hecatodihedron']; IC = St['icosahedron']
f = lambda v: np.array([x.f() for x in v]); OGf = np.array([f(v) for v in OG])
ax = gc.icosa_axes(np.array([f(v) for v in IC])); gc.frame(OGf, ax, 'Ogdoecontahedron')
out = []
# ---- the six basis vectors a_i: one icosahedron corner from each antipodal pair, scaled to the (0, ±1, ±phi) form, exact
phi = Q(Fr(1, 2), Fr(1, 2))
def snap1(x):  # 0, ±1, ±phi exactly
    for c in (Q(0), Q(1), Q(-1), phi, -phi):
        if abs(c.f() - x) < 1e-9: return c
    raise ValueError(x)
U = np.array([f(v) for v in IC]); U = U / np.linalg.norm(U[0]) * np.sqrt(1 + ((1 + 5 ** .5) / 2) ** 2)
basis = []
for u in U:
    if not any(np.allclose(u, -b, atol=1e-9) or np.allclose(u, b, atol=1e-9) for b in [f(x) for x in basis]): basis.append([snap1(c) for c in u])
assert len(basis) == 6
conj = lambda q: Q(q.a, -q.b)
# exact 6x6 rational system: coordinates (a, b) of a + b sqrt5 for x, y, z
M = [[getattr(basis[j][i // 2], 'ab'[i % 2]) for j in range(6)] for i in range(6)]
def solve(Mx, y):
    A = [row[:] + [yy] for row, yy in zip(Mx, y)]; n = len(A)
    for c in range(n):
        p = next(r for r in range(c, n) if A[r][c] != 0); A[c], A[p] = A[p], A[c]
        A[c] = [x / A[c][c] for x in A[c]]
        for r in range(n):
            if r != c and A[r][c] != 0: A[r] = [x - A[r][c] * y for x, y in zip(A[r], A[c])]
    return [A[r][n] for r in range(n)]
from math import lcm, gcd
def lift(V):                                          # smallest rational scale making every corner an integer 6D point
    N = [solve(M, [getattr(v[i // 2], 'ab'[i % 2]) for i in range(6)]) for v in V]
    den = 1
    for n in N:
        for x in n: den = lcm(den, x.denominator)
    Ni = [[int(x * den) for x in n] for n in N]; g = 0
    for n in Ni:
        for x in n: g = gcd(g, x)
    return [[x // g for x in n] for n in Ni], Fr(den, g)
best = None                                           # also allow golden scale factors phi^m: keep the smallest 6D lift
for m in range(-8, 9):
    pm = Q(1)
    for _ in range(abs(m)): pm = pm * (phi if m > 0 else phi - Q(1))
    Ni_, sc_ = lift([[c * pm for c in v] for v in OG]); nm = max(sum(x * x for x in n) for n in Ni_)
    if best is None or nm < best[0]: best = (nm, m, Ni_, sc_, pm)
_, mbest, Ni, scale, pm = best
OGf = OGf * pm.f()
out.append(f'1. 6D lift: smallest lift with the chain-scale solid scaled by {scale} x phi^{mbest} (6D coordinates integer, gcd 1); '
           f'6D norm^2 range {min(sum(x * x for x in n) for n in Ni)}..{max(sum(x * x for x in n) for n in Ni)}')
Bpar = np.array([f(b) for b in basis]); Bperp = np.array([[conj(c).f() for c in b] for b in basis])
Xpar = np.array(Ni, float) @ Bpar; Xperp = np.array(Ni, float) @ Bperp
assert np.allclose(Xpar, OGf * float(scale), atol=1e-6)
W = ConvexHull(np.array([np.array(s) @ Bperp for s in itertools.product([-.5, .5], repeat=6)]))   # canonical window: a triacontahedron
eq = W.equations
def fits(P):   # is there a translate t with every P - t inside W?  n.(p - t) + d <= 0  ->  -n.t <= -d - n.p  for all p
    A = -eq[:, :3]; b = -eq[:, 3] - np.max(P @ eq[:, :3].T, axis=0)
    r = linprog(np.zeros(3), A_ub=A, b_ub=b, bounds=[(None, None)] * 3); return r.status == 0
# rule 3, known case first: the triacontahedron spanned by the six unit 6D vectors is a genuine cluster of the canonical tiling;
# its corners must fit the window at k = 0 and every edge must run along a 5-fold axis
subs = list(itertools.product([0, 1], repeat=6)); Z = np.array([np.array(t, float) @ Bpar for t in subs]); hz = ConvexHull(Z)
RTn = [subs[i] for i in hz.vertices]; assert len(RTn) == 32
fitsRT = None
p = (1 + 5 ** .5) / 2
for k in range(0, 60):
    if k == 0:
        fitsRT = fits(np.array(RTn, float) @ Bperp); gc.known('unit triacontahedron fits the canonical window at k=0', float(fitsRT), 1.0)
        er = [np.array(RTn[i], float) - np.array(RTn[j], float) for i, j in itertools.combinations(range(32), 2)]
        er = [d @ Bpar for d in er if abs(np.linalg.norm(d @ Bpar) - np.linalg.norm(Bpar[0])) < 1e-9]
        gc.known('triacontahedron edges along 5-fold axes', float(all(np.max(np.abs(ax['5'] @ (d / np.linalg.norm(d)))) > 1 - 1e-9 for d in er)), 1.0)
        out.append(f'   known case passed: the unit triacontahedron (32 corners) fits the window at k = 0, its {len(er)} unit edges all along 5-fold axes')
    if fits(Xperp * (-1 / p) ** k):
        out.append(f'   canonical window: the perp images first fit after k = {k} phi-inflations of that smallest lift; perp radius at k=0 '
                   f'{np.linalg.norm(Xperp, axis=1).max():.3f} vs window circumradius {np.linalg.norm(W.points[W.vertices], axis=1).max():.3f}; '
                   f'its radius is then {np.linalg.norm(Xpar, axis=1).max() * p ** k / np.linalg.norm(Bpar[0]):.0f} tiling edges, so its corners are only scattered points of a huge patch')
        break
# edge directions
h = ConvexHull(OGf); pl = []
for e in h.equations:
    if not any(np.allclose(e, q, atol=1e-7) for q in pl): pl.append(e)
E = set()
for e in pl:
    idx = [i for i in range(len(OG)) if abs(OGf[i] @ e[:3] + e[3]) < 1e-7]; Qp = OGf[idx]; c = Qp.mean(0)
    a = Qp[0] - c; a /= np.linalg.norm(a); b = np.cross(e[:3], a); o = [idx[i] for i in np.argsort(np.arctan2((Qp - c) @ b, (Qp - c) @ a))]
    for i in range(len(o)): E.add(tuple(sorted((o[i], o[(i + 1) % len(o)]))))
kind = {}
for i, j in E:
    d = OGf[j] - OGf[i]; d /= np.linalg.norm(d)
    lab = next((k for k in '532' if np.max(np.abs(ax[k] @ d)) > 1 - 1e-9), 'none')
    kind[lab] = kind.get(lab, 0) + 1
out.append(f'   edge directions ({len(E)} edges): ' + ', '.join(f'{v} along {k}-fold axes' if k != 'none' else f'{v} along no symmetry axis' for k, v in kind.items())
           + ' (tiles of the Ammann-Kramer-Neri tiling have all edges along 5-fold axes)')
# ---- 2. clusters: corner orbits and their placement
r = np.linalg.norm(OGf, axis=1)
orb = {}
for v, rr in zip(OGf, r):
    u = v / np.linalg.norm(v); lab = next((k for k in '532' if np.max(np.abs(ax[k] @ u)) > 1 - 1e-9), 'm')
    orb.setdefault(lab, []).append(rr)
out.append('2. corner orbits: ' + ', '.join(f'{len(v)} on {k}-fold axes at r={v[0]:.6f}' if k != 'm' else f'{len(v)} on mirror planes at r={v[0]:.6f}' for k, v in orb.items()))
# the 60-orbit's position on its mirror: angle from the nearest 5-fold axis, compared with known 60-atom shells
def ang5(P): return np.degrees(min(np.arccos(np.clip(abs(ax['5'] @ (q / np.linalg.norm(q))), -1, 1)).min() for q in P))
m60 = OGf[[i for i in range(len(OG)) if not any(np.max(np.abs(ax[k] @ (OGf[i] / r[i]))) > 1 - 1e-9 for k in '532')]]
I0 = ax['5']; TI = []
for i, j in itertools.combinations(range(12), 2):
    if np.dot(I0[i], I0[j]) > 0.4: TI += [I0[i] + (I0[j] - I0[i]) / 3, I0[j] + (I0[i] - I0[j]) / 3]   # truncated icosahedron (Bergman 60)
RTm = []
D = ax['3'] * np.sqrt(3) / np.sqrt(3); Ir = I0 * 1.0
RTv = np.vstack([I0 * 1.0, ax['3'] * (np.sqrt(3) * (1 + 5 ** .5) / 2 / np.sqrt(1 + ((1 + 5 ** .5) / 2) ** 2)) / np.sqrt(3) * np.sqrt(3) / 1.0])
# RT with 5-fold corners at 1 and 3-fold corners at sqrt(3)/(phi*sqrt(phi^2+1))*phi ... built from the icosahedron and its dual dodecahedron
Dd = ax['3'] * (np.sqrt(3) / np.sqrt(1 + ((1 + 5 ** .5) / 2) ** 2) / ((1 + 5 ** .5) / 2) * ((1 + 5 ** .5) / 2) ** 1)
hR = ConvexHull(np.vstack([I0, Dd])); edgesR = set()
for s in hR.simplices:
    for a_, b_ in itertools.combinations(s, 2):
        if (a_ < 12) != (b_ < 12): edgesR.add(tuple(sorted((a_, b_))))
Pall = np.vstack([I0, Dd]); RTm = [(Pall[a_] + Pall[b_]) / 2 for a_, b_ in edgesR]
out.append(f'   60-orbit angle from the nearest 5-fold axis: Ogdoecontahedron {ang5(m60):.4f} deg; truncated icosahedron (Bergman 60-shell) {ang5(TI):.4f} deg; '
           f'triacontahedron edge midpoints (Tsai 92-shell, {len(RTm)} points) {ang5(RTm):.4f} deg')
# ---- 3. face angles against tile angles
golden = [np.degrees(np.arctan(2)), 180 - np.degrees(np.arctan(2))]       # golden rhombus 63.435, 116.565 (faces of the golden rhombohedra)
pen = [36, 72, 108, 144]
def sums(target, parts, kmax=6):
    for k in range(1, kmax + 1):
        for c in itertools.combinations_with_replacement(parts, k):
            if abs(sum(c) - target) < 1e-6: return c
    return None
angs = {}
for e in pl:
    idx = [i for i in range(len(OG)) if abs(OGf[i] @ e[:3] + e[3]) < 1e-7]; Qp = OGf[idx]; c = Qp.mean(0)
    a = Qp[0] - c; a /= np.linalg.norm(a); b = np.cross(e[:3], a); Qp = Qp[np.argsort(np.arctan2((Qp - c) @ b, (Qp - c) @ a))]
    for i in range(len(Qp)):
        u_, w_ = Qp[i - 1] - Qp[i], Qp[(i + 1) % len(Qp)] - Qp[i]
        angs[round(float(np.degrees(np.arccos(u_ @ w_ / np.linalg.norm(u_) / np.linalg.norm(w_)))), 6)] = len(Qp)
res = [f'{a:.4f} ({"hexagon" if n == 6 else "kite"}): golden rhombi {sums(a, golden)}, Penrose {sums(a, pen)}' for a, n in sorted(angs.items())]
out.append('3. face angles as sums of tile angles (None = impossible with up to 6 tiles at the corner): ' + '; '.join(res))
print('\n'.join(out)); open('data/bridge.txt', 'w').write('\n'.join(out) + '\n')
