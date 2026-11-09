"""Generic driver for one polar line: walls (with 4x4 determinants), wall kinds, foot walls (walls of the
foot-point hull P(S), i.e. of the antipol S^v), turn tests, and the exact t_min envelope with its maximum.
Used by s0b (cube-octahedron, known case), s1 (CO-RD) and s2 (ID-RT). Study 2026-11-09-dual-sweeps."""
import numpy as np
import sympy as sp
import sweeplib as L
from sweeplib import F, Q, ZERO, ONE, dot


def generic_start(sw, lo, hi, eps=Q(1, 1000)):
    """a generic exact point just above lo with no wall in (lo, s)."""
    e = F(eps) * (hi - lo)
    while True:
        s = lo + e
        try:
            pw = sw.prev_wall(s)
            sw.next_wall(s)
        except RuntimeError:
            e = e * Q(1, 3); continue
        if pw is None or pw <= lo:
            return s
        e = e * Q(1, 3)


def run_line(sw, s0, log, name):
    out = {}
    walls = sw.walk(s0)
    log(f'[{name}] walls of S(mu): ' + ', '.join(f'{w["mu"]} (~{float(w["mu"]):.10f})' for w in walls))
    wl = []
    for w in walls:
        quads = sorted({tuple(sorted(set(h[1]) | {h[2]})) for h in w['hits']})
        dets = []
        for qd in quads:
            d0, d1, lin, root = sw.wall_det(qd)
            dets.append((qd, d0, d1, lin, root))
        c = L.classify(sw, w['below'], w['above'])
        allin = all(d[3] for d in dets) and all(d[4] == w['mu'] for d in dets)
        qd, d0, d1, lin, root = dets[0]
        log(f'  wall {w["mu"]}: {len(quads)} concurrent quadruples (one orbit shown) planes {[sw.P[k][3] for k in qd]}: '
            f'det = {d0} + ({d1}) mu, all linear and rooted at the wall: {allin}')
        log(f'    kind: {c["kinds"]}; faces born {c["born"]}, died {c["died"]}; bonds lost {c["bonds_lost"]}, gained {c["bonds_gained"]}')
        log(f'    census {c["census_below"]} -> {c["census_above"]}; corners {c["V"]}; Euler {c["euler"]}')
        wl.append(dict(mu=w['mu'], dets_ok=allin, kind=c, below=w['below'], above=w['above']))
    out['walls'] = wl
    # foot walls per open interval between consecutive walls
    feet = []
    for i in range(len(wl) - 1):
        a, b = wl[i]['mu'], wl[i + 1]['mu']
        st = sw.structure(wl[i]['above'])
        fs = L.foot_sweep(sw, st['facets'])
        lo, hi = ONE / b, ONE / a
        s = generic_start(fs, lo, hi)
        fw = [w for w in fs.walk(s, top=hi) if w['mu'] < hi]
        for w in fw:
            mu = ONE / w['mu']
            c = L.classify(fs, w['below'], w['above'])
            feet.append(dict(mu=mu, interval=(a, b), kind=c))
            log(f'  foot wall mu = {mu} (~{float(mu):.10f}) in ({a}, {b}): S^v {c["kinds"]}; S^v census {c["census_below"]} -> {c["census_above"]}')
    out['feet'] = feet
    return out


def symmetric_under(vals, c):
    s = set(vals)
    return all((c / v) in s for v in vals)


def pair_functions(sw, s_mu, nu_s, fs):
    """t_min pieces on an interval with fixed S and S^v combinatorics: alpha + beta mu + gamma/mu."""
    X = sw.affine_vertices(s_mu)
    Y = fs.affine_vertices(nu_s)
    fun = []
    for p, q, _, _ in X:
        for pp, qq, _, _ in Y:
            fun.append((dot(p, pp) + dot(q, qq), dot(q, pp), dot(p, qq)))
    return fun


def tmin_envelope(sw, events, log, name, ngrid=400):
    """events: sorted exact mu values (walls of S and foot walls) spanning the middle of the line.
    On each sub-interval: all pair functions, float envelope, exact argmax (sympy). Returns list of maxima."""
    m = sp.symbols('m', positive=True)
    res = []
    for a, b in zip(events[:-1], events[1:]):
        mid = (a + b) * Q(1, 2)
        st = sw.structure(mid)
        fs = L.foot_sweep(sw, st['facets'])
        fun = pair_functions(sw, mid, ONE / mid, fs)
        # exact check of the envelope against direct t_min at the midpoint
        direct, _, _ = sw.tmin(mid, st)
        env_mid = max((al + be * mid + ga / mid for al, be, ga in fun), key=float)
        assert env_mid == direct, 'envelope != t_min'
        A = np.array([[float(x) for x in f] for f in fun])
        g = np.linspace(float(a), float(b), ngrid)[1:-1]
        vals = A[:, 0][:, None] + A[:, 1][:, None] * g[None, :] + A[:, 2][:, None] / g[None, :]
        env = vals.max(axis=0)
        i = int(np.argmax(env))
        # active pieces near the max (distinct functions)
        tops = sorted({tuple(fun[j]) for j in np.argsort(-vals[:, i])[:400] if vals[j, i] > env[i] - 1e-9}, key=str)
        def S(f):
            return f[0].sym() + f[1].sym() * m + f[2].sym() / m
        cands = []
        for f in tops:
            e = sp.simplify(S(f))
            for r in sp.solve(sp.diff(e, m), m):
                if r.is_real and float(a) < float(r) < float(b): cands.append(r)
        for f1 in tops:
            for f2 in tops:
                if str(f1) < str(f2):
                    for r in sp.solve(sp.together(S(f1) - S(f2)) * m, m):
                        if r.is_real and float(a) < float(r) < float(b): cands.append(r)
        cands += [a.sym(), b.sym()]
        best = None
        for r in cands:
            rf = float(r)
            envr = max(float(x[0]) + float(x[1]) * rf + float(x[2]) / rf for x in fun)
            if best is None or envr > best[1] + 1e-13:
                best = (r, envr)
        # exact value at best: max over the active pieces evaluated exactly
        r = best[0]
        val = max((sp.simplify(S(f).subs(m, r)) for f in tops), key=lambda z: float(z))
        val = sp.radsimp(sp.simplify(val))
        res.append(dict(interval=(a, b), argmax=sp.simplify(r), value=val, fvalue=float(val), grid_max=float(env.max()),
                        interior=not (r == a.sym() or r == b.sym()), npieces=len(tops)))
        log(f'  [{name}] t_min on ({a}, {b}): max {sp.simplify(val)} (~{float(val):.10f}) at mu = {sp.simplify(r)} (~{float(r):.10f})'
            f'{" interior" if res[-1]["interior"] else " (end of piece)"}; grid max {env.max():.10f}')
    return res
