# Catalogue step A: how far can a piece "see"? For each stacking and λ across the walk, the largest distance from a site to a corner
# of its cell (R). A site q can shape p's cell only if its bisector comes within R of p, i.e. |q − p| ≤ 2R + (w_q − w_p)/|q − p|
# (|Δw| ≤ 3/8 here). The exact census then re-checks the chosen distance bound on every stretch (bound_ok).
import itertools, numpy as np
from scipy.spatial import HalfspaceIntersection
from scipy.optimize import linprog
from stackings import net_for
d0 = (2 / 3) ** 0.5
def sites_of(word):
    net = net_for(word); G = np.array(net['G'], float); L = np.linalg.cholesky(G)
    M = [(k, L.T @ np.array([float(c) for c in p])) for k, p in net['motif']]
    T = [L.T @ np.array(t, float) for t in ((1, 0, 0), (0, 1, 0), (0, 0, 1))]
    S = [(k, p + a * T[0] + b * T[1] + c * T[2]) for a, b, c in itertools.product(range(-3, 4), range(-3, 4), range(-2, 3)) for k, p in M]
    return M, S
def radius(M, S, i, lam):
    w = lambda k: lam if k == 'tet' else 0.0; kp, p = M[i]; H = []
    for k, q in S:
        dv = q - p
        if np.allclose(dv, 0) or dv @ dv > 16: continue
        H.append(np.r_[2 * dv, -(q @ q - p @ p - w(k) + w(kp))])
    H = np.array(H); A, b = H[:, :3], -H[:, 3]
    r = linprog([0, 0, 0, -1], A_ub=np.c_[A, np.linalg.norm(A, axis=1)], b_ub=b, bounds=[(None, None)] * 3 + [(0, None)])
    if r.x[3] < 1e-7: return 0.0
    V = HalfspaceIntersection(H, r.x[:3]).intersections
    return float(np.max(np.linalg.norm(V - p, axis=1)))
Rmax = 0
for word in ('ABC', 'AB', 'ABAC', 'ABCACB'):
    M, S = sites_of(word); R = 0
    for lam in np.linspace(-0.374, 0.374, 61):
        for i in range(len(M)): R = max(R, radius(M, S, i, lam))
    Rmax = max(Rmax, R); print(f'{word}: largest piece radius over the walk R = {R:.6f}  (= {R / d0:.3f} layer spacings)', flush=True)
reach = 2 * Rmax + 0.375 / (2 * Rmax)
print(f'max R = {Rmax:.6f}; a site can matter only within {reach:.6f} = {reach / d0:.3f} layer spacings; suggested D2 = {(reach + 0.05) ** 2:.4f}')
