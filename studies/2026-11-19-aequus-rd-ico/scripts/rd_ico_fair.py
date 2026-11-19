# Two-depth line RD ∩ icosahedron under the pyritohedral group Th: faces
# RD (12, at 1), icosahedron's 8 cube-diagonal faces (at m1), its 12 other faces (at m2).
# Seek (m1, m2) with every face subtending solid angle 4π/32 (solid-angle model, as in Equanimity).
# Solid angle of a face: fan of triangles from the origin, Van Oosterom–Strackee (1983).
import itertools, numpy as np
from scipy.spatial import HalfspaceIntersection, ConvexHull
from scipy.optimize import fsolve
phi = (1 + 5 ** .5) / 2
def u(v): v = np.array(v, float); return v / np.linalg.norm(v)
RD = [u(p) for p in {tuple(np.roll(q, k)) for q in [(a, b, 0) for a in (1, -1) for b in (1, -1)] for k in range(3)}]
I8 = [u(p) for p in itertools.product((1, -1), repeat=3)]
I12 = [u(p) for p in {tuple(np.roll((0, a / phi, b * phi), k)) for a in (1, -1) for b in (1, -1) for k in range(3)}]
assert (len(RD), len(I8), len(I12)) == (12, 8, 12)
FAM = [RD, I8, I12]
def tri(a, b, c):
    num = abs(np.dot(a, np.cross(b, c)))
    den = 1 + np.dot(a, b) + np.dot(b, c) + np.dot(c, a)   # unit vectors
    return 2 * np.arctan2(num, den)
def angles(m1, m2):
    N = RD + I8 + I12; d = [1] * 12 + [m1] * 8 + [m2] * 12
    H = np.array([list(n) + [-di] for n, di in zip(N, d)])
    V = HalfspaceIntersection(H, np.zeros(3)).intersections
    out = []
    for n, di in zip(N, d):
        P = V[np.abs(V @ n - di) < 1e-9]
        if len(P) < 3: out.append(0.0); continue
        c = P.mean(0); e1 = u(P[0] - c); e2 = np.cross(n, e1)
        P = P[np.argsort(np.arctan2((P - c) @ e2, (P - c) @ e1))]
        out.append(sum(tri(u(c), u(P[i]), u(P[(i + 1) % len(P)])) for i in range(len(P))))
    out = np.array(out); return out[:12], out[12:20], out[20:]
T = 4 * np.pi / 32
def F(x):
    a, b, c = angles(*x); return [b.mean() - T, c.mean() - T]
best = []
for m1 in np.linspace(0.8, 1.3, 11):
    for m2 in np.linspace(0.8, 1.3, 11):
        try:
            s, info, ier, msg = fsolve(F, [m1, m2], full_output=True)
            if ier != 1: continue
            a, b, c = angles(*s)
            if min(a.min(), b.min(), c.min()) <= 0: continue
            r = max(abs(a - T).max(), abs(b - T).max(), abs(c - T).max())
            if r < 1e-9 and not any(np.allclose(s, q, atol=1e-7) for q, _ in best): best.append((s, r))
        except Exception: pass
print('solutions (m1 = 8 cube-diagonal faces, m2 = 12 other icosahedron faces; RD at 1):')
for s, r in best:
    a, b, c = angles(*s)
    print('  m1 = %.12f  m2 = %.12f  max |Ω - 4π/32| = %.1e  faces present 12/8/12: %s' % (s[0], s[1], r, (a > 0).sum() == 12 and (b > 0).sum() == 8 and (c > 0).sum() == 12))
# controls: Equanimity's one-parameter claim: m1 = m2 = μ cannot make all three equal
from scipy.optimize import brentq
g = lambda mu: angles(mu, mu)[1].mean() - angles(mu, mu)[2].mean()
print('control: one depth μ, I8 minus I12 share at μ = 0.9, 1.0, 1.1:', ['%.4f' % g(m) for m in (0.9, 1.0, 1.1)])
print('FINAL ok' if best else 'FINAL none found')
