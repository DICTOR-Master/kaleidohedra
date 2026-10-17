# The group as a space-filler (DICTO: "maybe as a group that forms a space-filling shape"): the core truncated icosahedron A, the scutoid
# layer A -> B, and a closing layer from B to a truncated octahedron T (squares on the coordinate axes, where the flips happen; hexagons on
# the cube diagonals, the Hd planes). The sweep runs over 38 planes: the 32 cage planes (in T they only touch it: their d1 is T's support)
# and the 6 square planes (in B they only touch it: d0 is B's support). T tiles space on the bcc lattice, so the whole bundle does. Exact.
import itertools, numpy as np
exec(open('/home/dicto/kaleidohedra/studies/2026-10-17-scutoids/scripts/scutoid_exact.py').read().split("out = ['DICTO")[0])
from scipy.spatial import HalfspaceIntersection, ConvexHull
SQ = [[Q(1), Q(0), Q(0)], [Q(-1), Q(0), Q(0)], [Q(0), Q(1), Q(0)], [Q(0), Q(-1), Q(0)], [Q(0), Q(0), Q(1)], [Q(0), Q(0), Q(-1)]]
NN = N + SQ; GG = GROUP + ['Sq'] * 6
def corners(planes):
    Hf = np.array([[x.f() for x in n] + [-d.f()] for n, d in planes])
    Vf = np.unique(np.round(HalfspaceIntersection(Hf, np.zeros(3)).intersections, 9), axis=0); V = []
    for v in Vf:
        act = [k for k in range(len(planes)) if abs(Hf[k, :3] @ v + Hf[k, 3]) < 1e-7]
        for a, b, c in itertools.combinations(act, 3):
            x = solve(planes[a], planes[b], planes[c])
            if x is not None: break
        V.append(x)
    return V
VB = corners(list(zip(N, dB)))
supB = lambda n: max((dot(n, v) for v in VB), key=lambda q: q.f())
# T = t × the truncated octahedron with corners (0, ±1, ±2) (permutations): squares at 2t, hexagons ((±1,±1,±1)·x) at 3t. Smallest golden-friendly t
hx = supB(SQ[0]); hd = max((dB[i] for i in range(32) if GROUP[i] == 'Hd'), key=lambda q: q.f())
t = Q(int(max(hx.f() / 2, hd.f() / 3) * 4) + 1, 0) / 4
TOV = []
for p in itertools.permutations([0, 1, 2]):
    for s in itertools.product((1, -1), repeat=3):
        v = [Q(s[k] * [0, 1, 2][p[k]]) * t for k in range(3)]
        if v not in TOV: TOV.append(v)
supT = lambda n: max((dot(n, v) for v in TOV), key=lambda q: q.f())
d0 = list(dB) + [supB(n) for n in SQ]
d1 = [supT(n) for n in N] + [2 * t] * 6
assert all((d1[j] - d0[j]).sgn() > 0 for j in range(38)), 'a plane does not move outward'
def cell38(i):
    D = [d1[j] - d0[j] for j in range(38)]
    H = [(NN[i], d1[i]), ([-x for x in NN[i]], -d0[i])]
    for j in range(38):
        if j != i: r = D[j] / D[i]; H.append(([NN[j][k] - r * NN[i][k] for k in range(3)], d0[j] - r * d0[i]))
    Hf = np.array([[x.f() for x in n] + [-d.f()] for n, d in H])
    # interior point: search along the face normal and around it
    nf = np.array([x.f() for x in NN[i]]); nn = nf @ nf; x0 = None
    for tt in np.linspace(0.05, 0.95, 37):
        for off in [np.zeros(3)] + [o * 0.05 for o in np.eye(3)] + [-o * 0.05 for o in np.eye(3)]:
            x = nf * (d0[i].f() + tt * D[i].f()) / nn + off
            if (Hf[:, :3] @ x + Hf[:, 3] < -1e-9).all(): x0 = x; break
        if x0 is not None: break
    if x0 is None: return None, Q(0)
    try: Vf = np.unique(np.round(HalfspaceIntersection(Hf, x0).intersections, 9), axis=0)
    except Exception: return None, Q(0)
    V = []
    for v in Vf:
        act = [k for k in range(len(H)) if abs(Hf[k, :3] @ v + Hf[k, 3]) < 1e-7]
        for a, b, c in itertools.combinations(act, 3):
            x = solve(H[a], H[b], H[c])
            if x is not None: break
        assert all((dot(n, x) - d).sgn() <= 0 for n, d in H)
        V.append(x)
    h = ConvexHull(np.array([[x.f() for x in v] for v in V])); vol = Q(0)
    for s in h.simplices:
        a, b, c = (V[k] for k in s); tt_ = dot(sub(a, V[0]), cross(sub(b, V[0]), sub(c, V[0]))); vol = vol + (tt_ if tt_.sgn() > 0 else -tt_)
    inner = sum(1 for v in V if dot(NN[i], v) == d0[i]); outer = sum(1 for v in V if dot(NN[i], v) == d1[i])
    return dict(group=GG[i], inner=inner, outer=outer, free=len(V) - inner - outer, corners=len(V)), vol / 6
out = ['DICTO · dictospheres.com', f'The scutoid bundle closed in a truncated octahedron T = {t} × (0, ±1, ±2) (exact)']
tot = Q(0); kinds = {}; missing = 0
for i in range(38):
    k, v = cell38(i)
    if k is None: missing += 1; continue
    tot = tot + v; kinds.setdefault(tuple(k.values()), []).append(v)
volT = Q(0); h = ConvexHull(np.array([[x.f() for x in v] for v in TOV]))
for s in h.simplices:
    a, b, c = (TOV[k] for k in s); tt_ = dot(a, cross(b, c)); volT = volT + (tt_ if tt_.sgn() > 0 else -tt_)
volT = volT / 6; layer = volT - cage_vol(dB)
out.append(f'closing layer B -> T: cells {tot} = T − B {layer}: {tot == layer}; cells with no volume: {missing}')
for k, vs in sorted(kinds.items()): out.append(f'   {k[0]}: {len(vs)} cells, inner {k[1]}-gon, outer {k[2]}-gon, {k[3]} free corner(s), {k[4]} corners; congruent: {len(set(vs)) == 1}')
out.append(f'the bundle (core A, scutoid layer A -> B, closing layer B -> T) = T, which tiles space on the bcc lattice (translations t·(4,0,0)-type and t·(2,2,2)-type)')
print('\n'.join(out)); open('/home/dicto/kaleidohedra/studies/2026-10-17-scutoids/data/scutoid-close.txt', 'w').write('\n'.join(out) + '\n')
