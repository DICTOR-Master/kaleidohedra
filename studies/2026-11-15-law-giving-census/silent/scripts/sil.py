"""Shared loader for the silent-coincidence study: invariant harmonics h_{k,i}(u) from data/hinv-G.json, evaluation of the
orbit-space coordinates u(c) of a seed c (exact K, arb balls, floats), sympy forms, and an interval Krawczyk test."""
import os, sys, json, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'scripts'))
import numpy as np
from flint import fmpq, arb, ctx
import exact as X
from exact import K

def kq(p): return K(fmpq(p[0]), fmpq(p[1]))

def ipow(x, n):
    """integer power by repeated squaring (arb ** int gives nan for an inexact negative base)"""
    r = None; b = x
    while n:
        if n & 1: r = b if r is None else r*b
        n >>= 1
        if n: b = b*b
    return r if r is not None else (x*0 + 1)

class H:
    def __init__(s, name):
        d = json.load(open(os.path.join(HERE, '..', 'data', f'hinv-{name}.json')))
        s.d = d; s.name = name; s.D = d['D']; X.set_field(s.D); s.r = d['r']; s.degs = d['degs']; s.n = len(s.degs)
        s.order = d['order']; s.aut = d['aut']
        s.harm = {int(k): [{tuple(e): kq(c) for e, c in h} for h in v] for k, v in d['harm'].items()}
        s.dims = {int(k): v for k, v in d['dims'].items()}
        s.G = [[kq(x) for x in row] for row in d['G']]; s.Gw = [[kq(x) for x in row] for row in d['Gw']]
        s.W = [[kq(x) for x in w] for w in d['W']]; s.R = [[kq(x) for x in a] for a in d['R']]
        s.hat = {int(ch): [[kq(x) for x in h] for h in v] for ch, v in d['omega_hat'].items()}
        s.choice = d['choice']
        s.Gf = np.array([[float(x) for x in row] for row in s.G]); s.Gwf = np.array([[float(x) for x in row] for row in s.Gw])
        s.hatf = {ch: np.array([[float(x) for x in h] for h in v]) for ch, v in s.hat.items()}
        s.Wf = np.array([[float(x) for x in w] for w in s.W]); s.Rf = np.array([[float(x) for x in a] for a in s.R])
        s.harmf = {k: [(np.array([e for e in h]), np.array([float(c) for c in h.values()])) for h in v] for k, v in s.harm.items()}
        s.sqD = arb(s.D).sqrt()
        s.hatA = {ch: [[arb(x.a) + arb(x.b)*s.sqD for x in h] for h in v] for ch, v in s.hat.items()}
        s.GwA = [[arb(x.a) + arb(x.b)*s.sqD for x in row] for row in s.Gw]
        s.harmA = {k: [[(e, arb(c.a) + arb(c.b)*s.sqD) for e, c in h.items()] for h in v] for k, v in s.harm.items()}
    def degrees(s, kmax): return [k for k in sorted(s.dims) if s.dims[k] and k <= kmax]
    # ---- exact ----
    def u_exact(s, c):
        out = [sum((c[i]*c[j]*s.Gw[i][j] for i in range(s.r) for j in range(s.r)), K(0))]
        for i, d in enumerate(s.degs[1:]):
            tot = K(0)
            for h in s.hat[s.choice[i]]:
                L = sum((h[j]*c[j] for j in range(s.r)), K(0)); p = K(1)
                for _ in range(d): p = p*L
                tot = tot + p
            out.append(tot)
        return out
    def h_exact(s, k, c, u=None):
        u = u or s.u_exact(c); out = []
        for h in s.harm[k]:
            tot = K(0)
            for e, co in h.items():
                t = co
                for ui, ei in zip(u, e):
                    for _ in range(ei): t = t*ui
                tot = tot + t
            out.append(tot)
        return out
    # ---- float (numpy), homogeneous: h(u(c)) of degree k ----
    def u_float(s, c):
        c = np.asarray(c, float); out = [c @ s.Gwf @ c]; J = [2*s.Gwf @ c]
        for i, d in enumerate(s.degs[1:]):
            hf = s.hatf[s.choice[i]]; L = hf @ c
            out.append(np.sum(L**d)); J.append(d*(L**(d - 1)) @ hf)
        return np.array(out), np.array(J)
    def h_float(s, k, c, jac=False):
        u, Ju = s.u_float(c); vals = []; jacs = []
        for E_, C_ in s.harmf[k]:
            mon = np.prod(u[None, :]**E_, axis=1); vals.append(np.dot(C_, mon))
            if jac:
                g = np.zeros(s.n)
                for i in range(s.n):
                    Ei = E_.copy(); m = Ei[:, i] > 0
                    if not m.any(): continue
                    Ei2 = Ei[m].copy(); Ei2[:, i] -= 1
                    g[i] = np.dot(C_[m]*E_[m, i], np.prod(u[None, :]**Ei2, axis=1))
                jacs.append(g @ Ju)
        return (np.array(vals), np.array(jacs)) if jac else np.array(vals)
    # ---- arb (intervals): values and Jacobian of h(u(c)) at a box c (list of arb) ----
    def u_arb(s, c):
        r = s.r
        out = [sum((c[i]*c[j]*s.GwA[i][j] for i in range(r) for j in range(r)), arb(0))]
        J = [[2*sum((s.GwA[i][j]*c[i] for i in range(r)), arb(0)) for j in range(r)]]
        for i, d in enumerate(s.degs[1:]):
            tot = arb(0); g = [arb(0)]*r
            for h in s.hatA[s.choice[i]]:
                L = sum((h[j]*c[j] for j in range(r)), arb(0)); Ld1 = ipow(L, d - 1)
                tot += Ld1*L
                for j in range(r): g[j] += d*Ld1*h[j]
            out.append(tot); J.append(g)
        return out, J
    def h_arb(s, k, c, jac=False, ub=None):
        u, Ju = ub if ub is not None else s.u_arb(c); vals = []; jacs = []
        for h in s.harmA[k]:
            v = arb(0); g = [arb(0)]*s.n
            for e, co in h:
                t = co
                for ui, ei in zip(u, e):
                    if ei: t = t*ipow(ui, ei)
                v += t
                if jac:
                    for i in range(s.n):
                        if e[i] == 0: continue
                        t2 = co*e[i]
                        for j, (uj, ej) in enumerate(zip(u, e)):
                            ee = ej - (1 if j == i else 0)
                            if ee: t2 = t2*ipow(uj, ee)
                        g[i] += t2
            vals.append(v)
            if jac: jacs.append([sum((g[i]*Ju[i][j] for i in range(s.n)), arb(0)) for j in range(s.r)])
        return (vals, jacs) if jac else vals

def krawczyk(F, J, x0, rad, iters=6):
    """F(list arb) -> list arb (n), J(list arb) -> n x n arb.  x0 float list.  Returns (status, box) with status 'unique' if the
    Krawczyk image lies inside the box (a unique zero exists in it), else 'fail'."""
    n = len(x0)
    for it in range(iters):
        m = [arb(x0[i].mid()) if isinstance(x0[i], arb) else arb(float(x0[i])) for i in range(n)]
        X_ = [arb(m[i], rad) for i in range(n)]
        Fm = F(m); JX = J(X_)
        Jm = np.array([[float(x.mid()) for x in row] for row in J(m)])
        try: Y = np.linalg.inv(Jm)
        except np.linalg.LinAlgError: return 'fail', None
        YA = [[arb(float(Y[i][j])) for j in range(n)] for i in range(n)]
        Kx = []
        for i in range(n):
            v = m[i] - sum((YA[i][j]*Fm[j] for j in range(n)), arb(0))
            for j in range(n):
                cij = (arb(1) if i == j else arb(0)) - sum((YA[i][l]*JX[l][j] for l in range(n)), arb(0))
                v += cij*(X_[j] - m[j])
            Kx.append(v)
        if all(X_[i].contains_interior(Kx[i]) for i in range(n)): return 'unique', X_
        rad = rad/4 if it % 2 else rad*4
    return 'fail', None
