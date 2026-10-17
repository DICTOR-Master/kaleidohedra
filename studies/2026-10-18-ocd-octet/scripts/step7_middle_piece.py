# DICTO 2026-10-18 octet study -- STEP 7 (first look, float): the shared middle piece (DICTO's choice 3) round m, the midpoint of the
# octahedron edge shared by the two OCDs whose five-fold stars face each other. Candidate: M = hull(star1 + star2) minus the two OCDs
# (symmetric under inversion through m). Where does it sit in the octet (caps of each octahedron, the 2 tetrahedra on the edge)?
# Section in the mirror plane x = 0, which holds c1, c2, the axis and the shared edge. -> data/step7-middle.json (2D coords + numbers)
import itertools, numpy as np
from scipy.spatial import ConvexHull
from q5 import *
S1 = load('step1-ocd-exact.json'); S4 = load('step4-stars.json'); S2 = load('step2-octet-frame.json')
V = np.array([[qf(q(x)) for x in v] for v in S1['V']]); R = qf(q(S1['R'])); o = np.array([0, R, R]); m = o / 2
r = np.linalg.norm(V, axis=1); i1 = [i for i in range(len(V)) if r[i] > r.max() - 1e-9 and abs(V[i, 0]) < 1e-9 and V[i, 1] > 0 and V[i, 2] > 0][0]
star1 = V[sorted({j for f in S1['faces'] if i1 in f for j in f})]; star2 = o - star1
E_o = ConvexHull(V).equations; H = ConvexHull(np.vstack([star1, star2])); E_h = H.equations
inside = lambda X, Eq: np.all(X @ Eq[:, :3].T + Eq[:, 3] <= 1e-12, axis=1)
Tp = np.array([[qf(q(x)) for x in v] for v in S2['Tplus']]); Tm = -Tp
# which tetrahedra hold the shared edge (0,R,0)-(0,0,R)? T+ at the origin cell and a T- translate
Lf = np.array([[qf(q(x)) for x in v] for v in S2['lattice']])
tets = []
for ijk in itertools.product(range(-2, 3), repeat=3):
    s_ = np.array(ijk) @ Lf
    for T in (Tp, Tm):
        X = T + s_
        if sum(np.allclose(X, p).any() if False else any(np.allclose(x, p) for x in X) for p in ([0, R, 0], [0, 0, R])) == 2: tets.append(X)
rng = np.random.default_rng(3); lo, hi = np.vstack([star1, star2]).min(0), np.vstack([star1, star2]).max(0)
P = rng.uniform(lo, hi, (400000, 3)); inH = inside(P, E_h); P = P[inH]; boxV = np.prod(hi - lo) * inH.mean()
in1 = inside(P, E_o); in2 = inside(P - o, E_o); M = ~in1 & ~in2; PM = P[M]
where = dict(cap_octa1=int(((np.abs(PM).sum(1) <= R)).sum()), cap_octa2=int(((np.abs(PM - o).sum(1) <= R)).sum()))
for k, X in enumerate(tets): where[f'tet{k+1}'] = int(inside(PM, ConvexHull(X).equations).sum())
inv = np.all([inside((2 * m - PM[:2000]), E_h)])
nums = dict(hull_volume=float(H.volume), middle_piece_volume=float(boxV * M.mean()), share_of_hull_in_OCDs=float(1 - M.mean()),
            tets_on_shared_edge=len(tets), middle_piece_samples=int(M.sum()), where_samples=where, inversion_symmetric=bool(inv))
print(nums)
# section x = 0 (2D coords y, z)
def sect(Eq, shift=np.zeros(3)):
    poly = [np.array(c) for c in [(-3, -3), (3, -3), (3, 3), (-3, 3)]]
    for e in Eq:
        a = e[1:3]; d = e[3] - e[:3] @ shift; out = []
        for i in range(len(poly)):
            A, B = poly[i], poly[(i + 1) % len(poly)]; da, db = a @ A + d, a @ B + d
            if da <= 0: out.append(A)
            if da * db < 0: out.append(A + (B - A) * da / (da - db))
        poly = out
        if len(poly) < 3: return []
    return [p.tolist() for p in poly]
dia = lambda c: [[c[0] + R, c[1]], [c[0], c[1] + R], [c[0] - R, c[1]], [c[0], c[1] - R]]
save('step7-middle.json', dict(mark=MARK, step=7, status='first look, float', numbers=nums, section_x0=dict(
    ocd1=sect(E_o), ocd2=sect(E_o, o), hull=sect(E_h), octa1=dia([0, 0]), octa2=dia([R, R]), m=[R / 2, R / 2], c1=V[i1, 1:].tolist(), c2=(o - V[i1])[1:].tolist())))
# do the step-5 keys (bumps of both OCDs) reach into the candidate middle piece?
S5 = load('step5-keyed-octet.json'); hitk = {}
for nm, K in S5['keys'].items():
    Kf = np.array([[qf(q(x)) for x in p] for p in K]); Ek = ConvexHull(Kf).equations
    for lab, sh in (('ocd1', np.zeros(3)), ('ocd2', o)):
        c = int(inside(PM - sh, Ek).sum())
        if c: hitk[f'{lab} key {nm}'] = c
print('keys inside middle piece (samples):', hitk)
d7 = load('step7-middle.json'); d7['numbers']['key_samples_inside_middle'] = hitk; save('step7-middle.json', d7)
