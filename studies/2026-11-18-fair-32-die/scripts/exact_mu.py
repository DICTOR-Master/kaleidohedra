# Closed form of every fair die from the hand proof (Theorem 7 draft):
# the regular m-gon face (m = order of its axis) has corner angle alpha = ((m-2)pi + 4pi/N)/m (Girard),
# the sloping plate meets the corner mirror's normal at theta = alpha/2, so a corner lies at polar angle rho from the axis with
# cos rho = cot(pi/m) cot(theta) (right spherical triangle centre-corner-edge midpoint), tan rho = t = sqrt(tan^2(pi/m) tan^2(theta) - 1).
# A plane b of the other family through that corner then gives mu in closed form: d_b = d (b.a + t b.u).
# Checks against the computed mu (100 digits) on all eight lines. Control: co must give mu = (1 + sqrt(2T))/sqrt3 (Lucky 7).
import json, sys
from mpmath import mp, mpf, sqrt, pi, tan, nstr, identify, cot
mp.dps = 110
def unit(v): n = sqrt(sum(c*c for c in v)); return [c/n for c in v]
def dot(a, b): return sum(x*y for x, y in zip(a, b))
NF = {'tc': 10, 'co': 14, 'tr': 16, 'cr': 18, 'or': 20, 'di': 32, 'dt': 42, 'it': 50}
ok = True
for mode in sys.argv[1:]:
    N = NF[mode]; D = json.load(open('verts-%s.json' % mode)); mu0 = mpf(D['mu'])
    faces = [[[mpf(c) for c in v] for v in vs] for vs in D['faces'].values() if len(vs) >= 3]
    # the regular face: the fewest sides, all corners at one distance from the centre
    reg = min(faces, key=len); m = len(reg)
    c = [sum(v[t] for v in reg)/m for t in range(3)]; a = unit(c); d = dot(a, reg[0])
    famA = abs(d - 1) < mpf(10)**-80
    theta = pi/2 - pi/m + 2*pi/(m*N)
    K = tan(pi/m)*tan(theta); t = sqrt(K**2 - 1)
    v = reg[0]; r_corner = sqrt(dot(v, v))
    e1 = abs(r_corner/d - K)
    u = unit([v[s] - dot(v, a)*a[s] for s in range(3)])
    # the other family's face planes through v: their unit normal = unit centroid direction, distance = normal . vertex
    other = []
    for f in faces:
        e1_ = [f[1][s]-f[0][s] for s in range(3)]; e2_ = [f[2][s]-f[0][s] for s in range(3)]
        cf = unit([e1_[1]*e2_[2]-e1_[2]*e2_[1], e1_[2]*e2_[0]-e1_[0]*e2_[2], e1_[0]*e2_[1]-e1_[1]*e2_[0]])
        if dot(cf, f[0]) < 0: cf = [-x for x in cf]
        df = dot(cf, f[0])   # true plane normal (a centroid direction is not the normal on an irregular face)
        if (abs(df - 1) < mpf(10)**-80) == famA: continue
        if any(all(abs(w[s] - v[s]) < mpf(10)**-80 for s in range(3)) for w in f): other.append((cf, df))
    b, db = other[0]
    p, q = dot(b, a), dot(b, u)
    mu = (p + t*q) if famA else 1/(p + t*q)
    e2 = abs(mu - mu0)
    good = e1 < mpf(10)**-90 and e2 < mpf(10)**-90
    if mode == 'co':
        T = tan(pi/14)*tan(2*pi/7); good = good and abs(mu - (1 + sqrt(2*T))/sqrt(3)) < mpf(10)**-90
    ok = ok and good
    print('== %s N=%d: regular %d-gon face, family %s, theta = %s pi; |corner|/d = tan(pi/m)tan(theta) err %s; '
          'mu = %s with p = b.a = %s (%s), q = b.u = %s (%s); mu err %s %s' % (
          mode, N, m, 'A (at 1)' if famA else 'B (at mu)', nstr(theta/pi, 12), nstr(e1, 3),
          '(p + q t)' if famA else '1/(p + q t)', nstr(p, 15), identify(p, ['sqrt(2)', 'sqrt(3)', 'sqrt(5)', 'sqrt(6)', 'sqrt(10)', 'sqrt(15)']),
          nstr(q, 15), identify(q, ['sqrt(2)', 'sqrt(3)', 'sqrt(5)', 'sqrt(6)', 'sqrt(10)', 'sqrt(15)']), nstr(e2, 3), 'OK' if good else 'FAIL'))
print('FINAL ok' if ok else 'FINAL FAIL')
