"""Study 9 checks (exact rational arithmetic, standard library only).
1. Volumes of the tetrahedron, octahedron and cube ∩ octahedron solids from their corners and face planes
   (fan from the origin over each face), compared with 8/3, 4/3, (4/3)(t^3 - 3(t-1)^3).
2. The polynomial identities used in Lean (Dehn9Same.lean).
3. g(t) = (2t-3)^3 / (t^3 - 3(t-1)^3): values, monotonicity on a grid, Lucky 7 value (float).
"""
from fractions import Fraction as Fr
from itertools import product, permutations
import math

def det3(a, b, c):
    return (a[0]*(b[1]*c[2]-b[2]*c[1]) - a[1]*(b[0]*c[2]-b[2]*c[0]) + a[2]*(b[0]*c[1]-b[1]*c[0]))

def volume(normals, offsets, verts):
    vol = Fr(0)
    for n, b in zip(normals, offsets):
        face = [v for v in verts if sum(ni*vi for ni, vi in zip(n, v)) == b]
        if len(face) < 3:
            continue
        c = [sum(v[i] for v in face)/len(face) for i in range(3)]
        # order around the face (floats only for the order)
        nn = [float(x) for x in n]
        u = [float(face[0][i]-c[i]) for i in range(3)]
        w = [nn[1]*u[2]-nn[2]*u[1], nn[2]*u[0]-nn[0]*u[2], nn[0]*u[1]-nn[1]*u[0]]
        def ang(v):
            d = [float(v[i]-c[i]) for i in range(3)]
            return math.atan2(sum(d[i]*w[i] for i in range(3)), sum(d[i]*u[i] for i in range(3)))
        face.sort(key=ang)
        for i in range(1, len(face)-1):
            vol += abs(det3(face[0], face[i], face[i+1])) / 6
    return vol

# tetrahedron (study 3): normals (1,1,1),(-1,-1,1),(-1,1,-1),(1,-1,-1), offsets 1
tetN = [(1,1,1),(-1,-1,1),(-1,1,-1),(1,-1,-1)]
tetV = [tuple(Fr(c) for c in v) for v in [(-1,-1,-1),(1,1,-1),(1,-1,1),(-1,1,1)]]
for v in tetV:
    assert all(sum(a*b for a, b in zip(n, v)) <= 1 for n in tetN)
VT = volume(tetN, [1]*4, tetV)
print("tetrahedron volume", VT, "expected 8/3:", VT == Fr(8, 3))

octN = [s for s in product([1,-1], repeat=3)]
octV = [tuple(Fr(c) for c in v) for v in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]]
VO = volume(octN, [1]*8, octV)
print("octahedron volume", VO, "expected 4/3:", VO == Fr(4, 3))

def co(t):
    N = [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)] + octN
    B = [1]*6 + [t]*8
    V = set()
    for p in permutations(range(3)):
        for s1, s2 in product([1,-1], repeat=2):
            x = [0, 0, 0]; x[p[0]] = s1; x[p[1]] = s2*(t-1); V.add(tuple(Fr(c) for c in x))
    V = list(V)
    assert len(V) == 24
    for v in V:
        assert all(sum(a*b for a, b in zip(n, v)) <= bb for n, bb in zip(N, B))
    return volume(N, B, V)

def D(t): return t**3 - 3*(t-1)**3
for t in [Fr(5,4), Fr(3,2), Fr(7,4), Fr(9,5), Fr(11,10), Fr(19,10)]:
    v = co(t)
    print("cube ∩ octahedron t =", t, "volume", v, "formula", Fr(4,3)*D(t), v == Fr(4,3)*D(t))

# 2. identities (as polynomials, checked at 40 rational points each: degree <= 6, so exact)
pts = [Fr(k, 7) for k in range(-20, 20)]
ok = all(2*(2*t-3)**3 - D(t) == -3 - 9*((t-1)*(2-t))*(2*t-3) for t in pts)
print("2(2t-3)^3 - D(t) = -3 - 9(t-1)(2-t)(2t-3):", ok)
ok = all((2*t-3)**3 + D(t) == 3*(t-1)*(2*t*t-7*t+8) for t in pts)
print("(2t-3)^3 + D(t) = 3(t-1)(2t^2-7t+8):", ok)
ok = all(4*D((x+3)/2) == 12 + 9*x - x**3 for x in pts)
print("4 D((x+3)/2) = 12 + 9x - x^3:", ok)
ok = all(x**3*(12+9*y-y**3) - y**3*(12+9*x-x**3) == (x-y)*(12*(x*x+x*y+y*y) + 9*x*y*(x+y))
         for x in pts for y in pts)
print("x^3(12+9y-y^3) - y^3(12+9x-x^3) = (x-y)(12(x^2+xy+y^2)+9xy(x+y)):", ok)
K = lambda x, y: 12*(x*x+x*y+y*y) + 9*x*y*(x+y)
grid = [Fr(k, 50) for k in range(-49, 50)]
print("K > 0 on the grid of (-1,1)^2 off (0,0):", all(K(x, y) > 0 for x in grid for y in grid if (x, y) != (0, 0)))

# 3. g and the scale-free number a^3/vol = 2592 sqrt2 g
g = lambda t: (2*t-3)**3 / D(t)
print("g(1) =", g(Fr(1)), " g(3/2) =", g(Fr(3,2)), " g(2) =", g(Fr(2)))
print("tetrahedron a^3/vol / (2592 sqrt2) = (12^3*2)/(8/3)/2592 =", Fr(12**3*2)/Fr(8,3)/2592)
print("octahedron  a^3/vol / (2592 sqrt2) =", Fr(-12**3*2)/Fr(4,3)/2592)
tg = [1 + Fr(k, 1000) for k in range(0, 1001)]
print("g strictly increasing on [1,2] (grid of 1001):", all(g(a) < g(b) for a, b in zip(tg, tg[1:])))
tL = 1.756582135945042  # Lucky 7: mu_f in studies/2026-11-18-fair-32-die/data/co.log (numerical)
print("Lucky 7: t = %.5f, g = %.6f, volume = %.6f, Dehn length 12*sqrt2*(2t-3) = %.6f" %
      (tL, float((2*tL-3)**3/(tL**3-3*(tL-1)**3)), 4/3*(tL**3-3*(tL-1)**3), 12*math.sqrt(2)*(2*tL-3)))
