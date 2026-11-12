#!/usr/bin/env python3
"""The pure swap in six dimensions (lead 3 of studies/2026-11-13-swaps-and-fixed-points; DICTO's 4D scutoid swap, #104 Theorem 1).

Permutohedron of order n (dimension d = n - 1): corners = orderings s of 1..n, corner x with x[s[j]] = j + 1; facets = proper subsets S,
inequality a_S . x >= b_S (regular: a_S = 1_S, b_S = |S|(|S|+1)/2), type of a facet = |S|. At corner s the d facets are the prefix sets
P_k = {s[0..k-1]}, k = 1..d (one of each type), and edge k (opposite P_k) goes to the ordering with places k-1, k swapped.
A sweep by a generic height u: D = down edges at a corner (labelled by the type k of the opposite facet), U = up edges.
Face spanned by an edge set E: it lies in the facets opposite the edges NOT in E; it is lost (its top) iff E <= D, made iff E <= U.
Event class = D (as a set of types); reverse class = U = complement. i = |D|; i = d/2 is the self-reverse class.

TILTED: a_S = 1_S + e_S with e_S small random rationals; corners solved exactly (Fractions) from their d facets + sum(x) = n(n+1)/2;
every corner checked strictly inside all other facets (same face lattice, simple); then each swap-neighbour lies on the line of the d-1
shared facets and is feasible, so it is the other end of that edge (exact). Exact arithmetic throughout; no floats decide anything.
Output: data/<tag>.json and PROGRESS / ok / FAIL lines; FINAL ok only if every control behaves as predicted.
"""
import sys, json, random, itertools, time
from fractions import Fraction as F
from math import comb

def solve(A, b):
    n = len(A); M = [list(A[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        p = next(r for r in range(c, n) if M[r][c] != 0); M[c], M[p] = M[p], M[c]
        pv = M[c][c]; M[c] = [x / pv for x in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c]; M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [M[i][n] for i in range(n)]

def dot(a, x): return sum(p * q for p, q in zip(a, x))

class Perm:
    def __init__(self, n, tilt=None, seed=0):
        self.n, self.d = n, n - 1
        rng = random.Random(seed)
        self.subsets = [frozenset(c) for k in range(1, n) for c in itertools.combinations(range(n), k)]
        self.a, self.b = {}, {}
        for S in self.subsets:
            a = [F(1) if i in S else F(0) for i in range(n)]
            if tilt: a = [ai + F(rng.randint(-tilt[0], tilt[0]), tilt[1]) for ai in a]
            self.a[S], self.b[S] = a, F(len(S) * (len(S) + 1), 2)
        self.corners = list(itertools.permutations(range(n)))
        self.index = {s: i for i, s in enumerate(self.corners)}
        tot = F(n * (n + 1), 2)
        self.x = []
        for s in self.corners:
            if not tilt:
                x = [F(0)] * n
                for j, e in enumerate(s): x[e] = F(j + 1)
            else:
                Ps = [frozenset(s[:k]) for k in range(1, n)]
                x = solve([self.a[P] for P in Ps] + [[F(1)] * n], [self.b[P] for P in Ps] + [tot])
            self.x.append(x)

    def check_lattice(self):
        """every corner tight exactly on its d prefix facets, strictly inside all others; sum hyperplane kept"""
        bad = 0; tot = F(self.n * (self.n + 1), 2)
        for s, x in zip(self.corners, self.x):
            pre = {frozenset(s[:k]) for k in range(1, self.n)}
            if sum(x) != tot: bad += 1
            for S in self.subsets:
                v = dot(self.a[S], x) - self.b[S]
                if (S in pre and v != 0) or (S not in pre and v <= 0): bad += 1
        return bad

    def nb(self, ci, k):   # neighbour across edge k (opposite prefix facet of type k): swap places k-1, k
        s = list(self.corners[ci]); s[k - 1], s[k] = s[k], s[k - 1]; return self.index[tuple(s)]

    def ledger(self, u):
        L = {}; h = [0] * (self.d + 1)
        ht = [dot(u, x) for x in self.x]
        for ci in range(len(self.corners)):
            D = []
            for k in range(1, self.n):
                dh = ht[self.nb(ci, k)] - ht[ci]
                if dh == 0: raise ValueError('direction not generic')
                if dh < 0: D.append(k)
            D = tuple(D); L[D] = L.get(D, 0) + 1; h[len(D)] += 1
        return L, h

def faces_lost_made(d, D):
    """dims of faces lost (E <= D, E nonempty) and made (E <= U); kinds = types of the facets containing the face (complement of E)"""
    U = tuple(k for k in range(1, d + 1) if k not in D)
    lost = [(len(E), tuple(k for k in range(1, d + 1) if k not in E)) for r in range(1, len(D) + 1) for E in itertools.combinations(D, r)]
    made = [(len(E), tuple(k for k in range(1, d + 1) if k not in E)) for r in range(1, len(U) + 1) for E in itertools.combinations(U, r)]
    return lost, made

def balanced(L, d, i=None):
    """class D against its reverse (complement); returns list of unbalanced (D, N(D), N(comp))"""
    out = []
    for D, c in L.items():
        if i is not None and len(D) != i: continue
        Dc = tuple(k for k in range(1, d + 1) if k not in D)
        if L.get(Dc, 0) != c: out.append((D, c, L.get(Dc, 0)))
    return out

def eulerian(n, k): return sum((-1) ** j * comb(n + 1, j) * (k + 1 - j) ** n for j in range(k + 2))

def beta(n, D):   # permutations of n with descent set exactly D (inclusion-exclusion over multinomials)
    from math import factorial
    tot = 0
    for r in range(len(D) + 1):
        for T in itertools.combinations(D, r):
            pts = [0] + list(T) + [n]; m = factorial(n)
            for a, b in zip(pts, pts[1:]): m //= factorial(b - a)
            tot += (-1) ** (len(D) - r) * m
    return tot

def rand_dir(n, rng):
    return [F(rng.randint(-10**6, 10**6), rng.randint(1, 1000)) for _ in range(n)]

OK = True; checks = {'pass': 0, 'fail': 0}; out = {}
def check(name, cond, info=''):
    global OK
    checks['pass' if cond else 'fail'] += 1; OK &= bool(cond)
    print(('ok   ' if cond else 'FAIL ') + name + (' : ' + str(info) if info != '' else ''), flush=True)

def expect_fail(name, cond_holds, info=''):
    """negative control: the property must FAIL here; record ok if it does"""
    check('negative control ' + name + ' (law must fail)', not cond_holds, info)

def run(tag, n, ndirs, ntilts, tilt, prog0, prog1):
    d = n - 1; rng = random.Random(1000 + n); res = {}
    steps = (1 + ntilts) * ndirs; done = 0
    reg = Perm(n); check(f'n={n} regular: lattice', reg.check_lattice() == 0)
    t0 = time.time(); ledgers = []
    for j in range(ndirs):
        u = rand_dir(n, rng); L, h = reg.ledger(u); ledgers.append(L)
        check(f'n={n} regular dir {j}: h-vector = Eulerian', h == [eulerian(n, k) for k in range(n)], h)
        check(f'n={n} regular dir {j}: every class balanced against its reverse', balanced(L, d) == [])
        done += 1; print(f'PROGRESS {prog0 + (prog1 - prog0) * done / steps:.3f} {tag} regular dir {j} ({time.time() - t0:.0f} s)', flush=True)
    check(f'n={n} regular: ledger identical in all {ndirs} directions', all(L == ledgers[0] for L in ledgers))
    # classical: N(D) = number of permutations with descent set D (in a suitable labelling), beta(D) = beta(complement)
    bvals = sorted(beta(n, D) for D in [tuple(D) for r in range(n) for D in itertools.combinations(range(1, n), r)])
    check(f'n={n} regular: class counts = descent-set numbers beta_n(D) (as a multiset)', sorted(ledgers[0].values()) == bvals and len(ledgers[0]) == 2 ** d)
    res['regular'] = {'classes': {''.join(map(str, D)) or '-': c for D, c in sorted(ledgers[0].items())}, 'h': [eulerian(n, k) for k in range(n)]}
    tilted = []
    for t in range(ntilts):
        P = Perm(n, tilt=tilt, seed=7 * t + n); bad = P.check_lattice()
        check(f'n={n} tilt {t}: same face lattice, simple (exact strict feasibility)', bad == 0, bad)
        Ls = []
        for j in range(ndirs):
            u = rand_dir(n, rng); L, h = P.ledger(u); Ls.append(L)
            check(f'n={n} tilt {t} dir {j}: h-vector = Eulerian', h == [eulerian(n, k) for k in range(n)], h)
            ub = balanced(L, d)
            check(f'n={n} tilt {t} dir {j}: every class balanced against its reverse', ub == [], ub[:4])
            done += 1; print(f'PROGRESS {prog0 + (prog1 - prog0) * done / steps:.3f} {tag} tilt {t} dir {j}', flush=True)
        check(f'n={n} tilt {t}: class counts equal the regular ones in every direction', all(L == ledgers[0] for L in Ls))
        tilted.append({'seed': 7 * t + n, 'ledgers_equal_regular': all(L == ledgers[0] for L in Ls)})
        # negative control: same tilted polytope, facet labels shuffled at random (not one of each type per corner)
        if t == 0:
            r2 = random.Random(99); lab = {S: r2.randint(1, d) for S in P.subsets}
            K = {}
            for ci, s in enumerate(P.corners):
                Ps = [frozenset(s[:k]) for k in range(1, n)]; ht0 = dot(u, P.x[ci])
                Dk = [k for k in range(1, n) if dot(u, P.x[P.nb(ci, k)]) < ht0]
                Uk = [k for k in range(1, n) if k not in Dk]
                # top face lost lies in the facets opposite U, made lies in the facets opposite D: kinds as label multisets
                X = tuple(sorted(lab[Ps[k - 1]] for k in Uk)); Y = tuple(sorted(lab[Ps[k - 1]] for k in Dk))
                K[(X, Y)] = K.get((X, Y), 0) + 1
            unb = [(k, c, K.get((k[1], k[0]), 0)) for k, c in K.items() if K.get((k[1], k[0]), 0) != c]
            expect_fail(f'n={n} tilt 0, random facet labels (no proper colouring): X->Y vs Y->X', unb == [], f'{len(unb)} unbalanced kinds, e.g. {unb[:2]}')
            res['random_labels_unbalanced_kinds'] = len(unb)
    res['tilted'] = tilted
    return res, ledgers[0]

if __name__ == '__main__':
    mode = sys.argv[1]
    T0 = time.time()
    if mode == 'pilot':
        plan = [('4D', 5, 3, 2, (1, 200)), ('6D', 7, 1, 1, (1, 400))]
    else:
        plan = [('4D', 5, 10, 10, (1, 200)), ('6D', 7, 8, 8, (1, 400)), ('6D-coarse', 7, 4, 4, (1, 100))]
    for q, (tag, n, nd, nt, tilt) in enumerate(plan):
        r, L = run(tag, n, nd, nt, tilt, q / len(plan), (q + 1) / len(plan)); out[tag] = r; d = n - 1
        if n == 5:
            # #108 / rosette-balance: 4D permutohedron swaps 6 / 16 / 11 each way (classes {1,2}|{3,4}, {1,3}|{2,4}, {1,4}|{2,3})
            sw = sorted(L.get(D, 0) for D in [(1, 2), (1, 3), (1, 4)])
            check('4D permutohedron swap counts 6, 11, 16 each way (rosette-balance control)', sw == [6, 11, 16] and
                  sorted(L.get(D, 0) for D in [(3, 4), (2, 4), (2, 3)]) == [6, 11, 16], sw)
        if tag == '6D':
            i3 = {D: c for D, c in L.items() if len(D) == 3}
            check('6D: the i = 3 class has 2416 corners', sum(i3.values()) == 2416, sum(i3.values()))
            lost, made = faces_lost_made(d, (1, 2, 3))
            dims_l = sorted(set(x[0] for x in lost)); dims_m = sorted(set(x[0] for x in made))
            check('6D i = 3: faces lost have dims 1,2,3 only, no 4-face (contact of two facets) and no facet lost or made',
                  dims_l == [1, 2, 3] and dims_m == [1, 2, 3], (dims_l, dims_m))
            check('6D i = 3: exactly one 3-face lost and one made (each the meeting of 3 facets)',
                  sum(1 for x in lost if x[0] == 3) == 1 and sum(1 for x in made if x[0] == 3) == 1)
            # all six-dim events: which dims of faces are lost at each i
            ev = {i: sorted(set(x[0] for x in faces_lost_made(d, tuple(range(1, i + 1)))[0])) for i in range(d + 1)}
            out['6D']['dims_lost_by_i'] = ev
            out['6D']['i3_pairs'] = [[''.join(map(str, D)), c, ''.join(map(str, [k for k in range(1, 7) if k not in D])),
                                     i3[tuple(k for k in range(1, 7) if k not in D)]] for D, c in sorted(i3.items()) if D < tuple(k for k in range(1, 7) if k not in D)]
            # negative control: the i = 2 classes against i = 2 classes (wrong partner: i = 2 reverses to i = 4)
            i2 = {D: c for D, c in L.items() if len(D) == 2}
            # pair D with the 2-set obtained by complement inside {1..6} restricted to size 2 is impossible; test N(D) = N(shift D)
            sh = [(D, c, i2.get(tuple(sorted(k % 6 + 1 for k in D)), 0)) for D, c in i2.items() if i2.get(tuple(sorted(k % 6 + 1 for k in D)), 0) != c]
            expect_fail('6D i = 2 paired with a wrong partner (shifted types)', sh == [], f'{len(sh)} mismatches')
            nd2 = sum(c for D, c in L.items() if len(D) == 2); nd4 = sum(c for D, c in L.items() if len(D) == 4)
            check('6D births/deaths pair: i = 2 total = i = 4 total (1191)', nd2 == nd4 == 1191, (nd2, nd4))
    # negative control: moved 16-cell (rosette-balance Theorem 4), non-simple, exact
    V = [(10, 2, -1, 0), (-10, 1, 0, 1), (1, 8, -2, 0), (1, -10, 1, -1), (0, -2, 10, 2), (-1, 2, -9, -2), (-1, -2, 1, 9), (-2, -1, 1, -8)]
    hts = [-3 * v[0] + v[3] for v in V]
    downs = [sum(1 for j in range(8) if j != i and j // 2 != i // 2 and hts[j] < hts[i]) for i in range(8)]
    N = {k: downs.count(k) for k in range(7)}
    check('moved 16-cell heights -30, -4, -3, -2, 1, 2, 12, 31 (rosette-balance)', sorted(hts) == [-30, -4, -3, -2, 1, 2, 12, 31], sorted(hts))
    expect_fail('moved 16-cell (non-simple): N(1 down) = N(5 down)', N[1] == N[5], f'N1 = {N[1]}, N5 = {N[5]}')
    out['checks'] = checks; out['seconds'] = round(time.time() - T0, 1)
    json.dump(out, open(f'data/pure-swap-{mode}.json', 'w'), indent=1, default=str)
    print(f"checks {checks['pass']} ok, {checks['fail']} FAIL; {time.time() - T0:.0f} s", flush=True)
    sys.exit(0 if OK else 1)
