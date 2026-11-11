# og_vacuus4d_exact.py, DICTO 11 Nov 2026 ("do the exact 4D vacuus count next"). As og_vacuus4d.py (central 3D slices through the centre
# c = (O, lc) carrying the walls of the hop's 4D sweep), but decided from the EXACT Q(sqrt5) coordinates at 60 digits:
#  - candidates X_i = exact foot points W_i / |W_i|^2 (no rescaling), b_i = |X_i|^2; walls (i, j) from the float sweep (combinatorics);
#  - special heights: float roots refined by Newton on the exact-coefficient quadratic minor, accepted only if ALL 2x2 minors vanish to
#    1e-40 (relative); trivial heights lc = -b_i (centre on cell i's own hyperplane) excluded and counted apart;
#  - slices counted by exact parallelism (normalised normals compared to 1e-40); GAP = smallest non-zero difference seen, must be > 1e-20.
# Per level: walls, generic slice count, every non-trivial special height with its slice count and the slice types (walls between
# active-active / active-cut / cut-cut cells). Control: counts at three generic heights agree; GAP check.
# usage: python -u og_vacuus4d_exact.py <five-fold-octet dir> <kmin> <kmax> <out.json>
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
    feet = list(feet)                                                  # exact points of D_{k+1} = candidates of hop k
    M, Dd, cor = FF
    W = symmetrise(M * Dd[:, None]); FN = faces(W); M2, D2, cor2 = FN
    if k >= K1:
        act = np.zeros(len(W), bool); act[cor2] = True
        tr = cKDTree(np.array([fl(v) for v in feet])); dd, mp_idx = tr.query(W)
        if dd.max() > 1e-9 or len(set(mp_idx.tolist())) != len(W): print(f'FINAL FAIL: exact/float candidate match at k {k}'); sys.exit(1)
        Xf = W / np.einsum('ij,ij->i', W, W)[:, None]; sc = np.linalg.norm(Xf, axis=1).max(); Xs = Xf / sc; bs = np.einsum('ij,ij->i', Xs, Xs)
        Xm = []; bm = []
        for q in range(len(W)):
            w = feet[mp_idx[q]]; wm = [m(x) for x in w]; w2 = sum(x * x for x in wm); x = [c / w2 for c in wm]; Xm.append(x); bm.append(sum(c * c for c in x))
        # walls from the float sweep (same code as og_vacuus4d.py)
        LAM, toplam = choose_LAM(Xs, bs); ev0 = events(Xs, bs, LAM, TOL)
        lv = np.array(sorted(set(np.round([e[0] for e in ev0], 9)), reverse=True))
        cuts = np.array([0.0] + list((lv[:-1] + lv[1:]) / 2) + [lv[-1] / 2]) if len(lv) else np.array([0.0, LAM / 2])
        cuts[0] = min(LAM * 0.9, max(toplam * 2, toplam + 0.1))
        walls = set()
        for l in list(cuts) + [0.0]:
            for pr in adjacency(Xs, bs, l)[0]: walls.add(tuple(sorted(pr)))
        Wp = np.array(sorted(walls)); nW = len(Wp)
        # float special heights in UNSCALED units (lc_unscaled = lc_scaled * sc^2), then exact refinement
        Xu = Xf; bu = np.einsum('ij,ij->i', Xu, Xu); i_, j_ = Wp[:, 0], Wp[:, 1]
        A = np.hstack([Xu[i_] - Xu[j_], np.zeros((nW, 1))]); C = np.hstack([bu[j_][:, None] * Xu[i_] - bu[i_][:, None] * Xu[j_], (bu[i_] - bu[j_])[:, None]])
        cand = {}
        for w1 in range(nW):
            for (p, q) in ((0, 3), (1, 3), (2, 3)):
                al = A[w1, p] * A[:, q] - A[w1, q] * A[:, p]; be = A[w1, p] * C[:, q] + C[w1, p] * A[:, q] - A[w1, q] * C[:, p] - C[w1, q] * A[:, p]
                ga = C[w1, p] * C[:, q] - C[w1, q] * C[:, p]
                sc_ = np.abs(np.stack([al, be, ga])).max(0) + 1e-300; al, be, ga = al / sc_, be / sc_, ga / sc_
                disc = be ** 2 - 4 * al * ga; quad = np.abs(al) > 1e-12; sq = np.sqrt(np.maximum(disc, 0))
                for r in (np.where(quad & (disc >= -1e-12), (-be + sq) / np.where(quad, 2 * al, 1), np.nan),
                          np.where(quad & (disc >= -1e-12), (-be - sq) / np.where(quad, 2 * al, 1), np.nan),
                          np.where(~quad & (np.abs(be) > 1e-12), -ga / np.where(np.abs(be) > 1e-12, be, 1), np.nan)):
                    for w2 in np.where(np.isfinite(r) & (np.arange(nW) > w1))[0]:
                        lc = float(r[w2]); n1 = lc * A[w1] + C[w1]; n2 = lc * A[w2] + C[w2]
                        if np.linalg.norm(n1) < 1e-12 or np.linalg.norm(n2) < 1e-12: continue
                        if abs(abs(n1 @ n2) / (np.linalg.norm(n1) * np.linalg.norm(n2)) - 1) < 1e-10:
                            cand.setdefault(round(lc, 8), []).append((w1, int(w2)))
                break
        # exact refinement per float height: Newton on |nu1 x nu2|^2 along lc using one pair, then accept if all minors vanish
        heights = []; trivial = 0
        for lcf, prs in cand.items():
            w1, w2 = prs[0]; lc = mp.mpf(lcf)
            def f(l):
                a = nu_of(l, Xm, bm, *map(int, Wp[w1])); b_ = nu_of(l, Xm, bm, *map(int, Wp[w2]))
                return a[0] * b_[3] - a[3] * b_[0] + a[1] * b_[3] - a[3] * b_[1] + a[2] * b_[3] - a[3] * b_[2]
            try: lc = mp.findroot(f, lc, tol=mp.mpf('1e-50'))
            except Exception: continue
            a = nu_of(lc, Xm, bm, *map(int, Wp[w1])); b_ = nu_of(lc, Xm, bm, *map(int, Wp[w2]))
            na = mp.sqrt(sum(x * x for x in a)); nb = mp.sqrt(sum(x * x for x in b_))
            if max(abs(a[p] * b_[q] - a[q] * b_[p]) for p in range(4) for q in range(p + 1, 4)) > TOLZ * na * nb: continue
            if min(abs(lc + x) for x in bm) < mp.mpf('1e-30'): trivial += 1; continue
            if all(abs(lc - h) > mp.mpf('1e-30') for h, _ in heights): heights.append((lc, len(prs)))
        maxb = max(bm)
        gens = [mp.mpf('0.1234567') * maxb, mp.mpf('0.4321') * maxb, -mp.mpf('0.2718') * maxb]
        NG = [count(g, Xm, bm, Wp)[0] for g in gens]; gen_ok = len(set(NG)) == 1; ok_all &= gen_ok
        typ = act[Wp[:, 0]].astype(int) + act[Wp[:, 1]].astype(int)
        res_h = []; mingap = mp.inf
        for lc, npr in sorted(heights, key=lambda h: -h[1])[:12]:
            Nn, lab, gap, nthr = count(lc, Xm, bm, Wp); mingap = min(mingap, gap)
            mix = {}
            for s_ in range(Nn):
                ts = tuple(sorted(set(int(typ[q]) for q in range(nW) if lab[q] == s_)))
                if ts: mix[str(ts)] = mix.get(str(ts), 0) + 1
            res_h.append(dict(lc_over_maxb=float(lc / maxb), N=Nn, drop=NG[0] - Nn, mix=mix, walls_through_centre=nthr))
        gap_ok = mingap > mp.mpf('1e-20'); ok_all &= gap_ok
        mono = all(r_['drop'] >= 0 for r_ in res_h); ok_all &= mono          # a special height can only merge slices
        rows.append(dict(k=k, cells=len(W), cut=int((~act).sum()), walls=nW, N_generic=NG[0], trivial_heights_skipped=trivial, special_heights=len(heights), top=res_h, min_gap=float(mingap) if mingap != mp.inf else None))
        print(f'PROGRESS {(k - K1 + 1) / (K2 - K1 + 1):.3f}', flush=True)
        print(f'k {k:2d}: cells {len(W)} (cut {int((~act).sum())}) | walls {nW} | generic slices {NG[0]} (3 heights agree {gen_ok}) | non-trivial special heights {len(heights)} (trivial skipped {trivial}) | min gap {mp.nstr(mingap, 3)} ({time.time() - t0:.0f}s)', flush=True)
        for r_ in res_h[:6]:
            print(f'      lc/max b {r_["lc_over_maxb"]:+.8f}: {r_["N"]} slices (drop {r_["drop"]}; walls through centre {r_["walls_through_centre"]}) | types (2 aa, 1 ac, 0 cc): {r_["mix"]}', flush=True)
    We = feet; V, FF = W, FN
json.dump(rows, open(OUT, 'w'), indent=1)
print('FINAL ok' if ok_all else 'FINAL FAIL: generic counts disagree or a gap below 1e-20')
