"""Twisted classes of the non-crystallographic reflection groups inside their matrix spheres (exact, Q(sqrt5), pure Python).
 W(H3) = {+-R_q : q in 2I} in O(3), points on S^8 in End(R^3) (<g,h> = tr(g^T h)/3, Gegenbauer lambda = 7/2).
 W(H4) = {x -> a x b, x -> a xbar b : a, b in 2I}/+-1 in O(4), points on S^15 in End(R^4) (<g,h> = tr(g^T h)/4, lambda = 7);
 elements are pairs (a, b, c) of 2I indices with a conjugation flag c; the 600-cell coordinates are those of the golden A4 study.
 Twists: id (ordinary classes); Galois sigma = P o (sqrt5 -> -sqrt5) o P^-1 on both factors (outer: changes the reflection character);
 for the rotation subgroup W+(H4) = (2I x 2I)/+-1 also the one-sided twist (sigma on the left factor only), which is an automorphism
 of W+(H4) but NOT of W(H4) (control: it must fail the homomorphism test on W(H4)).
 For each twisted class: exact signature (degrees k <= KMAX killed, sum over the class of the Gegenbauer polynomial of <x0, y>),
 and exact dimension of invariant harmonics of the twist group {X -> g X sigma(g)^-1} (forced zeros), via power sums
 tr(A^m) = tr(g^m) tr(sigma(g)^-m) and Newton's identities.  Unforced zeros are listed.
Prints CHECK lines; FINAL ok only if all checks pass."""
import sys, itertools
from fractions import Fraction as Fr
from collections import Counter

KMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 30
WHICH = sys.argv[2].split(',') if len(sys.argv) > 2 else ['H3', 'H4+', 'H4']
fails = 0
def check(ok, what):
    global fails
    if not ok: fails += 1
    print(('CHECK OK   ' if ok else 'CHECK FAIL ') + what, flush=True)

class Q:
    __slots__ = ('a', 'b')
    def __init__(s, a=0, b=0): s.a = Fr(a); s.b = Fr(b)
    @staticmethod
    def c(x): return x if isinstance(x, Q) else Q(x)
    def __add__(s, o): o = Q.c(o); return Q(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __neg__(s): return Q(-s.a, -s.b)
    def __sub__(s, o): o = Q.c(o); return Q(s.a - o.a, s.b - o.b)
    def __mul__(s, o): o = Q.c(o); return Q(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__
    def __truediv__(s, o):
        o = Q.c(o); n = o.a * o.a - 5 * o.b * o.b; return s * Q(o.a / n, -o.b / n)
    def gal(s): return Q(s.a, -s.b)
    def __eq__(s, o): o = Q.c(o); return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def z(s): return s.a == 0 and s.b == 0
    def __repr__(s): return f'({s.a}+{s.b}r5)' if s.b else f'{s.a}'
ZERO, ONE = Q(0), Q(1)
PHI = Q(Fr(1, 2), Fr(1, 2)); IPHI = PHI - 1; H = Q(Fr(1, 2))
def qmul(p, q):
    a0, a1, a2, a3 = p; b0, b1, b2, b3 = q
    return (a0*b0 - a1*b1 - a2*b2 - a3*b3, a0*b1 + a1*b0 + a2*b3 - a3*b2, a0*b2 - a1*b3 + a2*b0 + a3*b1, a0*b3 + a1*b2 - a2*b1 + a3*b0)
def qconj(p): return (p[0], -p[1], -p[2], -p[3])
def signs(v):
    return {tuple(x * s for x, s in zip(v, sg)) for sg in itertools.product((1, -1), repeat=4)}
def even_perms(v):
    out = []
    for p in itertools.permutations(range(4)):
        if sum(1 for i in range(4) for j in range(i + 1, 4) if p[i] > p[j]) % 2 == 0: out.append(tuple(v[p[i]] for i in range(4)))
    return out
G = set()
for i in range(4):
    e = [ZERO] * 4; e[i] = ONE; G |= signs(e)
G |= signs((H, H, H, H))
for v in even_perms((PHI * H, H, IPHI * H, ZERO)): G |= signs(v)
G = sorted(G, key=repr); N = len(G); idx = {g: i for i, g in enumerate(G)}
check(N == 120, '2I has 120 elements')
MUL = [[idx[qmul(G[i], G[j])] for j in range(N)] for i in range(N)]
INV = [idx[qconj(g)] for g in G]
NEG = [idx[tuple(-t for t in g)] for g in G]
ONEi = idx[(ONE, ZERO, ZERO, ZERO)]
def sig_q(p): w, x, y, z = (t.gal() for t in p); return (w, -x, z, y)
SIG = [idx[sig_q(g)] for g in G]
check(all(SIG[MUL[i][j]] == MUL[SIG[i]][SIG[j]] for i in range(N) for j in range(N)), 'sigma (Galois, then i->-i, j<->k) is an automorphism of 2I')
RE = [g[0] for g in G]
DOT = lambda i, j: sum((x * y for x, y in zip(G[i], G[j])), ZERO)

def gegen(k, lam, x):
    c0, c1 = ONE, 2 * lam * x
    if k == 0: return c0
    for n in range(2, k + 1):
        c0, c1 = c1, (2 * x * (n + lam - 1) * c1 - (n + 2 * lam - 2) * c0) * Q(Fr(1, n))
    return c1

def analyse(name, elems, mul, inv, trace, dimn, twists):
    """generic: elems list of hashable canonical elements, mul/inv functions, trace(g) exact; twists dict name -> function"""
    lam = Q(Fr(dimn * dimn - 2, 2))
    n = len(elems); eset = set(elems)
    print(f'== {name}: {n} elements, points on S^{dimn*dimn-1}', flush=True)
    rows = []
    for tname, s in twists.items():
        hom = all(s(mul(a, b)) == mul(s(a), s(b)) for a in elems[::97] for b in elems[::89]) and len({s(a) for a in elems}) == n and all(s(a) in eset for a in elems)
        if tname.startswith('WRONG'):
            check(not hom, f'{name} {tname}: not an automorphism (control)'); continue
        check(hom, f'{name} {tname}: automorphism')
        outer = any(not (trace(s(a)) == trace(a)) for a in elems)
        print(f'   twist {tname}: changes the character (outer, Galois-type): {outer}')
        # forced dims: power sums p_m = tr(g^m) tr(sigma(g)^-m), h_k by Newton, harmonic = h_k - h_{k-2}
        forced = {}
        pw = {}
        dims = [ZERO] * (KMAX + 1)
        for a in elems:
            sa = s(a)
            gm, sm = a, inv(sa); p = [None]
            for m in range(1, KMAX + 1):
                p.append(trace(gm) * trace(sm))
                gm = mul(gm, a); sm = mul(sm, inv(sa))
            h = [ONE]
            for k in range(1, KMAX + 1):
                t = ZERO
                for m in range(1, k + 1): t = t + p[m] * h[k - m]
                h.append(t * Q(Fr(1, k)))
            for k in range(1, KMAX + 1): dims[k] = dims[k] + h[k] - (h[k - 2] if k >= 2 else ZERO)
        dims = [d * Q(Fr(1, n)) for d in dims]
        check(all(d.b == 0 and d.a.denominator == 1 for d in dims[1:]), f'{name} {tname}: invariant-harmonic dimensions are integers')
        forced = [k for k in range(1, KMAX + 1) if dims[k].z()]
        print(f'   forced (no invariant harmonic) k<={KMAX}: {forced}; dims k=1..12: {[int(d.a) for d in dims[1:13]]}', flush=True)
        left = set(elems); ncl = 0
        while left:
            x0 = min(left)
            O = {mul(mul(a, x0), inv(s(a))) for a in elems}
            left -= O; ncl += 1
            cnt = Counter(trace(mul(inv(x0), y)) * Q(Fr(1, dimn)) for y in O)
            sigk = [k for k in range(1, KMAX + 1) if sum((gegen(k, lam, c) * m for c, m in cnt.items()), ZERO).z()]
            unf = [k for k in sigk if k not in forced]
            rows.append((name, tname, len(O), sigk, unf))
            print(f'SIG {name} {tname} |O|={len(O)} kills<={KMAX}={sigk} UNFORCED={unf}', flush=True)
        print(f'   {tname}: {ncl} twisted classes', flush=True)
    return rows

allrows = []
if 'H3' in WHICH:
    # W(H3) = {(e, q mod +-)}; R_q trace on R^3 = 4 Re(q)^2 - 1; element (e, q) acts as e R_q
    canon = lambda i: min(i, NEG[i])
    els = sorted({(e, canon(i)) for e in (1, -1) for i in range(N)})
    mul = lambda x, y: (x[0] * y[0], canon(MUL[x[1]][y[1]]))
    inv = lambda x: (x[0], canon(INV[x[1]]))
    tr = lambda x: Q(x[0]) * (4 * RE[x[1]] * RE[x[1]] - 1)
    tw = {'id': lambda x: x, 'galois': lambda x: (x[0], canon(SIG[x[1]])), 'WRONG(sign twist)': lambda x: (x[0] * (1 if RE[x[1]] * RE[x[1]] == Q(Fr(1, 4)) else -1), x[1]) if True else x}
    allrows += analyse('W(H3)', els, mul, inv, tr, 3, tw)
    print('PROGRESS 0.20 H3 done', flush=True)
def canon2(a, b, c):
    a2, b2 = NEG[a], NEG[b]
    return min((a, b, c), (a2, b2, c))
def mul4(x, y):
    a, b, c = x; cc, d, e = y
    if c == 0: return canon2(MUL[a][cc], MUL[d][b], e)
    return canon2(MUL[a][INV[d]], MUL[INV[cc]][b], 1 - e)
def inv4(x):
    a, b, c = x
    return canon2(INV[a], INV[b], 0) if c == 0 else canon2(b, a, 1)
def tr4(x):
    a, b, c = x
    return 4 * RE[a] * RE[b] if c == 0 else -2 * DOT(a, b)
if 'H4+' in WHICH:
    els = sorted({canon2(a, b, 0) for a in range(N) for b in range(N)})
    check(len(els) == 7200, f'W+(H4) has {len(els)} elements (7200)')
    tw = {'id': lambda x: x, 'galois both': lambda x: canon2(SIG[x[0]], SIG[x[1]], x[2]),
          'galois left only': lambda x: canon2(SIG[x[0]], x[1], x[2])}
    allrows += analyse('W+(H4)', els, mul4, inv4, tr4, 4, tw)
    print('PROGRESS 0.55 H4+ done', flush=True)
if 'H4' in WHICH:
    els = sorted({canon2(a, b, c) for a in range(N) for b in range(N) for c in (0, 1)})
    check(len(els) == 14400, f'W(H4) has {len(els)} elements (14400)')
    tw = {'id': lambda x: x, 'galois': lambda x: canon2(SIG[x[0]], SIG[x[1]], x[2]),
          'WRONG(left only)': lambda x: canon2(SIG[x[0]], x[1], x[2])}
    allrows += analyse('W(H4)', els, mul4, inv4, tr4, 4, tw)
    print('PROGRESS 1.00 H4 done', flush=True)
print('TABLE unforced silences in matrix spheres (group, twist, size, killed, unforced)')
for r in allrows:
    if r[4]: print('  ', r)
print(f'checks failed: {fails}')
print('FINAL ok' if fails == 0 else 'FINAL FAIL')
