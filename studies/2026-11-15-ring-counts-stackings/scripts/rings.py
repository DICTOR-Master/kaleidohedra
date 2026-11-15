"""Ring counts in the tetrahedral (diamond-type) network of close-packed stackings (study 2026-11-15).
Exact integers and fractions only. Needs the compiled rings_core (gcc -O2 -o rings_core rings_core.c) next to this file.

Network (as #102 and loop_checks.py): bilayer k = lower atom (u=0) and upper atom (u=1) at in-plane position of letter s[k]
(A, B, C = 0, 1, 2); the vertical bond joins them; the upper atom of bilayer k bonds to the three lower atoms of bilayer k+1
at in-plane distance a/sqrt3.  c/h word (Jagodzinski): bilayer k is h if s[k-1] = s[k+1], else c.
In-plane coordinates in thirds of the a1, a2 basis: atom (i, j) of letter p sits at 3(i, j) + p(1, 1); squared length of
(x, y) in units (a/3)^2 is x^2 + xy + y^2, so a bond between letters has squared in-plane length 3.

Usage:
  rings.py named L LNB        named stackings: cycles + SP rings to length L, NB loops to LNB, King/Guttman, strong check,
                              ice polymer series (bond order <= 14), controls
  rings.py local L W          every c/h word of 2W+1 letters around the root bilayer: cycles + SP rings to L, multilinear formula
  rings.py fib L              Fibonacci stacking: several sites, two window sizes (window independence)
  rings.py negative           negative controls only
Output lines: PROGRESS k/N ..., CHECK name ok/FAIL, data lines; last line 'ALLCHECKS ok' or 'ALLCHECKS FAIL'.
"""
import sys, os, subprocess, itertools, random, time
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
CORE = os.path.join(HERE, 'rings_core')
out = lambda *a: print(*a, flush=True)
T0 = time.time()
CHECKS = []
def check(name, ok):
    CHECKS.append((name, bool(ok))); out('CHECK', name, 'ok' if ok else 'FAIL'); return bool(ok)

# ---------------- stackings ----------------
def letters_from_ch(word, n, offset=0):
    """letters s[0..n-1]; bilayer k (1 <= k <= n-2) gets symbol word[(k + offset) % len(word)] (or word[k+offset] if long)."""
    s = [0, 1]
    for k in range(1, n - 1):
        x = word[(k + offset) % len(word)]
        d = (s[k] - s[k - 1]) % 3
        s.append((s[k] + d) % 3 if x == 'c' else s[k - 1])
    return s
def ch_of(s, k): return 'h' if s[k - 1] == s[k + 1] else 'c'
def fib_word(n):
    w = 'c'
    while len(w) < n: w = ''.join('ch' if x == 'c' else 'c' for x in w)
    return w

# ---------------- network on a finite window ----------------
def bond_offsets(p, q):
    r = []
    for di in range(-2, 3):
        for dj in range(-2, 3):
            x, y = 3 * di + (q - p), 3 * dj + (q - p)
            if x * x + x * y + y * y == 3: r.append((di, dj))
    assert len(r) == 3, (p, q, r); return r
OFF = {(p, q): bond_offsets(p, q) for p in range(3) for q in range(3) if p != q}
class Net:
    """window: bilayers 0..K-1 with letters s, in-plane i, j in 0..M-1. Node id ((k*M+i)*M+j)*2+u.
    Neighbour order: index 0 = the vertical bond, 1..3 = the slanted bonds."""
    def __init__(self, s, M):
        self.s, self.K, self.M = s, len(s), M
        K = self.K; n = K * M * M * 2; self.n = n
        nb = [[-1, -1, -1, -1] for _ in range(n)]
        cnt = [1] * n
        for k in range(K):
            for i in range(M):
                for j in range(M):
                    lo = self.id(k, i, j, 0); hi = lo + 1
                    nb[lo][0] = hi; nb[hi][0] = lo
                    if k + 1 < K:
                        for di, dj in OFF[(s[k], s[k + 1])]:
                            i2, j2 = i + di, j + dj
                            if 0 <= i2 < M and 0 <= j2 < M:
                                w = self.id(k + 1, i2, j2, 0)
                                nb[hi][cnt[hi]] = w; cnt[hi] += 1
                                nb[w][cnt[w]] = hi; cnt[w] += 1
        self.nb = nb
    def id(self, k, i, j, u): return ((k * self.M + i) * self.M + j) * 2 + u
    def coords(self, v): u = v % 2; v //= 2; j = v % self.M; v //= self.M; i = v % self.M; k = v // self.M; return k, i, j, u
    def bondtype(self, v, idx): return 'V' if idx == 0 else 'S'

def make_net(word, L, kroot_offset=0, word_is_long=False, root_bilayer=None):
    """window for cycles to length L around root bilayer; returns net and the two roots (lower, upper atom)."""
    K = L + 8; M = 2 * L + 6
    kr = K // 2 if root_bilayer is None else root_bilayer
    if word_is_long:
        s = letters_from_ch(word, K, offset=kroot_offset - kr)
    else:
        s = letters_from_ch(word, K, offset=kroot_offset - kr)
    net = Net(s, M)
    c = M // 2
    return net, [net.id(kr, c, c, 0), net.id(kr, c, c, 1)], kr

def run_core(net, L, roots):
    inp = [f'{net.n} {L} {len(roots)}'] + [' '.join(map(str, r)) for r in net.nb] + [' '.join(map(str, roots))]
    p = subprocess.run([CORE], input='\n'.join(inp) + '\n', capture_output=True, text=True)
    if p.returncode != 0: raise RuntimeError('rings_core failed: ' + p.stderr[-500:])
    res = {r: {} for r in roots}
    for line in p.stdout.splitlines():
        f = line.split()
        if f[0] == 'R':
            r, l = int(f[1]), int(f[2]); v = list(map(int, f[3:]))
            res[r][l] = dict(cyc=v[0], sp=v[1], cb=v[2:6], sb=v[6:10])
    return res

# ---------------- python-side counts (small lengths) ----------------
def bfs(nb, src, maxd, banned=None):
    d = {src: 0}; q = [src]; h = 0
    while h < len(q):
        v = q[h]; h += 1
        if d[v] >= maxd: continue
        for w in nb[v]:
            if w < 0: raise RuntimeError('window too small (bfs)')
            if w == banned or w in d: continue
            d[w] = d[v] + 1; q.append(w)
    return d
def nb_tailless(nb, root, mmax):
    """closed tailless non-backtracking walks at root, lengths 0..mmax (#102 'loops')."""
    dist = bfs(nb, root, mmax // 2 + 1)
    res = [0] * (mmax + 1)
    for a in nb[root]:
        cur = {(root, a): 1}
        for m in range(2, mmax + 1):
            nxt = {}
            for (u, v), c in cur.items():
                for w in nb[v]:
                    if w == u: continue
                    if dist.get(w, 99) > mmax - m: continue
                    nxt[(v, w)] = nxt.get((v, w), 0) + c
            cur = nxt
            res[m] += sum(c for (u, v), c in cur.items() if v == root and u != a)
    return res
def cycles_through(nb, root, L, dist=None):
    """all simple cycles through root of length <= L, each once, as vertex tuples starting at root."""
    if dist is None: dist = bfs(nb, root, L)
    res = []; path = [root]; on = {root}
    def rec(v):
        ln = len(path) - 1
        for w in nb[v]:
            if w == root:
                if ln >= 2 and path[1] < v: res.append(tuple(path))
                continue
            if w in on or dist[w] > L - ln - 1: continue
            on.add(w); path.append(w); rec(w); path.pop(); on.discard(w)
    rec(root); return res
def edges_of(cyc): return frozenset(frozenset((cyc[i], cyc[(i + 1) % len(cyc)])) for i in range(len(cyc)))
def coordination(nb, root, n):
    d = bfs(nb, root, n); return [sum(1 for x in d.values() if x == r) for r in range(n + 1)]
def king_guttman(nb, root):
    """King (1967): for each pair of neighbours of the root, rings = shortest paths between them avoiding the root.
    Guttman (1990): for each neighbour, rings = shortest cycles through the root via that neighbour."""
    nbs = nb[root]; king = {}; gut = {}
    paths = {}
    for a in nbs:
        d = bfs(nb, a, 12, banned=root)
        # number of shortest paths from a to every vertex avoiding root
        order = sorted(d, key=d.get); npth = {a: 1}
        for v in order:
            if v == a: continue
            npth[v] = sum(npth[w] for w in nb[v] if w in d and d[w] == d[v] - 1)
        paths[a] = (d, npth)
    for x, y in itertools.combinations(nbs, 2):
        d, npth = paths[x]; ln = d[y] + 2; king[ln] = king.get(ln, 0) + npth[y]
    for x in nbs:
        d, npth = paths[x]; m = min(d[y] for y in nbs if y != x); ln = m + 2
        gut[ln] = gut.get(ln, 0) + sum(npth[y] for y in nbs if y != x and d[y] == m)
    return king, gut
def gf2_in_span(target, basis_vecs):
    """is the int bit vector target in the GF(2) span of basis_vecs?"""
    piv = {}
    for v in basis_vecs:
        while v:
            h = v.bit_length() - 1
            if h in piv: v ^= piv[h]
            else: piv[h] = v; break
    t = target
    while t:
        h = t.bit_length() - 1
        if h not in piv: return False
        t ^= piv[h]
    return True
def all_short_cycles(nb, centre, R, lens):
    """all cycles of the given lengths with every vertex within distance R of centre (each once, as edge sets)."""
    dc = bfs(nb, centre, R + max(lens))
    found = set()
    for v in [x for x in dc if dc[x] <= R]:
        for c in cycles_through(nb, v, max(lens)):
            if len(c) in lens and min(c) == v and all(dc[x] <= R for x in c): found.add((len(c), c))
    return found
def strong_check(nb, root, Lmax=12, R=8):
    """every cycle through root of length 8..Lmax lies in the GF(2) span of the 6-rings within distance R (=> not strong)."""
    six = [c for (l, c) in all_short_cycles(nb, root, R, {6})]
    eidx = {}
    def vec(c):
        x = 0
        for e in edges_of(c):
            if e not in eidx: eidx[e] = len(eidx)
            x |= 1 << eidx[e]
        return x
    basis = [vec(c) for c in six]
    tested = 0; inspan = 0
    for c in cycles_through(nb, root, Lmax):
        if len(c) >= 8: tested += 1; inspan += gf2_in_span(vec(c), basis)
    return tested, inspan, len(six)

# ---------------- ice polymer series (Nagle's form) ----------------
# Z = (3/2)^N sum_F 3^(-n2(F)) over even subgraphs F (every vertex of even degree; n2 = vertices of degree 2) of the
# 4-regular network: Nagle 1966; written so by Chen-Ran 2026 (arXiv:2608.07613). Mark each bond of F by y.
# Polymers = connected even subgraphs; two polymers are compatible iff vertex-disjoint; ln Xi = sum over connected clusters
# (Mayer / cluster expansion: multiset M of polymers with connected incompatibility graph contributes
# phi(M) prod w / prod mult!, phi = sum over connected spanning subgraphs of the incompatibility graph of (-1)^edges).
# Per-site density at the root: each cluster's term shared equally among the vertices of its support.
# Bond order <= 18 (every polymer has >= 6 bonds, so at most 3 polymers):
#   1 polymer : cycles 6..18 (counts from rings_core), unions of 2 edge-disjoint cycles (6+6 .. 8+10), of 3 hexagons
#   2 polymers: sizes (6,6) (8,8) incl. equal, (6,8) (6,10) (6,12) (8,10), the 12 being a 12-cycle or a 6+6 union
#   3 polymers: three hexagons (equal ones allowed)
def wpoly(E):
    deg = {}
    for e in E:
        for x in e: deg[x] = deg.get(x, 0) + 1
    assert all(d % 2 == 0 for d in deg.values())
    return Fr(1, 3 ** sum(1 for d in deg.values() if d == 2)), frozenset(deg)
def phi_conn(inc):
    """inc: n x n boolean incompatibility (symmetric); sum over connected spanning subgraphs of (-1)^edges."""
    n = len(inc); pairs = [(i, j) for i in range(n) for j in range(i + 1, n) if inc[i][j]]
    tot = 0
    for r in range(len(pairs) + 1):
        for sub in itertools.combinations(pairs, r):
            par = list(range(n))
            def f(x):
                while par[x] != x: x = par[x]
                return x
            for i, j in sub: par[f(i)] = f(j)
            if len({f(i) for i in range(n)}) == 1: tot += (-1) ** r
    return tot
def ice_series(nb, root, cyc_counts, EMAX=18):
    assert EMAX == 18
    coef = [Fr(0)] * (EMAX + 1)
    dist = bfs(nb, root, 9)
    # cycles of length l with a vertex within distance (18 - l) / 2 of root, l = 6..12
    cyc = {}
    for l in (6, 8, 10, 12):
        R = (EMAX - l) // 2
        for v in [x for x in dist if dist[x] <= R]:
            for c in cycles_through(nb, v, l):
                if len(c) == l: cyc.setdefault(edges_of(c), (l, frozenset(c)))
    cl = [(E, l, V) for E, (l, V) in cyc.items()]
    hexes = [(E, V) for E, l, V in cl if l == 6]
    # 6+6 unions (12 bonds) within distance 3 of root, as polymers for the pair clusters
    byv = {}
    for idx, (E, V) in enumerate(hexes):
        for x in V: byv.setdefault(x, []).append(idx)
    unions12 = {}
    for i, (E, V) in enumerate(hexes):
        for x in V:
            for j in byv[x]:
                if j > i and not (E & hexes[j][0]):
                    U = E | hexes[j][0]; VU = V | hexes[j][1]
                    if min(dist.get(y, 99) for y in VU) <= 3: unions12[U] = VU
    polys = [(E, l, V) for E, l, V in cl] + [(U, 12, VU) for U, VU in unions12.items()]
    # single polymers through root: cycles (from rings_core counts), and unions of 2 or 3 edge-disjoint cycles
    for l in range(6, EMAX + 1, 2): coef[l] += Fr(cyc_counts[l], 3 ** l * l)
    singles = {}
    pv = {}
    for idx, (E, l, V) in enumerate(cl):
        for x in V: pv.setdefault(x, []).append(idx)
    for i, (E, l, V) in enumerate(cl):
        for x in V:
            for j in pv[x]:
                if j <= i: continue
                E2, l2, V2 = cl[j]
                if l + l2 > EMAX or (E & E2): continue
                U = E | E2; VU = V | V2
                if root in VU: singles[U] = VU
    for U, VU in list(unions12.items()):          # 6+6+6: a 6+6 union plus an edge-disjoint hexagon touching it
        for x in VU:
            for j in byv.get(x, []):
                E3, V3 = hexes[j]
                if E3 & U: continue
                W = U | E3; VW = VU | V3
                if root in VW: singles[W] = VW
    detail = {}
    for U, VU in singles.items():
        w, V = wpoly(U); assert V == VU; coef[len(U)] += w / len(VU)
        k = ('single', len(U), len(VU)); detail[k] = detail.get(k, 0) + 1
    # pair clusters
    ppv = {}
    for idx, (E, l, V) in enumerate(polys):
        for x in V: ppv.setdefault(x, []).append(idx)
    W = [wpoly(E)[0] for E, l, V in polys]
    for i, (E, l, V) in enumerate(polys):
        if 2 * l <= EMAX and root in V: coef[2 * l] += Fr(-1, 2) * W[i] * W[i] / len(V)
        seen = set()
        for x in V:
            for j in ppv[x]:
                if j <= i or j in seen: continue
                seen.add(j)
                E2, l2, V2 = polys[j]
                if l + l2 > EMAX: continue
                VU = V | V2
                if root in VU:
                    coef[l + l2] += -W[i] * W[j] / len(VU)
                    k = ('pair', tuple(sorted((l, l2))), len(V & V2)); detail[k] = detail.get(k, 0) + 1
    # triple clusters of hexagons (multisets), root in the support
    hx_root = [i for i, (E, V) in enumerate(hexes) if root in V]
    def nbr(i): return {j for x in hexes[i][1] for j in byv.get(x, [])}
    trip = set()
    for X in hx_root:
        NX = nbr(X)
        for Y in NX:
            for Z in NX | nbr(Y):
                trip.add(tuple(sorted((X, Y, Z))))
    w6 = Fr(1, 3 ** 6)
    for t in trip:
        inc = [[bool(hexes[t[a]][1] & hexes[t[b]][1]) for b in range(3)] for a in range(3)]
        ph = phi_conn(inc)
        if ph == 0: continue
        mult = 1
        for k in set(t): mult *= {1: 1, 2: 2, 3: 6}[t.count(k)]
        VU = hexes[t[0]][1] | hexes[t[1]][1] | hexes[t[2]][1]
        coef[18] += Fr(ph, mult) * w6 ** 3 / len(VU)
        k = ('triple', ph, mult); detail[k] = detail.get(k, 0) + 1
    ice_series.detail = detail
    return coef

# ---------------- references ----------------
A038515 = [1, 0, 0, 6, 12, 120, 564, 4074, 25008, 174618, 1181100, 8358306, 59167872]   # closed 2n-step SAWs on diamond
DIAMOND_CYC = {2 * n: 2 * A038515[n] for n in range(3, len(A038515))}                  # cycles through a site = 2 a(n)
NB102 = {6: 24, 8: 48, 10: 480, 12: 3432, 14: 25704, 16: 194256, 18: 1509072, 20: 11820000, 22: 93722376, 24: 750276792}
CS_DIA = [1, 4, 12, 24, 42, 64, 92, 124, 162]         # A005893-type, diamond coordination sequence
CS_LON = [1, 4, 12, 25, 44, 67, 96, 130, 170]         # A008264, lonsdaleite / wurtzite / tridymite

NAMED = [('3C', 'c'), ('2H', 'h'), ('4H', 'hc'), ('6H', 'hcc'), ('8H', 'hccc'), ('9R', 'hhc'), ('10H', 'hcccc'),
         ('15R', 'hchcc'), ('12R', 'hhhc'), ('21R', 'hcchccc'), ('10H*', 'hhchc')]

def site_label(s, kr, u): return f"bilayer {ch_of(s, kr)} ({'lower' if u == 0 else 'upper'} atom), local word {''.join(ch_of(s, k) for k in range(kr - 3, kr + 4))}"

def mode_named(L, LNB):
    out(f'MODE named L={L} LNB={LNB}')
    jobs = []
    sub = os.environ.get('NAMED_ONLY')
    for name, w in [x for x in NAMED if not sub or x[0] in sub.split(',')]:
        for ph in range(len(w)):   # every bilayer of the period as root bilayer
            jobs.append((name, w, ph))
    N = len(jobs); allres = {}
    for t, (name, w, ph) in enumerate(jobs):
        net, roots, kr = make_net(w, L, kroot_offset=ph)
        res = run_core(net, L, roots)
        for u, r in enumerate(roots):
            rr = res[r]
            cyc = [rr[l]['cyc'] for l in range(6, L + 1, 2)]; sp = [rr[l]['sp'] for l in range(6, L + 1, 2)]
            out(f'DATA named {name} phase {ph} u {u} {site_label(net.s, kr, u)}')
            out(f'  cycles l=6..{L} step 2: {cyc}')
            out(f'  SP rings l=6..{L} step 2: {sp}')
            out(f'  per bond (V,S,S,S) cycles: ' + ' | '.join(f"l{l}:{rr[l]['cb']}" for l in range(6, L + 1, 2)))
            out(f'  per bond (V,S,S,S) SP: ' + ' | '.join(f"l{l}:{rr[l]['sb']}" for l in range(6, L + 1, 2) if rr[l]['sp']))
            odd = sum(rr[l]['cyc'] for l in range(3, L + 1, 2))
            check(f'{name} ph{ph} u{u} no odd cycles (bipartite)', odd == 0)
            allres[(name, ph, u)] = rr
            # python-side: NB loops, coordination, King/Guttman, strong
            nbl = nb_tailless(net.nb, r, LNB)
            check(f'{name} ph{ph} u{u} NB loops = #102 values to {LNB}', all(nbl[m] == NB102[m] for m in range(6, LNB + 1, 2)) and all(nbl[m] == 0 for m in range(1, 6)))
            cs = coordination(net.nb, r, 8)
            out(f'  coordination sequence: {cs}')
            king, gut = king_guttman(net.nb, r)
            out(f'  King rings per site (length: number): {king}   Guttman: {gut}')
            check(f'{name} ph{ph} u{u} King = 12 six-rings (2 per angle), Guttman = 24 bond-ring incidences (12 six-rings)', king == {6: 12} and gut == {6: 24})
            if ph == 0:
                tested, inspan, nsix = strong_check(net.nb, r)
                out(f'  strong-ring check: {inspan}/{tested} cycles of length 8..12 in the span of {nsix} nearby 6-rings')
                check(f'{name} ph{ph} u{u} no strong rings of length 8..12', tested > 0 and inspan == tested)
            ice = ice_series(net.nb, r, {l: rr[l]['cyc'] for l in range(6, 19, 2)}) if os.environ.get('ICE', '1') == '1' else [Fr(0)] * 19
            out(f'  ice polymer series per site, y^0..18: {[str(x) for x in ice]}')
            if os.environ.get('ICE', '1') == '1': out('  ice clusters at the site (kind, bonds or sizes, vertices or shared vertices): ' + str(sorted(ice_series.detail.items())))
            allres[(name, ph, u, 'ice')] = ice
        out(f'PROGRESS {(t + 1) / N:.4f} named {t + 1}/{N} {name} phase {ph} ({time.time() - T0:.0f} s)')
    # controls with literature
    d = allres.get(('3C', 0, 0))
    if d: check('3C cycles = 2*A038515 (diamond closed SAWs, Guttmann-Jensen)', all(d[l]['cyc'] == DIAMOND_CYC[l] for l in range(6, L + 1, 2) if l in DIAMOND_CYC))
    for key in [k for k in allres if len(k) == 3]:
        check(f'{key} 12 six-rings per site (Herrero-Ramirez 2013 for Ih, Ic), all SP', allres[key][6]['cyc'] == 12 and allres[key][6]['sp'] == 12)
    # comparison tables
    out('TABLE cycles through a site (self-avoiding polygons), by length')
    for key in sorted(k for k in allres if len(k) == 3):
        out('  ', key, [allres[key][l]['cyc'] for l in range(6, L + 1, 2)])
    out('TABLE SP (primitive) rings through a site, by length')
    for key in sorted(k for k in allres if len(k) == 3):
        out('  ', key, [allres[key][l]['sp'] for l in range(6, L + 1, 2)])
    # period averages
    out('TABLE period averages (per site) of cycles, by length 6..L')
    for name, w in [x for x in NAMED if any(k[0] == x[0] for k in allres)]:
        keys = [k for k in allres if len(k) == 3 and k[0] == name]
        av = [Fr(sum(allres[k][l]['cyc'] for k in keys), len(keys)) for l in range(6, L + 1, 2)]
        hfrac = Fr(w.count('h'), len(w))
        out(f'   {name:5s} h-fraction {str(hfrac):5s} ' + ' '.join(str(x) for x in av))
    out('TABLE ice polymer series, period average per site (coefficients of y^6..y^18 in ln Xi / N)')
    for name, w in [x for x in NAMED if any(k[0] == x[0] for k in allres)]:
        keys = [k for k in allres if len(k) == 4 and k[0] == name]
        av = [sum((allres[k][e] for k in keys), Fr(0)) / len(keys) for e in range(19)]
        out(f'   {name:5s} h-fraction {str(Fr(w.count("h"), len(w))):5s} ' + ' '.join(f'y^{e}:{av[e]}' for e in range(6, 19, 2)))
    return allres

def multilinear(f, n):
    """f: dict from tuples in {0,1}^n (1 = h) to integers; returns {subset: coefficient} with f(x) = sum_S a_S prod_{j in S} x_j."""
    a = {}
    for S in itertools.product((0, 1), repeat=n):
        # Moebius inversion: a_S = sum_{T subset S} (-1)^{|S|-|T|} f(1_T)
        idx = [j for j in range(n) if S[j]]; tot = 0
        for r in range(len(idx) + 1):
            for T in itertools.combinations(idx, r):
                x = tuple(1 if j in T else 0 for j in range(n)); tot += (-1) ** (len(idx) - r) * f[x]
        if tot: a[tuple(idx)] = tot
    return a

def mode_local(L, W, chunk=0, nchunks=1):
    """raw data for every c/h word on bilayers kr-W..kr+W (outside letters c); words with index % nchunks == chunk.
    Every 8th word is recomputed with random outside letters (must not matter) and a doubled in-plane window."""
    out(f'MODE local L={L} W={W} chunk {chunk}/{nchunks}')
    n = 2 * W + 1; words = [x for i, x in enumerate(itertools.product((0, 1), repeat=n)) if i % nchunks == chunk]; N = len(words)
    rng = random.Random(1000 + chunk)
    K = L + 8; kr = K // 2
    for t, x in enumerate(words):
        full = ['c'] * K
        for j in range(n): full[kr - W + j] = 'h' if x[j] else 'c'
        s = letters_from_ch(''.join(full), K, offset=0)
        assert all(ch_of(s, kr - W + j) == ('h' if x[j] else 'c') for j in range(n))
        net = Net(s, 2 * L + 6); c = net.M // 2
        roots = [net.id(kr, c, c, 0), net.id(kr, c, c, 1)]
        res = run_core(net, L, roots)
        vals = {u: (tuple(res[r][l]['cyc'] for l in range(6, L + 1, 2)), tuple(res[r][l]['sp'] for l in range(6, L + 1, 2)), tuple(tuple(res[r][l]['cb']) for l in range(6, L + 1, 2))) for u, r in enumerate(roots)}
        for u in (0, 1):
            out(f"LOCALDATA L {L} W {W} u {u} word {''.join('h' if b else 'c' for b in x)} cyc {' '.join(map(str, vals[u][0]))} sp {' '.join(map(str, vals[u][1]))} bond {';'.join(','.join(map(str, q)) for q in vals[u][2])}")
            check(f'local {x} u{u}: 12 six-rings, no SP ring longer than 6', vals[u][0][0] == 12 and vals[u][1][0] == 12 and sum(vals[u][1][1:]) == 0)
        if t % 8 == 0:
            full2 = list(full)
            for k in range(1, K - 1):
                if not (kr - W <= k <= kr + W): full2[k] = rng.choice('ch')
            s2 = letters_from_ch(''.join(full2), K, offset=0); net2 = Net(s2, 2 * L + 10); c2 = net2.M // 2
            roots2 = [net2.id(kr, c2, c2, 0), net2.id(kr, c2, c2, 1)]
            res2 = run_core(net2, L, roots2)
            check(f'local {x}: outside letters and window size irrelevant', all(tuple(res2[r2][l]['cyc'] for l in range(6, L + 1, 2)) == vals[u][0] for u, r2 in enumerate(roots2)))
        if (t + 1) % max(1, N // 20) == 0 or t + 1 == N: out(f'PROGRESS {(t + 1) / N:.4f} local chunk {chunk} {t + 1}/{N} ({time.time() - T0:.0f} s)')

def mode_analyze(paths):
    """multilinear formulas in the h indicators from LOCALDATA lines (all chunks)."""
    data = {}
    for p in paths:
        for line in open(p):
            if not line.startswith('LOCALDATA'): continue
            f = line.split(); L, W, u, word = int(f[2]), int(f[4]), int(f[6]), f[8]
            i = f.index('cyc'); j = f.index('sp')
            data[(u, word)] = list(map(int, f[i + 1:j]))
    n = 2 * W + 1; words = list(itertools.product((0, 1), repeat=n))
    check(f'analyze: all {2 * len(words)} (site, word) pairs present', all((u, ''.join('h' if b else 'c' for b in x)) in data for u in (0, 1) for x in words))
    lens = list(range(6, L + 1, 2))
    for u in (0, 1):
        out(f'FORMULA site u={u} ({"lower" if u == 0 else "upper"} atom of bilayer 0); h[j] = 1 if bilayer j is h (j = -{W}..{W}), else 0')
        for li, l in enumerate(lens):
            f = {x: data[(u, ''.join('h' if b else 'c' for b in x))][li] for x in words}
            a = multilinear(f, n)
            terms = ' + '.join((f"({v})*" + '*'.join(f'h[{j - W}]' for j in S)) if S else str(v) for S, v in sorted(a.items(), key=lambda z: (len(z[0]), z[0])))
            dep = sorted({j - W for S in a for j in S})
            out(f'  l={l}: values {sorted(set(f.values()))}; depends on bilayers {dep}; = {terms}')
            # edge check: the extreme positions must not appear (window large enough)
            if l <= L: check(f'analyze u={u} l={l}: window edge bilayers -{W}, {W} not needed', not any((0 in S or n - 1 in S) for S in a))

def mode_fib(L):
    out(f'MODE fib L={L}: Fibonacci c/h word, sites at several positions, two window sizes')
    fw = fib_word(5000)
    ok = True
    for t, pos in enumerate([100, 233, 377, 610, 987, 1597, 2001, 2584]):
        vals = []
        for extra in (0, 6):
            Lw = L + extra; K = Lw + 8; kr = K // 2
            s = letters_from_ch(fw, K, offset=pos - kr)
            assert ch_of(s, kr) == fw[pos]
            net = Net(s, 2 * Lw + 6); c = net.M // 2
            roots = [net.id(kr, c, c, 0), net.id(kr, c, c, 1)]
            res = run_core(net, L, roots)
            vals.append([tuple(res[r][l]['cyc'] for l in range(6, L + 1, 2)) for r in roots] + [tuple(res[r][l]['sp'] for l in range(6, L + 1, 2)) for r in roots])
            if extra == 0:
                for u, r in enumerate(roots):
                    nbl = nb_tailless(net.nb, r, min(L, 16))
                    ok &= check(f'fib pos {pos} u{u} NB loops = #102', all(nbl[m] == NB102[m] for m in range(6, min(L, 16) + 1, 2)))
        check(f'fib pos {pos}: window independent', vals[0] == vals[1])
        out(f'DATA fib pos {pos} local word {fw[pos - 4:pos + 5]} (centre {fw[pos]}): cycles lower {vals[0][0]} upper {vals[0][1]}; SP lower {vals[0][2]} upper {vals[0][3]}')
        out(f'PROGRESS {(t + 1) / 8:.4f} fib {t + 1}/8 ({time.time() - T0:.0f} s)')


def ice_bruteforce(nb, EMAX=18):
    """sum over ALL even subgraphs F of a finite graph of y^|E(F)| 3^(-n2(F)) (cycle space, Gray code), then ln, to y^EMAX."""
    V = list(nb); edges = sorted({tuple(sorted((v, w))) for v in nb for w in nb[v]})
    eid = {e: i for i, e in enumerate(edges)}
    # fundamental cycles of a BFS spanning forest
    par = {}; seen = set(); basis = []
    for r0 in V:
        if r0 in seen: continue
        seen.add(r0); par[r0] = None; q = [r0]
        for v in q:
            for w in nb[v]:
                if w not in seen: seen.add(w); par[w] = v; q.append(w)
    def tpath(v):
        p = []
        while par[v] is not None: p.append(eid[tuple(sorted((v, par[v])))]); v = par[v]
        return p
    tree = {eid[tuple(sorted((v, par[v])))] for v in V if par[v] is not None}
    for e in edges:
        if eid[e] in tree: continue
        x = 0
        for i in tpath(e[0]) + tpath(e[1]) + [eid[e]]: x ^= 1 << i
        basis.append(x)
    dim = len(basis)
    deg = {v: 0 for v in V}; poly = [Fr(0)] * (EMAX + 1); cur = 0; ne = 0; n2 = 0
    ends = [e for e in edges]
    def toggle(i):
        nonlocal ne, n2
        a, b = ends[i]; on = (cur >> i) & 1     # state after toggle
        ne += 1 if on else -1
        for x in (a, b):
            d0 = deg[x]; d1 = d0 + (1 if on else -1); deg[x] = d1
            n2 += (d1 == 2) - (d0 == 2)
    poly[0] += 1
    for g in range(1, 2 ** dim):
        k = (g & -g).bit_length() - 1; diff = basis[k]; cur ^= diff
        i = 0; d = diff
        while d:
            if d & 1: toggle(i)
            d >>= 1; i += 1
        if ne <= EMAX: poly[ne] += Fr(1, 3 ** n2)
    # ln(poly) as a power series
    lg = [Fr(0)] * (EMAX + 1)
    for m in range(1, EMAX + 1):     # p' = p * lg'  =>  m lg_m = m p_m - sum_{k<m} k lg_k p_{m-k}
        lg[m] = (m * poly[m] - sum(k * lg[k] * poly[m - k] for k in range(1, m))) / m
    return lg, dim

def mode_icecontrol():
    out('MODE icecontrol: cluster expansion (ice_series, summed over all sites) = brute-force ln Xi on finite pieces, to y^18')
    for t, (w, target) in enumerate([('c', 20), ('h', 20), ('hc', 21), ('c', 23)]):
        net, roots, kr = make_net(w, 20)
        full = net.nb; r0 = roots[0]
        d = bfs(full, r0, 12); order = sorted(d, key=d.get)
        chosen = []
        for v in order:
            chosen.append(v); S = set(chosen)
            E = sum(1 for x in chosen for y in full[x] if y in S) // 2
            if E - len(chosen) + 1 >= target: break
        S = set(chosen); sub = {x: [y for y in full[x] if y in S] for x in chosen}
        lg, dim = ice_bruteforce(sub)
        tot = [Fr(0)] * 19
        for v in chosen:
            cc = cycles_through(sub, v, 18)
            counts = {l: sum(1 for c in cc if len(c) == l) for l in range(6, 19, 2)}
            cv = ice_series(sub, v, counts)
            for e in range(19): tot[e] += cv[e]
        out(f'  piece {w} {len(chosen)} vertices, cycle space dim {dim}: brute {[str(x) for x in lg[6:19:2]]}')
        out(f'  piece {w} cluster expansion                       {[str(x) for x in tot[6:19:2]]}')
        check(f'icecontrol piece {w} dim {dim}: cluster expansion = brute force to y^18', lg == tot and any(lg[12:]))
        out(f'PROGRESS {(t + 1) / 4:.4f} icecontrol {t + 1}/4 ({time.time() - T0:.0f} s)')

def mode_negative():
    out('MODE negative controls')
    net, roots, kr = make_net('c', 12)
    r = roots[0]
    res = run_core(net, 12, [r])
    # 1. a deliberately wrong expectation must be rejected by the same comparison used above
    wrong = dict(DIAMOND_CYC); wrong[12] = 1129
    check('POSITIVE twin: true expectation (2*A038515 to 12) is accepted', all(res[r][l]['cyc'] == DIAMOND_CYC[l] for l in range(6, 13, 2)))
    check('NEGATIVE wrong expectation (diamond 12-cycles = 1129) is rejected', not all(res[r][l]['cyc'] == wrong[l] for l in range(6, 13, 2)))
    # 2. a corrupted network (one bond moved) must break Loop Equality at the root
    nb = [list(x) for x in net.nb]
    a = nb[r][1]; b = nb[a][0]           # move bond r-a to r-b (b = vertical partner of a)
    c2 = nb[b].index(-1) if -1 in nb[b] else None
    nb[r][1] = b; nb[a][nb[a].index(r)] = -2
    nb[b] = nb[b] + [r]
    nb2 = [[w for w in x if w != -2] for x in nb]
    try:
        nbl = nb_tailless(nb2, r, 10); broken = any(nbl[m] != NB102[m] for m in range(6, 11, 2))
    except Exception: broken = True
    check('NEGATIVE corrupted network fails Loop Equality', broken)

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'named': mode_named(int(sys.argv[2]), int(sys.argv[3]))
    elif mode == 'local': mode_local(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))
    elif mode == 'analyze': mode_analyze(sys.argv[2:])
    elif mode == 'fib': mode_fib(int(sys.argv[2]))
    elif mode == 'negative': mode_negative()
    elif mode == 'icecontrol': mode_icecontrol()
    good = all(ok for _, ok in CHECKS) and len(CHECKS) > 0
    out(f'{len(CHECKS)} checks, {sum(1 for _, ok in CHECKS if not ok)} failed ({time.time() - T0:.0f} s)')
    out('ALLCHECKS ok' if good else 'ALLCHECKS FAIL')
    sys.exit(0 if good else 1)
