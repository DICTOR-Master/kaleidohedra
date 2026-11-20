# exactgeo.py -- exact convex hulls and exact star surfaces over a number field (nf.py). Floats only PROPOSE (scipy hull, angular
# order of a face's corners); every statement kept is checked exactly: each facet plane holds its points exactly, every other point
# lies strictly inside, each face polygon is strictly convex with no corner collinear, and every other point of the plane lies in it.
# Study 2026-11-21-gaps-batch-a.
import numpy as np
from scipy.spatial import ConvexHull
from nf import vsub, vadd, vmul, dot, cross, iszerov, key

def fl(P): return np.array([[float(x) for x in p] for p in P])

def exact_hull(P):
    """P: list of exact points. Returns (faces as ccw-outward corner index lists, ok). Points that are not corners are allowed
    (they must lie in a face or inside)."""
    PF = fl(P); H = ConvexHull(PF); groups = {}
    for sm, eq in zip(H.simplices, H.equations):
        groups.setdefault(tuple(np.round(eq / np.abs(eq[:3]).max(), 6)), (eq, set()))[1].update(sm.tolist())
    faces = []; ok = True; N = len(P)
    for eq, ids in groups.values():
        on = [i for i in range(N) if abs(eq[:3] @ PF[i] + eq[3]) < 1e-8 * max(1, np.abs(PF).max())]
        p0 = P[on[0]]; nrm = None
        for a in on[1:]:
            for b in on[1:]:
                c = cross(vsub(P[a], p0), vsub(P[b], p0))
                if not iszerov(c): nrm = c; break
            if nrm is not None: break
        off = dot(nrm, p0)
        # outward: interior points give negative
        s_out = [(dot(nrm, P[i]) - off).sign() for i in range(N) if i not in on]
        if any(x == 0 for x in s_out) or len(set(s_out)) > 1: ok = False
        if s_out and s_out[0] > 0: nrm = vmul(-1, nrm); off = -off
        if not all((dot(nrm, P[i]) - off).iszero() for i in on): ok = False
        # order by float angle, then keep the 2D hull corners, checked exactly
        n = eq[:3]; u = np.cross(n, [1, 0, 0] if abs(n[0]) < .9 else [0, 1, 0]); u /= np.linalg.norm(u); w = np.cross(n, u)
        c2 = PF[on].mean(0)
        if len(on) > 3:
            from scipy.spatial import ConvexHull as CH
            Q = np.array([[(PF[i] - c2) @ u, (PF[i] - c2) @ w] for i in on]); h2 = CH(Q); poly = [on[k] for k in h2.vertices]
        else: poly = list(on)
        # ccw seen from outside: (b - a) x (c - b) . nrm > 0 at every corner, exactly
        def turn(a, b, c): return dot(cross(vsub(P[b], P[a]), vsub(P[c], P[b])), nrm).sign()
        if turn(poly[0], poly[1], poly[2]) < 0: poly = poly[::-1]
        m = len(poly)
        if not all(turn(poly[k - 1], poly[k], poly[(k + 1) % m]) > 0 for k in range(m)): ok = False
        for i in on:
            if i in poly: continue
            if not all(dot(cross(vsub(P[poly[(k + 1) % m]], P[poly[k]]), vsub(P[i], P[poly[k]])), nrm).sign() >= 0 for k in range(m)): ok = False
        faces.append(poly)
    return faces, ok

def sides(F):
    s = {}
    for f in F: s[len(f)] = s.get(len(f), 0) + 1
    return dict(sorted(s.items()))

def face_normal(P, f):
    N = [P[f[0]][0] * 0] * 3
    for k in range(len(f)): N = vadd(N, cross(P[f[k]], P[f[(k + 1) % len(f)]]))
    return N

def feet_and_poles(P, F):
    feet, poles = [], []
    for f in F:
        N = face_normal(P, f); s = dot(N, P[f[0]])
        feet.append(vmul(s / dot(N, N), N)); poles.append(vmul(1 / s, N))
    return feet, poles

def star_surface(P, F, t):
    """the solid with each face pyramid to the tip t x foot, as a surface; neighbouring triangles merged only when EXACTLY coplanar;
    corners where the boundary turns (exactly). Returns points, faces (index loops), ok (closed, oriented)"""
    feet, _ = feet_and_poles(P, F); tips = [vmul(t, x) for x in feet]
    Q = list(P) + tips; n0 = len(P)
    tris = [[f[k], f[(k + 1) % len(f)], n0 + i] for i, f in enumerate(F) for k in range(len(f))]
    E = {}
    for i, tr in enumerate(tris):
        for k in range(3): E.setdefault(tuple(sorted((tr[k], tr[(k + 1) % 3]))), []).append(i)
    par = list(range(len(tris)))
    def fd(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    ok = all(len(l) == 2 for l in E.values())
    for e, l in E.items():
        if len(l) != 2: continue
        i, j = l; x = [v for v in tris[j] if v not in tris[i]][0]; a, b, c = (Q[v] for v in tris[i])
        if dot(cross(vsub(b, a), vsub(c, a)), vsub(Q[x], a)).iszero(): par[fd(i)] = fd(j)
    groups = {}
    for i in range(len(tris)): groups.setdefault(fd(i), []).append(i)
    faces = []
    for g in groups.values():
        cnt = {}
        for i in g:
            tr = tris[i]
            for k in range(3): e = (tr[k], tr[(k + 1) % 3]); cnt[e] = cnt.get(e, 0) + 1
        bd = [e for e in cnt if (e[1], e[0]) not in cnt]
        nxt = {}
        for a, b in bd:
            if a in nxt: ok = False
            nxt[a] = b
        start = bd[0][0]; loop = [start]; cur = nxt[start]
        while cur != start and len(loop) <= len(bd): loop.append(cur); cur = nxt.get(cur, start)
        if len(loop) != len(bd): ok = False                  # one boundary loop per merged face
        crn = [v for k, v in enumerate(loop) if not iszerov(cross(vsub(Q[v], Q[loop[k - 1]]), vsub(Q[loop[(k + 1) % len(loop)]], Q[v])))]
        faces.append(crn)
    return Q, faces, ok

def similar_same_frame(A, B):
    """exact: is the corner set A a positive multiple of B (same frame, no rotation)? compares directions and the squared-radius ratio"""
    if len(A) != len(B): return False
    ra = max(A, key=lambda v: float(dot(v, v))); rb = max(B, key=lambda v: float(dot(v, v)))
    lam2 = dot(ra, ra) / dot(rb, rb)
    for v in A:
        if not any(iszerov(cross(u, v)) and dot(u, v).sign() > 0 and (dot(v, v) - lam2 * dot(u, u)).iszero() for u in B): return False
    return True
