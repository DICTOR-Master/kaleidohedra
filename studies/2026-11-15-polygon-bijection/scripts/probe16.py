"""Why the 4-crossing term vanishes at l = 16 (study 2026-11-15-polygon-bijection).
At l = 16 the only possible split with both asymmetries nonzero is R = F = 6.  For the far half (3C letters) and the weighted
root half (root = boundary atom, 3C letters), list every shape S with A != 0 at 6 bonds and the matchings carrying it."""
import halves as H
from collections import defaultdict, Counter
c = [0, 1, 2, 0, 1, 2, 0]; Af = H.asym(H.tables(c, 6, None)[0])
cw = [0, 2, 1, 0, 2, 1, 0]; Aw = H.asym(H.tables(cw, 6, (0, 1))[0])
byS = defaultdict(dict)
for (S, M, F), v in Af.items():
    if v and F == 6: byS[S][M] = v
print('shapes with A_far != 0 at F = 6:', len(byS))
tot = 0; same = 0
for S, d in sorted(byS.items(), key=lambda z: sorted(z[0])):
    ws = {M: Aw.get((S, M, 6), 0) for M in H.matchings(S)}
    carrier_f = [M for M in d]; carrier_w = [M for M, v in ws.items() if v]
    same += carrier_f == carrier_w
    tot += sum(ws[M] * v for M in ws for Mp, v in d.items() if Mp != M)
    print('  S', sorted(S), 'A_far', [(sorted(map(sorted, M)), v) for M, v in d.items()], 'A_root_w', [(sorted(map(sorted, M)), v) for M, v in ws.items() if v])
print('shapes where both asymmetries sit on the same single matching:', same, 'of', len(byS))
print('sum over M != M\' of A_w * A_far at (6, 6):', tot)
