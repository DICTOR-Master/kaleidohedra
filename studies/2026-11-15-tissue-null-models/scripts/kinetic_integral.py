"""Independent second method for the linear-motion contact-change rate of a moving Poisson-Voronoi tessellation:
an integral over the typical Poisson-Delaunay simplex instead of a time-stepped simulation.
A flip happens when a seed crosses the circumsphere of a Delaunay simplex. The outside of an empty circumsphere is
an unconditioned Poisson field, so the crossing rate of one simplex is  n * (surface integral) E[(u.e - w.e)+],
u.e = normal speed of the moving circumsphere (from the vertices' velocities), w = an outside seed's velocity.
Typical Poisson-Delaunay simplex (Miles 1970; Moller 1989): circumradius density ~ R^(d^2-1) exp(-n kappa_d R^d),
vertex directions uniform on the sphere weighted by the simplex volume.
Bookkeeping: 2D, each T1 = 2 crossings, contact changes (lost+made) per cell = 2 * T1 per cell = (2 tri/cell) * rate / 2 * 2.
3D, a 2-3 flip = 2 crossings, a 3-2 flip = 3 crossings (equal numbers in steady state): changes per cell
= (24 pi^2/35 tets/cell) * rate / 2.5.  Velocities: components N(0, s^2); rms displacement rate s*sqrt(d); ell = n^(-1/d).
Usage: kinetic_integral.py [--pilot] OUT.json"""
import sys, json, math
import numpy as np
from scipy.stats import norm

PILOT = '--pilot' in sys.argv; OUT = sys.argv[-1]
rng = np.random.default_rng(7)
M = 20000 if PILOT else 400000
res = {}


def unit(d, k):
    x = rng.normal(size=(k, d)); return x / np.linalg.norm(x, axis=-1, keepdims=True)


def rate(d, M, nq):
    n = 1.0; s = 1.0
    kappa = math.pi if d == 2 else 4 * math.pi / 3
    # n kappa R^d ~ Gamma(d, 1) for density R^(d^2-1) exp(-n kappa R^d)
    R = (rng.gamma(d, 1.0, size=M) / (n * kappa)) ** (1 / d)
    E = np.stack([unit(d, M) for _ in range(d + 1)], axis=1)  # M x (d+1) x d directions
    X = R[:, None, None] * E
    D = X[:, 1:] - X[:, :1]
    vol = np.abs(np.linalg.det(D))
    V = rng.normal(size=X.shape) * s
    # circumcentre is 0; derivative: (x_k - x_0).cdot = x_k.v_k - x_0.v_0 - (v_k - v_0).c  with c = 0
    rhs = (X[:, 1:] * V[:, 1:]).sum(-1) - (X[:, :1] * V[:, :1]).sum(-1)
    cdot = np.linalg.solve(D, rhs[..., None])[..., 0]
    Rdot = (X[:, 0] * (V[:, 0] - cdot)).sum(-1) / R
    # quadrature over the sphere: random directions, nq per simplex
    Q = unit(d, M * nq).reshape(M, nq, d)
    a = (cdot[:, None, :] * Q).sum(-1) + Rdot[:, None]       # normal speed of the boundary
    flux = a * norm.cdf(a / s) + s * norm.pdf(a / s)          # E[(a - Z)+], Z ~ N(0, s^2)
    area = 2 * math.pi * R if d == 2 else 4 * math.pi * R ** 2
    per = n * area * flux.mean(1)
    shape = vol / R ** d          # volume of the simplex on the unit sphere
    w = shape / shape.mean()
    vals = per * w
    mean = vals.mean(); err = vals.std() / math.sqrt(M)
    if d == 2:
        changes = 2 * mean          # T1 per cell = (2 triangles/cell) * rate / 2 ; changes = 2 T1
        f = 2.0
    else:
        tets = 24 * math.pi ** 2 / 35
        changes = tets * mean / 2.5
        f = tets / 2.5
    disp_rate = s * math.sqrt(d)   # rms displacement per unit time, ell = 1
    return changes / disp_rate, f * err / disp_rate


for d in (2, 3):
    c, e = rate(d, M, 64)
    res[f'{d}D'] = {'changes_per_cell_per_ell': c, 'err': e}
    print(f'{d}D linear motion: contact changes per cell per ell of rms displacement = {c:.4f} +- {e:.4f}', flush=True)
    print(f'PROGRESS {(d - 1) / 2:.2f} dims', flush=True)
json.dump(res, open(OUT, 'w'), indent=1)
ok = all(np.isfinite(v['changes_per_cell_per_ell']) and v['err'] < 0.02 * v['changes_per_cell_per_ell'] for v in res.values())
print('X ' + ('PASS' if ok else 'FAIL') + ' integrals finite with relative error < 2 %', flush=True)
print('FINAL ok' if ok else 'FINAL FAIL', flush=True)
