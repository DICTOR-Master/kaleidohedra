# Step 7 (DICTO's question): the Hecatodihedron taken out, can a dual pair X, Y (one inside the other) fill the inner gap tightly?
# Chain D ⊂ s1*X ⊂ s2*Y ⊂ ID. Three contacts with two free scales: D touches X, Y touches ID, and X touches Y. The pair locks when
# all three hold at once: slack = (largest s2 with Y in ID) * (largest t with X in Y) / (smallest s1 with D in X) = 1.
import sys, numpy as np
from scipy.spatial import ConvexHull
src = open('scripts/polar_round.py').read().split('def rad(V, u):')[0]
exec(src)
D, ID = C['dodecahedron (inner)'], C['icosidodecahedron']
def grow(A, B): return min(-e[3] / max(A @ e[:3]) for e in ConvexHull(B).equations)   # largest s with s*A inside B
SOL['icosahedron'] = I0 @ SW; SOL['dodecahedron'] = dual(SOL['icosahedron'])
PAIRS = [('icosidodecahedron', 'rhombic triacontahedron'), ('truncated icosahedron', 'pentakis dodecahedron'),
         ('truncated dodecahedron', 'triakis icosahedron'), ('rhombicosidodecahedron', 'deltoidal hexecontahedron'),
         ('truncated icosidodecahedron', 'disdyakis triacontahedron'), ('icosahedron', 'dodecahedron')]
lines = []
for a, b in PAIRS:
    for X, Y in [(a, b), (b, a)]:
        s1 = 1 / grow(D, SOL[X]); s2 = grow(SOL[Y], ID); t = grow(SOL[X], SOL[Y])
        sl = s2 * t / s1                                   # s1*X inside s2*Y needs s1 <= s2*t
        lines.append(f'{X} inside {Y}: slack {sl:.6f} ' + ('LOCKED' if abs(sl - 1) < 1e-6 else 'fits, floats' if sl > 1 else 'does not fit'))
print('\n'.join(lines)); open('data/polar-dual-pair.txt', 'w').write('\n'.join(lines) + '\n')
