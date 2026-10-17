# DICTO 2026-10-18 octet study -- STEP 2: the octet truss frame round the OCD, exact.
# Octahedra |x|+|y|+|z| <= R (R = 2phi/3) on the fcc lattice R*(1,1,0)-type; regular tetrahedra of the same edge fill the rest:
#   T+ = conv(R e_x, R e_y, R e_z, R(1,1,1)) and T- = -T+ (one of each per lattice cell).
# Proves exactly: octa + 2 tets = cell volume; every face of T+ lies on an octahedron face whose normal has sign product +1 (the class
# of (1,1,1)), every face of T- on class -1. So the 8 joint hexagons split 4 + 4 between T+ and T- -- the bump/dent layout.
# Exact OCD volume too. Then a float sampling test: every point of space in exactly one of OCD / octa-minus-OCD (shell) / T+ / T-.
import itertools, numpy as np
from q5 import *
S1 = load('step1-ocd-exact.json'); V = [[q(x) for x in v] for v in S1['V']]; R = q(S1['R'])
e = [[ONE if i == j else Z for j in range(3)] for i in range(3)]
Tp = [vmul(e[0], R), vmul(e[1], R), vmul(e[2], R), [R, R, R]]
Tm = [[qn(x) for x in v] for v in Tp]
L = [[R, R, Z], [R, Z, R], [Z, R, R]]
cellV = det3(*L); cellV = cellV if sgn(cellV) > 0 else qn(cellV)
octV = qm(qr(Fr(4, 3)), qm(R, qm(R, R)))
def tetvol(T):
    d = det3(vsub(T[1], T[0]), vsub(T[2], T[0]), vsub(T[3], T[0])); d = d if sgn(d) > 0 else qn(d); return qm(d, qr(Fr(1, 6)))
# exact OCD volume: fan of tetrahedra from the origin over each face (faces are planar polygons; fan-triangulate each)
Vf = np.array([[qf(x) for x in v] for v in V]); ocdV = Z
for f in S1['faces']:
    P = Vf[f]; c = P.mean(0); n = np.cross(P[1] - P[0], P[2] - P[0]); n = n if n @ c > 0 else -n
    u = P[0] - c; w = np.cross(n, u); order = [f[i] for i in np.argsort(np.arctan2((P - c) @ w, (P - c) @ u))]
    for i in range(1, len(order) - 1):
        d = det3(V[order[0]], V[order[i]], V[order[i + 1]]); ocdV = qa(ocdV, d if sgn(d) > 0 else qn(d))
ocdV = qm(ocdV, qr(Fr(1, 6)))
fill_ok = qa(octV, qa(tetvol(Tp), tetvol(Tm))) == cellV
# faces of T+: which octahedron (lattice point c) carries each, and the sign class of that octahedron face's normal
def lattice_pts(n=2):
    for ijk in itertools.product(range(-n, n + 1), repeat=3):
        p = [Z, Z, Z]
        for c, Lv in zip(ijk, L): p = vadd(p, vmul(Lv, qr(c)))
        yield p
def face_class(T):
    res = []
    for tri in itertools.combinations(range(4), 3):
        F = [T[i] for i in tri]; cen = [qm(qa(qa(F[0][k], F[1][k]), F[2][k]), qr(Fr(1, 3))) for k in range(3)]
        hits = []
        for c in lattice_pts():
            rel = [vsub(x, c) for x in F]
            l1 = lambda v: qa(qa(*[x if sgn(x) >= 0 else qn(x) for x in v[:2]]), v[2] if sgn(v[2]) >= 0 else qn(v[2]))
            if all(l1(x) == R for x in rel):
                sg = [sgn(x) for x in vsub(cen, c)]
                if 0 not in sg: hits.append(([qs_(x) for x in c], sg[0] * sg[1] * sg[2]))
        res.append(hits)
    return res
fp, fm = face_class(Tp), face_class(Tm)
classes_ok = all(len(h) == 1 and h[0][1] == 1 for h in fp) and all(len(h) == 1 and h[0][1] == -1 for h in fm)
# float sampling: membership count must be exactly 1 everywhere (OCD, shell = octa minus OCD, T+, T-), on lattice translates
from scipy.spatial import ConvexHull
E_ocd = ConvexHull(Vf).equations; Rf = qf(R)
Lf = np.array([[qf(x) for x in v] for v in L]); Tpf = np.array([[qf(x) for x in v] for v in Tp])
Etp = ConvexHull(Tpf).equations; Etm = ConvexHull(-Tpf).equations
rng = np.random.default_rng(7); P = rng.uniform(-1.6, 1.6, (200000, 3)); cnt = {k: np.zeros(len(P), int) for k in ('ocd', 'shell', 'T+', 'T-')}
shifts = [np.array(c) @ Lf for c in itertools.product(range(-3, 4), repeat=3)]; shifts = [s for s in shifts if np.linalg.norm(s) < 4.2]
for s in shifts:
    X = P - s; ino = np.abs(X).sum(1) <= Rf + 1e-12; iocd = np.all(X @ E_ocd[:, :3].T + E_ocd[:, 3] <= 1e-12, axis=1)
    cnt['ocd'] += iocd; cnt['shell'] += ino & ~iocd
    cnt['T+'] += np.all(X @ Etp[:, :3].T + Etp[:, 3] <= 1e-12, axis=1); cnt['T-'] += np.all(X @ Etm[:, :3].T + Etm[:, 3] <= 1e-12, axis=1)
tot = sum(cnt.values()); sampling = dict(points=len(P), exactly_one=int((tot == 1).sum()), none=int((tot == 0).sum()), two_or_more=int((tot >= 2).sum()))
checks = dict(cell_volume=qs_(cellV), octa_volume=qs_(octV), tet_volume=qs_(tetvol(Tp)), ocd_volume=qs_(ocdV), ocd_volume_float=qf(ocdV),
              octa_plus_two_tets_equals_cell=fill_ok, Tplus_faces_on_class_plus_octa_faces=classes_ok and True,
              shell_volume=qs_(qs(octV, ocdV)), cap_volume_each=qs_(qm(qs(octV, ocdV), qr(Fr(1, 6)))), cap_volume_float=qf(qs(octV, ocdV)) / 6,
              ocd_fill_of_octa=qf(ocdV) / qf(octV), sampling=sampling)
print(checks); assert fill_ok and classes_ok
save('step2-octet-frame.json', dict(mark=MARK, step=2, lattice=[[qs_(x) for x in v] for v in L], Tplus=[[qs_(x) for x in v] for v in Tp],
     Tminus=[[qs_(x) for x in v] for v in Tm], Tplus_faces=fp, Tminus_faces=fm, checks=checks))
