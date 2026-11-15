"""Event census of a cell tiling seen from a geostationary satellite: open-cell convection or sea-ice floes.

Adapter to the shared event logger (studies/2026-11-15-event-logger/scripts/eventlog.py, imported unchanged). The neighbour
graph (junction blocks, segments per pair) and the mutual-best-overlap matching are those of the Sun stream
(studies/2026-11-15-sun-granulation/scripts/tiles.py: graph, match; imported unchanged). The elementary-swap rule and the
flicker rule follow the Sun stream's census.py (re-written here for an open patch).

Cell rules (fixed before counting):
  open : open-cell convection. Cells = cloud-free centres with their share of the cloud walls: basins of a marker watershed on
         the smoothed albedo; markers = regional minima of depth >= h (h-minima, albedo units). Every pixel belongs to a cell;
         boundaries run along the bright walls.
  floe : sea ice. Floes = connected regions of albedo > h with at least AMIN pixels. Floes do not tile (open water between),
         so each floe's ZONE OF INFLUENCE is its cell: the watershed of the distance to the nearest floe, seeded by the floes
         (the skeleton by influence zones, SKIZ = the Voronoi diagram of the floes as sets). Leads and open water are cut by the
         median lines between floes.
Open patch: the box is ringed by one OUTSIDE cell (label 0), so box + outside = a sphere, Euler V - E + F = 2 per frame.
Box tracking: the box follows the mean drift, measured between consecutive frames by phase correlation of the box contents
(scikit-image phase_cross_correlation, integer pixels). Interior events: no cell of the event is the outside cell or touches it
before or after (only cells wholly inside the box are counted).
Persistence: a swap undone by the reverse swap of the same four cells within W minutes is flicker (both removed); a cell split
off and merged back (or dying) within W minutes is flicker. Counts are reported for every W and every time step.

Usage: cellcensus.py DATA_DIR MODE SIGMA H STEPS(comma) WLIST(comma, minutes) BOX(px) R0 C0 OUT.json [NFRAMES|all] [AMIN]"""
import sys, os, json, itertools, time
from collections import Counter, defaultdict
import numpy as np
from scipy import ndimage as ndi
from skimage.segmentation import watershed
from skimage.morphology import h_minima
from skimage.registration import phase_cross_correlation
HERE = os.path.dirname(os.path.abspath(__file__))
ST = os.path.join(HERE, '..', '..')
sys.path.insert(0, os.path.join(ST, '2026-11-15-event-logger', 'scripts'))
sys.path.insert(0, os.path.join(ST, '2026-11-15-sun-granulation', 'scripts'))
import eventlog as EL
import tiles as TL


def segment(img, mode, sigma, h, amin=4):
    f = np.nan_to_num(img.astype(np.float64), nan=np.nanmean(img))
    f = ndi.gaussian_filter(f, sigma) if sigma > 0 else f
    if mode == 'open':
        mk, _ = ndi.label(h_minima(f, h))
        lab = watershed(f, mk, connectivity=1)
    else:
        m = f > h
        mk, n = ndi.label(m)
        sz = np.bincount(mk.ravel()); small = sz < amin; small[0] = False; mk[small[mk]] = 0
        if mk.max() == 0: return None
        d = ndi.distance_transform_edt(mk == 0)
        lab = watershed(d, mk, connectivity=1)
    u, inv = np.unique(lab, return_inverse=True)
    return (inv.reshape(lab.shape) + 1).astype(np.int64)


def pad0(lab):
    return np.pad(lab, 1, constant_values=0)


def tiling(lab, G, t, parents=None):
    cells = [str(c) for c in np.unique(lab)]
    bnd = [[str(a), str(b)] for (a, b), k in G['segs'].items() for _ in range(k)]
    jn = [[str(c) for c in cs] for cs, _ in G['junctions']]
    par = {str(k): {str(a): s for a, s in v.items()} for k, v in (parents or {}).items()}
    return EL.Tiling(cells, bnd, jn, 2, 'sphere', t, loops=G['loops'], parents=par)


def track_boxes(F, box, r0, c0, idx):
    """Box origin per frame index in idx, following the drift (phase correlation of the box contents, frame to frame)."""
    H, W = F.shape[1:]
    pos = {idx[0]: (r0, c0)}; r, c = float(r0), float(c0); drift = []
    for a, b in zip(idx, idx[1:]):
        ri, ci = int(round(r)), int(round(c))
        A = np.nan_to_num(F[a, ri:ri + box, ci:ci + box]); B = np.nan_to_num(F[b, ri:ri + box, ci:ci + box])
        sh, _, _ = phase_cross_correlation(A, B)
        r -= sh[0]; c -= sh[1]; drift.append((float(-sh[0]), float(-sh[1])))
        r = min(max(r, 0), H - box); c = min(max(c, 0), W - box)
        pos[b] = (int(round(r)), int(round(c)))
    return pos, drift


def census(F, times, mode, sigma, h, steps, Ws, box, r0, c0, amin=4):
    res = {}
    for s in steps:
        idx = list(range(0, len(F), s))
        pos, drift = track_boxes(F, box, r0, c0, idx)
        prev = None; next_id = 1; counts = Counter(); counts_all = Counter(); clumps = Counter()
        bad_euler = bad_tri = bad_bal = 0; neg = None; jdeg = Counter(); nint = []; pn = Counter()
        swaps = []; pend = []; splits_l = []; merges_l = []; gained_unmatched = 0; hist = []
        for q, k in enumerate(idx):
            ri, ci = pos[k]
            raw = segment(F[k, ri:ri + box, ci:ci + box], mode, sigma, h, amin)
            if raw is None: raw = np.ones((box, box), np.int64)
            raw = pad0(raw)
            if prev is None:
                lab = raw; next_id = int(lab.max()) + 1; par = her = {}
            else:
                lab, par, her, next_id = TL.match(prev_lab, raw, next_id)
            G = TL.graph(lab)
            T = tiling(lab, G, float(times[k]), par)
            if prev is not None:
                prev.heirs = {str(a): {str(b): v for b, v in d.items()} for a, d in her.items()}
            c = EL.check_tiling(T)
            if not c.get('euler_ok', False): bad_euler += 1
            if c.get('triple_formulas_ok') is False: bad_tri += 1
            jdeg.update(len(cs) for cs, _ in G['junctions'])
            border = set(T.nb['0']) | {'0'}
            inner = [x for x in T.cells if x not in border]
            nint.append(len(inner))
            if q % 4 == 0: pn.update(len(T.nb[x]) for x in inner)
            if prev is not None:
                ev = EL.classify(prev, T)
                ok, _, _ = EL.balance(prev, T, ev)
                if not ok: bad_bal += 1
                if neg is None and any(e['net'] for e in ev):
                    badl = [dict(e) for e in ev]; i = next(i for i, e in enumerate(badl) if e['net']); badl[i]['type'] = 'swap'
                    neg = not EL.balance(prev, T, badl)[0]
                pborder = set(prev.nb['0']) | {'0'}
                tm = float(times[k])
                for e in ev:
                    counts_all[e['type']] += 1
                    cs = e['cells']
                    if any(x in border or x in pborder for x in cs): continue
                    counts[e['type']] += 1
                    if e['type'] == 'clump': clumps[e['pattern']] += 1
                    if e['type'] == 'split':
                        x = next(y for y in cs if y not in prev.cells)
                        pp = T.parents.get(x, {}); splits_l.append((tm, x, max(pp, key=pp.get) if pp else None))
                    if e['type'] in ('merge', 'death'):
                        y = next(z for z in cs if z not in T.cells)
                        hh = prev.heirs.get(y, {}); merges_l.append((tm, y, max(hh, key=hh.get) if hh else None, e['type']))
                    scs = sorted(cs)
                    lost = [p for p in itertools.combinations(scs, 2) if p in prev.pairs and p not in T.pairs]
                    gained = [p for p in itertools.combinations(scs, 2) if p in T.pairs and p not in prev.pairs]
                    used = set(); clean = e['net'] == 0 and all(x in prev.cells and x in T.cells for x in cs)
                    for l in lost:
                        cn = prev.nb[l[0]] & prev.nb[l[1]]
                        g = next((g for g in gained if g not in used and set(g) <= cn and set(l) <= (T.nb[g[0]] & T.nb[g[1]])), None)
                        if g is not None: used.add(g); swaps.append((tm, frozenset(l), frozenset(g), 1))
                        elif clean: pend.append((tm, l, cn))
                    for g in gained:
                        if g in used or not clean: continue
                        j = next((j for j, (tl, l, cn) in enumerate(pend) if tm - tl <= max(Ws) + 1e-6 and set(g) <= cn
                                  and set(l) <= (T.nb[g[0]] & T.nb[g[1]])), None)
                        if j is not None:
                            tl, l, cn = pend.pop(j); swaps.append((tm, frozenset(l), frozenset(g), 2))
                        else: gained_unmatched += 1
            hist.append((float(times[k]), T.pairs))
            prev, prev_lab = T, lab
            print(f'PROGRESS {(steps.index(s) + (q + 1) / len(idx)) / len(steps):.3f} step {s} frame {q + 1}/{len(idx)}', flush=True)

        def flicker(Wf):
            open_, fl = {}, 0
            for tm, lo, ga, _ in swaps:
                if (ga, lo) in open_ and tm - open_[(ga, lo)] <= Wf + 1e-6: fl += 1; del open_[(ga, lo)]
                else: open_[(lo, ga)] = tm
            return fl

        def split_flicker(Wf):
            born = {x: (tm, p) for tm, x, p in splits_l}
            return sum(1 for tm, y, hr, ty in merges_l if y in born and tm - born[y][0] <= Wf + 1e-6 and (ty == 'death' or hr == born[y][1]))
        dur_h = float(times[idx[-1]] - times[idx[0]]) / 60.0
        mc = float(np.mean(nint)); cell_h = mc * dur_h
        new_raw = counts['birth'] + counts['split']
        per_W = {}
        for Wf in Ws:
            ps = len(swaps) - 2 * flicker(Wf); sf = split_flicker(Wf); newp = new_raw - sf
            per_W[str(Wf)] = dict(swaps_persistent=ps, split_flicker=sf, new_cells_persistent=newp,
                                  swaps_per_new_cell=ps / newp if newp > 0 else None,
                                  swaps_per_cell_hour=ps / cell_h if cell_h else None)
        # two-sided persistence (as in the Earth stream): a swap counts when its new contact holds in every frame of the next P
        # minutes and its old contact held in every frame of the previous P minutes; swaps closer than P to either end of the
        # record cannot be judged and are left out (with the cell-hours of those ends)
        t_first, t_last = hist[0][0], hist[-1][0]
        two_sided = {}
        for P in Ws:
            ev_n = ok_n = 0
            for tm, lo, ga, _ in swaps:
                if tm - P < t_first - 1e-6 or tm + P > t_last + 1e-6: continue
                ev_n += 1
                lo_t, ga_t = tuple(sorted(lo)), tuple(sorted(ga))
                if all(ga_t in pr for t_, pr in hist if tm <= t_ <= tm + P + 1e-6) and \
                   all(lo_t in pr for t_, pr in hist if tm - P - 1e-6 <= t_ < tm): ok_n += 1
            span_h = max(t_last - t_first - 2 * P, 0) / 60.0
            two_sided[str(P)] = dict(judged=ev_n, persistent=ok_n, per_cell_hour=ok_n / (mc * span_h) if span_h > 0 and mc else None)
        tot = sum(pn.values())
        mean_n = sum(k * v for k, v in pn.items()) / tot if tot else None
        mu2 = sum((k - mean_n) ** 2 * v for k, v in pn.items()) / tot if tot else None
        dt_min = float(np.median(np.diff([times[k] for k in idx]))) if len(idx) > 1 else None
        dr = np.array(drift) if drift else np.zeros((1, 2))
        res[str(s)] = dict(step=s, dt_min=dt_min, frames=len(idx), duration_h=dur_h, mean_interior_cells=mc,
                           drift_px_per_step_mean=[float(dr[:, 0].mean()), float(dr[:, 1].mean())],
                           counts_interior=dict(counts), counts_all=dict(counts_all), clump_patterns=dict(clumps.most_common(8)),
                           swaps_elementary=len(swaps), swaps_two_step=sum(1 for x in swaps if x[3] == 2),
                           gained_unmatched=gained_unmatched, lost_unmatched=len(pend), by_W=per_W, two_sided=two_sided,
                           frames_euler_bad=bad_euler, frames_triple_bad=bad_tri, junction_degrees=dict(jdeg),
                           balance_failures=bad_bal, neg_control_caught=neg,
                           p_n={int(k): v / tot for k, v in sorted(pn.items())} if tot else {}, mean_n_interior=mean_n, mu2=mu2)
    return res


if __name__ == '__main__':
    d, mode, sigma, h, steps, Ws, box, r0, c0, out = sys.argv[1:11]
    nf = sys.argv[11] if len(sys.argv) > 11 else 'all'
    amin = int(sys.argv[12]) if len(sys.argv) > 12 else 4
    t0 = time.time()
    F = np.load(os.path.join(d, 'frames.npy'), mmap_mode='r'); times = np.load(os.path.join(d, 'times.npy'))
    if nf != 'all': F = F[:int(nf)]; times = times[:int(nf)]
    steps = [int(x) for x in steps.split(',')]; Ws = [float(x) for x in Ws.split(',')]
    res = census(np.asarray(F), times, mode, float(sigma), float(h), steps, Ws, int(box), int(r0), int(c0), amin)
    out_d = dict(data=d, mode=mode, sigma=float(sigma), h=float(h), box=int(box), r0=int(r0), c0=int(c0), amin=amin,
                 frames=len(F), steps=res, wall_s=time.time() - t0)
    json.dump(out_d, open(out, 'w'), indent=1, default=float)
    ok = all(v['balance_failures'] == 0 and v['neg_control_caught'] in (True, None) for v in res.values())
    for s, r in res.items():
        print('STEP', s, json.dumps({k: r[k] for k in ('dt_min', 'mean_interior_cells', 'counts_interior', 'swaps_elementary', 'by_W', 'two_sided',
                                                       'frames_euler_bad', 'frames_triple_bad', 'balance_failures', 'neg_control_caught',
                                                       'mean_n_interior', 'drift_px_per_step_mean')}, default=float))
    print('CENSUS_OK' if ok else 'CENSUS_FAIL', flush=True)
