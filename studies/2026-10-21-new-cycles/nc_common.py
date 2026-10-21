# DICTO 2026-10-21, follow-up cycles to #43 (DICTO Kyushindo Cores): shared exact machinery, exec'd by cleo_turned.py,
# og_up_polar.py, ott_turned.py. Loads the #38/#39 exact machinery of studies/2026-10-19-five-fold-octet (Q5, PHI, step = T,
# rev = P, solid, polytope, volume, inside, kinds, shell, the OG and its 60 rotations G), with the two patches of polar_turned.py
# (face planes rescaled to unit size by an exact rational; corners chosen by EXACT determinant), plus: polar(), pw(), and
# shell_orbits(A, B, group): towers on the faces of the inner solid A cut by the outer solid B, grouped by orbits of the group,
# one volume per orbit, sum = B - A exactly.   Expects FIVE (the five-fold-octet dir) and HERE set by the caller.
import sys, os, json, time, itertools, inspect
sys.path.insert(0, FIVE); os.chdir(FIVE)
src = open('exact_downward.py').read(); exec(src.split("log = {")[0].replace("os.path.dirname(os.path.abspath(__file__))", repr(os.getcwd())))
import exact_shells as X
from fractions import Fraction as _Fr
_solid0 = X.solid
def _solid(S):
    out = []
    for n, d in _solid0(S):
        f = Q5(_Fr(1 / max(abs(x.f()) for x in n)).limit_denominator(10 ** 12)); out.append((tuple(f * x for x in n), f * d))
    return out
X.solid = _solid; solid = _solid
_src = inspect.getsource(X.polytope).replace("if abs(np.linalg.det(N[list(tri)])) > 1e-9: break",
    "if det3v(*[tuple(H[i][0]) for i in tri]) != Q5(0): break").replace(
    "        C.append(solve3([list(H[i][0]) for i in tri], [H[i][1] for i in tri]))",
    "        if det3v(*[tuple(H[i][0]) for i in tri]) == Q5(0): continue   # a float point on an edge, not a corner\n        C.append(solve3([list(H[i][0]) for i in tri], [H[i][1] for i in tri]))")
assert "a float point on an edge" in _src and "det3v(*" in _src
exec(_src, X.__dict__); polytope = X.polytope
ok = lambda cond, m: print(('PASS ' if cond else 'FAIL ') + m, flush=True) or cond
def pw(k):
    r = Q5(1)
    for _ in range(abs(k)): r = r * PHI if k > 0 else r / PHI
    return r
scale = lambda c, S: [tuple(c * x for x in v) for v in S]
def polar(S):                                       # corners n/d of the polar (unit sphere) of hull(S), faces n.x = d
    return list(dict.fromkeys(tuple(x / d for x in n) for n, d in solid(S)))
def corners(S):                                     # the true corners of hull(S) (drops listed points that are not corners)
    C, F = polytope(solid(S)); return C
def symmetric(S, group): s = set(S); return all({app(M, v) for v in S} == s for M in group)
def kind_str(K): return ', '.join(f'{c} {k[0]}-gons' for k, c in sorted(K.items(), key=lambda kc: (kc[0][0], -kc[1])))
def describe(S):
    C, F, K = kinds(S)
    return {'corners': len(C), 'faces': len(F), 'edges': sum(len(o) for o, _ in F) // 2,
            'faces_by_sides': {str(s): sum(c for k, c in K.items() if k[0] == s) for s in sorted({k[0] for k in K})},
            'face_kinds_exact': [{'sides': k[0], 'count': c, 'squared_sides': list(k[1])} for k, c in K.items()],
            'volume': repr(volume(C, F)), 'volume_float': volume(C, F).f(),
            'corner_radii_float': sorted({round(dot(v, v).f() ** .5, 6) for v in C})}, C, F, K
def shell_orbits(A, B, group, label):
    Hin, Hout = solid(A), solid(B); Cin, Fin = polytope(Hin); Cout, Fout = polytope(Hout); gap = volume(Cout, Fout) - volume(Cin, Fin)
    tow = {}
    for o, i in Fin:
        F = [Cin[j] for j in o]; n, d = Hin[i]; H = list(Hout) + [(tuple(-x for x in n), -d)]
        for a, b in zip(F, F[1:] + F[:1]):
            m = cross(a, b); other = [c for c in F if c not in (a, b)][0]
            if dot(m, other).sign() > 0: m = tuple(-x for x in m)
            H.append((m, Q5(0)))
        if any(all((dot(n2, c) - d2) == Q5(0) for c in F) for n2, d2 in Hout):     # the face lies ON the outer surface: a flat tower,
            tow[frozenset(F)] = (len(F), Q5(0)); continue                            # volume 0 exactly (the outer face plane holds it)
        C, Fc = polytope(H); tow[frozenset(F)] = (len(F), volume(C, Fc))
    left = set(tow); orbits = []
    while left:
        F0 = next(iter(left)); orb = {frozenset(app(M, v) for v in F0) for M in group}; assert orb <= left; left -= orb
        orbits.append({'sides': len(F0), 'faces': len(orb), 'volumes': sorted({repr(tow[f][1]) for f in orb}), 'volume_float': tow[F0][1].f()})
    total = Q5(0)
    for f in tow: total = total + tow[f][1]
    orbits.sort(key=lambda o: (o['sides'], o['volume_float']))
    shapes = len({o['volumes'][0] for o in orbits}); flat = sum(o['faces'] for o in orbits if o['volume_float'] == 0)
    return {'shell': label, 'towers': len(tow), 'flat_towers_volume_0': flat, 'orbits': orbits, 'distinct_volumes': shapes, 'one_volume_per_orbit': all(len(o['volumes']) == 1 for o in orbits),
            'sum_equals_gap_exactly': (total - gap) == Q5(0), 'gap': repr(gap), 'gap_float': gap.f()}
def shell_line(out):
    return (f"{out['shell']}: {out['towers'] - out['flat_towers_volume_0']} towers" + (f" (+{out['flat_towers_volume_0']} faces lying on the outer surface, flat)" if out['flat_towers_volume_0'] else '') + f" in {len(out['orbits'])} orbits (" + ', '.join(f"{o['faces']} on {o['sides']}-gons {o['volume_float']:.6f}" for o in out['orbits'])
            + f"), one volume per orbit, adding up to the shell exactly (gap {out['gap_float']:.6f})")
def tmin(D, PD):
    """exact t_min(D) = max over corners v of D and faces (n, d) of P(D) of n.v / d (D inside t.P(D) iff t >= t_min)"""
    best = None
    for v in D:
        for n, d in solid(PD):
            r = dot(n, v) / d
            if best is None or (r - best).sign() > 0: best = r
    return best
fl = lambda S: [[x.f() for x in v] for v in S]
