# Bundle A of the two thin layers (DICTO 2026-10-17: "A, shorter and fatter"), exact in Q(√5). Core: truncated icosahedron A (edge 2).
# Layer 1 A -> M, M = 11/10·(dP, dHd, 8/7·dHo): pentagon cells 5 -> 6, paired-hexagon cells 6 -> 5.
# Layer 2 M -> B, B = 77/60·(dP, dHd, 21/20·dHo): the swap back. Closing layer B -> RD, the RD 23/20 of the tightest around B.
# Every corner solved exactly from three planes and checked inside all its half-spaces; cell volumes summed exactly per layer against
# the shell volumes; scutoids counted exactly; congruence classes by exact volume. -> data/scutoid-two-exact.txt
import itertools, numpy as np
exec(open('scripts/scutoid_exact.py').read().split("def cell_exact(")[0])
from scipy.spatial import HalfspaceIntersection, ConvexHull
RDN = [[Q(a), Q(b), Q(0)] for a in (1, -1) for b in (1, -1)] + [[Q(a), Q(0), Q(b)] for a in (1, -1) for b in (1, -1)] + [[Q(0), Q(a), Q(b)] for a in (1, -1) for b in (1, -1)]
NR = N + RDN; GR = GROUP + ['RD'] * 12
fl = lambda v: np.array([x.f() for x in v])
def exact_corners(H, x0):
    Hf = np.array([list(fl(n)) + [-d.f()] for n, d in H]); V = []
    for v in np.unique(np.round(HalfspaceIntersection(Hf, x0).intersections, 9), axis=0):
        act = [m for m in range(len(H)) if abs(Hf[m, :3] @ v + Hf[m, 3]) < 1e-7]
        for a, b, c in itertools.combinations(act, 3):
            x = solve(H[a], H[b], H[c])
            if x is not None: break
        assert all((dot(n, x) - d).sgn() <= 0 for n, d in H), 'corner outside a half-space'
        V.append(x)
    return V
def vol(V, apex=None):
    h = ConvexHull(np.array([fl(v) for v in V])); o = V[0]; t = Q(0)
    for s in h.simplices:
        a, b, c = (V[m] for m in s); w = dot(sub(a, o), cross(sub(b, o), sub(c, o))); t = t + (w if w.sgn() > 0 else -w)
    return t / 6
def cell(NL, i, d0, d1):
    m = len(NL); D = [d1[j] - d0[j] for j in range(m)]
    H = [(NL[i], d1[i]), ([-x for x in NL[i]], -d0[i])]
    for j in range(m):
        if j != i: r = D[j] / D[i]; H.append(([NL[j][k] - r * NL[i][k] for k in range(3)], d0[j] - r * d0[i]))
    Hf = np.array([list(fl(n)) + [-d.f()] for n, d in H]); nf = fl(NL[i]); x0 = None
    for tt in np.linspace(0.03, 0.97, 33):
        for off in [np.zeros(3)] + list(np.eye(3) * 0.03) + list(-np.eye(3) * 0.03):
            x = nf * (d0[i].f() + tt * D[i].f()) / (nf @ nf) + off
            if (Hf[:, :3] @ x + Hf[:, 3] < -1e-9).all(): x0 = x; break
        if x0 is not None: break
    assert x0 is not None, f'cell {i} empty'
    V = exact_corners(H, x0)
    inn = sum(1 for v in V if dot(NL[i], v) == d0[i]); out = sum(1 for v in V if dot(NL[i], v) == d1[i])
    return (GR[i], inn, out, len(V) - inn - out, len(V)), vol(V)
def shell(NL, d): return exact_corners([(n, x) for n, x in zip(NL, d)], np.zeros(3))
a1, k1, a2, k2 = Q(Fr(11, 10)), Q(Fr(8, 7)), Q(Fr(7, 6)), Q(Fr(21, 20))
dM = [dA[i] * (a1 * k1 if GROUP[i] == 'Ho' else a1) for i in range(32)]
dB = [dA[i] * (a1 * a2 * k2 if GROUP[i] == 'Ho' else a1 * a2) for i in range(32)]
VB = shell(N, dB)
supB = lambda n: max((dot(n, v) for v in VB), key=lambda x: x.f())
r = max((supB(n) for n in RDN), key=lambda x: x.f()) * Fr(23, 20)
RDV = [[Q(s) * r, Q(0), Q(0)] for s in (1, -1)] + [[Q(0), Q(s) * r, Q(0)] for s in (1, -1)] + [[Q(0), Q(0), Q(s) * r] for s in (1, -1)] + \
      [[Q(a) * r / 2, Q(b) * r / 2, Q(c) * r / 2] for a in (1, -1) for b in (1, -1) for c in (1, -1)]
supRD = lambda n: max((dot(n, v) for v in RDV), key=lambda x: x.f())
vA, vM, vB, vR = vol(TI), vol(shell(N, dM)), vol(VB), 2 * r * r * r
out = ['DICTO · dictospheres.com', 'Two thin scutoid layers in the whole rhombic dodecahedron (bundle A), exact in Q(√5)',
       f'  M = 11/10·(dP, dHd, 8/7·dHo); B = 77/60·(dP, dHd, 21/20·dHo); RD corners on the axes at r = {r}']
want = {'layer 1': {'P': (5, 6), 'Ho': (6, 5)}, 'layer 2': {'P': (6, 5), 'Ho': (5, 6)}}
grand = Q(0); nsc = {}
for name, NL, d0, d1, idx, target in (('layer 1', N, dA, dM, range(32), vM - vA), ('layer 2', N, dM, dB, range(32), vB - vM),
                                       ('closing', NR, list(dB) + [supB(n) for n in RDN], [supRD(n) for n in N] + [r] * 12, range(44), vR - vB)):
    tot = Q(0); kinds = {}
    for i in idx:
        key, v = cell(NL, i, d0, d1); kinds.setdefault(key, []).append(v); tot = tot + v
    grand = grand + tot
    out.append(f'{name}: {sum(len(x) for x in kinds.values())} cells, volumes sum exactly to the shell between: {tot == target}')
    for key, vs in sorted(kinds.items()):
        g, inn, o, free, nc = key; sc = name in want and want[name].get(g) == (inn, o) and free > 0
        nsc[name] = nsc.get(name, 0) + (len(vs) if sc else 0)
        out.append(f'    {g}: {len(vs)} cells, inner {inn}, outer {o}, free corners {free}, corners {nc}; volume classes {len(set(vs))}' + ('  SCUTOID' if sc else ''))
out.append(f'scutoids: layer 1 {nsc.get("layer 1", 0)}, layer 2 {nsc.get("layer 2", 0)}; all cells = RD − core exactly: {grand == vR - vA}')
out.append(f'core share {vA.f() / vR.f():.4f}; the RD tiles space on the fcc lattice, so the bundle does')
print('\n'.join(out)); open('data/scutoid-two-exact.txt', 'w').write('\n'.join(out) + '\n')
