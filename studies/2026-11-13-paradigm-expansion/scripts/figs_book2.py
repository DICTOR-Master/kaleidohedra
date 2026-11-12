# Second half of figs_book.py (executed inside it): Chapters 8 to 15 and the Epilogue.

# ---------- Chapter 8: Centre I
U4 = np.array([0.0, 0.29, 0.53, 0.80, 1.0]) + np.array([0, 0.013, -0.021, 0.008, 0.0])   # generic, increasing
@fig('kelvin-swept')
def f_kswept():
    Pl = perms((1, 2, 3, 4)); P = np.array(Pl, float) - 2.5; E = perm_edges(Pl); B = basis_sum0(4); P3 = P @ B.T
    u = np.array([0.0, 0.31, 0.57, 1.0]); u3 = u @ B.T; idx = sweep_index(P, u, [(i, j) for i, j, k in E])
    cnt = [int((idx == i).sum()) for i in range(4)]
    check(f'Kelvin swept: corners with 0, 1, 2, 3 edges below = {cnt}', cnt == [1, 11, 11, 1])
    # orient the view so the height u3 points up the page
    up = u3 / np.linalg.norm(u3); a = np.cross(up, [0.3, 0.2, 0.9]); a /= np.linalg.norm(a); bb = np.cross(up, a)
    R0 = np.array([a, up, bb]); R = rot(0, 12) @ R0 if False else R0
    R = np.array([a * math.cos(0.35) + bb * math.sin(0.35), up, -a * math.sin(0.35) + bb * math.cos(0.35)])
    h = P @ u; F = hull_faces(P3); ts = np.quantile(h, [0.12, 0.33, 0.5, 0.67, 0.88])
    fig_, axs = plt.subplots(1, 5, figsize=(13, 4.2))
    cols = {0: '#555555', 1: GOLD_D, 2: RED, 3: VIOLET}
    for ax, t in zip(axs, ts):
        blank(ax); sc = Scene(R)
        sc.solid(P3, F, color='#dfe7f0', glass=True, alpha=0.22, lw=0.7, edge='#7d8fa3')
        cut = []
        for i, j, k in E:
            x, y = h[i] - t, h[j] - t
            if x * y < 0: cut.append(P3[i] + (P3[j] - P3[i]) * x / (x - y))
        cut = np.array(cut); cc = cut.mean(0)
        o = sorted(range(len(cut)), key=lambda k: math.atan2((cut[k] - cc) @ a, (cut[k] - cc) @ bb))
        sc.poly(cut[o], color='#f4c9bf', edge=RED, lw=1.6, alpha=0.85, z=1)
        for i in range(24):
            if h[i] < t: sc.dot(P3[i], color=cols[idx[i]], s=22, z=2)
        sc.draw(ax); ax.set_xlim(-3, 3); ax.set_ylim(-3.2, 3.2)
        below = [int(((idx == i) & (h < t)).sum()) for i in range(4)]
        ax.set_title(f'{len(cut)}-gon; passed: ' + ' · '.join(str(b) for b in below), fontsize=8.5)
    fig_.text(0.5, 0.07, 'corners passed, by edges below: 0 (grey) · 1 (gold) · 2 (red) · 3 (violet); in all 1, 11, 11, 1', ha='center', fontsize=9)
    mark(fig_); fig_.subplots_adjust(0.01, 0.1, 0.99, 0.92); save(fig_, 'kelvin-swept.png')

def facets5():
    """the 30 cells of the 4D permutohedron of 1..5 (centred): subset S of positions with sum_S x <= top |S| values sum."""
    out = []
    vals = [2, 1, 0, -1, -2]
    for k in range(1, 5):
        for S in itertools.combinations(range(5), k):
            n = np.zeros(5); n[list(S)] = 1; out.append((S, n, float(sum(vals[:k]))))
    return out
@fig('film-strip')
def f_film():
    Pl, P, E = perm4d(); u = U4 - U4.mean(); h = P @ u
    idx = sweep_index(P, u, [(i, j) for i, j, k in E]); cnt = [int((idx == i).sum()) for i in range(5)]
    check(f'4D permutohedron swept: corners with 0..4 edges below {cnt}', cnt == [1, 26, 66, 26, 1])
    FAC = facets5(); Bp = basis_perp(5, [u])
    # cells at a corner v: T_j = positions of the values > j+1 ... edge e_k (swap values k, k+1) lies in every cell at v but T_k
    def cells_at(i):
        p = Pl[i]; out = {}
        for k in range(1, 5):   # T_k: positions holding values k+1..5
            S = tuple(sorted(q for q in range(5) if p[q] > k)); out[k] = S
        return out
    swaps = []
    for i in range(len(P)):
        if idx[i] != 2: continue
        p = Pl[i]; T = cells_at(i); down = []
        for k in range(1, 5):
            q = tuple(k + 1 if x == k else k if x == k + 1 else x for x in p); j = Pl.index(q)
            if h[j] < h[i]: down.append(k)
        up = [k for k in range(1, 5) if k not in down]
        swaps.append((h[i], [T[k] for k in up], [T[k] for k in down]))
    swaps.sort()
    hs = np.sort(h); ts = np.linspace(hs[0] + 0.08 * (hs[-1] - hs[0]), hs[-1] - 0.08 * (hs[-1] - hs[0]), 9)
    R = rot(25, 18)
    def section(t):
        pts = []
        for i, j, k in E:
            x, y = h[i] - t, h[j] - t
            if x * y < 0: pts.append(P[i] + (P[j] - P[i]) * x / (x - y))
        pts = np.array(pts); X = pts @ Bp.T; return pts, X, hull_faces(X)
    def label(pts, f):
        for S, nn, rhs in FAC:
            if np.all(np.abs(pts[f] @ nn - rhs) < 1e-7): return S
    # gold: the cell of four values (|S| = 1 or 4) with the largest front face in the middle frame
    pts, X, F = section(ts[4]); best = None
    for f, n in F:
        S = label(pts, f); n = np.asarray(n) / np.linalg.norm(n)
        if len(S) in (1, 4) and (R[2] @ n) > 0:
            a = ConvexHull(X[f] @ np.linalg.svd(X[f] - X[f].mean(0))[2][:2].T).volume
            if best is None or a > best[0]: best = (a, S)
    gold = best[1]
    fig_, axs = plt.subplots(1, 9, figsize=(16, 3.6))
    for ax, t in zip(axs, ts):
        blank(ax); pts, X, F = section(t)
        sv = min(swaps, key=lambda s: abs(s[0] - t)); red = sv[1] if t < sv[0] else sv[2]
        cols = []
        for f, n in F:
            lab = label(pts, f)
            cols.append(GOLD if lab == gold else (RED if lab in red else '#e3ecf5'))
        sc = Scene(R); sc.solid(X, F, facecolors=cols, lw=0.6); sc.draw(ax)
        ax.set_xlim(-3.1, 3.1); ax.set_ylim(-3.1, 3.1)
        nb = [int(((idx == i) & (h < t)).sum()) for i in (1, 2, 3)]
        ax.set_title(f'{len(F)} cells\nborn {nb[0]} · swaps {nb[1]} · died {nb[2]}', fontsize=7.5)
    fig_.text(0.5, 0.05, 'gold: one cell (a permutohedron of four values); red: the pair at the nearest swap (still touching before it, just met after it); pale: the other cells', ha='center', fontsize=8.5)
    mark(fig_); fig_.subplots_adjust(0.005, 0.12, 0.995, 0.86); save(fig_, 'film-strip-4d.png')
@fig('eulerian-bars')
def f_ebars():
    fig_, ax = plt.subplots(figsize=(7.5, 3.6)); v = [1, 26, 66, 26, 1]
    lab = ['first corner\n(4 cells)', 'births', 'swaps', 'deaths', 'last corner\n(4 cells)']; col = ['#bbbbbb', GOLD, RED, VIOLET, '#bbbbbb']
    ax.bar(range(5), v, color=col, edgecolor=INK, lw=0.8)
    for k in range(5): ax.text(k, v[k] + 1.5, str(v[k]), ha='center', fontsize=11, weight='bold')
    ax.set_xticks(range(5)); ax.set_xticklabels([f'{i} edges below\n{l}' for i, l in enumerate(lab)], fontsize=8)
    ax.set_ylim(0, 76); ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False); ax.set_ylabel('corners')
    a = [[1]]
    for n in range(2, 6):
        a.append([(k + 1) * (a[-1][k] if k < len(a[-1]) else 0) + (n - k) * (a[-1][k - 1] if k >= 1 else 0) for k in range(n)])
    check(f'Eulerian numbers for five values {a[-1]}', a[-1] == v)
    mark(fig_); fig_.subplots_adjust(0.1, 0.22, 0.98, 0.97); save(fig_, 'eulerian-bars.png')

# ---------- Chapter 9: Centre II (the bitruncated 600-cell)
def h4_roots():
    a = np.array; c5 = math.cos(math.pi / 5)
    # simple roots of H4 (chain 5-3-3): angles 4π/5? use the standard choice with Gram matrix of the diagram
    G = np.array([[1, -c5, 0, 0], [-c5, 1, -0.5, 0], [0, -0.5, 1, -0.5], [0, 0, -0.5, 1]])
    L = np.linalg.cholesky(G); return L   # rows: simple roots with the right Gram matrix
def orbit(x, roots, nmax=20000):
    key = lambda v: tuple(np.round(v, 7)); seen = {key(x): x}; fr = [x]
    while fr:
        nf = []
        for v in fr:
            for r in roots:
                w = v - 2 * (v @ r) * r; k = key(w)
                if k not in seen: seen[k] = w; nf.append(w)
        fr = nf
        if len(seen) > nmax: raise RuntimeError('orbit too large')
    return np.array(list(seen.values()))
@fig('bt600-balance')
def f_bt():
    Rt = h4_roots(); W = np.linalg.inv(Rt).T   # rows: fundamental weights (dual to the simple roots)
    seed = W[1] + W[2]; V = orbit(seed, Rt)
    check(f'bitruncated 600-cell: {len(V)} corners (3600)', len(V) == 3600)
    nW = orbit(W[0] / np.linalg.norm(W[0]), Rt); nR = orbit(W[3] / np.linalg.norm(W[3]), Rt)
    check(f'cell normals: {len(nW)} truncated tetrahedra (600), {len(nR)} truncated icosahedra (120)', len(nW) == 600 and len(nR) == 120)
    N = np.vstack([nW, nR]); typ = np.array(['W'] * len(nW) + ['R'] * len(nR))
    S = V @ N.T; mx = S.max(0); onf = np.abs(S - mx) < 1e-6
    D = np.linalg.norm(V[:, None, :] - V[None, :, :], axis=2) if False else None
    # edges: nearest neighbours
    from scipy.spatial import cKDTree
    tr = cKDTree(V); d, j = tr.query(V, k=5); el = d[:, 1].min()
    nb = [[int(q) for q, dd in zip(j[i, 1:], d[i, 1:]) if abs(dd - el) < 1e-6] for i in range(len(V))]
    check('every corner has 4 edges and lies in 4 cells (2 W + 2 R)', all(len(x) == 4 for x in nb) and all(onf[i].sum() == 4 and (typ[onf[i]] == 'W').sum() == 2 for i in range(len(V))))
    rng = np.random.default_rng(7); u = np.array([0.13, 0.31, 0.47, 0.82]) + rng.normal(0, 0.01, 4); u /= np.linalg.norm(u)
    h = V @ u; ev = []
    for i in range(len(V)):
        cells = np.where(onf[i])[0]
        down = [q for q in nb[i] if h[q] < h[i]]
        if len(down) != 2: continue
        # the cell not containing edge (i, q) is the one of the four whose hyperplane does not hold q
        miss = {q: [c for c in cells if abs(V[q] @ N[c] - mx[c]) > 1e-6][0] for q in nb[i]}
        below = sorted(typ[miss[q]] for q in nb[i] if q not in down); above = sorted(typ[miss[q]] for q in down)
        ev.append((h[i], ''.join(below), ''.join(above)))
    ev.sort(); n_ = len(ev)
    ww = [e[0] for e in ev if e[1] == 'WW' and e[2] == 'RR']; rr = [e[0] for e in ev if e[1] == 'RR' and e[2] == 'WW']; mix = n_ - len(ww) - len(rr)
    check(f'generic sweep: {n_} swaps (2166): W–W → R–R {len(ww)}, R–R → W–W {len(rr)} (601 each), mixed {mix} (964)', n_ == 2166 and len(ww) == 601 and len(rr) == 601 and mix == 964)
    fig_, ax = plt.subplots(figsize=(9.5, 4.4)); lo, hi = h.min(), h.max(); X = lambda v: (np.array(v) - lo) / (hi - lo)
    ax.step(X(ww), np.arange(1, len(ww) + 1), where='post', color=RED, lw=2, label='W–W contact lost, R–R made')
    ax.step(X(rr), np.arange(1, len(rr) + 1), where='post', color=VIOLET, lw=2, label='R–R contact lost, W–W made')
    mixh = [e[0] for e in ev if not ((e[1] == 'WW' and e[2] == 'RR') or (e[1] == 'RR' and e[2] == 'WW'))]
    ax.step(X(mixh), np.arange(1, len(mixh) + 1), where='post', color='#9a9a9a', lw=1.2, label='W–R for W–R (mixed)')
    ax.axhline(601, color='#c9b37a', lw=0.8, ls='--'); ax.text(0.02, 615, '601 each way', color=GOLD_D, fontsize=9)
    ax.set_xlabel('height of the sweep (from the lowest corner to the highest)'); ax.set_ylabel('swaps so far'); ax.legend(frameon=False, fontsize=8.5, loc='upper left', bbox_to_anchor=(0.0, 0.93))
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False); ax.set_xlim(0, 1)
    mark(fig_); fig_.subplots_adjust(0.09, 0.14, 0.98, 0.97); save(fig_, 'bt600-balance.png')
@fig('h-vectors')
def f_hv():
    fig_, (a1, a2) = plt.subplots(1, 2, figsize=(11, 3.9), gridspec_kw=dict(width_ratios=[1.6, 1]))
    rows = [('120-cell', (1, 116, 366, 116, 1)), ('truncated 120-cell', (1, 716, 966, 716, 1)), ('bitruncated 600-cell', (1, 716, 2166, 716, 1)), ('4D permutohedron', (1, 26, 66, 26, 1))]
    fv = {'120-cell': (600, 120), 'truncated 120-cell': (2400, 720), 'bitruncated 600-cell': (3600, 720), '4D permutohedron': (120, 30)}
    for k, (nm, hv) in enumerate(rows):
        f0, f3 = fv[nm]; h1 = f3 - 4; h2 = f0 - 2 - 2 * h1
        check(f'{nm}: h from f by Dehn–Sommerville: h1 = f3 − 4 = {h1}, h2 = f0 − 2 − 2h1 = {h2}', (1, h1, h2, h1, 1) == hv)
        a1.bar(np.arange(5) + (k - 1.5) * 0.2, hv, width=0.2, color=[GREY, GOLD, RED, VIOLET][k] if False else ['#7f9cc4', '#d9b24a', RED, '#5aa07a'][k], edgecolor=INK, lw=0.5, label=nm)
    a1.set_yscale('log'); a1.set_xticks(range(5)); a1.set_xticklabels(['h₀', 'h₁ births', 'h₂ swaps', 'h₃ deaths', 'h₄'], fontsize=8.5); a1.legend(frameon=False, fontsize=8)
    a1.spines['top'].set_visible(False); a1.spines['right'].set_visible(False); a1.set_title('h-vectors: every simple 4-polytope swept', fontsize=10)
    mids = [('5-cell', 6, 10, 5), ('tesseract', 17, 32, 16), ('24-cell', 73, 96, 24), ('600-cell', 601, 720, 120)]
    for nm, b, E, Vv in mids: check(f'chain middle of the {nm}: E − V + 1 = {E - Vv + 1}', E - Vv + 1 == b)
    a2.bar(range(4), [m[1] for m in mids], color=RED, edgecolor=INK, lw=0.6); a2.set_yscale('log')
    for k, m in enumerate(mids): a2.text(k, m[1] * 1.15, str(m[1]), ha='center', fontsize=10, weight='bold')
    a2.set_xticks(range(4)); a2.set_xticklabels([m[0] for m in mids], fontsize=8.5); a2.set_ylim(1, 2500)
    a2.set_title('balanced swaps each way at the chain middles\n= E − V + 1 of the regular polytope', fontsize=9.5)
    a2.spines['top'].set_visible(False); a2.spines['right'].set_visible(False)
    mark(fig_); fig_.subplots_adjust(0.06, 0.14, 0.99, 0.88, wspace=0.25); save(fig_, 'h-vectors.png')

# ---------- Chapter 10: rosettes
CHAINS = {'A4': [3, 3, 3], 'B4': [4, 3, 3], 'F4': [3, 4, 3], 'H4': [5, 3, 3], 'A3': [3, 3]}
def cox_order(nodes, labels):
    """order of the parabolic subgroup on a set of nodes of a chain with bond labels (labels[i] joins i, i+1)."""
    nodes = sorted(nodes); comps = []; cur = []
    for v in nodes:
        if cur and v == cur[-1] + 1: cur.append(v)
        else:
            if cur: comps.append(cur)
            cur = [v]
    if cur: comps.append(cur)
    tot = 1
    for c in comps:
        n = len(c); labs = [labels[c[i]] for i in range(n - 1)]
        if n == 1: o = 2
        elif all(l == 3 for l in labs): o = math.factorial(n + 1)
        elif n == 2: o = 2 * labs[0]
        elif sorted(labs) == [3, 4] and n == 3: o = 48
        elif sorted(labs) == [3, 5] and n == 3: o = 120
        elif labs == [4, 3, 3] or labs == [3, 3, 4]: o = 384
        elif labs == [3, 4, 3]: o = 1152
        elif labs == [5, 3, 3] or labs == [3, 3, 5]: o = 14400
        else: raise ValueError(labs)
        tot *= o
    return tot
def edges_at_corner(chain, seed):
    labels = CHAINS[chain]; n = len(labels) + 1; S = [i for i in range(n) if seed[i]]; U = [i for i in range(n) if not seed[i]]
    e = 0
    for i in S:
        Ui = [j for j in U if abs(j - i) != 1]
        e += cox_order(U, labels) // cox_order(Ui, labels) if U else 1
    return e
def draw_diagram(ax, x, y, labels, seed, w=0.9, col=INK, fs=6):
    n = len(seed); xs = [x + (k - (n - 1) / 2) * w / (n - 1) * 1.0 for k in range(n)]
    for k in range(n - 1):
        ax.plot([xs[k], xs[k + 1]], [y, y], color=col, lw=0.8, zorder=2)
        if labels[k] != 3: ax.text((xs[k] + xs[k + 1]) / 2, y + 0.07, str(labels[k]), ha='center', fontsize=fs, color=col)
    for k in range(n):
        ax.scatter([xs[k]], [y], s=12, color='white', edgecolors=col, linewidths=0.8, zorder=3)
        if seed[k]: ax.scatter([xs[k]], [y], s=42, facecolors='none', edgecolors=col, linewidths=0.8, zorder=3)
@fig('coxeter-grid')
def f_cgrid():
    fig_, ax = plt.subplots(figsize=(13, 5.0)); blank(ax)
    seeds = [s for s in itertools.product((0, 1), repeat=4) if any(s)]
    seeds.sort(key=lambda s: (sum(s), s))
    tot = {'clean': 0, 'rosette': 0}
    for r, ch in enumerate(['A4', 'B4', 'F4', 'H4']):
        y = -r * 1.1; ax.text(-0.9, y, ch + '\n' + '–'.join(map(str, CHAINS[ch])), ha='right', va='center', fontsize=10, weight='bold')
        for c, s in enumerate(seeds):
            e = edges_at_corner(ch, s); clean = e == 4; tot['clean' if clean else 'rosette'] += 1
            x = c * 1.05
            ax.add_patch(Rectangle((x - 0.48, y - 0.42), 0.96, 0.84, fc='#f6e3a8' if clean else '#e4d7f4', ec=GOLD_D if clean else VIOLET, lw=0.8))
            draw_diagram(ax, x, y + 0.08, CHAINS[ch], s, w=0.72)
            ax.text(x, y - 0.27, f'{e} edges' if not clean else 'clean', ha='center', fontsize=6.6, color=GOLD_D if clean else '#4b2f78')
    check(f'Theorem (edges at a corner): the 600-cell e = {edges_at_corner("H4", (0, 0, 0, 1))} (12), the 120-cell {edges_at_corner("H4", (1, 0, 0, 0))} (4), (0,1,0,0) in B4 {edges_at_corner("B4", (0, 1, 0, 0))} (6), truncated 600-cell {edges_at_corner("H4", (0, 0, 1, 1))} (6), 24-cell {edges_at_corner("F4", (1, 0, 0, 0))} (8), the permutohedron {edges_at_corner("A4", (1, 1, 1, 1))} (4)',
          [edges_at_corner('H4', (0, 0, 0, 1)), edges_at_corner('H4', (1, 0, 0, 0)), edges_at_corner('B4', (0, 1, 0, 0)), edges_at_corner('H4', (0, 0, 1, 1)), edges_at_corner('F4', (1, 0, 0, 0)), edges_at_corner('A4', (1, 1, 1, 1))] == [12, 4, 6, 6, 8, 4])
    check(f'seeds drawn: {tot}', tot['clean'] + tot['rosette'] == 60)
    ax.text(7.5, 0.75, 'gold: clean tissue (four edges at every corner, one move at a time)    violet: rosette (edges at a corner)', ha='center', fontsize=9)
    ax.set_xlim(-1.9, 15.3); ax.set_ylim(-3.85, 1.0)
    mark(fig_); fig_.subplots_adjust(0.0, 0.06, 1.0, 1.0); save(fig_, 'coxeter-grid.png')
@fig('clean-crowded')
def f_cc():
    fig_, axs = plt.subplots(1, 2, figsize=(10, 4.6)); R = rot(30, 22)
    Pl = perms((1, 2, 3, 4)); P3 = (np.array(Pl, float) - 2.5) @ basis_sum0(4).T
    O = np.array([v for v in itertools.permutations((1.6, 0, 0))] + [v for v in itertools.permutations((-1.6, 0, 0))]); O = np.unique(np.round(O, 9), axis=0)
    for ax, X, lab, seed, e in ((axs[0], P3, "Kelvin's cell: 3 edges at a corner (clean)", (1, 1, 1), 3), (axs[1], O * 1.3, 'octahedron: 4 edges at a corner (rosette)', (0, 1, 0), 4)):
        blank(ax); F = hull_faces(X); sc = Scene(R); sc.solid(X, F, color='#e8edf3', lw=0.8)
        top = max(range(len(X)), key=lambda i: R[1] @ X[i] + 0.3 * (R[2] @ X[i]))
        d = np.linalg.norm(X - X[top], axis=1); el = np.sort(d)[1]
        nbr = [i for i in range(len(X)) if abs(d[i] - el) < 1e-6]
        for i in nbr: sc.line(X[top], X[i], color=RED, lw=2.8, z=1)
        sc.dot(X[top], color=RED, s=30, z=2); sc.draw(ax); ax.set_xlim(-3.2, 3.2); ax.set_ylim(-3.4, 3.0)
        ax.set_title(lab, fontsize=10); draw_diagram(ax, 0, -3.0, [3, 3], seed, w=1.4, fs=8)
        check(f'{lab}: {len(nbr)} edges at the corner; Theorem gives {edges_at_corner("A3", seed)}', len(nbr) == e == edges_at_corner('A3', seed))
    mark(fig_); fig_.subplots_adjust(0.01, 0.06, 0.99, 0.92); save(fig_, 'clean-crowded.png')
def sweep16(V, u):
    """events of a sweep of a polytope with the face lattice of the 16-cell: cells are the 16 sign-choice tetrahedra (pairs i, i+4 opposite)."""
    h = V @ u; ev = []
    for i in range(8):
        cells = [c for c in itertools.product((0, 1), repeat=4) if c[i % 4] == i // 4]
        idxs = lambda c: [k + 4 * c[k] for k in range(4)]
        nb = [j for j in range(8) if j % 4 != i % 4]
        down = [j for j in nb if h[j] < h[i]]
        born = sum(1 for c in cells if all(h[j] > h[i] for j in idxs(c) if j != i)); die = sum(1 for c in cells if all(h[j] < h[i] for j in idxs(c) if j != i))
        ev.append((h[i], len(down), born, die))
    return sorted(ev)
@fig('rosette-ledger')
def f_rled():
    Vm = np.array([(10, 2, -1, 0), (1, 8, -2, 0), (0, -2, 10, 2), (-1, -2, 1, 9), (-10, 1, 0, 1), (1, -10, 1, -1), (-1, 2, -9, -2), (-2, -1, 1, -8)], float)
    # order: corners i and i+4 are opposite (the 16-cell's pairs ±e_i): (10,2,-1,0)/(-10,1,0,1), (1,8,-2,0)/(1,-10,1,-1), (0,-2,10,2)/(-1,2,-9,-2), (-1,-2,1,9)/(-2,-1,1,-8)
    um = np.array([-3, 0, 0, 1.0]); evm = sweep16(Vm, um)
    Vr = np.vstack([np.eye(4), -np.eye(4)]) * 10; ur = np.array([0.91, 0.37, 0.19, 0.07]); evr = sweep16(Vr, ur)
    b4m = sum(1 for e in evm if e[2] == 4); d4m = sum(1 for e in evm if e[3] == 4); b4r = sum(1 for e in evr if e[2] == 4); d4r = sum(1 for e in evr if e[3] == 4)
    check(f'moved 16-cell, height −3x1 + x4: heights {[round(e[0]) for e in evm]}; corners where 4 cells are born {b4m}, where 4 die {d4m} (2 and 1: unbalanced)', b4m == 2 and d4m == 1)
    check(f'regular 16-cell, generic height: 4 born at {b4r}, 4 die at {d4r} (balanced)', b4r == d4r)
    fig_, ax = plt.subplots(figsize=(11, 3.8)); ax.axis('off')
    for row, (ev, lab) in enumerate(((evr, 'regular 16-cell, a generic sweep: balanced'), (evm, 'moved 16-cell (same face lattice), height −3x₁ + x₄: unbalanced'))):
        y = -row * 1.3; hs = np.array([e[0] for e in ev]); X = (hs - hs.min()) / (hs.max() - hs.min()) * 10
        ax.plot([0, 10], [y, y], color=INK, lw=1); ax.text(-0.2, y + 0.42, lab, fontsize=9.5, ha='left')
        for x, (hh, nd, born, die) in zip(X, ev):
            txt = (f'+{born}' if born else '') + (f' −{die}' if die else '')
            col = RED if born == 4 else (VIOLET if die == 4 else '#666')
            ax.scatter([x], [y], s=40 if col != '#666' else 18, color=col, zorder=3)
            ax.text(x, y - 0.28, txt.strip() or '·', ha='center', va='top', fontsize=8.5, color=col)
    ax.text(5, -2.35, 'each dot a corner, left to right by height; +k: k cells born there, −k: k cells die there. Red: four born at once; violet: four die at once', ha='center', fontsize=8.5, color='#444')
    ax.set_xlim(-0.4, 10.4); ax.set_ylim(-2.6, 0.7)
    mark(fig_); fig_.subplots_adjust(0.01, 0.06, 0.99, 0.98); save(fig_, 'rosette-ledger.png')

# ---------- Chapter 11
@fig('stacking-word')
def f_word():
    word = 'ABCACB'; n = len(word)
    typ = ['c' if word[(k - 1) % n] != word[(k + 1) % n] else 'h' for k in range(n)]
    fig_, ax = plt.subplots(figsize=(9.5, 5.4)); blank(ax)
    off = {'A': 0.0, 'B': 1 / 3, 'C': 2 / 3}; colL = {'A': GOLD, 'B': BLUE, 'C': TEAL}
    for k, L in enumerate(word):
        y = k * 0.8
        ax.add_patch(MPoly([[0, y], [5, y], [6.2, y + 0.45], [1.2, y + 0.45]], closed=True, fc=colL[L], ec=INK, lw=0.8, alpha=0.55 if typ[k] == 'c' else 0.85))
        for i in range(5):
            for j in range(2):
                x = 0.5 + i + 0.6 * (j + off[L]) ; yy = y + 0.1 + 0.25 * (j + off[L]) * 0.9
                ax.scatter([x], [yy], s=22, color=INK, zorder=3)
        ax.text(-0.3, y + 0.22, L, fontsize=14, weight='bold', ha='right', va='center')
        ax.text(6.5, y + 0.22, typ[k], fontsize=14, weight='bold', color=RED if typ[k] == 'h' else INK, va='center')
        ax.text(7.0, y + 0.22, f'between {word[(k - 1) % n]} and {word[(k + 1) % n]}' + (' : alike, a mirror' if typ[k] == 'h' else ' : different'), fontsize=8.5, va='center', color='#444')
    ax.set_xlim(-0.8, 10.6); ax.set_ylim(-0.4, n * 0.8 + 0.3)
    check(f'stacking word {word} (repeated): layer types {"".join(typ)}', ''.join(typ) == 'hcchcc')
    mark(fig_); fig_.subplots_adjust(0.01, 0.06, 0.99, 0.99); save(fig_, 'stacking-word.png')

# ---------- Chapter 12
@fig('growth')
def f_growth():
    ns = list(range(3, 10))
    ridges = [6, 36, 150, 540, 1806, 5796, 18150]; N = [3, 15, 65, 225, 770, 2443, 7761]
    def eul(n):
        a = [1]
        for m in range(2, n + 1): a = [(k + 1) * (a[k] if k < len(a) else 0) + (m - k) * (a[k - 1] if k >= 1 else 0) for k in range(m)]
        return a
    A2 = [eul(n)[2] for n in ns]
    r2 = [math.factorial(n) * sum(1 for c in itertools.product(range(1, n), repeat=2) if c[0] + c[1] < n) // 2 for n in ns]
    # ridges = ordered splits into three blocks: sum n!/(a! b! c!) over a, b, c >= 1
    rr = [sum(math.factorial(n) // (math.factorial(a) * math.factorial(b) * math.factorial(n - a - b)) for a in range(1, n) for b in range(1, n - a)) for n in ns]
    def T(n): return 2 ** (n - 1) - 1 if n % 2 else 2 ** (n - 2) - 1
    NN = [sum(math.factorial(n) // (math.factorial(a) * math.factorial(b) * math.factorial(c)) for a in range(1, n) for c in range(a + 1, n) for b in [n - a - c] if b >= 1) + T(n) for n in ns]
    check(f'ridges {rr} match the table', rr == ridges); check(f'Vacuus count N(n) {NN} matches Theorem (3, 15, 65, …, 7761)', NN == N)
    check(f'corners with two edges below A(n, 2) = {A2}', A2 == [1, 11, 66, 302, 1191, 4293, 14608])
    fig_, ax = plt.subplots(figsize=(8.5, 4.4))
    ax.semilogy(ns, ridges, 'o-', color='#7f9cc4', lw=2, label='ridges (2-faces in 4D)'); ax.semilogy(ns, N, 's-', color=GOLD_D, lw=2, label='Vacuus slices N(n)')
    ax.semilogy(ns, A2, 'D-', color=RED, lw=2, label='corners with two edges below (the swaps in 4D)')
    for n, v in zip(ns, N): ax.text(n, v / 1.7, str(v), ha='center', fontsize=7.5, color=GOLD_D)
    for n, v in zip(ns, A2): ax.text(n + 0.12, v * 1.5, str(v), ha='left', fontsize=7.5, color=RED)
    ax.set_xlabel('number of values n (dimension n − 1)'); ax.legend(frameon=False, fontsize=8.5); ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    mark(fig_); fig_.subplots_adjust(0.09, 0.14, 0.98, 0.97); save(fig_, 'growth.png')

# ---------- Chapter 13: the golden slice
UG = np.array([1, PHI, PHI ** 2, PHI ** 3, PHI ** 4])
def heights_golden():
    P = np.array(perms((-2, -1, 0, 1, 2)), float); hs = P @ UG
    # exact: phi^i = F(i-1) + F(i) phi; height = a + b phi with integers
    F = [0, 1]
    for _ in range(8): F.append(F[-1] + F[-2])
    Fm = lambda i: F[i - 1] if i >= 1 else 1   # F_{-1} = 1
    ex = []
    for p in perms((-2, -1, 0, 1, 2)):
        a = sum(p[i] * (Fm(i) if i else 1) for i in range(5)); b = sum(p[i] * (F[i] if i else 0) for i in range(5))
        ex.append((a, b))
    return P, hs, ex
@fig('golden-heights')
def f_gh():
    P, hs, ex = heights_golden(); ok = all(abs(a + b * PHI - h) < 1e-9 for (a, b), h in zip(ex, hs))
    from collections import Counter
    C = Counter(ex); d = len(C)
    check(f'golden heights: exact a + bφ agree with floats {ok}; {d} distinct heights (70), {120 - d} coincidences (50)', ok and d == 70)
    fig_, ax = plt.subplots(figsize=(11.5, 3.6)); ax.axis('off')
    keys = sorted(C, key=lambda k: k[0] + k[1] * PHI); lo = min(k[0] + k[1] * PHI for k in keys); hi = max(k[0] + k[1] * PHI for k in keys)
    X = lambda k: (k[0] + k[1] * PHI - lo) / (hi - lo) * 10
    ax.plot([0, 10], [0, 0], color=INK, lw=0.8)
    for k in keys:
        m = C[k]
        for j in range(m): ax.scatter([X(k)], [0.12 + j * 0.16], s=14, color=RED if m > 1 else '#777', zorder=3)
        if m > 1: ax.plot([X(k), X(k)], [0.12, 0.12 + (m - 1) * 0.16], color=RED, lw=1.2)
    mult = Counter(C.values())
    ax.text(5, -0.35, f'the 120 corners of the permutohedron of −2, …, 2 at their golden heights u · x, u = (1, φ, φ², φ³, φ⁴): {d} distinct heights; ' + ', '.join(f'{v} heights carry {k} corners' for k, v in sorted(mult.items())), ha='center', fontsize=8.5)
    ax.text(5, -0.62, 'red: corners at one height (linked); they meet because φ² = φ + 1', ha='center', fontsize=8.5, color=RED)
    ax.set_xlim(-0.3, 10.3); ax.set_ylim(-0.8, 1.0)
    mark(fig_); fig_.subplots_adjust(0.01, 0.08, 0.99, 0.98); save(fig_, 'golden-heights.png')
def decode_An_star(X):
    """nearest point of A4* = projection of Z^5 onto sum 0, scaled so that its Voronoi cell is the permutohedron of −2..2 (factor 5)."""
    # Voronoi cell of pi(Z^5) is (1/5) * permutohedron of (0..4) centred = (1/5) Perm(−2..2); so the lattice L = 5 pi(Z^5)
    Y = X / 5.0; best = None; bd = None
    for k in range(5):
        g = np.zeros(5); g[:k] = 1; g = g - g.mean()            # glue vector, a coset of A4 in A4*
        Z = Y - g; R = np.round(Z); s = R.sum(1)
        # fix the sum to 0 (A4 = integer vectors with sum 0): move the coordinates with the largest rounding error
        err = Z - R
        for i in range(len(Z)):
            si = int(s[i])
            if si > 0:
                o = np.argsort(err[i])[:si]; R[i, o] -= 1
            elif si < 0:
                o = np.argsort(-err[i])[:-si]; R[i, o] += 1
        Lp = R + g; dd = ((Y - Lp) ** 2).sum(1)
        if best is None: best, bd = Lp.copy(), dd
        else:
            m = dd < bd; best[m] = Lp[m]; bd[m] = dd[m]
    return best * 5.0
def golden_plane(u, c, w, ext=9.0, res=900):
    Bp = basis_perp(5, [u]); a, b = Bp[0], Bp[1]
    x0 = u / (u @ u) * c
    s = np.linspace(-ext, ext, res); S, T = np.meshgrid(s, s * 0.62)
    X = x0 + S.reshape(-1, 1) * a + T.reshape(-1, 1) * b
    Lp = decode_An_star(X)
    return X, Lp, S, T
@fig('golden-patch')
def f_gp():
    P, hs, ex = heights_golden(); lev = np.unique(np.round(hs, 9))
    fig_, axs = plt.subplots(1, 2, figsize=(13, 4.6))
    for ax, (u, lab) in zip(axs, ((np.array([1.0, -1.0, 0, 0, 0]) + np.array([0, 0, 0.0, 0.0, 0.0]), 'a rational cut, u = (1, −1, 0, 0, 0): one kind, repeating'), (UG - UG.mean(), 'the golden cut, u = (1, φ, φ², φ³, φ⁴): they never repeat across'))):
        uu = u - u.mean(); c = 0.4123
        X, Lp, S, T = golden_plane(uu, c, None, ext=11, res=1100)
        off = c - Lp @ uu          # the height of the section inside the cell of λ
        levs = np.unique(np.round(np.array(perms((-2, -1, 0, 1, 2)), float) @ uu, 9))
        band = np.searchsorted(levs, off) - 1; kind = np.minimum(band, len(levs) - 2 - band)
        img = kind.reshape(S.shape).astype(float)
        cmap = plt.get_cmap('tab20b' if 'golden' in lab else 'Set3')
        ax.imshow(img, origin='lower', extent=[S.min(), S.max(), T.min(), T.max()], cmap=cmap, interpolation='nearest')
        key = (Lp * 1000).round().astype(np.int64); kk = key @ np.array([1, 7919, 104729, 1299709, 15485863], dtype=np.int64)
        K = kk.reshape(S.shape); edge = np.zeros(S.shape, bool); edge[:, 1:] |= K[:, 1:] != K[:, :-1]; edge[1:, :] |= K[1:, :] != K[:-1, :]
        ov = np.zeros(S.shape + (4,)); ov[edge] = (0.1, 0.1, 0.1, 1)
        ax.imshow(ov, origin='lower', extent=[S.min(), S.max(), T.min(), T.max()], interpolation='nearest')
        nk = len(np.unique(kind))
        ax.set_title(lab + f'\n{nk} kinds in this window', fontsize=9); ax.axis('off')
        if 'golden' in lab: check(f'golden plane section: {nk} kinds of section seen in the window (at most 35), {len(levs)} heights (70)', nk <= 35 and len(levs) == 70)
        else: check(f'rational plane section: {nk} kinds seen (few), {len(levs)} heights', nk <= 4)
    fig_.text(0.5, 0.04, 'a flat plane inside the three-dimensional slice of the 4D permutohedron filling; each region is one cell of the slice, coloured by the kind of its section', ha='center', fontsize=8.5)
    mark(fig_); fig_.subplots_adjust(0.01, 0.08, 0.99, 0.9); save(fig_, 'golden-patch.png')

# ---------- Chapter 14: the family
def gp_member(z):
    """generalized permutohedron in R^4 (sum = z[0123]) from heights z[S] (frozenset), in 3D coordinates of the sum hyperplane."""
    B = basis_sum0(4); tot = z[frozenset(range(4))]; c = np.ones(4) * tot / 4
    A = []; b = []
    for S, v in z.items():
        if len(S) in (1, 2, 3):
            n = np.zeros(4); n[list(S)] = 1
            A.append(-(n @ B.T)); b.append(-(v - n @ c))
    return halfspace_vertices(np.array(A), np.array(b)), A, b
SUBS = [frozenset(S) for k in (1, 2, 3, 4) for S in itertools.combinations(range(4), k)]
def interval(S): S = sorted(S); return S == list(range(S[0], S[-1] + 1))
def zPi(S): return len(S) * (len(S) + 1) / 2
def zL(S):
    S = sorted(S); return sum(1 for a in range(4) for b in range(a, 4) if all(x in S for x in range(a, b + 1)))
@fig('road')
def f_road():
    fig_, axs = plt.subplots(1, 4, figsize=(13, 4.0)); R = rot(30, 22); B = basis_sum0(4)
    for ax, t in zip(axs, (0.0, 0.5, 0.9, 1.0)):
        blank(ax); z = {S: (1 - t) * zPi(S) + t * zL(S) for S in SUBS}
        V, A, b = gp_member(z); F = hull_faces(V)
        cols = []
        for f, n in F:
            m = V[f].mean(0); lab = None
            for S in SUBS[:-1]:
                nn = np.zeros(4); nn[list(S)] = 1
                if all(abs(((V[q] @ B) + 2.5) @ nn - z[S]) < 1e-6 for q in f): lab = S; break
            cols.append(GOLD if lab is not None and interval(lab) else VIOLET)
        sc = Scene(R); sc.solid(V, F, facecolors=cols, lw=0.9); sc.draw(ax); ax.set_xlim(-3.2, 3.2); ax.set_ylim(-3.2, 3.2)
        nv = len(V); nf = len(F); ax.set_title(f't = {t:g}: {nv} corners, {nf} faces', fontsize=9.5)
        if t < 1: check(f'road t = {t}: the permutohedron\'s face lattice kept: 24 corners, 14 faces', nv == 24 and nf == 14)
        else: check(f'road t = 1: Loday\'s associahedron: 14 corners, 9 faces', nv == 14 and nf == 9)
    fig_.text(0.5, 0.05, "gold: the 9 interval walls, which stay; violet: the 5 other walls, sliding out until they vanish together at t = 1", ha='center', fontsize=9)
    mark(fig_); fig_.subplots_adjust(0.01, 0.1, 0.99, 0.92); save(fig_, 'road.png')
def zonotope(gens):
    pts = np.unique(np.round(np.array([sum(c * g for c, g in zip(cs, gens)) for cs in itertools.product([0, 1], repeat=len(gens))]), 9), axis=0)
    return pts[sorted(set(ConvexHull(pts).vertices))]
GRAPHS = [('a tree (path)', [(0, 1), (1, 2), (2, 3)], 'parallelepiped (cube)'), ('4-cycle', [(0, 1), (1, 2), (2, 3), (3, 0)], 'rhombic dodecahedron'),
          ('triangle + pendant', [(0, 1), (1, 2), (2, 0), (2, 3)], 'hexagonal prism'), ('K₄ minus an edge', [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)], 'elongated dodecahedron'),
          ('K₄', [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2), (1, 3)], 'truncated octahedron')]
@fig('fedorov')
def f_fed():
    fig_ = plt.figure(figsize=(13, 5.0)); R = rot(28, 20); B = basis_sum0(4)
    want = [(8, 6), (14, 12), (12, 8), (18, 12), (24, 14)]
    for k, (gn, E, sol) in enumerate(GRAPHS):
        ax = fig_.add_axes([0.01 + k * 0.197, 0.33, 0.19, 0.6]); blank(ax)
        gens = []
        for i, j in E: v = np.zeros(4); v[i] = 1; v[j] = -1; gens.append(v @ B.T)
        Z = zonotope(gens); Z = Z - Z.mean(0); F = hull_faces(Z)
        check(f'Fedorov {sol}: graphical zonotope of the {gn}: {len(Z)} corners, {len(F)} faces', (len(Z), len(F)) == want[k])
        sc = Scene(R); sc.solid(Z, F, facecolors=[[GOLD, BLUE, TEAL, VIOLET][min(len(f) // 2 - 2, 3)] if len(f) != 6 else BLUE for f, n in F], lw=0.9)
        sc.draw(ax); m = np.abs(Z).max() * 1.2; ax.set_xlim(-m, m); ax.set_ylim(-m, m); ax.set_title(sol, fontsize=9.5)
        ag = fig_.add_axes([0.06 + k * 0.197, 0.06, 0.09, 0.22]); blank(ag)
        pos = np.array([[0, 1], [1, 1], [1, 0], [0, 0]], float)
        for i, j in E: ag.plot(*zip(pos[i], pos[j]), color=RED, lw=2)
        ag.scatter(pos[:, 0], pos[:, 1], s=30, color=INK, zorder=3); ag.set_xlim(-0.3, 1.3); ag.set_ylim(-0.3, 1.3); ag.set_title(gn, fontsize=8.5)
    mark(fig_); save(fig_, 'fedorov.png')
@fig('coa13')
def f_coa():
    C = [np.array(p, float) for p in set(itertools.permutations((1, 1, 0))) | set(itertools.permutations((1, -1, 0))) | set(itertools.permutations((-1, -1, 0)))]
    X = np.unique(np.round(np.array(C + [np.array([2.0, 0, 0])]), 9), axis=0); F = hull_faces(X)
    kinds = {}
    for f, n in F:
        if len(f) == 3: k = 'triangle'
        else:
            e = [np.linalg.norm(X[f[i]] - X[f[(i + 1) % 4]]) for i in range(4)]; d1 = np.linalg.norm(X[f[0]] - X[f[2]]); d2 = np.linalg.norm(X[f[1]] - X[f[3]])
            k = 'square' if abs(d1 - d2) < 1e-9 else 'rhombus'
        kinds[k] = kinds.get(k, 0) + 1
    nE = sum(len(f) for f, n in F) // 2; L = {round(np.linalg.norm(X[f[i]] - X[f[(i + 1) % len(f)]]), 9) for f, n in F for i in range(len(f))}
    check(f'13-COA: {len(X)} corners, {nE} edges, faces {kinds}, edge lengths {L}', len(X) == 13 and nE == 24 and kinds == {'triangle': 4, 'square': 5, 'rhombus': 4} and len(L) == 1)
    fig_, axs = plt.subplots(1, 3, figsize=(13, 4.8))
    colk = {'triangle': GOLD, 'square': '#5fa35f', 'rhombus': BLUE}
    def kind(f): return 'triangle' if len(f) == 3 else ('square' if abs(np.linalg.norm(X[f[0]] - X[f[2]]) - np.linalg.norm(X[f[1]] - X[f[3]])) < 1e-9 else 'rhombus')
    for ax, (az, el) in zip(axs[:2], ((20, 18), (200, 25))):
        blank(ax); sc = Scene(rot(az, el)); sc.solid(X, F, facecolors=[colk[kind(f)] for f, n in F], lw=1.0); sc.draw(ax); ax.set_xlim(-2.4, 2.4); ax.set_ylim(-2.4, 2.4)
    axs[0].set_title('pyramid side: 4 rhombi of 60° (blue)', fontsize=9.5); axs[1].set_title('far side: triangles (gold), squares (green)', fontsize=9.5)
    # the Vacuus: a fin from the corner centroid to every edge; coplanar fins share a colour
    c = X.mean(0); E = set()
    for f, n in F:
        for i in range(len(f)): E.add(tuple(sorted((f[i], f[(i + 1) % len(f)]))))
    fins = [(a, b, np.cross(X[a] - c, X[b] - c)) for a, b in E]
    groups = []
    for a, b, n in fins:
        n = n / np.linalg.norm(n); d = n @ c
        for g in groups:
            if abs(abs(g[0] @ n) - 1) < 1e-9: g[1].append((a, b)); break
        else: groups.append([n, [(a, b)]])
    multi = [g for g in groups if len(g[1]) > 1]
    check(f'13-COA Vacuus: 24 fins in {len(groups)} planes, {len(multi)} planes with two fins (22 planes, 2 pairs)', len(groups) == 22 and len(multi) == 2)
    ax = axs[2]; blank(ax); sc = Scene(rot(20, 18)); sc.solid(X, F, color='#e6eef6', glass=True, alpha=0.16, lw=0.6, edge='#7d8fa3')
    pal = [RED, VIOLET]; mi = 0
    for n, es in groups:
        if len(es) > 1: col = pal[mi % 2]; mi += 1
        else: col = '#b9b9b9'
        for a, b in es: sc.poly([c, X[a], X[b]], color=col, edge=INK, lw=0.5, alpha=0.75 if len(es) > 1 else 0.35, z=1, shade_it=False)
    sc.draw(ax); ax.set_xlim(-2.4, 2.4); ax.set_ylim(-2.4, 2.4); ax.set_title('its Vacuus: 24 fins; the two coplanar pairs in colour', fontsize=9.5)
    mark(fig_); fig_.subplots_adjust(0.01, 0.06, 0.99, 0.92); save(fig_, 'coa13.png')
@fig('one-cone')
def f_cone():
    B = basis_sum0(4); R = rot(28, 20)
    items = []
    for vals, lab in (((1, 2, 3, 4), "Kelvin's cell"), ((1, 2, 4, 5), 'DICTO 1:2'), ((-PHI ** 3, -1, 1, PHI ** 3), 'Icosaxes (golden)'), ((-5, -1, 1, 5), 'DICTO 2:1')):
        P = np.array(perms(vals), float); P = (P - P.mean(0)) @ B.T; items.append((np.unique(np.round(P, 7), axis=0), lab, 'values moved'))
    for vals, lab in (((0, 0, 1, 1), 'octahedron = values 0, 0, 1, 1'), ((0, 1, 1, 1), 'tetrahedron = values 0, 1, 1, 1'), ((0, 0, 1, 2), 'truncated tetrahedron = 0, 0, 1, 2')):
        P = np.array(perms(vals), float); P = (P - P.mean(0)) @ B.T; items.append((np.unique(np.round(P, 7), axis=0), lab, 'repeated values'))
    gens = []
    for i, j in [(0, 1), (1, 2), (2, 3), (3, 0)]: v = np.zeros(4); v[i] = 1; v[j] = -1; gens.append(v @ B.T)
    Z = zonotope(gens); items.append((Z - Z.mean(0), 'rhombic dodecahedron (Fedorov)', 'walls moved'))
    z = {S: zL(S) for S in SUBS}; V, _, _ = gp_member(z); items.append((V, "Loday's associahedron", 'walls moved'))
    fig_, axs = plt.subplots(1, len(items), figsize=(15, 3.6))
    for ax, (X, lab, how) in zip(axs, items):
        blank(ax); F = hull_faces(X); sc = Scene(R)
        sc.solid(X, F, color={'values moved': GOLD, 'repeated values': TEAL, 'walls moved': VIOLET}[how], lw=0.8); sc.draw(ax)
        m = np.abs(X).max() * 1.2; ax.set_xlim(-m, m); ax.set_ylim(-m, m); ax.set_title(lab, fontsize=7.6); ax.text(0, -m * 0.98, how, ha='center', fontsize=7, color='#555')
        # every edge parallel to a root e_i − e_j (a swap direction)
        Rts = [((np.eye(4)[i] - np.eye(4)[j]) @ B.T) / 2 ** .5 for i in range(4) for j in range(i + 1, 4)]
        ok = all(any(abs(abs((X[f[k]] - X[f[(k + 1) % len(f)]]) / np.linalg.norm(X[f[k]] - X[f[(k + 1) % len(f)]]) @ r) - 1) < 1e-6 for r in Rts) for f, n in F for k in range(len(f)))
        check(f'one cone: {lab}: every edge parallel to a swap direction', ok)
    mark(fig_); fig_.subplots_adjust(0.0, 0.08, 1.0, 0.88); save(fig_, 'one-cone.png')

# ---------- Chapter 15: Grandsire Doubles on the 4D permutohedron
def ring(pn_list, n=5, start=None):
    row = list(start or range(1, n + 1)); rows = [tuple(row)]
    for pn in pn_list:
        keep = set(int(ch) for ch in pn if ch.isdigit()) if pn != 'x' else set()
        i = 1; new = row[:]
        while i <= n:
            if i in keep: i += 1; continue
            if i + 1 <= n and (i + 1) not in keep: new[i - 1], new[i] = row[i], row[i - 1]; i += 2
            else: i += 1
        row = new; rows.append(tuple(row))
    return rows
@fig('grandsire')
def f_gr():
    plain = ['3', '1', '5', '1', '5', '1', '5', '1', '5', '1']; bob = plain[:8] + ['3', '1']; single = plain[:8] + ['3', '123']
    found = None
    for word in ('BPBPSP' * 2, 'PBPBPS' * 2):
        seq = []
        for c in word: seq += {'P': plain, 'B': bob, 'S': single}[c]
        rows = ring(seq)
        if len(set(rows[:-1])) == 120 and rows[-1] == rows[0]: found = (word, rows); break
    check(f'Grandsire Doubles: calling {found[0] if found else None} rings 120 distinct rows and comes round', found is not None)
    word, rows = found
    Pl = perms((1, 2, 3, 4, 5)); P = np.array(Pl, float); E = perm_edges(Pl)
    def pt(r):
        place = {b: i + 1 for i, b in enumerate(r)}; return tuple(place[b] for b in range(1, 6))
    th = 2 * np.pi * np.arange(5) / 5; Q = np.c_[P @ np.cos(th), P @ np.sin(th)]
    key = {p: i for i, p in enumerate(Pl)}
    fig_, ax = plt.subplots(figsize=(8.4, 8.4)); blank(ax)
    for i, j, k in E: ax.plot(*zip(Q[i], Q[j]), color='#c9c9c9', lw=0.5, zorder=1)
    ne = nd = 0
    for a, b in zip(rows[:-1], rows[1:]):
        i, j = key[pt(a)], key[pt(b)]; sw = sum(x != y for x, y in zip(a, b)) // 2
        ne += sw == 1; nd += sw == 2
        ax.plot(*zip(Q[i], Q[j]), color=RED, lw=1.6 if sw == 1 else 1.0, ls='-' if sw == 1 else (0, (3, 2)), zorder=2)
    ax.scatter(Q[:, 0], Q[:, 1], s=8, color=INK, zorder=3)
    r0 = key[pt((1, 2, 3, 4, 5))]; rb = key[pt((5, 4, 3, 2, 1))]
    for i, lab in ((r0, 'rounds 12345'), (rb, 'backrounds 54321')):
        ax.scatter(*Q[i], s=60, color=GOLD, edgecolors=INK, zorder=4); ax.text(Q[i, 0], Q[i, 1] + 0.35, lab, ha='center', fontsize=9, weight='bold')
    check(f'Grandsire extent: {ne} single swaps (edges) + {nd} double swaps (square diagonals), as in Table: 2 + 118', ne == 2 and nd == 118)
    ax.set_title(f'Grandsire Doubles, {" ".join(word[:6])} twice: 120 rows on the 4D permutohedron\nsolid red: one swap (an edge); dashed red: two swaps at once (across a square)', fontsize=9.5)
    mark(fig_); fig_.subplots_adjust(0.01, 0.04, 0.99, 0.93); save(fig_, 'grandsire.png')
