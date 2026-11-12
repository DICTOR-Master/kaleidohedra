# own_check.py: independent recomputation (kind B) of Babanskyy, "Type-A Poset Cones and Extension Tilers" (aiXiv 2610.01847).
# None of the author's code is imported. Convention (as stated in the paper): a linear extension is the word w = (w[0], ..., w[n-1])
# listing the elements bottom to top; a relabelled copy is a.w with (a.w)[i] = a[w[i]]; P is an EXTENSION TILER if some A in S_n has
# {a.w : a in A, w in L(P)} = S_n with every product once.
# (1) P038 (0<1, 1<2, 1<3, 4<3, 4<5, 5<2): |L| = 15; A = HK u H tau K with the stated generators has 48 elements and the 720 products
#     cover S_6 once each. Negative control: replacing tau by the identity must fail.
# (2) Theorem 1.1 through n = 5: for every poset on n <= 5 elements (all labelled posets, reduced up to isomorphism), decide tiling by an
#     exact-cover SAT search (pysat) and compare with series-parallel (= no induced N, the 4-element zigzag a<c, b<c, b<d).
#     Controls: the antichain and the chain tile (A = {id}, resp. A = S_n); the N tiles nothing on 4 elements (known small case).
import sys, itertools, time
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
t0 = time.time()
def compose(p, q): return tuple(p[i] for i in q)
def gen_group(gens, n):
    e = tuple(range(n)); G = {e}; todo = [e]
    while todo:
        x = todo.pop()
        for g in gens:
            y = compose(g, x)
            if y not in G: G.add(y); todo.append(y)
    return G
def perm_from_cycles(cycles, n):
    p = list(range(n))
    for c in cycles:
        for i in range(len(c)): p[c[i]] = c[(i + 1) % len(c)]
    return tuple(p)
def extensions(n, rel):
    out = []
    for w in itertools.permutations(range(n)):
        pos = {x: i for i, x in enumerate(w)}
        if all(pos[a] < pos[b] for a, b in rel): out.append(w)
    return out
ok = True
def check(name, cond):
    global ok; ok &= bool(cond); print(('ok   ' if cond else 'FAIL ') + name, flush=True)

# (1) P038
rel = [(0, 1), (1, 2), (1, 3), (4, 3), (4, 5), (5, 2)]; L = extensions(6, rel)
check(f'(1) P038 has {len(L)} linear extensions (paper 15)', len(L) == 15)
H = gen_group([perm_from_cycles([(2, 3), (4, 5)], 6), perm_from_cycles([(0, 1), (3, 5)], 6)], 6)
K = gen_group([perm_from_cycles([(2, 3), (4, 5)], 6), perm_from_cycles([(0, 4, 5), (1, 3, 2)], 6)], 6)
def build_A(tau):
    HK = {compose(h, k) for h in H for k in K}; HtK = {compose(compose(h, tau), k) for h in H for k in K}
    return HK, HtK
HK, HtK = build_A(perm_from_cycles([(3, 4)], 6)); A = HK | HtK
check(f'(1) |H| = {len(H)}, |K| = {len(K)}, |HK| = {len(HK)}, |H tau K| = {len(HtK)}, disjoint: {not (HK & HtK)}, |A| = {len(A)} (paper 24 + 24 = 48)',
      len(HK) == 24 and len(HtK) == 24 and not (HK & HtK) and len(A) == 48)
from collections import Counter
cnt = Counter(compose(a, w) for a in A for w in L)
check(f'(1) the {len(A) * len(L)} products a.w cover {len(cnt)} of 720 permutations, multiplicities {sorted(set(cnt.values()))} (paper: all 720 once)',
      len(cnt) == 720 and set(cnt.values()) == {1})
HK0, HtK0 = build_A(tuple(range(6))); cnt0 = Counter(compose(a, w) for a in HK0 | HtK0 for w in L)
check(f'(1) negative control (tau = identity): covers {len(cnt0)} of 720 -> not a tiling', not (len(cnt0) == 720 and set(cnt0.values()) == {1}))

# (2) all posets on n <= 5
def posets(n):
    pairs = [(a, b) for a in range(n) for b in range(n) if a != b]
    seen = set(); out = []
    # enumerate strict partial orders as transitively closed acyclic relations, naturally labelled (a<b only if a<b as ints)
    up = [(a, b) for a in range(n) for b in range(a + 1, n)]
    for mask in range(1 << len(up)):
        R = {up[i] for i in range(len(up)) if mask >> i & 1}
        if any((a, c) not in R for (a, b) in R for (b2, c) in R if b == b2): continue
        key = min(tuple(sorted((p[a], p[b]) for a, b in R)) for p in itertools.permutations(range(n)))
        if key in seen: continue
        seen.add(key); out.append(sorted(R))
    return out
def has_induced_N(n, R):
    S = set(R)
    for a, b, c, d in itertools.permutations(range(n), 4):
        if (a, c) in S and (b, c) in S and (b, d) in S and (a, d) not in S and (d, a) not in S and \
           all((x, y) not in S for x, y in [(a, b), (b, a), (c, d), (d, c)]): return True
    return False
def tiles(n, R):
    L = extensions(n, R); N = list(itertools.permutations(range(n))); idx = {p: i for i, p in enumerate(N)}
    if len(N) % len(L): return False
    cover = [[] for _ in N]
    for i, a in enumerate(N):
        for w in L: cover[idx[compose(a, w)]].append(i + 1)
    s = Cadical153(); top = len(N)
    for lits in cover:
        enc = CardEnc.equals(lits, 1, top_id=top, encoding=EncType.seqcounter); top = max(top, enc.nv)
        for cl in enc.clauses: s.add_clause(cl)
    r = s.solve(); s.delete(); return r
tot = 0; agree = 0
for n in range(1, 6):
    P = posets(n); t = [(R, tiles(n, R), not has_induced_N(n, R)) for R in P]
    a = sum(1 for _, x, y in t if x == y); tot += len(P); agree += a
    nsp = sum(1 for _, _, y in t if not y); nt = sum(1 for _, x, _ in t if x)
    check(f'(2) n = {n}: {len(P)} posets up to isomorphism, {nt} tile, {nsp} not series-parallel; tiler <=> series-parallel for {a} of {len(P)}', a == len(P))
check(f'(2) census sizes 1, 2, 5, 16, 63 (OEIS A000112)', [len(posets(n)) for n in range(1, 6)] == [1, 2, 5, 16, 63])
check('(2) controls: antichain and chain on 5 tile; N on 4 does not', tiles(5, []) and tiles(5, [(i, j) for i in range(5) for j in range(i + 1, 5)]) and not tiles(4, [(0, 2), (1, 2), (1, 3)]))
# (3) Appendix B data for the order polytope O(P038) = {0 <= x <= 1, x_i <= x_j for i <_P j}, our own computation:
#     Ehrhart values L(m) = number of order-preserving maps P -> {0..m}; vertices = 0/1 order-preserving maps (order ideals);
#     facets from the cover relations and the minimal/maximal elements; f-vector from the face lattice (all intersections of facet
#     vertex sets, dimension by affine rank). h* from L(m) in the binomial basis. Linear extensions = h*(1) = 15 (volume x 6!).
import numpy as np
rel6 = rel
def order_maps(m): return [x for x in itertools.product(range(m + 1), repeat=6) if all(x[a] <= x[b] for a, b in rel6)]
Lm = [len(order_maps(m)) for m in range(7)]
check(f'(3) Ehrhart values m = 0..6: {Lm} (paper 1, 13, 77, 302, 917, 2338, 5250)', Lm == [1, 13, 77, 302, 917, 2338, 5250])
from math import comb
# h* coefficients: L(m) = sum_j h_j binom(m + 6 - j, 6)
h = []
for j in range(7):
    h.append(Lm[j] - sum(h[i] * comb(j + 6 - i, 6) for i in range(j)))
check(f'(3) h* = {h} (paper 1 + 6t + 7t^2 + t^3), h*(1) = {sum(h)} = |L| = 15', h == [1, 6, 7, 1, 0, 0, 0] and sum(h) == 15)
V = order_maps(1); check(f'(3) vertices (order ideals) {len(V)} (paper 13)', len(V) == 13)
mins = [i for i in range(6) if not any(b == i for a, b in rel6)]; maxs = [i for i in range(6) if not any(a == i for a, b in rel6)]
F = [[v for v in V if v[a] == v[b]] for a, b in rel6] + [[v for v in V if v[i] == 0] for i in mins] + [[v for v in V if v[i] == 1] for i in maxs]
def dim(S):
    if not S: return -1
    M = np.array(S, float); return int(np.linalg.matrix_rank(M[1:] - M[0])) if len(S) > 1 else 0
check(f'(3) {len(F)} facets, all of dimension {sorted(set(dim(f) for f in F))} (paper 10 facets of dimension 5)', len(F) == 10 and {dim(f) for f in F} == {5})
faces = set(); todo = [frozenset(V)]
while todo:
    S = todo.pop()
    for f in F:
        T = S & frozenset(f)
        if T and T not in faces and T != S: faces.add(T); todo.append(T)
fv = Counter(dim(list(S)) for S in faces)
fvec = [fv[d] for d in range(6)]
check(f'(3) boundary f-vector {fvec} (paper 13, 50, 88, 81, 40, 10)', fvec == [13, 50, 88, 81, 40, 10])
print(f'({time.time() - t0:.0f}s)')
print('FINAL ok: every claim in scope confirmed' if ok else 'FINAL FAIL')
