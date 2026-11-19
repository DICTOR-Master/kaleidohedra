# More Aequi? Fair dice with three face families (two free depths), from the axis orbits of the cube and icosahedron frames.
# Orbits: Oh: C6, O8, RD12. Ih: D12, I20, RT30. Th (pyritohedral, shared): C6, O8, RD12, D12, I12 (= I20 less O8), RT24 (= RT30 less C6).
# For each set of three orbits (one at depth 1, two free depths), seek depths where all faces subtend 4π/N (solid-angle model,
# Van Oosterom–Strackee), all faces present. Grid of starts, fsolve. Double precision pilot.
import itertools, numpy as np, sys
from scipy.spatial import HalfspaceIntersection
from scipy.optimize import fsolve
phi = (1 + 5 ** .5) / 2
def u(v): v = np.array(v, float); return v / np.linalg.norm(v)
def cyc(base): return [u(p) for p in {tuple(np.roll(np.array(q, float), k)) for q in base for k in range(3)}]
def signs(t):
    out = set()
    for s in itertools.product((1, -1), repeat=3): out.add(tuple(a * b for a, b in zip(s, t)))
    return list(out)
C6 = cyc(signs((1, 0, 0))); O8 = [u(p) for p in itertools.product((1, -1), repeat=3)]
RD12 = cyc(signs((1, 1, 0))); D12 = cyc(signs((0, 1, phi))); I12 = cyc(signs((0, 1 / phi, phi)))
RT24 = cyc(signs((1, phi, 1 / phi)))
def dedup(L):
    out = []
    for v in L:
        if not any(np.allclose(v, w) for w in out): out.append(v)
    return out
ORB = {k: dedup(v) for k, v in dict(C6=C6, O8=O8, RD12=RD12, D12=D12, I12=I12, RT24=RT24).items()}
assert [len(v) for v in ORB.values()] == [6, 8, 12, 12, 12, 24], [len(v) for v in ORB.values()]
def tri(a, b, c): return 2 * np.arctan2(abs(np.dot(a, np.cross(b, c))), 1 + a @ b + b @ c + c @ a)
def omegas(fams, d):
    N = [n for f in fams for n in ORB[f]]; D = [di for f, di in zip(fams, d) for _ in ORB[f]]
    H = np.array([list(n) + [-x] for n, x in zip(N, D)]); V = HalfspaceIntersection(H, np.zeros(3)).intersections
    res = []
    for f, di in zip(fams, d):
        om = []
        for n in ORB[f]:
            P = V[np.abs(V @ n - di) < 1e-9]
            if len(P) < 3: om.append(0.0); continue
            c = P.mean(0); e1 = u(P[0] - c); e2 = np.cross(n, e1)
            P = P[np.argsort(np.arctan2((P - c) @ e2, (P - c) @ e1))]
            om.append(sum(tri(u(c), u(P[i]), u(P[(i + 1) % len(P)])) for i in range(len(P))))
        res.append(np.array(om))
    return res
found = []
for fams in itertools.combinations(ORB, 3):
    N = sum(len(ORB[f]) for f in fams); T = 4 * np.pi / N
    sols = []
    for x0 in itertools.product(np.linspace(0.7, 1.8, 9), repeat=2):
        try:
            F = lambda x: [omegas(fams, [1, *x])[1].mean() - T, omegas(fams, [1, *x])[2].mean() - T]
            s, info, ier, msg = fsolve(F, x0, full_output=True)
            if ier != 1: continue
            om = omegas(fams, [1, *s])
            if min(o.min() for o in om) <= 1e-9: continue
            r = max(abs(o - T).max() for o in om)
            if r < 1e-9 and not any(np.allclose(s, q, atol=1e-6) for q in sols): sols.append(s)
        except Exception: pass
    print('%-16s N=%2d  fair solutions: %s' % ('+'.join(fams), N, ['(%.9f, %.9f)' % tuple(s) for s in sols] or 'none'), flush=True)
    found += [(fams, N, s) for s in sols]
print('total', len(found)); print('FINAL ok')
