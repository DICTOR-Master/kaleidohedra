# Hand-proof support for Conjecture A: for every face of each fair die, the corner angles of the spherical polygon
# cut from the unit sphere by the cone over the face (angles between consecutive Vacuus plates), as multiples of pi,
# and, for each sloping plate, its neighbour plate at each end: a mirror plate, or its own mirror image.
# Girard: sum(alpha) - (n-2)pi = 4pi/N must hold on every face (check).
# Control: Lucky 7 (co) square-face corners must be 4pi/7 and the sloping plate normal at 2pi/7 to a 4-fold axis.
import json, itertools, sys
from mpmath import mp, mpf, sqrt, acos, pi, pslq, nstr, atan2
mp.dps = 110
phi = (1 + sqrt(5)) / 2
def unit(v): n = sqrt(sum(c*c for c in v)); return [c/n for c in v]
def cross(a, b): return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]
def dot(a, b): return sum(x*y for x, y in zip(a, b))
def rat(a):
    if abs(a) < mpf(10)**-60: return '0'
    rel = pslq([a, pi], maxcoeff=500, maxsteps=10**6)
    if rel and rel[0] != 0:
        p, q = -rel[1], rel[0]
        if q < 0: p, q = -p, -q
        return '%d/%d' % (p, q)
    return None
def uniq(L):
    out = []
    for m in L:
        m = unit(m)
        if not any(abs(abs(dot(m, q)) - 1) < mpf(10)**-60 for q in out): out.append(m)
    return out
# mirror normals: Oh (9), Td (6 diagonal), Ih (15 two-fold axes)
OH = uniq([(1,0,0),(0,1,0),(0,0,1),(1,1,0),(1,-1,0),(1,0,1),(1,0,-1),(0,1,1),(0,1,-1)])
TD = uniq([(1,1,0),(1,-1,0),(1,0,1),(1,0,-1),(0,1,1),(0,1,-1)])
IH = uniq([(1,0,0),(0,1,0),(0,0,1)] + [p for s1, s2 in itertools.product((1,-1), repeat=2) for p in ((1, s1*phi, s2/phi), (s2/phi, 1, s1*phi), (s1*phi, s2/phi, 1))])
NF = {'rdd': 24, 'cd': 18, 'od': 20, 'td': 16, 'tc': 10, 'co': 14, 'tr': 16, 'cr': 18, 'or': 20, 'di': 32, 'dt': 42, 'it': 50}
ok = True
for mode in sys.argv[1:]:
    TH = uniq([(1,0,0),(0,1,0),(0,0,1)])     # pyritohedral group: the 3 coordinate mirrors only
    mirrors = IH if mode in ('di', 'dt', 'it') else (TD if mode in ('tc', 'tr') else (TH if mode in ('cd', 'od') else ([] if mode == 'td' else OH)))
    # all rotation axes of the cube and the icosahedron, for the angle test on the mixed lines
    AXES = uniq([v for v in itertools.product((1,0,-1), repeat=3) if any(v)] + IH +
                [p for s1, s2 in itertools.product((1,-1), repeat=2) for p in ((0, s1, s2*phi), (s2*phi, 0, s1), (s1, s2*phi, 0))] +
                [p for s1, s2 in itertools.product((1,-1), repeat=2) for p in ((0, s1/phi, s2*phi), (s1/phi, s2*phi, 0), (s2*phi, 0, s1/phi))])
    N = NF[mode]
    D = json.load(open('verts-%s.json' % mode))
    faces = [[[mpf(c) for c in v] for v in vs] for vs in D['faces'].values() if len(vs) >= 3]
    assert len(faces) == N, (mode, len(faces))
    seen = {}
    for vs in faces:
        n = len(vs); c = [sum(v[t] for v in vs)/n for t in range(3)]
        nn = unit(c); u = unit([vs[0][t]-c[t] for t in range(3)]); w = cross(nn, u)
        vs = sorted(vs, key=lambda v: float(atan2(dot([v[t]-c[t] for t in range(3)], w), dot([v[t]-c[t] for t in range(3)], u))))
        V = [unit(v) for v in vs]
        P = [unit(cross(V[i], V[(i+1) % n])) for i in range(n)]          # plate i through V[i], V[i+1]
        onm = [any(abs(abs(dot(p, m)) - 1) < mpf(10)**-60 for m in mirrors) for p in P]
        alpha = []
        for i in range(n):
            a, b, x = V[i-1], V[(i+1) % n], V[i]
            t1 = unit([a[t] - dot(a, x)*x[t] for t in range(3)]); t2 = unit([b[t] - dot(b, x)*x[t] for t in range(3)])
            alpha.append(acos(dot(t1, t2)))
        exc = sum(alpha) - (n-2)*pi
        if abs(exc - 4*pi/N) > mpf(10)**-80: ok = False
        # each sloping plate: its angle to each mirror normal, and its neighbours
        rows = []
        for i in range(n):
            if onm[i]: continue
            th = [rat(acos(min(mpf(1), abs(dot(P[i], m))))) for m in (AXES if mode in ('cd', 'od', 'td') else mirrors)]
            th = sorted(set(t for t in th if t))
            nb = []
            for j, corner in (((i-1) % n, i), ((i+1) % n, (i+1) % n)):
                if onm[j]: nb.append('mirror plate, corner %s' % rat(alpha[corner]))
                else:
                    refl = [m for m in mirrors if all(abs(P[j][t] - (P[i][t] - 2*dot(P[i], m)*m[t])) < mpf(10)**-60 for t in range(3))]
                    nb.append(('own mirror image across a mirror' if refl else 'other sloping plate') + ', corner %s' % rat(alpha[corner]))
            rows.append((tuple(th), tuple(nb)))
        key = (n, tuple(rat(a) or nstr(a/pi, 12) + '(irr)' for a in alpha), tuple(sorted(set(rows))))
        seen[key] = seen.get(key, 0) + 1
    print('== %s  N=%d  Girard excess = 4pi/N on all faces: %s' % (mode, N, 'yes' if ok else 'NO'))
    for (n, al, rows), cnt in seen.items():
        print('  %d faces with %d sides; corner angles (x pi): %s' % (cnt, n, ' '.join(al)))
        for th, nb in rows: print('     sloping plate: rational angles to mirror normals %s | neighbours: %s' % (list(th), '; '.join(nb)))
print('FINAL ok' if ok else 'FINAL FAIL')
