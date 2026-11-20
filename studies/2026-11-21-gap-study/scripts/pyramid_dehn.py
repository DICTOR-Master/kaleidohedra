# Centre pyramids of the icosidodecahedron (ID) and the cuboctahedron (CO): the Dehn count (#44's test).
# Gap study 2026-11-21, grid cells "ID x DEHN" and "CO x DEHN".
# Exact: sympy algebraic numbers. Floats are used only to find the faces of the hull; every number used in a claim is exact.
# Controls: cube, RD (pyramids Dehn zero, rational angles), tetrahedron (its pyramid alone is nonzero),
#           the rationality test on cos(pi/5) (rational multiple of pi) and on 1/3 (irrational).
import itertools, sys
import numpy as np
from scipy.spatial import ConvexHull
import sympy as sp
from sympy import sqrt, Rational as Q

x = sp.Symbol('x')
phi = (1 + sqrt(5)) / 2
FAIL = []

def check(label, ok):
    print(('ok   ' if ok else 'FAIL ') + label); sys.stdout.flush()
    if not ok: FAIL.append(label)

def faces_of(V):
    P = np.array([[float(c) for c in v] for v in V]); h = ConvexHull(P)
    out = {}
    for eq in h.equations:
        n, d = eq[:3], eq[3]
        S = tuple(sorted(i for i in range(len(P)) if abs(P[i] @ n + d) < 1e-9))
        out[S] = n
    faces = []
    for S, n in out.items():
        c = P[list(S)].mean(0); u = P[S[0]] - c; u /= np.linalg.norm(u); w = np.cross(n, u)
        ang = [np.arctan2((P[i] - c) @ w, (P[i] - c) @ u) for i in S]
        faces.append([S[k] for k in np.argsort(ang)])
    return faces

def vec(V, i): return sp.Matrix(V[i])
def perp(u, d):  # component of u perpendicular to d
    return u - (u.dot(d) / d.dot(d)) * d
def cosang(u, w):
    return sp.radsimp(sp.simplify(u.dot(w) / sp.sqrt(u.dot(u) * w.dot(w))))

def pyramid_edges(V, F):
    """Edges of the centre pyramid over face F (corner indices in cyclic order): (kind, exact length, exact cos of dihedral)."""
    O = sp.Matrix([0, 0, 0]); n = len(F); cen = sum((vec(V, i) for i in F), sp.zeros(3, 1)) / n
    E = []
    for k in range(n):
        p, q = vec(V, F[k]), vec(V, F[(k + 1) % n]); d = q - p
        E.append(('base', sp.sqrt(d.dot(d)), cosang(perp(cen - p, d), perp(O - p, d))))
    for k in range(n):
        v = vec(V, F[k]); a, b = vec(V, F[k - 1]), vec(V, F[(k + 1) % n])
        E.append(('lateral', sp.sqrt(v.dot(v)), cosang(perp(a, v), perp(b, v))))
    return E

def totient(n): return sp.totient(n)

def rational_pi(c):
    """Exact test: is arccos(c)/pi rational?  True iff, for some n with phi(n) = 2*deg(c) (or n <= 2 when deg 1),
    the minimal polynomial of c divides T_n(x) - 1 (then cos(n*theta) = 1).  If theta = 2*pi*k/n in lowest terms,
    cos(theta) has degree phi(n)/2, so the list of n is complete."""
    mp = sp.Poly(sp.minimal_polynomial(c, x), x); d = mp.degree()
    cands = [n for n in range(1, 8 * d * d + 9) if (n <= 2 and d == 1) or (n >= 3 and totient(n) == 2 * d)]
    for n in cands:
        T = sp.Poly(sp.chebyshevt(n, x) - 1, x)
        if T.rem(mp).is_zero:
            return True, n
    return False, None

# ---- controls for the rationality test
check('rational_pi(cos pi/5) is rational', rational_pi(phi / 2)[0])
check('rational_pi(1/3) is irrational (arccos 1/3)', not rational_pi(Q(1, 3))[0])
check('rational_pi(-1/2) is rational (120 deg)', rational_pi(Q(-1, 2))[0])

def evenperms(t):
    a, b, c = t; return [(a, b, c), (b, c, a), (c, a, b)]
def signs(t):
    out = set()
    for s in itertools.product([1, -1], repeat=3):
        out.add(tuple(si * ti for si, ti in zip(s, t)))
    return list(out)
def allperms(t): return list(set(itertools.permutations(t)))

def dedupe(L):
    out = []
    for v in L:
        if not any(all(sp.simplify(a - b) == 0 for a, b in zip(v, w)) for w in out): out.append(v)
    return out

solids = {}
solids['cube'] = [p for p in itertools.product([1, -1], repeat=3)]
solids['RD'] = solids['cube'] + [p for s in signs((2, 0, 0)) for p in allperms(s)]
solids['tetrahedron'] = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
solids['CO'] = [p for s in signs((1, 1, 0)) for p in allperms(s)]
ID = [p for s in signs((0, 0, phi)) for p in allperms(s)]
ID += [p for s in signs((Q(1, 2), phi / 2, phi ** 2 / 2)) for p in evenperms(s)]
solids['ID'] = ID
for k in solids: solids[k] = dedupe([tuple(sp.nsimplify(c) if not isinstance(c, sp.Basic) else c for c in v) for v in solids[k]])
check('ID has 30 corners', len(solids['ID']) == 30)
check('CO has 12 corners', len(solids['CO']) == 12)
check('RD has 14 corners', len(solids['RD']) == 14)

summary = {}
for name, V in solids.items():
    F = faces_of(V)
    kinds = {}
    for f in F:
        E = pyramid_edges(V, f)
        key = len(f)
        rec = sorted((k, sp.nsimplify(sp.simplify(L)), sp.simplify(c)) for k, L, c in [(a, sp.simplify(b), c) for a, b, c in E])
        kinds.setdefault(key, rec)
        rep = kinds[key]
        def same(r1, r2): return r1[0] == r2[0] and sp.simplify(r1[1] - r2[1]) == 0 and sp.simplify(r1[2] - r2[2]) == 0
        pool = list(rep); okm = len(rec) == len(rep)
        for r in rec:
            j = next((j for j, r2 in enumerate(pool) if same(r, r2)), None)
            if j is None: okm = False; break
            pool.pop(j)
        if not okm: check(f'{name}: {key}-gon pyramid edge data differs between faces', False)
    check(f'{name}: all pyramids over faces of the same size have the same edge data (exact)', True)
    summary[name] = kinds
    print(f'--- {name}: {len(V)} corners, faces by size', {k: sum(1 for f in F if len(f) == k) for k in kinds})
    for k, rec in kinds.items():
        agg = {}
        for kind, L, c in rec:
            agg.setdefault((kind, str(L), str(c)), 0); agg[(kind, str(L), str(c))] += 1
        for (kind, L, c), m in agg.items():
            rp = rational_pi(sp.sympify(c))
            print(f'    {k}-gon pyramid: {m} x {kind} edge, length {L}, cos(dihedral) = {c}, angle/pi rational: {rp[0]}' + (f' (n = {rp[1]})' if rp[0] else ''))

# ---- cube and RD: every pyramid angle is a rational multiple of pi, so each pyramid alone has Dehn invariant zero
for name in ['cube', 'RD']:
    ok = all(rational_pi(c)[0] for rec in summary[name].values() for _, _, c in rec)
    check(f'control {name}: every centre-pyramid dihedral is a rational multiple of pi (Dehn zero)', ok)
# ---- tetrahedron control: its centre pyramid has an irrational angle (alone it cannot fill space, #44)
ok = any(not rational_pi(c)[0] for rec in summary['tetrahedron'].values() for _, _, c in rec)
check('control tetrahedron: its centre pyramid has an irrational dihedral', ok)

# ---- CO: pieces are the regular tetrahedron (edge sqrt2) and the half-octahedron; t = arccos(1/3)
t3 = summary['CO'][3]; t4 = summary['CO'][4]
check('CO triangle pyramid: all six dihedrals have cos 1/3 (regular tetrahedron)', all(sp.simplify(c - Q(1, 3)) == 0 for _, _, c in t3))
check('CO triangle pyramid: all six edges sqrt2', all(sp.simplify(L - sqrt(2)) == 0 for _, L, _ in t3))
base4 = [c for k, L, c in t4 if k == 'base']; lat4 = [c for k, L, c in t4 if k == 'lateral']
# cos((pi - t)/2) = sin(t/2) = +sqrt((1 - cos t)/2) = 1/sqrt3, since (pi - t)/2 lies in (0, pi/2)
check('CO square pyramid: base dihedrals cos = 1/sqrt3 = sin(t/2) = cos((pi - t)/2)', all(sp.simplify(c - 1 / sqrt(3)) == 0 for c in base4) and sp.simplify((1 - Q(1, 3)) / 2 - Q(1, 3)) == 0)
check('CO square pyramid: lateral dihedrals cos = -1/3 = cos(pi - t)', all(sp.simplify(c + Q(1, 3)) == 0 for c in lat4))
check('CO square pyramid: all eight edges sqrt2', all(sp.simplify(L - sqrt(2)) == 0 for _, L, _ in t4))
# Dehn(T) = 6 sqrt2 (x) t ; Dehn(S) = 4 sqrt2 (x) (pi - t)/2 + 4 sqrt2 (x) (pi - t) = -6 sqrt2 (x) t  (mod pi)
print('CO: Dehn(T) = 6*sqrt2 (x) t,  Dehn(S) = -2*sqrt2 (x) t - 4*sqrt2 (x) t = -6*sqrt2 (x) t;  n3*T + n4*S = 0 iff n3 = n4')
check('CO: t = arccos(1/3) is irrational in pi, so the count is exactly n3 = n4 (the octet: one tetrahedron per half-octahedron)', not rational_pi(Q(1, 3))[0])

# ---- ID: the proof
P3 = summary['ID'][3]; P5 = summary['ID'][5]
def only(rec, kind):
    vals = [(L, c) for k, L, c in rec if k == kind]
    L0, c0 = vals[0]
    for L, c in vals[1:]:   # exact equality: minimal polynomial of the difference is x
        assert sp.minimal_polynomial(sp.sympify(L) - L0, x) == x and sp.minimal_polynomial(sp.sympify(c) - c0, x) == x, (L, c, L0, c0)
    return L0, c0
L3b, ca3 = only(P3, 'base'); L3l, cb3 = only(P3, 'lateral'); L5b, ca5 = only(P5, 'base'); L5l, cb5 = only(P5, 'lateral')
check('ID: base edges have length 1, lateral edges length phi (circumradius)', all(sp.simplify(a - b) == 0 for a, b in [(L3b, 1), (L5b, 1), (L3l, phi), (L5l, phi)]))
sa3, sa5, sb3, sb5 = [sp.sqrt(1 - c ** 2) for c in (ca3, ca5, cb3, cb5)]  # all angles lie in (0, pi), so sin > 0
cos_b_sum = sp.simplify(sp.radsimp(cb3 * cb5 - sb3 * sb5))
check('ID: beta3 + beta5 = pi exactly (cos of the sum = -1): the four lateral wedges round a corner, T P T P, fill 2 pi', sp.simplify(sp.minimal_polynomial(cos_b_sum, x) - (x + 1)) == 0)
cdelta = sp.simplify(sp.radsimp(ca3 * ca5 - sa3 * sa5))
cdelta_known = -sp.sqrt((5 + 2 * sp.sqrt(5)) / 15)
check('ID: alpha3 + alpha5 = delta, the ID dihedral, cos = -sqrt((5 + 2 sqrt5)/15)', sp.simplify(sp.minimal_polynomial(cdelta - cdelta_known, x) - x) == 0)
rb, nb = rational_pi(cb3); rd, nd = rational_pi(cdelta)
check('ID: the pentagon pyramid base angle alpha5 equals beta3 (both cos = 1/sqrt5)', sp.minimal_polynomial(ca5 - cb3, x) == x)
print('ID: cos beta3 =', cb3, ' minimal polynomial', sp.minimal_polynomial(cb3, x))
print('ID: cos delta =', cdelta_known, ' minimal polynomial', sp.minimal_polynomial(cdelta_known, x))
check('ID: beta3/pi is irrational', not rb)
check('ID: delta/pi is irrational', not rd)
check('ID: 1 and phi are linearly independent over Q (phi irrational)', sp.minimal_polynomial(phi, x).as_poly().degree() == 2)
print('ID: n3*Dehn(P3) + n5*Dehn(P5) = 1 (x) (3 n3 alpha3 + 5 n5 alpha5) + phi (x) (3 n3 beta3 + 5 n5 beta5)')
print('    = 1 (x) (3 n3 alpha3 + 5 n5 (delta - alpha3)) + phi (x) (3 n3 - 5 n5) beta3   (mod Q pi)')
print('    phi-part zero and beta3 irrational  =>  3 n3 = 5 n5 = m;  then the 1-part is m*delta, zero only if m = 0 (delta irrational).')
print('THEOREM (ID x DEHN): no nonzero set of the icosidodecahedron\'s centre pyramids (with any multiplicities) has Dehn invariant zero;')
print('    by #44 Lemma 1 (edge counting, several kinds of tile) no set of them fills space.')
print('FINAL ok' if not FAIL else f'FINAL FAIL {FAIL}')
