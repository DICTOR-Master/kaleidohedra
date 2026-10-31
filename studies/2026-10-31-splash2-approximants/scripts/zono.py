# Exact canonical cut-and-project tilings from Z^n onto a 2-plane, by the quotient method.
# A rational plane E' (spanned by integer u, v) gives the period lattice Lam = Z^n cap E'; an integer matrix K (2 x n)
# with kernel Lam maps Z^n onto Z^2. Vertices of one period of the canonical tiling are the points y of Z^2 + gamma inside the
# zonogon W = sum [0,1) g_k, g_k = K e_k (integer). For an irrational plane the same formulas run in Q(sqrt d) with g_k = eps_k.
from fractions import Fraction as Fr
import math


# ---------- integer linear algebra
def int_kernel(A):
    """saturated integer basis of {x in Z^n : A x = 0} (A: list of integer rows), by unimodular column operations"""
    m, n = len(A), len(A[0])
    M = [row[:] for row in A]
    U = [[int(i == j) for j in range(n)] for i in range(n)]
    def colop(i, j, c):          # col_j += c col_i
        for r in M: r[j] += c * r[i]
        for r in U: r[j] += c * r[i]
    def swap(i, j):
        for r in M: r[i], r[j] = r[j], r[i]
        for r in U: r[i], r[j] = r[j], r[i]
    piv = 0
    for r in range(m):
        if piv >= n: break
        while True:
            nz = [j for j in range(piv, n) if M[r][j] != 0]
            if not nz: break
            j0 = min(nz, key=lambda j: abs(M[r][j])); swap(piv, j0)
            done = True
            for j in range(piv + 1, n):
                if M[r][j]:
                    colop(piv, j, -(M[r][j] // M[r][piv]))
                    if M[r][j]: done = False
            if done: break
        if any(M[r][j] for j in range(piv, n)): piv += 1
    return [[U[i][j] for i in range(n)] for j in range(piv, n)]


def minors2(u, v):
    n = len(u)
    return {(i, j): u[i] * v[j] - u[j] * v[i] for i in range(n) for j in range(i + 1, n)}


def det(M):
    n = len(M)
    if n == 1: return M[0][0]
    return sum((-1) ** j * M[0][j] * det([r[:j] + r[j + 1:] for r in M[1:]]) for j in range(n))


# ---------- exact planar geometry over any ordered field (Fraction, QF)
def cross(a, b): return a[0] * b[1] - a[1] * b[0]
def sub(a, b): return (a[0] - b[0], a[1] - b[1])
def add(a, b): return (a[0] + b[0], a[1] + b[1])


def zonogon(gens):
    """vertices (counter-clockwise) of sum_k [0,1] g_k"""
    zero = gens[0][0] * 0
    base = (zero, zero); G = []
    for g in gens:
        if g[1] < 0 or (g[1] == 0 and g[0] < 0):
            base = add(base, g); G.append((-g[0], -g[1]))
        else:
            G.append(g)
    # sort by angle in [0, pi): a before b iff cross(a, b) > 0
    import functools
    G.sort(key=functools.cmp_to_key(lambda a, b: -1 if cross(a, b) > 0 else (1 if cross(a, b) < 0 else 0)))
    V = [base]; p = base
    for g in G: p = add(p, g); V.append(p)
    for g in G[:-1]: p = sub(p, g); V.append(p)
    # remove collinear repeats
    out = []
    for i, q in enumerate(V):
        a, c = V[i - 1], V[(i + 1) % len(V)]
        if cross(sub(q, a), sub(c, q)) != 0: out.append(q)
    return out


def area(P):
    s = P[0][0] * 0
    for i in range(len(P)):
        s = s + cross(P[i], P[(i + 1) % len(P)])
    return s / 2


def halfplanes(P):
    """convex ccw polygon -> list of (a, b): inside iff cross(b - a, z - a) > 0"""
    return [(P[i], P[(i + 1) % len(P)]) for i in range(len(P))]


def clip(P, h, keep_inside=True):
    a, b = h; d = sub(b, a); out = []
    n = len(P)
    for i in range(n):
        p, q = P[i], P[(i + 1) % n]
        sp, sq = cross(d, sub(p, a)), cross(d, sub(q, a))
        if not keep_inside: sp, sq = -sp, -sq
        if sp >= 0: out.append(p)
        if (sp > 0 and sq < 0) or (sp < 0 and sq > 0):
            t = sp / (sp - sq); out.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
    # drop degenerate
    if len(out) < 3: return None
    if area(out) == 0: return None
    return out


def split(P, Q):
    """convex P by convex Q: (P cap Q, [pieces of P outside Q])"""
    inside, outs = P, []
    for h in halfplanes(Q):
        if inside is None: break
        o = clip(inside, h, keep_inside=False)
        if o is not None: outs.append(o)
        inside = clip(inside, h, keep_inside=True)
    return inside, outs


def arrangement(W, gens):
    """cells of W by the 2n translates W - g_k (edge +k) and W + g_k (edge -k); returns [(polygon, star)] with
    star = tuple of 2n booleans (+0..+(n-1), -0..-(n-1))"""
    n = len(gens)
    trans = [[(p[0] - g[0], p[1] - g[1]) for p in W] for g in gens] + [[(p[0] + g[0], p[1] + g[1]) for p in W] for g in gens]
    cells = [(W, ())]
    for T in trans:
        new = []
        for P, st in cells:
            ins, outs = split(P, T)
            if ins is not None: new.append((ins, st + (True,)))
            for o in outs: new.append((o, st + (False,)))
        cells = new
    return cells


def inside_strict(z, W):
    for a, b in halfplanes(W):
        s = cross(sub(b, a), sub(z, a))
        if s < 0: return False
        if s == 0: raise ValueError('boundary point')
    return True


def lattice_points(W, gamma):
    """integer points y with y - gamma strictly inside W (W rational)"""
    xs = [p[0] for p in W]; ys = [p[1] for p in W]
    x0, x1 = math.floor(min(xs) + gamma[0]), math.ceil(max(xs) + gamma[0])
    y0, y1 = math.floor(min(ys) + gamma[1]), math.ceil(max(ys) + gamma[1])
    H = halfplanes(W); pts = []
    for y in range(y0, y1 + 1):
        # x-range on this row
        z1 = y - gamma[1]
        lo, hi = None, None
        for a, b in H:
            d = sub(b, a)
            # cross(d, (x - gamma0 - a0, z1 - a1)) > 0  <=>  d0 (z1 - a1) - d1 (x - g0 - a0) > 0
            if d[1] == 0:
                if d[0] * (z1 - a[1]) <= 0: lo, hi = 1, 0; break
                continue
            c = (d[0] * (z1 - a[1])) / d[1] + a[0] + gamma[0]   # boundary x
            if d[1] > 0:   # need x < c
                hi = c if hi is None or c < hi else hi
            else:
                lo = c if lo is None or c > lo else lo
        if lo is None or hi is None or lo >= hi: continue
        for x in range(math.floor(lo), math.ceil(hi) + 1):
            if lo < x < hi:
                pts.append((x, y))
            elif x == lo or x == hi:
                raise ValueError('boundary')
    return pts
