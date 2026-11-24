"""Audit item 5 of #118 (24 Nov 2026): rotations and mirrors.  Does the Scutoid-Frusta layer have exactly the symmetries of the tiling?
All arithmetic exact: Q(sqrt5) as pairs of Fractions (a + b sqrt5); no floating point anywhere.
 A. The tiling T_gamma of tiling.py / patch.json (tile n + C_A iff gamma in pi'(n + 1_A/2) + sum_{b not in A} [-1/2,1/2] e_b').
    A1. I_h: the orthogonal maps permuting the 12 edge vectors +-e_i are the 120 signed permutations preserving the Gram matrix; for each,
        the Galois conjugate matrix g' acts on the e_i' by the same signed permutation.
    A2. pi'(Z^6) is closed under multiplication by phi'^3 = 2 - sqrt5 (|phi'^3| < 1), so it is dense in R^3 (phi' itself does not keep it).
    A3. gamma lies on no window boundary anywhere (not only in the patch): for each of the 15 face normals N = e_b' x e_c', every
        boundary value of N.x lies in the Z-module spanned by N.e_j'/2, whose denominators divide D_N; N.gamma has a denominator that does not.
    A4. For each g in I_h: d_g = gamma - g' gamma; is d_g in pi'(Z^6)?  (coordinates in the basis e_1',...,e_6' of Q^6; integral or not.)
        By the lemma in the AUDIT note, x -> g x + t is a symmetry of T_gamma iff t = pi(k) with pi'(k) = d_g.
    A5. The symmetric shift gamma = 0: search {-1,0,1}^6 x 20 triples for a tile window having 0 on its boundary (singular shift).
 B. The finite 402-tile patch of the paper: every isometry of the patch fixes the barycentre b of the tile centres and has its linear part
    in I_h (A1); test all 120 maps x -> g(x - b) + b on the set of tiles (centre, triple), exactly.
 C. The layer: equivariance of the cell division (default Rollerball C2, S0, centroid seeds; any core and setting
    given as arguments; the 20 exact runs of exact_cell.py, data/exact/).
    Each piece is compared by its facets (maximal flat faces, as boundary-edge sets of exact points), so the comparison does not
    depend on how a flat facet was triangulated.  Checks: (i) the 12 elements of the stabiliser (D3d) of the base triple map its
    pieces onto themselves (72 for the Rollerball: one per core face); (ii) for every other triple A of the same type one g in I_h with g(base) = A maps the pieces of base onto
    the pieces of A.  Together: g(pieces(A)) = pieces(gA) for all 120 g and all 20 A.
Last line FINAL ok only if: |I_h| = 120 with g' acting as g; A2, A3 hold; exactly one g (the identity) has d_g in pi'(Z^6), with k = 0;
B finds only the identity; C (i), (ii) hold for both types in every setting asked.
Usage: python sym_check.py [core:scale:seed ...]  (default C2:S0:cen, the Rollerball of Theorem 1; e.g. C1:S0:cproj;
part C fails with a note if data/exact is absent)."""
import itertools, json, os, sys
from fractions import Fraction as Fr
from math import lcm
HERE = os.path.dirname(os.path.abspath(__file__))
def pr(*a): print(*a, flush=True)

class Q:
    __slots__ = ("a", "b")
    def __init__(s, a=0, b=0): s.a = Fr(a); s.b = Fr(b)
    def __add__(s, o): o = o if isinstance(o, Q) else Q(o); return Q(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __neg__(s): return Q(-s.a, -s.b)
    def __sub__(s, o): o = o if isinstance(o, Q) else Q(o); return Q(s.a - o.a, s.b - o.b)
    def __mul__(s, o): o = o if isinstance(o, Q) else Q(o); return Q(s.a*o.a + 5*s.b*o.b, s.a*o.b + s.b*o.a)
    __rmul__ = __mul__
    def __truediv__(s, o):
        o = o if isinstance(o, Q) else Q(o); n = o.a*o.a - 5*o.b*o.b
        return Q((s.a*o.a - 5*s.b*o.b)/n, (s.b*o.a - s.a*o.b)/n)
    def conj(s): return Q(s.a, -s.b)
    def iszero(s): return s.a == 0 and s.b == 0
    def sign(s):
        a, b = s.a, s.b
        if a >= 0 and b >= 0: return 0 if (a == 0 and b == 0) else 1
        if a <= 0 and b <= 0: return -1
        d = a*a - 5*b*b
        return (1 if d > 0 else -1 if d < 0 else 0)*(1 if a > 0 else -1)
    def key(s): return (s.a, s.b)
    def __repr__(s): return f"{s.a}+{s.b}r5" if s.b else f"{s.a}"
def parseQ(t):
    t = t.strip()
    if "r5" in t: a, b = t[:-2].split("+"); return Q(Fr(a), Fr(b))
    return Q(Fr(t))
def dot(u, v): return u[0]*v[0] + u[1]*v[1] + u[2]*v[2]
def cross(u, v): return [u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]]
def det3(a, b, c): return dot(a, cross(b, c))
def act(g, x): return [dot(g[r], x) for r in range(3)]
def key(v): return tuple(x.key() for x in v)
def absq(x): return x if x.sign() >= 0 else -x

O, I = Q(0), Q(1); PHI = Q(Fr(1, 2), Fr(1, 2))
E = [[O, I, PHI], [O, -I, PHI], [I, PHI, O], [-I, PHI, O], [PHI, O, I], [-PHI, O, I]]   # as tiling.py
EP = [[x.conj() for x in v] for v in E]
TRIPLES = list(itertools.combinations(range(6), 3))
ok = True
def check(cond, msg):
    global ok
    pr(("  ok   " if cond else "  FAIL ") + msg)
    ok = ok and bool(cond)

# ---------- A1: I_h as signed permutations ----------
pr("A1. orthogonal maps permuting the edge vectors +-e_i")
G = [[dot(E[i], E[j]) for j in range(6)] for i in range(6)]
basis = [0, 2, 4]; D0 = det3(*[E[i] for i in basis])
dual = [[x/D0 for x in cross(E[basis[1]], E[basis[2]])], [x/D0 for x in cross(E[basis[2]], E[basis[0]])], [x/D0 for x in cross(E[basis[0]], E[basis[1]])]]
IH = []   # entries (g, perm, signs)
for p in itertools.permutations(range(6)):
    for eps in itertools.product((1, -1), repeat=6):
        if all(((G[p[i]][p[j]]*(eps[i]*eps[j])) - G[i][j]).iszero() for i in range(6) for j in range(i, 6)):
            im = [[x*eps[i] for x in E[p[i]]] for i in basis]
            g = [[sum((im[k][r]*dual[k][c] for k in range(3)), O) for c in range(3)] for r in range(3)]
            IH.append((g, p, eps))
check(len(IH) == 120, f"signed permutations of the six axes preserving the Gram matrix: {len(IH)} (expect 120 = |I_h|)")
allgood = True
for g, p, eps in IH:
    gp = [[x.conj() for x in row] for row in g]
    for i in range(6):
        if key(act(g, E[i])) != key([x*eps[i] for x in E[p[i]]]): allgood = False
        if key(act(gp, EP[i])) != key([x*eps[i] for x in EP[p[i]]]): allgood = False
    gt = [[g[c][r] for c in range(3)] for r in range(3)]
    if any(not (dot(gt[r], [g[0][c], g[1][c], g[2][c]]) - (1 if r == c else 0)).iszero() for r in range(3) for c in range(3)): allgood = False
check(allgood, "each g is orthogonal, g e_i = eps_i e_p(i), and its Galois conjugate g' satisfies g' e_i' = eps_i e_p(i)' (so g' W = W)")
rot = sum(1 for g, _, _ in IH if det3(*[[g[r][c] for r in range(3)] for c in range(3)]).sign() > 0)
pr(f"     rotations {rot}, improper {120 - rot}; contains -1: {any(all((g[r][c] + (1 if r == c else 0)).iszero() for r in range(3) for c in range(3)) for g, _, _ in IH)}")

# ---------- linear algebra over Q on Q^6 = Q(sqrt5)^3 ----------
def flat6(v): return [c for x in v for c in (x.a, x.b)]
Mcols = [flat6(EP[j]) for j in range(6)]            # columns
def solve6(rhs):
    A = [[Mcols[j][r] for j in range(6)] + [rhs[r]] for r in range(6)]
    for c in range(6):
        piv = next(r for r in range(c, 6) if A[r][c] != 0); A[c], A[piv] = A[piv], A[c]
        A[c] = [x/A[c][c] for x in A[c]]
        for r in range(6):
            if r != c and A[r][c] != 0: A[r] = [x - A[r][c]*y for x, y in zip(A[r], A[c])]
    return [A[r][6] for r in range(6)]
def coords(v): return solve6(flat6(v))

# ---------- A2: density ----------
pr("A2. pi'(Z^6) is dense")
PHIC = PHI.conj(); res = {}
for kp in (1, 2, 3):
    f = O + 1
    for _ in range(kp): f = f*PHIC
    res[kp] = all(all(k.denominator == 1 for k in coords([f*x for x in EP[i]])) for i in range(6))
pr(f"     phi'^k pi'(Z^6) inside pi'(Z^6): " + ", ".join(f"k = {kp}: {res[kp]}" for kp in res))
check(res[3], "phi'^3 e_i' is an integer combination of e_1',...,e_6' for every i (phi'^3 = 2 - sqrt5, |phi'^3| < 1): "
      "the module is closed under phi'^3, so it holds arbitrarily short vectors in three independent directions: dense")

# ---------- A3: gamma regular everywhere ----------
P = json.load(open(os.path.join(HERE, "../data/patch.json")))
gamma = [Q(Fr(x)) for x in P["gamma"]]
pr(f"A3. gamma = {P['gamma']} on no window boundary of the infinite tiling")
reg = True
for b, c in itertools.combinations(range(6), 2):
    N = cross(EP[b], EP[c]); vals = [dot(N, EP[j])/2 for j in range(6)]
    Da = lcm(*[v.a.denominator for v in vals]); Db = lcm(*[v.b.denominator for v in vals]); ng = dot(N, gamma)
    if Da % ng.a.denominator == 0 and Db % ng.b.denominator == 0: reg = False; pr(f"     normal e{b+1}' x e{c+1}': not excluded")
check(reg, "for all 15 face normals N, N.gamma is outside the Z-module of boundary values (denominator test)")

# ---------- A4: which g can be symmetries ----------
pr("A4. symmetries of T_gamma: g with gamma - g' gamma in pi'(Z^6)")
hits = []
for idx, (g, p, eps) in enumerate(IH):
    gp = [[x.conj() for x in row] for row in g]
    d = [gamma[r] - dot(gp[r], gamma) for r in range(3)]
    k = coords(d)
    if all(x.denominator == 1 for x in k): hits.append((idx, k))
ident = [idx for idx, (g, p, eps) in enumerate(IH) if p == tuple(range(6)) and all(e == 1 for e in eps)]
check(len(hits) == 1 and hits[0][0] == ident[0] and all(x == 0 for x in hits[0][1]),
      f"g with integral coordinates: {len(hits)} ({'the identity, k = 0' if len(hits) == 1 and hits[0][0] == ident[0] else hits})")
pr("     so T_gamma has no symmetry but the identity: no rotation, mirror, inversion, screw, glide, or translation")

# ---------- A5: gamma = 0 ----------
pr("A5. the symmetric shift gamma = 0")
wit = None
for A in TRIPLES:
    Bc = [b for b in range(6) if b not in A]; Mx = [EP[b] for b in Bc]; Dm = det3(*Mx)
    for n in itertools.product((-1, 0, 1), repeat=6):
        m = [Fr(n[i]) + (Fr(1, 2) if i in A else 0) for i in range(6)]
        d = [-sum((EP[i][r]*m[i] for i in range(6)), O) for r in range(3)]
        ts = [det3(*[d if q == kk else Mx[q] for q in range(3)])/Dm for kk in range(3)]
        if all((absq(x) - Fr(1, 2)).sign() <= 0 for x in ts) and any((absq(x) - Fr(1, 2)).iszero() for x in ts):
            wit = (A, n, ts); break
    if wit: break
if wit: pr(f"     gamma = 0 IS on a window boundary: triple {wit[0]}, n = {wit[1]}, window coordinates {wit[2]} (singular shift)")
else: pr("     no boundary hit in the box {-1,0,1}^6 (not a proof of regularity)")

# ---------- B: the finite patch ----------
pr("B. the finite 402-tile patch")
T = P["tiles"]
tiles = {(key([parseQ(x) for x in t["centre_exact"]]), frozenset(t["A"])) for t in T}
C = [[parseQ(x) for x in t["centre_exact"]] for t in T]
bc = [sum((c[r] for c in C), O)/len(C) for r in range(3)]
pr(f"     tiles {len(tiles)}; triples present {len({frozenset(t['A']) for t in T})} of 20; barycentre of centres {bc}")
sym = []
for idx, (g, p, eps) in enumerate(IH):
    img = set()
    for t in T:
        c = [parseQ(x) for x in t["centre_exact"]]
        y = [dot(g[r], [c[q] - bc[q] for q in range(3)]) + bc[r] for r in range(3)]
        img.add((key(y), frozenset(p[a] for a in t["A"])))
        if (key(y), frozenset(p[a] for a in t["A"])) not in tiles: break
    else:
        if img == tiles: sym.append(idx)
check(sym == ident, f"isometries of the patch: {len(sym)} ({'identity only' if sym == ident else sym})")

# ---------- C: equivariance of the layer ----------
# settings "core:scale:seed" from the command line (default the Rollerball C2:S0:cen of Theorem 1)
SETTINGS = [tuple(a.split(":")) for a in sys.argv[1:]] or [("C2", "S0", "cen")]
XD = os.path.join(HERE, "../data/exact")
KIND = {tuple(t["A"]): t["kind"] for t in T}
def kindA(A): return KIND[tuple(A)]
for core, sc, seed in SETTINGS:
    pr(f"C. the Scutoid-Frusta layer ({core}, {sc}, {seed} seeds): g(pieces(A)) = pieces(gA)")
    if not os.path.exists(os.path.join(XD, f"ammann_{core}_012_{sc}_{seed}.json")):
        pr("     data/exact absent here: part C not run"); ok = False; continue
    def load(A):
        d = json.load(open(os.path.join(XD, f"ammann_{core}_{''.join(map(str, A))}_{sc}_{seed}.json")))
        assert d["valid"] is True and len(d["pieces"]) == d["n_faces"]
        pts = {}
        def pt(s):
            if s not in pts: pts[s] = [parseQ(x) for x in s.split(",")]
            return pts[s]
        pieces = []
        for pc in d["pieces"]:
            pieces.append([[(pt(e[0]), pt(e[1])) for e in fac] for fac in pc["sig"]])
        return pieces
    def canon(pieces, g=None):
        cache = {}
        def m(v):
            k0 = key(v)
            if k0 not in cache: cache[k0] = key(act(g, v)) if g else k0
            return cache[k0]
        return frozenset(frozenset(frozenset(frozenset((m(a), m(b))) for a, b in fac) for fac in pc) for pc in pieces)
    for typ in ("P", "O"):
        As = [A for A in TRIPLES if kindA(A) == typ]; A0 = As[0]; base = load(A0); cb = canon(base)
        check(len(cb) == len(base), f"type {typ}: base triple {A0}: {len(cb)} distinct pieces")
        stab = [(g, p) for g, p, eps in IH if frozenset(p[a] for a in A0) == frozenset(A0)]
        si = all(canon(base, g) == cb for g, p in stab)
        check(len(stab) == 12 and si, f"type {typ}: the {len(stab)} elements of the stabiliser of {A0} map its pieces onto themselves")
        for A in As[1:]:
            g = next(g for g, p, eps in IH if frozenset(p[a] for a in A0) == frozenset(A))
            check(canon(base, g) == canon(load(A)), f"type {typ}: g({A0}) = {A}: g maps the pieces of {A0} onto the pieces of {A}")
            pr(f"PROGRESS {core} {sc} {seed} {(As.index(A) + (0 if typ == 'P' else 10))/20:.2f} {typ} {A}")
pr("FINAL ok" if ok else "FAILED")
