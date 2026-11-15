#!/usr/bin/env python3
"""Lead: where do B's 40 visible plates (phi*sqrt2 triangles) lie? Test against the walls (60 H4 mirrors) of the Galois-twin
600-cell P' = closure under self-reflection of X' = perms of (s^2, s^2, s^2, s, 0), s = -1/phi (sqrt5 -> -sqrt5 applied to X).
Controls: P' has 120 corners and 60 mirrors; P and P' share only the S5 mirrors (expected 10)."""
import runpy, sys, io, contextlib, itertools, numpy as np
with contextlib.redirect_stdout(io.StringIO()):
    g = runpy.run_path(sys.argv[1] if len(sys.argv) > 1 else 'walls.py')
orbit, to4, canon, F, X, faces2, plane_normal, mirrors = (g[k] for k in ('orbit', 'to4', 'canon', 'F', 'X', 'faces2', 'plane_normal', 'mirrors'))
s = (1 - 5 ** .5) / 2
Xt5 = orbit((s*s, s*s, s*s, s, 0)); Xt = to4(Xt5, Xt5.mean(0))
key = lambda u: tuple(np.round(u, 6) + 0.0); Pd = {key(v): v for v in Xt}; grow = True
while grow:
    grow = False; A_ = list(Pd.values())
    for v in A_:
        for w in A_:
            u = w - 2 * (w @ v) / (v @ v) * v; k = key(u)
            if k not in Pd: Pd[k] = u; grow = True
    if len(Pd) > 200: raise SystemExit('closure exploded')
Pt = np.array(list(Pd.values())); print("twin 600-cell P' corners:", len(Pt))
mt = np.unique(np.round([canon(v) for v in Pt], 9), axis=0); print("P' mirrors:", len(mt))
shared = sum(np.min(np.linalg.norm(mirrors - n, axis=1)) < 1e-7 for n in mt); print('mirrors shared by P and P\':', shared)
res = {}
for nm, V in (('A', X), ('B', F)):
    fac, rid = faces2(V); r = {}
    for c in rid:
        n = plane_normal(V, c); k = (len(c), bool(np.min(np.linalg.norm(mirrors - n, axis=1)) < 1e-7), bool(np.min(np.linalg.norm(mt - n, axis=1)) < 1e-7))
        r[k] = r.get(k, 0) + 1
    res[nm] = r; print(nm, 'by (corners, P wall, twin P\' wall):', r)
allB = sum(v for k, v in res['B'].items() if k[1] or k[2])
print(f'B plates in the walls of P or its twin: {allB} of 80')
checks = [len(Pt) == 120, len(mt) == 60]
print('checks', checks); print('FINAL ok' if all(checks) else 'FINAL FAIL checks')
