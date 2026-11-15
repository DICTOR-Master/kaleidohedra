"""Exact check (in Q(sqrt5)) of the twisted-class mechanism for the golden A4 sets.
Pure Python, Fractions only.  Prints a log; every line marked CHECK must say OK."""
from fractions import Fraction as Fr
from itertools import permutations, product
from collections import Counter

class Q:                                   # a + b*sqrt5
    __slots__ = ("a", "b")
    def __init__(s, a=0, b=0): s.a = Fr(a); s.b = Fr(b)
    @staticmethod
    def c(x): return x if isinstance(x, Q) else Q(x)
    def __add__(s, o): o = Q.c(o); return Q(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __neg__(s): return Q(-s.a, -s.b)
    def __sub__(s, o): o = Q.c(o); return Q(s.a - o.a, s.b - o.b)
    def __rsub__(s, o): return Q.c(o) - s
    def __mul__(s, o): o = Q.c(o); return Q(s.a*o.a + 5*s.b*o.b, s.a*o.b + s.b*o.a)
    __rmul__ = __mul__
    def inv(s): n = s.a*s.a - 5*s.b*s.b; return Q(s.a/n, -s.b/n)
    def __truediv__(s, o): return s * Q.c(o).inv()
    def gal(s): return Q(s.a, -s.b)
    def __eq__(s, o): o = Q.c(o); return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def iszero(s): return s.a == 0 and s.b == 0
    def __repr__(s): return f"({s.a}+{s.b}r5)" if s.b else f"{s.a}"
ZERO, ONE = Q(0), Q(1)
PHI = Q(Fr(1, 2), Fr(1, 2)); IPHI = PHI - 1; R5 = Q(0, 1)

def dot(u, v):
    t = ZERO
    for x, y in zip(u, v): t = t + x*y
    return t
def cheb(k, c):                             # U_k(c): zonal harmonic of degree k on S^3
    u0, u1 = ONE, 2*c
    if k == 0: return u0
    for _ in range(k - 1): u0, u1 = u1, 2*c*u1 - u0
    return u1
def kills(points, kmax, x0=None):
    """degrees 1..kmax killed by a set (sum of zonal over all pairs = 0)."""
    n2 = dot(points[0], points[0])
    cnt = Counter()
    for x in ([x0] if x0 is not None else points):
        for y in points: cnt[dot(x, y)/n2] += 1
    out = []
    for k in range(1, kmax + 1):
        t = ZERO
        for c, m in cnt.items(): t = t + m*cheb(k, c)
        if t.iszero(): out.append(k)
    return out
def gram(points):
    n2 = dot(points[0], points[0])
    return [[dot(x, y)/n2 for y in points] for x in points]
def isos(GA, GB, count_all=True):
    """number of Gram-preserving bijections A->B (A spans a 4-space)."""
    n = len(GA)
    # greedy basis of 4 points with nonsingular Gram
    def det(M):
        M = [r[:] for r in M]; d = ONE; m = len(M)
        for i in range(m):
            p = next((r for r in range(i, m) if not M[r][i].iszero()), None)
            if p is None: return ZERO
            if p != i: M[i], M[p] = M[p], M[i]; d = -d
            d = d*M[i][i]
            for r in range(i + 1, m):
                f = M[r][i]/M[i][i]
                M[r] = [a - f*b for a, b in zip(M[r], M[i])]
        return d
    B = []
    for i in range(n):
        T = B + [i]
        if not det([[GA[a][b] for b in T] for a in T]).iszero(): B = T
        if len(B) == 4: break
    found = 0
    def rec(img):
        nonlocal found
        if len(img) == 4:
            used = set(); 
            mp = []
            for p in range(n):
                q = [j for j in range(n) if all(GB[j][img[i]] == GA[p][B[i]] for i in range(4))]
                if len(q) != 1 or q[0] in used: return
                used.add(q[0]); mp.append(q[0])
            if all(GA[p][r] == GB[mp[p]][mp[r]] for p in range(n) for r in range(n)): found += 1
            return
        i = len(img)
        for j in range(n):
            if j in img: continue
            if all(GB[j][img[t]] == GA[B[i]][B[t]] for t in range(i)):
                rec(img + [j])
                if found and not count_all: return
    rec([])
    return found
def ok(name, cond): print(f"CHECK {name}: {'OK' if cond else 'FAIL'}")

KMAX = 30
print("== A. The 20-set X from its definition (R^5, centred) ==")
def centred(v):
    m = (v[0] + v[1] + v[2] + v[3] + v[4])/5
    return tuple(x - m for x in v)
def orbit5(v): return sorted({tuple(p) for p in permutations(v)}, key=repr)
P2 = PHI*PHI
X = [centred(p) for p in orbit5((P2, P2, P2, PHI, ZERO))]
GX = gram(X)
cosset = {c for r in GX for c in r}
C600 = {ZERO, ONE, -ONE, Q(Fr(1, 2)), Q(Fr(-1, 2)), PHI/2, -PHI/2, IPHI/2, -(IPHI/2)}
ok("X has 20 points, cosines in the 600-cell set", len(X) == 20 and cosset <= C600)
print("   cosine distribution from one point:", sorted(Counter(GX[0]).items(), key=lambda t: repr(t[0])))
nx = isos(GX, GX)
print("   Gram automorphisms of X:", nx); ok("symmetry group of X has order 120", nx == 120)
def refl(s, t): f = 2*dot(s, t)/dot(t, t); return tuple(a - f*b for a, b in zip(s, t))
V = set(X); grew = True
while grew:
    grew = False
    for s in list(V):
        for t in list(V):
            r = refl(s, t)
            if r not in V: V.add(r); grew = True
    if len(V) > 200: break
V = sorted(V, key=repr)
cosV = {dot(x, y)/dot(x, x) for x in V[:1] for y in V}
ok("reflection closure of X has 120 points with 600-cell cosines (H4 roots)", len(V) == 120 and cosV <= C600)
kv = kills(V, KMAX)
print("   600-cell kills:", kv)
# S5-orbits (coordinate permutations) of the 120 points
left = set(V); orbs = []
while left:
    v = sorted(left, key=repr)[0]; o = {tuple(v[i] for i in p) for p in permutations(range(5))}
    orbs.append(sorted(o, key=repr)); left -= o
def shape(v):                                # shift so min coordinate is 0, report sorted coordinates
    m = min(v, key=lambda q: float(q.a) + float(q.b)*5**.5)
    return sorted([x - m for x in v], key=lambda q: float(q.a) + float(q.b)*5**.5)
killsA = {}
for o in orbs:
    neg = sorted([tuple(-x for x in v) for v in o], key=repr)
    kk = kills(o, KMAX, x0=o[0]); killsA[len(o), tuple(kk)] = o
    print(f"   S5-orbit size {len(o):3d} antipodal={neg == o} is_X={o == sorted(X, key=repr)} "
          f"shape(min->0)={shape(o[0])} kills={kk}")
F = [centred(p) for p in orbit5((P2, P2, ONE, ONE, ZERO))]
sF = F[0]; scale = None
for o in orbs:
    if len(o) == 30:
        for v in o:
            # proportional?
            j = next(i for i in range(5) if not sF[i].iszero())
            lam = v[j]/sF[j]
            if all(v[i] == lam*sF[i] for i in range(5)) and lam.a*1.0 + lam.b*5**.5 > 0: scale = lam
ok("the 30-set perms(phi^2,phi^2,1,1,0) is (up to scale) an S5-orbit of the same 600-cell", scale is not None)
print("   X kills:", kills(X, KMAX), "  F(30) kills:", kills(F, KMAX))
mol = [0]*(KMAX + 1); mol[0] = 1
for d in (3, 4, 5):
    for k in range(d, KMAX + 1): mol[k] += mol[k - d]
print("   S5-invariant harmonics, dim by degree 1..:", mol[1:])
print("   degrees forced by S5 (dim 0):", [k for k in range(1, KMAX + 1) if mol[k] == 0])

print("== B. Quaternion model: 2I, the outer automorphism, twisted classes ==")
def qmul(p, q):
    a, b, c, d = p; e, f, g, h = q
    return (a*e - b*f - c*g - d*h, a*f + b*e + c*h - d*g, a*g - b*h + c*e + d*f, a*h + b*g - c*f + d*e)
def qconj(p): return (p[0], -p[1], -p[2], -p[3])
def even_perms(v):
    out = set()
    for p in permutations(range(4)):
        inv = sum(1 for i in range(4) for j in range(i) if p[j] > p[i])
        if inv % 2 == 0: out.add(tuple(v[i] for i in p))
    return out
def signs(v):
    out = set()
    for s in product((1, -1), repeat=4): out.add(tuple(x*e for x, e in zip(v, s)))
    return out
H = Q(Fr(1, 2))
G = set()
for i in range(4):
    for s in (1, -1): G.add(tuple(Q(s) if j == i else ZERO for j in range(4)))
G |= signs((H, H, H, H))
for v in even_perms((PHI/2, H, IPHI/2, ZERO)): G |= signs(v)
G = sorted(G, key=repr)
ok("2I has 120 elements and is closed", len(G) == 120 and all(qmul(G[3], g) in set(G) for g in G) and all(qmul(g, G[57]) in set(G) for g in G))
def sigma(q): w, x, y, z = (t.gal() for t in q); return (w, -x, z, y)
Gs = set(G)
ok("sigma (Galois conjugation, then i->-i, j<->k) maps 2I to 2I", all(sigma(g) in Gs for g in G))
ok("sigma is multiplicative", all(sigma(qmul(a, b)) == qmul(sigma(a), sigma(b)) for a in G[::7] for b in G))
ok("sigma moves the order-10 class to the other one (outer)", any(g[0] == PHI/2 and sigma(g)[0] != PHI/2 for g in G))
def torbit(x, grp=G, sg=sigma): return sorted({qmul(qmul(a, x), qconj(sg(a))) for a in grp}, key=repr)
left = set(G); tw = []
while left:
    x = sorted(left, key=repr)[0]; o = torbit(x); tw.append(o); left -= set(o)
tw.sort(key=lambda o: (len(o), repr(kills(o, 8, x0=o[0]))))
tk = []
for o in tw:
    neg = sorted([tuple(-x for x in v) for v in o], key=repr)
    kk = kills(o, KMAX, x0=o[0]); tk.append(kk)
    print(f"   twisted class size {len(o):3d} antipodal={neg == o} kills={kk}")
cand = [o for o, kk in zip(tw, tk) if len(o) == 20 and kk == kills(X, KMAX)]
ok("X is congruent to a twisted class of 2I (exact Gram isomorphism)", any(isos(GX, gram(o), count_all=False) for o in cand))
cand = [o for o, kk in zip(tw, tk) if len(o) == 30]
ok("F is congruent to a twisted class of 2I (exact Gram isomorphism)", any(isos(gram(F), gram(o), count_all=False) for o in cand))

print("== C. Characters: restriction of V_k (dim k+1) to 2I; prediction versus direct sums ==")
re = [g[0] for g in G]; res = [sigma(g)[0] for g in G]
irr = {"1": [ONE]*120, "2": [cheb(1, c) for c in re], "2'": [cheb(1, c) for c in res],
       "3": [cheb(2, c) for c in re], "3'": [cheb(2, c) for c in res],
       "4": [cheb(1, a)*cheb(1, b) for a, b in zip(re, res)], "4s": [cheb(3, c) for c in re],
       "5": [cheb(4, c) for c in re], "6": [cheb(5, c) for c in re]}
def ip(f, g):
    t = ZERO
    for a, b in zip(f, g): t = t + a*b
    return t/120
ok("the nine characters are orthonormal", all(ip(irr[a], irr[b]) == (ONE if a == b else ZERO) for a in irr for b in irr))
def decomp(k):
    ch = [cheb(k, c) for c in re]; d = {}
    for n, f in irr.items():
        m = ip(ch, f); assert m.b == 0 and m.a.denominator == 1
        if m.a: d[n] = int(m.a)
    return d
stable = ["1", "4", "4s", "5", "6"]
dec = {k: decomp(k) for k in range(0, KMAX + 1)}
for k in range(1, 13): print(f"   V_{k} =", " + ".join(f"{m}*{n}" if m > 1 else n for n, m in dec[k].items()))
ok("pinning degrees: V_3=4s, V_4=5, V_5=6, V_6=3'+4", dec[3] == {"4s": 1} and dec[4] == {"5": 1} and dec[5] == {"6": 1} and dec[6] == {"3'": 1, "4": 1})
print("   zero pattern of twisted characters (pinned by degrees 3,4,5,6 only):")
allok = True
for o, kk in zip(tw, tk):
    zero = {"1": False, "4s": 3 in kk, "5": 4 in kk, "6": 5 in kk, "4": 6 in kk}
    pred = [k for k in range(1, KMAX + 1) if all(zero[n] for n in dec[k] if n in stable)]
    print(f"     class size {len(o)}: zero at {[n for n in stable if zero[n]]}; predicted kills {pred}; direct {kk}")
    allok &= pred == kk
ok(f"theorem prediction = direct exact sums, all five twisted classes, degrees 1..{KMAX}", allok)
print("   A5-invariant harmonics dim (degree 1..):", [sum(m*dec[k].get({"2": "2'", "2'": "2", "3": "3'", "3'": "3"}.get(n, n), 0) for n, m in dec[k].items()) for k in range(1, KMAX + 1)])
print("   ordinary conjugacy classes (sigma = identity): kills predicted by character zeros vs direct")
left = set(G); allok = True
while left:
    x = sorted(left, key=repr)[0]; o = torbit(x, sg=lambda a: a); left -= set(o)
    if len(o) == 1: continue
    i = G.index(x)
    pred = [k for k in range(1, KMAX + 1) if all(irr[n][i].iszero() for n in dec[k])]
    kk = kills(o, KMAX, x0=o[0]); allok &= pred == kk
    print(f"     class size {len(o)}, real part {x[0]}: zero characters {[n for n in irr if irr[n][i].iszero()]}; kills {kk}")
ok("ordinary classes: prediction = direct", allok)

print("== D. Unions of twisted classes: prediction from weighted twisted characters vs direct ==")
byk = {}
for o, kk in zip(tw, tk): byk.setdefault((len(o), tuple(kk[:4])), []).append(o)
Rr = byk[20, (1, 2, 3, 5)][0]; Xa, Xb = byk[20, (1, 2, 5, 7)]; Fa, Fb = byk[30, (1, 2, 3, 6)]
ok("the two 20-classes are negatives of each other, likewise the two 30-classes",
   sorted([tuple(-t for t in v) for v in Xa], key=repr) == Xb and sorted([tuple(-t for t in v) for v in Fa], key=repr) == Fb)
odd = [k for k in range(1, KMAX + 1) if k % 2]
tests = [("R + X + (-X), 60 points", Rr + Xa + Xb, sorted(odd + [2, 6])),
         ("F + (-F), 60 points", Fa + Fb, sorted(odd + [2, 6])),
         ("X + (-X), 40 points", Xa + Xb, sorted(odd + [2])),
         ("R + F, 50 points", Rr + Fa, [1, 2, 3]),
         ("X + (-X) + F, 70 points", Xa + Xb + Fa, [1, 2, 3]),
         ("R + X, 40 points", Rr + Xa, [1, 2, 5, 7]),
         ("X + F, 50 points (either sign choice a)", Xa + Fa, [1, 2]),
         ("X + (-F'), 50 points (other sign choice)", Xa + Fb, [1, 2])]
for name, pts, pred in tests:
    kk = kills(pts, KMAX); print(f"   {name}: predicted {pred if len(pred) < 8 else 'all odd + ' + str([k for k in pred if k % 2 == 0])}; direct {kk}")
    ok("union " + name, kk == pred)

print("== E. 120-cell (cell centres of the 600-cell, 600 points): A5 twisted orbits, direct sums (data, not predicted) ==")
nb = [g for g in G if g[0] == PHI/2]
one = G[[i for i, g in enumerate(G) if g[0] == ONE][0]]
def adj(a, b): return dot(a, b) == PHI/2
cells = [(a, b, c) for i, a in enumerate(nb) for j, b in enumerate(nb) if j > i and adj(a, b) for c in nb[j + 1:] if adj(a, c) and adj(b, c)]
cen = [tuple(w + x + y + z for w, x, y, z in zip(one, a, b, c)) for a, b, c in cells]
C = {qmul(g, v) for g in G for v in cen}
n8 = dot(cen[0], cen[0])
ok("120-cell: 20 cells at a vertex, 600 centres, equal norms", len(cells) == 20 and len(C) == 600 and all(dot(v, v) == n8 for v in C))
ok("120-cell is invariant under left and right multiplication by 2I", all(qmul(g, v) in C and qmul(v, g) in C for g in G[::5] for v in C))
left = set(C); rows = Counter(); tot = 0
while left:
    x = sorted(left, key=repr)[0]; o = torbit(x); left -= set(o); tot += len(o)
    neg = sorted([tuple(-t for t in v) for v in o], key=repr)
    rows[len(o), neg == o, tuple(kills(o, 20, x0=o[0]))] += 1
ok("orbits partition the 600 vertices", tot == 600)
for (n, anti, kk), m in sorted(rows.items(), key=repr): print(f"   {m} orbit(s) of size {n}, antipodal={anti}, kills (<=20) {list(kk)}")
Cs = sorted(C, key=repr)
print("   whole 120-cell kills (<=30):", kills(Cs, KMAX, x0=Cs[0]))
