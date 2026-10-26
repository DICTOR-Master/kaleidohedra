# Lotus Jewel Axes stops (DICTO 2026-10-27, closing the [CHECK]): the Lotus Jewel Axes is the Icosaxes minus 8 Tricap dents, so it
# touches no earlier than the Icosaxes; it touches at the same d (and its windows close at the same d) exactly when the meeting points
# of the Icosaxes lie outside the dents. Here: the meeting set at first touch (two neighbours) and the window-closing point on the
# five-fold axis, each tested against the Tricaps of the pieces that meet there.
import numpy as np, itertools, json
from scipy.spatial import HalfspaceIntersection, ConvexHull
from scipy.optimize import linprog
exec(open('twenty.py').read().split('def pieces(d)')[0])        # sites, rotations M, u; I0 = Icosaxes corners
PHI = (1 + 5 ** .5) / 2
SIGNS = [np.array(s, float) for s in itertools.product([1, -1], repeat=3)]
ICO = np.array([p for s in itertools.product([1, -1], repeat=2) for p in [(0, s[0] * .5, s[1] * PHI / 2), (s[0] * .5, s[1] * PHI / 2, 0), (s[1] * PHI / 2, 0, s[0] * .5)]])
def tricaps():   # tetrahedra: the icosahedron face facing s (its 3 corners nearest 10 s) + tip s/(2 phi)
    out = []
    for s in SIGNS:
        base = ICO[np.argsort(-(ICO @ s))[:3]]; out.append(np.vstack([base, s / (2 * PHI)]))
    return out
TRI = tricaps()
def in_tet(T, x, eps=1e-9):
    A = np.c_[T[1:] - T[0]].T; l = np.linalg.solve(A, x - T[0]); return l.min() > eps and l.sum() < 1 - eps
H = [(np.eye(3)[i] * sg, PHI / 2) for i in range(3) for sg in (1, -1)] + [(s, PHI ** 2 / 2) for s in SIGNS]
def halfspaces(M, c):   # piece turned by M at centre c: M n . (x - c) <= h
    return np.array([np.r_[M @ n, -(M @ n) @ c - h] for n, h in H])
S = list(sites.values()); touch = PHI ** 2 * 3 ** .5 / 2
A = S[0]; B = sorted(S[1:], key=lambda M: np.linalg.norm(M @ u - A @ u))[0]
# 1) first touch: the meeting set at d = touch (both pieces, closed) via LP: the points in both, extremes in many directions
hs = np.vstack([halfspaces(A, touch * (A @ u)), halfspaces(B, touch * (B @ u))])
pts = []
for dvec in np.random.default_rng(1).normal(size=(200, 3)):
    r = linprog(dvec, A_ub=hs[:, :3], b_ub=-hs[:, 3] + 1e-12, bounds=[(-5, 5)] * 3)
    if r.success: pts.append(r.x)
pts = np.unique(np.round(pts, 9), axis=0)
def local(M, c, x): return M.T @ (x - c)
bad = [x for x in pts for M in (A, B) if any(in_tet(T, local(M, touch * (M @ u), x)) for T in TRI)]
print(f'first touch: meeting set has {len(pts)} extreme points; inside a Tricap dent: {len(bad)}', 'meeting set spans', np.round(np.ptp(pts, 0), 6) if len(pts) else '')
# 2) windows: the point where the five-fold axis first meets a piece at d = phi sqrt3/2
ax = np.array([0, 1, PHI]); ax /= np.linalg.norm(ax); d = PHI * 3 ** .5 / 2; hit = []   # the window stop (exact.py)
for M in S:
    if (M @ u) @ ax < .5: continue
    h = halfspaces(M, d * (M @ u)); a_ = h[:, :3] @ ax; b_ = -h[:, 3]
    lo = max([b / a for a, b in zip(a_, b_) if a < -1e-12], default=-9); hi = min([b / a for a, b in zip(a_, b_) if a > 1e-12], default=9)
    flat = [b for a, b in zip(a_, b_) if abs(a) <= 1e-12]           # constraints parallel to the axis: need b >= 0
    slack = min(flat, default=1)
    if lo <= hi + 1e-9 and slack >= -1e-9:
        ts = np.linspace(lo, hi, 41); dent = sum(any(in_tet(T, local(M, d * (M @ u), t * ax)) for T in TRI) for t in ts)
        hit.append(dict(segment=(round(lo, 6), round(hi, 6)), flat_slack=round(slack, 12), points_in_dent=int(dent)))
    for f in (1.000001, 0.999999):                                    # just outside / just inside the stop
        hf = halfspaces(M, f * d * (M @ u)); af = hf[:, :3] @ ax; bf = -hf[:, 3]
        lo2 = max([b / a for a, b in zip(af, bf) if a < -1e-12], default=-9); hi2 = min([b / a for a, b in zip(af, bf) if a > 1e-12], default=9)
        ok = lo2 <= hi2 and min([b for a, b in zip(af, bf) if abs(a) <= 1e-12], default=1) >= 0
        print(f'  piece at d x {f}: axis meets it: {ok}')
    break
print('windows close: axis meets the piece at the stop:', hit)
