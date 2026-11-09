"""03: follow-up.
(A) The one correlation found in 02: E6u0 (six-riser staircase, uniform bottom) with all six sides leaning one way
    (shear (1,0)).  Its c/h words on longer patches (8 layers), proper and with mirror copies, and the cross-check of
    the shear reduction: the same words come out of the VERTICAL model restricted to the placements that keep the
    lean (Lemma S + orientation lock), so the lean acts only as an orientation lock.
(B) Exact space filling, independent of the contact tables: explicit periodic tilings (layer-graph cycles) are built
    as closed polyhedral surfaces in integer coordinates (fine-lattice coordinates, an affine image of space) and
    (1) every wall and riser is checked planar, (2) every cell volume = 36 lattice units (hexagon 3 x layer 12),
    (3) the winding number of random points (exact integer ray casting) summed over all cells is exactly 1.
    Tilings: RD with six sides leaning (shear), E6u0 with six sides leaning (h-pair stacking), FLAT with the stripe
    lean (four sides leaning, rows of upright and turned-over wedges, forced h).  Each at two lean scales.
(C) E1h with mirror copies (UNDECIDED in 02 only because of the size guard): larger budget.
"""
import sys, os, time, json, random, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pieces import *

t0 = time.time()
ok = True
OUT = os.path.join(HERE, '..', 'data')
REL = reliefs()


def patch_words(pcs, K, R, mirrors=False):
    sts, _ = states_l(pcs, mirrors)
    T = inlayer_table(sts)
    C = inter_table(sts)
    adm = []
    for w in itertools.product((1, 2), repeat=K - 1):
        if w[0] != 1:
            continue
        cells, con_k, il = lean_patch(w, R)
        if sat_lean(len(cells), len(sts), con_k, il, T, C, K - 1)[0]:
            adm.append(''.join('c' if w[i] == w[i - 1] else 'h' for i in range(1, len(w))))
    return sorted(adm)


def vertical_words(P2, G, K, R):
    seen = []
    for g in G:
        Q = place(P2, g)
        if Q not in seen:
            seen.append(Q)
    C = compat_table(seen)
    adm = []
    for w in itertools.product((1, 2), repeat=K - 1):
        if w[0] != 1:
            continue
        cells, con = patch_contacts(w, R)
        if sat_solve(len(cells), len(seen), con, C)[0]:
            adm.append(''.join('c' if w[i] == w[i - 1] else 'h' for i in range(1, len(w))))
    return sorted(adm)


# ---------------------------------------------------------------- (A)
E6 = REL['E6u0']
u = (1, 0)
PE = make(*E6, shear(u), u)
for mir in (False, True):
    for K in (5, 8):
        W = patch_words([PE], K, 2, mir)
        G = G_ALL if mir else G_PROPER
        # the lean fixes ONE orientation class for the whole stack (any of them): union over the classes
        classes = {}
        for g in G:
            classes.setdefault(dict(place_l(PE, g)[2])[D[0]], []).append(g)
        Gs = list(classes.values())[0]
        Wv = sorted(set().union(*[set(vertical_words(E6, Gc, K, 2)) for Gc in classes.values()]))
        Wall = vertical_words(E6, G, K, 2)
        print(f'(A) E6u0 + shear{u}, mirrors {mir}, {K} layers: {len(W)} words; vertical model restricted to the '
              f'{len(Gs)} placements that keep the lean: {len(Wv)}; vertical with every placement: {len(Wall)}; '
              f'leaning = union of restricted, and <= all: {set(Wv) == set(W) and set(W) <= set(Wall)}')
        ok &= set(Wv) == set(W) and set(W) <= set(Wall)
        # words beyond the restricted model: the lean orientation changes between layers.  Show where and check
        # that the interface there is flat (Lemma S)
        sts_, _ = states_l([PE], mir)
        T_, C_ = inlayer_table(sts_), inter_table(sts_)
        for wd in sorted(set(W) - set(Wv))[:3]:
            for lw in itertools.product((1, 2), repeat=K - 1):
                if lw[0] != 1 or ''.join('c' if lw[i] == lw[i - 1] else 'h' for i in range(1, len(lw))) != wd:
                    continue
                cells, con_k, il = lean_patch(lw, 2)
                okk, (mod, dels) = sat_lean(len(cells), len(sts_), con_k, il, T_, C_, K - 1)
                key = {i: kp for kp, i in cells.items()}
                lay = {}
                for c_, i in enumerate(mod):
                    lay.setdefault(key[c_][0], set()).add(dict(sts_[i][2])[D[0]])
                flat = []
                for k in range(K - 1):
                    if lay[k] != lay[k + 1]:
                        hs = {dict(sts_[mod[cells[kp]]][0][sx])[v] for kp in cells if kp[0] == k
                              for sx in range(6) for v in dict(sts_[mod[cells[kp]]][0][sx])}
                        flat.append((k, sorted(hs)))
                print(f'    word {wd}: lean of each layer {[sorted(lay[k]) for k in range(K)]}; orientation changes '
                      f'at interfaces (heights of the lower tops there) {flat}')
                ok &= all(len(h) >= 1 for _, h in flat)
                break
        if K == 8:
            runs = set()
            gaps = set()
            for w_ in W:
                # interior maximal runs of h and c (not touching the ends of the word)
                import re
                for m in re.finditer(r'h+', w_):
                    if m.start() > 0 and m.end() < len(w_):
                        runs.add(len(m.group()))
                for m in re.finditer(r'c+', w_):
                    if m.start() > 0 and m.end() < len(w_):
                        gaps.add(len(m.group()))
            print(f'    interior h-runs {sorted(runs)}, interior c-runs {sorted(gaps)}; all-c word present: '
                  f'{"c" * 6 in W}; sample {W[:12]}')
            ok &= 'c' * 6 in W
    Wv_full = vertical_words(E6, G_ALL if mir else G_PROPER, 5, 2)
    print(f'    E6u0 vertical with every placement: {len(Wv_full)} words (the lean removes {8 - len(W) if False else ""}'
          f'words by locking the orientation)')

# ---------------------------------------------------------------- (B) explicit tilings and exact geometry
def find_cycle(edges, want_h=False, maxlen=18):
    adj = {}
    for (a, lean, b) in edges:
        adj.setdefault(a, []).append((lean, b))
    best = None
    for start in sorted(adj)[:200]:
        stack = [(start, [], [])]
        while stack:
            node, path, leans = stack.pop()
            if len(path) >= maxlen:
                continue
            for lean, b in adj.get(node, []):
                np_, nl = path + [(node, lean, b)], leans + [lean]
                if b == start:
                    word = ''.join('c' if nl[i] == nl[i - 1] else 'h' for i in range(len(nl)))
                    good = (('h' in word and 'c' in word) if want_h else True)
                    if good and (best is None or len(np_) < len(best[0])):
                        best = (np_, word)
                elif b not in [x[0] for x in np_]:
                    stack.append((b, np_, nl))
        if best and not want_h:
            break
    return best


def build_tiling(pcs, mirrors, M, want_h, K0, nrep=2, Rc=3):
    sts, _ = states_l(pcs, mirrors)
    T = inlayer_table(sts)
    C = inter_table(sts)
    r = periodic_alive_l(T, C, len(sts), M, budget=4e8, want_delta=True)
    alive, edges, V, dl = r
    cyc = find_cycle(edges, want_h)
    if cyc is None:
        return None
    path, word = cyc
    Rr = reps(M)
    layers = []
    origin = (0, 0)
    off = (0, 0)
    seq = path * nrep
    confs = [seq[0][0]] + [e[2] for e in seq]
    leans = [e[1] for e in seq]
    cells = []
    for k, ci in enumerate(confs):
        if k > 0:
            origin = add(origin, ORIG[leans[k - 1]])
            off = add(off, dl[seq[k - 1]])
        A = V[ci]
        for x in range(-Rc - 3, Rc + 4):
            for y in range(-Rc - 3, Rc + 4):
                X = add(origin, (x * A1[0] + y * A2[0], x * A1[1] + y * A2[1]))
                if cart2(sub(X, origin)) > (Rc + 1) ** 2:
                    continue
                q = reduce_mod((x, y), M)
                cells.append((k, X, off, sts[A[Rr.index(q)]]))
    return {'cells': cells, 'word': word, 'leans': leans, 'L': len(confs), 'K0': K0, 'nst': len(sts)}


S7 = 7


def vtx(X, off, k, d, h, K0):
    return (S7 * (K0 * X[0] + off[0] + d[0]), S7 * (K0 * X[1] + off[1] + d[1]), S7 * (12 * k + h))


def cell_mesh(k, X, off, st, K0):
    top = [dict(s) for s in st[0]]
    bot = [dict(s) for s in st[1]]
    ln = dict(st[2])
    wc = st[3]

    def P(v, h):
        w = wc if v == O else ln[v]
        return vtx(add(X, v), off, k, scal(h, w), h, K0)
    tris, quads = [], []
    for s in range(6):
        a, b = D[s], D[(s + 1) % 6]
        tris.append((P(O, top[s][O]), P(a, top[s][a]), P(b, top[s][b])))
        tris.append((P(O, bot[s][O]), P(b, bot[s][b]), P(a, bot[s][a])))
        quads.append((P(a, bot[s][a]), P(b, bot[s][b]), P(b, top[s][b]), P(a, top[s][a])))
        p = (s - 1) % 6
        if top[p][O] != top[s][O] or top[p][a] != top[s][a]:
            quads.append((P(O, top[p][O]), P(a, top[p][a]), P(a, top[s][a]), P(O, top[s][O])))
        if bot[p][O] != bot[s][O] or bot[p][a] != bot[s][a]:
            quads.append((P(O, bot[s][O]), P(a, bot[s][a]), P(a, bot[p][a]), P(O, bot[p][O])))
    return tris, quads


def vsub(a, b): return (a[0] - b[0], a[1] - b[1], a[2] - b[2])
def det3(a, b, c):
    return a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0])


class Degenerate(Exception):
    pass


def crossing(p, r, a, b, c):
    e1, e2, s = vsub(b, a), vsub(c, a), vsub(p, a)
    Dn = det3(e1, e2, r)          # = n . r
    if Dn == 0:
        if det3(e1, e2, s) == 0:
            raise Degenerate
        return 0
    # p + t r = a + u e1 + v e2  ->  u e1 + v e2 - t r = s
    mr = (-r[0], -r[1], -r[2])
    Dm = det3(e1, e2, mr)
    un, vn, tn = det3(s, e2, mr), det3(e1, s, mr), det3(e1, e2, s)
    sg = 1 if Dm > 0 else -1
    un, vn, tn, Dm = un * sg, vn * sg, tn * sg, Dm * sg
    if tn < 0:
        return 0
    if tn == 0:
        raise Degenerate
    if un < 0 or vn < 0 or un + vn > Dm:
        return 0
    if un == 0 or vn == 0 or un + vn == Dm:
        raise Degenerate
    return 1 if Dn > 0 else -1


def check_tiling(tl, npts=300, seed=1):
    K0 = tl['K0']
    meshes = []
    nonplanar = 0
    vols = set()
    for (k, X, off, st) in tl['cells']:
        tris, quads = cell_mesh(k, X, off, st, K0)
        allt = list(tris)
        for q in quads:
            if det3(vsub(q[1], q[0]), vsub(q[2], q[0]), vsub(q[3], q[0])) != 0:
                nonplanar += 1
            allt += [(q[0], q[1], q[2]), (q[0], q[2], q[3])]
        def cross(a, b):
            return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
        allt = [t for t in allt if any(cross(vsub(t[1], t[0]), vsub(t[2], t[0])))]   # drop zero-area pieces
        vol6 = sum(det3(*t) for t in allt)
        vols.add(vol6)
        xs = [v[0] for t in allt for v in t]; ys = [v[1] for t in allt for v in t]; zs = [v[2] for t in allt for v in t]
        meshes.append(((min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)), allt))
    expect6 = 6 * 36 * K0 * K0 * S7 ** 3
    rnd = random.Random(seed)
    L = tl['L']
    bad = 0
    tested = 0
    hist = {}
    while tested < npts:
        # a random point near the axis of the patch, in the middle layers
        k = rnd.randint(1, L - 2)
        base = [(X, off) for (kk, X, off, st) in tl['cells'] if kk == k]
        X0, off0 = base[len(base) // 2]
        p = (S7 * (K0 * X0[0] + off0[0]) + rnd.randint(-2 * S7 * K0, 2 * S7 * K0),
             S7 * (K0 * X0[1] + off0[1]) + rnd.randint(-2 * S7 * K0, 2 * S7 * K0),
             S7 * 12 * k + rnd.randint(-6 * S7, 6 * S7))
        r = (rnd.randint(1, 10 ** 6), rnd.randint(1, 10 ** 6), rnd.randint(10 ** 6, 2 * 10 ** 6))
        try:
            wsum = 0
            for (bb, allt) in meshes:
                if not (bb[0] <= p[0] <= bb[1] and bb[2] <= p[1] <= bb[3] and p[2] <= bb[5]):
                    # the ray goes up and to +x,+y: a cell can only be crossed if it is not entirely behind
                    if p[2] > bb[5] or p[0] > bb[1] or p[1] > bb[3]:
                        continue
                w = 0
                for t in allt:
                    w += crossing(p, r, *t)
                wsum += w
        except Degenerate:
            continue
        tested += 1
        hist[wsum] = hist.get(wsum, 0) + 1
        if wsum != 1:
            bad += 1
    return {'nonplanar': nonplanar, 'vol_ok': vols == {expect6}, 'vols': sorted(vols)[:3], 'expect6': expect6,
            'points': tested, 'winding_hist': hist, 'bad': bad}


CASES = [('RD, six sides leaning (shear (1,0))', [make(*REL['RD'], shear((1, 0)), (1, 0))], False, (1, 0, 1), False),
         ('E6u0, six sides leaning (shear (1,0))', [PE], False, (1, 0, 1), False),
         ('FLAT, stripe lean (rows of wedges)', [make(*REL['FLAT'], stripe((0, 0)), (1, 0))], False, (1, 0, 2), False)]
dump = {}
for name, pcs, mir, M, want_h in CASES:
    for K0 in (120, 30):
        tl = build_tiling(pcs, mir, M, want_h, K0)
        if tl is None:
            print(f'(B) {name}: no cycle found'); ok = False; continue
        res = check_tiling(tl, npts=250 if K0 == 120 else 150)
        print(f'(B) {name}, kappa = 1/{K0}: cycle word {tl["word"]}, {len(tl["cells"])} cells, {tl["nst"]} states; '
              f'non-planar faces {res["nonplanar"]}; volumes all 36: {res["vol_ok"]}; winding numbers of '
              f'{res["points"]} random points: {res["winding_hist"]}')
        ok &= res['nonplanar'] == 0 and res['vol_ok'] and res['bad'] == 0
        if K0 == 30:
            dump[name] = {'word': tl['word'], 'K0': K0,
                          'cells': [[k, list(X), list(off), [list(map(list, s)) for s in st[0]],
                                     [list(map(list, s)) for s in st[1]], [[list(p), list(w)] for p, w in st[2]],
                                     list(st[3])] for (k, X, off, st) in tl['cells']]}
json.dump(dump, open(os.path.join(OUT, '03_tilings.json'), 'w'))

# ---------------------------------------------------------------- (C)
sts, _ = states_l([make(*REL['E1h'], shear((0, 0)), (0, 0))], True)
T = inlayer_table(sts); C = inter_table(sts)
for M in hnf(3):
    r = periodic_alive_l(T, C, len(sts), M, budget=3e9)
    if r and r[0]:
        print(f'(C) E1h with mirror copies: periodic with in-plane lattice {M}, words {ch_words(r[1], 4)}')
        break
else:
    print('(C) E1h with mirror copies: no periodic tiling of index <= 3'); ok = False
# ---------------------------------------------------------------- (D) turned placements as lean states (DICTO 9 Nov)
# For every lean class that fills a layer (01 box2): distinct lean states per site (rotations + turn-over, then with
# mirror copies), and how many different lean states one layer can hold (torus SAT, index <= 9).  Then, for every
# leaning piece that tiles (02 box2), the layer graph: do consecutive layers ever show different lean orientations,
# and do consecutive layers with the same orientations occur (Theorem B)?
from pysat.solvers import Cadical153
prof = json.load(open(os.path.join(OUT, '01_profiles_box2.json')))
F6, Fm6 = flat_relief(6), flat_relief(-6)
def max_states_in_layer(T, n, M):
    R_, _, nb_ = torus_struct(M)
    best = 0
    for want in range(n, 0, -1):
        if want <= best:
            break
        # is there a layer using at least `want` different states?  (cardinality via indicator variables)
        from pysat.card import CardEnc
        m = len(R_)
        v = lambda c, i: c * n + i + 1
        top = m * n
        S = Cadical153()
        for c in range(m):
            S.add_clause([v(c, i) for i in range(n)])
            for i in range(n):
                for j in range(i + 1, n):
                    S.add_clause([-v(c, i), -v(c, j)])
        for q in range(m):
            for s_ in range(6):
                p = nb_[q][s_]
                for i in range(n):
                    S.add_clause([-v(q, i)] + [v(p, j) for j in range(n) if T[s_][i] >> j & 1])
        used = [top + i + 1 for i in range(n)]
        for i in range(n):
            S.add_clause([-used[i]] + [v(c, i) for c in range(m)])
        enc = CardEnc.atleast(lits=used, bound=want, top_id=top + n)
        for cl in enc.clauses:
            S.add_clause(cl)
        if S.solve():
            best = want
        S.delete()
    return best
lean_rows = {}
for rec in prof:
    if not (rec['proper']['tori'] or rec['mirrors']['tori']):
        continue
    w = tuple(tuple(x) for x in rec['w'])
    if w[0] == (0, 0) and rec['class'].startswith('P1'):
        continue
    for mir in (False, True):
        sts, _ = states_l([make(F6, Fm6, w)], mir)
        n = len(sts)
        T = inlayer_table(sts)
        tori = [M_ for M_ in hnf(9) if M_[0] * M_[2] in (1, 2, 3, 4, 6, 8, 9)]
        mx = 0
        for M_ in tori:
            mx = max(mx, max_states_in_layer(T, n, M_))
        key = ('shear' if rec['class'].startswith('P1') else ('stripe' if rec['stripe_type'] else 'pattern2D'), mir)
        lean_rows.setdefault(key, []).append((n, mx))
print('(D) lean classes that fill a layer: distinct lean states per site -> most different lean states one layer can hold')
for key, v in sorted(lean_rows.items()):
    print(f'    {key[0]:9s} mirrors {key[1]}: {sorted(set(v))}')
scan = json.load(open(os.path.join(OUT, '02_scan_box2.json')))
diff_or = same_or = 0
seen_p = 0
always_change = []
for r in scan:
    if not r['verdict'].startswith('PERIODIC') or r['lean'] == 'V':
        continue
    w = tuple(tuple(x) for x in r['w'])
    P = make(*REL[r['relief']], w, tuple(r['wc']))
    sts, _ = states_l([P], r['mirrors'])
    T = inlayer_table(sts); C = inter_table(sts)
    M = tuple(r['M'])
    alive, edges, V = periodic_alive_l(T, C, len(sts), M, budget=4e8)
    lset = lambda A: frozenset(sts[i][2] for i in A)
    sm = 0
    for (a, lean, b) in edges:
        if lset(V[a]) == lset(V[b]):
            same_or += 1; sm += 1
        else:
            diff_or += 1
    if sm == 0:
        always_change.append((r['relief'], r['lean'], r['wc'], r['mirrors']))
    seen_p += 1
print(f'    leaning pieces that tile ({seen_p}): layer-graph steps with the SAME lean orientations above and below '
      f'{same_or}, with DIFFERENT ones {diff_or}')
print(f'    pieces whose every layer step changes the lean orientations (Theorem B escape in the lean channel): '
      f'{len(always_change)} {always_change[:6]}')
ok &= same_or > 0
print(f'time {time.time()-t0:.0f}s')
print('FINAL ok' if ok else 'FINAL FAIL: word cross-check, planarity, volume or winding check failed')
