# og_vacuus4d_free.py, DICTO 11 Nov 2026 ("most big vacuus dont pass thru center" -> "a sheets without a centre"). Built on
# og_vacuus4d_exact.py (exact coordinates at 60 digits). SHEETS WITHOUT A CENTRE: a sheet is a 3D hyperplane of the sweep's 4D space
# carrying two or more walls of DIFFERENT cells (the walls of one cell always share that cell's own hyperplane: trivial, excluded).
# Wall (i, j) lies in every hyperplane of the pencil span(h_i, h_j), h_m = (X_m, -1, -b_m) in R^5 (homogeneous). Walls (i, j), (k, l)
# with four different cells share a hyperplane iff rank[h_i, h_j, h_k, h_l] <= 3; since h has -1 in one slot and b = |X|^2 in another this
# is: the lifted points (X_m, |X_m|^2) are affinely dependent = the four candidates X_i, X_j, X_k, X_l lie on ONE CIRCLE.
# Float screen (smallest singular value), exact check: 4th singular value at 60 digits below 1e-40 of the largest, common hyperplane from the null vector,
# sheets grouped by exact hyperplane. Report: sheets, walls per sheet, wall types (aa / ac / cc), do sheets separate cut from survivors.
# Original header follows.
# og_vacuus4d_exact.py, DICTO 11 Nov 2026 ("do the exact 4D vacuus count next"). As og_vacuus4d.py (central 3D slices through the centre
# c = (O, lc) carrying the walls of the hop's 4D sweep), but decided from the EXACT Q(sqrt5) coordinates at 60 digits:
#  - candidates X_i = exact foot points W_i / |W_i|^2 (no rescaling), b_i = |X_i|^2; walls (i, j) from the float sweep (combinatorics);
#  - special heights: float roots refined by Newton on the exact-coefficient quadratic minor, accepted only if ALL 2x2 minors vanish to
#    1e-40 (relative); trivial heights lc = -b_i (centre on cell i's own hyperplane) excluded and counted apart;
#  - slices counted by exact parallelism (normalised normals compared to 1e-40); GAP = smallest non-zero difference seen, must be > 1e-20.
# Per level: walls, generic slice count, every non-trivial special height with its slice count and the slice types (walls between
# active-active / active-cut / cut-cut cells). Control: counts at three generic heights agree; GAP check.
# usage: python -u og_vacuus4d_free.py <five-fold-octet dir> <kmin> <kmax> <out.json>
import sys, os, json, time
here = os.path.dirname(os.path.abspath(__file__)); ARGS = list(sys.argv)
_K1, _K2, _OUT = int(ARGS[2]), int(ARGS[3]), os.path.abspath(ARGS[4])
sys.argv = [ARGS[0], ARGS[1], str(_K1), str(_K2), '/dev/null']
exec(open(os.path.join(here, 'og_exchanges.py')).read().split('for k in range(KMAX + 1):')[0])  # faces, symmetrise, events, adjacency
_keep = dict(faces=faces, symmetrise=symmetrise)
sys.argv = [ARGS[0], ARGS[1], '0', '/dev/null']
exec(open(os.path.join(here, 'exact_family.py')).read().split("t0 = time.time()")[0])          # R5, cv, exact_faces, OG (last: its G wins)
faces, symmetrise = _keep['faces'], _keep['symmetrise']
import numpy as np, mpmath as mp
mp.mp.dps = 60; TOLZ = mp.mpf('1e-40'); S5m = mp.sqrt(5)
K1, K2, OUT = _K1, _K2, _OUT
def m(x): return mp.mpf(int(x.a.numerator)) / int(x.a.denominator) + mp.mpf(int(x.b.numerator)) / int(x.b.denominator) * S5m
def nu_of(lc, Xm, bm, i, j):
    return [(lc + bm[j]) * Xm[i][t] - (lc + bm[i]) * Xm[j][t] for t in range(3)] + [-(lc + bm[j]) + (lc + bm[i])]
def canon(v):
    nr = mp.sqrt(sum(x * x for x in v))
    if nr < mp.mpf('1e-30'): return None                                   # wall plane through the centre: no single slice
    v = [x / nr for x in v]
    for x in v:
        if abs(x) > mp.mpf('1e-30'): s = 1 if x > 0 else -1; break
    return tuple(s * x for x in v)
SCALE = mp.mpf(10) ** 35
def count(lc, Xm, bm, Wp):
    keys = [canon(nu_of(lc, Xm, bm, int(i), int(j))) for i, j in Wp]
    through = [q for q, kk in enumerate(keys) if kk is None]
    ik = {q: tuple(int(mp.nint(x * SCALE)) for x in kk) for q, kk in enumerate(keys) if kk is not None}
    order = sorted(ik, key=lambda q: ik[q])
    lab = [-1] * len(keys); cur = -1; gap = mp.inf; prev = None
    for q in order:
        if prev is None or max(abs(x - y) for x, y in zip(keys[q], keys[prev])) > TOLZ:
            if prev is not None: gap = min(gap, max(abs(x - y) for x, y in zip(keys[q], keys[prev])))
            cur += 1
        lab[q] = cur; prev = q
    # safety: equal keys must be adjacent in numeric order; check no two different labels have keys within TOLZ (sampled neighbours)
    return cur + 1 + (1 if through else 0), lab, gap, len(through)
t0 = time.time(); rows = []; ok_all = True
We = [tuple(cv(x) for x in v) for v in OG]; V = OGf; FF = faces(V)
for k in range(K2 + 1):
    idx = {v: i for i, v in enumerate(We)}; Wfx = np.array([fl(v) for v in We])
    Fx, _, _ = exact_faces(We, idx, Wfx); feet = {}
    for n_, d_, _ in Fx.values():
        s_ = d_ / dot(n_, n_); feet[tuple(s_ * x for x in n_)] = 1
    feet = list(feet)
    M, Dd, cor = FF
    W = symmetrise(M * Dd[:, None]); FN = faces(W); M2, D2, cor2 = FN
    if k >= K1:
        act = np.zeros(len(W), bool); act[cor2] = True; n = len(W)
        tr = cKDTree(np.array([fl(v) for v in feet])); dd, mp_idx = tr.query(W)
        if dd.max() > 1e-9 or len(set(mp_idx.tolist())) != n: print(f'FINAL FAIL: exact/float candidate match at k {k}'); sys.exit(1)
        Xf = W / np.einsum('ij,ij->i', W, W)[:, None]; sc = np.linalg.norm(Xf, axis=1).max(); Xs = Xf / sc; bs = np.einsum('ij,ij->i', Xs, Xs)
        Hm = []
        for q in range(n):
            w = feet[mp_idx[q]]; wm = [m(x) for x in w]; w2 = sum(x * x for x in wm); x = [c / w2 for c in wm]
            Hm.append(x + [mp.mpf(-1), -sum(c * c for c in x)])
        LAM, toplam = choose_LAM(Xs, bs); ev0 = events(Xs, bs, LAM, TOL)
        lv = np.array(sorted(set(np.round([e[0] for e in ev0], 9)), reverse=True))
        cuts = np.array([0.0] + list((lv[:-1] + lv[1:]) / 2) + [lv[-1] / 2]) if len(lv) else np.array([0.0, LAM / 2])
        cuts[0] = min(LAM * 0.9, max(toplam * 2, toplam + 0.1))
        walls = set()
        for l in list(cuts) + [0.0]:
            for pr in adjacency(Xs, bs, l)[0]: walls.add(tuple(sorted(pr)))
        Wp = np.array(sorted(walls)); nW = len(Wp)
        Hf = np.hstack([Xs, -np.ones((n, 1)), -bs[:, None]])                 # float screen in scaled units (rank is scale-free)
        hits = []
        for w1 in range(nW):
            i, j = Wp[w1]; o = np.arange(w1 + 1, nW); o = o[(Wp[o, 0] != i) & (Wp[o, 0] != j) & (Wp[o, 1] != i) & (Wp[o, 1] != j)]
            if len(o) == 0: continue
            Mx = np.stack([np.broadcast_to(Hf[i], (len(o), 5)), np.broadcast_to(Hf[j], (len(o), 5)), Hf[Wp[o, 0]], Hf[Wp[o, 1]]], 1)
            sv = np.linalg.svd(Mx, compute_uv=False)
            for w2 in o[sv[:, 3] / sv[:, 0] < 1e-9]: hits.append((w1, int(w2)))
        # exact check + common hyperplane
        sheets = {}; svec = {}; rejected = 0; mingap = mp.inf
        for w1, w2 in hits:
            i, j = map(int, Wp[w1]); kk, ll = map(int, Wp[w2])
            A = mp.matrix([[Hm[i][t], Hm[j][t], -Hm[kk][t], -Hm[ll][t]] for t in range(5)])
            U, S, Vt = mp.svd_r(A)                                            # rank <= 3  <=>  4th singular value ~ 0 (60 digits)
            if S[3] > TOLZ * S[0]: rejected += 1; mingap = min(mingap, S[3] / S[0]); continue
            c = [Vt[3, t] for t in range(4)]
            v = [c[0] * Hm[i][t] + c[1] * Hm[j][t] for t in range(5)]
            nv = mp.sqrt(sum(x * x for x in v)); v = [x / nv for x in v]
            sg = next(1 if x > 0 else -1 for x in v if abs(x) > mp.mpf('1e-30')); key = tuple(int(mp.nint(sg * x * mp.mpf(10) ** 35)) for x in v)
            sheets.setdefault(key, set()).update([w1, w2]); svec[key] = v
        typ = act[Wp[:, 0]].astype(int) + act[Wp[:, 1]].astype(int)
        sizes = {}; mix = {}; cells_cut_in = 0; cells_act_in = 0; incell = set()
        for key, ws in sheets.items():
            sizes[len(ws)] = sizes.get(len(ws), 0) + 1
            ts = str(tuple(sorted(set(int(typ[w]) for w in ws)))); mix[ts] = mix.get(ts, 0) + 1
            for w in ws: incell.update(map(int, Wp[w]))
        # where does each sheet meet the slider axis (y = 0)? hyperplane v.(y, lam, 1) = 0 with h = (X, -1, -b) convention: v_y.y + v_lam*lam + v_1 = 0
        hts = []; vertical = 0
        for key, v in svec.items():
            if abs(v[3]) < mp.mpf('1e-30'): vertical += 1; continue
            hts.append(float(-v[4] / v[3]) / float(sc ** 2))          # in units of max b (scaled)
        hts = np.array(hts); uh = len(np.unique(np.round(hts, 9)))
        print(f'      sheets meet the slider axis at {uh} different heights (of {len(hts)} non-vertical; {vertical} vertical sheets contain the axis direction); heights/max b from {hts.min() if len(hts) else 0:+.3f} to {hts.max() if len(hts) else 0:+.3f}', flush=True)
        cut_in = sum(1 for c_ in incell if not act[c_]); act_in = sum(1 for c_ in incell if act[c_])
        gap_ok = mingap > mp.mpf('1e-20'); ok_all &= gap_ok
        rows.append(dict(k=k, cells=n, cut=int((~act).sum()), walls=nW, float_hits=len(hits), exact_rejected=rejected, sheets=len(sheets),
                         walls_per_sheet=sizes, sheet_types=mix, cut_cells_on_sheets=cut_in, active_cells_on_sheets=act_in,
                         min_rejected_gap=float(mingap) if mingap != mp.inf else None))
        print(f'PROGRESS {(k - K1 + 1) / (K2 - K1 + 1):.3f}', flush=True)
        print(f'k {k:2d}: cells {n} (cut {int((~act).sum())}) | walls {nW} | float hits {len(hits)}, exact {len(hits) - rejected} (rejected {rejected}, min gap {mp.nstr(mingap, 3)}) '
              f'| SHEETS {len(sheets)} | walls per sheet {dict(sorted(sizes.items()))} | types (2 aa, 1 ac, 0 cc) {mix} | cells on sheets: cut {cut_in}/{int((~act).sum())}, active {act_in}/{int(act.sum())} ({time.time() - t0:.0f}s)', flush=True)
    We = feet; V, FF = W, FN
json.dump(rows, open(OUT, 'w'), indent=1)
print('FINAL ok' if ok_all else 'FINAL FAIL: an exactly rejected float hit too close to zero (gap <= 1e-20)')
