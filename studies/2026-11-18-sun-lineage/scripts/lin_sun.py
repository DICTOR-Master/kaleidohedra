"""Lineage net change of granule neighbours after a fixed elapsed time tau, for one setting, at steps 10 s and 80 s (README.md).

Segmentation, tracking, contacts, centroids and survivor counts exactly as net_sz.py of studies/2026-11-18-sun-net-change
(its functions are imported; tiles.py of the 15 Nov study unchanged). Added: at every transition of the tracking, the ancestor
links A(n) = {best_par(n)} plus the old cells that are nobody's best_par and whose best_heir is n (largest pixel overlaps, the
quantities tiles.match uses, same tie rule), composed from each start to each end; then the lineage counts of lineage_lib.py.
Check: the survivor columns of every row equal the parent's stored rows (PARENT.json).

Usage: lin_sun.py DATA RUN VAR DZ SIGMA [hmax:|thr:]H OUT.json PARENT.json|none [NFRAMES|all] [steps=1,8] [tauf=8,...]"""
import sys, os, json, time
import numpy as np
import scipy.sparse as sp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '2026-11-18-sun-net-change', 'scripts'))
sys.path.insert(0, HERE)
import net_sz as NZ                      # imports tiles.py of 2026-11-17-sun-step-zero/scripts
TL = NZ.TL
from lineage_lib import lineage_counts, identity_test

START, BIG = NZ.START, NZ.BIG


def links(prev, raw, out):
    """Ancestor links of one transition: arrays (new tracked label, old tracked label)."""
    K = np.int64(raw.max() + 1)
    key = prev.astype(np.int64) * K + raw
    u, cnt = np.unique(key, return_counts=True)
    old, new = u // K, u % K
    best_par, best_heir = {}, {}
    for o, n, c in zip(old.tolist(), new.tolist(), cnt.tolist()):      # the loop of tiles.match: strict >, ascending keys
        if c > best_par.get(n, (0, -1))[1]: best_par[n] = (o, c)
        if c > best_heir.get(o, (0, -1))[1]: best_heir[o] = (n, c)
    fl = raw.ravel(); ids, first = np.unique(fl, return_index=True)
    tr = dict(zip(ids.tolist(), out.ravel()[first].tolist()))          # raw new label -> tracked label
    pars = {o for o, _ in best_par.values()}
    L = [(tr[n], o) for n, (o, _) in best_par.items()]
    L += [(tr[n], o) for o, (n, _) in best_heir.items() if o not in pars]
    a = np.array(L, np.int64)
    return a[:, 0], a[:, 1]


def run(data, run_, var, dz, sigma, h, out, parent=None, nframes=None, method='thr', steps=(1, 8), tauf=(8, 16, 24, 32, 48, 64)):
    t0 = time.time()
    F = np.load(f'{data}/{run_}_{var}_dz{dz}.npy', mmap_mode='r')
    times = np.load(f'{data}/{run_}_times.npy')
    nt = len(times) if nframes is None else min(nframes, len(times))
    L = F.shape[1]
    raw = [TL.segment(NZ.prep(np.asarray(F[k]), var), sigma, h, method=method) for k in range(nt)]
    print(f'PROGRESS segment {nt} frames {time.time() - t0:.0f} s', flush=True)
    mean_cells = float(np.mean([len(np.unique(r)) for r in raw]))
    ell = (L * L / mean_cells) ** 0.5
    P = json.load(open(parent)) if parent and parent != 'none' else None
    res = dict(run=run_, var=var, dz=dz, sigma=sigma, h=h, method=method, frames=nt, L_px=L, mean_cells=mean_cells, ell_px=ell,
               dt_s=float(np.median(np.diff(times))), start_every=START, identity_test=bool(identity_test()), steps={},
               parent_rows_equal=None if P is None else True, links_ok=True)
    cols = ['k0', 'n0', 'n1', 'surv', 'E0s', 'E1s', 'lost', 'made', 'all_lost', 'all_made', 'E0', 'E1', 'd2_px2', 'rel2_px2',
            'lin_lost', 'lin_made', 'lin_pairs', 'fused', 'lin_size', 'multi_anc']
    for s in steps:
        rec, lk, ids_at = {}, {}, {}; prev = None; next_id = 1
        for k in range(0, nt, s):
            if prev is None:
                lab = raw[k].astype(np.int64); next_id = int(lab.max()) + 1
            else:
                lab, _, _, next_id = TL.match(prev, raw[k], next_id)
                lk[k] = links(prev, raw[k], lab)
            prev = lab
            ids_at[k] = np.unique(lab)
            if k % START == 0:
                ids, cen = NZ.centroids(lab, L)
                rec[k] = (ids, cen, NZ.pairs_of(lab))
        R = {str(tf): [] for tf in tauf}
        for k0 in range(0, nt - min(tauf), START):
            i0, c0, E0 = rec[k0]; N0 = len(i0)
            a0, b0 = E0 // BIG, E0 % BIG
            E0i = np.searchsorted(i0, a0).astype(np.int64) * N0 + np.searchsorted(i0, b0)     # start-index keys (a < b kept)
            cur = i0; M = sp.identity(N0, dtype=np.int64, format='csr')
            k = k0
            for tf in sorted(tauf):
                k1 = k0 + tf
                if k1 > nt - 1: break
                while k < k1:
                    k += s
                    nl, ol = lk[k]; nxt = ids_at[k]
                    T = sp.coo_matrix((np.ones(len(nl), np.int64), (np.searchsorted(nxt, nl), np.searchsorted(cur, ol))),
                                      shape=(len(nxt), len(cur))).tocsr()
                    T.data[:] = 1
                    if (np.asarray(T.sum(0)).ravel() == 0).any() or (np.asarray(T.sum(1)).ravel() == 0).any():
                        res['links_ok'] = False
                    M = (T @ M).tocsr(); M.data[:] = 1; cur = nxt
                i1, c1, E1 = rec[k1]
                assert np.array_equal(i1, cur)
                # survivor columns: exactly net_sz.py
                S = np.intersect1d(i0, i1)
                a1, b1 = E1 // BIG, E1 % BIG
                E0s = E0[np.isin(a0, S) & np.isin(b0, S)]; E1s = E1[np.isin(a1, S) & np.isin(b1, S)]
                lost = int(np.setdiff1d(E0s, E1s, assume_unique=True).size); made = int(np.setdiff1d(E1s, E0s, assume_unique=True).size)
                all_lost = int(np.setdiff1d(E0, E1, assume_unique=True).size); all_made = int(np.setdiff1d(E1, E0, assume_unique=True).size)
                p0 = {int(i): c0[j] for j, i in enumerate(i0)}; p1 = {int(i): c1[j] for j, i in enumerate(i1)}
                dS = np.array([NZ.wrap(p1[int(i)] - p0[int(i)], L) for i in S]) if len(S) else np.zeros((0, 2))
                d2 = float((dS ** 2).sum())
                disp = {int(i): dS[j] for j, i in enumerate(S)}
                rel2 = 0.0
                for p in E0s:
                    a, b = int(p // BIG), int(p % BIG)
                    rel2 += float(((disp[b] - disp[a]) ** 2).sum())
                lc = lineage_counts(E0i, N0, np.searchsorted(i1, a1), np.searchsorted(i1, b1), len(i1), M)
                multi = int((np.asarray(M.sum(1)).ravel() > 1).sum())
                R[str(tf)].append([k0, N0, len(i1), int(S.size), int(E0s.size), int(E1s.size), lost, made, all_lost, all_made,
                                   int(E0.size), int(E1.size), round(d2, 3), round(rel2, 3),
                                   lc['lost'], lc['made'], lc['pairs'], lc['fused'], lc['size'], multi])
        RR = {}
        for tf in tauf:
            rows = R[str(tf)]
            RR[str(tf)] = dict(tau_s=tf * res['dt_s'], cols=cols, rows=rows)
            if P is not None:
                pr = P['steps'][str(s)][str(tf)]['rows']
                byk = {int(b[0]): list(map(float, b)) for b in pr}
                eq = all(byk.get(int(a[0])) == list(map(float, a[:14])) for a in rows) and (nframes is not None or len(pr) == len(rows))
                if not eq: res['parent_rows_equal'] = False
                print(f'CHECK step {s} tau {tf}: parent rows equal {eq}', flush=True)
            r = np.array(rows, float)
            if len(r):
                print(f'LIN step {s} tau {tf * res["dt_s"]:.0f} s starts {len(r)} net/surv {(r[:, 6] + r[:, 7]).sum() / r[:, 3].sum():.4f} '
                      f'lineage net/cell {(r[:, 14] + r[:, 15]).sum() / r[:, 1].sum():.4f} D/l {np.sqrt(r[:, 12].sum() / r[:, 3].sum()) / ell:.4f} '
                      f'lineage size {r[:, 18].sum() / r[:, 1].sum():.3f}', flush=True)
        res['steps'][str(s)] = RR
        print(f'PROGRESS step {s} done {time.time() - t0:.0f} s', flush=True)
    res['wall_s'] = time.time() - t0
    os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
    json.dump(res, open(out, 'w'))
    return res


if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if '=' not in x]
    kw = dict(x.split('=') for x in sys.argv[1:] if '=' in x)
    data, run_, var, dz, sigma, h, out, parent = a[:8]
    nf = int(a[8]) if len(a) > 8 and a[8] != 'all' else None
    method, hv = h.split(':')
    steps = tuple(int(x) for x in kw.get('steps', '1,8').split(','))
    tauf = tuple(int(x) for x in kw.get('tauf', '8,16,24,32,48,64').split(','))
    res = run(data, run_, var, dz, float(sigma), float(hv), out, parent, nf, method, steps, tauf)
    ok = (res['identity_test'] and res['links_ok'] and res['parent_rows_equal'] is not False
          and all(len(v['rows']) > 0 for R in res['steps'].values() for v in R.values()))
    print(f'WALL {res["wall_s"]:.0f} s', flush=True)
    print('FINAL ok' if ok else 'FINAL FAIL (identity test, links, parent rows or empty tau)', flush=True)
