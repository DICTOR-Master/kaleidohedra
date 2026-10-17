# DICTO 2026-10-18 octet study: exact convex polytopes in Q(sqrt5) -- planes n.x <= d, intersection, vertices, volume.
# Float (scipy) only finds WHICH planes meet at each corner; every corner is then solved and checked exactly.
import itertools, numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
from q5 import *
def planes_of(P):
    """exact planes (n, d), n.x <= d, of the convex hull of exact points P"""
    Pf = np.array([[qf(x) for x in p] for p in P]); h = ConvexHull(Pf); out = []
    for e in h.equations:
        idx = [i for i in range(len(P)) if abs(Pf[i] @ e[:3] + e[3]) < 1e-9]
        a, b, c = None, None, None
        for i, j, k in itertools.combinations(idx, 3):
            n = cross(vsub(P[j], P[i]), vsub(P[k], P[i]))
            if any(x != Z for x in n): a = i; break
        d = dot(n, P[a])
        if qf(dot(n, [qa(x, y) for x, y in zip(P[a], [(Fr(0), Fr(0))] * 3)])) and False: pass
        # orient outward: interior point = mean of hull points
        if np.dot([qf(x) for x in n], Pf.mean(0)) > qf(d): n = [qn(x) for x in n]; d = qn(d)
        if not any(all(qf(qs(qm(x, dd), qm(y, d))) == 0 for x, y in zip(n, nn)) and sgn(qm(d, dd)) >= 0 for nn, dd in out if False): out.append((n, d))
    # dedupe parallel equal planes
    uniq = []
    for n, d in out:
        nf = np.array([qf(x) for x in n]); df = qf(d); nn = np.linalg.norm(nf)
        if not any(np.allclose(nf / nn, u[2]) and abs(df / nn - u[3]) < 1e-12 for u in uniq): uniq.append((n, d, nf / nn, df / nn))
    return [(n, d) for n, d, _, _ in uniq]
def shift(planes, t): return [(n, qa(d, dot(n, t))) for n, d in planes]
def solve3(A, b):
    D = det3(*A)
    if D == Z: return None
    cols = lambda k: [[b[i] if j == k else A[i][j] for j in range(3)] for i in range(3)]
    return [qd(det3(*cols(k)), D) for k in range(3)]
def intersect(planes):
    """exact corners of {x: n.x <= d for all planes}; [] if empty or flat"""
    nf = np.array([[qf(x) for x in n] for n, d in planes]); df = np.array([qf(d) for n, d in planes])
    # interior point by LP-free trick: Chebyshev centre via scipy linprog
    from scipy.optimize import linprog
    norm = np.linalg.norm(nf, axis=1)
    res = linprog(np.r_[np.zeros(3), -1], A_ub=np.c_[nf, norm], b_ub=df, bounds=[(None, None)] * 3 + [(0, None)])
    if not res.success or res.x[3] < 1e-9: return []
    hs = HalfspaceIntersection(np.c_[nf, -df], res.x[:3]); corners = []
    for v, dual in zip(hs.intersections, hs.dual_facets):
        act = [i for i in range(len(planes)) if abs(nf[i] @ v - df[i]) < 1e-9 * max(1, norm[i])]
        x = None
        for i, j, k in itertools.combinations(act, 3):
            x = solve3([planes[i][0], planes[j][0], planes[k][0]], [planes[i][1], planes[j][1], planes[k][1]])
            if x is not None: break
        assert x is not None and all(sgn(qs(d, dot(n, x))) >= 0 for n, d in planes), 'corner failed exact check'
        if not any(all(a == b for a, b in zip(x, y)) for y in corners): corners.append(x)
    return corners
def volume(corners):
    """exact volume of the convex hull of exact corners"""
    if len(corners) < 4: return Z
    Pf = np.array([[qf(x) for x in p] for p in corners]); h = ConvexHull(Pf); c0 = corners[0]; vol = Z
    for s in h.simplices:
        d = det3(vsub(corners[s[0]], c0), vsub(corners[s[1]], c0), vsub(corners[s[2]], c0)); vol = qa(vol, d if sgn(d) >= 0 else qn(d))
    return qm(vol, qr(Fr(1, 6)))
