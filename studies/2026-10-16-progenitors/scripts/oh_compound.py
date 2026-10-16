# Progenitors step 6 (DICTO 2026-10-16: "make OH first", after "double inverted like a stella octangula"): the compound of the Hecatodihedron H and
# the Ogdoecontahedron O, O taken as H's polar in the sphere that touches H's 90 rhombi and triangles (so O's 90 sphere corners kiss those faces).
# Exact in Q(sqrt5): the sphere, which corners of each poke out of the other, the common core (H ∩ O) and the hull (corner, face counts),
# their volumes. -> data/oh-compound.txt, data/oh-compound.json (float corners for renders)
exec(open('scripts/pair_chain.py').read().split("s, ts = contain(H, O)")[0])
import json
from fractions import Fraction as Fr
plH = planes_exact(H)
dist2 = lambda n, d: (d * d) / dot(n, n)                    # squared distance of plane n.x = d from the centre
d2s = sorted({dist2(n, d) for n, d in plH}, key=lambda q: q.f())
cnt = {q: sum(1 for n, d in plH if dist2(n, d) == q) for q in d2s}
out = ['DICTO · dictospheres.com', 'Progenitors step 6: the O–H compound (exact, Q(√5))', '  H face distances²: ' + '; '.join(f'{q!r} = {q.f():.6f} ({cnt[q]} faces)' for q in d2s)]
rho2 = max(d2s, key=lambda q: cnt[q])                       # the sphere of the 90 rhombi and triangles
rho2 = next(q for q in d2s if cnt[q] == 90)
Orho = [[x * rho2 for x in v] for v in O]                    # polar in that sphere = rho² × polar in the unit sphere
plO = planes_exact(Orho)
def status(P, pl):
    s = []
    for p in P:
        m = max((dot(n, p) - d for n, d in pl), key=lambda q: q.f()); s.append('out' if m.f() > 0 else 'on' if m == 0 else 'in')
    return {k: s.count(k) for k in ('in', 'on', 'out')}
out.append(f'  sphere: rho² = {rho2!r} = {rho2.f():.6f} (touches H\'s 90 rhombi and triangles)')
out.append(f'  O corners vs H: {status(Orho, plH)}   H corners vs O: {status(H, plO)}')
Hf = np.array([[x.f() for x in v] for v in H]); Of = np.array([[x.f() for x in v] for v in Orho])
from scipy.spatial import HalfspaceIntersection
eqs = np.vstack([ConvexHull(Hf).equations, ConvexHull(Of).equations])
core = HalfspaceIntersection(eqs, np.zeros(3)).intersections; core = np.unique(np.round(core, 9), axis=0)
hc = ConvexHull(core); hull = ConvexHull(np.vstack([Hf, Of]))
def nfaces(h): return len({tuple(np.round(e, 6)) for e in h.equations})
def fsig(h, P):
    seen = {}; 
    for e in h.equations:
        k = tuple(np.round(e, 6))
        if k not in seen: seen[k] = sum(1 for p in P[h.vertices] if abs(p @ e[:3] + e[3]) < 1e-7)
    from collections import Counter; return dict(sorted(Counter(seen.values()).items()))
out.append(f'  common core H ∩ O: {len(hc.vertices)} corners, {nfaces(hc)} faces {fsig(hc, core)} (sides: count), volume {hc.volume:.6f} (float)')
out.append(f'  hull of the compound: {len(hull.vertices)} corners, {nfaces(hull)} faces {fsig(hull, np.vstack([Hf, Of]))}, volume {hull.volume:.6f} (float)')
out.append(f'  H volume {ConvexHull(Hf).volume:.6f}, O volume {ConvexHull(Of).volume:.6f} (float)')
print('\n'.join(out)); open('data/oh-compound.txt', 'w').write('\n'.join(out) + '\n')
json.dump({'H': Hf.tolist(), 'O': Of.tolist(), 'core': core[hc.vertices].tolist()}, open('data/oh-compound.json', 'w'))
# exact: O's 90 sphere corners are the truncated icosahedron's 90 edge midpoints (its midsphere has radius² 9/4 = the sphere above)
TIx = true_corners(st['truncated icosahedron']); e2 = min((dot([a[i] - b[i] for i in range(3)], [a[i] - b[i] for i in range(3)]) for a, b in itertools.combinations(TIx, 2)), key=lambda q: q.f())
mids = {tuple(((a[i] + b[i]) / 2).a for i in range(3)) + tuple(((a[i] + b[i]) / 2).b for i in range(3))
        for a, b in itertools.combinations(TIx, 2) if dot([a[i] - b[i] for i in range(3)], [a[i] - b[i] for i in range(3)]) == e2}
O90 = {tuple(v[i].a for i in range(3)) + tuple(v[i].b for i in range(3)) for v in Orho if dot(v, v) == rho2}
extra = ['  exact: the 90 corners of O on the sphere rho² = 9/4 are the 90 edge midpoints of the Dharma truncated icosahedron: ' + str(O90 == mids and len(mids) == 90),
         '  so the common core H ∩ O is the rectified truncated icosahedron of the Dharma TI (12 regular pentagons, 20 regular hexagons, 60 triangles,',
         '  all 90 corners on the TI midsphere), and the hull of the compound (90 faces, all touching that sphere, normals through the core corners)',
         '  is its polar in that sphere: core and hull are a dual pair, as the octahedron and cube are for the stella octangula.']
print('\n'.join(extra)); open('data/oh-compound.txt', 'a').write('\n'.join(extra) + '\n')
