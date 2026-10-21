# DICTO 2026-10-21: the polar of the OG turned out (DICTO: "polar cycles of the OG turned out"), EXACT in Q(sqrt5), frame of #39.
# Theorem (general): for a convex solid S with the centre inside, polar(P(S)) = T(polar(S)), polar about any sphere x.x = rho^2. Hence
# polar(S_k) = polar(phi^k D_k) = phi^-k T^k(polar(OG)), and polar(OG) is the DICTO Hecatodihedron (#31: the OG is its polar).
# Checked here for k = 0..4 (rho = 1): (1) polar(OG) has the Hecatodihedron's counts; (2) the corner set of polar(S_k) equals
# phi^-k T^k(polar(OG)) exactly (T = exact_cycle.step); (3) faces and face kinds of each solid; (4) the inward sequence nests
# (polar(S_k) inside polar(S_{k-1})); (5) the shells of 1, 1 and 2 beats, inward, cut into towers on the faces of each shell's INNER
# solid (exact_shells.shell: one volume and one orbit per kind, sum = shell exactly) -- the polar towers.
# The small inner solids give exact face normals of size ~1e-6, which trip the float guessing of the #38 helpers, so kinds and towers
# are computed on phi^4 polar(S_k) (the outermost of these then being phi^4 times the Hecatodihedron); volumes are in that frame.
# usage: python3 polar_turned.py <studies/2026-10-19-five-fold-octet>
import sys, os, json
sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1])
HERE = os.path.dirname(os.path.abspath(__file__))
src = open('exact_downward.py').read(); exec(src.split("log = {")[0].replace("os.path.dirname(os.path.abspath(__file__))", repr(os.getcwd())))
# Rescale every exact face plane (n, d) by a rational close to 1/|n| (still exact), so the float guessing in the #38 helpers sees unit-size
# normals (the inner polar solids otherwise give normals of size ~1e-6).
import exact_shells as X
from fractions import Fraction as _Fr
_solid0 = X.solid
def _solid(S):
    out = []
    for n, d in _solid0(S):
        f = Q5(_Fr(1 / max(abs(x.f()) for x in n)).limit_denominator(10 ** 12)); out.append((tuple(f * x for x in n), f * d))
    return out
X.solid = _solid; solid = _solid
# As in polar_exact.py: choose the three faces at a float corner guess by their EXACT determinant, skipping float points on an edge.
import inspect
_src = inspect.getsource(X.polytope).replace("if abs(np.linalg.det(N[list(tri)])) > 1e-9: break",
    "if det3v(*[tuple(H[i][0]) for i in tri]) != Q5(0): break").replace(
    "        C.append(solve3([list(H[i][0]) for i in tri], [H[i][1] for i in tri]))",
    "        if det3v(*[tuple(H[i][0]) for i in tri]) == Q5(0): continue   # a float point on an edge, not a corner\n        C.append(solve3([list(H[i][0]) for i in tri], [H[i][1] for i in tri]))")
assert "a float point on an edge" in _src and "det3v(*" in _src
exec(_src, X.__dict__); polytope = X.polytope
def shell_orbits(A, B, label):
    """towers on the faces of A cut by B, grouped by orbits of the 60 rotations: one volume per orbit, sum = B - A exactly"""
    Hin, Hout = solid(A), solid(B); Cin, Fin = polytope(Hin); Cout, Fout = polytope(Hout); gap = volume(Cout, Fout) - volume(Cin, Fin)
    tow = {}
    for o, i in Fin:
        F = [Cin[j] for j in o]; n, d = Hin[i]; H = list(Hout) + [(tuple(-x for x in n), -d)]
        for a, b in zip(F, F[1:] + F[:1]):
            m = cross(a, b); other = [c for c in F if c not in (a, b)][0]
            if dot(m, other).sign() > 0: m = tuple(-x for x in m)
            H.append((m, Q5(0)))
        C, Fc = polytope(H); tow[frozenset(F)] = (len(F), volume(C, Fc))
    left = set(tow); orbits = []
    while left:
        F0 = next(iter(left)); orb = {frozenset(app(M, v) for v in F0) for M in G}; assert orb <= left; left -= orb
        orbits.append({'sides': len(F0), 'faces': len(orb), 'volumes': sorted({repr(tow[f][1]) for f in orb}), 'volume_float': tow[F0][1].f()})
    total = Q5(0)
    for f in tow: total = total + tow[f][1]
    orbits.sort(key=lambda o: (o['sides'], o['volume_float']))
    return {'shell': label, 'towers': len(tow), 'orbits': orbits, 'one_volume_per_orbit': all(len(o['volumes']) == 1 for o in orbits),
            'sum_equals_gap_exactly': (total - gap) == Q5(0), 'gap': repr(gap), 'gap_float': gap.f()}
ok = lambda cond, m: print(('PASS ' if cond else 'FAIL ') + m, flush=True) or cond
def pw(k):
    r = Q5(1)
    for _ in range(abs(k)): r = r * PHI if k > 0 else r / PHI
    return r
def polar(S):                                       # corners n/d of the polar (unit sphere) for the face planes n.x = d of hull(S)
    return list(dict.fromkeys(tuple(x / d for x in n) for n, d in solid(S)))
D = [OG]
for _ in range(4): D.append(rev(D[-1]))
S = [[tuple(pw(k) * x for x in v) for v in D[k]] for k in range(5)]
Pk = [polar(s) for s in S]
H = Pk[0]; C, F, Kd = kinds(H)
ok(len(H) == 80 and len(F) == 102, f'polar(OG) = the DICTO Hecatodihedron: {len(H)} corners, {len(F)} faces, kinds ' + ', '.join(f'{c} {k[0]}-gons' for k, c in Kd.items()))
TH = [H]
for _ in range(4): TH.append(step(TH[-1])[0])
res = {'mark': 'DICTO polar of the OG turned out, exact, 2026-10-21 · DICTO · dictospheres.com', 'solids': {}, 'shells': []}
for k in range(5):
    same = set(Pk[k]) == {tuple(pw(-k) * x for x in v) for v in TH[k]}
    C, F, Kd = kinds([tuple(pw(4) * x for x in v) for v in Pk[k]])
    res['solids'][f'polar S{k}'] = {'corners': len(C), 'faces': len(F), 'kinds': {f'{k_[0]}-gon': c for k_, c in Kd.items()}}
    ok(same, f'polar(S_{k}) = phi^-{k} T^{k}(Hecatodihedron) exactly: {len(C)} corners, {len(F)} faces (' + ', '.join(f'{c} {k_[0]}-gons' for k_, c in sorted(Kd.items())) + ')')
    if k: o, nb, _ = inside([tuple(pw(4) * x for x in v) for v in Pk[k]], [tuple(pw(4) * x for x in v) for v in Pk[k - 1]]); ok(o, f'polar(S_{k}) lies inside polar(S_{k - 1}) (exact)')
Q = [[tuple(pw(4) * x for x in v) for v in p] for p in Pk]
for a, b in [(1, 0), (2, 1), (4, 2)]:
    out = shell_orbits(Q[a], Q[b], f'polar S{a} -> polar S{b} (inward)'); res['shells'].append(out)
    ok(out['sum_equals_gap_exactly'] and out['one_volume_per_orbit'],
       f"inward shell polar(S_{a}) -> polar(S_{b}) ({b - a + (a - b) * 2 if False else abs(a - b)} beat{'s' if abs(a - b) > 1 else ''}): {out['towers']} towers in {len(out['orbits'])} shapes (" +
       ', '.join(f"{o['faces']} on {o['sides']}-gons {o['volume_float']:.6f}" for o in out['orbits']) + f"), adding up to the shell exactly ({out['gap_float']:.4f}, phi^4 frame)")
res['boundaries_float'] = {f'polar S{k}': [[x.f() for x in v] for v in Q[k]] for k in range(5)}   # phi^4 frame
json.dump(res, open(os.path.join(HERE, 'polar-turned.json'), 'w'), indent=1)
