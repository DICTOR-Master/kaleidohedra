"""Finite reflection groups A3, B3, H3, A4, B4, D4, F4, H4 with UNIT simple roots, exact over Q(sqrt D).

With unit roots alpha_i and the dual basis w_i (<w_i, alpha_j> = delta_ij), a seed v = sum c_j w_j has <v, alpha_j> = c_j and the
edge made by the reflection s_j has length 2 c_j: the c's are the edge lengths of the Wythoff polytope (halved).
Every diagram automorphism sigma permutes unit simple roots with the same Gram matrix, so alpha_i -> alpha_sigma(i) extends to an
isometry L_sigma, and P(sigma c) = L_sigma P(c): congruent.
"""
import itertools
from fractions import Fraction as Fr
import exact as X
from exact import K, kk

def dot(u, v):
    s = K(0)
    for a, b in zip(u, v): s = s + a*b
    return s

def refl(x, a):
    """reflection of x in the hyperplane orthogonal to the unit vector a"""
    c = dot(x, a); c2 = c + c
    return tuple(xi - c2*ai for xi, ai in zip(x, a))

def vkey(v): return tuple(c.key() for c in v)

def mat_inv(M):
    n = len(M); A = [list(r) + [K(1) if i == j else K(0) for j in range(n)] for i, r in enumerate(M)]
    for i in range(n):
        p = next(r for r in range(i, n) if not A[r][i].iszero()); A[i], A[p] = A[p], A[i]
        iv = A[i][i].inv(); A[i] = [x*iv for x in A[i]]
        for r in range(n):
            if r != i and not A[r][i].iszero():
                f = A[r][i]; A[r] = [x - f*y for x, y in zip(A[r], A[i])]
    return [r[n:] for r in A]

def det(M):
    M = [list(r) for r in M]; n = len(M); d = K(1)
    for i in range(n):
        p = next((r for r in range(i, n) if not M[r][i].iszero()), None)
        if p is None: return K(0)
        if p != i: M[i], M[p] = M[p], M[i]; d = -d
        d = d*M[i][i]; iv = M[i][i].inv()
        for r in range(i+1, n):
            if not M[r][i].iszero():
                f = M[r][i]*iv; M[r] = [x - f*y for x, y in zip(M[r], M[i])]
    return d

def phi(): return K(Fr(1, 2), Fr(1, 2))     # (1+sqrt5)/2 in Q(sqrt5)

def h4_roots():
    """search four unit vectors among the 120 unit icosians with the H4 Gram matrix (5,3,3 chain)"""
    p = phi(); ip = p - 1; h = K(Fr(1, 2))
    V = set()
    for i in range(4):
        for s in (1, -1):
            v = [K(0)]*4; v[i] = K(s); V.add(tuple(v))
    for sg in itertools.product((1, -1), repeat=4): V.add(tuple(K(Fr(s, 2)) for s in sg))
    base = (p*h, h, ip*h, K(0))
    evens = [q for q in itertools.permutations(range(4)) if sum(1 for i in range(4) for j in range(i+1, 4) if q[i] > q[j]) % 2 == 0]
    for q in evens:
        for sg in itertools.product((1, -1), repeat=3):
            b = [base[0]*sg[0], base[1]*sg[1], base[2]*sg[2], K(0)]
            v = [None]*4
            for i in range(4): v[q[i]] = b[i]
            V.add(tuple(v))
    V = list(V); assert len(V) == 120
    c5 = -(p*h); c3 = K(Fr(-1, 2))
    a1 = V[0]
    for a2 in V:
        if dot(a1, a2) != c5: continue
        for a3 in V:
            if dot(a2, a3) != c3 or not dot(a1, a3).iszero(): continue
            for a4 in V:
                if dot(a3, a4) == c3 and dot(a1, a4).iszero() and dot(a2, a4).iszero(): return [a1, a2, a3, a4]
    raise RuntimeError('no H4 roots')

def group_data(name):
    """returns dict: field D, ambient n, rank r, unit simple roots, automorphisms (node permutations), order"""
    s2 = K(0, Fr(1, 2))   # 1/sqrt2 = sqrt2/2
    def e(n, i): return [K(1) if j == i else K(0) for j in range(n)]
    def sub(u, v): return [a - b for a, b in zip(u, v)]
    def add(u, v): return [a + b for a, b in zip(u, v)]
    def sc(k, u): return [k*a for a in u]
    if name in ('H3', 'H4'): X.set_field(5)
    else: X.set_field(2)
    s2 = K(0, Fr(1, 2)) if X.D == 2 else None
    if name == 'A3':   # as D3, chain (e2-e3)-(e1-e2)-(e2+e3)
        n = 3; R = [sc(s2, sub(e(3, 1), e(3, 2))), sc(s2, sub(e(3, 0), e(3, 1))), sc(s2, add(e(3, 1), e(3, 2)))]; aut = [(2, 1, 0)]; order = 24
    elif name == 'B3':
        n = 3; R = [sc(s2, sub(e(3, 0), e(3, 1))), sc(s2, sub(e(3, 1), e(3, 2))), e(3, 2)]; aut = []; order = 48
    elif name == 'H3':
        p = phi(); ip = p - 1; h = K(Fr(-1, 2))
        n = 3; R = [e(3, 0), [h*p, h*ip, h], e(3, 2)]; aut = []; order = 120
    elif name == 'A4':
        n = 5; R = [sc(s2, sub(e(5, i), e(5, i+1))) for i in range(4)]; aut = [(3, 2, 1, 0)]; order = 120
    elif name == 'B4':
        n = 4; R = [sc(s2, sub(e(4, i), e(4, i+1))) for i in range(3)] + [e(4, 3)]; aut = []; order = 384
    elif name == 'D4':   # node 1 central
        n = 4; R = [sc(s2, sub(e(4, 0), e(4, 1))), sc(s2, sub(e(4, 1), e(4, 2))), sc(s2, sub(e(4, 2), e(4, 3))), sc(s2, add(e(4, 2), e(4, 3)))]
        aut = [(2, 1, 0, 3), (3, 1, 2, 0), (0, 1, 3, 2), (2, 1, 3, 0), (3, 1, 0, 2)]; order = 192
    elif name == 'F4':
        n = 4; h = K(Fr(1, 2))
        R = [sc(s2, sub(e(4, 1), e(4, 2))), sc(s2, sub(e(4, 2), e(4, 3))), e(4, 3), [h, -h, -h, -h]]; aut = [(3, 2, 1, 0)]; order = 1152
    elif name == 'H4':
        n = 4; R = [list(x) for x in h4_roots()]; aut = []; order = 14400
    R = [tuple(r) for r in R]; r = len(R)
    G = [[dot(R[i], R[j]) for j in range(r)] for i in range(r)]
    for i in range(r): assert G[i][i] == K(1), (name, i, G[i][i])
    for s in aut:
        for i in range(r):
            for j in range(r): assert G[s[i]][s[j]] == G[i][j], ('automorphism not isometric', name, s)
    Ginv = mat_inv(G)
    W = [tuple(sum((Ginv[j][k]*R[k][m] for k in range(r)), K(0)) for m in range(n)) for j in range(r)]   # dual basis
    for i in range(r):
        for j in range(r): assert dot(W[i], R[j]) == (K(1) if i == j else K(0))
    Gw = [[dot(W[i], W[j]) for j in range(r)] for i in range(r)]
    return {'name': name, 'D': X.D, 'n': n, 'r': r, 'R': R, 'W': W, 'G': G, 'Gw': Gw, 'aut': aut, 'order': order}

def coxeter_m(gd):
    """Coxeter labels from the Gram matrix (cos(pi/m) = -G_ij)"""
    import math
    r = gd['r']; M = {}
    for i in range(r):
        for j in range(i+1, r):
            c = -float(gd['G'][i][j]); m = round(math.pi/math.acos(max(-1, min(1, c)))) if c > 1e-12 else 2; M[(i, j)] = m
    return M

def elements(gd):
    """all group elements as tuples (g w_1, ..., g w_r) by breadth-first search from the identity; returns list"""
    R, W = gd['R'], gd['W']
    start = tuple(W); seen = {tuple(vkey(w) for w in start): start}; frontier = [start]
    while frontier:
        nf = []
        for st in frontier:
            for a in R:
                ns = tuple(refl(w, a) for w in st); kk_ = tuple(vkey(w) for w in ns)
                if kk_ not in seen: seen[kk_] = ns; nf.append(ns)
        frontier = nf
    els = list(seen.values())
    assert len(els) == gd['order'], (gd['name'], len(els), gd['order'])
    return els
