"""Are the three permutahedra (uniform truncated octahedron, truncated cuboctahedron, truncated icosidodecahedron) fair dice?
By Theorem 2 this asks whether their polars, the face-transitive Aequi Nos. 1233-1235, have equal curvature at every corner.
Solid angles of the faces seen from the centre, in ball arithmetic (python-flint arb); combinatorics from a floating hull.
FINAL ok when every face kind is certified distinct from 4*pi/N and the kinds add to 4*pi."""
import itertools, numpy as np
from scipy.spatial import ConvexHull
from flint import arb, ctx
ctx.prec = 200
S2, S5 = arb(2).sqrt(), arb(5).sqrt(); PH = (1 + S5) / 2
def perms_signs(t, even_only=False):
    out = {}
    P = [(0, 1, 2), (1, 2, 0), (2, 0, 1)] + ([] if even_only else [(0, 2, 1), (2, 1, 0), (1, 0, 2)])
    t = [x if isinstance(x, arb) else arb(x) for x in t]
    for p in P:
        for s in itertools.product((1, -1), repeat=3):
            v = tuple(s[i] * t[p[i]] for i in range(3)); out[tuple(round(float(x.mid()), 9) + 0.0 for x in v)] = v
    return list(out.values())
def solid(poly):
    """poly: arb vectors of a convex face in cyclic order; fan of Van Oosterom-Strackee triangles (vectors need not be unit)"""
    def n(v): return (v[0] * v[0] + v[1] * v[1] + v[2] * v[2]).sqrt()
    def d(a, b): return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
    def c(a, b): return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
    a = poly[0]; s = arb(0)
    for i in range(1, len(poly) - 1):
        b, cc = poly[i], poly[i + 1]; la, lb, lc = n(a), n(b), n(cc)
        s += 2 * arb.atan2(abs(d(a, c(b, cc))), la * lb * lc + d(a, b) * lc + d(a, cc) * lb + d(b, cc) * la)
    return s
def run(name, Varb, Nexp):
    Vf = np.array([[float(x.mid()) for x in v] for v in Varb]); H = ConvexHull(Vf)
    planes = {}
    for eq, sim in zip(H.equations, H.simplices):
        planes.setdefault(tuple(np.round(eq, 9)), set()).update(sim.tolist())
    kinds = {}
    for eq, idx in planes.items():
        idx = list(idx); n = np.array(eq[:3]); cen = Vf[idx].mean(0)
        e1 = Vf[idx[0]] - cen; e1 /= np.linalg.norm(e1); e2 = np.cross(n, e1)
        idx.sort(key=lambda i: np.arctan2((Vf[i] - cen) @ e2, (Vf[i] - cen) @ e1))
        kinds.setdefault(len(idx), []).append(solid([Varb[i] for i in idx]))
    N = len(planes); assert N == Nexp, (name, N)
    tot = sum((x for L in kinds.values() for x in L), arb(0)); four = 4 * arb.pi(); tgt = four / N
    ok = tot.overlaps(four)
    rep = {}
    for k, L in sorted(kinds.items()):
        ok &= all(x.overlaps(L[0]) for x in L) and not L[0].overlaps(tgt)
        rep[k] = (len(L), L[0].str(12, radius=False))
    print(name, 'faces', N, 'kinds (sides: count, solid angle)', rep, '4pi/N =', tgt.str(12, radius=False), 'ok' if ok else 'FAIL')
    return ok
ok = run('truncated octahedron', perms_signs((0, 1, 2)), 14)
ok &= run('truncated cuboctahedron', perms_signs((arb(1), 1 + S2, 1 + 2 * S2)), 26)
ip = 1 / PH
TID = perms_signs((ip, ip, 3 + PH), True) + perms_signs((2 * ip, PH, 1 + 2 * PH), True) + perms_signs((ip, PH * PH, 3 * PH - 1), True) + \
      perms_signs((2 * PH - 1, arb(2), 2 + PH), True) + perms_signs((PH, arb(3), 2 * PH), True)
ok &= run('truncated icosidodecahedron', TID, 62)
if ok: print('FINAL ok')
