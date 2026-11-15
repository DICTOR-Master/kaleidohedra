"""Type A5 (W = Sym6) under its exceptional outer automorphism xi: the case Proposition 6 (c) must handle (exact, pure Python).
 rho = the reflection representation of Sym6 on {x in R^6 : sum x = 0}, character chi(g) = fix(g) - 1.
 xi is found by search: images of the Coxeter generators s_i = (i i+1) among the 15 triple transpositions satisfying the
 Coxeter relations; it is checked to be a bijective homomorphism that is not inner.
 Checks: chi o xi is neither chi nor chi*sign (so xi is case (c) of Proposition 6) and is not a reflection character;
 the full character tables of Sym6 (Murnaghan-Nakayama) give the action of xi on the irreducibles;
 the twisted classes {a x xi(a)^-1} as points rho(x) on the unit sphere S^24 of End(R^5) (<g,h> = tr(g^T h)/5, Gegenbauer
 lambda = 23/2), their exact silence signatures for k <= KMAX, and the exact dimension of invariant harmonics of the twist group
 X -> rho(g) X rho(xi(g))^-1 at each degree (forced zeros, from power sums and Newton's identities); unforced zeros are listed.
Prints CHECK lines; FINAL ok only if all checks pass."""
import sys, itertools
from fractions import Fraction as Fr
from collections import Counter

KMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 24
fails = 0
def check(ok, what):
    global fails
    if not ok: fails += 1
    print(('CHECK OK   ' if ok else 'CHECK FAIL ') + what, flush=True)

n = 6
G = list(itertools.permutations(range(n)))
idx = {g: i for i, g in enumerate(G)}
def mul(p, q): return tuple(p[q[i]] for i in range(n))   # (p q)(i) = p(q(i))
def inv(p):
    r = [0] * n
    for i, x in enumerate(p): r[x] = i
    return tuple(r)
E = tuple(range(n))
def cyc(p):
    seen, out = set(), []
    for i in range(n):
        if i in seen: continue
        L, j = 0, i
        while j not in seen: seen.add(j); j = p[j]; L += 1
        out.append(L)
    return tuple(sorted(out, reverse=True))
def fix(p): return sum(1 for i in range(n) if p[i] == i)
def sgn(p): return (-1) ** (n - len(cyc(p)))
def chi(p): return fix(p) - 1
def tp(*pairs):
    r = list(range(n))
    for a, b in pairs: r[a], r[b] = b, a
    return tuple(r)
def order(p):
    k, q = 1, p
    while q != E: q = mul(q, p); k += 1
    return k

# --- xi by search on Coxeter generators
S = [tp((i, i + 1)) for i in range(n - 1)]
T3 = [g for g in G if cyc(g) == (2, 2, 2)]
check(len(T3) == 15, 'there are 15 triple transpositions')
def ok_pair(a, b, adj): return order(mul(a, b)) == (3 if adj else 2)
sol = None
def search(chosen):
    global sol
    if sol: return
    k = len(chosen)
    if k == n - 1: sol = list(chosen); return
    for t in T3:
        if all(ok_pair(chosen[j], t, j == k - 1) for j in range(k)):
            search(chosen + [t])
search([])
check(sol is not None, 'Coxeter relations solved by triple transpositions')
# extend to a map by BFS over words
xi = {E: E}
frontier = [E]
while frontier:
    nf = []
    for g in frontier:
        for s, t in zip(S, sol):
            h = mul(g, s)
            if h not in xi: xi[h] = mul(xi[g], t); nf.append(h)
    frontier = nf
check(len(xi) == 720 and len(set(xi.values())) == 720, 'xi is a bijection of Sym6')
check(all(xi[mul(g, h)] == mul(xi[g], xi[h]) for g in G[::7] for h in G), 'xi is a homomorphism (every 7th g against all h)')
check(all(xi[mul(g, h)] == mul(xi[g], xi[h]) for g in G for h in S), 'xi is a homomorphism (all g against generators)')
inner = any(all(xi[s] == mul(mul(c, s), inv(c)) for s in S) for c in G)
check(not inner, 'xi is not inner (no conjugation agrees on the generators)')
check(all(cyc(xi[g]) == (2, 2, 2) for g in G if cyc(g) == (2, 1, 1, 1, 1)), 'xi sends transpositions to triple transpositions (not to reflections)')

# --- characters: chi o xi against chi, chi*sign
classes = sorted(set(cyc(g) for g in G), key=lambda c: (-c[0], c))
csize = Counter(cyc(g) for g in G)
cxi = {c: chi(xi[next(g for g in G if cyc(g) == c)]) for c in classes}
print('class          size  chi  chi*sign  chi o xi')
for c in classes:
    g = next(g for g in G if cyc(g) == c)
    print(f'{str(c):14s} {csize[c]:4d} {chi(g):4d} {chi(g) * sgn(g):8d} {cxi[c]:8d}')
check(all(chi(xi[g]) == cxi[cyc(g)] for g in G), 'chi o xi is a class function')
check(any(cxi[c] != chi(next(g for g in G if cyc(g) == c)) for c in classes), 'chi o xi differs from chi')
check(any(cxi[c] != chi(next(g for g in G if cyc(g) == c)) * sgn(next(g for g in G if cyc(g) == c)) for c in classes), 'chi o xi differs from chi*sign')
check(cxi[(2, 1, 1, 1, 1)] == -1, 'chi o xi has value -1 on transpositions (a reflection of R^5 has trace 3)')
ip = Fr(sum(chi(g) * chi(xi[g]) for g in G), 720)
check(ip == 0, f'<chi, chi o xi> = {ip}: rho o xi is a different irreducible')
# rho o xi is not a reflection representation of the Coxeter system (W, S): the generators s_i act with trace -1, not 3
check(all(chi(xi[s]) == -1 for s in S), 'rho o xi sends every Coxeter generator s_i to a non-reflection (trace -1; a reflection has trace 3)')
check(all(chi(xi[g]) == 3 for g in T3), 'rho o xi sends the triple transpositions to reflections (same matrix group rho(Sym6), other generators)')

# --- full character table by Murnaghan-Nakayama; action of xi on irreducibles
def partitions(m, mx=None):
    if mx is None: mx = m
    if m == 0: yield (); return
    for k in range(min(m, mx), 0, -1):
        for r in partitions(m - k, k): yield (k,) + r
def mn(lam, mu):
    # character of irreducible lam on cycle type mu (rim hooks via beta-numbers)
    if not mu: return 1
    r, rest = mu[0], mu[1:]
    L = len(lam); beta = [lam[i] + (L - 1 - i) for i in range(L)]
    tot = 0
    for i, b in enumerate(beta):
        nb = b - r
        if nb < 0 or nb in beta: continue
        sign = (-1) ** sum(1 for x in beta if nb < x < b)
        newb = sorted([x for x in beta if x != b] + [nb], reverse=True)
        L2 = len(newb); new = tuple(x - (L2 - 1 - j) for j, x in enumerate(newb))
        new = tuple(x for x in new if x > 0)
        tot += sign * mn(new, rest)
    return tot
irr = list(partitions(6))
tab = {lam: {c: mn(lam, c) for c in classes} for lam in irr}
check(all(sum(csize[c] * tab[l][c] * tab[m][c] for c in classes) == (720 if l == m else 0) for l in irr for m in irr), 'character table orthonormal (11 irreducibles)')
check(all(tab[(5, 1)][c] == chi(next(g for g in G if cyc(g) == c)) for c in classes), 'rho = [5,1]')
rep = {c: next(g for g in G if cyc(g) == c) for c in classes}
xmap = {}
for l in irr:
    img = {c: tab[l][cyc(xi[rep[c]])] for c in classes}
    m = [m for m in irr if all(tab[m][c] == img[c] for c in classes)]
    check(len(m) == 1, f'{l} o xi is irreducible')
    xmap[l] = m[0]
stable = [l for l in irr if xmap[l] == l]
print('xi on irreducibles:', ', '.join(f'{l}<->{xmap[l]}' for l in irr if xmap[l] != l and irr.index(l) < irr.index(xmap[l])))
print('xi-stable irreducibles:', stable)
check(xmap[(5, 1)] == (2, 2, 2), 'rho o xi = [2,2,2]')

# --- twist group A(g) = rho(g) (x) rho(xi(g)) on End(R^5): decomposition
trA = {g: chi(g) * chi(xi[g]) for g in G}
norm = Fr(sum(t * t for t in trA.values()), 720)
mult = {l: Fr(sum(trA[g] * tab[l][cyc(g)] for g in G), 720) for l in irr}
print('rho (x) (rho o xi) =', ' + '.join(f'{int(m)}{l}' if m != 1 else f'{l}' for l, m in mult.items() if m))
check(mult[(6,)] == 0 and mult[(1,) * 6] == 0, 'twisted action contains neither the trivial nor the sign character (no hyperplane, no latitude pair)')
print(f'sum chi_A^2/|G| = {norm}')

# --- twisted classes
seen, tclasses = set(), []
for x in G:
    if x in seen: continue
    O = {mul(mul(a, x), inv(xi[a])) for a in G}
    seen |= O; tclasses.append((x, sorted(O)))
check(len(tclasses) == len(stable), f'{len(tclasses)} twisted classes = number of xi-stable irreducibles (Fel\'shtyn-Troitsky)')

# --- Gegenbauer on S^24, lambda = 23/2
lam = Fr(23, 2)
def gegen_all(t, K):
    C = [Fr(1), 2 * lam * t]
    for k in range(2, K + 1):
        C.append((2 * t * (k + lam - 1) * C[-1] - (k + 2 * lam - 2) * C[-2]) / k)
    return C
def matchi(g, h): return chi(mul(inv(g), h))   # tr(rho(g)^T rho(h)) = chi(g^-1 h)

# --- forced zeros: dim of invariant harmonics of the twist group, degree k
def charpoly_coeffs(pows, d):
    # e_1..e_d from power sums p_1..p_d (Newton)
    e = [Fr(1)]
    for k in range(1, d + 1):
        e.append(sum((-1) ** (i - 1) * e[k - i] * pows[i] for i in range(1, k + 1)) / k)
    return e  # det(I - tA) = sum (-1)^k e_k t^k
def series_inv(c, K):
    # 1 / sum c_k t^k up to t^K
    out = [Fr(1) / c[0]]
    for k in range(1, K + 1):
        out.append(-sum(c[j] * out[k - j] for j in range(1, min(k, len(c) - 1) + 1)) / c[0])
    return out
d = 25
poly = [Fr(0)] * (KMAX + 1)
pw = {}
for g in G:
    pows = [None] + [None] * d
    gm, xm = E, E
    for m in range(1, d + 1):
        gm, xm = mul(gm, g), mul(xm, xi[g])
        pows[m] = chi(gm) * chi(xm)
    key = tuple(pows[1:])
    pw[key] = pw.get(key, 0) + 1
for key, cnt in pw.items():
    e = charpoly_coeffs([None] + list(key), d)
    s = series_inv([(-1) ** k * e[k] for k in range(d + 1)], KMAX)
    for k in range(KMAX + 1): poly[k] += cnt * s[k]
poly = [p / 720 for p in poly]
check(all(p.denominator == 1 for p in poly), 'Molien coefficients are integers')
harm = [int(poly[k] - (poly[k - 2] if k >= 2 else 0)) for k in range(KMAX + 1)]
print('invariant harmonics of the twist group, k = 1..%d:' % KMAX, harm[1:])
forced = {k for k in range(1, KMAX + 1) if harm[k] == 0}

# --- signatures
print(f'\ntwisted classes of Sym6 under xi on S^24 (k <= {KMAX}):')
print('rep (cycle type of x)   size  stab  killed                       forced by twist group  unforced')
total_unforced = 0
for x, O in tclasses:
    sums = [Fr(0)] * (KMAX + 1)
    for y in O:
        C = gegen_all(Fr(matchi(x, y), 5), KMAX)
        for k in range(KMAX + 1): sums[k] += C[k]
    killed = [k for k in range(1, KMAX + 1) if sums[k] == 0]
    unf = [k for k in killed if k not in forced]
    total_unforced += len(unf)
    xs = [k for k in killed if k in forced]
    print(f'{str(cyc(x)):22s} {len(O):5d} {720 // len(O):5d}  {str(killed):28s} {str(xs):22s} {unf}')
    check(forced <= set(killed), f'class of size {len(O)} kills every degree the twist group forces')
print(f'\nunforced zeros (by the twist group) over all classes: {total_unforced}')
print('FINAL', 'ok' if fails == 0 else f'FAIL ({fails})')
