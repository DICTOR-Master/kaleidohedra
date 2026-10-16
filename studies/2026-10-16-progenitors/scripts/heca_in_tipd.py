# Prior-art check (2026-10-16): is the Hecatodihedron's Shield apex exactly a vertex of the canonical pentakis dodecahedron (the truncated
# icosahedron's polar in its own midsphere, rho² = 9/4)? Exact in Q(sqrt5). -> data/heca-in-tipd.txt
exec(open('scripts/pair_chain.py').read().split("s, ts = contain(H, O)")[0])
from fractions import Fraction as Fr
TI = true_corners(st['truncated icosahedron']); rho2 = Q(Fr(9, 4))
PD = [[x * rho2 for x in v] for v in polar(TI)]
key = lambda v: tuple((x.a, x.b) for x in v)
Hk = {key(v) for v in H}; TIk = {key(v) for v in TI}; PDk = {key(v) for v in PD}
apex = Hk - TIk
out = ['DICTO · dictospheres.com', 'Is the Hecatodihedron TI + the 20 hexagon tips of the canonical pentakis dodecahedron? (exact)',
       f'  H corners {len(Hk)} = TI corners {len(Hk & TIk)} + Shield apexes {len(apex)}',
       f'  canonical PD (polar of TI in its midsphere, rho² = 9/4): {len(PD)} corners',
       f'  every Shield apex is a corner of the canonical PD: {apex <= PDk} ({len(apex & PDk)} of 20)',
       '  so H = convex hull of TI and the 20 three-fold corners of its canonical dual PD; the H–O compound shares core (rTI) and hull (joined TI) with the classical TI–PD compound']
print('\n'.join(out)); open('data/heca-in-tipd.txt', 'w').write('\n'.join(out) + '\n')
