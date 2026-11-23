# Certify the dice whose fair point lies (to 60 digits) on a hyperplane h(x) = 0 of depth space where four or more
# face planes meet in one corner only for depths on that hyperplane ("accidental" corners). Across h = 0 the
# combinatorial type changes. Method: the two types T+ (h > 0) and T- (h < 0) are taken from the 60-digit solution
# moved by 1e-6 to each side; each type is certified on its closed half-box (every corner strictly inside every other
# half-space, except slacks that are multiples of h, which vanish only on h = 0); the fairness map F is continuous and
# piecewise smooth, so F(x) - F(y) lies in hull(J+(X), J-(X)) (x - y) on X, and Krawczyk's test with that hull proves
# one and only one zero in X. Then: a 1-dimensional (or lower) certification ON the hyperplane (the restricted
# system) for the zero there, when the solution is claimed to lie exactly on it (see README).
# usage: accidental.py OUT.json
import json, sys, os, itertools, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import certify as C
from flint import arb, arb_mat, ctx
ctx.prec = C.PREC

def side_die(rec, hcoef, sgn, delta=1e-6):
    """the die with the same faces at depths moved off the hyperplane by delta to side sgn"""
    x = np.array([float(v) for v in rec['depths'][1:]]); c = np.array(hcoef[1:], float)
    xs = x + sgn * delta * c / (c @ c)
    r2 = dict(rec); r2['depths'] = ['1.0'] + ['%.20f' % v for v in xs]
    s = C.Die(r2); s.setup()
    assert not s.accidental and s.graph_ok, 'side type not clean'
    s.allow_flat = True
    s.xt = [arb(v).mid() for v in rec['depths'][1:]]            # back to the solution's midpoint for the box
    return s

def slack_ok_halfbox(s, h, sgn, r):
    """every corner of s's type strictly inside every other half-space on X ∩ {sgn*h >= 0}, X = x~ ± r;
    slacks proportional to h (vanishing exactly on h = 0) are accepted when they have the sign of sgn*h"""
    bad = 0; prop = 0
    for vi, I in enumerate(s.full):
        A = s.A[vi]
        for f in range(s.N):
            if f in I: continue
            c = [C.dot(s.n[f], A[o]) for o in range(s.m)]; c[s.orb[f]] -= 1
            c = [-x for x in c]                       # slack = d_f - n_f.v = sum_o c_o d_o
            sl0 = c[0] + sum((c[k] * s.xt[k - 1] for k in range(1, s.m)), arb(0))
            L = sum((abs(c[k]) for k in range(1, s.m)), arb(0)) * r
            if (sl0 - L) > 0: continue
            # proportional to h?  c = lam * h with lam of sign sgn
            k0 = max(range(s.m), key=lambda k: abs(float(h[k].mid())))
            lam = c[k0] / h[k0]
            if all((c[k] - lam * h[k]).contains(0) and abs(float((c[k] - lam * h[k]).rad())) < 1e-60 for k in range(s.m)) and (lam * sgn) > 0:
                prop += 1; continue
            bad += 1
    return bad, prop

def run(rec):
    s0 = C.Die(rec); s0.setup()
    acc = s0.accidental
    # all accidental forms must be one hyperplane (up to scale)
    H = []
    for e in acc:
        f = e['plane']; t = e['triple']; A = s0.A[e['corner']]
        c = [C.dot(s0.n[f], A[o]) for o in range(s0.m)]; c[s0.orb[f]] -= 1; H.append(c)
    h = H[0]; k0 = max(range(s0.m), key=lambda k: abs(float(h[k].mid())))
    one = all(all((c[k] - (c[k0] / h[k0]) * h[k]).contains(0) for k in range(s0.m)) for c in H)
    hval = h[0] + sum((h[k] * s0.xt[k - 1] for k in range(1, s0.m)), arb(0))
    out = dict(label=rec['label'], sid=rec['sid'], study=rec['study'], n_accidental=len(acc), one_hyperplane=bool(one),
               h=[x.str(30, radius=False) for x in h], h_at_midpoint=hval.str(5))
    sides = {}
    for sgn in (1, -1):
        s = side_die(rec, [float(x.mid()) for x in h], sgn); sides[sgn] = s
    n = s0.m - 1
    def attempt(r):
        ra = arb(r)
        ok_types = True; Js = []
        for sgn, s in sides.items():
            bad, prop = slack_ok_halfbox(s, h, sgn, r)
            if bad: ok_types = False; break
            X = [C.D(arb(v, ra), [arb(1) if j == i else arb(0) for j in range(n)]) for i, v in enumerate(s.xt)]
            Fx, sok = s.F(X)
            if not sok: ok_types = False; break
            Js.append([[Fx[i].g[j] for j in range(n)] for i in range(n)])
        if not ok_types: return None
        J = arb_mat([[Js[0][i][j].union(Js[1][i][j]) for j in range(n)] for i in range(n)])
        # F at the midpoint, with the type of the side the midpoint is on (both agree on h = 0 by continuity)
        sg = 1 if hval > 0 else (-1 if hval < 0 else 1)
        s = sides[sg]
        F0, _ = s.F([C.D(v, [arb(0)] * n) for v in s.xt])
        f0 = arb_mat([[F0[i].v] for i in range(n)])
        Jm = arb_mat([[arb(J[i, j].mid()) for j in range(n)] for i in range(n)])
        Cm = Jm.inv(); Cq = arb_mat([[arb(Cm[i, j].mid()) for j in range(n)] for i in range(n)])
        Id = arb_mat([[arb(1) if i == j else arb(0) for j in range(n)] for i in range(n)])
        K = -(Cq * f0) + (Id - Cq * J) * arb_mat([[arb(0, ra)] for _ in range(n)])
        if all(K[i, 0].abs_upper() < ra for i in range(n)):
            return dict(ok=True, r=r, dev=max(float(K[i, 0].abs_upper()) for i in range(n)), fres=max(float(f0[i, 0].abs_upper()) for i in range(n)),
                       enclosure=[(s.xt[i] + K[i, 0]).str(30, radius=True) for i in range(n)],
                       h_on_enclosure=(h[0] + sum((h[k] * (s.xt[k - 1] + K[k - 1, 0]) for k in range(1, s0.m)), arb(0))).str(5))
        return None
    res = None
    for e in range(4, 25):
        res = attempt(10.0 ** (-e / 2))
        if res: break
    out['split_krawczyk'] = res or dict(ok=False)
    out['tight'] = attempt(1e-40) or dict(ok=False)
    return out

if __name__ == '__main__':
    recs = C.load_all(); outs = []
    for st, sid in [('2026-11-19', 504), ('2026-11-20', 95), ('2026-11-20', 124)]:
        rec = [x for x in recs if x['study'].startswith(st) and x['sid'] == sid][0]
        o = run(rec); print(json.dumps(o)); outs.append(o)
    json.dump(outs, open(sys.argv[1], 'w'), indent=1)
    print('FINAL ok' if all(o['split_krawczyk'].get('ok') and o['tight'].get('ok') for o in outs) else 'NOT all certified')
