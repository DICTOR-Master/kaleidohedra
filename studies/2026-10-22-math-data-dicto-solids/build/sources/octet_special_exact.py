# Special positions of the octet family, exact (DICTO 10-23: find special positions first, then name).
# Each position lives in a number field Q(r), r^n = k: Q(√6), Q(√2), Q(∛2) (the Delian bond, Samson and Delilah), Q(∛6).
# Field elements are exact vectors of Fractions in the basis 1, r, ..., r^(n-1). Equalities (edges, volumes, "is this point on
# the plane") are decided exactly; the side of a plane is read from the float value only when it is not exactly zero.
from fractions import Fraction as Fr
from itertools import combinations, product
import math
class K:
    n = 2; k = 2
    def __init__(s, c):
        c = list(c) if isinstance(c, (list, tuple)) else [c]
        s.c = [Fr(x) for x in c] + [Fr(0)] * (K.n - len(c))
    @staticmethod
    def of(x): return x if isinstance(x, K) else K(x)
    def __add__(s, o): o = K.of(o); return K([a + b for a, b in zip(s.c, o.c)])
    __radd__ = __add__
    def __neg__(s): return K([-a for a in s.c])
    def __sub__(s, o): return s + (-K.of(o))
    def __rsub__(s, o): return K.of(o) - s
    def __mul__(s, o):
        o = K.of(o); r = [Fr(0)] * (2 * K.n)
        for i, a in enumerate(s.c):
            for j, b in enumerate(o.c): r[i + j] += a * b
        for i in range(2 * K.n - 1, K.n - 1, -1):
            r[i - K.n] += r[i] * K.k; r[i] = Fr(0)
        return K(r[:K.n])
    __rmul__ = __mul__
    def inv(s):   # solve s * x = 1 with the multiplication matrix
        cols = []
        for j in range(K.n):
            e = [0] * K.n; e[j] = 1; cols.append((s * K(e)).c)
        M = [[cols[j][i] for j in range(K.n)] + [Fr(1 if i == 0 else 0)] for i in range(K.n)]
        for col in range(K.n):
            piv = next(r for r in range(col, K.n) if M[r][col] != 0); M[col], M[piv] = M[piv], M[col]
            p = M[col][col]; M[col] = [x / p for x in M[col]]
            for r in range(K.n):
                if r != col and M[r][col] != 0:
                    f = M[r][col]; M[r] = [x - f * y for x, y in zip(M[r], M[col])]
        return K([M[i][K.n] for i in range(K.n)])
    def __truediv__(s, o): return s * K.of(o).inv()
    def iszero(s): return all(x == 0 for x in s.c)
    def __eq__(s, o): return (s - K.of(o)).iszero()
    def __float__(s): r = K.k ** (1 / K.n); return sum(float(a) * r ** i for i, a in enumerate(s.c))
    def sign(s):
        if s.iszero(): return 0
        f = float(s); assert abs(f) > 1e-9, 'too close to zero to read the side from floats'
        return 1 if f > 0 else -1
    def __repr__(s): return ' + '.join(f'{a}·r^{i}' for i, a in enumerate(s.c) if a) or '0'
dot = lambda a, b: a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
sub = lambda a, b: tuple(x - y for x, y in zip(a, b))
def det3(m): return m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])-m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])+m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0])
def solve(A, b):
    D = det3(A)
    if D.iszero(): return None
    out = []
    for k in range(3):
        M = [list(r) for r in A]
        for i in range(3): M[i][k] = b[i]
        out.append(det3(M) / D)
    return tuple(out)
O = [(1,0,0),(0,1,0),(0,0,1),(1,1,1)]
Tc = [tuple(Fr(a, 2) for a in p) for p in product((1,3), repeat=3)]
def setup():
    S = []
    for c in product(range(-1, 2), repeat=3):
        o = tuple(2 * x for x in c)
        S += [('O', tuple(K(p[i] + o[i]) for i in range(3))) for p in O] + [('T', tuple(K(p[i] + o[i]) for i in range(3))) for p in Tc]
    return S
def cell(S, kind, c, t):
    w = {'O': K(0), 'T': K(Fr(3, 4)) * (2 * t - 1)}
    H = []
    for k2, c2 in S:
        if all((x - y).iszero() for x, y in zip(c2, c)): continue
        n = sub(c2, c)
        if float(dot(n, n)) > 4.0001: continue
        H.append((n, (dot(c2, c2) - dot(c, c) - w[k2] + w[kind]) / 2))
    P = []
    for (n1, b1), (n2, b2), (n3, b3) in combinations(H, 3):
        p = solve([n1, n2, n3], [b1, b2, b3])
        if p is None or not all((b - dot(n, p)).sign() >= 0 for n, b in H): continue
        if not any(all((x - y).iszero() for x, y in zip(p, q)) for q in P): P.append(p)
    F = []
    for n, b in H:
        on = [p for p in P if (dot(n, p) - b).iszero()]
        if len(on) >= 3: F.append((n, on))
    return P, F
def volume(P, F, c):
    v = K(0)
    for n, on in F:
        cen = [sum(float(p[k]) for p in on) / len(on) for k in range(3)]
        u = [float(on[0][k]) - cen[k] for k in range(3)]; nf = [float(x) for x in n]
        w = [nf[1]*u[2]-nf[2]*u[1], nf[2]*u[0]-nf[0]*u[2], nf[0]*u[1]-nf[1]*u[0]]
        on = sorted(on, key=lambda p: math.atan2(sum((float(p[k])-cen[k])*w[k] for k in range(3)), sum((float(p[k])-cen[k])*u[k] for k in range(3))))
        for j in range(1, len(on) - 1):
            d = det3([sub(on[0], c), sub(on[j], c), sub(on[j + 1], c)]); v = v + (d if d.sign() >= 0 else -d)
    return v / 6
def edges2(P, F):
    E = []
    for a, b in combinations(range(len(P)), 2):
        if sum(1 for n, on in F if any(all((x-y).iszero() for x,y in zip(P[a],q)) for q in on) and any(all((x-y).iszero() for x,y in zip(P[b],q)) for q in on)) >= 2:
            d = sub(P[a], P[b]); E.append(dot(d, d))
    return E
fails = 0
def check(lab, ok):
    global fails; fails += not ok; print(('PASS ' if ok else 'FAIL ') + lab, flush=True)
def run(name, n, k, t_of):
    K.n, K.k = n, k; S = setup(); t = t_of()
    PT, FT = cell(S, 'T', Tc[0] if False else tuple(K(x) for x in Tc[0]), t); PO, FO = cell(S, 'O', tuple(K(x) for x in O[0]), t)
    vT = volume(PT, FT, tuple(K(x) for x in Tc[0])); vO = volume(PO, FO, tuple(K(x) for x in O[0]))
    eT, eO = edges2(PT, FT), edges2(PO, FO)
    print(f'--- {name}: t = {float(t):.6f}; tetra piece {len(PT)} corners {len(FT)} faces, octa piece {len(PO)} corners {len(FO)} faces')
    check(f'{name}: 8 tetra pieces + 4 octa pieces = 8 (the cube of side 2), exactly', (8 * vT + 4 * vO) == 8)
    return t, vT, vO, eT, eO, (len(PT), len(FT), len(PO), len(FO))
# 1. equilateral, rhombic-dodecahedron side: t = 1/(3 + 2√6) = (2√6 − 3)/15  in Q(√6)
t, vT, vO, eT, eO, cnt = run('equilateral (rhombic dodecahedron side)', 2, 6, lambda: K([Fr(-3, 15), Fr(2, 15)]))
check(f'every edge of both pieces has the same length, exactly (edge² = {eT[0]}, ≈ {float(eT[0])**.5:.6f}); counts {cnt}', all(e == eT[0] for e in eT + eO) and cnt == (4, 4, 30, 20))
# 2. equilateral, cube side: t = 1 − 2(√2 − 1)/3 = 5/3 − (2/3)√2  in Q(√2)
t, vT, vO, eT, eO, cnt = run('equilateral (cube side)', 2, 2, lambda: K([Fr(5, 3), Fr(-2, 3)]))
check(f'every edge of both pieces has the same length, exactly: edge² = {eT[0]} = (2 − √2)²; counts {cnt}', all(e == eT[0] for e in eT + eO) and eT[0] == K([6, -4]) and cnt == (16, 10, 6, 8))
# 3. the Delian bond: t = 1 − (2/3)·2^(−1/3) = 1 − r²/3 with r = ∛2  in Q(∛2)
t, vT, vO, eT, eO, cnt = run('Delian bond (Samson and Delilah)', 3, 2, lambda: K([1, 0, Fr(-1, 3)]))
check(f'Samson (tetra piece) and Delilah (octa piece) have equal volume 2/3, exactly: {vT}, {vO}', vT == Fr(2, 3) and vO == Fr(2, 3))
check(f'Delilah is a regular octahedron with edge² = ∛2 (edge 2^(1/6)), exactly: {set(map(repr, eO))}', all(e == K([0, 1, 0]) for e in eO) and cnt[2:] == (6, 8))
check(f'Samson: 16 corners, 10 faces (4 triangles, 6 hexagons); its edges have two lengths, squared {sorted(set(map(repr, eT)))}', cnt[:2] == (16, 10) and len({repr(e) for e in eT}) == 2)
# 4. half each: t = 1 − (2/3)(3/4)^(1/3) = 1 − (1/3)·∛6  in Q(∛6)
t, vT, vO, eT, eO, cnt = run('tetrahedra and octahedra fill half of space each', 3, 6, lambda: K([1, Fr(-1, 3), 0]))
check(f'8 tetra pieces = 4 octa pieces = 4, exactly: vT = {vT}, vO = {vO}', vT == Fr(1, 2) and vO == 1)
print('ALL PASS' if fails == 0 else f'{fails} FAIL')
