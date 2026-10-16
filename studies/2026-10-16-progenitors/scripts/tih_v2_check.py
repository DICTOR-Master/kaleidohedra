# Exact checks for #28 Version 2 (Fable's merit-and-order advice, 2026-10-16), all in Q(sqrt5), Dharma frame (TI of edge 1/φ, midsphere 3/2):
# (1) the 20 Shield apexes of the Hecatodihedron H are the 20 three-fold vertices of the canonical pentakis dodecahedron PD (TI's polar in its
#     midsphere, rho² = 9/4); (2) the face planes of H are exactly the 90 face planes of the joined truncated icosahedron jtI = hull(TI ∪ PD)
#     and TI's 12 pentagon planes, i.e. H = jtI with its 12 five-fold corners cut off at the pentagon planes; (3) the DICTO Hecatogdoecontahedron
#     (H with O = H's polar in the same sphere): the hull of H ∪ O has exactly the corners of TI ∪ PD (so it is jtI), and O's 90 sphere corners
#     are TI's edge midpoints (the corners of the rectified TI, the core); (4) by polarity O = PD cut by TI's 20 hexagon planes (checked: O's
#     face planes = PD's 60 face planes ∪ TI's 20 hexagon planes, pole-for-plane). -> data/tih-v2-check.txt
exec(open('scripts/pair_chain.py').read().split("s, ts = contain(H, O)")[0])
from fractions import Fraction as Fr
TI = true_corners(st['truncated icosahedron']); rho2 = Q(Fr(9, 4))
pol = lambda V: [[x * rho2 for x in v] for v in polar(V)]                       # polar in the TI midsphere
PD = true_corners(pol(TI)); O9 = true_corners(pol(H))
key = lambda v: tuple((x.a, x.b) for x in v)
def pkeys(V):                                                                     # face planes as their poles n/d (unique, exact)
    return {key([x / d for x in n]) for n, d in planes_exact(V)}
K = lambda V: {key(v) for v in V}
apex = K(H) - K(TI)
jtI = true_corners(TI + PD)
pen = {key([x / d for x in n]) for n, d in planes_exact(TI) if sum(1 for v in TI if dot(n, v) == d) == 5}
hexp = {key([x / d for x in n]) for n, d in planes_exact(TI) if sum(1 for v in TI if dot(n, v) == d) == 6}
out = ['DICTO · dictospheres.com', '#28 Version 2: exact checks (Q(√5), Dharma frame, TI midsphere radius 3/2)',
       f'  (1) the 20 Shield apexes are corners of the canonical pentakis dodecahedron: {apex <= K(PD)} ({len(apex & K(PD))} of {len(apex)})',
       f'  (2) jtI = hull(TI ∪ PD): {len(jtI)} corners, {len(pkeys(jtI))} faces; face planes of H = jtI planes ∪ TI pentagon planes: {pkeys(H) == (pkeys(jtI) | pen)}',
       f'      ({len(pkeys(H))} = {len(pkeys(jtI))} + {len(pen)}); so H = jtI with its 12 five-fold corners cut off at the pentagon planes',
       f'  (3) hull of H ∪ O: corners = TI ∪ PD corners: {K(true_corners(H + O9)) == K(TI) | K(PD)} (the jtI)']
E2 = min((dot([a[i] - b[i] for i in range(3)], [a[i] - b[i] for i in range(3)]) for a, b in itertools.combinations(TI, 2)), key=lambda q: q.f())
mids = {key([(a[i] + b[i]) / 2 for i in range(3)]) for a, b in itertools.combinations(TI, 2) if dot([a[i] - b[i] for i in range(3)], [a[i] - b[i] for i in range(3)]) == E2}
O90 = {key(v) for v in O9 if dot(v, v) == rho2}
out.append(f'      O\'s 90 sphere corners are TI\'s 90 edge midpoints (the rectified TI\'s corners, the common core): {O90 == mids}')
out.append(f'  (4) O\'s face planes = PD\'s face planes ∪ TI\'s hexagon planes: {pkeys(O9) == (pkeys(PD) | hexp)} ({len(pkeys(O9))} = {len(pkeys(PD))} + {len(hexp)}), so O = PD cut by the 20 hexagon planes')
out.append(f'  counts: H {len(H)} corners, {len(pkeys(H))} faces; O {len(O9)} corners, {len(pkeys(O9))} faces; the compound 182 faces, 182 corners')
print('\n'.join(out)); open('data/tih-v2-check.txt', 'w').write('\n'.join(out) + '\n')
