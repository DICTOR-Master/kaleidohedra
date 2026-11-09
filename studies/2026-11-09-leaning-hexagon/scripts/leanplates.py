"""Leaning-plate model (leaning-sided Escher hexagon study, 9 Nov 2026).  Extends plates.py (copied unchanged from
studies/2026-11-09-escher-hexagon) by leaning side walls.

Everything is written in fine-lattice coordinates (i, j) (point = i*g1 + j*g2), which is an affine image of the
plane: planarity, parallelism, incidence, signed area ratios and winding numbers are affine invariants, so every
check here is exact in integers.  Heights are in twelfths of a layer (layer spacing H = 12), as in plates.py.

A cell of layer k sits on a seat X.  At its WAIST (height 12k, the seat level) its cross-section is the regular
hexagon of the 6 fine triangles round X.  Its 6 vertical edges of the vertical model are replaced by LINES
    corner line s :  X + D_s + kappa*(z - 12k)*w_s        (lean w_s, an integer vector; kappa a small scale)
    centre line   :  X + kappa*(z - 12k)*w_c
Side wall s is the strip between corner lines s and s+1.  It is a PLANE (a tilted plate) iff
    w_{s+1} - w_s  is parallel to the rim edge D_{s+1} - D_s = D_{s+2},  i.e.  w_{s+1} = w_s + lam_s * D_{s+2}.
The 6 lams and w_0 parametrise all leaning hexagons with planar sides (closure: the w_s close up round the hexagon).
Top / bottom plates are as in plates.py: planar triangles over the 6 sectors, now with vertices ON the lines.

Contacts.
 * in a layer: neighbours share a wall; the wall planes coincide iff the two cells have the SAME LINES at the two
   shared corners (corner leans equal).  Round a corner where 3 cells meet this is the closure condition (three
   tilted plates meet in one line).  This is the in-plane channel the vertical model did not have.
 * between layers: on every shared fine triangle the plate vertices coincide: heights as in plates.py AND positions:
   lower line at height h meets upper line at height h-12 (upper frame):  h*w_low - (h-12)*w_up = Delta,
   Delta (integer vector) = the drift of the upper layer's waist lattice, one value per interface.
Since the vertical-model conditions are kept, the leaning model's contacts are a SUBSET of the vertical model's
contacts for the same plates: leaning can only remove tilings, never create them.
"""
import sys, itertools
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from plates import *

AC = [add(D[s], D[(s + 1) % 6]) for s in range(6)]      # the 6 neighbour vectors of a layer (coarse lattice)


def neg(v): return (-v[0], -v[1])
def scal(a, v): return (a * v[0], a * v[1])
def det(a, b): return a[0] * b[1] - a[1] * b[0]


def corner_leans(w0, lam):
    """w_0 = w0, w_{s+1} = w_s + lam_s * D_{s+2}; None if the six do not close up."""
    w = [tuple(w0)]
    for s in range(5):
        w.append(add(w[-1], scal(lam[s], D[(s + 2) % 6])))
    if add(w[5], scal(lam[5], D[1])) != tuple(w0):
        return None
    return tuple(w)


def lam_of(w):
    """inverse of corner_leans (None if some wall is not planar)."""
    out = []
    for s in range(6):
        d = sub(w[(s + 1) % 6], w[s])
        e = D[(s + 2) % 6]
        if det(d, e) != 0:
            return None
        out.append(d[0] // e[0] if e[0] else d[1] // e[1])
    return tuple(out)


def make(top, bot, w, wc=(0, 0)):
    return (top, bot, tuple(sorted((D[s], tuple(w[s])) for s in range(6))), tuple(wc))


def flat_relief(v):
    return relief([(v, v, v)] * 6)


def place_l(piece, g):
    r, m, z = g
    f = planar(r, m)
    top, bot, lean, wc = piece
    if z == 0:
        return (map_relief(top, f), map_relief(bot, f), tuple(sorted((f(p), f(w)) for p, w in lean)), f(wc))
    return (map_relief(bot, f, True), map_relief(top, f, True),
            tuple(sorted((f(p), neg(f(w))) for p, w in lean)), neg(f(wc)))


def states_l(pieces, mirrors=False):
    G = G_ALL if mirrors else G_PROPER
    seen = {}
    for pi, P in enumerate(pieces):
        for g in G:
            Q = place_l(P, g)
            if Q not in seen:
                seen[Q] = (pi, g)
    return list(seen.keys()), list(seen.values())


def inlayer_table(sts):
    """T[s][i] = mask of states j allowed at X + AC[s] when state i sits at X (same layer)."""
    n = len(sts)
    L = [dict(st[2]) for st in sts]
    T = [[0] * n for _ in range(6)]
    for s in range(6):
        a, b = D[s], D[(s + 1) % 6]
        a2, b2 = D[(s + 4) % 6], D[(s + 3) % 6]
        for i in range(n):
            for j in range(n):
                if L[i][a] == L[j][a2] and L[i][b] == L[j][b2]:
                    T[s][i] |= 1 << j
    return T


def inter_table(sts, vertical=False):
    """C[Delta][s][il] = mask of upper states at D_s on lower state il with drift Delta (vertical=True: ignore leans)."""
    n = len(sts)
    tops = [[dict(x) for x in st[0]] for st in sts]
    bots = [[dict(x) for x in st[1]] for st in sts]
    leans = [dict(st[2]) for st in sts]
    wcs = [st[3] for st in sts]
    C = {}
    for s in range(6):
        tris = [TRI[(s - 1) % 6], TRI[s]]
        for il in range(n):
            for iu in range(n):
                delta = None
                ok = True
                for T in tris:
                    lt = tops[il][sec(T)]
                    ub = bots[iu][sec([sub(v, D[s]) for v in T])]
                    for v in T:
                        vu = sub(v, D[s])
                        h, hu = lt[v], ub[vu]
                        if h != hu + H:
                            ok = False
                            break
                        if vertical:
                            d = (0, 0)
                        else:
                            wl = wcs[il] if v == O else leans[il][v]
                            wu = wcs[iu] if vu == O else leans[iu][vu]
                            d = sub(scal(h, wl), scal(hu, wu))
                        if delta is None:
                            delta = d
                        elif d != delta:
                            ok = False
                            break
                    if not ok:
                        break
                if ok:
                    C.setdefault(delta, [[0] * n for _ in range(6)])[s][il] |= 1 << iu
    return C


# ---------------------------------------------------------------- geometry of one cell (exact)
def hex_area2(w, z):
    """twice the lattice area of the cross-section at height z (kappa = 1): corners D_s + z*w_s.  Returns the
    polynomial coefficients (a0, a1, a2) of 2*area = a0 + a1 z + a2 z^2."""
    a = [0, 0, 0]
    for s in range(6):
        p, q = D[s], D[(s + 1) % 6]
        u, v = w[s], w[(s + 1) % 6]
        a[0] += det(p, q)
        a[1] += det(p, v) + det(u, q)
        a[2] += det(u, v)
    return tuple(a)


def area_profile(piece):
    w = [dict(piece[2])[D[s]] for s in range(6)]
    return hex_area2(w, None)


# ---------------------------------------------------------------- SAT: patches with in-layer contacts and drift
def lean_patch(leans, R):
    cells, con = patch_contacts(leans, R)
    key = {i: kp for kp, i in cells.items()}
    il = []
    for (k, p), idx in cells.items():
        for s in range(3):
            q = (k, add(p, AC[s]))
            if q in cells:
                il.append((idx, cells[q], s))
    con_k = [(u, l, s, key[l][0]) for (u, l, s) in con]
    return cells, con_k, il


def sat_lean(ncell, nst, con_k, il, T, C, nint, extra=None):
    from pysat.solvers import Cadical153
    v = lambda c, i: c * nst + i + 1
    deltas = sorted(C.keys())
    base = ncell * nst
    dv = lambda k, d: base + k * len(deltas) + d + 1
    S = Cadical153()
    for c in range(ncell):
        S.add_clause([v(c, i) for i in range(nst)])
        for i in range(nst):
            for j in range(i + 1, nst):
                S.add_clause([-v(c, i), -v(c, j)])
    for k in range(nint):
        S.add_clause([dv(k, d) for d in range(len(deltas))])
        for a in range(len(deltas)):
            for b in range(a + 1, len(deltas)):
                S.add_clause([-dv(k, a), -dv(k, b)])
    for (a, b, s) in il:
        Ts = T[s]
        for i in range(nst):
            S.add_clause([-v(a, i)] + [v(b, j) for j in range(nst) if Ts[i] >> j & 1])
        Tb = T[(s + 3) % 6]
        for j in range(nst):
            S.add_clause([-v(b, j)] + [v(a, i) for i in range(nst) if Tb[j] >> i & 1])
    for (u, l, s, k) in con_k:
        for di, d in enumerate(deltas):
            Cs = C[d][s]
            for i in range(nst):
                S.add_clause([-dv(k, di), -v(l, i)] + [v(u, j) for j in range(nst) if Cs[i] >> j & 1])
            for j in range(nst):
                S.add_clause([-dv(k, di), -v(u, j)] + [v(l, i) for i in range(nst) if Cs[i] >> j & 1])
    for cl in (extra or []):
        S.add_clause(cl(v))
    ok = S.solve()
    model = None
    if ok:
        m = set(x for x in S.get_model() if x > 0)
        model = ([next(i for i in range(nst) if v(c, i) in m) for c in range(ncell)],
                 [deltas[next(d for d in range(len(deltas)) if dv(k, d) in m)] for k in range(nint)])
    S.delete()
    return ok, model


# ---------------------------------------------------------------- periodic tilings (finite layer graph)
def torus_struct(M):
    R = reps(M)
    idx = {r: n for n, r in enumerate(R)}
    m = len(R)
    up = {}
    for lean in (1, 2):
        u = {}
        for n, r in enumerate(R):
            X = (r[0] * A1[0] + r[1] * A2[0], r[0] * A1[1] + r[1] * A2[1])
            for s in range(6):
                if coset(D[s]) == lean:
                    Y = add(X, D[s])
                    q = reduce_mod(coarse(sub(Y, ORIG[lean])), M)
                    u.setdefault(idx[q], []).append((n, s))
        up[lean] = u
    nb = []
    for n, r in enumerate(R):
        X = (r[0] * A1[0] + r[1] * A2[0], r[0] * A1[1] + r[1] * A2[1])
        row = []
        for s in range(6):
            q = reduce_mod(coarse(add(X, AC[s])), M)
            row.append(idx[q])
        nb.append(row)
    return R, up, nb


def valid_layers(T, nst, M, nb=None, cap=2_000_000):
    """all layer configurations mod M that satisfy the in-layer contacts (backtracking)."""
    if nb is None:
        _, _, nb = torus_struct(M)
    m = len(nb)
    out = []
    cur = [None] * m

    def rec(q):
        if len(out) > cap:
            return
        if q == m:
            out.append(tuple(cur))
            return
        mask = (1 << nst) - 1
        for s in range(6):
            p = nb[q][s]                       # p sits at q + AC[s], so q sits at p + AC[s+3]
            if p < q:
                mask &= T[(s + 3) % 6][cur[p]]
        for i in range(nst):
            if mask >> i & 1:
                if any(nb[q][s] == q and not (T[s][i] >> i & 1) for s in range(6)):
                    continue
                cur[q] = i
                rec(q + 1)
        cur[q] = None
    rec(0)
    # final full check (handles wrap-around neighbours placed later)
    res = []
    for A in out:
        if all(T[s][A[q]] >> A[nb[q][s]] & 1 for q in range(m) for s in range(6)):
            res.append(A)
    return res


def periodic_alive_l(T, C, nst, M, budget=4e7, want_delta=False):
    """layer graph on in-layer-valid configurations mod M; edges for lean 1/2 and any drift.  Returns
    (alive, edges, configs); None if the graph is too large for the budget."""
    R, up, nb = torus_struct(M)
    m = len(R)
    V = valid_layers(T, nst, M, nb)
    if len(V) * len(V) * 2 * max(1, len(C)) > budget:
        return None
    dl = {}
    Vid = {A: n for n, A in enumerate(V)}
    succ = {}
    for n, A in enumerate(V):
        for lean in (1, 2):
            tgt = set()
            for d, Cd in C.items():
                masks = []
                for q in range(m):
                    mk = (1 << nst) - 1
                    for (ln, s) in up[lean].get(q, []):
                        mk &= Cd[s][A[ln]]
                    masks.append(mk)
                if not all(masks):
                    continue
                size = 1
                for mk in masks:
                    size *= bin(mk).count('1')
                if size <= len(V):
                    for B in itertools.product(*[[i for i in range(nst) if mk >> i & 1] for mk in masks]):
                        if B in Vid:
                            tgt.add(Vid[B])
                            if want_delta:
                                dl.setdefault((n, lean, Vid[B]), d)
                else:
                    for B, b in Vid.items():
                        if all(masks[q] >> B[q] & 1 for q in range(m)):
                            tgt.add(b)
                            if want_delta:
                                dl.setdefault((n, lean, b), d)
            if tgt:
                succ[(n, lean)] = sorted(tgt)
    alive = set(range(len(V)))
    while True:
        new = {n for n in alive if any(b in alive for lean in (1, 2) for b in succ.get((n, lean), []))}
        if new == alive:
            break
        alive = new
    edges = [(n, lean, b) for (n, lean), bs in succ.items() if n in alive for b in bs if b in alive]
    if want_delta:
        return alive, edges, V, dl
    return alive, edges, V


def ch_words(edges, L):
    return ch_words_from_edges(edges, L)


def lean_battery(pieces, mirrors=False, patch=(4, 2), maxidx=3, words_len=4, cap_states=300000):
    """verdict in {'NO LAYER','NO PATCH','PERIODIC-k','CANDIDATE'}"""
    sts, _ = states_l(pieces, mirrors)
    n = len(sts)
    T = inlayer_table(sts)
    C = inter_table(sts)
    res = {'states': n, 'deltas': len(C)}
    if not C:
        res['verdict'] = 'NO PATCH'
        res['patch_words'] = []
        return res
    K, R = patch
    adm = []
    for w in itertools.product((1, 2), repeat=K - 1):
        if w[0] != 1:
            continue
        cells, con_k, il = lean_patch(w, R)
        if sat_lean(len(cells), n, con_k, il, T, C, K - 1)[0]:
            adm.append(''.join('c' if w[i] == w[i - 1] else 'h' for i in range(1, len(w))))
    res['patch_words'] = adm
    if not adm:
        res['verdict'] = 'NO PATCH'
        return res
    skipped = []
    for M in hnf(maxidx):
        r = periodic_alive_l(T, C, n, M)
        if r is None:
            skipped.append(M)
            continue
        alive, edges, V = r
        if alive:
            res['verdict'] = f'PERIODIC-{M[0]*M[2]}'
            res['M'] = M
            res['periodic_words'] = ch_words(edges, words_len)
            return res
    res['verdict'] = 'CANDIDATE' if not skipped else 'UNDECIDED'
    res['skipped'] = skipped
    return res
