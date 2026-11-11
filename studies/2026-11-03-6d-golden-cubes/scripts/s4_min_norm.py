"""Step 4: for each named depth mu of the cube x octahedron sections (s3 part C), the shortest lattice vectors v in Z^6
whose shadow orbit on F_mu is the section's corner set (search box {-4..4}^6 in floating point, every hit then confirmed
exactly in K). Sweep vectors (shadow = section for every mu) are excluded: a hit must fail at mu +- 0.01.
Expected: Icosaxes (phi) norm 2 (the mixed D6 roots); Golden Cut Cubes: no vector at all (s3: degree argument).
usage (compute-host): python3 s4_min_norm.py -> ../data/s4-min-norm.json
"""
from sixd_lib import *          # noqa
import numpy as np

xG, xL = x_golden(4)
targets = [('Unborn Axes', 3 - PHI), ('Icosaxes', PHI), ('truncated octahedron', K(Fr(3, 2))),
           ('cut cube 2 + 1/phi^2', 2 + PHI.inv() * PHI.inv()), ('Greater Golden Cut Cube', 3 - 2 * xG),
           ('truncated cube', 1 + S2), ('Lesser Golden Cut Cube', 3 - 2 * xL), ('cut cube 2 + 1/phi', 2 + PHI.inv())]
r = np.arange(-4, 5)
V = np.array(np.meshgrid(*[r] * 6, indexing='ij')).reshape(6, -1).T
V = V[np.any(V != 0, axis=1)]
N = (V ** 2).sum(1)


def pattern_ok(mu, VV, tol=1e-9):
    w = np.abs(VV[:, :3] + VV[:, 3:] / mu); w = -np.sort(-w, axis=1)
    ok = w[:, 0] > 1e-12; w = w / np.where(ok, w[:, 0], 1)[:, None]
    if mu > 2: pat = np.array([1, 1, mu - 2])
    else: pat = np.array([1, mu - 1, 0])
    return ok & np.all(np.abs(w - pat) < tol, axis=1)


def exact_ok(mu, v):
    w = [K(v[k]) + K(v[k + 3]) / mu for k in range(3)]
    a = sorted([x if x >= 0 else -x for x in w], key=float, reverse=True)
    pat = (ONE, ONE, mu - 2) if mu > 2 else (ONE, mu - 1, ZERO)
    return not a[0].iszero() and all(a[q] == a[0] * pat[q] for q in range(3))


out = {}
for name, mu in targets:
    f = float(mu)
    hit = pattern_ok(f, V) & ~pattern_ok(f + 0.01, V, 1e-6) & ~pattern_ok(f - 0.01, V, 1e-6)
    if hit.any():
        nmin = int(N[hit].min()); best = [tuple(int(x) for x in v) for v in V[hit & (N == nmin)]][:3]
        ok = all(exact_ok(mu, v) for v in best)
        check(f'{name} (mu ~ {f:.6f}): shortest selecting vectors have norm {nmin}, e.g. {best[0]} (exact)', ok)
        out[name] = {'mu': kstr(mu), 'min_norm': nmin, 'examples': best}
    else:
        out[name] = {'mu': kstr(mu), 'min_norm': None}
        check(f'{name} (mu ~ {f:.6f}): no selecting vector in {{-4..4}}^6', 'Golden' in name)
dump('s4-min-norm.json', out)
