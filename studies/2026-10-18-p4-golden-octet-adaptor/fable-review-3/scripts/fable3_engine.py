# Fable review 3 (2026-10-18, OCD + W_OCD): the exact Q(sqrt5) polytope engine, copied unchanged from
# studies/2026-10-18-ocd-octet/fable-review/scripts/fable_exact.py lines 8-126 (via fable-review-2/scripts/fable2_engine.py).
# STUDY points at the octet study, whose data (step1-ocd-exact.json, step2-octet-frame.json) and q5.py it reads.
import sys, os, json, itertools, time, numpy as np
from fractions import Fraction as Fr
from scipy.spatial import ConvexHull, QhullError
HERE = os.path.dirname(os.path.abspath(__file__)); STUDY = os.path.join(HERE, "..", "..", "..", "2026-10-18-ocd-octet"); sys.path.insert(0, os.path.join(STUDY, "scripts"))
from q5 import q, qs_, qa, qs, qm, qn, qr, qd, qinv, qf, sgn, vadd, vsub, vmul, dot, cross, det3, PHI, ONE, Z, MARK
OUT = os.path.join(HERE, "..", "data"); os.makedirs(OUT, exist_ok=True)
loadS = lambda n: json.load(open(os.path.join(STUDY, 'data', n)))
f3 = lambda v: np.array([qf(x) for x in v], float)
qv = lambda v: [q(x) for x in v]
def qstr(x): return qs_(x) + f' ({qf(x):.9f})'
TOL_PRESCREEN = 1e-7

# ---------------------------------------------------------------- exact polytopes
def same_plane(p1, p2):
    (n1, d1), (n2, d2) = p1, p2
    if any(x != Z for x in cross(n1, n2)) or sgn(dot(n1, n2)) <= 0: return False
    return all(qm(d1, n2[i]) == qm(d2, n1[i]) for i in range(3))
def solve3(A, b):
    D = det3(*A)
    if D == Z: return None
    cols = lambda k: [[b[i] if j == k else A[i][j] for j in range(3)] for i in range(3)]
    return [qd(det3(*cols(k)), D) for k in range(3)]
def enumerate_corners(planes):
    """exact corners of {x : n.x <= d for all (n,d)}; empty list if empty or lower-dimensional"""
    m = len(planes)
    if m < 3: return []
    nf = np.array([f3(n) for n, d in planes]); df = np.array([qf(d) for n, d in planes]); nrm = np.linalg.norm(nf, axis=1)
    trip = np.array(list(itertools.combinations(range(m), 3)), int)
    cand = []
    for s in range(0, len(trip), 20000):
        T = trip[s:s + 20000]; A = nf[T]; b = df[T]
        det = np.linalg.det(A); scale = nrm[T].prod(1)
        ill = np.abs(det) < 1e-9 * scale
        X = np.zeros((len(T), 3))
        ok = ~ill
        if ok.any(): X[ok] = np.linalg.solve(A[ok], b[ok][..., None])[..., 0]
        viol = ((X @ nf.T) - df) / nrm
        keep = ill | (viol.max(1) <= TOL_PRESCREEN)
        cand += [tuple(t) for t in T[keep]]
    corners = []
    for i, j, k in cand:
        x = solve3([planes[i][0], planes[j][0], planes[k][0]], [planes[i][1], planes[j][1], planes[k][1]])
        if x is None: continue
        if all(sgn(qs(d, dot(n, x))) >= 0 for n, d in planes) and not any(all(a == b for a, b in zip(x, y)) for y in corners): corners.append(x)
    return corners
def exact_volume(corners):
    """exact volume of conv(corners); each qhull facet is re-proved exactly to be a supporting plane"""
    if len(corners) < 4: return Z
    Pf = np.array([f3(p) for p in corners])
    try: h = ConvexHull(Pf)
    except QhullError:
        return Z   # flat (all corners satisfy one plane both ways; a flat set has volume 0 by definition)
    vol = Z
    for s in h.simplices:
        a, b, c = corners[s[0]], corners[s[1]], corners[s[2]]; n = cross(vsub(b, a), vsub(c, a))
        if all(x == Z for x in n): continue
        side = [sgn(dot(n, vsub(p, a))) for p in corners]
        assert all(t <= 0 for t in side) or all(t >= 0 for t in side), 'facet plane is not a supporting plane'
        d = det3(a, b, c)
        if all(t <= 0 for t in side): vol = qa(vol, d)        # outward normal: signed fan from the origin
        else: vol = qs(vol, d)
    vol = qm(vol, qr(Fr(1, 6)))
    assert sgn(vol) >= 0 and abs(qf(vol) - h.volume) < 1e-9, ('volume mismatch', qf(vol), h.volume)
    return vol
class Poly:
    def __init__(self, planes, corners=None, name=''):
        self.planes = planes; self.name = name
        self.corners = enumerate_corners(planes) if corners is None else corners
        self.cf = np.array([f3(p) for p in self.corners]) if self.corners else np.zeros((0, 3))
        self._vol = None
    @property
    def vol(self):
        if self._vol is None: self._vol = exact_volume(self.corners)
        return self._vol
    def centre_radius(self):
        c = self.cf.mean(0); return c, np.linalg.norm(self.cf - c, axis=1).max()
    def shifted(self, t):
        return Poly([(n, qa(d, dot(n, t))) for n, d in self.planes], [vadd(p, t) for p in self.corners], self.name)
    def mapped(self, G, t):
        """image under x -> G x + t, G an exact 3x3 signed permutation (orthogonal), t exact"""
        Gt = [[G[j][i] for j in range(3)] for i in range(3)]                  # G^T
        mv = lambda M, v: [dot(M[i], v) for i in range(3)]
        planes = [(mv(G, n), qa(d, dot(mv(G, n), t))) for n, d in self.planes]   # (G n).(x) <= d + (G n).t
        return Poly(planes, [vadd(mv(G, p), t) for p in self.corners], self.name)
def hull_poly(points, name=''):
    """exact supporting planes of conv(points) from qhull facets, each proved exactly; corners re-enumerated and checked = points"""
    Pf = np.array([f3(p) for p in points]); h = ConvexHull(Pf); planes = []
    for s in h.simplices:
        a, b, c = points[s[0]], points[s[1]], points[s[2]]; n = cross(vsub(b, a), vsub(c, a))
        if all(x == Z for x in n): continue
        side = [sgn(dot(n, vsub(p, a))) for p in points]
        if all(t <= 0 for t in side): pl = (n, dot(n, a))
        elif all(t >= 0 for t in side): pl = ([qn(x) for x in n], qn(dot(n, a)))
        else: raise AssertionError('qhull facet not supporting')
        if not any(same_plane(pl, p2) for p2 in planes): planes.append(pl)
    P = Poly(planes, name=name)
    pts = [tuple(p) for p in points]
    assert all(tuple(c) in pts for c in P.corners), 'hull has a corner that is not an input point'
    return P
def intersect(A, B, name=''):
    """exact A & B with exact pruning: planes not cutting the other body are redundant; a plane excluding the other body -> empty"""
    if len(A.corners) == 0 or len(B.corners) == 0: return Poly([], [], name)
    cA, rA = A.centre_radius(); cB, rB = B.centre_radius()
    if np.linalg.norm(cA - cB) > rA + rB + 1e-6: return Poly([], [], name)
    planes = []
    for P, Q in ((A, B), (B, A)):
        for n, d in P.planes:
            s = [sgn(qs(d, dot(n, x))) for x in Q.corners]
            if all(t > 0 for t in s): continue                  # does not cut Q: redundant
            if all(t < 0 for t in s): return Poly([], [], name)   # excludes Q: empty
            if not any(same_plane((n, d), p2) for p2 in planes): planes.append((n, d))
    return Poly(planes, name=name)
def inter(*bodies, name=''):
    P = bodies[0]
    for B in bodies[1:]:
        P = intersect(P, B, name)
        if not P.corners: break
    return P

