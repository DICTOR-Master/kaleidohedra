#!/usr/bin/env python3
"""Quick certified checks of the design loci left open by the short 4D runs: a certified seed on the H4 curve T12 = T20 = 0
(Krawczyk on T12, T20 and a linear slice), and the realizability of the single D4 7-design u-point (u2, u3, u4) = (4, 4, 5)."""
import sys, os, json, warnings
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
warnings.filterwarnings('ignore')
import numpy as np
from flint import arb
import sil, symm
from four_d import newton, fold, hsys_float, utarget_float, seeds_for, certify_seed, tone_status
rng = np.random.default_rng(5); out = {}
H = sil.H('H4'); F00 = hsys_float(H, [(12, 0), (20, 0)]); found = []
sc = np.array([abs(F00(np.array([0.3, 0.2, 0.25, 0.25]))[0][i]) for i in range(2)] + [1.0])   # equation scales (values are ~1e6..1e10)
def F0(c):
    f, J = F00(c); return f/sc, J/sc[:, None]
for _ in range(300):
    a = rng.normal(size=4)
    c0 = rng.dirichlet(np.ones(4)); val = a @ c0
    def F(c, a=a, val=val):
        f, J = F0(c); return np.append(f, a @ c - val), np.vstack([J, a])
    c = newton(F, c0)
    if c is None or np.any(~np.isfinite(c)): continue
    cc = fold(H, c); cc = cc/cc.sum()
    if cc.min() > 1e-6: found.append(cc)
print('H4: seeds found on T12 = T20 = 0:', len(found))
cert = []
for cc in found[:5]:
    a = np.zeros(4); a[0] = 1; val = cc[0]
    def Fa(z):
        return [H.h_arb(12, z)[0], H.h_arb(20, z)[0], z[0] - arb(float(val)), sum(z, arb(0)) - 1]
    def Ja(z):
        ub = H.u_arb(z); r = []
        for k in (12, 20): r.append(H.h_arb(k, z, jac=True, ub=ub)[1][0])
        return r + [[arb(1), arb(0), arb(0), arb(0)], [arb(1)]*4]
    cs = np.array(cc); cs[0] = float(val)
    st, bx = sil.krawczyk(Fa, Ja, list(cs), 1e-10)
    if st == 'unique':
        stt = tone_status(H, bx, 48); cert.append({'seed': cc.tolist(), 'zero_degrees': [k for k, v in stt.items() if v == 'zero?']})
        print('H4 certified curve point', np.round(cc, 6).tolist(), 'zero', cert[-1]['zero_degrees'])
zs = sorted(found, key=lambda c: c[0])
out['H4_curve'] = {'n_found': len(found), 'certified': cert, 'c0_range': [float(zs[0][0]), float(zs[-1][0])] if zs else None}
D = sil.H('D4'); F = utarget_float(D, [], [(1, 4.0), (2, 4.0), (3, 5.0)]); s = seeds_for(D, F, 400, rng)
print('D4 7-design u-point (4,4,5): seeds found', [np.round(x, 6).tolist() for x in s])
rec = []
for cc in s:
    bx = certify_seed(D, [(4, 0), (4, 1), (6, 0)], cc) if cc.min() > 1e-5 else None
    r = {'seed': cc.tolist(), 'certified': bx is not None}
    if bx is not None:
        stt = tone_status(D, bx, 24); r['zero_degrees'] = [k for k, v in stt.items() if v == 'zero?']; r['symmetry'] = symm.explain(D, cc)
    rec.append(r); print('D4', r)
out['D4_7design'] = rec
json.dump(out, open(os.path.join(HERE, '..', 'data', 'curves-check.json'), 'w'), indent=1, default=str)
