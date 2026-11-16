"""Granule tubes in space-time: prisms or scutoids (README section "Granule tubes in space-time: prisms and scutoids", 16 Nov 2026;
DICTO: "on the sun skeleton render I think the dark patches are more like scutoid shapes").

Reading DICTO confirmed: the dark patches of the 10-minute lane stack are shadows of each granule's history, its TUBE through space-time
(x, y, t). A tube that keeps the same neighbours all its life is a PRISM in space-time; one whose neighbours change along t is a
SCUTOID in space-time, with extra corners on its lateral surface at the moments of change. Time plays the apico-basal role of the
epithelial scutoid (the scutoid: Gomez-Galvez et al. 2018, Nature Communications 9, 2960).

Tubes. Sun: the census cells of every frame (tiles.segment, threshold 0.25, smoothing 1.5, as census.py) on the full 24 x 24 Mm
periodic box, labelled through time by the census overlap rule (mutual largest overlap; tiles.match), optionally with a tracking
tolerance f: a mutual-best link is kept only if the overlap is at least f times the larger of the two areas. A tube is one label;
it is used when it does not touch the first or last frame (the box is periodic, so no tube touches a side).
Neighbours along t. For each tube c and each other tube n, the contact series s(t) = 1 when c and n share a pixel edge in frame t,
over c's life. Runs of contact or of no contact shorter than 60 s are flicker: contact runs shorter than 60 s are removed first,
then gaps shorter than 60 s are filled (the same 60 s as the persistence rule of census.py; at a step of 60 s or more nothing is
removed). PRISM: every filtered series is constant over c's life. SCUTOID: otherwise. Each switch of a filtered series is a
neighbour change, typed "between living tubes" (n exists from 60 s before to 60 s after the switch) or "birth or death" (n starts or
ends within 60 s of it).
Extra corners (geometry, no filter). Corner windows: 2 x 2 x 2 voxels (two frames, 2 x 2 pixels) holding four or more distinct
tubes, joined into corners by 26-connectivity (as spacetime_tilt.py). A corner is LATERAL to tube c when c is one of its tubes and
the corner's frames do not include c's first or last frame (so the caps, where a tube starts or ends, are left out). Typed: a
swap-type corner when no tube of the corner has its first or last frame among the corner's frames (+-1 frame), otherwise a birth or
death corner (a tube starts or ends there: the 1-3 and 3-1 corners, or a split or merge of the tracking).

Nulls. Space-time Poisson-Voronoi (spacetime_tilt.block_pv, the Part A yardstick blocks): every cell is a convex polytope; seen
along t it has one lowest and one highest corner, and every other corner of it is lateral (at a corner of index 1, 2 or 3 the cell
gains or loses a neighbour), so the exact scutoid share is 1 and the exact number of lateral corners of a cell is (its corners) - 2;
in the bulk this averages 2 k - 6 = 25.07 (k = 15.535 faces per cell), of which 2 k - 12 = 19.07 are swap corners and 6 are
neighbour births and deaths. Computed exactly per cell from the Delaunay tetrahedra and compared with the voxel pipeline.
Moving Voronoi (500 seeds on the paths of control_voronoi.py, full periodic box): no cell is born or dies, so tubes are cut into
windows of 3, 5 and 10 min; a window is a prism when the seed's Delaunay neighbour set does not change in it; exact from the
periodic Delaunay triangulation at every frame (10 s), against the voxel pipeline.

Usage:
  spacetime_scutoids.py sun SEG OUT.json [step=S] [order=real|shuf:SEED] [rev=1] [tol=F] [tag=NAME]
  spacetime_scutoids.py pv SEED VC OUT.json
  spacetime_scutoids.py mv SEED OUT.json
  spacetime_scutoids.py fig STUDYDIR SEG
Data credit: Bifrost code, Gudiksen et al. 2011, A&A 531, A154; runs en024048_hion and qs024048_by3363, Carlsson, Hansteen,
Gudiksen, Leenaarts & De Pontieu 2016, A&A 585, A4; Hinode Science Data Centre Europe (sdc.uio.no). Labelling and connectivity:
scipy.ndimage; Delaunay: scipy.spatial (Qhull, Barber, Dobkin & Huhdanpaa 1996)."""
import sys, os, json, time
import numpy as np
from collections import Counter, defaultdict
from scipy import ndimage as ndi
from scipy.stats import spearmanr
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tiles as TL

DT, DX = 10.0, 24000.0 / 504
LIFE_MIN = 180.0                     # s: tubes of 3 min or more are the main sample (3 frames even at an 80 s step)
FLICK = 60.0                         # s
BINS = [(0, 180), (180, 360), (360, 600), (600, 1e9)]


def order_of(order, n):
    if order == 'real': return np.arange(n)
    return np.random.default_rng(int(order.split(':')[1])).permutation(n)


def match_tol(prev, lab, nid, tol):
    """tiles.match (mutual largest overlap), with a tolerance: the link is kept only if overlap >= tol * max(area old, area new)."""
    K = np.int64(lab.max() + 1)
    u, cnt = np.unique(prev.astype(np.int64) * K + lab, return_counts=True)
    old, new = u // K, u % K
    ao = np.bincount(prev.ravel()); an = np.bincount(lab.ravel())
    o_s = np.lexsort((-cnt, new)); first_n = np.r_[True, new[o_s][1:] != new[o_s][:-1]]
    bp = dict(zip(new[o_s][first_n].tolist(), zip(old[o_s][first_n].tolist(), cnt[o_s][first_n].tolist())))
    o_s2 = np.lexsort((-cnt, old)); first_o = np.r_[True, old[o_s2][1:] != old[o_s2][:-1]]
    bh = dict(zip(old[o_s2][first_o].tolist(), new[o_s2][first_o].tolist()))
    lut = np.zeros(K, np.int64)
    for n in np.flatnonzero(an).tolist():
        o, c = bp[n]
        if bh[o] == n and c >= tol * max(ao[o], an[n]): lut[n] = o
        else: lut[n] = nid; nid += 1
    return lut[lab], nid


def track(seg, step, order, rev, tol):
    S = np.load(seg, mmap_mode='r')
    idx = order_of(order, S.shape[0])[::step]
    if rev: idx = idx[::-1]
    L = np.empty((len(idx),) + S.shape[1:], np.int32); prev, nid = None, 1
    for k, j in enumerate(idx):
        raw = np.asarray(S[j]).astype(np.int64)
        if prev is None:
            lab = raw.copy(); nid = int(raw.max()) + 1
        else:
            lab, nid = match_tol(prev, raw, nid, tol)
        prev = lab; L[k] = lab
    u, inv = np.unique(L, return_inverse=True)
    return (inv.reshape(L.shape) + 1).astype(np.int32)


def frame_pairs(F, periodic):
    if periodic:
        R = np.roll(F, -1, 1); D = np.roll(F, -1, 0); A1, B1, A2, B2 = F, R, F, D
    else:
        A1, B1, A2, B2 = F[:, :-1], F[:, 1:], F[:-1, :], F[1:, :]
    a = np.concatenate([A1[A1 != B1], A2[A2 != B2]]).astype(np.int64)
    b = np.concatenate([B1[A1 != B1], B2[A2 != B2]]).astype(np.int64)
    lo, hi = np.minimum(a, b), np.maximum(a, b)
    return np.unique(lo * (1 << 32) + hi)


def filt(s, dt):
    """Remove contact runs shorter than 60 s, then fill gaps shorter than 60 s (time-symmetric)."""
    s = s.copy()
    for val in (1, 0):
        n = len(s); i = 0
        while i < n:
            j = i
            while j < n and s[j] == s[i]: j += 1
            if s[i] == val and (j - i) * dt < FLICK - 1e-9: s[i:j] = 1 - val
            i = j
    return s


def corners3d(L, periodic):
    """Corner windows (2 x 2 x 2, >= 4 distinct tubes), clustered (26-connectivity): per corner its frame range and tubes."""
    nt = L.shape[0]
    shp = L.shape[1:] if periodic else (L.shape[1] - 1, L.shape[2] - 1)
    mask = np.zeros((nt - 1,) + shp, bool); simple = np.zeros(mask.shape, bool)
    def shifts(F):
        if periodic:
            return [F, np.roll(F, -1, 1), np.roll(F, -1, 0), np.roll(np.roll(F, -1, 0), -1, 1)]
        return [F[:-1, :-1], F[:-1, 1:], F[1:, :-1], F[1:, 1:]]
    prevs = shifts(L[0])
    for a in range(nt - 1):
        nxt = shifts(L[a + 1])
        W = np.stack(prevs + nxt, -1); W.sort(-1); nd = 1 + (np.diff(W, axis=-1) != 0).sum(-1)
        mask[a] = nd >= 4; simple[a] = nd == 4
        prevs = nxt
    if mask.sum() > 2e7:              # shuffled frames: nearly every lane voxel is a corner window; corners are not counted
        print('CORNERS skipped: corner windows', int(mask.sum()), flush=True)
        return [], int(mask.sum()), -1
    cl, ncl = ndi.label(mask, structure=np.ones((3, 3, 3)))
    if ncl == 0: return [], 0, 0
    pos = np.nonzero(mask); cid = cl[pos]
    labs = []
    for dt_ in (0, 1):
        for dy in (0, 1):
            for dx in (0, 1):
                yy = pos[1] + dy; xx = pos[2] + dx
                if periodic: yy %= L.shape[1]; xx %= L.shape[2]
                labs.append(L[pos[0] + dt_, yy, xx])
    labs = np.stack(labs, 1)
    key = np.unique(np.repeat(cid.astype(np.int64), 8) * (1 << 32) + labs.ravel().astype(np.int64))
    pairs = np.stack([key >> 32, key & ((1 << 32) - 1)], 1)
    a0 = ndi.minimum(pos[0], cid, np.arange(1, ncl + 1)); a1 = ndi.maximum(pos[0], cid, np.arange(1, ncl + 1))
    cyx = np.array(ndi.center_of_mass(mask, cl, np.arange(1, ncl + 1)))
    tubes = defaultdict(list)
    for c, l in pairs.tolist(): tubes[c].append(l)
    out = [(int(a0[c - 1]), int(a1[c - 1]), tubes[c], (float(cyx[c - 1, 1]) + 0.5, float(cyx[c - 1, 2]) + 0.5)) for c in range(1, ncl + 1)]
    return out, int(mask.sum()), int(sum(1 for o in out if len(o[2]) == 4))



def analyse(L, dt, periodic, keep_events=False, include_cut=False):
    """Per-tube records. L: (nt, Y, X) labels."""
    nt = L.shape[0]
    objs = ndi.find_objects(L)
    f0 = np.full(len(objs) + 1, -1); f1 = np.full(len(objs) + 1, -1); side = np.zeros(len(objs) + 1, bool)
    for lab, sl in enumerate(objs, 1):
        if sl is None: continue
        f0[lab], f1[lab] = sl[0].start, sl[0].stop - 1
        if not periodic: side[lab] = sl[1].start == 0 or sl[2].start == 0 or sl[1].stop == L.shape[1] or sl[2].stop == L.shape[2]
    area = np.zeros(len(objs) + 1); cy = np.zeros(len(objs) + 1); cx = np.zeros(len(objs) + 1); nfr = np.zeros(len(objs) + 1)
    pk, pf = [], []
    for k in range(nt):
        F = L[k]
        a = np.bincount(F.ravel(), minlength=len(objs) + 1); area += a
        p = frame_pairs(F, periodic); pk.append(p); pf.append(np.full(len(p), k, np.int32))
    pk = np.concatenate(pk); pf = np.concatenate(pf)
    o = np.lexsort((pf, pk)); pk, pf = pk[o], pf[o]
    life_fr = f1 - f0 + 1
    w60 = max(1, int(np.ceil(FLICK / dt - 1e-9)))
    cutm = (f0 == 0) | (f1 == nt - 1)
    want = np.flatnonzero((f0 >= 0) & ~side & (include_cut | ~cutm))
    want_set = set(want.tolist())
    mid = {lab: (int(f0[lab]) + int(f1[lab])) // 2 for lab in want.tolist()}
    # mid-life centroid (for quadrant and figure): one pass per frame over the tubes whose mid frame it is
    bymid = defaultdict(list)
    for lab, km in mid.items(): bymid[km].append(lab)
    for km, labs in bymid.items():
        F = L[km]
        m = np.isin(F, labs)
        fl = F[m]; ii = np.flatnonzero(m.ravel())
        Y, X = ii // F.shape[1], ii % F.shape[1]
        if periodic:   # circular mean
            for arr, out_, n_ in ((Y, cy, F.shape[0]), (X, cx, F.shape[1])):
                ang = 2 * np.pi * arr / n_
                s_ = np.bincount(fl, np.sin(ang), minlength=len(out_)); c_ = np.bincount(fl, np.cos(ang), minlength=len(out_))
                for lab in labs: out_[lab] = (np.arctan2(s_[lab], c_[lab]) % (2 * np.pi)) * n_ / (2 * np.pi)
        else:
            cnt = np.bincount(fl, minlength=len(cy))
            sy = np.bincount(fl, Y, minlength=len(cy)); sx = np.bincount(fl, X, minlength=len(cy))
            for lab in labs: cy[lab] = sy[lab] / cnt[lab]; cx[lab] = sx[lab] / cnt[lab]
    # contact series per (tube, neighbour)
    a_ = pk >> 32; b_ = pk & ((1 << 32) - 1)
    brk = np.flatnonzero(np.r_[True, pk[1:] != pk[:-1], True])
    series = defaultdict(dict)
    for i in range(len(brk) - 1):
        s, e = brk[i], brk[i + 1]
        A, B = int(a_[s]), int(b_[s]); fr = pf[s:e]
        if A in want_set: series[A][B] = fr
        if B in want_set: series[B][A] = fr
    alive = lambda n, k0, k1: bool(f0[n] <= k0 and f1[n] >= k1)
    ends_in = lambda n, k0, k1: bool(k0 <= f0[n] <= k1 or k0 <= f1[n] <= k1)
    recs = {}
    for lab in want.tolist():
        F0, F1 = int(f0[lab]), int(f1[lab]); n = F1 - F0 + 1
        sw_all, sw_live, sw_bd, nbs, ev = 0, 0, 0, 0, []
        for nbr, fr in series.get(lab, {}).items():
            s = np.zeros(n, np.int8); s[fr - F0] = 1
            s = filt(s, dt)
            if s.any(): nbs += 1
            d = np.flatnonzero(np.diff(s) != 0)
            for i in d.tolist():
                kk = F0 + i                       # switch between frames kk and kk + 1
                live = alive(nbr, kk + 1 - w60, kk + w60)
                sw_all += 1; sw_live += live; sw_bd += (not live)
                if keep_events: ev.append(('s', kk, int(live), nbr))
        recs[lab] = dict(cut=bool(cutm[lab]), f0=F0, f1=F1, life_s=n * dt, area_Mm2=float(area[lab] / n * (DX / 1000) ** 2), cy=float(cy[lab]), cx=float(cx[lab]),
                         neighbours=nbs, changes=sw_all, changes_live=sw_live, changes_bd=sw_bd, corners=0, corners_live=0, corners_bd=0,
                         **({'events': ev} if keep_events else {}))
    cors, nwin, nsimple = corners3d(L, periodic)
    for a0, a1, tubes, yx in cors:
        # swap-type corner: no tube of the corner starts or ends at it (first or last frame within the corner's frames, +-1)
        live = not any(ends_in(t, a0 - 1, a1 + 2) for t in tubes)
        for t in tubes:
            r = recs.get(t)
            if r is None: continue
            if a0 >= r['f0'] + 1 and a1 + 1 <= r['f1'] - 1:       # lateral: away from the tube's own first and last frame
                r['corners'] += 1; r['corners_live'] += live; r['corners_bd'] += (not live)
                if keep_events: r['events'].append(('c', a0, int(live), [int(x) for x in tubes], yx))
    return recs, dict(corner_windows=nwin, corners=len(cors), corners_simple=nsimple, frames=nt, tubes_total=int((f0 >= 0).sum()))


def summarise(recs, dt, extra=None):
    cutr = [r for r in recs.values() if r.get('cut')]
    R = [r for r in recs.values() if not r.get('cut')]
    main = [r for r in R if r['life_s'] >= LIFE_MIN - 1e-9]
    def share(rs, key='changes'):
        return float(np.mean([r[key] > 0 for r in rs])) if rs else None
    out = dict(step_s=dt, tubes=len(R), tubes_3min=len(main), tubes_cut_by_block_ends=len(cutr),
               cut_with_a_change_seen=float(np.mean([r['changes'] > 0 for r in cutr])) if cutr else None,
               scutoid_share_3min=share(main), corner_share_3min=share(main, 'corners'),
               scutoid_share_all=share(R), corner_share_all=share(R, 'corners'))
    out['by_life'] = {f'{a / 60:g}-{b / 60:g} min' if b < 1e8 else f'{a / 60:g}+ min': dict(
        n=len(rs), scutoid_share=share(rs), corner_share=share(rs, 'corners'),
        changes_mean=float(np.mean([r['changes'] for r in rs])) if rs else None,
        corners_mean=float(np.mean([r['corners'] for r in rs])) if rs else None)
        for a, b in BINS for rs in [[r for r in R if a <= r['life_s'] < b]]}
    if main:
        ar = np.array([r['area_Mm2'] for r in main]); qs = np.quantile(ar, [0.25, 0.5, 0.75])
        out['by_size_3min'] = {lab: dict(n=len(rs), scutoid_share=share(rs), corners_mean=float(np.mean([r['corners'] for r in rs])))
                               for lab, rs in (('Q1 smallest', [r for r in main if r['area_Mm2'] < qs[0]]),
                                               ('Q2', [r for r in main if qs[0] <= r['area_Mm2'] < qs[1]]),
                                               ('Q3', [r for r in main if qs[1] <= r['area_Mm2'] < qs[2]]),
                                               ('Q4 largest', [r for r in main if r['area_Mm2'] >= qs[2]]))}
        out['area_quartiles_Mm2'] = qs.tolist()
        for key in ('changes', 'changes_live', 'changes_bd', 'corners', 'corners_live', 'corners_bd', 'neighbours'):
            v = np.array([r[key] for r in main])
            out[f'{key}_3min'] = dict(mean=float(v.mean()), median=float(np.median(v)),
                                      per_min=float(v.sum() / sum(r['life_s'] for r in main) * 60))
        out['corners_hist_3min'] = {str(k): int(v) for k, v in sorted(Counter(min(r['corners'], 30) for r in main).items())}
        out['changes_hist_3min'] = {str(k): int(v) for k, v in sorted(Counter(min(r['changes'], 30) for r in main).items())}
        life = np.array([r['life_s'] for r in main]); ch = np.array([r['changes'] for r in main]); co = np.array([r['corners'] for r in main])
        out['spearman_3min'] = dict(changes_life=float(spearmanr(ch, life)[0]), corners_life=float(spearmanr(co, life)[0]),
                                    changes_area=float(spearmanr(ch, ar)[0]), corners_area=float(spearmanr(co, ar)[0]),
                                    life_area=float(spearmanr(life, ar)[0]),
                                    rate_area=float(spearmanr(ch / life, ar)[0]))
        out['life_3min'] = dict(mean_min=float(life.mean() / 60), median_min=float(np.median(life) / 60))
        out['prism_life_3min_mean_min'] = float(np.mean([r['life_s'] for r in main if r['changes'] == 0]) / 60) if any(r['changes'] == 0 for r in main) else None
        out['prism_area_3min_mean_Mm2'] = float(np.mean([r['area_Mm2'] for r in main if r['changes'] == 0])) if any(r['changes'] == 0 for r in main) else None
        out['scutoid_area_3min_mean_Mm2'] = float(np.mean([r['area_Mm2'] for r in main if r['changes'] > 0])) if any(r['changes'] > 0 for r in main) else None
    if extra: out.update(extra)
    return out


def quadrant_shares(recs, Y, X):
    q = defaultdict(list)
    for r in recs.values():
        if r['life_s'] >= LIFE_MIN - 1e-9 and not r.get('cut'): q[int(r['cy'] >= Y / 2) * 2 + int(r['cx'] >= X / 2)].append(r['changes'] > 0)
    return {str(k): dict(n=len(v), scutoid_share=float(np.mean(v))) for k, v in sorted(q.items())}


def cmd_sun(seg, outf, opts):
    t0 = time.time()
    o = dict(x.split('=', 1) for x in opts)
    step = int(o.get('step', 1)); order = o.get('order', 'real'); rev = o.get('rev') == '1'; tol = float(o.get('tol', 0))
    L = track(seg, step, order, rev, tol)
    print(f'PROGRESS 0.3 tracked {L.shape} {time.time() - t0:.0f}s', flush=True)
    recs, info = analyse(L, DT * step, True, include_cut=True)
    print(f'PROGRESS 0.9 analysed {time.time() - t0:.0f}s', flush=True)
    res = summarise(recs, DT * step, dict(tag=o.get('tag', ''), seg=os.path.basename(seg), step=step, order=order, rev=rev, tol=tol,
                                          quadrants=quadrant_shares(recs, L.shape[1], L.shape[2]), seconds=round(time.time() - t0, 1), **info))
    json.dump(res, open(outf, 'w'), indent=1)
    json.dump({str(k): {kk: vv for kk, vv in v.items()} for k, v in recs.items()}, open(outf.replace('.json', '_tubes.json'), 'w'))
    print('TUBES ' + json.dumps({k: res[k] for k in ('tag', 'tubes', 'tubes_3min', 'scutoid_share_3min', 'corner_share_3min')}), flush=True)
    print('TUBES_OK', outf, flush=True)


def cmd_pv(seed, vc, outf):
    import spacetime_tilt as ST
    t0 = time.time()
    L, info, ex = ST.block_pv(seed, vc, 242)
    recs, cinfo = analyse(L, DT, False)
    # exact, per interior cell (label = seed index + 1): corners of the cell = Delaunay tetrahedra holding its seed
    C, nb, simp = ex['C'], ex['nb'], ex['simp']; h = C[:, 2]
    ok = (nb >= 0).all(1)
    i = np.where(ok[:, None], h[nb] < h[:, None], False).sum(1)
    born = np.full(len(C), -1); died = np.full(len(C), -1)
    for t in np.flatnonzero(ok & (i == 1)).tolist():
        j = int(np.flatnonzero(h[nb[t]] < h[t])[0]); born[t] = simp[t, j]
    for t in np.flatnonzero(ok & (i == 3)).tolist():
        j = int(np.flatnonzero(h[nb[t]] > h[t])[0]); died[t] = simp[t, j]
    lat, lat_sw, lat_bd, tmin, tmax = Counter(), Counter(), Counter(), {}, {}
    for t, s4 in enumerate(simp.tolist()):
        for s in s4:
            tmin[s] = min(tmin.get(s, 1e18), h[t]); tmax[s] = max(tmax.get(s, -1e18), h[t])
            if born[t] == s or died[t] == s: continue
            lat[s] += 1
            if i[t] == 2: lat_sw[s] += 1
            else: lat_bd[s] += 1
    exact = {}
    for lab, r in recs.items():
        s = lab - 1
        exact[lab] = dict(corners=lat[s], corners_swap=lat_sw[s], corners_bd=lat_bd[s], life_s=(tmax[s] - tmin[s]) / vc)
    E = list(exact.values())
    main = [lab for lab, r in recs.items() if r['life_s'] >= LIFE_MIN - 1e-9]
    ext = dict(exact_scutoid_share=float(np.mean([e['corners'] > 0 for e in E])),
               exact_corners_mean=float(np.mean([e['corners'] for e in E])), exact_corners_swap_mean=float(np.mean([e['corners_swap'] for e in E])),
               exact_corners_bd_mean=float(np.mean([e['corners_bd'] for e in E])),
               exact_corners_mean_3min=float(np.mean([exact[l]['corners'] for l in main])) if main else None,
               pipeline_over_exact_corners_3min=float(sum(recs[l]['corners'] for l in main) / max(1, sum(exact[l]['corners'] for l in main))),
               pipeline_over_exact_changes_3min=float(sum(recs[l]['changes'] for l in main) / max(1, sum(exact[l]['corners'] for l in main))),
               seed=seed, vc=vc, seconds=round(time.time() - t0, 1), **cinfo)
    res = summarise(recs, DT, ext)
    json.dump(res, open(outf, 'w'), indent=1)
    print('TUBES ' + json.dumps({k: res.get(k) for k in ('tubes', 'tubes_3min', 'scutoid_share_3min', 'exact_scutoid_share', 'exact_corners_mean', 'pipeline_over_exact_corners_3min')}), flush=True)
    print('TUBES_OK', outf, flush=True)


def mv_full(seed, nt=242):
    L0, N, speed = 504, 500, 1.0
    rng = np.random.default_rng(seed)
    p0 = rng.uniform(0, L0, (N, 2))
    A = rng.normal(0, 1, (N, 2, 2)); w = rng.uniform(0.002, 0.01, (N, 2, 2)); ph = rng.uniform(0, 2 * np.pi, (N, 2, 2))
    pos = lambda t: (p0 + speed * (A * np.sin(w * t + ph)).sum(2) / np.maximum(w.mean(2), 1e-9) * 0.01) % L0
    from scipy.spatial import cKDTree
    yy, xx = np.indices((L0, L0)); grid = np.stack([yy.ravel(), xx.ravel()], 1) + 0.5
    L = np.empty((nt, L0, L0), np.int32); NBS = []
    for k in range(nt):
        P = pos(DT * k)
        _, idx = cKDTree(P, boxsize=L0).query(grid)
        L[k] = idx.reshape(L0, L0) + 1
        NBS.append(TL.periodic_voronoi_counts(P, L0))
    return L, NBS, N


def cmd_mv(seed, outf):
    t0 = time.time()
    L, NBS, N = mv_full(seed)
    nt = L.shape[0]
    recs, cinfo = analyse_all_tubes(L)
    res = dict(seed=seed, seeds=N, seconds=0, **cinfo)
    for tau_min in (3, 5, 10):
        wl = int(round(tau_min * 60 / DT)); starts = list(range(wl, nt - wl, wl))   # windows away from both block ends
        ex_raw, ex_f, pipe, pipe_c = [], [], [], []
        for s in range(N):
            # exact neighbour series of seed s over the whole block
            nbs = sorted(set().union(*[NBS[k][s] for k in range(nt)]))
            ser = {n: np.array([n in NBS[k][s] for k in range(nt)], np.int8) for n in nbs}
            serf = {n: filt(v, DT) for n, v in ser.items()}
            r = recs[s + 1]
            for a in starts:
                b = a + wl - 1
                ex_raw.append(any((v[a:b + 1] != v[a]).any() for v in ser.values()))
                ex_f.append(any((v[a:b + 1] != v[a]).any() for v in serf.values()))
                pipe.append(any(a <= kk and kk + 1 <= b for kind, kk, *_ in r['events'] if kind == 's'))
                pipe_c.append(any(a <= kk and kk + 1 <= b for kind, kk, *_ in r['events'] if kind == 'c'))
        res[f'window_{tau_min}min'] = dict(windows=len(pipe), exact_scutoid_share=float(np.mean(ex_raw)),
                                           exact_filtered_scutoid_share=float(np.mean(ex_f)), pipeline_scutoid_share=float(np.mean(pipe)),
                                           pipeline_corner_share=float(np.mean(pipe_c)))
        print(f'PROGRESS {0.5 + tau_min / 20:.2f} window {tau_min} min', flush=True)
    # exact flips per seed per minute (each Delaunay flip touches 4 seeds) against pipeline lateral corners per tube per minute
    flips = sum(len({(min(i, j), max(i, j)) for i in range(N) for j in NBS[k][i]} - {(min(i, j), max(i, j)) for i in range(N) for j in NBS[k + 1][i]})
                for k in range(nt - 1))
    res['exact_flips'] = flips; res['exact_seed_changes_per_min'] = 4 * flips / N / ((nt - 1) * DT / 60)
    res['pipeline_corners_per_tube_per_min'] = sum(r['corners'] for r in recs.values()) / N / ((nt - 1) * DT / 60)
    res['pipeline_changes_per_tube_per_min'] = sum(r['changes'] for r in recs.values()) / N / ((nt - 1) * DT / 60)
    res['seconds'] = round(time.time() - t0, 1)
    json.dump(res, open(outf, 'w'), indent=1)
    print('TUBES ' + json.dumps({k: v for k, v in res.items() if k.startswith('window') or k.startswith('exact_seed') or k.startswith('pipeline')}), flush=True)
    print('TUBES_OK', outf, flush=True)


def analyse_all_tubes(L):
    """As analyse(), but every tube is kept (moving Voronoi: every tube spans the block), with its events; laterality margin is
    only from the block ends."""
    nt = L.shape[0]
    Lp = np.concatenate([np.zeros((1,) + L.shape[1:], L.dtype), L, np.zeros((1,) + L.shape[1:], L.dtype)])
    # pad with an empty frame at both ends so that every tube is 'inside'; the pad label 0 is not a tube
    recs, info = analyse(Lp, DT, True, keep_events=True)
    # shift frame indices back by one
    out = {}
    for lab, r in recs.items():
        if lab == 0: continue
        r = dict(r); r['events'] = [(e[0], e[1] - 1) + tuple(e[2:]) for e in r['events']]; out[lab] = r
    return out, info


def cmd_fig(S, seg):
    """Figure: left, the 10-minute lane stack of RENDER-sun-skeleton (same window, colours and ground) with the outline of every
    tracked tube crossing the middle frame (scutoid tubes coloured by their number of lateral extra corners, prisms grey); right, a
    3D view (x, y, t) of the four tubes at one swap corner and two prism tubes nearby, extra corners marked."""
    import pickle
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    from skimage.measure import find_contours, marching_cubes
    FE = pickle.load(open(f'{S}/data/skeleton/feat_en024048_hion_dz0.1.pkl', 'rb'))
    lanes = np.unpackbits(FE['lanes'])[:np.prod(FE['shape'])].reshape(FE['shape'])
    k0, half, X0, X1 = 120, 30, 0, 250
    occ = lanes[k0 - half:k0 + half].mean(0)[X0:X1, X0:X1]
    D_, I_, C_, T_, O_ = [np.array(c) / 255 for c in ((138, 92, 196), (58, 112, 205), (72, 142, 72), (205, 62, 40), (232, 200, 82))]
    GREY = np.array([0.62, 0.62, 0.66])
    bg = np.array([0.06, 0.06, 0.08])
    img = bg + occ[..., None] * (0.55 * I_ + 0.15 - bg)
    cmap = LinearSegmentedColormap.from_list('dicto', [D_, I_, C_, O_, T_])
    L = track(seg, 1, 'real', False, 0.0)
    recs, info = analyse(L, DT, True, keep_events=True, include_cut=True)
    dx = DX / 1000
    cmax = 16; rmax = 2.0
    fig = plt.figure(figsize=(13.0, 7.2), facecolor='#0f0f14')
    ax = fig.add_axes([0.05, 0.2, 0.42, 0.7]); ax.set_facecolor('#0f0f14')
    ax.imshow(img, origin='lower', extent=[X0 * dx, X1 * dx, X0 * dx, X1 * dx], interpolation='nearest')
    F = L[k0]
    shown = Counter()
    FAINT = np.array([0.42, 0.42, 0.5])
    for lab in np.unique(F[X0:X1, X0:X1]).tolist():
        r = recs.get(lab)
        m = F == lab
        sub = m[X0:X1, X0:X1]
        if r is None or not sub.any(): continue
        if m.sum() != sub.sum(): continue                      # tube crosses the panel edge: left out
        sub = ndi.binary_erosion(sub, iterations=1)
        if not sub.any(): continue
        if r['changes'] > 0: col, lw, kind = cmap(min(r['corners'] / (r['life_s'] / 60), rmax) / rmax)[:3], 1.6, 'scutoid'
        elif r['cut']: col, lw, kind = FAINT, 0.7, 'runs past the block, no change seen'
        else: col, lw, kind = GREY, 1.6, 'prism'
        if r['life_s'] < LIFE_MIN and not r['cut']: lw = 0.9
        for c in find_contours(np.pad(sub, 1).astype(float), 0.5):
            ax.plot((c[:, 1] - 1 + 0.5) * dx, (c[:, 0] - 1 + 0.5) * dx, color=col, lw=lw, alpha=0.95)
        shown[kind + (' (cut by the block ends)' if r['cut'] and kind == 'scutoid' else '')] += 1
    ax.set_xlim(X0 * dx, X1 * dx); ax.set_ylim(X0 * dx, X1 * dx)
    for s_ in ax.spines.values(): s_.set_color('#55555f')
    ax.tick_params(colors='#b0b0bb', labelsize=8); ax.set_xlabel('Mm', color='#b0b0bb', fontsize=9); ax.set_ylabel('Mm', color='#b0b0bb', fontsize=9)
    cax = fig.add_axes([0.07, 0.085, 0.27, 0.018])
    cb = plt.colorbar(plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(0, rmax)), cax=cax, orientation='horizontal')
    cb.ax.tick_params(colors='#b0b0bb', labelsize=8); cb.outline.set_edgecolor('#55555f')
    cax.set_title(f'scutoid tubes: lateral extra corners per minute of life', color='#b0b0bb', fontsize=8.5)
    fig.add_artist(plt.Line2D([0.36, 0.385], [0.11, 0.11], color=GREY, lw=2, transform=fig.transFigure))
    fig.text(0.39, 0.11, 'prism tube', color=GREY, fontsize=8.5, va='center')
    fig.add_artist(plt.Line2D([0.36, 0.385], [0.07, 0.07], color=FAINT, lw=1, transform=fig.transFigure))
    fig.text(0.39, 0.07, 'runs past the 40 min,\nno change seen yet', color=FAINT + 0.2, fontsize=7.5, va='center')
    fig.text(0.04, 0.945, 'Granule tubes through space-time: the lanes over 10 min and every tube at the middle minute', color='#e6e6ee', fontsize=10.5)
    # right: a scutoid tube wholly inside the block (3 to 10 min, few corners, so they stay legible) and three of its neighbours that
    # are scutoid tubes of the same kind, near the panel's window; two prism tubes nearby. (Almost every swap corner has a tube that
    # runs past the 40-min block, so the four tubes of one corner cannot all be shown whole.)
    ok = lambda q: q is not None and not q['cut'] and q['changes'] > 0 and LIFE_MIN <= q['life_s'] <= 600 and q['corners'] <= 12
    ok2 = lambda q: q is not None and not q['cut'] and q['changes'] > 0 and q['life_s'] >= 120 and q['corners'] <= 16
    best = None; ncand = Counter()
    for lab, r in recs.items():
        if not ok(r) or not (40 <= r['cy'] < 464 and 40 <= r['cx'] < 464): continue
        nb = sorted({ev[3] for ev in r['events'] if ev[0] == 's' and ok2(recs.get(ev[3]))} |
                    {t for ev in r['events'] if ev[0] == 'c' for t in ev[3] if t != lab and ok2(recs.get(t))})
        ncand[min(len(nb), 3)] += 1
        if not nb: continue
        if len(nb) < 3:     # fill with the nearest other scutoid tubes alive at the same time
            near = sorted([(np.hypot(q['cy'] - r['cy'], q['cx'] - r['cx']), t) for t, q in recs.items()
                           if t != lab and t not in nb and ok2(q) and q['f0'] <= r['f1'] and q['f1'] >= r['f0']])
            nb = nb + [t for _, t in near[:3 - len(nb)]]
        nb = nb[:3]
        km = (r['f0'] + r['f1']) // 2
        sc = abs(km - k0) / 12 + (0 if (10 <= r['cy'] < 240 and 10 <= r['cx'] < 240) else 8) - 6 * min(3, len(nb)) + \
            sum(np.hypot(recs[t]['cy'] - r['cy'], recs[t]['cx'] - r['cx']) for t in nb) / 15 - 0.5 * sum(recs[t]['corners_live'] for t in nb + [lab])
        if best is None or sc < best[0]: best = (sc, [lab] + nb)
    print('FIG candidate tubes by touching scutoid neighbours (3 = 3 or more)', dict(ncand), flush=True)
    group = best[1]; r0 = recs[group[0]]; cy, cx = r0['cy'], r0['cx']; tc = (r0['f0'] + r0['f1']) // 2
    prisms = sorted([(np.hypot(r['cy'] - cy, r['cx'] - cx), lab) for lab, r in recs.items()
                     if not r['cut'] and r['changes'] == 0 and r['life_s'] >= LIFE_MIN and abs((r['f0'] + r['f1']) / 2 - tc) < 30],
                    key=lambda z: z[0])[:2]
    e = (None, None, None, group)
    show = [(t, col) for t, col in zip(e[3], (D_, I_, C_, O_))] + [(p, GREY) for _, p in prisms]
    if X0 <= cx < X1 and X0 <= cy < X1:
        ax.scatter([cx * dx], [cy * dx], s=160, facecolors='none', edgecolors='white', linewidths=1.4, zorder=6)
        ax.text(cx * dx + 0.35, cy * dx + 0.35, '3D view', color='white', fontsize=8, zorder=6)
    if not (X0 <= cx < X1 and X0 <= cy < X1): print('FIG note: the 3D group lies outside the left panel', flush=True)
    a3 = fig.add_axes([0.5, 0.03, 0.48, 0.82], projection='3d'); a3.set_facecolor('#0f0f14')
    fig.text(0.74, 0.9, 'Scutoid tubes (coloured) that touch or lie side by side, and two prism tubes (grey), each whole\n'
             'white dots: swap corners; small dots: corners where a tube starts or ends', color='#e6e6ee', fontsize=9, ha='center')
    allp = []
    for t, col in show:
        r = recs[t]
        fr = slice(r['f0'], r['f1'] + 1)
        ys, xs = np.nonzero((L[fr] == t).any(0))
        y0, y1, x0, x1 = ys.min() - 3, ys.max() + 4, xs.min() - 3, xs.max() + 4
        if y1 - y0 > 200 or x1 - x0 > 200: continue          # wraps the periodic box: not drawn
        m = (L[fr, y0:y1, x0:x1] == t).astype(float)
        m = np.pad(m, ((1, 1), (0, 0), (0, 0)))
        m = ndi.gaussian_filter(m, (0.8, 0.8, 0.8))
        v, f_, _, _ = marching_cubes(m, 0.5)
        P = np.stack([(v[:, 2] + x0) * dx, (v[:, 1] + y0) * dx, (v[:, 0] - 1 + r['f0']) * DT / 60], 1)
        pc = Poly3DCollection(P[f_], facecolor=(*col, 0.32), edgecolor=(*col, 0.04), linewidths=0.1)
        a3.add_collection3d(pc); allp.append(P)
        for ev in r['events']:
            if ev[0] != 'c': continue
            yy, xx = ev[4]
            a3.scatter([xx * dx], [yy * dx], [(ev[1] + 0.5) * DT / 60], s=40 if ev[2] else 14, color='white' if ev[2] else (*col,),
                       edgecolors=(*col,) if ev[2] else 'white', linewidths=0.9 if ev[2] else 0.4, depthshade=False, zorder=5)
    P = np.concatenate(allp)
    lo, hi = P.min(0), P.max(0); c3 = (lo + hi) / 2; span = (hi - lo)[:2].max() / 2 + 0.2
    a3.set_xlim(c3[0] - span, c3[0] + span); a3.set_ylim(c3[1] - span, c3[1] + span); a3.set_zlim(lo[2], hi[2])
    a3.set_box_aspect((1, 1, 1.25))
    a3.view_init(elev=14, azim=-58)
    for axis in (a3.xaxis, a3.yaxis, a3.zaxis):
        axis.set_pane_color((0.08, 0.08, 0.1, 1.0)); axis.label.set_color('#b0b0bb'); axis._axinfo['grid']['color'] = (0.2, 0.2, 0.25, 1)
    a3.tick_params(colors='#b0b0bb', labelsize=7)
    a3.set_xlabel('x (Mm)', fontsize=8); a3.set_ylabel('y (Mm)', fontsize=8); a3.set_zlabel('t (min)', fontsize=8)
    fig.text(0.04, 0.012, 'Vertical velocity of the Bifrost run en024048_hion, 0.1 Mm below the surface (Carlsson et al. 2016; Gudiksen et al. 2011; Hinode SDC Europe); scutoid: Gómez-Gálvez et al. 2018.',
             color='#9a9aa6', fontsize=7.5)
    fig.text(0.985, 0.012, 'DICTO · dictospheres.com', ha='right', va='bottom', color='#e6e6ee', fontsize=9)
    os.makedirs(f'{S}/results/figures', exist_ok=True)
    out = f'{S}/results/figures/sun_spacetime_scutoids.png'
    fig.savefig(out, dpi=130, facecolor=fig.get_facecolor())
    print('FIG outlines', dict(shown), 'corner tubes', e[3], 'prisms', [p for _, p in prisms], 'at frame', tc, flush=True)
    print('FIG_OK' if shown['scutoid'] + shown['scutoid (cut by the block ends)'] > 0 and len(prisms) == 2 else 'FIG_FAIL', out, flush=True)


if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'sun': cmd_sun(sys.argv[2], sys.argv[3], sys.argv[4:])
    elif c == 'pv': cmd_pv(int(sys.argv[2]), float(sys.argv[3]), sys.argv[4])
    elif c == 'mv': cmd_mv(int(sys.argv[2]), sys.argv[3])
    elif c == 'fig': cmd_fig(sys.argv[2], sys.argv[3])
