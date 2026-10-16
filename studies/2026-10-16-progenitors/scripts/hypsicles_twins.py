# Progenitors step 11 (DICTO 2026-10-16: "it should be a special filling variety like Cleo-Icosa" → Hypsicles twins). The Dharma icosahedron I
# (20 Cleo-Icos) and the dodecahedron D'' in the same circumsphere (12 "Cleo-Dodecas", its central pyramids). Exact in Q(sqrt5): Hypsicles'
# equal heights, the interlocked pair, its common core and hull (counts float), and how core, hull and D'' sit in the nine-station cycle.
# -> data/hypsicles.txt, data/hypsicles.json
exec(open('scripts/core_hull_in_cycle.py').read().split("S = dict(C)")[0])
import json
I = C[0][1]; Dd = true_corners(st['dodecahedron'])
r2 = lambda V: dot(V[0], V[0])
k2 = r2(I) / r2(Dd)                                                     # D'' = s·D with s² = k2; s must lie in Q(√5)
from fractions import Fraction as Fr
def sqrtQ(t):
    f = float(t.f()) ** .5
    for den in range(1, 400):
        for bb in range(-300, 301):
            b = Fr(bb, den); a = Fr(round((f - float(b) * 5 ** .5) * den), den); s = Q(a, b)
            if s * s == t and s.f() > 0: return s
s = sqrtQ(k2); D2 = [[x * s for x in v] for v in Dd]
inr2 = lambda V: min((d * d / dot(n, n) for n, d in planes_exact(V)), key=lambda q: q.f())
out = ['DICTO · dictospheres.com', 'Progenitors step 11: the Hypsicles twins, I (20 Cleo-Icos) and D\'\' (12 Cleo-Dodecas) in one sphere (exact)',
       f'  D\'\' = s·D with s = {s!r} = {s.f():.6f}; circumradius² both {r2(I)!r}',
       f'  Hypsicles: inradius² of I {inr2(I)!r}, of D\'\' {inr2(D2)!r}: equal {inr2(I) == inr2(D2)} (Cleo-Ico and Cleo-Dodeca have the same height)']
If = np.array([[x.f() for x in v] for v in I]); Df = np.array([[x.f() for x in v] for v in D2])
from scipy.spatial import HalfspaceIntersection
core = HalfspaceIntersection(np.vstack([ConvexHull(If).equations, ConvexHull(Df).equations]), np.zeros(3)).intersections; core = np.unique(np.round(core, 9), axis=0)
hc = ConvexHull(core); core = core[hc.vertices]; hc = ConvexHull(core); hull = ConvexHull(np.vstack([If, Df]))
def sig(h, P):
    from collections import Counter; seen = {}
    for e in h.equations:
        kk = tuple(np.round(e, 6))
        if kk not in seen: seen[kk] = sum(1 for p in P if abs(p @ e[:3] + e[3]) < 1e-7)
    return dict(sorted(Counter(seen.values()).items()))
rc = np.linalg.norm(core, axis=1)
out.append(f'  core I ∩ D\'\': {len(core)} corners (radius {rc.min():.6f}–{rc.max():.6f}), faces {sig(hc, core)} (sides: count); all 32 face planes touch the common insphere')
E = sorted(set(np.round([np.linalg.norm(core[a] - core[b]) for sm in hc.simplices for a, b in itertools.combinations(sm, 2)], 6)))
out.append(f'    core distances along faces (float) include {E[:4]}')
P = np.vstack([If, Df]); out.append(f'  hull: {len(hull.vertices)} corners (all on the common circumsphere), faces {sig(hull, P)}')
# place in the cycle: D'' and the core against the stations
def rel(A, B):
    pl = planes_exact(B); m = [max((dot(n, a) - d for n, d in pl), key=lambda q: q.f()) for a in A]
    return all(not (x.f() > 0 and x != 0) for x in m), sum(1 for x in m if x == 0)
for n, V in C[:3]:
    a, t = rel(D2, V); b, u = rel(V, D2); out.append(f'  D\'\' vs {n}: inside {a} ({t} touch); {n} inside D\'\' {b} ({u} touch)')
print('\n'.join(out)); open('data/hypsicles.txt', 'w').write('\n'.join(out) + '\n')
json.dump({'I': If.tolist(), 'D': Df.tolist(), 'core': core.tolist()}, open('data/hypsicles.json', 'w'))
