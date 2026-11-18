# Off-mirror Vacuus plates of each fair die: angle of the plate normal to every symmetry axis; report the angles that are
# rational multiples of pi (denominator <= 200), PSLQ at 100 digits. Control: Lucky 7 must show 2pi/7 to two cube axes.
import json, itertools, sys
from mpmath import mp, mpf, sqrt, acos, pi, pslq, nstr, atan2
mp.dps = 110
phi = (1 + sqrt(5)) / 2
def unit(v): n = sqrt(sum(c*c for c in v)); return [c/n for c in v]
def cross(a, b): return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]
def dot(a, b): return sum(x*y for x, y in zip(a, b))
def uniq(L):
    out = []
    for m in L:
        m = unit(m)
        if not any(abs(abs(dot(m, q)) - 1) < mpf(10)**-60 for q in out): out.append(m)
    return out
CUB = uniq([v for v in itertools.product((1,0,-1), repeat=3) if any(v)])          # 4-, 3- and 2-fold axes (and more) of the cube
ICO = uniq([p for s1, s2 in itertools.product((1,-1), repeat=2) for p in ((0, s1, s2*phi), (s2*phi, 0, s1), (s1, s2*phi, 0))] +   # 5-fold
           [p for p in itertools.product((1,-1), repeat=3)] + [p for s1, s2 in itertools.product((1,-1), repeat=2) for p in ((0, s1/phi, s2*phi), (s1/phi, s2*phi, 0), (s2*phi, 0, s1/phi))] +  # 3-fold
           [(1,0,0),(0,1,0),(0,0,1)] + [p for s1, s2 in itertools.product((1,-1), repeat=2) for p in ((1, s1*phi, s2/phi), (s2/phi, 1, s1*phi), (s1*phi, s2/phi, 1))])  # 2-fold
CUBIC_MIRRORS = uniq([(1,0,0),(0,1,0),(0,0,1),(1,1,0),(1,-1,0),(1,0,1),(1,0,-1),(0,1,1),(0,1,-1)])
ok = True
for mode in sys.argv[1:]:
    axes = ICO if mode in ('di', 'dt', 'it') else CUB
    D = json.load(open('verts-%s.json' % mode))
    faces = [[[mpf(c) for c in v] for v in vs] for vs in D['faces'].values()]
    found = set()
    for vs in faces:
        n = len(vs); c = [sum(v[t] for v in vs)/n for t in range(3)]
        nn = unit(c); u = unit([vs[0][t]-c[t] for t in range(3)]); w = cross(nn, u)
        vs = sorted(vs, key=lambda v: float(atan2(dot([v[t]-c[t] for t in range(3)], w), dot([v[t]-c[t] for t in range(3)], u))))
        for i in range(n):
            nrm = unit(cross(vs[i], vs[(i+1) % n]))
            # off every axis-perpendicular mirror? (mirror planes of these groups are perpendicular to 2-fold or 4-fold axes)
            angs = []
            for ax in axes:
                a = acos(min(mpf(1), abs(dot(nrm, ax))))
                if a < mpf(10)**-50: continue
                rel = pslq([a, pi], maxcoeff=200, maxsteps=10**6)
                if rel and rel[0] != 0: angs.append('%d/%d' % (-rel[1], rel[0]) if rel[0] > 0 else '%d/%d' % (rel[1], -rel[0]))
            found.add((tuple(sorted(set(angs))), nstr(min(acos(min(mpf(1), abs(dot(nrm, ax)))) for ax in axes), 10)))
    print('==', mode)
    for f in sorted(found): print('   plate class: rational angles to axes (x pi):', list(f[0]) or 'none', '| smallest angle to an axis', f[1])
    if mode == 'co' and not any('2/7' in f[0] for f in found): ok = False
print('FINAL ok' if ok else 'FINAL FAIL (control: Lucky 7 2pi/7 not found)')
