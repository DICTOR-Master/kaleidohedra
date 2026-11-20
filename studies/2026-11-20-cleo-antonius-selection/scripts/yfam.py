"""Shared numeric model for this study (mpmath).  The (b), (c) family of #103 with free great slopes u, v.

Construction: exactly the line-by-line construction of #103 Theorem 15's census (studies/2026-11-15-dicto-yantra-uniqueness,
scripts/s1_system.py), with numbers in place of symbols: u = w7/b7, v = w3/(1 - b3), t = b1/w1 ((b) by construction), S = b9.
Polynomials G ((c)), H1 (closing marma (1,4,6)), D ((d) squared) and C (t4 right leg, t5 base, t6 right leg concurrent) come
from data/system-uv.json (s0_generic.py, exact over Q).
"""
import json, os, itertools
import mpmath as mp
from fractions import Fraction as Fr

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SYS = json.load(open(os.path.join(ROOT, 'data', 'system-uv.json')))
POL = {k: [(tuple(e), int(c)) for e, c in v] for k, v in SYS.items()}
DOWN = (1, 2, 3, 4, 5)


def coeffs(name, var, vals):
    """Univariate coefficients (highest first) of polynomial `name` in variable index var (0 u, 1 v, 2 t, 3 S),
    the other variables set to vals (dict index -> mpf)."""
    deg = max(e[var] for e, _ in POL[name])
    cs = [mp.mpf(0)] * (deg + 1)
    for e, c in POL[name]:
        term = mp.mpf(c)
        for i in range(4):
            if i != var:
                term *= vals[i] ** e[i]
        cs[e[var]] += term
    return cs[::-1]


def peval(name, u, v, t, S):
    tot = mp.mpf(0); size = mp.mpf(0)
    for e, c in POL[name]:
        term = c * u ** e[0] * v ** e[1] * t ** e[2] * S ** e[3]
        tot += term; size += abs(term)
    return tot, size


def build(u, v, t, S):
    """The yantra (b, w, a dicts 1..9) from (u, v, t, S), as in s1_system.py."""
    P = v**2 / (1 + v**2); R = 1 / (1 + u**2)
    w3 = v / (1 + v**2); w7 = u / (1 + u**2)
    b1 = t**2 / (1 + t**2); w1 = t / (1 + t**2)
    xW = w7 * P / R
    xX = xW * (S - R) / (S - P)
    k9 = xX / (R - P)
    w9 = k9 * (S - P)
    k3 = w3 / (1 - P)
    xZ = k3 * (1 - R)
    c138 = w1 * (R - b1) - xZ * (P - b1)
    Q = (w1 * P * (R - b1) - xZ * b1 * (P - b1)) / c138
    m1 = w1 / (Q - b1)
    b8 = (k3 + k9 * P) / (k3 + k9)
    xF = k9 * (Q - P)
    w6 = xW * (S - Q) / (S - P)
    k7 = w7 / R
    b2 = m1 * Q / (m1 + k7)
    c4 = xF / (b8 - Q); c8 = xZ / (R - b1)
    b4 = (c4 * b8 + c8 * b1) / (c4 + c8)
    b5 = (m1 * Q + k9 * P) / (m1 + k9)
    w5 = w6 * (b5 - b2) / (Q - b2)
    b = {1: b1, 2: b2, 3: P, 4: b4, 5: b5, 6: Q, 7: R, 8: b8, 9: S}
    a = {1: Q, 2: S, 3: mp.mpf(1), 4: b8, 5: R, 6: b2, 7: mp.mpf(0), 8: b1, 9: P}
    w = {1: w1, 2: xW * (S - b2) / (S - P), 3: w3, 4: xF * (b8 - b4) / (b8 - Q), 5: w5, 6: w6, 7: w7,
         8: xZ * (b8 - b1) / (R - b1), 9: w9}
    return dict(b=b, w=w, a=a, u=u, v=v, t=t, S=S)


def admissible(y, tol=None):
    tol = mp.mpf(10) ** (-(mp.mp.dps - 15)) if tol is None else tol
    b, w, a = y['b'], y['w'], y['a']
    if not all(b[i] < b[i + 1] for i in range(1, 9)): return False
    if not all(w[i] > 0 for i in range(1, 10)): return False
    if not all((a[i] > b[i]) if i in DOWN else (a[i] < b[i]) for i in range(1, 10)): return False
    return all(w[i]**2 + b[i]**2 - b[i] <= tol for i in range(1, 10))


def margin(y):
    """Smallest admissibility slack (positive = strictly admissible), and which test."""
    b, w, a = y['b'], y['w'], y['a']
    m = [(b[i + 1] - b[i], f'b{i}<b{i+1}') for i in range(1, 9)] + [(w[i], f'w{i}>0') for i in range(1, 10)]
    m += [((a[i] - b[i]) if i in DOWN else (b[i] - a[i]), f'apex side t{i}') for i in range(1, 10)]
    m += [(-(w[i]**2 + b[i]**2 - b[i]), f't{i} in disc') for i in range(1, 10) if i not in (1, 3, 7, 9)]
    return min(m, key=lambda z: z[0])


def bindu(y):
    """(d): incircle centre depth minus 1/2 (as rhombus.py's extra)."""
    b, w, Q = y['b'], y['w'], y['b'][6]
    m1 = w[1] / (Q - b[1]); sn = m1 / mp.sqrt(1 + m1**2)
    r = (Q - b[5]) * sn / (1 + sn)
    return b[5] + r - mp.mpf(1) / 2, r


def real_roots(cs, lo, hi):
    rts = mp.polyroots(cs, maxsteps=400, extraprec=4 * mp.mp.dps)
    eps = mp.mpf(10) ** (-(mp.mp.dps // 2))
    return sorted(mp.re(r) for r in rts if abs(mp.im(r)) < eps and lo < mp.re(r) < hi)


def members(u, v):
    """Every admissible (b), (c) yantra with great slopes u, v: S from G (quadratic), t from H1 (degree 10)."""
    out = []
    R = 1 / (1 + u**2)
    for S in real_roots(coeffs('G', 3, {0: u, 1: v, 2: 0}), R, 1):
        for t in real_roots(coeffs('H1', 2, {0: u, 1: v, 3: S}), 0, 10):
            try:
                y = build(u, v, t, S)
            except ZeroDivisionError:
                continue
            if admissible(y):
                out.append(y)
    return out


# ------------------------------------------------------------------ lines and their concurrencies
def lines(y):
    b, w, a = y['b'], y['w'], y['a']
    L = {}
    for i in range(1, 10):
        L[f'base{i}'] = ((-w[i], b[i]), (w[i], b[i]))
        L[f'R{i}'] = ((w[i], b[i]), (0, a[i]))
        L[f'L{i}'] = ((-w[i], b[i]), (0, a[i]))
    return L


def hom(pp):
    (x1, y1), (x2, y2) = pp
    A, B, C = y1 - y2, x2 - x1, x1 * y2 - x2 * y1
    n = mp.sqrt(A * A + B * B)
    return (A / n, B / n, C / n)


def dets(y):
    """Normalised 3x3 determinants of every triple of the 27 lines, and the direction cross product of every pair
    (the triple with the line at infinity).  Sign vector of these fixes the combinatorics of the arrangement."""
    L = {k: hom(v) for k, v in lines(y).items()}
    names = sorted(L)
    out = {}
    for p, q, r in itertools.combinations(names, 3):
        A, B, C = L[p], L[q], L[r]
        out[(p, q, r)] = (A[0] * (B[1] * C[2] - B[2] * C[1]) - A[1] * (B[0] * C[2] - B[2] * C[0])
                          + A[2] * (B[0] * C[1] - B[1] * C[0]))
    for p, q in itertools.combinations(names, 2):
        out[(p, q, 'inf')] = L[p][0] * L[q][1] - L[p][1] * L[q][0]
    return out


# ------------------------------------------------------------------ counts
def counts_traditional(y, dig=40):
    """counts.py of #103 (marmas = points where exactly three sides meet, sandhis = exactly two cross, corners excluded),
    on Fractions of the values, meeting tolerance 10^-(dig-10)."""
    f = lambda z: Fr(mp.nstr(z, dig, min_fixed=-mp.inf, max_fixed=mp.inf)) if z != 0 else Fr(0)
    b = {i: f(y['b'][i]) for i in range(1, 10)}; w = {i: f(y['w'][i]) for i in range(1, 10)}; a = {i: f(y['a'][i]) for i in range(1, 10)}
    segs = []
    for i in b:
        Lp, Rp, Ap = (-w[i], b[i]), (w[i], b[i]), (Fr(0), a[i]); segs += [((Lp, Rp), i), ((Lp, Ap), i), ((Rp, Ap), i)]
    TOL = Fr(1, 10 ** (dig - 10)); pts = []
    def same(p, q): return abs(p[0] - q[0]) < TOL and abs(p[1] - q[1]) < TOL
    for (s, i), (t, j) in itertools.combinations(segs, 2):
        (x1, y1), (x2, y2) = s; (x3, y3), (x4, y4) = t
        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if abs(den) < TOL: continue
        px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / den
        py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / den
        on = lambda p, q: min(p[0], q[0]) - TOL <= px <= max(p[0], q[0]) + TOL and min(p[1], q[1]) - TOL <= py <= max(p[1], q[1]) + TOL
        if not (on(*s) and on(*t)): continue
        for Pp in pts:
            if same(Pp[0], (px, py)): Pp[1].update({id(s), id(t)}); break
        else: pts.append([(px, py), {id(s), id(t)}])
    corners = [((-w[i], b[i]), i) for i in b] + [((w[i], b[i]), i) for i in b] + [((Fr(0), a[i]), i) for i in b]
    def is_corner(p): return any(same(p, c) for c, _ in corners)
    marma = sum(1 for p, s in pts if len(s) == 3 and not is_corner(p))
    sandhi = sum(1 for p, s in pts if len(s) == 2 and not is_corner(p))
    return marma, sandhi


def regions(y, dig=40):
    """Odd regions and their split (yarr.py of study 2026-11-17-yantra-sequence, decimal mode)."""
    from yarr import Arr
    f = lambda z: Fr(mp.nstr(z, dig, min_fixed=-mp.inf, max_fixed=mp.inf)) if z != 0 else Fr(0)
    T = [(f(y['b'][i]), f(y['w'][i]), f(y['a'][i])) for i in range(1, 10)]
    r = Arr(T, eps=Fr(1, 10 ** (dig - 10)), eps_cross=Fr(1, 10 ** (dig - 10))).analyse()
    return r
