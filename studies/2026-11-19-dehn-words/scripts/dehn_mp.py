# Dehn words (DICTO 19 Nov 2026, shape language: "the perfect math of adding shapes together"; "Yes please run away").
# Dehn(P) = sum_e L_e (x) theta_e in R (x)_Q R/Q pi. High-precision version of 2026-11-04-dehn-screen/scripts/dehn.py:
# exact corners (Q(sqrt5) or 100-digit data), 80-digit arithmetic, PSLQ among the distinct dihedral angles and pi
# (tol 1e-50, coefficients <= 2000), basis beta_j independent mod Q pi; Dehn = 0 iff every coefficient sum X_j = sum c L is 0.
# Zero is claimed at |X_j| < 1e-45 (with the relations found); nonzero at |X_j| > 1e-6. Anything between = UNDECIDED.
# Calibration (must hold): zero for cube, RD, TO, RT, golden oblate and prolate rhombohedra, the RD centre pyramid over a rhombus
# (the old float tool got this one wrong, 5 Nov); nonzero for regular tetrahedron, octahedron, icosahedron, dodecahedron.
import json, sys, itertools, numpy as np
from mpmath import mp, mpf, sqrt, atan2, pi, pslq, nstr, identify
from scipy.spatial import ConvexHull
mp.dps = 80
R5 = sqrt(5); PHI = (1 + R5)/2
def cross(a, b): return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]
def dot(a, b): return sum(x*y for x, y in zip(a, b))
def sub(a, b): return [x-y for x, y in zip(a, b)]
def nrm(a): return sqrt(dot(a, a))
def hull_faces(V):
    """faces of a convex hull as ordered index lists (float grouping, exact coordinates kept)"""
    Vf = np.array([[float(c) for c in v] for v in V]); h = ConvexHull(Vf); pl = {}
    for eq in h.equations: pl.setdefault(tuple(np.round(eq, 7)), eq)
    F = []
    for eq in pl.values():
        idx = [i for i in range(len(Vf)) if abs(Vf[i] @ eq[:3] + eq[3]) < 1e-7]
        c = Vf[idx].mean(0); u = Vf[idx[0]] - c; u /= np.linalg.norm(u); w = np.cross(eq[:3], u)
        idx.sort(key=lambda i: np.arctan2((Vf[i]-c) @ w, (Vf[i]-c) @ u)); F.append(idx)
    return F
def dehn(V, F, name):
    vol = sum(dot(V[f[0]], cross(V[f[i]], V[f[i+1]])) for f in F for i in range(1, len(f)-1))/6
    if vol < 0: F = [f[::-1] for f in F]
    def normal(f):
        n = [mpf(0)]*3
        for i in range(len(f)):
            c = cross(V[f[i]], V[f[(i+1) % len(f)]]); n = [x+y for x, y in zip(n, c)]
        L = nrm(n); return [x/L for x in n]
    N = [normal(f) for f in F]; E = {}
    for fi, f in enumerate(F):
        for i in range(len(f)): E[(f[i], f[(i+1) % len(f)])] = fi
    rows = []
    for (a, b), f1 in E.items():
        if a > b: continue
        f2 = E[(b, a)]; d = sub(V[b], V[a]); L = nrm(d); e = [x/L for x in d]
        ang = atan2(dot(cross(N[f1], N[f2]), e), dot(N[f1], N[f2]))
        if abs(ang) < mpf(10)**-60: continue
        rows.append((L, pi - ang))
    angs = []
    for L, th in rows:
        if not any(abs(th - a) < mpf(10)**-60 for a in angs): angs.append(th)
    basis, coef = [], {}
    for i, a in enumerate(angs):
        r = pslq([a] + [angs[b] for b in basis] + [pi], maxcoeff=2000, maxsteps=10**6, tol=mpf(10)**-50)
        if r is not None and r[0] != 0: coef[i] = {b: mpf(-r[1+j])/r[0] for j, b in enumerate(basis)}
        else: basis.append(i); coef[i] = {i: mpf(1)}
    X = {b: mpf(0) for b in basis}
    for L, th in rows:
        i = next(k for k, a in enumerate(angs) if abs(th - a) < mpf(10)**-60)
        for b, c in coef[i].items(): X[b] += c*L
    mx = max([abs(x) for x in X.values()] + [mpf(0)])
    verdict = 'ZERO' if mx < mpf(10)**-45 else ('NONZERO' if mx > mpf(10)**-6 else 'UNDECIDED')
    rat = sorted(set(nstr(a*180/pi, 8) for i, a in enumerate(angs) if not coef[i]))
    return {'name': name, 'faces': len(F), 'edges': len(rows), 'distinct_dihedrals': len(angs), 'independent_mod_pi': len(basis),
            'rational_pi_dihedrals_deg': rat, 'max_coefficient_sum': nstr(mx, 5), 'verdict': verdict}
def ps(t, even=False):
    out = []
    for p in itertools.permutations(range(3)):
        if even and p not in [(0,1,2),(1,2,0),(2,0,1)]: continue
        for s in itertools.product([1,-1], repeat=3):
            v = [s[i]*t[p[i]] for i in range(3)]
            if not any(all(abs(x-y) < mpf(10)**-60 for x, y in zip(v, w)) for w in out): out.append(v)
    return out
def M(*t): return [mpf(x) if not hasattr(x, 'ae') else x for x in t]
cube = ps(M(1,1,1)); octa = ps(M(1,0,0)); tet = [M(1,1,1), M(1,-1,-1), M(-1,1,-1), M(-1,-1,1)]
ico = ps(M(0,1,PHI), True); dod = cube + ps(M(0,1/PHI,PHI), True)
rd = cube + [[2*x for x in v] for v in octa]; to = ps(M(0,1,2))
AX6 = [v for v in ico if (v[0], v[1], v[2]) > (0, 0, 0)][:0] or [ico[i] for i in range(12) if all(not all(abs(x+y) < mpf(10)**-60 for x, y in zip(ico[i], ico[j])) for j in range(i))]
rt = [[sum(e*v[k] for e, v in zip(es, AX6)) for k in range(3)] for es in itertools.product((1,-1), repeat=6)]   # zonohedron of the 6 five-fold axes
a, b, c = ico[0], None, None
# golden rhombohedra: spanned by three icosahedron corners round one face (prolate) / with one reversed (oblate)
FI = hull_faces(ico); f0 = FI[0]; A, B, C = [ico[i] for i in f0]
def para(u, v, w): return [[i*u[k]+j*v[k]+l*w[k] for k in range(3)] for i in (0,1) for j in (0,1) for l in (0,1)]
prol = para(A, B, C); obl = para(A, B, [-x for x in C])
rdpyr = [M(0,0,0), M(1,1,1), M(2,0,0), M(1,1,-1), M(0,2,0)]      # centre + one rhombus of the RD (1,1,1),(2,0,0),(1,1,-1)? check below
CAL = [('cube', cube, 'ZERO'), ('rhombic dodecahedron', rd, 'ZERO'), ('truncated octahedron', to, 'ZERO'), ('rhombic triacontahedron', rt, 'ZERO'),
       ('golden prolate rhombohedron', prol, 'ZERO'), ('golden oblate rhombohedron', obl, 'ZERO'),
       ('tetrahedron', tet, 'NONZERO'), ('octahedron', octa, 'NONZERO'), ('icosahedron', ico, 'NONZERO'), ('dodecahedron', dod, 'NONZERO')]
if __name__ == '__main__':
    out = []; ok = True
    # RD centre pyramid: centre + the rhombus of RD corners (2,0,0), (1,1,1), (0,2,0), (1,1,-1)
    rhomb = [M(0,0,0), M(2,0,0), M(1,1,1), M(0,2,0), M(1,1,-1)]
    CAL.append(('RD centre pyramid over one rhombus', rhomb, 'ZERO'))
    for name, V, want in CAL:
        r = dehn(V, hull_faces(V), name); r['calibration'] = want; out.append(r); ok = ok and r['verdict'] == want
        print('CAL %-36s %-8s (want %s) faces %d dihedrals %d indep %d max %s' % (name, r['verdict'], want, r['faces'], r['distinct_dihedrals'], r['independent_mod_pi'], r['max_coefficient_sum']), flush=True)
    # the words: AXE, CLEO, FUJI (corners identified in Q(sqrt5) from the 9-digit data of 2026-10-14-axe-cleo-fuji, then exact)
    P = json.load(open(sys.argv[1]))
    def exact(x):
        if abs(x) < 1e-12: return mpf(0)
        r = pslq([mpf(repr(x)), mpf(1), R5], maxcoeff=400, maxsteps=10**5, tol=mpf(10)**-8)
        assert r and r[0] != 0, x
        v = (-mpf(r[1]) - r[2]*R5)/r[0]; assert abs(v - x) < 2e-9, (x, v); return v
    for nm in ('AXE', 'CLEO', 'FUJI'):
        V = [[exact(x) for x in v] for v in P[nm]['vertices']]
        r = dehn(V, hull_faces(V), nm); out.append(r)
        print('WORD %-12s %-8s faces %d dihedrals %d indep %d rational %s max %s' % (nm, r['verdict'], r['faces'], r['distinct_dihedrals'], r['independent_mod_pi'], r['rational_pi_dihedrals_deg'], r['max_coefficient_sum']), flush=True)
    # the twelve fair dice (#111), 100-digit corners
    for m in sys.argv[2:]:
        D = json.load(open('verts-%s.json' % m)); pts = []
        for vs in D['faces'].values():
            for v in vs:
                v = [mpf(c) for c in v]
                if not any(all(abs(x-y) < mpf(10)**-60 for x, y in zip(v, w)) for w in pts): pts.append(v)
        r = dehn(pts, hull_faces(pts), 'fair die %s (%d faces)' % (m, len(D['faces']))); out.append(r)
        print('DIE  %-22s %-8s dihedrals %d indep %d max %s' % (r['name'], r['verdict'], r['distinct_dihedrals'], r['independent_mod_pi'], r['max_coefficient_sum']), flush=True)
    json.dump(out, open('dehn-words.json', 'w'), indent=1)
    und = [r['name'] for r in out if r['verdict'] == 'UNDECIDED']
    print('undecided:', und)
    print('FINAL ok' if ok and not und else 'FINAL FAIL')
