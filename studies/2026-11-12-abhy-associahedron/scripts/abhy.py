"""Aim 2, chunk 4 (12 Nov 2026): the associahedron sanity case. Reproduce, exactly and with our own chunk-2/3 tools, the theorem of
Arkani-Hamed, Bai, He, Yan ("Scattering forms and the positive geometry of kinematics, color and the worldsheet", JHEP 2018,
arXiv:1711.09102): the kinematic (ABHY) associahedron A_n has canonical form = the bi-adjoint scalar tree amplitude
m_n = sum over planar cubic trees (= triangulations of the n-gon) of prod 1/X_d over the tree's propagators.
Setup: planar variables X_{i,j} (1 <= i < j <= n, j >= i+2, (i,j) != (1,n)); X_{i,i+1} = X_{1,n} = 0; Mandelstams
s_{a,b} = X_{a,b+1} + X_{a+1,b} - X_{a,b} - X_{a+1,b+1}; ABHY slice: s_{a,b} = -c_{a,b} (constants > 0) for 1 <= a < b <= n-1,
b >= a+2. Coordinates y = (X_{1,3}, ..., X_{1,n-1}); every X_d is then affine in y; A_n = {all X_d >= 0}, dimension n-3.
Canonical form by Warren's vertex formula (chunk 3): Omega(Y) = sum over vertices |det(grad X_d, d tight)| / prod_{d tight} X_d(Y).
CONTROLS / CHECKS (per n):
 (V) vertices: every triangulation of the n-gon gives a feasible vertex with exactly n-3 tight facets (simple); count = Catalan(n-2);
     for n <= 8 an independent enumeration of ALL (n-3)-subsets of facets finds no other vertex.
 (D) every vertex determinant |det| = 1 (ABHY: unimodular).
 (A) THE THEOREM: Omega(Y) = m_n(Y) exactly at 3 random rational interior points, and identically (symbolic y) for n <= 6.
 (T) independent formula for n = 5, 6, 7: sum over a Delaunay triangulation of the polytope of simplex canonical forms
     <Z0..Zd>^d / prod <Y Z..> (chunk 2 method, any dimension) equals Omega.
 (N1) negative: a non-ABHY slice (one constraint tilted: s_{1,3} = -c_{1,3} + X_{1,3}) still cuts a polytope, but must NOT give
     m_n (some |det| != 1, Omega != m_n at the sample point) - checked for n = 6, 7. (Pilot 12 Nov: a first tilt along X_{1,4} kept
     every |det| = 1 and still gave m_n - a shear of the coordinates, so no negative control; replaced.)
 (N2) negative: m_n with one tree dropped must differ from Omega.
Runs n = 4..10 in parallel on 4 cores. Usage: python -u abhy.py [nmax]"""
import itertools, sys, time, random
from fractions import Fraction as Fr
from multiprocessing import Pool
import sympy as sp, numpy as np

def catalan(k): return sp.binomial(2 * k, k) // (k + 1)

def triangulations(poly):
    """all triangulations of the convex polygon with vertex list poly, as sets of diagonals (i, j), i < j"""
    if len(poly) < 3: return [frozenset()]
    if len(poly) == 3: return [frozenset()]
    a, b = poly[0], poly[-1]; out = []
    for k in range(1, len(poly) - 1):
        c = poly[k]
        for L in triangulations(poly[:k + 1]):
            for R in triangulations(poly[k:]):
                D = set(L) | set(R)
                for e in ((a, c), (c, b)):
                    if abs(e[0] - e[1]) > 1 and not (min(e) == 1 and max(e) == len_n[0]): D.add((min(e), max(e)))
                out.append(frozenset(D))
    return out
len_n = [0]

def setup(n, tilt=False):
    """X_d as affine functions of y (sympy), the diagonal list, the constants c"""
    y = sp.symbols(f'y3:{n}')                              # y_j = X_{1,j}, j = 3..n-1
    rng = random.Random(1000 + n); c = {}
    X = {}
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            if j == i + 1 or (i, j) == (1, n): X[(i, j)] = sp.Integer(0)
    for j in range(3, n): X[(1, j)] = y[j - 3]
    for a in range(1, n):
        for b in range(a + 2, n):
            c[(a, b)] = sp.Rational(rng.randint(1, 9), rng.randint(1, 5))
    for a in range(1, n):                                   # X_{a+1,b+1} = X_{a,b+1} + X_{a+1,b} - X_{a,b} + c_{a,b}
        for b in range(a + 2, n):
            rhs = X[(a, b + 1)] + X[(a + 1, b)] - X[(a, b)] + c[(a, b)]
            if tilt and (a, b) == (1, 3): rhs = rhs - X[(1, 3)]     # s_{1,3} = -c_{1,3} + X_{1,3}: vertex {X14, X24} gets |det| 2
            X[(a + 1, b + 1)] = sp.expand(rhs)
    diags = [(i, j) for i in range(1, n + 1) for j in range(i + 2, n + 1) if (i, j) != (1, n)]
    assert len(diags) == n * (n - 3) // 2
    return y, X, diags, c

def run(args):
    n, tilt = args
    t0 = time.time(); out = []; ok = True
    def chk(name, cond):
        nonlocal ok; ok &= bool(cond); out.append(('ok   ' if cond else 'FAIL ') + f'n={n}{" (tilted slice)" if tilt else ""}: ' + name)
    len_n[0] = n
    y, X, diags, c = setup(n, tilt)
    G = {d: [sp.diff(X[d], v) for v in y] for d in diags}  # gradients (constant)
    tris = triangulations(list(range(1, n + 1)))
    tris = list(set(tris))
    if not tilt: chk(f'{len(tris)} triangulations = Catalan({n-2}) = {catalan(n-2)}', len(tris) == catalan(n - 2))
    Xn = {d: sp.lambdify(y, X[d]) for d in diags}
    verts = {}; dets = []; simple = True; feasible = True
    for T in tris:
        T = sorted(T); M = sp.Matrix([G[d] for d in T]); b = sp.Matrix([-X[d].subs({v: 0 for v in y}) for d in T])
        if M.det() == 0: feasible = False; continue
        v = M.LUsolve(b); vals = {d: X[d].subs(dict(zip(y, v))) for d in diags}
        tight = [d for d in diags if vals[d] == 0]
        if any(vals[d] < 0 for d in diags): feasible = False
        if len(tight) != n - 3: simple = False
        dv = abs(M.det()); verts[tuple(v)] = (T, dv); dets.append(dv)
    if not tilt:
        chk(f'(V) every triangulation gives a feasible simple vertex ({len(verts)} vertices)', feasible and simple and len(verts) == catalan(n - 2))
        chk(f'(D) every vertex |det| = 1', all(d == 1 for d in dets))
    if not tilt and n <= 8:                                   # independent vertex enumeration over all facet subsets
        extra = 0
        for S in itertools.combinations(diags, n - 3):
            M = sp.Matrix([G[d] for d in S])
            if M.det() == 0: continue
            v = M.LUsolve(sp.Matrix([-X[d].subs({w: 0 for w in y}) for d in S]))
            if all(X[d].subs(dict(zip(y, v))) >= 0 for d in diags) and tuple(v) not in verts: extra += 1
        chk(f'(V) all {sp.binomial(len(diags), n-3)} facet subsets: no vertex outside the triangulations', extra == 0)
    def omega(Y):
        sub = dict(zip(y, Y)); tot = 0
        for v, (T, dv) in verts.items():
            den = 1
            for d in T: den *= X[d].subs(sub)
            tot += dv / den
        return tot
    def amp(Y, drop=None):
        sub = dict(zip(y, Y)); tot = 0
        for k, T in enumerate(sorted(tris, key=sorted)):
            if k == drop: continue
            den = 1
            for d in T: den *= X[d].subs(sub)
            tot += 1 / den
        return tot
    # interior points: centroid of the vertices, moved slightly at random (exact rationals)
    V = np.array([[float(x) for x in v] for v in verts]); cen = V.mean(0); rng = random.Random(7 * n + tilt)
    pts = []
    while len(pts) < 3:
        P = [sp.Rational(round(float(x) * 997) + rng.randint(-40, 40), 997) for x in cen]
        if all(X[d].subs(dict(zip(y, P))) > 0 for d in diags): pts.append(P)
    if not tilt:
        chk('(A) Omega = m_n exactly at 3 random rational interior points', all(sp.simplify(omega(P) - amp(P)) == 0 for P in pts))
        chk('(N2) m_n with one tree dropped differs from Omega', sp.simplify(omega(pts[0]) - amp(pts[0], drop=0)) != 0)
        if n <= 6:
            chk('(A) Omega = m_n identically (symbolic y)', sp.simplify(omega(list(y)) - amp(list(y))) == 0)
        if 5 <= n <= 7:
            from scipy.spatial import Delaunay
            vs = list(verts); Vf = np.array([[float(x) for x in v] for v in vs]); Tr = Delaunay(Vf); dd = n - 3
            Y = sp.Matrix([1, *pts[0]]); tot = 0
            br = lambda Zs: sp.Matrix.hstack(*Zs).det()
            for simp in Tr.simplices:
                Z = [sp.Matrix([1, *vs[k]]) for k in simp]; o = br(Z)
                if o == 0: continue
                if o < 0: Z[0], Z[1] = Z[1], Z[0]; o = -o
                den = 1
                for j in range(dd + 1): den *= br([Z[k] if k != j else Y for k in range(dd + 1)])
                tot += o ** dd / den
            chk(f'(T) triangulation formula ({len(Tr.simplices)} simplices) = Omega', sp.simplify(tot - omega(pts[0])) == 0)
    else:
        chk('(N1) tilted slice: some vertex |det| != 1 or Omega != m_n (must hold: not the ABHY realisation)',
            any(d != 1 for d in dets) or sp.simplify(omega(pts[0]) - amp(pts[0])) != 0)
        out.append(f'      tilted slice: vertices {len(verts)}, feasible {feasible}, simple {simple}, dets {sorted(set(map(str, dets)))}')
    out.append(f'n={n}{" tilted" if tilt else ""}: done in {time.time() - t0:.1f}s, {len(tris)} trees, {len(diags)} facets, dimension {n-3}')
    return n, tilt, ok, out

if __name__ == '__main__':
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    jobs = [(n, False) for n in range(nmax, 3, -1)] + [(6, True), (7, True)]
    allok = True; done = 0
    with Pool(4) as pool:
        for n, tilt, ok, out in pool.imap_unordered(run, jobs):
            allok &= ok; done += 1
            for line in out: print(line, flush=True)
            print(f'PROGRESS {done / len(jobs):.2f} cases', flush=True)
    print('FINAL ok: all checks and controls held' if allok else 'FINAL FAIL')
