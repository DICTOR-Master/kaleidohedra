import sys, numpy as np
sys.path.insert(0, 'scripts/_lib'); import methods as M
exec(open('scripts/measures.py').read().split("out = {}")[0])
from scipy.special import sph_harm_y
def q0(P, l):  # m=0 coefficient about a 3-fold axis (1,1,1): rotate axis to z
    a = np.array([1, 1, 1])/3**.5; z = np.array([0, 0, 1.]); v = np.cross(a, z); s = np.linalg.norm(v); c = a @ z
    K = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]]); R = np.eye(3) + K + K @ K*((1 - c)/s**2)
    u = P @ R.T; u = u/np.linalg.norm(u, axis=1)[:, None]
    return float(sph_harm_y(l, 0, np.arccos(np.clip(u[:, 2], -1, 1)), np.arctan2(u[:, 1], u[:, 0])).mean().real)
mus = np.linspace(1.001, 2.999, 1999); prev = None; out = {4: [], 6: []}
for m in mus:
    P = poly(m); v = {l: q0(P, l) for l in (4, 6)}
    if prev:
        for l in (4, 6):
            if v[l]*prev[1][l] < 0: out[l].append(round((m + prev[0])/2, 4))
    prev = (m, v)
print('sign changes (mu in (1,3); mirror at 1/mu):', out, '| Q6 at octahedron', M.Q3d(poly(1.0), 6), 'at mu=2', M.Q3d(poly(2.0), 6))
