# Exact check (Q(√5)) of the golden scutoid layers of scutoid_layers.py: every corner of every cell solved exactly from three of its planes,
# every cell checked against all its half-spaces exactly, its faces counted exactly, and the cell volumes summed exactly against the layer.
import json, itertools, numpy as np, sys
sys.path.insert(0, '/home/dicto/kaleidohedra/papers/intro-solids/scripts')
from fractions import Fraction as Fr
exec(open('/home/dicto/kaleidohedra/papers/intro-solids/scripts/hull_family_exact.py').read().split("def member(")[0])
from scipy.spatial import ConvexHull
# the 32 directions exactly (unnormalised: the 12 icosahedron corners and the 20 dodecahedron corners in dual position)
P5 = ICO; D3 = DOD
diag = [abs(v[0].f()) == abs(v[1].f()) == abs(v[2].f()) for v in D3]
N = P5 + [v for v, g in zip(D3, diag) if g] + [v for v, g in zip(D3, diag) if not g]; GROUP = ['P'] * 12 + ['Hd'] * 8 + ['Ho'] * 12
# the truncated icosahedron of edge 2 (corners (0, ±1, ±3φ) …): its face distances along these (unnormalised) directions
TI = []
for b in ([Q(0), Q(1), 3 * phi], [Q(1), 2 + phi, 2 * phi], [phi, Q(2), phi * phi * phi]):
    for c in cyc(b):
        for s in itertools.product((1, -1), repeat=3): TI.append([c[k] * s[k] for k in range(3)])
uniq = {tuple(v): v for v in TI}; TI = list(uniq.values()); assert len(TI) == 60
dmax = lambda n: max((dot(n, v) for v in TI), key=lambda q: q.f())
dA = [dmax(n) for n in N]
dB = [phi * (dA[i] if GROUP[i] != 'Ho' else dA[i] * 2 / phi) for i in range(32)]
dA2 = [phi * phi * d for d in dA]
def solve(p1, p2, p3):
    (a, da), (b, db), (c, dc) = p1, p2, p3; det = dot(a, cross(b, c))
    if det == 0: return None
    return [(cross(b, c)[k] * da + cross(c, a)[k] * db + cross(a, b)[k] * dc) / det for k in range(3)]
def cell_exact(i, d0, d1):
    D = [d1[j] - d0[j] for j in range(32)]
    H = [(N[i], d1[i]), ([-x for x in N[i]], -d0[i])]
    for j in range(32):
        if j != i: r = D[j] / D[i]; H.append(([N[j][k] - r * N[i][k] for k in range(3)], d0[j] - r * d0[i]))
    Hf = np.array([[x.f() for x in n] + [-d.f()] for n, d in H])
    from scipy.spatial import HalfspaceIntersection
    x0 = None
    for t in np.linspace(0.3, 0.7, 9):
        x = np.array([v.f() for v in N[i]]) * ((d0[i] + Q(Fr(int(t * 100), 100)) * D[i]).f() / dot(N[i], N[i]).f())
        if (Hf[:, :3] @ x + Hf[:, 3] < -1e-9).all(): x0 = x; break
    Vf = np.unique(np.round(HalfspaceIntersection(Hf, x0).intersections, 9), axis=0)
    V = []
    for v in Vf:
        act = [k for k in range(len(H)) if abs(Hf[k, :3] @ v + Hf[k, 3]) < 1e-7]
        for a, b, c in itertools.combinations(act, 3):
            x = solve(H[a], H[b], H[c])
            if x is not None: break
        assert all((dot(n, x) - d).sgn() <= 0 for n, d in H), 'corner outside a half-space'
        V.append(x)
    # volume: exact, by a fan of tetrahedra from the first corner over the hull's triangles (hull from floats, corners exact)
    h = ConvexHull(np.array([[x.f() for x in v] for v in V])); vol = Q(0)
    for s in h.simplices:
        a, b, c = (V[k] for k in s); t = dot(sub(a, V[0]), cross(sub(b, V[0]), sub(c, V[0])))
        vol = vol + (t if t.sgn() > 0 else -t)
    vol = vol / 6
    inner = sum(1 for v in V if dot(N[i], v) == d0[i]); outer = sum(1 for v in V if dot(N[i], v) == d1[i])
    return dict(group=GROUP[i], inner=inner, outer=outer, free=len(V) - inner - outer, corners=len(V)), vol
def cage_vol(d):
    from scipy.spatial import HalfspaceIntersection
    Hf = np.array([[x.f() for x in n] + [-dd.f()] for n, dd in zip(N, d)])
    Vf = np.unique(np.round(HalfspaceIntersection(Hf, np.zeros(3)).intersections, 9), axis=0); V = []
    for v in Vf:
        act = [k for k in range(32) if abs(Hf[k, :3] @ v + Hf[k, 3]) < 1e-7]
        for a, b, c in itertools.combinations(act, 3):
            x = solve((N[a], d[a]), (N[b], d[b]), (N[c], d[c]))
            if x is not None: break
        V.append(x)
    h = ConvexHull(np.array([[x.f() for x in v] for v in V])); vol = Q(0)
    for s in h.simplices:
        a, b, c = (V[k] for k in s); t = dot(a, cross(b, c)); vol = vol + (t if t.sgn() > 0 else -t)
    return vol / 6
out = ['DICTO · dictospheres.com', 'Golden scutoid layers, exact (Q(√5)): corners solved exactly, half-spaces checked exactly, volumes exact']
for name, d0, d1 in (('layer 1: A -> B', dA, dB), ('layer 2: B -> φ²A', dB, dA2)):
    tot = Q(0); kinds = {}
    for i in range(32):
        k, v = cell_exact(i, d0, d1); tot = tot + v; kinds.setdefault(tuple(k.values()), []).append(v)
    layer = cage_vol(d1) - cage_vol(d0)
    out.append(f'{name}: cells {tot} = layer {layer}: {tot == layer}')
    for k, vs in sorted(kinds.items()):
        out.append(f'   {k[0]}: {len(vs)} cells, inner {k[1]}-gon, outer {k[2]}-gon, {k[3]} Y-corner(s), {k[4]} corners; all congruent volume: {len(set(vs)) == 1} ({vs[0]})')
print('\n'.join(out)); open('/home/dicto/kaleidohedra/studies/2026-10-17-scutoids/data/scutoid-exact.txt', 'w').write('\n'.join(out) + '\n')
