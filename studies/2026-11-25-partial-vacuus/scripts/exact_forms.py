# DICTO · partial Vacuus 1b: closed forms of the special depths (26 Nov 2026). With Claude (Anthropic).
# Each depth recomputed at full double precision (least-squares over EVERY wall of the solid, not one), then mpmath.findpoly
# (degree <= 4, coefficients <= 10^4); a polynomial is kept only if its root matches to 1e-13 and it is the lowest degree found.
import json, os, sys, numpy as np, mpmath as mp
HERE = os.path.dirname(os.path.abspath(__file__)); sys.argv = [sys.argv[0]]
exec(open(os.path.join(HERE, 'special_depths_all.py')).read().split('found = []')[0])
found = json.load(open(os.path.join(HERE, '../data-special-all.json'))); mp.mp.dps = 30; out = []; seen = set()
for f in found:
    key = (f['P'], round(f['s'], 6))
    if key in seen: continue
    seen.add(key); V, F, N, D = S[f['P']]; W = walls(V, F, N, D)
    # refine s: every wall normal m0 + a m1 (a = s d) must be parallel to some face normal of lam Q; minimise sum |m x w|^2 over s
    VQ, FQ, NQ0, DQ = S[f['Q']]
    def resid(s):
        r = 0.0
        for fj, m0, m1, u in W:
            m = m0 + s * D[fj] * m1; m /= np.linalg.norm(m)
            r += min(np.linalg.norm(np.cross(m, M @ w)) ** 2 for M in FRAME for w in NQ0)
        return r
    from scipy.optimize import minimize_scalar
    s0 = f['s']; r = minimize_scalar(resid, bounds=(s0 - 1e-6, s0 + 1e-6), method='bounded', options={'xatol': 1e-16})
    s = float(r.x); best = None
    for deg in (1, 2, 3, 4):
        c = mp.findpoly(mp.mpf(s), deg, maxcoeff=10 ** 4, tol=1e-13)
        if c: best = c; break
    out.append(dict(P=f['P'], Q=f['Q'], s=s, poly=best)); print(f"{f['P']:26s} on {f['Q']:30s} s = {s:.15f}  minimal polynomial (coeffs, highest first): {best}", flush=True)
json.dump(out, open(os.path.join(HERE, '../data-exact-forms.json'), 'w'), indent=1)
print('FINAL ok' if all(o['poly'] for o in out) else 'FINAL partial (some depths without a small polynomial)')
