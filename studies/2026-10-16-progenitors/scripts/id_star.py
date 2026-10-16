# Progenitors step 12 (DICTO 2026-10-16: the icosidodecahedron star; "shortening the spikes feels like cheating, one more solid is needed").
# The Dharma ID with its own central pyramids flipped out at full height (tips at twice the face centres), and X = the hull of its 32 tips.
# Exact in Q(sqrt5): X's corners, its face shape (cosines of the face angles), its relation to every station and to I·φ³ (corners in, out, on).
# -> data/id-star.txt, data/id-star.json
exec(open('scripts/core_hull_in_cycle.py').read().split("S = dict(C)")[0])
import json
from collections import Counter
ID = C[1][1]
fcs = []
for idx in planes(ID):
    fcs.append(([sum((ID[i][k] for i in idx), Q(0)) / len(idx) for k in range(3)], len(idx)))
T = [[x * 2 for x in c] for c, n in fcs]; kind = [n for c, n in fcs]
X = true_corners(T); plX = planes_exact(X)
out = ['DICTO · dictospheres.com', 'Progenitors step 12: the full-height icosidodecahedron star and its hull X (exact)']
r2 = lambda v: dot(v, v)
out.append(f'  tips: 20 over triangles at radius² {r2(T[kind.index(3)])!r} = {r2(T[kind.index(3)]).f():.6f}; 12 over pentagons at {r2(T[kind.index(5)])!r} = {r2(T[kind.index(5)]).f():.6f}')
out.append(f'  X: {len(X)} corners (all 32 tips are corners: {len(X) == 32}), {len(plX)} faces')
# face shape: for each face (triangle), cos of its angles, exactly: cos² = (u·v)²/(u·u v·v)
cos2 = Counter()
for n, d in plX:
    F = [v for v in X if dot(n, v) == d]; assert len(F) == 3
    for i in range(3):
        a, b, c = F[i], F[(i + 1) % 3], F[(i + 2) % 3]; u = [b[k] - a[k] for k in range(3)]; w = [c[k] - a[k] for k in range(3)]
        uw = dot(u, w); cos2[(repr(uw * uw / (dot(u, u) * dot(w, w))), uw.f() > 0)] += 1
out.append('  face angles, exact cos² (and sign): ' + '; '.join(f'cos² = {k[0]} ({"+" if k[1] else "−"}) × {v}' for k, v in sorted(cos2.items())))
def rel(A, B):
    pl = planes_exact(B); m = [max((dot(n, a) - d for n, d in pl), key=lambda q: q.f()) for a in A]
    return Counter('out' if x.f() > 0 and x != 0 else 'on' if x == 0 else 'in' for x in m)
for nm, V in C:
    a = rel(V, X); b = rel(X, V); out.append(f'  {nm:5s}: its corners vs X {dict(a)};  X corners vs {nm} {dict(b)}')
print('\n'.join(out)); open('data/id-star.txt', 'w').write('\n'.join(out) + '\n')
json.dump({'ID': [[x.f() for x in v] for v in ID], 'tips': [[x.f() for x in v] for v in T], 'kind': kind, 'X': [[x.f() for x in v] for v in X]}, open('data/id-star.json', 'w'))
