# DICTO 2026-10-18 octet study -- STEP 9: are the two notched, dented tetrahedra (T+ and T-) the same piece or mirror images?
# T- is T+ turned inside out through the OCD centre (the whole build is centrosymmetric), so they are the same piece exactly when T+
# with its 4 key dents and 6 middle-piece notches has a mirror symmetry. Test all 6 mirror planes of the regular tetrahedron on the
# corner sets of the keys and middle-piece hulls that touch it (float, tolerance 1e-9). -> data/step9-handedness.json
import itertools, numpy as np
from scipy.spatial import ConvexHull
from q5 import *
S1 = load('step1-ocd-exact.json'); S2 = load('step2-octet-frame.json'); S5 = load('step5-keyed-octet.json')
V = np.array([[qf(q(x)) for x in v] for v in S1['V']]); R = qf(q(S1['R']))
Tp = np.array([[qf(q(x)) for x in v] for v in S2['Tplus']]); Lf = np.array([[qf(q(x)) for x in v] for v in S2['lattice']]); C = Tp.mean(0)
E_t = ConvexHull(Tp).equations; near = lambda X: np.all(X @ E_t[:, :3].T + E_t[:, 3] <= 0.05, axis=1)
shifts = [np.array(ijk) @ Lf for ijk in itertools.product(range(-2, 3), repeat=3)]
K = [np.array([[qf(q(x)) for x in p] for p in Kk]) for Kk in S5['keys'].values()]
r = np.linalg.norm(V, axis=1); five = [i for i in range(len(V)) if r[i] > r.max() - 1e-9]
hulls = []
for i in five:
    c = V[i]; o = R * np.sign(np.where(np.abs(c) < 1e-9, 0, c)); star = V[sorted({j for f in S1['faces'] if i in f for j in f})]
    hulls.append(np.vstack([star, o - star]))
pts_k, pts_m = [], []
for s in shifts:
    for k in K:
        X = k + s
        if near(X).all(): pts_k.append(X)
    for h in hulls:
        X = h + s
        if near(X).sum() >= 3: pts_m.append(X)
Pk = np.vstack(pts_k) - C; Pm = np.vstack(pts_m) - C
def same_set(A, B): return all(np.min(np.linalg.norm(B - a, axis=1)) < 1e-9 for a in A)
mirrors = []
for i, j in itertools.combinations(range(4), 2):
    k, l = [x for x in range(4) if x not in (i, j)]
    n = np.cross(Tp[j] - Tp[i], (Tp[k] + Tp[l]) / 2 - Tp[i]); n /= np.linalg.norm(n)   # plane through edge ij and midpoint of kl
    refl = lambda P: P - 2 * np.outer(P @ n, n)
    mirrors.append(dict(edge=[i, j], keys_symmetric=same_set(refl(Pk), Pk), middle_symmetric=same_set(refl(Pm), Pm)))
rots = []
for ax in Tp - C:
    a = ax / np.linalg.norm(ax); ang = 2 * np.pi / 3; K_ = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    Rm = np.eye(3) + np.sin(ang) * K_ + (1 - np.cos(ang)) * K_ @ K_
    rots.append(same_set(Pk @ Rm.T, Pk) and same_set(Pm @ Rm.T, Pm))
any_mirror = any(m_['keys_symmetric'] and m_['middle_symmetric'] for m_ in mirrors)
checks = dict(keys_found=len(pts_k), middle_hulls_found=len(pts_m), mirrors=mirrors, threefold_turns_symmetric=rots,
              verdict='T+ and T- are the same piece' if any_mirror else 'T+ and T- are mirror images (a left and a right tetrahedron)')
print(json.dumps(checks, indent=1)); save('step9-handedness.json', dict(mark=MARK, step=9, status='float', checks=checks))
