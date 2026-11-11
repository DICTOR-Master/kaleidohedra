# s2_census3d.py -- the Star Cores census of the nine regular solids (5 Platonic, 4 Kepler-Poinsot), exactly, with the census
# tools' own definitions (studies 2026-10-30-star-cores-exact study1/2/5 and 2026-11-02-halo-census). Study 2026-11-09-regular-stars-census.
#  T-chain: DICTO's growth rule T(S) = {x : v.x <= v.v for every corner v} (#38; exactlib.ustep), run until a step is similar to an
#           earlier one (study5.run); period and gain (radius^2 per period). Known-case check: cube 3, dodecahedron 15 - 6 sqrt5 (#80).
#  Star Core: the core of the turn (#79/#81; study2.core_turn): the faces grouped into families (sides, distance), the tips at t x the
#           feet of the face perpendiculars, the core = the common part of the family hulls; followed turn after turn until similar.
#           For a star polygon face the foot is its centre.
#  Star Halo: the hull of the tips (shape independent of t); Polar Halo: the polar reciprocal (for a star solid: its reciprocal
#           star, whose hull is reported).
#  Stars: the solid with the pyramid over each face to the tip t x foot, t = 2 (DICTO's doubled star) and t = phi (golden star).
#  Star line (t >= 1): the hulls K_t = conv(corners, tips). Walls (exact): t = rho_k^2 / h^2 (the join at k = 1, T(P) at k = 0, g),
#           the Catalan kis t_C (all edges tangent to the midsphere), and the incidences where a spike side plane passes through a
#           corner or another tip (stellations, joins).
# Usage: python3 -u s2_census3d.py <exactlib dir> <flags.json> <out json>
import sys, os, json, time, itertools
LIB, FL, OUT = sys.argv[1:4]; sys.path.insert(0, LIB)
import exactlib as EL
from exactlib import QF, fmt, hull as hull_ccw, ustep, volume, face_planes, halfspace_solid
from fractions import Fraction as Fr
import numpy as np, sympy as sp
from regstar import *
T0 = time.time()

def toQF(x): return QF(x.a, x.b, 5)
def vQF(v): return tuple(toQF(x) for x in v)
def kinds(F):
    k = {}
    for f in F: k[len(f)] = k.get(len(f), 0) + 1
    return {str(a): b for a, b in sorted(k.items())}
def rad2(V): return max((EL.dot(v, v) for v in V), key=lambda x: x.f())
def similar(A, B, g2):
    if len(A) != len(B): return False
    for v in B:
        if not any(all(x.sign() == 0 for x in EL.cross(u, v)) and EL.dot(u, v).sign() > 0 and (EL.dot(v, v) - g2 * EL.dot(u, u)).sign() == 0 for u in A):
            return False
    return True
def run_T(V0):
    V, F = hull_ccw(V0); hist = [(V, F, rad2(V))]; S = V; out = dict(steps=[])
    for k in range(1, 7):
        S, SF = ustep(S); r = rad2(S); out['steps'].append(dict(step=k, corners=len(S), faces=kinds(SF)))
        for j, (A, AF, ra) in enumerate(hist):
            if kinds(AF) == kinds(SF) and similar(A, S, r / ra):
                out.update(enters_cycle_at_step=j, period=k - j, gain_radius2=fmt(r / ra), gain_radius=str(sp.sqrtdenest(sp.sqrt(sp.sympify(fmt(r / ra))))), gain_f=(r / ra).f() ** .5); return out
        hist.append((S, SF, r))
    return out
def core_turn(V, F):   # study2.core_turn (t = 1)
    fam = {}
    for f, (n, c) in zip(F, face_planes(V, F)):
        foot = EL.mul(c / EL.dot(n, n), n); fam.setdefault((len(f), fmt(EL.dot(foot, foot))), []).append(foot)
    planes = []
    for key_, T in fam.items():
        if len(T) < 4: continue
        A, AF = hull_ccw(T); planes += face_planes(A, AF)
    C, CF = halfspace_solid(planes)
    return C, CF, len(fam)
def run_core(V, F, feet=None):
    """core cycle; for a star solid the first core is the hull of its face centres (one family)"""
    hist = []; out = dict(turns=[])
    if feet is not None:
        A, AF = hull_ccw(feet); C, CF = halfspace_solid(face_planes(A, AF)); fams = 1
    else:
        hist.append((V, F, rad2(V), 0)); C, CF, fams = core_turn(V, F)
    for k in range(1, 6):
        r = rad2(C); out['turns'].append(dict(turn=k, families=fams, corners=len(C), faces=kinds(CF)))
        for (A, AF, ra, j) in hist:
            if kinds(AF) == kinds(CF) and similar(A, C, r / ra):
                out.update(cycle_from_turn=j, period=k - j, scale_radius2_t1=fmt(r / ra),
                           scale_radius_t1=str(sp.sqrtdenest(sp.sqrt(sp.sympify(fmt(r / ra))))), scale_f=(r / ra).f() ** .5); return out, hist
        hist.append((C, CF, r, k)); C, CF, fams = core_turn(C, CF)
    return out, hist

# ---------- the nine solids from their flags (exact orbits under the flag mirrors) ----------
rows = [r for r in json.load(open(FL)) if r['d'] == 3]
def orbit_exact(gens, x):
    seen = {key(x): x}; fr = [x]
    while fr:
        nx = []
        for y in fr:
            for m in gens:
                z = refl(m, y)
                if key(z) not in seen: seen[key(z)] = z; nx.append(z)
        fr = nx
    return list(seen.values())
def faces_of(ms, q):
    """face polygons: the orbit of q_0 under <rho_0, rho_1>, in the cyclic order of the rotation rho_1 rho_0; all faces by the
    full group orbit of that polygon"""
    m0, m1 = ms[0], ms[1]; poly = [q[0]]
    while True:
        nxt = refl(m1, refl(m0, poly[-1]))
        if key(nxt) == key(poly[0]): break
        poly.append(nxt)
    G = [ms[0], ms[1], ms[2]]
    seen = {}; fr = [tuple(poly)]
    while fr:
        nx = []
        for P in fr:
            for m in G:
                Q = tuple(refl(m, p) for p in P); k = frozenset(key(p) for p in Q)
                if k not in seen: seen[k] = Q; nx.append(Q)
        fr = nx
    return list(seen.values()), poly

phi = (1 + sp.sqrt(5)) / 2
def nice(x):
    """a short exact form of the algebraic number x: nsimplify over sqrt5, accepted only if the minimal polynomials agree"""
    X = sp.Symbol('X')
    try:
        y = sp.nsimplify(sp.N(x, 60), [sp.sqrt(5)], tolerance=1e-45)
        if sp.minimal_polynomial(y, X) == sp.minimal_polynomial(x, X): return y
    except Exception: pass
    return sp.radsimp(x)
def S(x): return sp.Rational(x.a.numerator, x.a.denominator) + sp.Rational(x.b.numerator, x.b.denominator) * sp.sqrt(5)
res = []; allok = True
for row in rows:
    ms = [vp(m) for m in row['mirrors']]; q = [vp(x) for x in row['q']]; r2 = [q5p(x) for x in row['r2']]
    V = orbit_exact(ms, q[0]); feetQ = orbit_exact(ms, q[2]); Fpolys, poly = faces_of(ms, q)
    R2, rho1, h2 = r2; g = R2 / h2
    rec = dict(symbol=row['symbol'], name=row['name'], density=row['density'], V=len(V), E=row['counts'][1], F=len(Fpolys),
               face_sides=len(poly), R2_over_h2=q5s(g), rho1_2_over_h2=q5s(rho1 / h2))
    convex = row['density'] == 1
    # T-chain (corners only)
    rec['T_chain'] = run_T([vQF(v) for v in V])
    # cores
    if convex:
        Vh, Fh = hull_ccw([vQF(v) for v in V]); core, hist = run_core(Vh, Fh)
    else:
        Vh, Fh = hull_ccw([vQF(v) for v in V]); core, hist = run_core(Vh, Fh, feet=[vQF(f) for f in feetQ])
    rec['core'] = core
    # the first core = hull of the feet (t = 1): which solid, and its radius vs the solid's
    A, AF = hull_ccw([vQF(f) for f in feetQ]); rec['star_halo'] = dict(corners=len(A), faces=kinds(AF), note='hull of t x the face centres; shape independent of t')
    # polar halo: reciprocal in the sphere of radius^2 = R2: corners at the poles of the face planes (R2/h2 x the feet)
    P = [scal(R2 / h2, f) for f in feetQ]; A, AF = hull_ccw([vQF(p) for p in P])
    rec['polar_halo'] = dict(corners=len(A), faces=kinds(AF), note='the reciprocal; for a star solid, the hull of its reciprocal star')
    # stars at t = 2, phi: hull, convex or not (convex iff t <= join wall rho1^2/h2 for the convex solids)
    stars = {}
    for tn, t in (('2', Q5(2)), ('phi', PHI)):
        tips = [scal(t, f) for f in feetQ]
        Hs, HF = hull_ccw([vQF(v) for v in V + tips])
        ncorners = len(Hs); sol_corners_on_hull = sum(1 for v in V if any(EL.dot(EL.sub(vQF(v), w), EL.sub(vQF(v), w)).sign() == 0 for w in Hs))
        if convex:
            wall = rho1 / h2; state = 'convex (kis)' if t < wall else ('at the join' if t == wall else 'non-convex')
            vol_ratio = 't (pyramids add (t-1) x the solid)'
        else:
            state = 'star (pyramids on star faces)'; vol_ratio = None
        region = 'inside the T range (1, g)' if t < g else ('at T(P)' if t == g else 'beyond T(P): hull = tips only')
        stars[tn] = dict(t=q5s(t), hull_corners=ncorners, hull_faces=kinds(HF), solid_corners_on_hull=sol_corners_on_hull, state=state,
                         star_line_region=region, turned_partner=q5s(g / t), turned_partner_f=(g / t).f())
    rec['stars'] = stars
    # star line events, exact (sympy): walls, Catalan kis, incidences of a spike side plane
    ts = sp.Symbol('t', positive=True)
    Rs, r1s, hs = S(R2), S(rho1), S(h2)
    ev = [dict(t='1', kind='wall', what='the solid itself (t = 1)'), dict(t=str(sp.nsimplify(r1s / hs)), kind='wall (incidence)',
           what='join: neighbouring spike sides coplanar (hull = polar of the dual\'s rectification)'),
          dict(t=str(sp.nsimplify(Rs / hs)), kind='wall (incidence)', what='g: tips at the corners of T(P)'),
          dict(t=str(nice(sp.sqrt(Rs / hs))), kind='turn fixed point (stationary)', what='tips on the circumsphere')]
    tt_ = sp.Symbol('tt')
    for x in sp.solve(tt_ ** 2 * hs * (Rs - hs - r1s) + 2 * tt_ * r1s * hs - r1s * Rs, tt_):
        if not x.is_real: continue
        y = nice(x)
        ev.append(dict(t=str(y), kind='metric', what='edge-tangent kis: every edge tangent to the midsphere' +
                       ('' if float(x) > 1 else (' (t < 1: apex inside the face plane)' if float(x) > 0 else ' (t < 0: apex beyond the centre)'))))
    # incidences: spike over face poly (centre q2), side plane through the edge (q0, rho0 q0) and the tip t q2
    a, b = [S(x) for x in poly[0]], [S(x) for x in poly[1]]; fc = [S(x) for x in q[2]]
    def det3s(u, v, w): return sp.Matrix([u, v, w]).det()
    hits = {}
    for w in V:
        ws = [S(x) for x in w]
        if ws == a or ws == b: continue
        e = sp.expand(det3s([a[i] - ws[i] for i in range(3)], [b[i] - ws[i] for i in range(3)], [ts * fc[i] - ws[i] for i in range(3)]))
        if e == 0: continue
        for x in sp.solve(e, ts):
            if x.is_real and float(x) > 1 + 1e-12: hits.setdefault(str(nice(x)), set()).add('corner')
    for f in feetQ:
        fs = [S(x) for x in f]
        if fs == fc: continue
        e = sp.expand(det3s([a[i] - ts * fs[i] for i in range(3)], [b[i] - ts * fs[i] for i in range(3)], [ts * (fc[i] - fs[i]) for i in range(3)]))
        if e == 0: continue
        for x in sp.solve(sp.factor(e), ts):
            if x.is_real and float(x) > 1 + 1e-12: hits.setdefault(str(nice(x)), set()).add('tip')
    # does the side plane at that t coincide with a face plane of the solid (a stellation)?
    fplanes = []
    for Pp in Fpolys:
        p0, p1, p2 = [[S(x) for x in v] for v in Pp[:3]]
        n = sp.Matrix(p1) - sp.Matrix(p0); n = n.cross(sp.Matrix(p2) - sp.Matrix(p0)); fplanes.append((n, n.dot(sp.Matrix(p0))))
    for tv, kinds_ in sorted(hits.items(), key=lambda kv: float(sp.sympify(kv[0]))):
        tt = sp.sympify(tv); A3, B3, C3 = sp.Matrix(a), sp.Matrix(b), tt * sp.Matrix(fc)
        n = (B3 - A3).cross(C3 - A3); cc = n.dot(A3)
        stell = any(sp.simplify(n.cross(m)).norm() == 0 and sp.simplify(cc * m.norm() ** 2 - mc * n.dot(m)) == 0 for m, mc in fplanes)
        ev.append(dict(t=tv, kind='incidence', what='spike side through another ' + ' and '.join(sorted(kinds_)) +
                       ('; the side lies in a face plane of the solid (stellation)' if stell else '')))
    for e in ev: e['t_f'] = float(sp.sympify(e['t']))
    rec['star_line_events'] = sorted(ev, key=lambda e: e['t_f'])
    # known-case checks
    if row['name'] == 'cube': allok &= rec['T_chain'].get('gain_radius') == '3'
    if row['name'] == 'dodecahedron': allok &= sp.simplify(sp.sympify(rec['T_chain'].get('gain_radius')) - (15 - 6 * sp.sqrt(5))) == 0
    allok &= 'period' in rec['T_chain'] and 'period' in rec['core']
    print(row['symbol'], row['name'], '| T', rec['T_chain'].get('period'), rec['T_chain'].get('gain_radius'), '| core', core.get('cycle_from_turn'),
          core.get('period'), core.get('scale_radius_t1'), [tt['corners'] for tt in core['turns']], '| halo', rec['star_halo']['corners'],
          '| polar halo', rec['polar_halo']['corners'], '| stars', {k: (v['state'], v['hull_corners'], v['star_line_region']) for k, v in stars.items()},
          '|', round(time.time() - T0), 's', flush=True)
    for e in rec['star_line_events']: print('     t = %-40s %.6f  %s: %s' % (e['t'], e['t_f'], e['kind'], e['what']), flush=True)
    res.append(rec); json.dump(res, open(OUT, 'w'), indent=1, default=str)
print('FINAL ok' if allok else 'FINAL FAIL: a known-case check (#80 cube 3, dodecahedron 15 - 6 sqrt5) or a cycle failed')
