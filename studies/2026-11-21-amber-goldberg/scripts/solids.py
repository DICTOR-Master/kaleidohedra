"""Amber-Goldberg study (21 Nov 2026): Goldberg cores GP(m,n) for amber.py (unchanged copy of the amber-cell sweep's).
Goldberg (1937): the icosahedral polyhedra with 12 pentagons and 10(T-1) hexagons, T = m^2 + mn + n^2, all vertices 3-valent.

Realisation chosen (one standard form, planar faces by construction): the POLAR (reciprocal in the unit sphere) of the geodesic sphere.
  1. Icosahedron cyc(0, +-1, +-phi) (T_h axes on the cube axes, 2-fold axes = coordinate axes), faces oriented outward.
  2. Goldberg-Coxeter subdivision of every face: the triangular-lattice points of the triangle 0, P1 = m e1 + n e2, P2 = P1 turned 60 deg,
     mapped barycentrically onto the face, then projected centrally onto the unit sphere: 10T + 2 points p_i (the geodesic sphere).
  3. Core = { x : p_i . x <= 1 for all i }: every face is tangent to the unit sphere at p_i (insphere radius 1 for every member).
     Face i is a pentagon at the 12 icosahedron vertices, a hexagon elsewhere; vertices = the 20T triangles of the hull of the p_i.
All arithmetic at 60 digits (resin.R).  Checks (asserted): 10T+2 points; 20T hull triangles; every triangle's plane leaves all other
points strictly on the centre side (margin printed); hence every core vertex lies on exactly 3 face planes and strictly inside the others
(convex, simple, planar faces); 12 pentagons, 10(T-1) hexagons; Euler V - E + F = 2.  build(name) with name GP_m_n."""
import itertools, math, os, sys
from fractions import Fraction as Fr
import numpy as np
from resin import R, CTX, PHI, dot, cross, vsub, vadd, vsc, det3

def icosahedron():
    P = []
    for a, b in itertools.product((1, -1), repeat=2):
        for c in range(3):
            v = [R(0), R(a), PHI*b]; P.append([v[(i - c) % 3] for i in range(3)])
    F = np.array([[float(x) for x in p] for p in P])
    from scipy.spatial import ConvexHull
    h = ConvexHull(F); faces = []
    for t in h.simplices:
        a, b, c = t
        if np.dot(np.cross(F[b] - F[a], F[c] - F[a]), F[a]) < 0: b, c = c, b
        faces.append((a, b, c))
    assert len(faces) == 20
    return P, faces

def unit(v):
    n = CTX.sqrt(sum(x.v*x.v for x in v)); return [R.of(x.v/n) for x in v]

def geodesic(m, n):
    P, faces = icosahedron()
    P1, P2 = (m, n), (-n, m + n)          # lattice coordinates in the basis e1, e2 (60 deg)
    det = P1[0]*P2[1] - P1[1]*P2[0]
    pts, idx = [], {}
    def add(p):
        u = unit(p); k = tuple(x.key() // 10**5 for x in u)
        if k not in idx: idx[k] = len(pts); pts.append(u)
        return idx[k]
    for A, B, C in faces:
        for i in range(-n, m + 1):
            for j in range(0, m + n + 1):
                l1 = Fr(i*P2[1] - j*P2[0], det); l2 = Fr(P1[0]*j - P1[1]*i, det); l0 = 1 - l1 - l2
                if min(l0, l1, l2) < 0: continue
                add([l0*P[A][t] + l1*P[B][t] + l2*P[C][t] for t in range(3)])
    T = m*m + m*n + n*n
    assert len(pts) == 10*T + 2, (len(pts), 10*T + 2)
    ico = {add(p) for p in P}
    return pts, ico, T

def build(name):
    m, n = map(int, name.split("_")[1:3])
    pts, ico, T = geodesic(m, n)
    if name.startswith("GPc_"): pts = canonical(pts, m, n)
    N = len(pts)
    F = np.array([[float(x) for x in p] for p in pts])
    from scipy.spatial import ConvexHull
    h = ConvexHull(F)
    tris = []
    for t in h.simplices:
        a, b, c = map(int, t)
        if np.dot(np.cross(F[b] - F[a], F[c] - F[a]), F[a]) < 0: b, c = c, b
        tris.append((a, b, c))
    assert len(tris) == 20*T, (len(tris), 20*T)
    # core vertex of each triangle: p_a.x = p_b.x = p_c.x = 1 (Cramer, 60 digits)
    V = []
    for a, b, c in tris:
        A, B, C = pts[a], pts[b], pts[c]; D = det3(A, B, C)
        x = vsc(R(1)/D, vadd(vadd(cross(B, C), cross(C, A)), cross(A, B)))
        V.append(x)
    if name.startswith("GPc_"): assert len(set(tuple(v.key() for v in x) for x in V)) == len(V), "distinct vertices"
    # exact-at-60-digits convexity: every core vertex strictly inside every other face plane
    margin = None
    for vi, (a, b, c) in ([] if os.environ.get("SOLIDS_FAST") else enumerate(tris)):     # SOLIDS_FAST: summary.py's counts only
        x = V[vi]
        for j in range(N):
            d = dot(pts[j], x) - 1
            if j in (a, b, c): assert d.sign() == 0, "vertex on its own planes"
            else:
                assert d.sign() < 0, "convexity / simple vertex"
                margin = -float(d) if margin is None else min(margin, -float(d))
    inc = {j: [] for j in range(N)}
    for vi, t in enumerate(tris):
        for j in t: inc[j].append(vi)
    faces, planes = [], []
    for j in range(N):
        L = inc[j]; nrm = F[j]; u = np.cross(nrm, [1, 0, 0] if abs(nrm[0]) < .9 else [0, 1, 0]); u /= np.linalg.norm(u); w = np.cross(nrm, u)
        Vf = {vi: np.array([float(x) for x in V[vi]]) for vi in L}
        cyc = sorted(L, key=lambda vi: math.atan2(Vf[vi] @ w, Vf[vi] @ u))
        k = len(cyc)
        assert (k == 5) == (j in ico) and k in (5, 6), "12 pentagons at the icosahedron vertices, hexagons elsewhere"
        faces.append((cyc, "pent" if k == 5 else "hex")); planes.append((pts[j], R(1)))
    E = sum(len(f) for f, k in faces)//2
    assert len(V) - E + len(faces) == 2
    return dict(V=V, faces=faces, planes=planes, name=name, T=T, margin=margin)

CANON = {}
def canonical(pts, m, n):
    """Second realisation, names GPc_m_n: the CANONICAL form (every edge tangent to the unit sphere; the tangency points' centroid is the
    centre, here by symmetry).  Face planes q_i . x = 1; edge {i, j} tangent to the unit sphere <=> |q_i - q_j|^2 = |q_i x q_j|^2.
    Gauss-Newton with minimum-norm steps (float64) from the insphere form (q_i = p_i): the step is equivariant, so the icosahedral
    symmetry is kept.  Then the q_i are made exactly T_h- (chiral: T-) symmetric at 60 digits: one representative per orbit, averaged
    over its stabiliser, the rest by the signed-permutation action (exact).  Tangency then holds to the float residual (printed,
    stored in CANON); planarity is exact (faces are defined by their planes).  Also checked: each tangency point lies inside its edge."""
    from resin import TH, act
    from scipy.spatial import ConvexHull
    N = len(pts); P = np.array([[float(x) for x in p] for p in pts])
    h = ConvexHull(P); E = set()
    for t in h.simplices:
        for a, b in ((t[0], t[1]), (t[1], t[2]), (t[0], t[2])): E.add((min(a, b), max(a, b)))
    third = {}
    for t in h.simplices:
        for k in range(3):
            a, b, c = t[k], t[(k+1) % 3], t[(k+2) % 3]; third.setdefault((min(a, b), max(a, b)), []).append(c)
    E = sorted(E); I = np.array([e[0] for e in E]); J = np.array([e[1] for e in E])
    q = P.copy()
    for it in range(60):
        qi, qj = q[I], q[J]
        n2i, n2j, dij = (qi*qi).sum(1), (qj*qj).sum(1), (qi*qj).sum(1)
        f = ((qi - qj)**2).sum(1) - (n2i*n2j - dij**2)
        if np.abs(f).max() < 1e-15: break
        Jm = np.zeros((len(E), 3*N))
        gi = 2*(qi - qj) - (2*n2j[:, None]*qi - 2*dij[:, None]*qj)
        gj = -2*(qi - qj) - (2*n2i[:, None]*qj - 2*dij[:, None]*qi)
        for k in range(3):
            Jm[np.arange(len(E)), 3*I + k] = gi[:, k]; Jm[np.arange(len(E)), 3*J + k] = gj[:, k]
        dq = np.linalg.lstsq(Jm, -f, rcond=None)[0]
        q = q + dq.reshape(N, 3)
    # exact T_h / T symmetrisation at 60 digits
    keyf = lambda v: tuple(np.round(v, 6))
    pos = {keyf(P[i]): i for i in range(N)}
    Q = [None]*N
    for i in range(N):
        if Q[i] is not None: continue
        img = {}
        for g in TH:
            j = pos[keyf(np.array(act(g, list(P[i]))))]; img.setdefault(j, []).append(g)
        stab = img[i]
        qr = [R(0)]*3
        for hh in stab: qr = vadd(qr, act(hh, [R(float(x)) for x in q[i]]))
        qr = vsc(Fr(1, len(stab)), qr)
        for j, gs in img.items(): Q[j] = act(gs[0], qr)
    res = 0.0; inside = None
    for a, b in E:
        qa, qb = Q[a], Q[b]; d = vsub(qa, qb); c = cross(qa, qb)
        res = max(res, abs(float(dot(d, d) - dot(c, c))))
        # tangency point t = x qa + y qb with qa.t = qb.t = 1 (closest point of the edge line); inside the edge <=> strictly inside the
        # planes of the two faces at the edge's ends (the third vertices of the two hull triangles on edge a-b)
        A, B, C = dot(qa, qa), dot(qa, qb), dot(qb, qb); D = A*C - B*B
        x, y = (C - B)/D, (A - B)/D; t = vadd(vsc(x, qa), vsc(y, qb))
        for cc in third[(a, b)]:
            g = 1 - dot(Q[cc], t); assert g.sign() > 0, "tangency point inside its edge"
            inside = float(g) if inside is None else min(inside, float(g))
    CANON.update(residual=res, iterations=it, inside_margin=inside)
    print(f"canonical form GP({m},{n}): Gauss-Newton iterations {it}, max edge tangency residual (60-digit check) {res:.2e}, tangency points inside their edges (margin {inside:.3e})", flush=True)
    return Q

if __name__ == "__main__":
    for nm in sys.argv[1:]:
        S = build(nm)
        from collections import Counter
        print(nm, "T", S["T"], "vertices", len(S["V"]), dict(Counter(k for f, k in S["faces"])), f"convexity margin {S['margin']}", "ok")
