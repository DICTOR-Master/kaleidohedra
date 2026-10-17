# DICTO 2026-10-18 octet study -- STEP 5: the keyed octet with DICTO's chosen key (the tetrahedral envelope corner, step 3).
# The key's base reaches the octahedron edges, so a dent INSIDE the OCD would also cut the caps; so the keys go out as bumps on all 8
# joint faces (OCD + 8 keys = one piece, the OCD with its envelope corners) and both tetrahedra take 4 dents each.
# Exact: the 4 keys entering one tetrahedron each stay inside that face's pyramid to the tetrahedron centre (so they never overlap);
# volumes. Float: sampling, every point in exactly one piece. -> data/step5-keyed-octet.json
import itertools, numpy as np
from scipy.spatial import ConvexHull
from q5 import *
S1 = load('step1-ocd-exact.json'); S2 = load('step2-octet-frame.json'); S3 = load('step3-key-candidate.json')
V = [[q(x) for x in v] for v in S1['V']]; R = q(S1['R']); key0 = [[q(x) for x in v] for v in S3['key']]
Tp = [[q(x) for x in v] for v in S2['Tplus']]; Tm = [[q(x) for x in v] for v in S2['Tminus']]; L = [[q(x) for x in v] for v in S2['lattice']]
signs = list(itertools.product([1, -1], repeat=3))
sv = lambda v, s: [x if si > 0 else qn(x) for x, si in zip(v, s)]
keys = {s: [sv(p, s) for p in key0] for s in signs}                 # key on the joint face of sign pattern s (Th: sign flips map keys)
# the key over face s must be the RT corner there too: check its apex is an RT corner (sign flips are symmetries of the RT)
def in_pyr(p, apex, F):   # p inside pyramid (apex, triangle F)? exact half-space tests
    pts = [apex] + F
    for i in range(4):
        G = [pts[j] for j in range(4) if j != i]; n = cross(vsub(G[1], G[0]), vsub(G[2], G[0]))
        if sgn(dot(n, vsub(pts[i], G[0]))) < 0: n = [qn(x) for x in n]
        if sgn(dot(n, vsub(p, G[0]))) < 0: return False
    return True
def tet_keys(T):
    """the 4 keys entering tetrahedron T: for each face, the octahedron centre across it and its key; check inside face pyramid."""
    cen = [qm(qa(qa(qa(T[0][k], T[1][k]), T[2][k]), T[3][k]), qr(Fr(1, 4))) for k in range(3)]
    out, ok = [], True
    for tri in itertools.combinations(range(4), 3):
        F = [T[i] for i in tri]
        for c in [[Z, Z, Z]] + [vadd(vmul(L[i], qr(a)), [Z, Z, Z]) for i in range(3) for a in (1, -1)] + [vsub(vmul(L[i], ONE), L[j]) for i in range(3) for j in range(3) if i != j]:
            rel = [vsub(x, c) for x in F]
            l1 = lambda v: qa(qa(*[x if sgn(x) >= 0 else qn(x) for x in v[:2]]), v[2] if sgn(v[2]) >= 0 else qn(v[2]))
            if all(l1(x) == R for x in rel):
                fc = [qa(qa(rel[0][k], rel[1][k]), rel[2][k]) for k in range(3)]; s = tuple(sgn(x) for x in fc)
                K = [vadd(p, c) for p in keys[s]]; ok &= all(in_pyr(p, cen, F) for p in K); out.append(K); break
    return out, ok
kp, okp = tet_keys(Tp); km, okm = tet_keys(Tm)
kv = q(S3['checks']['key_volume']); tv = q(S2['checks']['tet_volume']); ov = q(S2['checks']['ocd_volume']); cap = q(S2['checks']['cap_volume_each'])
piece_ocd = qa(ov, qm(qr(8), kv)); piece_tet = qs(tv, qm(qr(4), kv))
cell = q(S2['checks']['cell_volume']); total = qa(qa(piece_ocd, qm(qr(6), cap)), qm(qr(2), piece_tet))
# float sampling over lattice translates
f3 = lambda v: np.array([qf(x) for x in v]); Vf = np.array([f3(v) for v in V]); E_o = ConvexHull(Vf).equations
Ek = [ConvexHull(np.array([f3(p) for p in keys[s]])).equations for s in signs]
Etp = ConvexHull(np.array([f3(v) for v in Tp])).equations; Etm = ConvexHull(np.array([f3(v) for v in Tm])).equations; Rf = qf(R)
inside = lambda X, Eq: np.all(X @ Eq[:, :3].T + Eq[:, 3] <= 1e-12, axis=1)
Lf = np.array([f3(v) for v in L]); rng = np.random.default_rng(11); P = rng.uniform(-1.6, 1.6, (200000, 3))
cnt = np.zeros(len(P), int)
for ijk in itertools.product(range(-3, 4), repeat=3):
    s_ = np.array(ijk) @ Lf
    if np.linalg.norm(s_) > 4.3: continue
    X = P - s_; io = inside(X, E_o); ik = np.zeros(len(P), bool)
    for Eq in Ek: ik |= inside(X, Eq)
    cnt += io | ik                                         # OCD with its 8 keys
    cnt += (np.abs(X).sum(1) <= Rf + 1e-12) & ~io          # the 6 caps (shell)
    cnt += inside(X, Etp) & ~ik; cnt += inside(X, Etm) & ~ik   # dented tetrahedra (keys of THIS octahedron only would be wrong:
# a tetrahedron's dents come from 4 different octahedra) -- so recount the tets against ALL keys:
cnt2 = np.zeros(len(P), int); kall = np.zeros(len(P), bool); tets = np.zeros(len(P), int); ocds = np.zeros(len(P), int)
for ijk in itertools.product(range(-3, 4), repeat=3):
    s_ = np.array(ijk) @ Lf
    if np.linalg.norm(s_) > 4.3: continue
    X = P - s_; io = inside(X, E_o); ik = np.zeros(len(P), bool)
    for Eq in Ek: ik |= inside(X, Eq)
    kall |= ik; ocds += io | ik; cnt2 += (np.abs(X).sum(1) <= Rf + 1e-12) & ~io; tets += inside(X, Etp).astype(int) + inside(X, Etm)
total_cnt = ocds + cnt2 + np.where(kall, 0, tets)
sampling = dict(points=len(P), exactly_one=int((total_cnt == 1).sum()), none=int((total_cnt == 0).sum()), two_or_more=int((total_cnt >= 2).sum()))
checks = dict(keys_inside_face_pyramids_Tplus=okp, keys_inside_face_pyramids_Tminus=okm, keys_per_tet=(len(kp), len(km)),
              piece_OCD_with_8_keys=qs_(piece_ocd), piece_OCD_float=qf(piece_ocd), cap=qs_(cap), cap_float=qf(cap),
              piece_tet_with_4_dents=qs_(piece_tet), piece_tet_float=qf(piece_tet), pieces_sum_equals_cell=total == cell, sampling=sampling)
print(checks); assert okp and okm and total == cell
save('step5-keyed-octet.json', dict(mark=MARK, step=5, key_choice='tetrahedral envelope corner (DICTO 2026-10-18)', keys={''.join('+' if x > 0 else '-' for x in s): [[qs_(x) for x in p] for p in keys[s]] for s in signs}, checks=checks))
