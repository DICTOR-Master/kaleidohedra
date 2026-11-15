#!/usr/bin/env python3
"""The two golden A4 edge points (main-census lead): full symmetry order of the corner sets and whether the joint zero set of the
two silent tones is a curve through them reaching into the 3-parameter seed space (Jacobian rank + numeric continuation)."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import sil, symm
from four_d import newton, fold
H = sil.H('A4'); phi = (1 + 5**0.5)/2; F = symm.frame(H); out = {}
for name, (a, b, t), degs in [('T5=T7 edge (0,1)', (0, 1, 1/phi), (5, 7)), ('T3=T6 edge (0,2)', (0, 2, phi), (3, 6))]:
    c = np.zeros(4); c[a] = 1; c[b] = t; c /= c.sum()
    P = symm.orbit(H, c); so = symm.sym_order(P @ F)
    J = np.array([H.h_float(k, c, jac=True)[1][0] for k in degs] + [np.ones(4)])
    sv = np.linalg.svd(J, compute_uv=False)
    ker = np.linalg.svd(J)[2][-1]
    # continuation along the kernel direction (both signs), Newton back to the curve with a slice
    traces = []
    for sgn in (1, -1):
        cc = c.copy(); d = sgn*ker; pts = []
        for step in range(40):
            guess = cc + 0.004*d; a_ = d.copy(); val = a_ @ guess
            def Fn(z):
                f = [H.h_float(k, z, jac=True) for k in degs]
                return (np.array([x[0][0] for x in f] + [z.sum() - 1, a_ @ z - val]),
                        np.array([x[1][0] for x in f] + [np.ones(4), a_]))
            z = newton(Fn, guess)
            if z is None: break
            d = (z - cc)/np.linalg.norm(z - cc); cc = z; pts.append(cc.tolist())
        traces.append({'direction': sgn, 'steps': len(pts), 'min_c_along': [float(min(p)) for p in pts[:10]], 'end': pts[-1] if pts else None})
    rec = {'seed': c.tolist(), 'orbit': len(P), 'full_symmetry_order': so, 'A4_order': 120,
           'jacobian_singular_values': sv.tolist(), 'kernel_direction': ker.tolist(), 'continuation': traces}
    out[name] = rec
    print(name, 'orbit', len(P), 'symmetry order', so, 'sv', np.round(sv, 6).tolist(), 'kernel', np.round(ker, 5).tolist())
    for tr in traces: print('   direction', tr['direction'], 'steps', tr['steps'], 'min c', np.round(tr['min_c_along'], 5).tolist())
json.dump(out, open(os.path.join(HERE, '..', 'data', 'lead-A4.json'), 'w'), indent=1)
