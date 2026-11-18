# Vacuus of each fair die: one plate through the centre and each edge. For each plate class: whether it lies on a mirror of the
# symmetry group, its kind (full sheet: the plate also holds the opposite edge; shared: two or more edges; single fin), and the angle
# between its normal and the nearest mirror normal: is angle/pi rational (polygon angle)? PSLQ on [angle, pi] at 100 digits.
import json, itertools, sys
from mpmath import mp, mpf, sqrt, acos, pi, pslq, nstr
mp.dps = 110
phi = (1 + sqrt(5)) / 2
def unit(v): n = sqrt(sum(c*c for c in v)); return [c/n for c in v]
def cross(a, b): return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]
def dot(a, b): return sum(x*y for x, y in zip(a, b))
CUBIC_MIRRORS = [unit(v) for v in [(1,0,0),(0,1,0),(0,0,1),(1,1,0),(1,-1,0),(1,0,1),(1,0,-1),(0,1,1),(0,1,-1)]]
TET_MIRRORS = [unit(v) for v in [(1,1,0),(1,-1,0),(1,0,1),(1,0,-1),(0,1,1),(0,1,-1)]]
def ico_mirrors():
    # 15 mirrors of the icosahedral group: normals = the 30 edge-midpoint directions of the icosahedron (cyclic perms of (0,0,1),(1/2, phi/2, 1/(2phi)) with signs)
    M = []
    for v in [(1,0,0),(0,1,0),(0,0,1)]: M.append(unit(v))
    for s1, s2 in itertools.product((1,-1), repeat=2):
        for p in ((1, s1*phi, s2/phi), (s2/phi, 1, s1*phi), (s1*phi, s2/phi, 1)):
            M.append(unit(p))
    out = []
    for m in M:
        if not any(abs(abs(dot(m, q)) - 1) < mpf(10)**-60 for q in out): out.append(m)
    return out
MIR = {'co': CUBIC_MIRRORS, 'cr': CUBIC_MIRRORS, 'or': CUBIC_MIRRORS, 'tc': TET_MIRRORS, 'di': ico_mirrors()}
allok = True
for mode in sys.argv[1:]:
    D = json.load(open('verts-%s.json' % mode)); mirrors = MIR[mode]
    faces = [[[mpf(c) for c in v] for v in vs] for vs in D['faces'].values()]
    key = lambda v: tuple(round(float(c), 9) for c in v)
    edges = {}
    for vs in faces:
        n = len(vs)
        # vertices are not in cyclic order in the dump: an edge = a pair whose midpoint-direction is extreme; use convex order by angle
        c = [sum(v[t] for v in vs)/n for t in range(3)]
        nn = unit(c); u = unit([vs[0][t]-c[t] for t in range(3)]); w = cross(nn, u)
        from mpmath import atan2
        vs = sorted(vs, key=lambda v: float(atan2(dot([v[t]-c[t] for t in range(3)], w), dot([v[t]-c[t] for t in range(3)], u))))
        for i in range(n):
            a, b = vs[i], vs[(i+1) % n]
            edges[tuple(sorted([key(a), key(b)]))] = (a, b)
    plates = {}
    for a, b in edges.values():
        nrm = unit(cross(a, b)); k = tuple(round(abs(float(x)), 9) for x in nrm)  # class up to sign
        k = tuple(sorted(k))  # coarse class key (up to coordinate permutation)
        plates.setdefault(tuple(round(float(x), 9) if nrm[[abs(float(y)) > 1e-12 for y in nrm].index(True)] > 0 else round(-float(x), 9) for x in nrm), []).append((a, b, nrm))
    print('==', mode, '| faces', len(faces), '| edges', len(edges), '| plates', len(plates))
    classes = {}
    for pk, lst in plates.items():
        nrm = lst[0][2]
        on_mirror = any(abs(abs(dot(nrm, m)) - 1) < mpf(10)**-60 for m in mirrors)
        ang = min(acos(min(mpf(1), abs(dot(nrm, m)))) for m in mirrors)
        kind = 'single fin' if len(lst) == 1 else ('full sheet (edge + opposite)' if len(lst) == 2 and all(abs(x + y) < 1e-50 for x, y in zip(lst[0][0], [-t for t in lst[1][0]]) ) or len(lst) == 2 else 'shared (%d edges)' % len(lst))
        ck = (on_mirror, len(lst), nstr(ang, 12))
        classes.setdefault(ck, []).append(ang)
    for (onm, ne, angs), lst in sorted(classes.items()):
        rel = None if onm else pslq([lst[0], pi], maxcoeff=1000, maxsteps=10**6)
        poly = '' if onm else (' | angle/pi = %s' % ('%d/%d' % (-rel[1], rel[0]) if rel else 'not a fraction with denominator <= 1000'))
        print('  %3d plates | %s | edges per plate %d | angle to nearest mirror %s rad%s' % (len(lst), 'ON MIRROR' if onm else 'off mirrors', ne, angs, poly))
print('FINAL ok' if allok else 'FINAL FAIL')
