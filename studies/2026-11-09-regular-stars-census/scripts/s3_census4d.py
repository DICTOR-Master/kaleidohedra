# s3_census4d.py -- the Star Cores census in 4D: the six convex regular 4-polytopes and the ten Schlafli-Hess star polychora,
# exactly in Q(sqrt5). Study 2026-11-09-regular-stars-census.
#  T-chain: T(S) = {x : v.x <= v.v} on the corners (exact half-space corners, turnlib.corners), two steps; check T^2(P) = g P exactly,
#           g = R^2/h^2 (the radius gain per period). For a star polychoron T sees only the corner set, i.e. its convex hull.
#  Star Core: one family of facets; core = hull of t x the facet centres; the core of the core = hull of the feet of its facets;
#           check exactly that two turns give s.P with s = 1/g (radius, t = 1), for the convex six.
#  Star Halo = the hull of the tips (= the core here); Polar Halo = the reciprocal (corners at the poles of the facet hyperplanes).
#  Star line: walls t = rho_k^2/h^2 (join at k = d-2 = 2, the ridge centres: the star is convex exactly up to it; g at k = 0), the fixed point R/h of the
#           turn t -> g/t, DICTO's t = 2 and phi placed in their hops, and the incidences where the side hyperplane of a facet
#           pyramid (through a ridge and the tip) passes through a corner or another tip, flagged when it is a facet hyperplane
#           of P (a stellation). Known checks: tesseract at t = 2 -> 24-cell; small stellated 120-cell = 120-cell star at t = 2/phi.
# Usage: ~/geom/bin/python -u s3_census4d.py <flags.json> <out json>
import sys, json, time
from regstar import *
import turnlib as TL
FL, OUT = sys.argv[1:3]; T0 = time.time()
rows = [r for r in json.load(open(FL)) if r['d'] == 4]
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
def poly_of(ms, q):
    poly = [q[0]]
    while True:
        nxt = refl(ms[1], refl(ms[0], poly[-1]))
        if key(nxt) == key(poly[0]): break
        poly.append(nxt)
    return poly
res = []; allok = True
byname = {}
for row in rows:
    ms = [vp(m) for m in row['mirrors']]; q = [vp(x) for x in row['q']]; r2 = [q5p(x) for x in row['r2']]
    R2, h2 = r2[0], r2[-1]; g = R2 / h2; convex = row['density'] == 1
    V = orbit_exact(ms, q[0]); feet = orbit_exact(ms, q[3])
    rec = dict(symbol=row['symbol'], name=row['name'], density=row['density'], counts=row['counts'], g=q5s(g), g_f=g.f(),
               walls_t=[q5s(x / h2) for x in reversed(r2)], walls_t_f=[(x / h2).f() for x in reversed(r2)])
    Vs = {key(v) for v in V}
    # T-chain
    if convex:
        T1 = TL.corners([(v, dotv(v, v)) for v in V]); T2 = TL.corners([(v, dotv(v, v)) for v in T1])
        ok = {key(v) for v in T2} == {key(scal(g, v)) for v in V}
        rec['T_chain'] = dict(period=2, gain_radius=q5s(g), corners=[len(V), len(T1), len(T2)], exact_check=ok)
    else:
        hull_name = '600-cell' if len(V) == 120 else '120-cell'
        rec['T_chain'] = dict(note='T sees only the corners: the chain of the convex hull, a ' + hull_name, corners=len(V))
        ok = True
    # cores
    if convex:
        N1 = TL.facets(feet); feet2 = [scal(ONE / dotv(N, N), N) for N in N1]
        s = ONE / g
        ok2 = {key(v) for v in feet2} == {key(scal(s, v)) for v in V}
        rec['core'] = dict(cycle_from_turn=0, period=2, scale_radius_t1=q5s(s), corners=[len(feet), len(feet2)], exact_check=ok2)
    else:
        rec['core'] = dict(first_core_corners=len(feet), note='the hull of the facet centres: a ' + ('600-cell' if len(feet) == 120 else '120-cell') +
                           '; from there the convex cycle (period 2)')
        ok2 = True
    rec['star_halo'] = dict(corners=len(feet), note='hull of t x the facet centres (= the first core)')
    rec['polar_halo'] = dict(corners=len(feet), note='reciprocal: corners at the poles of the facet hyperplanes, R^2/h^2 x the facet centres')
    # stars at 2 and phi: hop on the star line
    walls = [x / h2 for x in reversed(r2)]
    st = {}
    for tn, t in (('2', Q5(2)), ('phi', PHI)):
        hop = next((f'[{q5s(a)}, {q5s(b)}]' for a, b in zip(walls, walls[1:]) if a <= t <= b), 'beyond g')
        on = [q5s(w) for w in walls if w == t]
        st[tn] = dict(hop=hop, on_wall=on, convex=bool(convex and t <= walls[1]), turned_partner=q5s(g / t), turned_partner_f=(g / t).f())
    rec['stars'] = st
    # incidences on the star line: ridge (a, b, c) of the facet with centre q3, tip t q3
    poly = poly_of(ms, q); a, b, c = poly[0], poly[1], poly[2]; f = q[3]
    def side_det(t, w=None, wtip=None):
        T = scal(t, f)
        W = w if w is not None else scal(t, wtip)
        return det([subv(a, W), subv(b, W), subv(c, W), subv(T, W)])
    hits = {}
    for w in V:
        if key(w) in {key(x) for x in poly}: continue
        d0, d1 = side_det(ZERO, w=w), side_det(ONE, w=w)
        if d1 == d0: continue
        t = d0 / (d0 - d1)
        if t > ONE: hits.setdefault((t.a, t.b), [t, set()])[1].add('corner')
    for wt in feet:
        if key(wt) == key(f): continue
        # det is t x (affine in t): evaluate the affine factor at 1 and 2
        e1, e2 = side_det(ONE, wtip=wt), side_det(Q5(2), wtip=wt) / Q5(2)
        if e1 == e2: continue
        t = e1 / (e1 - e2) + ONE   # root of the affine factor through (1, e1), (2, e2)
        if t > ONE: hits.setdefault((t.a, t.b), [t, set()])[1].add('tip')
    Nf = {key(scal(ONE / h2, x)) for x in feet}   # facet hyperplanes N.x = 1, N = foot/h^2
    ev = []
    for k_, (t, kinds_) in sorted(hits.items(), key=lambda kv: kv[1][0].f()):
        T = scal(t, f); n = perp([subv(b, a), subv(c, a), subv(T, a)], 4); off = dotv(n, a)
        stell = (not off == ZERO) and key(scal(ONE / off, n)) in Nf
        ev.append(dict(t=q5s(t), t_f=t.f(), what='side hyperplane through another ' + ' and '.join(sorted(kinds_)) + ('; it is a facet hyperplane of P (stellation)' if stell else '')))
    rec['incidences'] = ev
    rec['fixed_point_t'] = 'sqrt(' + q5s(g) + ')'; rec['fixed_point_t_f'] = g.f() ** .5
    allok &= ok and ok2
    byname[row['name']] = (rec, V, feet, q, r2)
    print(row['symbol'], row['name'], '| g', q5s(g), '| T', rec['T_chain'], '| core', rec['core'], '| walls', [round(x, 5) for x in rec['walls_t_f']],
          '| stars', st, '| incid', [(e['t'], e['what'][27:]) for e in ev][:8], '|', round(time.time() - T0), 's', flush=True)
    res.append(rec); json.dump(res, open(OUT, 'w'), indent=1)
# known checks: tesseract star at t = 2: hull corners = V u tips all on one sphere, 24 of them (the 24-cell); 120-cell star at
# t = 2/phi: tips = the corners of the small stellated 120-cell scaled to share the 120-cell's facet hyperplanes
rt, V, feet, q, r2 = byname['tesseract']; tips = [scal(Q5(2), x) for x in feet]
k1 = len({dotv(v, v) for v in V + tips}) == 1 and len(V + tips) == 24
rc, V, feet, q, r2 = byname['120-cell']; rs, Vs, feets, qs, r2s = byname['small stellated 120-cell']
t = Q5(2) / PHI; tips = [scal(t, x) for x in feet]
sc = r2[-1] / r2s[-1]   # squared scale making the stellated polychoron's facet distance equal to the 120-cell's
# directions + radii: every tip is parallel to a corner of the stellated one, and |tip|^2 = sc * R_s^2
k2 = all(dotv(x, x) == sc * r2s[0] for x in tips) and all(any(parallel(x, v) for v in Vs) for x in tips[:40]) and \
     all(any(parallel(x, y) for y in feets) for x in feet[:40]) and len(feet) == len(feets)
print('check tesseract star t=2 -> 24-cell:', k1, '| small stellated 120-cell = 120-cell star at 2/phi:', k2)
allok &= k1 and k2
print('FINAL ok' if allok else 'FINAL FAIL: an exact check failed')
