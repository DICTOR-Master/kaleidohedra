# Fair member of a dual line: P = {n_i.x <= 1 (family A)} ∩ {m_j.x <= mu (family B)}.
# Find mu where every face subtends the same solid angle 4π/N from the centre.
# Control: the cube–octahedron line must give Lucky 7, mu_f = 1 + sqrt(2T) (same scaling: cube faces at 1, octahedron |x|+|y|+|z| <= mu,
# so the octahedron's unit normals are at distance mu/sqrt3).
# Usage: fair_line.py co|di   (co = cube–octahedron control, di = dodecahedron–icosahedron)
import sys, itertools
import numpy as np
from scipy.spatial import ConvexHull
from mpmath import pslq, mp, mpf, sqrt, atan2, pi, findroot, matrix, lu_solve, tan, cos, nstr, identify, findpoly
mp.dps = 140
phi = (1 + sqrt(5)) / 2

def unit(v):
    n = sqrt(sum(c*c for c in v)); return [c/n for c in v]

def ico_vertices():
    V = []
    for s1 in (1, -1):
        for s2 in (1, -1):
            V += [(0, s1*phi, s2), (s2, 0, s1*phi), (s1*phi, s2, 0)]  # dual-aligned with dod_vertices (checked below)
    return [unit(v) for v in V]

def dod_vertices():
    V = [(a, b, c) for a in (1, -1) for b in (1, -1) for c in (1, -1)]
    for s1 in (1, -1):
        for s2 in (1, -1):
            V += [(0, s1/phi, s2*phi), (s1/phi, s2*phi, 0), (s2*phi, 0, s1/phi)]
    return [unit(v) for v in V]

mode = sys.argv[1]
AX = [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]
CORN = list(itertools.product((1,-1), repeat=3))
TET = [v for v in CORN if v[0]*v[1]*v[2] == 1]
RD = [v for v in itertools.product((1,-1,0), repeat=3) if sum(1 for c in v if c) == 2]
FAM = {'co': (AX, CORN), 'cr': (AX, RD), 'tc': (TET, AX), 'or': (CORN, RD), 'di': (None, None)}
if mode == 'di':
    A = ico_vertices(); B = dod_vertices()
else:
    A = [unit(v) for v in FAM[mode][0]]; B = [unit(v) for v in FAM[mode][1]]
scaleB = 1
N = len(A) + len(B)
planes = lambda mu: [(n, mpf(1)) for n in A] + [(m, mu*scaleB) for m in B]

def solid_angle_tri(a, b, c):
    # Van Oosterom & Strackee (1983)
    na, nb, nc = [sqrt(sum(x*x for x in v)) for v in (a, b, c)]
    trip = a[0]*(b[1]*c[2]-b[2]*c[1]) - a[1]*(b[0]*c[2]-b[2]*c[0]) + a[2]*(b[0]*c[1]-b[1]*c[0])
    dot = lambda u, v: sum(x*y for x, y in zip(u, v))
    den = na*nb*nc + dot(a,b)*nc + dot(a,c)*nb + dot(b,c)*na
    return 2*abs(atan2(trip, den))

def face_angles(mu):
    P = planes(mu)
    # combinatorics in double precision, vertices recomputed in mp from plane triples
    pts = []
    for (i, j, k) in itertools.combinations(range(len(P)), 3):
        M = matrix([[float(c) for c in P[t][0]] for t in (i, j, k)])
        Mn = np.array(M.tolist(), dtype=float)
        if abs(np.linalg.det(Mn)) < 1e-9: continue
        x = np.linalg.solve(Mn, np.array([float(P[t][1]) for t in (i, j, k)]))
        if all(float(sum(float(a)*b for a, b in zip(n, x))) <= float(d) + 1e-9 for n, d in P):
            pts.append((i, j, k))
    # exact (mp) vertices; group by face
    faces = {f: [] for f in range(len(P))}
    for (i, j, k) in pts:
        M = matrix([P[t][0] for t in (i, j, k)]); rhs = matrix([P[t][1] for t in (i, j, k)])
        x = lu_solve(M, rhs); x = [x[0], x[1], x[2]]
        for f in (i, j, k):
            if not any(all(abs(a-b) < mpf(10)**-40 for a, b in zip(x, y)) for y in faces[f]): faces[f].append(x)
    out = {}
    for f, vs in faces.items():
        if len(vs) < 3: out[f] = mpf(0); continue
        n = P[f][0]; c = [sum(v[t] for v in vs)/len(vs) for t in range(3)]
        # order around normal
        u = unit([vs[0][t]-c[t] for t in range(3)]); w = [n[1]*u[2]-n[2]*u[1], n[2]*u[0]-n[0]*u[2], n[0]*u[1]-n[1]*u[0]]
        vs = sorted(vs, key=lambda v: float(atan2(sum((v[t]-c[t])*w[t] for t in range(3)), sum((v[t]-c[t])*u[t] for t in range(3)))))
        out[f] = sum(solid_angle_tri(c, vs[t], vs[(t+1) % len(vs)]) for t in range(len(vs)))
    return out, faces

def shareA(mu):
    o, _ = face_angles(mu); return o[0]

# bracket: scan mu for faces of both families present and shareA crossing 4pi/N
target = 4*pi/N
grid = np.linspace(0.30, 3.00, 541)
prev = None; bracket = None
for g in grid:
    o, fc = face_angles(mpf(g))
    nA = sum(1 for f in range(len(A)) if o[f] > 0); nB = sum(1 for f in range(len(A), N) if o[f] > 0)
    s = float(o[0] - target) if nA == len(A) and nB == len(B) else None
    if s is not None and prev is not None and prev[1] * s < 0: bracket = (prev[0], g)
    if s is not None: prev = (g, s)
    if mode == 'co' and g == grid[0]: pass
print('mode', mode, 'faces', N, 'bracket', bracket, flush=True)
mu = findroot(lambda m: shareA(m) - target, (mpf(bracket[0]), mpf(bracket[1])), solver='anderson')
o, faces = face_angles(mu)
print('mu_f =', nstr(mu, 60))
print('checks: A share', nstr(o[0]/(4*pi), 30), ' B share', nstr(o[len(A)]/(4*pi), 30), ' total', nstr(sum(o.values())/(4*pi), 30))
sA = [o[f] for f in range(len(A))]; sB = [o[f] for f in range(len(A), N)]
sym = max(sA)-min(sA) < mpf(10)**-60 and max(sB)-min(sB) < mpf(10)**-60
print('SYMMETRY CHECK (all faces of a family equal):', 'OK' if sym else 'FAIL')
if not sym: sys.exit('FAIL')
print('face sizes A,B:', len(faces[0]), len(faces[len(A)]))
# radii (centre = origin by symmetry)
allv = [v for vs in faces.values() for v in vs]
R = max(sqrt(sum(c*c for c in v)) for v in allv); r = min(mpf(1), mu)
print('r/R =', nstr(r/R, 40), ' R =', nstr(R, 40))
for name, val in (('(R/r)^2', (R/r)**2), ('mu^2', mu**2), ('mu', mu)):
    p = None
    for d in range(1, 25):
        rel = pslq([val**k for k in range(d+1)], maxcoeff=10**9, maxsteps=10**6)
        if rel: p = (d, rel); break
    print('minpoly', name, p)
ok = sym and abs(o[0]/(4*pi) - mpf(1)/N) < mpf(10)**-60 and abs(o[len(A)]/(4*pi) - mpf(1)/N) < mpf(10)**-60 and abs(sum(o.values())/(4*pi) - 1) < mpf(10)**-60
print('FINAL ok' if ok else 'FINAL FAIL')
# Field test: does (R/r)^2 lie in Q(cos 2pi/(N/2)) together with the frame's square roots?
import sympy as sp
X = sp.symbols('x')
val = (R/r)**2; rel = None
for d in range(1, 25):
    rel = pslq([val**k for k in range(d+1)], maxcoeff=10**9, maxsteps=10**6)
    if rel: break
if rel and max(abs(c) for c in rel) < 10**7:
    P = sum(c*X**k for k, c in enumerate(rel))
    m = N // 2
    c_m = sp.cos(2*sp.pi/m)
    gen = sp.minimal_polynomial(c_m, X)
    print('N/2 =', m, ' minimal polynomial of cos(2pi/N/2):', gen)
    ext_m = [sp.cos(2*sp.pi/m).rewrite(sp.sqrt)] if m in (3, 4, 5, 6, 8, 10, 12, 16) else None
    for frame in ([], [sp.sqrt(2)], [sp.sqrt(3)], [sp.sqrt(5)]):
        if ext_m is None: break
        try:
            fl = sp.factor_list(P, extension=ext_m + frame)[1]
            print('  over Q(cos 2pi/%d)%s: factor degrees' % (m, ''.join(', ' + str(f) for f in frame)), [sp.degree(f, X) for f, _ in fl])
        except Exception as e:
            print('  factor error', e)
    if ext_m is None:
        # m = 7, 9: test by root containment numerically: is val a Q-combination of 1, c, c^2 (c = cos 2pi/m) [times frame sqrt]?
        c = mp.cos(2*pi/m); deg = sp.degree(gen, X)
        for fr_name, fr in (('', mpf(1)), ('sqrt2', sqrt(2)), ('sqrt3', sqrt(3)), ('sqrt5', sqrt(5))):
            basis = [c**k for k in range(deg)] + ([fr*c**k for k in range(deg)] if fr_name else [])
            rr = pslq([val] + basis, maxcoeff=10**6, maxsteps=10**6)
            print('  in Q(cos 2pi/%d%s)?' % (m, (', ' + fr_name) if fr_name else ''), rr)
else:
    print('no small polynomial for (R/r)^2 up to degree 24:', rel)
import json
json.dump({'mode': mode, 'mu': str(mu), 'faces': {str(f): [[nstr(c, 120) for c in v] for v in vs] for f, vs in faces.items() if len(vs) >= 3}},
          open('verts-%s.json' % mode, 'w'))
