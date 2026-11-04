#!/usr/bin/env python3
"""#91's 4D sweep S(mu) = [-1,1]^4 ∩ {|x|_1 <= mu}, 1 < mu < 4 (16-cell .. 24-cell at mu=2 .. tesseract): isoperimetric quotient V^3/A^4 (4D, scale-free) and Mahler V·V°.
Prediction from 3D (IQ max exactly at the core-turn fixed point sqrt 3): max at the 24-cell, fixed point of mu <-> 4/mu. Also Dehn-type note only (no 4D tiling test here)."""
import itertools, json, numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
def planes(mu):
    P = [(e, 1.0) for i in range(4) for s in (1, -1) for e in [np.eye(4)[i]*s]]
    P += [(np.array(sg, float), mu) for sg in itertools.product((1, -1), repeat=4)]
    return P
def meas(mu):
    pl = planes(mu); H = np.array([[*n, -c] for n, c in pl]); V = HalfspaceIntersection(H, np.zeros(4)).intersections
    h = ConvexHull(V); pol = ConvexHull(np.array([n/c for n, c in pl])); return h.volume, h.area, pol.volume
mus = np.linspace(1.002, 3.998, 1499); rows = [(m, *meas(m)) for m in mus]
IQ = [(m, V**3/A**4) for m, V, A, Vp in rows]; MA = [(m, V*Vp) for m, V, A, Vp in rows]
def refine(f, a, b):
    from scipy.optimize import minimize_scalar
    r = minimize_scalar(lambda x: -f(x), bounds=(a, b), method='bounded', options={'xatol': 1e-10}); return r.x, -r.fun
iq = max(IQ, key=lambda r: r[1])[0]; ma = max(MA, key=lambda r: r[1])[0]
iqx = refine(lambda m: (lambda V, A, Vp: V**3/A**4)(*meas(m)), iq - .01, iq + .01)
max_ = refine(lambda m: (lambda V, A, Vp: V*Vp)(*meas(m)), ma - .01, ma + .01)
out = {'iq_max': iqx, 'mahler_max': max_, 'mahler_at': {str(m): meas(m)[0]*meas(m)[2] for m in (1.0001, 2.0, 3.9999, (1+5**.5)**2/4, 2 + 1/((1+5**.5)/2)**2)},
       'iq_at': {str(m): (lambda V, A, Vp: V**3/A**4)(*meas(m)) for m in (1.0001, 2.0, 3.9999)}}
print(json.dumps(out, indent=1))
