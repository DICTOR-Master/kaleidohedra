"""Event census of a granulation tiling sequence with the shared event logger (studies/2026-11-15-event-logger, imported unchanged).

For one segmentation setting (run, field, depth, smoothing sigma, threshold h): segment every snapshot once (tiles.py), then for each
time step (every s-th snapshot) match cells across frames, log events with eventlog.classify, check every frame (torus Euler
V - E + F = 0; triple junctions) and every step (balance, with a negative control), and count:
  elementary swaps: inside every logged event (swap or clump), each lost contact (a, b) paired with a gained contact (c, d) of the
  same four cells (c, d touched a and b before; a, b touch c and d after); and two-step swaps (a lost-only change, the four-fold
  junction, then the matching gained-only change within W seconds); swaps undone within W seconds (flicker: the same four cells
  swap back); persistent swaps (= elementary - 2 x flicker pairs),
  births, deaths, splits, merges, relabels, clumps; rates per cell per minute; mean cell lifetime by Little's law
  (mean number of cells / rate of new labels) and from complete tracks; swaps per split, per birth, per cell lifetime.
Cell statistics on every 5th frame: side-number distribution p(n), mean, variance mu2, Aboav-Weaire fit n m(n) = (6 - a) n + 6a + mu2
(Aboav 1970, Metallography 3, 383; Weaire 1974, Metallography 7, 157), Lewis's law fit A(n) linear in n (Lewis 1928, Anat. Rec. 38,
341); the same for the periodic Voronoi tiling of the cell centroids.

ADDED for studies/2026-11-17-sun-step-zero (copy of census.py of studies/2026-11-15-sun-granulation; every count above is
unchanged and must reproduce): per step, (1) the full list of elementary swaps [time, lost pair, gained pair, two-step?, share], so
the persistence window P can be applied afterwards at ANY value (persistent = elementary - 2 x swaps undone by the same four cells
within P, the census rule); share = the smallest frame-to-frame overlap (Jaccard: overlap / union of the same label in the two
frames) of the four cells, at the frame(s) where the contacts were lost and gained (a continuity measure: unrelated frames give low
shares); (2) centroid displacements of kept cells between sampled frames (periodic circular means), for an apparent cell speed.

Usage: census_sz.py DATA RUN VAR DZ SIGMA [hmax:|thr:]H STEPS(comma) W_SECONDS OUT.json [NFRAMES|all]"""
import sys, os, json, itertools, time
import numpy as np
from collections import Counter, defaultdict
from scipy import ndimage as ndi
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', '2026-11-15-event-logger', 'scripts'))
import eventlog as EL
_p = (lambda *a, **k: None) if os.environ.get('CENSUS_QUIET') else print
import tiles as TL


def share_disp(a, b, L):
    """Jaccard share of every label present in both maps a (earlier) and b (later), and the periodic centroid displacement (pixels)."""
    a = a.ravel().astype(np.int64); b = b.ravel().astype(np.int64); M = int(max(a.max(), b.max())) + 1
    same = a == b
    ov = np.bincount(a[same], minlength=M).astype(float)
    na = np.bincount(a, minlength=M).astype(float); nb = np.bincount(b, minlength=M).astype(float)
    both = np.nonzero((na > 0) & (nb > 0))[0]
    jac = ov[both] / (na[both] + nb[both] - ov[both])
    yy, xx = np.divmod(np.arange(L * L), L)
    def cen(lab, n):
        out = []
        for c in (yy, xx):
            th = 2 * np.pi * c / L
            cs = np.bincount(lab, weights=np.cos(th), minlength=M); sn = np.bincount(lab, weights=np.sin(th), minlength=M)
            out.append(np.arctan2(sn, cs) * L / (2 * np.pi))
        return np.stack(out, 1)
    ca, cb = cen(a, na), cen(b, nb)
    d = (cb[both] - ca[both] + L / 2) % L - L / 2
    return dict(zip(both.tolist(), jac.tolist())), d, jac


def load_field(data, run, var, dz):
    a = np.load(f'{data}/{run}_{var}_dz{dz}.npy', mmap_mode='r')
    return a


def prep(img, var):
    return 10.0 ** img if var == 'lgtg' else img     # temperature in K; uz as stored (upflow positive, checked in the pilot)


def centroids(lab, L):
    ids = np.unique(lab)
    yy, xx = np.indices(lab.shape)
    out = {}
    for coord, k in ((yy, 0), (xx, 1)):
        th = 2 * np.pi * coord / L
        s = ndi.mean(np.sin(th), lab, ids); c = ndi.mean(np.cos(th), lab, ids)
        out[k] = (np.arctan2(s, c) % (2 * np.pi)) * L / (2 * np.pi)
    return ids, np.stack([out[0], out[1]], 1)


def aboav_lewis(n, m, A):
    ns = np.array(list(n.values())); ms = np.array([m[c] for c in n]); As = np.array([A[c] for c in n], float)
    mu = ns.mean(); mu2 = ((ns - mu) ** 2).mean()
    s, i = np.polyfit(ns, ns * ms, 1)
    lew = {}
    for k in sorted(set(ns.tolist())):
        sel = ns == k
        if sel.sum() >= 20: lew[int(k)] = float(As[sel].mean() / As.mean())
    if len(lew) >= 3:
        kk = np.array(list(lew)); vv = np.array(list(lew.values()))
        ls, li = np.polyfit(kk, vv, 1); var = ((vv - vv.mean()) ** 2).sum()
        r2 = float(1 - ((vv - (ls * kk + li)) ** 2).sum() / var) if var > 0 else None
    else: ls = li = r2 = None
    return dict(mean_n=float(mu), mu2=float(mu2), aboav_a=float(6 - s), aboav_intercept=float(i), aboav_pred_intercept=float(6 * (6 - s) + mu2),
                lewis_rel_area=lew, lewis_slope=ls, lewis_intercept=li, lewis_r2=r2)


def run_config(data, run, var, dz, sigma, h, steps, W, out, nframes=None, method='hmax'):
    t0 = time.time()
    meta = json.load(open(f'{data}/{run}_meta.json')) if os.path.exists(f'{data}/{run}_meta.json') else {}
    F = load_field(data, run, var, dz)
    times = np.load(f'{data}/{run}_times.npy')
    nt = len(times) if nframes is None else min(nframes, len(times))
    L = F.shape[1]
    labs = []
    for k in range(nt):
        labs.append(TL.segment(prep(np.asarray(F[k]), var), sigma, h, method=method))
        _p(f'PROGRESS {0.5 * (k + 1) / nt:.4f} segment {k + 1}/{nt}', flush=True)
    res = dict(run=run, var=var, dz=dz, sigma=sigma, h=h, method=method, W_s=W, frames_available=nt, dx_Mm=meta.get('dx_Mm'), box_Mm=L * meta.get('dx_Mm', 0),
               steps={})
    # cell statistics (step independent) on every 5th frame
    pn, stats, vstats, vpn = Counter(), [], [], Counter()
    for k in range(0, nt, 5):
        G = TL.graph(labs[k]); n, A, m = TL.cell_stats(labs[k], G)
        pn.update(n.values()); stats.append(aboav_lewis(n, m, A))
        ids, cen = centroids(labs[k], L)
        nb = TL.periodic_voronoi_counts(cen, L)
        vn = {i: len(nb[i]) for i in nb}; vm = {i: np.mean([vn[j] for j in nb[i]]) for i in nb}
        vA = {i: 1.0 for i in nb}
        vpn.update(vn.values()); vstats.append(aboav_lewis(vn, vm, vA))
    agg = lambda S, key: float(np.mean([s[key] for s in S]))
    res['cells'] = dict(frames_sampled=len(stats), mean_cells=float(np.mean([len(np.unique(l)) for l in labs[::5]])),
                        p_n={int(k): v / sum(pn.values()) for k, v in sorted(pn.items())},
                        mean_n=agg(stats, 'mean_n'), mu2=agg(stats, 'mu2'), aboav_a=agg(stats, 'aboav_a'),
                        aboav_intercept=agg(stats, 'aboav_intercept'), aboav_pred_intercept=agg(stats, 'aboav_pred_intercept'),
                        lewis=stats[len(stats) // 2]['lewis_rel_area'], lewis_slope=stats[len(stats) // 2]['lewis_slope'],
                        lewis_r2=stats[len(stats) // 2]['lewis_r2'])
    res['centroid_voronoi'] = dict(p_n={int(k): v / sum(vpn.values()) for k, v in sorted(vpn.items())}, mean_n=agg(vstats, 'mean_n'),
                                   mu2=agg(vstats, 'mu2'), aboav_a=agg(vstats, 'aboav_a'))
    for si, s in enumerate(steps):
        idx = list(range(0, nt, s))
        prev = None; next_id = 1; counts = Counter(); clumps = Counter(); nfail = 0; bad_bal = 0; neg = None
        euler_bad = 0; odd_frames = 0; jdeg = Counter(); ncell_sum = 0; first_seen, last_seen = {}, {}
        swaps = []; pend_lost = []; unmatched_gain = 0; splits_l = []; merges_l = []
        lost_sh = {}; swap_sh = []; d2_all = []; d2_cont = []; jac_med = []
        for q, k in enumerate(idx):
            raw = labs[k]
            if prev is None:
                lab = raw.astype(np.int64); next_id = int(lab.max()) + 1; par = her = {}
            else:
                lab, par, her, next_id = TL.match(prev_lab, raw, next_id)
                sh, dsp, jac = share_disp(prev_lab, lab, L)
                d2 = (dsp ** 2).sum(1); d2_all.append(float(d2.sum())); d2_cont.append((float(d2[jac >= 0.5].sum()), int((jac >= 0.5).sum()), len(d2)))
                jac_med.append(float(np.median(jac)) if len(jac) else 0.0)
                shr = lambda cc: min(sh.get(int(c), 0.0) for c in cc)
            G = TL.graph(lab)
            ncell = len(np.unique(lab)); ncell_sum += ncell
            chi = TL.torus_euler(ncell, G)
            if chi != 0: euler_bad += 1
            if G['odd']: odd_frames += 1
            jdeg.update(len(cs) for cs, _ in G['junctions'])
            T = TL.to_tiling(EL.Tiling, lab, G, float(times[k]), par, None)
            if prev is not None:      # heirs (shares of a vanished OLD cell's area) belong to the earlier frame, as the logger reads them
                prev.heirs = {str(a): {str(b): s for b, s in v.items()} for a, v in her.items()}
            c = EL.check_tiling(T)
            if not c['ok']: nfail += 1
            for cid in T.cells:
                first_seen.setdefault(cid, q); last_seen[cid] = q
            if prev is not None:
                ev = EL.classify(prev, T)
                ok, sm, d = EL.balance(prev, T, ev)
                if not ok: bad_bal += 1
                if neg is None and any(e['net'] for e in ev):
                    bad = [dict(e) for e in ev]; i = next(i for i, e in enumerate(bad) if e['net']); bad[i]['type'] = 'swap'
                    neg = not EL.balance(prev, T, bad)[0]
                for e in ev:
                    counts[e['type']] += 1
                    if e['type'] == 'split':
                        x = next(c for c in e['cells'] if c not in prev.cells)
                        pp = T.parents.get(x, {}); par0 = max(pp, key=pp.get) if pp else None
                        splits_l.append((float(times[k]), x, par0))
                    if e['type'] in ('merge', 'death'):
                        y = next(c for c in e['cells'] if c not in T.cells)
                        hh = prev.heirs.get(y, {}); heir0 = max(hh, key=hh.get) if hh else None
                        merges_l.append((float(times[k]), y, heir0, e['type']))
                    if e['type'] == 'clump': clumps[e['pattern']] += 1
                    # elementary swaps inside every event: a lost pair (a, b) and a gained pair (c, d) of kept cells form one swap when
                    # c, d touched both a and b before and a, b touch both c and d after (the 2-2 move)
                    cs = sorted(e['cells'])
                    lost = [p for p in itertools.combinations(cs, 2) if p in prev.pairs and p not in T.pairs]
                    gained = [p for p in itertools.combinations(cs, 2) if p in T.pairs and p not in prev.pairs]
                    used = set()
                    for l in lost:
                        cn = prev.nb[l[0]] & prev.nb[l[1]]
                        g = next((g for g in gained if g not in used and set(g) <= cn and set(l) <= (T.nb[g[0]] & T.nb[g[1]])), None)
                        if g is not None:
                            used.add(g); swaps.append((float(times[k]), frozenset(l), frozenset(g), 'same step', e['type']))
                            swap_sh.append(shr(set(l) | set(g)))
                        elif e['net'] == 0 and not any(c not in prev.cells or c not in T.cells for c in cs):
                            pend_lost.append((float(times[k]), l, cn)); lost_sh[(float(times[k]), l)] = shr(cs)
                    for g in gained:
                        if g in used: continue
                        if e['net'] == 0 and not any(c not in prev.cells or c not in T.cells for c in cs):
                            j = next((j for j, (tl, l, cn) in enumerate(pend_lost) if float(times[k]) - tl <= W + 1e-6 and set(g) <= cn
                                      and set(l) <= (T.nb[g[0]] & T.nb[g[1]])), None)
                            if j is not None:
                                tl, l, cn = pend_lost.pop(j); swaps.append((float(times[k]), frozenset(l), frozenset(g), 'two steps', e['type']))
                                swap_sh.append(min(lost_sh.get((tl, l), 0.0), shr(set(l) | set(g))))
                            else: unmatched_gain += 1
            prev, prev_lab = T, lab
            _p(f'PROGRESS {0.5 + 0.5 * (si + (q + 1) / len(idx)) / len(steps):.4f} step {s} frame {q + 1}/{len(idx)}', flush=True)
        # flicker: a swap undone (same two pairs, reversed) within W seconds
        def flicker(Wf):
            open_, fl = {}, 0
            for t, lo, ga, how, typ in swaps:
                key = (ga, lo)
                if key in open_ and t - open_[key] <= Wf + 1e-6:
                    fl += 1; del open_[key]
                else:
                    open_[(lo, ga)] = t
            return fl
        flick = flicker(W)
        # split flicker: a piece split off a cell merges back into the same cell within W seconds
        def split_flicker(Wf, kind=None):
            # a piece split off a cell that vanishes again within Wf seconds: merges back into the same cell, or dies (three-sided)
            born = {x: (t, p) for t, x, p in splits_l}
            return sum(1 for t, y, hr, ty in merges_l if y in born and t - born[y][0] <= Wf + 1e-6
                       and (kind is None or ty == kind) and (ty == 'death' or hr == born[y][1]))
        sm_flick = split_flicker(W)
        splits_persistent = counts['split'] - sm_flick
        merges_persistent = counts['merge'] - split_flicker(W, 'merge'); deaths_persistent = counts['death'] - split_flicker(W, 'death')
        splits_persistent_by_W = {str(int(Wf)): counts['split'] - split_flicker(Wf) for Wf in (20, 30, 60, 120, 240)}
        persistent_by_W = {str(int(Wf)): len(swaps) - 2 * flicker(Wf) for Wf in (20, 30, 60, 120, 240)}
        sw_total = len(swaps); sw_two = sum(1 for x in swaps if x[3] == 'two steps')
        sw_in = Counter(x[4] for x in swaps)
        dur = float(times[idx[-1]] - times[idx[0]])
        mean_cells = ncell_sum / len(idx)
        cell_minutes = mean_cells * dur / 60.0
        new_labels = counts['birth'] + counts['split'] + counts['relabel'] + sum(
            int(p.split()[1]) * v for p, v in clumps.items())
        tau_little = mean_cells * dur / new_labels if new_labels else None
        new_labels_p = new_labels - sm_flick          # new cells that do not merge straight back into their parent
        tau_little_p = mean_cells * dur / new_labels_p if new_labels_p > 0 else None
        complete = [last_seen[c] - first_seen[c] for c in first_seen if first_seen[c] > 0 and last_seen[c] < len(idx) - 1]
        dts = s * float(np.median(np.diff(times)))
        persistent = sw_total - 2 * flick
        r = dict(step=s, dt_s=dts, frames=len(idx), duration_s=dur, mean_cells=mean_cells, counts=dict(counts),
                 clump_patterns=dict(clumps.most_common(12)), n_clumps=sum(clumps.values()),
                 swaps_logger=counts['swap'], swaps_elementary=sw_total, swaps_two_step=sw_two, swaps_by_event_type=dict(sw_in),
                 swap_flicker_pairs=flick, swaps_persistent=persistent, swaps_persistent_by_W=persistent_by_W, lost_unmatched=len(pend_lost), gained_unmatched=unmatched_gain,
                 frames_failing_logger_check=nfail, frames_torus_euler_bad=euler_bad, frames_odd_segment_parity=odd_frames,
                 junction_degrees=dict(jdeg), balance_failures=bad_bal, neg_control_caught=neg,
                 rate_per_cell_per_min=dict(swaps_elementary=sw_total / cell_minutes, swaps_persistent=persistent / cell_minutes,
                                            splits=counts['split'] / cell_minutes, splits_persistent=splits_persistent / cell_minutes,
                                            merges_persistent=merges_persistent / cell_minutes, births=counts['birth'] / cell_minutes,
                                            merges=counts['merge'] / cell_minutes, deaths=counts['death'] / cell_minutes,
                                            clumps=sum(clumps.values()) / cell_minutes),
                 lifetime_little_s=tau_little, lifetime_little_persistent_s=tau_little_p,
                 lifetime_complete_tracks=dict(n=len(complete), mean_s=float(np.mean(complete) * dts) if complete else None,
                                               median_s=float(np.median(complete) * dts) if complete else None),
                 swaps_per_split=persistent / splits_persistent if splits_persistent > 0 else None,
                 swaps_per_split_raw=persistent / counts['split'] if counts['split'] else None,
                 split_flicker=sm_flick, splits_persistent=splits_persistent, merges_persistent=merges_persistent, deaths_persistent=deaths_persistent,
                 splits_persistent_by_W=splits_persistent_by_W,
                 swaps_per_birth=persistent / counts['birth'] if counts['birth'] else None,
                 swaps_per_new_cell=persistent / new_labels_p if new_labels_p > 0 else None,
                 swaps_per_cell_lifetime=(persistent / cell_minutes) * (tau_little_p / 60.0) if tau_little_p else None)
        assert len(swap_sh) == len(swaps)
        r['swap_list'] = [[t, sorted(int(c) for c in lo), sorted(int(c) for c in ga), int(how == 'two steps'), round(float(x), 4)]
                          for (t, lo, ga, how, typ), x in zip(swaps, swap_sh)]
        npair = len(idx) - 1
        r['centroid'] = dict(frame_pairs=npair, msd_px2_all=sum(d2_all) / max(1, sum(n for _, _, n in d2_cont)),
                             msd_px2_share05=sum(a for a, _, _ in d2_cont) / max(1, sum(m for _, m, _ in d2_cont)),
                             kept_share05_frac=sum(m for _, m, _ in d2_cont) / max(1, sum(n for _, _, n in d2_cont)),
                             median_share=float(np.median(jac_med)) if jac_med else None, L_px=L)
        r['swaps_touching_one_cell_per_lifetime'] = 4 * r['swaps_per_cell_lifetime'] if r['swaps_per_cell_lifetime'] else None
        res['steps'][str(s)] = r
    res['wall_s'] = time.time() - t0
    json.dump(res, open(out, 'w'), indent=1, default=float)
    ok = all(v['balance_failures'] == 0 and v['neg_control_caught'] in (True, None) for v in res['steps'].values())
    return res, ok


if __name__ == '__main__':
    data, run, var, dz, sigma, h, steps, W, out = sys.argv[1:10]
    nf = int(sys.argv[10]) if len(sys.argv) > 10 and sys.argv[10] != 'all' else None
    method, hv = h.split(':') if ':' in h else ('hmax', h)
    res, ok = run_config(data, run, var, float(dz) if '.' in dz else dz, float(sigma), float(hv), [int(x) for x in steps.split(',')],
                         float(W), out, nf, method)
    for s, r in res['steps'].items():
        print('STEP', s, json.dumps({k: r[k] for k in ('dt_s', 'mean_cells', 'counts', 'swaps_elementary', 'swaps_two_step', 'swaps_persistent', 'lost_unmatched', 'gained_unmatched', 'frames_torus_euler_bad',
                                                       'balance_failures', 'neg_control_caught', 'lifetime_little_s', 'swaps_per_split')}))
    print('CELLS', json.dumps(res['cells'])[:600])
    print('CENSUS_OK' if ok else 'CENSUS_FAIL', flush=True)
