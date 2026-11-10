"""Aim 2, chunk 2 (DICTO 10 Nov "yes 1 then 2"): canonical form along the cube-octahedron sweep S(mu) = cube ∩ mu·octahedron
(cube [-1,1]^3, octahedron |x|+|y|+|z| <= 1). Per chamber of mu (between consecutive candidate walls), exactly in sympy:
(a) Omega(S; 0) by the positive-geometry formula: sum over a triangulation of S of the simplex canonical forms
    <Z0 Z1 Z2 Z3>^3 / (<Y Z1 Z2 Z3><Y Z0 Z2 Z3><Y Z0 Z1 Z3><Y Z0 Z1 Z2>), Y = (1,0,0,0), Z = (1, vertex);
(b) 3!·vol(S*), S* = conv(octahedron, cube/mu) (the bridge fact Omega(S;0) = 3! vol(S*));
(c) vol(S) for comparison; the walls where the piecewise formulas change; the poles of each piece continued in mu.
Usage: python canon_sweep.py"""
import itertools, sympy as sp, numpy as np
from scipy.spatial import ConvexHull, Delaunay
mu = sp.Symbol('mu', positive=True)
cube = [sp.Matrix(p) for p in itertools.product([1, -1], repeat=3)]
octa = [sp.Matrix(v) * sg for v in ([1, 0, 0], [0, 1, 0], [0, 0, 1]) for sg in (1, -1)]
# halfspaces of S(mu): cube |x_i| <= 1; octahedron facets ±x±y±z <= mu
H = [(sp.Matrix(e) * sg, sp.Integer(1)) for e in ([1, 0, 0], [0, 1, 0], [0, 0, 1]) for sg in (1, -1)] + \
    [(sp.Matrix(sg), mu) for sg in itertools.product([1, -1], repeat=3)]
def S_vertices(m):
    """exact vertices of S at a numeric rational mu = m, as symbolic expressions in mu (each vertex = 3 planes)"""
    out = {}
    for tri in itertools.combinations(range(len(H)), 3):
        A = sp.Matrix.hstack(*[H[k][0] for k in tri]).T
        if A.det() == 0: continue
        b = sp.Matrix([H[k][1] for k in tri]); X = A.LUsolve(b)
        Xm = X.subs(mu, m)
        if all((H[k][0].T * Xm)[0] <= H[k][1].subs(mu, m) for k in range(len(H))):
            out.setdefault(tuple(Xm), sp.simplify(X))
    return list(out.values()), [tuple(float(x) for x in k) for k in out]
def bracket(*Z): return sp.Matrix.hstack(*Z).det()
Y0 = (sp.Rational(1, 97), sp.Rational(1, 89), sp.Rational(1, 83))     # a generic point near the centre (no inner triangulation face through it)
def omega_at(m, y):
    Vs, Vf = S_vertices(m); T = Delaunay(np.array(Vf)); Y = sp.Matrix([1, *y]); tot = 0
    for simp in T.simplices:
        Z = [sp.Matrix([1] + [x.subs(mu, m) for x in Vs[k]]) for k in simp]
        o = bracket(*Z)
        if o < 0: Z[0], Z[1] = Z[1], Z[0]; o = -o                 # every simplex positively oriented
        num = o ** 3; den = 1
        for j in range(4): den *= bracket(*[Z[k] if k != j else Y for k in range(4)])
        tot += num / den
    return tot, len(Vs)
def vol_polar_at(m, y):
    """polar of S about y: vertices n/(b - n.y) over the facets of S at mu = m"""
    yv = sp.Matrix(y); U = []
    Vs, Vf = S_vertices(m); h = ConvexHull(np.array(Vf))
    for eq in {tuple(np.round(e, 9)) for e in h.equations}:
        # match the exact plane among H
        for n_, b_ in H:
            nb = np.array([float(x) for x in n_]); bb = float(b_.subs(mu, m))
            if np.allclose(nb / np.linalg.norm(nb), eq[:3], atol=1e-7) and abs(bb / np.linalg.norm(nb) + eq[3]) < 1e-7:
                U.append(n_ / (b_.subs(mu, m) - (n_.T * yv)[0])); break
    Uf = np.array([[float(x) for x in u] for u in U]); hh = ConvexHull(Uf); c = sum(U, sp.zeros(3, 1)) / len(U); tot = 0
    for simp in hh.simplices: tot += abs(sp.Matrix.hstack(*[U[k] - c for k in simp]).det()) / 6
    return tot
def vol_polar(m):
    """S* = conv(octahedron, cube/mu) about the centre: symbolic in mu, structure from mu = m"""
    P = octa + [cc / mu for cc in cube]; Pf = np.array([[float(x.subs(mu, m)) for x in p] for p in P])
    h = ConvexHull(Pf); tot = 0
    for simp in h.simplices:
        d = sp.Matrix.hstack(*[P[k] for k in simp]).det(); tot += d * sp.sign(d.subs(mu, m)) / 6
    return sp.factor(sp.simplify(tot)), sorted(h.vertices)
def vol_S(m):
    Vs, Vf = S_vertices(m); T = Delaunay(np.array(Vf)); tot = 0
    for simp in T.simplices:
        M = sp.Matrix.hstack(*[Vs[k] - Vs[simp[0]] for k in simp[1:]]); d = M.det(); tot += d * sp.sign(d.subs(mu, m)) / 6
    return sp.factor(sp.simplify(tot))
samples = [sp.Rational(1, 2), sp.Rational(3, 2), sp.Rational(9, 5), sp.Rational(2, 1) + sp.Rational(1, 3), sp.Rational(5, 2), sp.Rational(7, 2), 5]
rows = []
for m in samples:
    om, nv = omega_at(m, Y0); vpy = vol_polar_at(m, Y0); vp, used = vol_polar(m); vs = vol_S(m)
    ratio = sp.nsimplify(om / vpy); agree = sp.simplify(om - 6 * vpy) == 0; rows.append(agree); print(f'   Omega / vol(polar about y) = {ratio}', flush=True)
    poles = sorted(set(sp.solve(sp.denom(sp.together(vp)), mu)), key=lambda x: complex(x).real)
    print(f'mu = {m}: S {nv} vertices; bridge at a generic point: Omega = 3! vol(polar): {agree};  vol(S*) = {vp}  (poles in mu {poles});  vol(S) = {vs}', flush=True)
print('FINAL ok' if all(rows) else 'FINAL FAIL: bridge identity')
