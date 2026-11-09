# ID / RT planes (exec-ed by s3; same as s2_id_rt.py)
import itertools
phi = F(Q(1, 2), Q(1, 2))
I = []
for s1, s2 in itertools.product((1, -1), repeat=2):
    base = [F(0), F(s1), phi * s2]
    for r in range(3):
        I.append(base[r:] + base[:r])
sub = lambda u, v: [a - b for a, b in zip(u, v)]
Iedges = [(i, j) for i, j in itertools.combinations(range(12), 2) if dot(sub(I[i], I[j]), sub(I[i], I[j])) == F(4)]
assert len(Iedges) == 30
ID = [[(a + b) * Q(1, 2) for a, b in zip(I[i], I[j])] for i, j in Iedges]
Ifaces = [t for t in itertools.combinations(range(12), 3) if all(tuple(sorted(p)) in set(Iedges) for p in itertools.combinations(t, 2))]
assert len(Ifaces) == 20
cent = [[I[t[0]][k] + I[t[1]][k] + I[t[2]][k] for k in range(3)] for t in Ifaces]
pl = []
for u in I:
    pl.append((u, max((dot(u, m) for m in ID), key=float), ZERO, 'pent'))
for c in cent:
    pl.append((c, max((dot(c, m) for m in ID), key=float), ZERO, 'tri'))
for m in ID:
    pl.append((m, ZERO, ONE, 'rhomb'))
