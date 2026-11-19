# 100-digit refinement of the two-depth fair RD ∩ icosahedron die (start from the float pilot),
# then search for closed forms of m1, m2 (findpoly / identify) and of the corner angles of the faces' spherical polygons.
import itertools
from mpmath import mp, mpf, sqrt, atan2, pi, findroot, findpoly, identify, nstr, matrix, lu_solve, acos
mp.dps = 110
phi = (1 + sqrt(5)) / 2
def u(v): n = sqrt(sum(c*c for c in v)); return [c/n for c in v]
def dot(a, b): return sum(x*y for x, y in zip(a, b))
def cross(a, b): return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]
roll = lambda q, k: tuple(q[(i - k) % 3] for i in range(3))
RD = [u(p) for p in sorted({roll(q, k) for q in [(a, b, 0) for a in (1, -1) for b in (1, -1)] for k in range(3)})]
I8 = [u(p) for p in itertools.product((1, -1), repeat=3)]
I12 = [u(p) for p in sorted({roll((0, a/phi, b*phi), k) for a in (1, -1) for b in (1, -1) for k in range(3)})]
N = RD + I8 + I12
TRIPLES = None
def det3(a, b, c): return dot(a, cross(b, c))
def solve3(i, j, k, d):
    a, b, c = N[i], N[j], N[k]; D = det3(a, b, c)
    # Cramer: x = (d_i (b×c) + d_j (c×a) + d_k (a×b)) / D
    bc, ca, ab = cross(b, c), cross(c, a), cross(a, b)
    return [(d[i]*bc[t] + d[j]*ca[t] + d[k]*ab[t]) / D for t in range(3)]
def verts(d):
    global TRIPLES
    if TRIPLES is None:   # combinatorics once, at the start point (it does not change near the root)
        mp.dps = 30
        TRIPLES, V = [], []
        for i, j, k in itertools.combinations(range(32), 3):
            if abs(det3(N[i], N[j], N[k])) < mpf(10)**-12: continue
            x = solve3(i, j, k, d)
            if all(dot(n, x) <= dd + mpf(10)**-12 for n, dd in zip(N, d)) and not any(max(abs(a-b) for a, b in zip(x, y)) < mpf(10)**-9 for y in V):
                V.append(x); TRIPLES.append((i, j, k))
        mp.dps = 110
    return [solve3(i, j, k, d) for i, j, k in TRIPLES]
def tri(a, b, c):
    return 2 * atan2(abs(dot(a, cross(b, c))), 1 + dot(a, b) + dot(b, c) + dot(c, a))
def omegas(m1, m2):
    d = [mpf(1)]*12 + [m1]*8 + [m2]*12; V = verts(d); out = []
    for n, dd in zip(N, d):
        P = [v for v in V if abs(dot(n, v) - dd) < mpf(10)**-60]
        c = [sum(p[t] for p in P)/len(P) for t in range(3)]
        e1 = u([P[0][t]-c[t] for t in range(3)]); e2 = cross(n, e1)
        P.sort(key=lambda p: atan2(dot([p[t]-c[t] for t in range(3)], e2), dot([p[t]-c[t] for t in range(3)], e1)))
        out.append(sum(tri(u(c), u(P[i]), u(P[(i+1) % len(P)])) for i in range(len(P))))
    return out, V
T = 4*pi/32
def f(a, b):
    o = omegas(a, b)[0]; return [o[12] - T, o[20] - T]
m1, m2 = findroot(f, (mpf('1.002759250954'), mpf('1.010663942602')), tol=mpf(10)**-95)
om, V = omegas(m1, m2)
print('m1 =', nstr(m1, 60)); print('m2 =', nstr(m2, 60))
print('max |Ω - 4π/32| =', nstr(max(abs(o - T) for o in om), 3), '| corners', len(V))
for name, x in (('m1', m1), ('m2', m2), ('m1^2', m1**2), ('m2^2', m2**2)):
    p = findpoly(x, 8, maxcoeff=10**6)
    print(name, 'findpoly deg<=8:', p, '| identify:', identify(x, ['sqrt(5)', 'sqrt(2)', 'sqrt(3)', 'sqrt(15)', 'sqrt(10)', 'sqrt(6)']))
print('FINAL ok' if max(abs(o - T) for o in om) < mpf(10)**-80 and len(V) == 60 else 'FINAL FAIL')
