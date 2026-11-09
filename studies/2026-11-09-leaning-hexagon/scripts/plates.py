"""Plate model of layered RD/TRD-type tilings (Escher stepped hexagon study, 9 Nov 2026).

Carrier: close-packed layers stacked along [111], ball spacing 1, layer spacing H_real = sqrt(2/3).
Heights are integers in units of H_real/12 (so the layer spacing is H = 12).

Fine lattice = A u B u C seat points (triangular lattice of spacing 1/sqrt3).  Point (i,j) = i*g1 + j*g2 with
g1 = (1/2, sqrt3/6) (30 deg), g2 = (0, sqrt3/3) (90 deg).  Coset (seat letter) = (i-j) mod 3 (0=A,1=B,2=C).
Every fine triangle has one vertex of each coset.

A layer-k cell sits on a coset-c_k site X at height 12k.  Its footprint is the hexagon of the 6 fine triangles
around X (vertical side walls, as RD and TRD: hat-sectors study 01_sectors_exact.py).  Over each fine triangle the
cell is a prism between a planar BOTTOM plate and a planar TOP plate (given by values at the 3 corners).  Plates of
neighbouring sectors need not agree on their common edge: a jump there is a vertical step (riser) of the cell.

Layered tiling <=> on every fine triangle, the top plate of the layer-k cell containing it equals the bottom plate of
the layer-(k+1) cell containing it (shifted by H).  Then every triangle column is a stack of prisms whose
consecutive planes coincide, so space is filled exactly once.  All checks below are integer arithmetic (exact).

RD (fcc cell) in these units: top = centre 9, corners toward the next layer's seats 3, other corners 6;
bottom = centre -9, corners under the previous layer's balls -3, others -6.  TRD = same top, bottom = -top.
"""
from fractions import Fraction as Fr
import itertools

H = 12
O = (0, 0)
D = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]   # 6 fine directions, ccw from 30 deg


def add(a, b): return (a[0] + b[0], a[1] + b[1])
def sub(a, b): return (a[0] - b[0], a[1] - b[1])
def coset(p): return (p[0] - p[1]) % 3


def rot(p, r=1):
    for _ in range(r % 6):
        p = (-p[1], p[0] + p[1])
    return p


def mir(p):      # reflection in the line of g1 (30 deg); D_k -> D_{-k}
    return (p[0] + p[1], -p[1])


TRI = [frozenset({O, D[s], D[(s + 1) % 6]}) for s in range(6)]


def sec(vs):
    return TRI.index(frozenset(vs))


def relief(triples):
    """triples[s] = (centre, value at D_s, value at D_{s+1}) for sector s (ccw)."""
    return tuple(tuple(sorted({O: c, D[s]: u, D[(s + 1) % 6]: w}.items())) for s, (c, u, w) in enumerate(triples))


def rd(s):  # helpers to read a relief: dict of sector s
    return dict(s)


def planar(r, m):
    def f(p):
        if m:
            p = mir(p)
        return rot(p, r)
    return f


def map_relief(rel, f, neg=False):
    out = [None] * 6
    for s in range(6):
        d = {f(v): (-x if neg else x) for v, x in rel[s]}
        out[sec(d.keys())] = tuple(sorted(d.items()))
    return tuple(out)


G_ALL = [(r, m, z) for z in (0, 1) for m in (0, 1) for r in range(6)]
G_PROPER = [g for g in G_ALL if g[1] == g[2]]          # rotations, and turned over (C2 about a horizontal axis)


def place(piece, g):
    r, m, z = g
    f = planar(r, m)
    top, bot = piece
    if z == 0:
        return (map_relief(top, f), map_relief(bot, f))
    return (map_relief(bot, f, True), map_relief(top, f, True))


def states(pieces, mirrors=False):
    """distinct placed copies (12 proper placements, 24 with mirror copies) of every piece in the list."""
    G = G_ALL if mirrors else G_PROPER
    seen = {}
    for pi, P in enumerate(pieces):
        for g in G:
            Q = place(P, g)
            if Q not in seen:
                seen[Q] = (pi, g)
    return list(seen.keys()), list(seen.values())


def compat_table(sts):
    """C[s][il] = bitmask of upper states iu that fit on lower state il when upper centre = lower centre + D_s.
    The two cells share the fine triangles s-1 and s of the lower cell; all 3 corner values must agree (+H)."""
    n = len(sts)
    C = [[0] * n for _ in range(6)]
    for s in range(6):
        tris = [TRI[(s - 1) % 6], TRI[s]]
        for il, L in enumerate(sts):
            for iu, U in enumerate(sts):
                ok = True
                for T in tris:
                    lt = dict(L[0][sec(T)])
                    Tu = [sub(v, D[s]) for v in T]
                    ub = dict(U[1][sec(Tu)])
                    for v in T:
                        if lt[v] != ub[sub(v, D[s])] + H:
                            ok = False
                            break
                    if not ok:
                        break
                if ok:
                    C[s][il] |= 1 << iu
    return C


def valid(piece):
    """positive thickness at every corner of every sector, and neighbouring prisms share a wall of positive area."""
    top, bot = piece
    for s in range(6):
        t, b = dict(top[s]), dict(bot[s])
        if any(t[v] <= b[v] for v in t):
            return False
    for s in range(6):
        a, c = (s - 1) % 6, s
        ta, ba, tc, bc = dict(top[a]), dict(bot[a]), dict(top[c]), dict(bot[c])
        # along the radial edge O -> D_s, parameter x in [0,1]
        def lin(d, x): return d[O] + (d[D[s]] - d[O]) * x
        xs = {Fr(0), Fr(1)}
        for p, q in ((ta, tc), (ba, bc)):
            den = (p[D[s]] - p[O]) - (q[D[s]] - q[O])
            if den != 0:
                x = Fr(q[O] - p[O], den)
                if 0 < x < 1:
                    xs.add(x)
        if max(min(lin(ta, x), lin(tc, x)) - max(lin(ba, x), lin(bc, x)) for x in xs) <= 0:
            return False
    return True


def thickness_sum(piece):
    """sum over the 18 sector corners of (top - bottom); a space-filler must have mean thickness H, i.e. 18*H = 216."""
    top, bot = piece
    return sum(dict(top[s])[v] - dict(bot[s])[v] for s in range(6) for v in dict(top[s]))


# ---------------------------------------------------------------- reference pieces
def rd_piece():
    top = relief([(9, 3, 6) if s % 2 == 0 else (9, 6, 3) for s in range(6)])
    bot = relief([(-9, -6, -3) if s % 2 == 0 else (-9, -3, -6) for s in range(6)])
    return (top, bot)


def trd_piece():
    top = relief([(9, 3, 6) if s % 2 == 0 else (9, 6, 3) for s in range(6)])
    bot = map_relief(top, planar(0, 0), True)
    return (top, bot)


# ---------------------------------------------------------------- reassembly: bottom from the tops of 3 lower cells
def reassembled_bottom(top, lean_below, rots):
    """bottom of a cell at O whose 3 lower neighbours (at D_t with coset(D_t) = -lean_below) carry `top`
    turned by rots[0..2] (multiples of 60 deg, upright).  Returns a relief or None."""
    ts = [t for t in range(6) if coset(D[t]) == (-lean_below) % 3]
    bot = [None] * 6
    for t, r in zip(ts, rots):
        Lt = map_relief(top, planar(r, 0))
        # lower cell centre X = D_t; it shares its sectors containing direction -D_t (towards O)
        s = [k for k in range(6) if D[k] == sub(O, D[t])][0]
        for T in (TRI[(s - 1) % 6], TRI[s]):
            vals = dict(Lt[sec(T)])
            Tg = [add(v, D[t]) for v in T]            # global (origin-cell) coordinates
            d = {add(v, D[t]): vals[v] - H for v in T}
            bot[sec(Tg)] = tuple(sorted(d.items()))
    if any(b is None for b in bot):
        return None
    return tuple(bot)


# ---------------------------------------------------------------- patches and tori
def cart2(p):        # squared distance from origin in ball units
    i, j = p
    return Fr(3 * i * i + (i + 2 * j) ** 2, 12)


ORIG = {0: (0, 0), 1: (1, 0), 2: (0, 1)}             # a fixed point of each coset


def layer_cosets(leans):
    c = [0]
    for l in leans:
        c.append((c[-1] + l) % 3)
    return c


def patch_contacts(leans, R):
    """layers 0..len(leans), sites of the layer's coset within radius R; contacts (upper, lower, s)."""
    cs = layer_cosets(leans)
    rng = range(-3 * R - 3, 3 * R + 4)
    cells = {}
    for k, c in enumerate(cs):
        for i in rng:
            for j in rng:
                p = (i, j)
                if coset(p) == c and cart2(p) <= R * R:
                    cells[(k, p)] = len(cells)
    con = []
    for k, l in enumerate(leans):
        for (kk, p), idx in cells.items():
            if kk != k:
                continue
            for s in range(6):
                if coset(D[s]) == l:
                    q = (k + 1, add(p, D[s]))
                    if q in cells:
                        con.append((cells[q], idx, s))
    return cells, con


def sat_solve(ncell, nst, con, C, assumptions=None):
    from pysat.solvers import Cadical153
    from pysat.card import CardEnc
    v = lambda c, i: c * nst + i + 1
    S = Cadical153()
    for c in range(ncell):
        S.add_clause([v(c, i) for i in range(nst)])
        for i in range(nst):
            for j in range(i + 1, nst):
                S.add_clause([-v(c, i), -v(c, j)])
    for (u, l, s) in con:
        Cs = C[s]
        for il in range(nst):
            S.add_clause([-v(l, il)] + [v(u, iu) for iu in range(nst) if Cs[il] >> iu & 1])
        for iu in range(nst):
            S.add_clause([-v(u, iu)] + [v(l, il) for il in range(nst) if Cs[il] >> iu & 1])
    ok = S.solve()
    model = None
    if ok:
        m = set(x for x in S.get_model() if x > 0)
        model = [next(i for i in range(nst) if v(c, i) in m) for c in range(ncell)]
    S.delete()
    return ok, model


def hnf(maxidx):
    out = []
    for n in range(1, maxidx + 1):
        for a in range(1, n + 1):
            if n % a:
                continue
            d = n // a
            for b in range(a):
                out.append((a, b, d))
    return out


A1, A2 = (1, 1), (-1, 2)       # coarse (ball) lattice basis in fine coordinates


def coarse(q):  # q of coset 0 -> coarse coordinates (x,y), q = x*A1 + y*A2
    i, j = q
    y = (j - i) // 3
    x = i + y
    assert (x - y, x + 2 * y) == q
    return x, y


def reduce_mod(xy, M):
    a, b, d = M
    x, y = xy
    t = y // d
    x, y = x - t * b, y - t * d
    return (x % a, y)


def reps(M):
    a, b, d = M
    return [(x, y) for y in range(d) for x in range(a)]


def periodic_alive(C, nst, M):
    """Does a tiling exist whose every layer is periodic under the in-plane sublattice M (any stacking word, any
    vertical period, any skew)?  Layer configurations mod M form a finite graph; edges = compatible next layer
    (lean 1 or 2); a tiling of this kind exists iff the graph has a cycle.  Upper cells only touch lower cells, so
    the successors of a configuration form a product of per-cell allowed sets.  Returns (alive configs, lean-labelled
    edges among alive configs)."""
    R = reps(M)
    idx = {r: n for n, r in enumerate(R)}
    m = len(R)
    # contact structure (same for every coset by translation; take lower layer on coset 0)
    struct = {}
    for lean in (1, 2):
        up = {}
        for n, r in enumerate(R):
            X = (r[0] * A1[0] + r[1] * A2[0], r[0] * A1[1] + r[1] * A2[1])
            for s in range(6):
                if coset(D[s]) == lean:
                    Y = add(X, D[s])
                    q = reduce_mod(coarse(sub(Y, ORIG[lean])), M)
                    up.setdefault(idx[q], []).append((n, s))
        struct[lean] = up
    allconf = list(itertools.product(range(nst), repeat=m))
    cid = {c: n for n, c in enumerate(allconf)}
    succ = {}
    for n, A in enumerate(allconf):
        for lean in (1, 2):
            masks = []
            for q in range(m):
                mk = (1 << nst) - 1
                for (ln, s) in struct[lean][q]:
                    mk &= C[s][A[ln]]
                masks.append(mk)
            if all(masks):
                lists = [[i for i in range(nst) if mk >> i & 1] for mk in masks]
                succ[(n, lean)] = [cid[B] for B in itertools.product(*lists)]
    alive = set(range(len(allconf)))
    while True:
        new = {n for n in alive if any(b in alive for lean in (1, 2) for b in succ.get((n, lean), []))}
        if new == alive:
            break
        alive = new
    edges = [(n, lean, b) for (n, lean), bs in succ.items() if n in alive for b in bs if b in alive]
    return alive, edges, allconf


def ch_words_from_edges(edges, L):
    """c/h words of length L realised by walks in the lean-labelled graph (c = same lean as before, h = other)."""
    out = {}
    adj = {}
    for (a, lean, b) in edges:
        adj.setdefault(a, []).append((lean, b))
    words = set()
    # walks of L+1 edges -> L c/h letters
    frontier = {(a, ()) for a in adj}
    for step in range(L + 1):
        nf = set()
        for (a, w) in frontier:
            for lean, b in adj.get(a, []):
                nf.add((b, w + (lean,)))
        frontier = nf
        if len(frontier) > 200000:
            frontier = set(list(frontier)[:200000])
    for (_, w) in frontier:
        words.add(''.join('c' if w[i] == w[i - 1] else 'h' for i in range(1, len(w))))
    return sorted(words)
