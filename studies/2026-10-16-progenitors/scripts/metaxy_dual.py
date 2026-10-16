# The dual of the DICTO Metaxyhexecontahedron M (exact, Q(√5)). M has an insphere (all 60 faces at one distance), so its polar in any sphere
# has all 60 corners on one sphere. In the ends sphere of Double Vision (ρ² = φ²/4, which swaps the original and reversed cycles):
# RT ⊂ M ⊂ I·φ³ becomes polar(I·φ³) ⊂ polar(M) ⊂ polar(RT); checks that polar(M) touches both, its faces (12 pentagons, 20 hexagons),
# the hexagon's two side lengths and their ratio, and that it is the icosahedron polar(RT)… cut by a dodecahedron. -> data/metaxy-dual.txt
exec(open('scripts/core_hull_in_cycle.py').read().split("S = dict(C)")[0])
from fractions import Fraction as Fr
S = dict(C); RT = S['RT']; IP = S['I·φ³']
sq = lambda v: dot(v, v); RI2 = max((sq(v) for v in RT), key=lambda q: q.f())
fc = [[sum((IP[i][k] for i in idx), Q(0)) / len(idx) for k in range(3)] for idx in planes(IP)]
M = [v for v in RT if sq(v) == RI2] + fc
rho2 = Q(Fr(3, 8), Fr(1, 8))   # φ²/4
def pol(V): return [[x * rho2 / d for x in n] for n, d in planes_exact(V)]
PM, PIP, PRT = pol(M), pol(IP), pol(RT)
def sgn(q):
    a, b = q.a, q.b
    if b == 0: return (a > 0) - (a < 0)
    if a == 0: return (b > 0) - (b < 0)
    if (a > 0) == (b > 0): return 1 if a > 0 else -1
    return (1 if a > 0 else -1) * ((a * a > 5 * b * b) - (a * a < 5 * b * b))
le = lambda x, y: sgn(y - x) >= 0
inside = lambda A, B: all(le(dot(n, v), d) for n, d in planes_exact(B) for v in A)
touch = lambda A, B: sum(1 for v in A if any(dot(n, v) == d for n, d in planes_exact(B)))
r2 = {repr(sq(v)) for v in PM}
pl = planes_exact(PM); kinds = {}
for n, d in pl: k = sum(1 for v in PM if dot(n, v) == d); kinds[k] = kinds.get(k, 0) + 1
n, d = next((n, d) for n, d in pl if sum(1 for v in PM if dot(n, v) == d) == 6)
H = [v for v in PM if dot(n, v) == d]
L = sorted({sq([a[i] - b[i] for i in range(3)]) for a in H for b in H if a is not b}, key=lambda q: q.f())[:2]
out = ['DICTO · dictospheres.com', 'The dual of the DICTO Metaxyhexecontahedron (exact, Q(√5)); polar in ρ² = φ²/4',
       f'  60 corners, all at squared radius {sorted(r2)};  faces by corner count {kinds}',
       f'  hexagon sides, squared: {L[0]!r} and {L[1]!r}; ratio² {L[1] / L[0]!r} = {(L[1] / L[0]).f():.9f} (ratio {(L[1] / L[0]).f() ** .5:.9f})',
       f'  polar(I·φ³) inside it: {inside(PIP, PM)}, touching corners {touch(PIP, PM)};  it inside polar(RT): {inside(PM, PRT)}, its corners on polar(RT)\'s faces: {touch(PM, PRT)}']
print('\n'.join(out)); open('data/metaxy-dual.txt', 'w').write('\n'.join(out) + '\n')
