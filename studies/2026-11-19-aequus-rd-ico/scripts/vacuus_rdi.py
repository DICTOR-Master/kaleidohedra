# The Vacuus of the fair RD ∩ icosahedron die (D191), at 100 digits, as Equanimity §5 and 2026-11-18-fair-32-die/scripts/corners.py:
# for every face, the corner angles of the spherical polygon cut from the unit sphere by the cone over the face (= the angles
# between consecutive Vacuus plates); Girard check (excess = 4π/32 on every face); which plates lie on the mirrors of Th
# (the 3 coordinate planes) and which slope; PSLQ (Ferguson–Bailey) for rational multiples of π among the corner angles and the
# plate angles (to every mirror and rotation axis of the cube's and the icosahedron's groups, and to the face's own axis plane,
# the angle of Equanimity Theorem 6). Also: side lengths per face kind (is any face regular?), the Dehn invariant (dehn_mp.py of
# 2026-11-19-dehn-words), and the corner/face dump for the figure and the catalogue picture.
# Usage: python vacuus_rdi.py <out dir>   (needs mpmath, numpy, scipy; dehn_mp.py importable from the same directory)
import itertools, json, sys, os
from mpmath import mp, mpf, sqrt, atan2, acos, pi, findroot, pslq, nstr
mp.dps = 110
out = sys.argv[1] if len(sys.argv) > 1 else '.'
phi = (1 + sqrt(5)) / 2
def u(v): n = sqrt(sum(c*c for c in v)); return [c/n for c in v]
def dot(a, b): return sum(x*y for x, y in zip(a, b))
def cross(a, b): return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]
roll = lambda q, k: tuple(q[(i - k) % 3] for i in range(3))
RD = [u(p) for p in sorted({roll(q, k) for q in [(a, b, 0) for a in (1, -1) for b in (1, -1)] for k in range(3)})]
I8 = [u(p) for p in itertools.product((1, -1), repeat=3)]
I12 = [u(p) for p in sorted({roll((0, a/phi, b*phi), k) for a in (1, -1) for b in (1, -1) for k in range(3)})]
N = RD + I8 + I12; KIND = ['RD'] * 12 + ['I8'] * 8 + ['I12'] * 12
EPS = mpf(10)**-60
def solve3(i, j, k, d):
    a, b, c = N[i], N[j], N[k]; D = dot(a, cross(b, c)); bc, ca, ab = cross(b, c), cross(c, a), cross(a, b)
    return [(d[i]*bc[t] + d[j]*ca[t] + d[k]*ab[t]) / D for t in range(3)]
TRIPLES = None
def verts(d):
    global TRIPLES
    if TRIPLES is None:
        TRIPLES, V = [], []
        for i, j, k in itertools.combinations(range(32), 3):
            if abs(dot(N[i], cross(N[j], N[k]))) < mpf(10)**-12: continue
            x = solve3(i, j, k, d)
            if all(dot(n, x) <= dd + mpf(10)**-12 for n, dd in zip(N, d)) and not any(max(abs(a-b) for a, b in zip(x, y)) < mpf(10)**-9 for y in V):
                V.append(x); TRIPLES.append((i, j, k))
    return [solve3(i, j, k, d) for i, j, k in TRIPLES]
def face_polys(d):
    V = verts(d); F = []
    for n, dd in zip(N, d):
        P = [v for v in V if abs(dot(n, v) - dd) < EPS]
        c = [sum(p[t] for p in P)/len(P) for t in range(3)]
        e1 = u([P[0][t]-c[t] for t in range(3)]); e2 = cross(n, e1)      # (e1, e2, n) right-handed: sorted CCW seen from outside
        P.sort(key=lambda p: atan2(dot([p[t]-c[t] for t in range(3)], e2), dot([p[t]-c[t] for t in range(3)], e1)))
        F.append(P)
    return V, F
def tri(a, b, c): return 2 * atan2(abs(dot(a, cross(b, c))), 1 + dot(a, b) + dot(b, c) + dot(c, a))   # Van Oosterom–Strackee
def omegas(m1, m2):
    d = [mpf(1)]*12 + [m1]*8 + [m2]*12; V, F = face_polys(d); o = []
    for n, P in zip(N, F):
        c = u([sum(p[t] for p in P) for t in range(3)])
        o.append(sum(tri(c, u(P[i]), u(P[(i+1) % len(P)])) for i in range(len(P))))
    return o
T = 4*pi/32
m1, m2 = findroot(lambda a, b: (lambda o: [o[12] - T, o[20] - T])(omegas(a, b)),
                  (mpf('1.00275925096526736511385882249432921691204423331627286783923'),
                   mpf('1.01066394259642760139472117979255505248970311395773977913196')), tol=mpf(10)**-95)
d = [mpf(1)]*12 + [m1]*8 + [m2]*12
V, F = face_polys(d); om = omegas(m1, m2)
print('m1 =', nstr(m1, 40)); print('m2 =', nstr(m2, 40))
print('max |Omega - 4pi/32| (Van Oosterom-Strackee fans) =', nstr(max(abs(o - T) for o in om), 3), '| corners', len(V))
# ---- the Vacuus: plates, corner angles, Girard
RC = {}
def rat(a, maxc=500):
    if abs(a) < EPS: return '0'
    key = nstr(a, 50)
    if key in RC: return RC[key]
    RC[key] = _rat(a, maxc); return RC[key]
def _rat(a, maxc):
    r = pslq([a, pi], maxcoeff=maxc, maxsteps=10**6)
    if r and r[0] != 0:
        p, q = -r[1], r[0]
        if q < 0: p, q = -p, -q
        return '%d/%d' % (p, q)
    return None
def uniq(L):
    o = []
    for m in L:
        m = u(m)
        if not any(abs(abs(dot(m, q)) - 1) < EPS for q in o): o.append(m)
    return o
TH = uniq([(1,0,0),(0,1,0),(0,0,1)])
OH = uniq([(1,0,0),(0,1,0),(0,0,1),(1,1,0),(1,-1,0),(1,0,1),(1,0,-1),(0,1,1),(0,1,-1)])
IH = uniq([(1,0,0),(0,1,0),(0,0,1)] + [p for s1, s2 in itertools.product((1,-1), repeat=2) for p in ((1, s1*phi, s2/phi), (s2/phi, 1, s1*phi), (s1*phi, s2/phi, 1))])
AXES = uniq([v for v in itertools.product((1,0,-1), repeat=3) if any(v)] + IH +
            [p for s1, s2 in itertools.product((1,-1), repeat=2) for p in ((0, s1, s2*phi), (s2*phi, 0, s1), (s1, s2*phi, 0))] +
            [p for s1, s2 in itertools.product((1,-1), repeat=2) for p in ((0, s1/phi, s2*phi), (s1/phi, s2*phi, 0), (s2*phi, 0, s1/phi))])
ok = len(V) == 60 and max(abs(o - T) for o in om) < mpf(10)**-80
rational = []; seen = {}; plates = {}
for fi, (n, P) in enumerate(zip(N, F)):
    k = len(P); W = [u(p) for p in P]
    side = [sqrt(sum((P[i][t] - P[(i+1) % k][t])**2 for t in range(3))) for i in range(k)]
    pl = [u(cross(W[i], W[(i+1) % k])) for i in range(k)]                      # plate i: centre, P[i], P[i+1]
    onTH = [any(abs(abs(dot(p, m)) - 1) < EPS for m in TH) for p in pl]
    onOI = [any(abs(abs(dot(p, m)) - 1) < EPS for m in OH + IH) for p in pl]
    alpha = []
    for i in range(k):
        a, b, x = W[i-1], W[(i+1) % k], W[i]
        t1 = u([a[t] - dot(a, x)*x[t] for t in range(3)]); t2 = u([b[t] - dot(b, x)*x[t] for t in range(3)])
        alpha.append(acos(dot(t1, t2)))
    exc = sum(alpha) - (k-2)*pi
    if abs(exc - T) > mpf(10)**-80: ok = False
    ra = [rat(a) for a in alpha]
    rows = []
    for i in range(k):
        # plate angles: to the 3 mirrors of Th, to every mirror/rotation axis of the cube's and icosahedron's groups,
        # and to the plane through the face axis n and either end of its edge (Equanimity Theorem 6)
        ang = [acos(min(mpf(1), abs(dot(pl[i], m)))) for m in AXES]
        ax = [u(cross(n, W[i])), u(cross(n, W[(i+1) % k]))]
        ang += [acos(min(mpf(1), abs(dot(pl[i], q)))) for q in ax]
        rr = sorted(set(r for r in (rat(a) for a in ang) if r and r != '0' and r != '1/2'))
        rows.append(('mirror' if onTH[i] else 'slope', 'on an Oh/Ih mirror' if onOI[i] and not onTH[i] else '', tuple(rr)))
        plates[tuple(sorted([tuple(nstr(c, 30) for c in P[i]), tuple(nstr(c, 30) for c in P[(i+1) % k])]))] = (P[i], P[(i+1) % k], not onTH[i])
        if rr: rational.append((KIND[fi], fi, i, rr))
    sides = sorted(set(nstr(s, 12) for s in side))
    key = (KIND[fi], k, tuple(sides), tuple(r or nstr(a/pi, 15) + '(irr)' for r, a in zip(ra, alpha)), tuple(rows))
    seen.setdefault(key, []).append(fi)
    if any(ra): rational.append((KIND[fi], fi, 'corner', ra))
print('Girard: excess = 4pi/32 on every face (to 1e-80):', 'yes' if ok else 'NO')
for (kind, k, sides, al, rows), fs in seen.items():
    print('\n%s faces %s: %d sides; side lengths %s' % (kind, fs, k, list(sides)))
    print('   corner angles (x pi): %s' % ' '.join(al))
    for i, (s, x, rr) in enumerate(rows): print('   plate %d: %s %s | rational angles (x pi, excluding 0 and 1/2): %s' % (i, s, x, list(rr)))
nsl = sum(1 for v in plates.values() if v[2])
print('\nplates: %d (= edges), on Th mirrors %d, sloping %d' % (len(plates), len(plates) - nsl, nsl))
print('rational multiples of pi found (corner angles, or plate angles other than 0 and pi/2):', rational if rational else 'none')
# regular faces?
reg = [fi for fi, P in enumerate(F) if len(set(nstr(sqrt(sum((P[i][t]-P[(i+1) % len(P)][t])**2 for t in range(3))), 20) for i in range(len(P)))) == 1]
print('faces with all sides equal:', reg if reg else 'none')
# ---- dump for the figure and the catalogue picture
uv = []
for v in V:
    if not any(max(abs(a-b) for a, b in zip(v, w)) < EPS for w in uv): uv.append(v)
idx = lambda p: next(i for i, w in enumerate(uv) if max(abs(a-b) for a, b in zip(p, w)) < EPS)
json.dump({'mode': 'rdi', 'm1': nstr(m1, 105), 'm2': nstr(m2, 105),
           'faces': {str(i): [[nstr(c, 105) for c in p] for p in P] for i, P in enumerate(F)}}, open(os.path.join(out, 'verts-rdi.json'), 'w'))
json.dump({'name': 'Aequus 32 (rhombic dodecahedron ∩ icosahedron)', 'd_number': 'D191', 'status': 'new', 'convex': 'True',
           'vertices': [{'decimal': [nstr(c, 20) for c in v]} for v in uv],
           'faces': [[idx(p) for p in P] for P in F]}, open(os.path.join(out, 'aequus-32-rdi.json'), 'w'))
# ---- Dehn invariant (2026-11-19-dehn-words/scripts/dehn_mp.py, unchanged, imported)
sys.argv = sys.argv[:1]
import dehn_mp
dehn_mp.mp.dps = 80
pts = [[dehn_mp.mpf(nstr(c, 100)) for c in v] for v in uv]
r = dehn_mp.dehn(pts, dehn_mp.hull_faces(pts), 'D191')
print('\nDehn:', r)
mp.dps = 110
print('FINAL ok' if ok and len(uv) == 60 and r['verdict'] != 'UNDECIDED' else 'FINAL FAIL')
