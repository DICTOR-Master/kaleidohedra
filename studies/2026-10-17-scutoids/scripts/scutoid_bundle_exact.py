# The compact scutoid bundle (late squares), exact in Q(√5): core truncated icosahedron A (edge 2); scutoid layer A -> B over 38 planes,
# the 6 square planes starting at (1 + q) × A's axis support; B = T minus its 24 corners (its Hd and square faces are T's); closing corner
# cells B -> T; T = t·(0, ±1, ±2), t = s × A's diagonal-hexagon distance / 3. Pinned point: s = 27/20, p = 13/20, k = 33/25, q = 1/50.
# Checks: every corner solved exactly and inside all its half-spaces; cell volumes sum to vol T − vol A exactly; the scutoids (inner and
# outer face sides differ, a free corner); congruence classes by exact volume. -> data/scutoid-bundle-exact.txt
import itertools, numpy as np
exec(open('/home/dicto/kaleidohedra/studies/2026-10-17-scutoids/scripts/scutoid_exact.py').read().split("out = ['DICTO")[0])
from scipy.spatial import HalfspaceIntersection, ConvexHull
s, p, k, q = Q(Fr(27, 20)), Q(Fr(13, 20)), Q(Fr(33, 25)), Q(Fr(1, 50))
SQ = [[Q(1), Q(0), Q(0)], [Q(-1), Q(0), Q(0)], [Q(0), Q(1), Q(0)], [Q(0), Q(-1), Q(0)], [Q(0), Q(0), Q(1)], [Q(0), Q(0), Q(-1)]]
NN = N + SQ; GG = GROUP + ['Sq'] * 6
supA = lambda n: max((dot(n, v) for v in TI), key=lambda x: x.f())
dHd = max((dA[i] for i in range(32) if GROUP[i] == 'Hd'), key=lambda x: x.f())
t = s * dHd / 3
TOV = []
for pm in itertools.permutations([0, 1, 2]):
    for sg in itertools.product((1, -1), repeat=3):
        v = [Q(sg[j] * [0, 1, 2][pm[j]]) * t for j in range(3)]
        if v not in TOV: TOV.append(v)
supT = lambda n: max((dot(n, v) for v in TOV), key=lambda x: x.f())
d0 = list(dA) + [supA(n) * (1 + q) for n in SQ]
dB = []
for i, g in enumerate(GROUP):
    if g == 'Hd': dB.append(3 * t)
    elif g == 'P': dB.append(dA[i] + p * (supT(N[i]) - dA[i]))
    else: dB.append(min(dA[i] * k * s, supT(N[i]), key=lambda x: x.f()))   # past T's corner: the plane only touches T (no corner cell)
dB += [2 * t] * 6
assert all((dB[j] - d0[j]).sgn() > 0 for j in range(38)), 'a plane does not move out'
assert all((dB[i] - supT(N[i])).sgn() < 0 for i in range(32) if GROUP[i] == 'P'), 'a pentagon plane misses T'
d1c = [supT(N[i]) if GROUP[i] in ('P', 'Ho') else dB[i] for i in range(32)] + dB[32:]
def cell(i, a0, a1):
    D = [a1[j] - a0[j] for j in range(38)]
    H = [(NN[i], a1[i]), ([-x for x in NN[i]], -a0[i])]
    for j in range(38):
        if j != i: r = D[j] / D[i]; H.append(([NN[j][m] - r * NN[i][m] for m in range(3)], a0[j] - r * a0[i]))
    Hf = np.array([[x.f() for x in n] + [-d.f()] for n, d in H]); nf = np.array([x.f() for x in NN[i]]); nn = nf @ nf; x0 = None
    for tt in np.linspace(0.03, 0.97, 33):
        for off in [np.zeros(3)] + list(np.eye(3) * 0.03) + list(-np.eye(3) * 0.03):
            x = nf * (a0[i].f() + tt * D[i].f()) / nn + off
            if (Hf[:, :3] @ x + Hf[:, 3] < -1e-9).all(): x0 = x; break
        if x0 is not None: break
    if x0 is None: return None
    Vf = np.unique(np.round(HalfspaceIntersection(Hf, x0).intersections, 9), axis=0); V = []
    for v in Vf:
        act = [m for m in range(len(H)) if abs(Hf[m, :3] @ v + Hf[m, 3]) < 1e-7]
        for a, b, c in itertools.combinations(act, 3):
            x = solve(H[a], H[b], H[c])
            if x is not None: break
        assert all((dot(n, x) - d).sgn() <= 0 for n, d in H), 'corner outside'
        V.append(x)
    h = ConvexHull(np.array([[x.f() for x in v] for v in V])); vol = Q(0)
    for sp in h.simplices:
        a, b, c = (V[m] for m in sp); w = dot(sub(a, V[0]), cross(sub(b, V[0]), sub(c, V[0]))); vol = vol + (w if w.sgn() > 0 else -w)
    inn = sum(1 for v in V if dot(NN[i], v) == a0[i]); out = sum(1 for v in V if dot(NN[i], v) == a1[i])
    return (GG[i], inn, out, len(V) - inn - out, len(V)), vol / 6
def vol_of(V):
    h = ConvexHull(np.array([[x.f() for x in v] for v in V])); vol = Q(0)
    for sp in h.simplices:
        a, b, c = (V[m] for m in sp); w = dot(a, cross(b, c)); vol = vol + (w if w.sgn() > 0 else -w)
    return vol / 6
out = ['DICTO · dictospheres.com', f'The compact scutoid bundle, exact (Q(√5)): s = 27/20, p = 13/20, k = 33/25, q = 1/50; T = {t} × (0, ±1, ±2)']
tot = Q(0); kinds = {}
for i in range(38):
    c = cell(i, d0, dB)
    if c: kinds.setdefault(('layer',) + c[0], []).append(c[1]); tot = tot + c[1]
for i in range(32):
    if GROUP[i] in ('P', 'Ho') and (d1c[i] - dB[i]).sgn() > 0:
        c = cell(i, dB, d1c)
        if c: kinds.setdefault(('close',) + c[0], []).append(c[1]); tot = tot + c[1]
vT = vol_of(TOV); vA = vol_of(TI)
out.append(f'all cells {tot} = vol T − vol A {vT - vA}: {tot == vT - vA}')
nsc = 0
for key, vs in sorted(kinds.items()):
    tag = key[0]; g, inn, outn, free, nc = key[1:]
    sc = tag == 'layer' and inn > 2 and outn > 2 and inn != outn and free > 0; nsc += len(vs) if sc else 0
    out.append(f'  {tag} {g}: {len(vs)} cells, inner {inn}, outer {outn}, free corners {free}, corners {nc}; volume classes {len(set(vs))}' + ('  SCUTOID' if sc else ''))
out.append(f'scutoids: {nsc}; the bundle T tiles space on the bcc lattice')
print('\n'.join(out)); open('/home/dicto/kaleidohedra/studies/2026-10-17-scutoids/data/scutoid-bundle-exact.txt', 'w').write('\n'.join(out) + '\n')
