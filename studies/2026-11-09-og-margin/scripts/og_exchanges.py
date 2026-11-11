# og_exchanges.py, DICTO 11 Nov 2026 ("nothing from exchange of communication of scutoids helps?").
# The #104 sweep of one OG hop (og_sweep.py) as a SCUTOID TISSUE: going down in lam the 3D slice T_lam = {y : X_j.y <= |X_j|^2 + lam}
# changes only at the vertices of the 4D polyhedron P = {(y, lam) : X_j.y - lam <= |X_j|^2, 0 <= lam <= LAM}.
# Generic vertex (4 facets): its 4 edges split up/down as 3/1 = a face DIES (triangle shrinks to a point; its 3 neighbours lose a side)
# or 2/2 = an EXCHANGE (2-2 edge flip: the two faces of the vanishing edge lose a side, the other two gain one). 1/3 = birth (impossible).
# Symmetric clusters are resolved by an infinitesimal (symbolic) random perturbation eps_j of the offsets |X_j|^2: every degenerate
# 4D vertex (event with > 4 facets) and every degenerate slice vertex (> 3 faces, e.g. on an axis) is resolved LOCALLY by the
# arrangement {A_r z <= eps_r, r tight} (scale-free, so exact; consistent with the global perturbed polyhedron as its size -> 0).
# Two seeds of eps: is s perturbation-independent?
# and also measured WITHOUT perturbation from the slices between distinct event levels (net side changes; s_min = net gains / 2).
# DICTO addition ("shape of cells how many walls"): each candidate's facet of P is a 3D CELL; walls = distinct neighbours over the
# sweep + caps (top; bottom if active); corners = 4D vertices on it; edges by Euler; kind PRISM / TRUNCATED PRISM (walls lost only to
# dying neighbours) / SCUTOID (an exchange changes its walls) / PYRAMID (cut, ends in a point), per orbit class.
# Records per level: candidates n, cut c, active a, exchanges s (generic count, both seeds) and s_min (unperturbed lower bound),
# sides of every face at the top and at death, sides lost by dying faces via exchanges vs via neighbour deaths, flips in clusters.
# Controls: cut set from the sweep = hull cut set (og_sweep); tracked side counts = slice side counts at the bottom and at mid levels;
# every dying face is a triangle at death (generic); sum of sides = 2E and Euler V - E + F = 2 in every slice; no 1/3 vertices;
# LAM above every event; generic tight sets have exactly 4 facets with a clear gap to the 5th.
# usage: python -u og_exchanges.py <five-fold-octet dir> <kmin> <kmax> <out.json>
import sys, os, json, time
import numpy as np
from scipy.spatial import ConvexHull, cKDTree, HalfspaceIntersection
from scipy.sparse import csr_matrix
OUT = os.path.abspath(sys.argv[4])
sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1])
src = open('exact_upward.py').read(); exec(src.split("def kinds(S)")[0])   # OG (exact), G (60 exact rotations)
KMIN, KMAX = int(sys.argv[2]), int(sys.argv[3])
OGf = np.array([[x.f() for x in v] for v in OG]); Gf = np.array([[[x.f() for x in row] for row in M] for M in G])
SEEDS = [1, 2]; TOL = 1e-9

def faces(V, tol=1e-9):                                                     # as og_sweep.py
    h = ConvexHull(V); E = h.equations; n = len(E); par = np.arange(n)
    def find(i):
        while par[i] != i: par[i] = par[par[i]]; i = par[i]
        return i
    for f in range(n):
        for g in h.neighbors[f]:
            if g > f and np.abs(E[f] - E[g]).max() < tol: par[find(f)] = find(g)
    roots = np.array([find(i) for i in range(n)]); u, inv = np.unique(roots, return_inverse=True)
    M = np.zeros((len(u), 3)); Dd = np.zeros(len(u)); cnt = np.bincount(inv)
    np.add.at(M, inv, E[:, :3]); np.add.at(Dd, inv, -E[:, 3]); M /= np.linalg.norm(M, axis=1)[:, None]; Dd /= cnt
    return M, Dd, np.unique(h.vertices)

def symmetrise(W):
    X = np.vstack([W @ g.T for g in Gf]); X = X[np.lexsort(X.T[::-1])]
    t = cKDTree(X); groups = {}
    for i, js in enumerate(t.query_ball_point(X, 1e-8)):
        groups.setdefault(min(js), []).append(i)
    return np.array([X[g].mean(0) for g in groups.values()])

def dedupe(P, tol):
    t = cKDTree(P); seen = -np.ones(len(P), int); out = []
    for i in range(len(P)):
        if seen[i] < 0:
            js = t.query_ball_point(P[i], tol); seen[js] = len(out); out.append(P[js].mean(0))
    return np.array(out)

def slice_sides(X, b, lam, tol=1e-9):
    """3D slice {X_j.y <= b_j + lam}: sides of every face (0 = not a face), V, E, F, sum sides."""
    H = np.hstack([X, -(b + lam)[:, None]])
    hs = HalfspaceIntersection(H, np.zeros(3))
    P = dedupe(hs.intersections, 1e-10)
    R = X @ P.T - (b + lam)[:, None]                                         # n x V residuals (<= 0)
    inc = np.abs(R) < tol
    sides = inc.sum(1)
    sides[sides < 3] = 0
    Ic = csr_matrix(inc.astype(np.int32)); S = (Ic @ Ic.T).toarray(); np.fill_diagonal(S, 0)
    E = int((S >= 2).sum() // 2); F = int((sides > 0).sum()); V = len(P)
    return sides, V, E, F

def vertices4(X, b, LAM):
    n = len(X)
    H = np.vstack([np.hstack([X, -np.ones((n, 1)), -b[:, None]]),
                   [[0, 0, 0, -1, 0], [0, 0, 0, 1, -LAM]]])
    hs = HalfspaceIntersection(H, np.array([0, 0, 0, LAM / 2]))
    return dedupe(hs.intersections, 1e-11)

def events(X, b, LAM, tight_tol):
    """Interior vertices of P: (lam, point, tight facets sorted by residual, 5th residual gap)."""
    P = vertices4(X, b, LAM)
    P = P[(P[:, 3] > 1e-12) & (P[:, 3] < LAM * (1 - 1e-9))]
    R = np.abs(X @ P[:, :3].T - P[:, 3][None, :] - b[:, None])             # n x V
    out = []
    for v in range(len(P)):
        r = R[:, v]; T = np.where(r < tight_tol)[0]
        rest = np.sort(r[r >= tight_tol])
        out.append((P[v, 3], P[v], T, rest[0] if len(rest) else np.inf))
    return out

def classify4(X, T, xi=None):
    """Generic vertex with tight facets T (4): up-edges; returns ('death', i, nbrs) or ('flip', losers, gainers) or ('bad', ...).
    A horizontal edge (d_lam = 0, coplanar normals on a mirror) gets its sign from the second-order tilt of the normals (xi)."""
    T = np.asarray(T); A = np.hstack([X[T], -np.ones((4, 1))]); C = np.linalg.inv(A)
    dC = None if xi is None else -C @ np.hstack([xi[T], np.zeros((4, 1))]) @ C
    up = []
    for p in range(4):
        dl = -C[3, p]
        if abs(dl) < 1e-9 * np.abs(C).max() and dC is not None: dl = -dC[3, p]
        if dl > 0: up.append(p)
    if len(up) == 3:
        dn = [p for p in range(4) if p not in up][0]
        return ('death', T[dn], [T[p] for p in up])
    if len(up) == 2:
        return ('flip', [T[p] for p in range(4) if p not in up], [T[p] for p in up])
    return ('bad', len(up), list(T))

def choose_LAM(X, b):
    LAM = 4.0 * b.max()
    for _ in range(12):
        ev = events(X, b, LAM, 1e-9)
        top = max([e[0] for e in ev], default=0)
        if top < LAM / 4: return LAM, top
        LAM *= 4
    raise RuntimeError('LAM search failed')


def slice_inc(X, b, lam, tol=TOL):
    """Unperturbed slice: vertices and their incident face sets."""
    H = np.hstack([X, -(b + lam)[:, None]])
    P = dedupe(HalfspaceIntersection(H, np.zeros(3)).intersections, 1e-10)
    R = np.abs(X @ P.T - (b + lam)[:, None])
    return P, [np.where(R[:, v] < tol)[0] for v in range(len(P))]

def local_vertices(Arows, e1, e2, XI, d):
    """Vertices of the lexicographically perturbed cone: offsets delta*e1 (random), normals tilted by eta*xi (second order
    e2 = -xi.p at the point p, third order delta*eta: -xi.z1); delta >> eta >> delta*eta. All d-subsets that stay feasible,
    residual ties at one order broken at the next. Returns (z1, z2, z3, subset)."""
    from itertools import combinations
    m = len(Arows); out = []
    for S in combinations(range(m), d):
        S = list(S); A = Arows[S]
        if np.linalg.cond(A) > 1e10: continue
        z1 = np.linalg.solve(A, e1[S]); z2 = np.linalg.solve(A, e2[S]); e3 = -XI @ z1[:3]; z3 = np.linalg.solve(A, e3[S])
        cs = [Arows @ z1 - e1, Arows @ z2 - e2, Arows @ z3 - e3]
        ts = [1e-9 * (1 + np.abs(z).max()) for z in (z1, z2, z3)]
        ok = True
        for r in range(m):
            if r in S: continue
            for c, t in zip(cs, ts):
                if c[r] < -t: break
                if c[r] > t: ok = False; break
            if not ok: break
        if ok: out.append((z1, z2, z3, S))
    return out

def resolved_sides(X, b, lam, eps, xi):
    """Sides of every face in the slice with degenerate vertices resolved by eps (generic simple slice). Also V, E, F."""
    P, inc = slice_inc(X, b, lam); n = len(X); sides = np.zeros(n, int); Vr = 0
    for v, T in enumerate(inc):
        if len(T) == 3: sides[T] += 1; Vr += 1; continue
        lv_ = local_vertices(X[T], eps[T], -xi[T] @ P[v], xi[T], 3)
        for z1, z2, z3, S in lv_: sides[T[S]] += 1; Vr += 1
    F = int((sides > 0).sum()); E = int(sides.sum()) // 2
    return sides, Vr, E, F, int(sides.sum()) % 2 == 0 and Vr - E + F == 2 and 3 * Vr == 2 * E

def adjacency(X, b, lam):
    P, inc = slice_inc(X, b, lam); n = len(X)
    rows_, cols_ = [], []
    for v, T in enumerate(inc):
        for t in T: rows_.append(t); cols_.append(v)
    I = csr_matrix((np.ones(len(rows_), np.int32), (rows_, cols_)), shape=(n, len(P)))
    S = (I @ I.T).tocoo(); pairs = set()
    for i, j, c in zip(S.row, S.col, S.data):
        if i < j and c >= 2: pairs.add((int(i), int(j)))
    vcount = np.asarray(I.sum(1)).ravel()
    return pairs, vcount

rows = []; ok_all = True; fails = []; t0 = time.time()
V = OGf; FF = faces(V)
for k in range(KMAX + 1):
    M, Dd, cor = FF
    W = symmetrise(M * Dd[:, None]); FN = faces(W); M2, D2, cor2 = FN
    if k < KMIN:
        V, FF = W, FN; continue
    act = np.zeros(len(W), bool); act[cor2] = True
    X = W / np.einsum('ij,ij->i', W, W)[:, None]; X /= np.linalg.norm(X, axis=1).max()   # scale: max |X| = 1
    b = np.einsum('ij,ij->i', X, X); n = len(X)
    tree = cKDTree(X); perms = [tree.query(X @ g.T)[1] for g in Gf]
    orb = -np.ones(n, int); reps = []
    for i in range(n):
        if orb[i] < 0:
            for p_ in perms: orb[p_[i]] = len(reps)
            reps.append(i)
    LAM, toplam = choose_LAM(X, b)
    row = dict(k=k, n=n, active=int(act.sum()), cut=int((~act).sum()), LAM=LAM, top_event_lam=toplam, orbits=len(reps))
    ev0 = events(X, b, LAM, TOL)
    gap0 = float(min([e[3] for e in ev0], default=np.inf))
    lv = np.array(sorted(set(np.round([e[0] for e in ev0], 9)), reverse=True))
    tsh = np.bincount([len(e[2]) for e in ev0]); row['tight_size_hist'] = {i: int(c) for i, c in enumerate(tsh) if c}
    row.update(events=len(ev0), levels=len(lv), gap5=gap0)
    cuts = np.array([0.0] + list((lv[:-1] + lv[1:]) / 2) + [lv[-1] / 2]) if len(lv) else np.array([0.0, LAM / 2])
    cuts[0] = min(LAM * 0.9, max(toplam * 2, toplam + 0.1))
    # ---------------- unperturbed slices: direct side counts, s_min, cell walls ----------------
    sl = [slice_sides(X, b, l) for l in cuts]
    euler0 = all(Vv - Ee + Ff == 2 and int(s.sum()) == 2 * Ee for s, Vv, Ee, Ff in sl)
    top_ok = bool((sl[0][0] > 0).all()); bot_ok = bool(((sl[-1][0] > 0) == act).all())
    smin = 0.0
    for j in range(len(lv)):
        A_, B_ = sl[j][0], sl[j + 1][0]
        if ((A_ == 0) & (B_ > 0)).any(): fails.append(f'k{k}: unperturbed birth going down'); ok_all = False
        surv = (A_ > 0) & (B_ > 0); d = B_[surv] - A_[surv]; smin += d[d > 0].sum() / 2
    adj = [adjacency(X, b, l)[0] for l in cuts]
    nb = [set() for _ in range(n)]
    for pr in adj:
        for i, j in pr: nb[i].add(j); nb[j].add(i)
    alive = np.array([s[0] > 0 for s in sl])                                # slices x n
    kind = []; exch_touched = np.zeros(n, bool)
    for q in range(len(adj) - 1):                                          # walls changing while both cells alive = exchange
        for pr in adj[q] ^ adj[q + 1]:
            i, j = pr
            if alive[q, i] and alive[q + 1, i] and alive[q, j] and alive[q + 1, j]: exch_touched[i] = exch_touched[j] = True
    nb_top = [set() for _ in range(n)]
    for i, j in adj[0]: nb_top[i].add(j); nb_top[j].add(i)
    _, vtop = adjacency(X, b, cuts[0]); _, vbot = adjacency(X, b, 0.0)
    vev = np.zeros(n, int)
    for e in ev0: vev[e[2]] += 1
    cells = []
    for i in range(n):
        walls = len(nb[i]) + 1 + int(act[i]); corners = int(vtop[i] + vev[i] + (vbot[i] if act[i] else 0))
        if not act[i]: kd = 'pyramid (exchanged)' if exch_touched[i] else 'pyramid'
        elif exch_touched[i]: kd = 'scutoid'
        elif nb[i] != nb_top[i] or any(not alive[-1, j] for j in nb[i]): kd = 'truncated prism'
        else: kd = 'prism'
        cells.append((walls, corners, walls + corners - 2, kd))
    orbit_cells = []
    for o, i in enumerate(reps):
        mem = np.where(orb == o)[0]
        orbit_cells.append(dict(size=len(mem), active=bool(act[i]), walls=cells[i][0], corners=cells[i][1], edges=cells[i][2], kind=cells[i][3],
                                consistent=all(cells[j][:3] == cells[i][:3] for j in mem)))
    cell_ok = all(c['consistent'] for c in orbit_cells)
    wa = [cells[i][0] for i in range(n) if act[i]]; wc = [cells[i][0] for i in range(n) if not act[i]]
    kinds_ = {}
    for c in cells: kinds_[c[3]] = kinds_.get(c[3], 0) + 1
    row.update(unpert_euler_ok=euler0, all_faces_at_top=top_ok, bottom_equals_active=bot_ok, s_min=smin, cells_by_orbit=orbit_cells,
               walls_active_hist={int(w): wa.count(w) for w in sorted(set(wa))}, walls_cut_hist={int(w): wc.count(w) for w in sorted(set(wc))},
               walls_active_mean=float(np.mean(wa)), walls_cut_mean=float(np.mean(wc)) if wc else None, cell_kinds=kinds_, cells_orbit_consistent=cell_ok)
    if not (euler0 and top_ok and bot_ok and cell_ok): ok_all = False; fails.append(f'k{k}: unperturbed slice/cell control')
    # ---- WALLS as sheets (DICTO "a or c, the sheets are continuous"): wall (i, j) = 2D face of P; its lam-range must be ONE interval
    span = {}
    for q, pr in enumerate(adj):
        for w in pr: span.setdefault(w, []).append(q)
    contiguous = all(qs == list(range(qs[0], qs[-1] + 1)) for qs in span.values())
    wtype = {}
    for w, qs in span.items():
        st, en = qs[0] == 0, qs[-1] == len(adj) - 1                         # present at top / reaches the slice just above 0
        wtype[w] = 'full' if st and en else 'ends' if st else 'starts' if en else 'both'
    wcount = {t: sum(1 for v in wtype.values() if v == t) for t in ('full', 'starts', 'ends', 'both')}
    per_cell = np.zeros((n, 4), int); tix = {'full': 0, 'starts': 1, 'ends': 2, 'both': 3}
    for (i, j), t in wtype.items(): per_cell[i, tix[t]] += 1; per_cell[j, tix[t]] += 1
    all_end = set(np.where((per_cell[:, 0] + per_cell[:, 1] == 0))[0].tolist())   # no wall reaches lam = 0
    cut_eq_allend = all_end == set(np.where(~act)[0].tolist())
    Arow = np.hstack([X, -np.ones((n, 1))]); par_pairs = np.zeros(n, int)
    for i in range(n):
        Ni = sorted(nb[i]); a = Arow[i] / np.linalg.norm(Arow[i])
        U = Arow[Ni] - np.outer(Arow[Ni] @ a, a); U /= np.linalg.norm(U, axis=1)[:, None]
        G_ = U @ U.T; par_pairs[i] = int((np.triu(G_, 1) < -1 + 1e-9).sum() + (np.triu(G_, 1) > 1 - 1e-9).sum())
    for o, i in enumerate(reps):
        orbit_cells[o].update(walls_full=int(per_cell[i, 0]), walls_start=int(per_cell[i, 1]), walls_end=int(per_cell[i, 2]),
                              walls_both=int(per_cell[i, 3]), parallel_side_wall_pairs=int(par_pairs[i]))
    row.update(walls_total=len(span), walls_by_type=wcount, walls_one_interval=contiguous, cut_equals_all_walls_end=cut_eq_allend,
               cells_with_parallel_side_walls=int((par_pairs > 0).sum()), parallel_side_wall_pairs=int(par_pairs.sum()))
    if not (contiguous and cut_eq_allend): ok_all = False; fails.append(f'k{k}: wall control (one interval / cut = all walls end)')
    # ---------------- generic resolution (symbolic offsets) ----------------
    per = []
    for seed in SEEDS:
        rng = np.random.default_rng(seed + 1000 * k); eps = rng.uniform(-1, 1, n); xi = rng.normal(size=(n, 3))
        top = resolved_sides(X, b, cuts[0], eps, xi); sides = top[0].copy(); tsides = sides.copy()
        nd = nf = nbad = 0; lost_flip = np.zeros(n, int); gain_flip = np.zeros(n, int); lost_death = np.zeros(n, int)
        dlam = np.full(n, -np.inf); tri_ok = True; f_cl = 0; f_gen = 0; d_cl = 0
        res = []                                                            # resolved generic events with lexicographic lam keys
        for (l, p, T, g) in ev0:
            A = np.hstack([X[T], -np.ones((len(T), 1))])
            for z1, z2, z3, S in local_vertices(A, eps[T], -xi[T] @ p[:3], xi[T], 4):
                res.append((round(l, 9), round(z1[3], 6), round(z2[3], 6), z3[3], l, len(T), T[S]))
        res.sort(key=lambda r: (-r[0], -r[1], -r[2], -r[3]))
        mid_ok = True; checks = 0; lvl_index = {l: q for q, l in enumerate(lv)}; last = None
        elig = [q for q in range(len(lv) - 1) if lv[q] - lv[q + 1] > 1e-6]; check_lv = set(elig[::max(1, len(elig) // 6)])
        for (lr, k1, k2, k3, l, m, TT) in res:
            if last is not None and lr != last and lvl_index[last] in check_lv:   # control at a few well-separated levels
                q = lvl_index[last]; s_ = resolved_sides(X, b, cuts[q + 1], eps, xi)[0]; checks += 1
                if not (s_ == sides).all():
                    mid_ok = False; print(f'    level-slice mismatch k {k} level {q} lam {last} faces {np.where(s_ != sides)[0][:8].tolist()} slice {s_[s_ != sides][:8].tolist()} tracked {sides[s_ != sides][:8].tolist()}', flush=True)
            last = lr
            T = TT
            sub = [(None, TT)]
            for z, TT in sub:
                typ = classify4(X, TT, xi)
                if typ[0] == 'death':
                    i = typ[1]; nd += 1; dlam[i] = l
                    if m > 4: d_cl += 1
                    if sides[i] != 3: tri_ok = False
                    sides[i] = 0
                    for j in typ[2]: sides[j] -= 1; lost_death[j] += 1
                elif typ[0] == 'flip':
                    nf += 1
                    if m > 4: f_cl += 1
                    else: f_gen += 1
                    for j in typ[1]: sides[j] -= 1; lost_flip[j] += 1
                    for j in typ[2]: sides[j] += 1; gain_flip[j] += 1
                else: nbad += 1
        bot = resolved_sides(X, b, cuts[-1], eps, xi); track_ok = bool((bot[0] == sides).all())
        cutp = set(np.where(dlam > 0)[0].tolist()); cut_ok = cutp == set(np.where(~act)[0].tolist())
        dy = np.array(sorted(cutp), int)
        lf, ld, gf = int(lost_flip[dy].sum()), int(lost_death[dy].sum()), int(gain_flip[dy].sum())
        ctrl = dict(top_simple_euler=top[4], bottom_simple_euler=bot[4], all_faces_at_top=bool((tsides > 0).all()), no_birth_vertices=nbad == 0,
                    tracked_equals_bottom_slice=track_ok, tracked_equals_level_slices=mid_ok, dying_are_triangles=tri_ok,
                    cut_set_equals_hull=cut_ok, deaths_equal_cut=nd == row['cut'],
                    side_balance=int((tsides[dy] - 3).sum()) == lf + ld - gf,
                    top_sum_6n_minus_12=int(tsides.sum()) == 6 * n - 12, bottom_sum_6a_minus_12=int(bot[0].sum()) == 6 * row['active'] - 12)
        if not all(ctrl.values()): ok_all = False; fails.append(f'k{k} seed{seed}: ' + ','.join(a for a, v in ctrl.items() if not v))
        ta = tsides[act]; td = tsides[dy] if len(dy) else np.array([0])
        per.append(dict(seed=seed, s=nf, deaths=nd, deaths_in_clusters=d_cl, flips_at_clusters=f_cl, flips_at_generic_points=f_gen,
                        level_checks=checks, dying_top_sides_sum=int(tsides[dy].sum()), dying_lost_via_flips=lf, dying_lost_via_deaths=ld,
                        dying_gained_via_flips=gf, all_lost_via_flips=int(lost_flip.sum()), all_lost_via_deaths=int(lost_death.sum()),
                        flips_touching_dying=int(((lost_flip > 0) | (gain_flip > 0))[dy].sum()),
                        dying_top_sides_hist={int(v): int((td == v).sum()) for v in sorted(set(td.tolist()))},
                        active_top_sides_mean=float(ta.mean()), dying_top_sides_mean=float(td.mean()), controls=ctrl))
    row['generic'] = per
    rows.append(row)
    g1 = per[0]
    print(f"k {k:2d}: n {n:5d} c {row['cut']:4d} a {row['active']:5d} | s {[p_['s'] for p_ in per]} s_min {smin:.0f} | c/s {row['cut'] / max(1, g1['s']):.3f} s/n {g1['s'] / n:.3f} | "
          f"dying: top-sides sum {g1['dying_top_sides_sum']} (mean {g1['dying_top_sides_mean']:.2f}; active {g1['active_top_sides_mean']:.2f}) lost via flips {g1['dying_lost_via_flips']} "
          f"via deaths {g1['dying_lost_via_deaths']} gained {g1['dying_gained_via_flips']} | flips clusters/generic {g1['flips_at_clusters']}/{g1['flips_at_generic_points']} "
          f"deaths in clusters {g1['deaths_in_clusters']} | tight sizes {row['tight_size_hist']} gap {gap0:.1e} | walls active mean {row['walls_active_mean']:.2f} "
          f"cut mean {row['walls_cut_mean'] if row['walls_cut_mean'] is None else round(row['walls_cut_mean'], 2)} | kinds {row['cell_kinds']} | "
          f"walls {row['walls_total']} {row['walls_by_type']} one-interval {row['walls_one_interval']} cut=all-walls-end {row['cut_equals_all_walls_end']} "
          f"parallel side-wall pairs {row['parallel_side_wall_pairs']} | "
          f"controls {all(all(p_['controls'].values()) for p_ in per) and euler0 and top_ok and bot_ok and cell_ok and contiguous and cut_eq_allend} | {time.time() - t0:.0f}s", flush=True)
    for c in orbit_cells:
        print(f"    orbit size {c['size']:3d} {'active' if c['active'] else 'cut   '} walls {c['walls']:3d} corners {c['corners']:3d} edges {c['edges']:3d} {c['kind']:20s} walls full/start/end/both {c['walls_full']}/{c['walls_start']}/{c['walls_end']}/{c['walls_both']} parallel {c['parallel_side_wall_pairs']}", flush=True)
    V, FF = W, FN
json.dump({'mark': 'DICTO #43 scutoid exchanges, 2026-11-11 · DICTO · dictospheres.com', 'k': rows},
          open(OUT, 'w'), default=lambda o: o.item() if hasattr(o, 'item') else str(o))
print('FINAL ok' if ok_all else 'FINAL FAIL ' + '; '.join(fails))
