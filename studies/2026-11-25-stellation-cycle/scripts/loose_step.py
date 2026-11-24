"""Earlier cycles, open problem (1) of the Golden Cycle book: close the loose step O ⊂ rTI with a polyhedron touching both.
Test the uniform H3 permutahedron (truncated icosidodecahedron) exactly in Q(sqrt5): least scale s with O inside s.P (touching corners), then
whether s.P lies inside rTI and touches it; and the other way (largest scale inside rTI, does it hold O). The stations O and rTI are rebuilt
by the Progenitors study's own code (study 2026-10-16-progenitors, core_hull_in_cycle.py, Dharma frame); run from inside that study.
-> ../2026-11-25-stellation-cycle/data/loose-step.json"""
import os, sys, json
_c = os.chdir
os.chdir = lambda p: _c(os.path.expanduser(p).replace("/kaleidohedra/", "/k-research/"))
import builtins
_o = builtins.open
builtins.open = lambda p, *a, **k: _o(os.path.expanduser(p).replace("/kaleidohedra/", "/k-research/") if isinstance(p, str) else p, *a, **k)
exec(open('scripts/core_hull_in_cycle.py').read().split("S = dict(C)")[0])
builtins.open = _o
os.chdir = _c
OUT = os.path.expanduser('~/k-research/studies/2026-11-25-stellation-cycle')
sys.path.insert(0, os.path.join(OUT, 'scripts'))
import q5
from fractions import Fraction as Fr
def conv(v): return tuple(q5.Q(Fr(x.a), Fr(x.b)) for x in v)
S = dict(C); O = [conv(v) for v in S['O']]; rTI = [conv(v) for v in core]; Id = [conv(v) for v in S['I']]
# H3 permutahedron, same coordinates as cycle.py; turned to the Dharma frame (5-fold axes along the Dharma icosahedron's corners)
ip = q5.IPHI; PHI = q5.PHI
P = q5.cyclic_signs([(ip, ip, 3 + PHI), (2 * ip, PHI, 1 + 2 * PHI), (ip, PHI + 1, 3 * PHI - 1), (2 * PHI - 1, q5.Q(2), 2 + PHI), (PHI, q5.Q(3), 2 * PHI)])
def supp(V, n):
    h = max((q5.dot(n, v) for v in V), key=lambda q: q.f()); return h, sum(1 for v in V if q5.dot(n, v) == h)
if supp(P, Id[0])[1] != 10:
    P = [(v[1], v[0], v[2]) for v in P]
assert supp(P, Id[0])[1] == 10
def facets(V):
    """exact facet planes (n, h) of a centrally placed convex polytope with vertices V: supporting planes through >= 3 corners"""
    import itertools
    pl = {}
    Vf = [[x.f() for x in v] for v in V]
    def fcross(u, w): return (u[1]*w[2]-u[2]*w[1], u[2]*w[0]-u[0]*w[2], u[0]*w[1]-u[1]*w[0])
    for a, b, c in itertools.combinations(range(len(V)), 3):
        A, B, Cc = Vf[a], Vf[b], Vf[c]
        nf = fcross([B[i]-A[i] for i in range(3)], [Cc[i]-A[i] for i in range(3)])
        if sum(x*x for x in nf) < 1e-18: continue
        hf = sum(nf[i]*A[i] for i in range(3))
        if abs(hf) < 1e-12: continue
        if hf < 0: nf = [-x for x in nf]; hf = -hf
        if any(sum(nf[i] * w[i] for i in range(3)) > hf + 1e-9 for w in Vf): continue
        n = q5.cross(q5.vsub(V[b], V[a]), q5.vsub(V[c], V[a]))
        if q5.iszero(n): continue
        h = q5.dot(n, V[a])
        if h.sign() < 0: n = q5.vsc(q5.Q(-1), n); h = -h
        if h.sign() == 0: continue
        k = (q5.pkey(n), next(x.sign() for x in n if x.sign() != 0))
        if k in pl: continue
        nf = [x.f() for x in n]; hf = h.f()
        if any(sum(nf[i] * w[i] for i in range(3)) > hf + 1e-9 for w in Vf): continue
        if all(q5.dot(n, v) <= h for v in V): pl[k] = (n, h)
    return list(pl.values())
res = {}
FP, FR, FO = facets(P), facets(rTI), facets(O)
res['facets'] = dict(P=len(FP), rTI=len(FR), O=len(FO), O_corners=len(O), rTI_corners=len(rTI))
def least(X, F):            # least s with X inside s.(polytope with facets F)
    return max((q5.dot(n, v) / h for v in X for n, h in F), key=lambda q: q.f())
def touch(X, F, s):         # corners of X on the faces of s.polytope
    return sum(1 for v in X if any(q5.dot(n, v) == s * h for n, h in F))
s1 = least(O, FP)           # O inside s1.P, touching
t1 = least([q5.vsc(s1, v) for v in P], FR)   # s1.P inside t1.rTI; closes the step iff t1 == 1 and touching
res['P scaled to hold O'] = dict(scale=repr(s1), approx=s1.f(), O_corners_touching=touch(O, FP, s1),
                                  P_inside_rTI=(t1 <= 1), reach_toward_rTI=t1.f(), closes=(t1 == 1))
s2 = q5.Q(1) / least(P, FR)  # largest scale inside rTI
res['P scaled to touch rTI from inside'] = dict(scale=repr(s2), approx=s2.f(), holds_O=(least(O, FP) <= s2))
res['O inside rTI (check)'] = repr(least(O, FR))
print(json.dumps(res, indent=1)); json.dump(res, open(os.path.join(OUT, 'data/loose-step.json'), 'w'), indent=1)
ok = (len(FP), len(FR), len(FO)) == (62, 92, 80) and least(O, FR) < 1 and touch(O, FP, s1) > 0
print('FINAL ok' if ok else 'FINAL FAIL: facet counts or nesting check')
