"""Persistence and recurrence of the granulation skeleton (README section "The skeleton: persistence or reappearance", 16 Nov 2026).

DICTO, 16 Nov 2026: "better framing can still be achieved with the sun, maybe there is a persistence, or reappearance of
structures that reappear in cycles"; sharpened the same day: "it's a reappearance that seems to be persistence". No swap matching
is used here: the measured objects are positions (corners, downflow sinks, cell centres) and a pixel mask (the downflow lanes).

Objects, per frame of uz on a horizontal plane (upflow positive; smoothing 1.5 pixels as the census):
  lanes   pixels with downflow (smoothed uz < 0);
  corners junctions of the census tiling (2 x 2 pixel blocks where at least three cells meet, blocks within one pixel merged),
          with the cells that meet there;
  sinks   local maxima of downflow speed (at least 4 pixels apart, downflow faster than 1.5 standard deviations of uz);
  cells   the census cells (threshold mean + 0.25 std, marker watershed of tiles.py), tracked by mutual largest overlap
          (tiles.match, the census rule) and also by their centres with the position tracker below.
Position tracker: a feature at one sampled frame continues at the next when each is the other's nearest feature within r
(periodic box). Lifetime = frames present x step. Tracks that start at the first sampled frame are left out of lifetime
distributions (start unknown); tracks alive at the last frame are right-censored (Kaplan-Meier median beside the plain median).
Sites (DICTO's sharpening): corner tracks are joined into one site when a new track starts within r of where the old one ended,
at most G seconds later; a site's span runs from its first to its last frame. A site whose span is at least LS seconds is
"apparently persistent" and is classified as (a) continuous with the same cells, (b) continuous with renewed cells (the set of
cells meeting at the corner changed), (c) intermittent and re-formed (absent at least one sampled frame inside its span).
Recurrence: births of cells (overlap rule) within r of a death in the preceding T seconds, and within r of a long-lived corner,
against random positions with the same number and times (and against the centres of all cells then present); families of
fragmenting granules (split genealogy, after Roudier and co-workers) against single-cell lifetimes; the lane mask at fixed pixels:
autocorrelation over lag, power spectrum, gaps in presence.
Control (moving Voronoi tiling, control_voronoi.py regenerated from its seed): exact corners = circumcentres of the periodic
Delaunay triangles; their exact combinatorial lifetimes, their position-tracked lifetimes, and the pipeline's on the image.

Usage:
  skeleton.py feat  DATA RUN DZ SEG|- OUT.pkl         per-frame features (SEG = census label maps; '-' segments here)
  skeleton.py anal  FEAT.pkl SEG|- DATA RUN DZ ORDER STEP OUT.json   ORDER real | rev | shuf:SEED
  skeleton.py voro  DATA NAME SPEED SEED OUT.json     moving-Voronoi control (exact and pipeline)
  skeleton.py combine RESULTSDIR                      tables (summary.json, summary.md)
Data credit: Bifrost code, Gudiksen et al. 2011, A&A 531, A154; run en024048_hion, Carlsson, Hansteen, Gudiksen, Leenaarts & De
Pontieu 2016, A&A 585, A4; qs024048_by3363 from the same archive; Hinode Science Data Centre Europe (sdc.uio.no). Hinode is a
Japanese mission developed and launched by ISAS/JAXA, with NAOJ as domestic partner and NASA and STFC (UK) as international
partners. It is operated by these agencies in co-operation with ESA and NSC (Norway)."""
import sys, os, json, pickle, glob
import numpy as np
from scipy import ndimage as ndi
from scipy.spatial import cKDTree
from collections import defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tiles as TL

SIGMA, THR = 1.5, 0.25
DT = 10.0                      # s between snapshots
RS = (2, 3, 4)                 # tolerance r in pixels (48 km): 96, 144, 192 km
LS = 300.0                     # s: span for an apparently persistent site / a long-lived corner
GS = (30.0, 60.0, 120.0)       # s: largest gap closed when joining tracks into sites
TB = 60.0                      # s: window for a birth after a death
NULL_DRAWS = 20


def order_of(order, n):
    if order == 'real': return np.arange(n)
    if order == 'rev': return np.arange(n)[::-1].copy()
    return np.random.default_rng(int(order.split(':')[1])).permutation(n)


# ---------------------------------------------------------------- features
def corners(lab):
    """Junction corners: (positions (k x 2, pixel-corner coordinates), list of cell tuples)."""
    R = np.roll(lab, -1, 1); D = np.roll(lab, -1, 0); RD = np.roll(R, -1, 0)
    nd = sum((p != q).astype(np.int8) for p, q in ((lab, R), (lab, D), (R, RD), (D, RD)))
    cand = np.argwhere(nd >= 3)
    keep, cells = [], []
    for i, j in cand:
        cs = {int(lab[i, j]), int(R[i, j]), int(D[i, j]), int(RD[i, j])}
        if len(cs) >= 3: keep.append((i, j)); cells.append(cs)
    if not keep: return np.zeros((0, 2)), []
    P = np.array(keep, float); L = lab.shape[0]
    par = list(range(len(P)))
    def find(a):
        while par[a] != a: par[a] = par[par[a]]; a = par[a]
        return a
    for a, b in kd(P, L).query_pairs(1.5):
        ra, rb = find(a), find(b)
        if ra != rb: par[ra] = rb
    grp = defaultdict(list)
    for a in range(len(P)): grp[find(a)].append(a)
    pos, cl = [], []
    for g in grp.values():
        th = 2 * np.pi * (P[g] + 1.0) / L
        pos.append((np.arctan2(np.sin(th).mean(0), np.cos(th).mean(0)) % (2 * np.pi)) * L / (2 * np.pi))
        cl.append(tuple(sorted(set().union(*[cells[a] for a in g]))))
    return np.array(pos), cl


def sinks(f):
    from skimage.feature import peak_local_max
    dn = -f; pad = 8; L = f.shape[0]
    t = np.pad(dn, pad, mode='wrap')
    pk = peak_local_max(t, min_distance=4, threshold_abs=1.5 * f.std(), exclude_border=False)
    pk = pk[(pk[:, 0] >= pad) & (pk[:, 0] < pad + L) & (pk[:, 1] >= pad) & (pk[:, 1] < pad + L)] - pad
    return pk.astype(float) + 0.5


def centres(lab):
    ids = np.unique(lab); L = lab.shape[0]
    yy, xx = np.indices(lab.shape); out = []
    for coord in (yy, xx):
        th = 2 * np.pi * (coord + 0.5) / L
        s = ndi.mean(np.sin(th), lab, ids); c = ndi.mean(np.cos(th), lab, ids)
        out.append((np.arctan2(s, c) % (2 * np.pi)) * L / (2 * np.pi))
    return ids, np.stack(out, 1)


def load_seg(seg, data, run, dz, n=None):
    if seg != '-': return np.load(seg, mmap_mode='r')
    F = np.load(f'{data}/{run}_uz_dz{dz}.npy', mmap_mode='r')
    n = n or F.shape[0]
    return np.array([TL.segment(np.asarray(F[k]), SIGMA, THR, method='thr') for k in range(n)])


def cmd_feat(data, run, dz, seg, out):
    F = np.load(f'{data}/{run}_uz_dz{dz}.npy', mmap_mode='r')
    n = min(F.shape[0], int(os.environ.get('SKEL_N', F.shape[0])))
    S = np.load(seg, mmap_mode='r') if seg != '-' else None
    fr = []; lanes = np.zeros((n,) + F.shape[1:], dtype=bool); uzc = []
    segs = [] if S is None else None
    for k in range(n):
        f = ndi.gaussian_filter(np.asarray(F[k], np.float64), SIGMA, mode='wrap')
        lab = np.asarray(S[k]) if S is not None else TL.segment(np.asarray(F[k]), SIGMA, THR, method='thr')
        if segs is not None: segs.append(lab.astype(np.int16))
        cp, cc = corners(lab)
        ids, cen = centres(lab)
        fr.append(dict(cpos=cp, ccells=cc, spos=sinks(f), cid=ids, cen=cen, ncell=len(ids)))
        lanes[k] = f < 0
        uzc.append(np.asarray(F[k][::8, ::8], np.float32))
        if k % 20 == 0: print(f'PROGRESS {(k + 1) / n:.4f} feat {run} dz{dz} {k + 1}/{n}', flush=True)
    if segs is not None: np.save(out.replace('.pkl', '_seg.npy'), np.array(segs))
    pickle.dump(dict(run=run, dz=dz, n=n, L=F.shape[1], frames=fr, lanes=np.packbits(lanes, axis=None), shape=lanes.shape,
                     uz_sub=np.array(uzc)), open(out, 'wb'))
    print('FEAT_OK', run, dz, n, 'corners/frame', np.mean([len(x['cpos']) for x in fr]).round(1), 'sinks/frame',
          np.mean([len(x['spos']) for x in fr]).round(1), 'cells/frame', np.mean([x['ncell'] for x in fr]).round(1),
          'lane share', round(float(lanes.mean()), 3), flush=True)


# ---------------------------------------------------------------- tracking
def kd(P, L):
    P = np.mod(np.asarray(P, float), L)
    return cKDTree(np.where(P >= L, 0.0, P), boxsize=L)


def link(P, Q, r, L):
    """Mutual nearest neighbours within r (periodic): dict index in P -> index in Q."""
    if len(P) == 0 or len(Q) == 0: return {}
    dq, iq = kd(Q, L).query(P % L, distance_upper_bound=r)
    dp, ip = kd(P, L).query(Q % L, distance_upper_bound=r)
    return {a: int(b) for a, b in enumerate(iq) if np.isfinite(dq[a]) and ip[b] == a}


def tracks_of(pos_list, r, L):
    """pos_list: positions per sampled frame. Returns list of tracks [(frame index, feature index), ...]."""
    tr = []; cur = {}
    for k, P in enumerate(pos_list):
        nxt = {}
        lk = link(pos_list[k - 1], P, r, L) if k else {}
        for a, b in lk.items():
            t = cur.pop(a); t.append((k, b)); nxt[b] = t
        tr.extend(cur.values())
        for b in range(len(P)):
            if b not in nxt: nxt[b] = [(k, b)]
        cur = nxt
    tr.extend(cur.values())
    return tr


def km_median(life, cens):
    """Kaplan-Meier median for right-censored lifetimes (cens True = still alive at the end)."""
    life = np.asarray(life, float); cens = np.asarray(cens, bool)
    if len(life) == 0: return None
    s = 1.0
    for t in np.unique(life):
        at = (life >= t).sum(); d = ((life == t) & ~cens).sum()
        if at: s *= 1 - d / at
        if s <= 0.5: return float(t)
    return None   # median beyond the run


def lifestats(life, cens):
    life = np.asarray(life, float); cens = np.asarray(cens, bool)
    if len(life) == 0: return dict(n=0)
    q = np.percentile(life, [25, 50, 75, 90])
    return dict(n=int(len(life)), censored=int(cens.sum()), median=float(q[1]), q25=float(q[0]), q75=float(q[2]), q90=float(q[3]),
                mean=float(life.mean()), km_median=km_median(life, cens), share_1frame=float((life == life.min()).mean()) if len(life) else None,
                hist=np.histogram(life, bins=[0, 15, 25, 45, 65, 95, 125, 185, 245, 365, 605, 905, 1205, 1805, 2500])[0].tolist())


def survival(idsets, dt, maxlag_s=1200):
    """Time-weighted persistence: S(tau) = share of the objects present at a frame that are still present (same id) tau later,
    averaged over all start frames (no truncation bias). Returns lags, S, and the half-time (first lag with S < 0.5)."""
    nk = len(idsets); lags, S = [], []
    for lag in range(0, min(nk - 1, int(maxlag_s / dt)) + 1):
        num = sum(len(idsets[k] & idsets[k + lag]) for k in range(nk - lag)); den = sum(len(idsets[k]) for k in range(nk - lag))
        lags.append(lag * dt); S.append(num / max(den, 1))
    half = next((l for l, v in zip(lags, S) if v < 0.5), None)
    return dict(lags_s=lags, S=[round(v, 4) for v in S], half_s=half)


def track_idsets(tr, nk):
    ids = [set() for _ in range(nk)]
    for ti, t in enumerate(tr):
        for k, _ in t: ids[k].add(ti)
    return ids


def track_lifetimes(tr, nk, dt):
    life, cens = [], []
    for t in tr:
        if t[0][0] == 0: continue
        life.append(len(t) * dt); cens.append(t[-1][0] == nk - 1)
    return life, cens


# ---------------------------------------------------------------- sites (DICTO 16 Nov: reappearance that seems to be persistence)
def sites_of(tr, pos_list, cells_of, r, L, gap_f, nk, dt):
    """Join corner tracks into sites: a track starting within r of where another ended, after at most gap_f sampled frames
    absent (0 = the next frame, a relinked replacement). cells_of(k, i) -> frozenset of persistent cell ids at corner i of frame k."""
    by_start = defaultdict(list)
    for ti, t in enumerate(tr): by_start[t[0][0]].append(ti)
    succ, taken = {}, set()
    order = sorted(range(len(tr)), key=lambda ti: tr[ti][-1][0])
    for ti in order:
        k1, i1 = tr[ti][-1]
        if k1 >= nk - 1: continue
        p = pos_list[k1][i1]; best = None
        for g in range(0, gap_f + 1):
            ks = k1 + 1 + g
            if ks >= nk: break
            cands = [tj for tj in by_start.get(ks, []) if tj not in taken]
            if not cands: continue
            Q = np.array([pos_list[ks][tr[tj][0][1]] for tj in cands])
            d = np.abs(Q - p); d = np.minimum(d, L - d); d = np.hypot(d[:, 0], d[:, 1])
            j = int(np.argmin(d))
            if d[j] <= r: best = (cands[j], g); break
        if best: succ[ti] = best; taken.add(best[0])
    sites = []
    for ti in range(len(tr)):
        if ti in taken: continue
        chain = [ti]; gaps = []
        sid = len(sites)
        while chain[-1] in succ:
            nx, g = succ[chain[-1]]; chain.append(nx); gaps.append(g)
        k0 = tr[chain[0]][0][0]; k1 = tr[chain[-1]][-1][0]
        present = sum(len(tr[c]) for c in chain)
        cellsets = [cells_of(k, i) for c in chain for (k, i) in tr[c]]
        distinct = set().union(*cellsets) if cellsets else set()
        sites.append(dict(k0=k0, k1=k1, span=(k1 - k0 + 1) * dt, present=present * dt, gaps=[g * dt for g in gaps if g > 0],
                          relinks=sum(1 for g in gaps if g == 0), same_cells=len(set(cellsets)) == 1,
                          kept_cells=len(cellsets[0] & cellsets[-1]) >= 2 if cellsets else True, ncells=len(distinct),
                          ncellsets=len(set(cellsets)), censored=k0 == 0 or k1 == nk - 1, frames=[k for c in chain for (k, i) in tr[c]]))
    return sites


def classify(sites, ls):
    """(a) continuous with the same cells (at least two of the cells at its first frame still meet there at its last frame),
    (b) continuous with renewed cells (at most one kept), (c) intermittent and re-formed. Strict variant: (a) only if the set
    of cells never changed."""
    ap = [s for s in sites if s['span'] >= ls]
    a = sum(1 for s in ap if not s['gaps'] and s['kept_cells'])
    b = sum(1 for s in ap if not s['gaps'] and not s['kept_cells'])
    c = sum(1 for s in ap if s['gaps'])
    a_strict = sum(1 for s in ap if not s['gaps'] and s['same_cells'])
    n = max(len(ap), 1)
    g = [x for s in ap for x in s['gaps']]
    return dict(n_apparent=len(ap), a_same=a, b_renewed=b, c_reformed=c, share_a=a / n, share_b=b / n, share_c=c / n,
                a_strict=a_strict, share_a_strict=a_strict / n,
                gaps_per_site=float(np.mean([len(s['gaps']) for s in ap])) if ap else None,
                gap_median_s=float(np.median(g)) if g else None,
                gap_hist=np.histogram(g, bins=[0, 15, 25, 35, 65, 125, 305])[0].tolist(),
                absent_share=float(np.mean([1 - s['present'] / s['span'] for s in ap])) if ap else None,
                ncells_median=float(np.median([s['ncells'] for s in ap])) if ap else None,
                ncells_per_min=float(np.median([s['ncells'] / (s['span'] / 60) for s in ap])) if ap else None,
                span_median_s=float(np.median([s['span'] for s in ap])) if ap else None,
                span_ncells=[[s['span'], s['ncells']] for s in ap][:3000],
                censored=sum(1 for s in ap if s['censored']))


def reform_vs_chance(tr, pos_list, r, L, gap_f, nk, rng):
    """Share of corner-track ends followed by a new track start within r inside gap_f+1 sampled frames, at the true end place,
    against (i) a uniform random place at the same time, (ii) the same place with the starts taken half the run away in time
    (time-shifted null: keeps any fixed spatial pattern, removes continuity in time)."""
    starts = defaultdict(list)
    for t in tr:
        if t[0][0] > 0: starts[t[0][0]].append(pos_list[t[0][0]][t[0][1]])
    trees = {k: kd(np.array(v), L) for k, v in starts.items()}
    sh = nk // 2
    hit, hitr, hits, n = 0, 0.0, 0, 0
    for t in tr:
        k1, i1 = t[-1]
        if k1 >= nk - 1 - gap_f: continue
        n += 1; p = pos_list[k1][i1]
        def any_near(q, shift=0):
            for g in range(gap_f + 1):
                kk = k1 + 1 + g
                if shift: kk = 1 + (kk - 1 + shift) % (nk - 1)
                tt = trees.get(kk)
                if tt is not None and tt.query_ball_point(q % L, r): return True
            return False
        hit += any_near(p)
        hitr += np.mean([any_near(rng.uniform(0, L, 2)) for _ in range(4)])
        hits += any_near(p, sh)
    return dict(n_ends=n, reform_share=hit / max(n, 1), chance_share=hitr / max(n, 1), shifted_share=hits / max(n, 1),
                ratio=(hit / max(hitr, 1e-9)) if n else None, ratio_shifted=(hit / max(hits, 1e-9)) if n else None)


def disk_mask(points, r, L):
    m = np.zeros((L, L), bool)
    if len(points):
        P = np.mod(np.round(np.asarray(points) - 0.5).astype(int), L); m[P[:, 0], P[:, 1]] = True
    yy, xx = np.mgrid[-r:r + 1, -r:r + 1]
    t = ndi.binary_dilation(np.pad(m, r, mode='wrap'), structure=(yy ** 2 + xx ** 2 <= r * r))
    return t[r:r + L, r:r + L]


# ---------------------------------------------------------------- lanes at fixed pixels
def lane_stats(lanes, dt):
    nk = lanes.shape[0]
    m = lanes.reshape(nk, -1).astype(np.float32)
    p = m.mean()
    ac = []
    for lag in range(0, min(nk - 1, int(1200 / dt)) + 1):
        a, b = m[:nk - lag], m[lag:]
        ma, mb = a.mean(), b.mean()
        cov = (a * b).mean() - ma * mb
        ac.append(float(cov / np.sqrt(ma * (1 - ma) * mb * (1 - mb))))
    x = m - m.mean(0)
    w = np.hanning(nk)[:, None]
    spec = (np.abs(np.fft.rfft(x * w, axis=0)) ** 2).mean(1)
    freq = np.fft.rfftfreq(nk, dt)
    occ = m.mean(0)
    sel = occ >= 0.5
    sub = lanes.reshape(nk, -1)[:, sel].astype(bool)
    # absence runs inside each pixel's presence span (first to last lane frame)
    trans = np.diff(sub.astype(np.int8), axis=0)
    ngaps = (trans == -1).sum(0) - (~sub[-1]).astype(int)        # absence runs that end before the last frame (sub is bool: 11-16 fix)
    ngaps = np.maximum(ngaps, 0)
    return dict(lane_share=float(p), lags_s=[i * dt for i in range(len(ac))], autocorr=ac, freq_mHz=(freq * 1000).tolist(),
                power=spec.tolist(), pixels_occ50=int(sel.sum()), occ50_no_gap=float((ngaps == 0).mean()) if sel.any() else None,
                occ50_gaps_median=float(np.median(ngaps)) if sel.any() else None,
                occ50_absent_share=float(1 - sub.mean()) if sel.any() else None)


def uz_spectrum(uz, dt):
    nk = uz.shape[0]; x = uz.reshape(nk, -1); x = x - x.mean(0)
    spec = (np.abs(np.fft.rfft(x * np.hanning(nk)[:, None], axis=0)) ** 2).mean(1)
    return dict(freq_mHz=(np.fft.rfftfreq(nk, dt) * 1000).tolist(), power=spec.tolist())


def ac_features(ac, lags):
    """Secondary maximum of an autocorrelation curve: first local minimum, then the next local maximum, and its height."""
    ac = np.asarray(ac)
    for i in range(1, len(ac) - 1):
        if ac[i] < ac[i - 1] and ac[i] <= ac[i + 1]:
            j = i + int(np.argmax(ac[i:]))
            return dict(first_min_s=lags[i], first_min=float(ac[i]), next_max_s=lags[j], next_max=float(ac[j]), bump=float(ac[j] - ac[i]))
    return dict(first_min_s=None, bump=0.0, monotone=True)


def efold(ac, lags):
    for i, v in enumerate(ac):
        if v < np.exp(-1): return lags[i]
    return None


# ---------------------------------------------------------------- analysis of one order and step
def cmd_anal(featf, seg, data, run, dz, order, step, out):
    FE = pickle.load(open(featf, 'rb'))
    n, L = FE['n'], FE['L']
    S = np.load(seg, mmap_mode='r') if seg != '-' else np.load(featf.replace('.pkl', '_seg.npy'), mmap_mode='r')
    idx = order_of(order, n)[::step]; nk = len(idx); dt = DT * step
    fr = [FE['frames'][k] for k in idx]
    rng = np.random.default_rng(11)
    res = dict(run=run, dz=dz, order=order, step=step, dt=dt, frames=nk, r_px=list(RS), px_km=48)
    # overlap-tracked cells (census rule) and the raw -> persistent label tables
    prev = None; nid = 1; luts = []; parents_all = {}; heirs_all = {}
    for j, k in enumerate(idx):
        lab = np.asarray(S[k]).astype(np.int64)
        if prev is None:
            u = np.unique(lab); mp = {int(a): i + 1 for i, a in enumerate(u)}; nid = len(u) + 1
            lut = np.zeros(lab.max() + 1, np.int64)
            for a, v in mp.items(): lut[a] = v
            out_ = lut[lab]; par, hr = {}, {}
        else:
            out_, par, hr, nid = TL.match(prev, lab, nid)
            lut = np.zeros(lab.max() + 1, np.int64); lut[lab.ravel()] = out_.ravel()
        luts.append(lut); parents_all[j] = par; heirs_all[j] = hr; prev = out_
        if j % 40 == 0: print(f'PROGRESS {0.5 * (j + 1) / nk:.4f} match {order} s{step} {j + 1}/{nk}', flush=True)
    first, last, cenof = {}, {}, {}
    for j, f in enumerate(fr):
        for a, c in zip(f['cid'].tolist(), f['cen']):
            pid = int(luts[j][a]); first.setdefault(pid, j); last[pid] = j; cenof[(pid, j)] = c
    life, cens = [], []
    for pid in first:
        if first[pid] == 0: continue
        life.append((last[pid] - first[pid] + 1) * dt); cens.append(last[pid] == nk - 1)
    res['cells_overlap'] = lifestats(life, cens)
    pidsets = [set() for _ in range(nk)]
    for (p, j) in cenof: pidsets[j].add(p)
    res['cells_overlap']['survival'] = survival(pidsets, dt)
    # families of fragmenting granules: child -> main parent (share >= 0.5); split+merge: dying cell -> main heir (share >= 0.5)
    children = defaultdict(list); heir_of = {}
    for j in range(1, nk):
        for c, ps in parents_all[j].items():
            o, sh = max(ps.items(), key=lambda x: x[1])
            if sh >= 0.5 and o in first: children[int(o)].append(int(c))
        for o, hs in heirs_all[j].items():
            h, sh = max(hs.items(), key=lambda x: x[1])
            if sh >= 0.5: heir_of[int(o)] = int(h)
    def fam_end(root, merge):
        seen, stack, end = set(), [root], 0
        while stack:
            c = stack.pop()
            if c in seen: continue
            seen.add(c); end = max(end, last[c])
            stack.extend(children.get(c, []))
            if merge and c in heir_of and heir_of[c] in last: stack.append(heir_of[c])
        return end, len(seen)
    fl, fc, fs, ml, mc = [], [], [], [], []
    sizes = []
    for pid in first:
        if first[pid] == 0: continue
        e, sz = fam_end(pid, False); fl.append((e - first[pid] + 1) * dt); fc.append(e == nk - 1); sizes.append(sz)
        e2, _ = fam_end(pid, True); ml.append((e2 - first[pid] + 1) * dt); mc.append(e2 == nk - 1)
    res['families_split'] = lifestats(fl, fc); res['families_split']['size_mean'] = float(np.mean(sizes)) if sizes else None
    res['families_split']['share_with_children'] = float(np.mean([s > 1 for s in sizes])) if sizes else None
    res['families_splitmerge'] = lifestats(ml, mc)
    # position tracking: corners, sinks, cell centres
    cpos = [f['cpos'] for f in fr]; spos = [f['spos'] for f in fr]; cen = [f['cen'] for f in fr]
    def cells_of(j, i): return frozenset(int(luts[j][a]) for a in fr[j]['ccells'][i])
    res['by_r'] = {}
    for r in RS:
        R = {}
        trc = tracks_of(cpos, r, L); trs = tracks_of(spos, r, L); trn = tracks_of(cen, r, L)
        R['corners'] = lifestats(*track_lifetimes(trc, nk, dt))
        R['sinks'] = lifestats(*track_lifetimes(trs, nk, dt))
        R['cells_centre'] = lifestats(*track_lifetimes(trn, nk, dt))
        for key, tr_ in (('corners', trc), ('sinks', trs), ('cells_centre', trn)): R[key]['survival'] = survival(track_idsets(tr_, nk), dt)
        # corner tracks that keep the same cells all along vs change
        lc = [t for t in trc if len(t) * dt >= LS]
        R['corner_tracks_long'] = dict(n=len(lc), same_cells=sum(1 for t in lc if len({cells_of(k, i) for k, i in t}) == 1),
                                       ncells_median=float(np.median([len(set().union(*[cells_of(k, i) for k, i in t])) for t in lc])) if lc else None)
        R['sites'] = {}
        for G in GS:
            gf = int(round(G / dt))
            st = sites_of(trc, cpos, cells_of, r, L, gf, nk, dt)
            R['sites'][str(int(G))] = classify(st, LS)
            sids = [set() for _ in range(nk)]
            for si, x in enumerate(st):
                for k in x['frames']: sids[k].add(si)
            R['sites'][str(int(G))]['survival_site'] = survival(sids, dt)
            R['sites'][str(int(G))]['reform'] = reform_vs_chance(trc, cpos, r, L, gf, nk, rng)
            ss = sites_of(trs, spos, lambda j, i: frozenset(), r, L, gf, nk, dt)
            cs = classify(ss, LS); R['sites'][str(int(G))]['sinks'] = dict(n_apparent=cs['n_apparent'], share_c=cs['share_c'],
                                                                           absent_share=cs['absent_share'])
        # recurrence: births near deaths (null: uniform places; deaths taken half the run away in time)
        births = [(first[p], cenof[(p, first[p])], p) for p in first if first[p] > 0]
        deaths = defaultdict(list)
        for p in last:
            if last[p] < nk - 1: deaths[last[p]].append(cenof[(p, last[p])])
        dtrees = {k: kd(np.array(v), L) for k, v in deaths.items()}
        tb = max(1, int(round(TB / dt))); sh = nk // 2
        def near_death(j, q, shift=0):
            for k in range(max(0, j - tb), j):
                kk = (k + shift) % nk if shift else k
                if kk in dtrees and dtrees[kk].query_ball_point(q % L, r): return True
            return False
        obs_d = float(np.mean([near_death(j, q) for j, q, _ in births])) if births else None
        rnd_d = float(np.mean([np.mean([near_death(j, rng.uniform(0, L, 2)) for j, _, _ in births]) for _ in range(NULL_DRAWS // 4)])) if births else None
        shf_d = float(np.mean([near_death(j, q, sh) for j, q, _ in births])) if births else None
        # births over a long-lived corner place: share of the new cell's pixels within r of a corner of a track lasting >= LS,
        # present in the preceding TB seconds; chance = the share of all pixels so covered (and the same with corners half the run away)
        longc = defaultdict(list)
        for t in trc:
            if len(t) * dt >= LS:
                for k, i in t: longc[k].append(cpos[k][i])
        def cover(j, shift=0):
            pts = [p for k in range(max(0, j - tb), j) for p in longc.get(((k + shift) % nk) if shift else k, [])]
            return disk_mask(pts, r, L)
        cb, ca, cs = [], [], []
        byj = defaultdict(list)
        for j, q, p in births: byj[j].append(p)
        for j, ps in byj.items():
            M = cover(j); Ms = cover(j, sh); lab = luts[j][np.asarray(S[idx[j]])]
            for p in ps:
                sel = lab == p
                if sel.any(): cb.append(M[sel].mean()); cs.append(Ms[sel].mean())
            ca.append(M.mean())
        R['recurrence'] = dict(births=len(births), born_near_death=obs_d, chance_uniform_death=rnd_d, shifted_death=shf_d,
                               ratio_death=(obs_d / rnd_d) if births and rnd_d else None,
                               ratio_death_shifted=(obs_d / shf_d) if births and shf_d else None,
                               birth_cover_long_corner=float(np.mean(cb)) if cb else None,
                               chance_cover_long_corner=float(np.mean(ca)) if ca else None,
                               shifted_cover_long_corner=float(np.mean(cs)) if cs else None)
        if r == 3: res['tracks_r3'] = dict(corners=[[(int(k), [round(float(x), 1) for x in cpos[k][i]]) for k, i in t] for t in trc if len(t) >= 3])
        res['by_r'][str(r)] = R
        print(f'PROGRESS {0.5 + 0.4 * (RS.index(r) + 1) / len(RS):.4f} r={r}', flush=True)
    lanes = np.unpackbits(FE['lanes'])[:np.prod(FE['shape'])].reshape(FE['shape'])[idx]
    res['lanes'] = lane_stats(lanes, dt)
    res['lanes']['ac_features'] = ac_features(res['lanes']['autocorr'], res['lanes']['lags_s'])
    res['lanes']['efold_s'] = efold(res['lanes']['autocorr'], res['lanes']['lags_s'])
    res['uz'] = uz_spectrum(FE['uz_sub'][idx], dt)
    json.dump(res, open(out, 'w'))
    ok = res['cells_overlap']['n'] > 0 and res['by_r']['3']['corners']['n'] > 0
    print('ANAL_OK' if ok else 'ANAL_FAIL', run, dz, order, step, flush=True)
    print('FINAL ok' if ok else 'FINAL FAIL', flush=True)


# ---------------------------------------------------------------- second pass (16 Nov, after reading the first results)
def reform_conditional(pos_list, tr, r, L, gap_f, nk, rng, nnull=4, far_s=600, dt=10.0):
    """Re-formation without the linking bias: a corner track ends at frame k1 at place p AND no corner lies within r of p at k1+1
    (a true vanishing). Re-formed if any corner lies within r of p in frames k1+2 .. k1+1+gap_f. Null: the same conditional event
    at the same place p at frames k' at least far_s away in time (any spatial pattern kept, continuity removed). In shuffled frames
    the two are equal in expectation."""
    trees = [kd(P, L) if len(P) else None for P in pos_list]
    near = lambda k, q: trees[k] is not None and bool(trees[k].query_ball_point(q % L, r))
    far = max(1, int(far_s / dt))
    obs, n, nul, nn = 0, 0, 0, 0
    for t in tr:
        k1, i1 = t[-1]
        if k1 >= nk - 2 - gap_f: continue
        p = pos_list[k1][i1]
        if near(k1 + 1, p): continue
        n += 1; obs += any(near(k, p) for k in range(k1 + 2, k1 + 2 + gap_f))
        cand = [k for k in range(0, nk - 2 - gap_f) if abs(k - k1) >= far]
        for k in (rng.choice(cand, size=min(nnull, len(cand)), replace=False) if cand else []):
            if near(k + 1, p): continue
            nn += 1; nul += any(near(kk, p) for kk in range(k + 2, k + 2 + gap_f))
    return dict(vanishings=n, reformed=obs / max(n, 1), null_events=nn, null_reformed=nul / max(nn, 1),
                ratio=(obs / max(n, 1)) / max(nul / max(nn, 1), 1e-9) if n and nn else None)


def cmd_anal2(featf, seg, data, run, dz, order, step, out):
    """Families as presence (time-weighted), re-formation without the linking bias, lanes with the gap fix and quadrant errors."""
    FE = pickle.load(open(featf, 'rb'))
    n, L = FE['n'], FE['L']
    S = np.load(seg, mmap_mode='r') if seg != '-' else np.load(featf.replace('.pkl', '_seg.npy'), mmap_mode='r')
    idx = order_of(order, n)[::step]; nk = len(idx); dt = DT * step
    fr = [FE['frames'][k] for k in idx]
    rng = np.random.default_rng(13)
    res = dict(run=run, dz=dz, order=order, step=step, dt=dt, frames=nk)
    prev = None; nid = 1; present = []; main_par = {}; main_heir = {}
    for j, k in enumerate(idx):
        lab = np.asarray(S[k]).astype(np.int64)
        if prev is None:
            u = np.unique(lab); lut = np.zeros(lab.max() + 1, np.int64); lut[u] = np.arange(1, len(u) + 1); nid = len(u) + 1
            out_ = lut[lab]; par, hr = {}, {}
        else:
            out_, par, hr, nid = TL.match(prev, lab, nid)
        for c, ps in par.items():
            o, sh = max(ps.items(), key=lambda x: x[1])
            if sh >= 0.5: main_par[int(c)] = int(o)
        for o, hs in hr.items():
            h, sh = max(hs.items(), key=lambda x: x[1])
            if sh >= 0.5: main_heir[int(o)] = int(h)
        present.append(set(np.unique(out_).tolist())); prev = out_
        if j % 40 == 0: print(f'PROGRESS {0.6 * (j + 1) / nk:.4f} match {order} s{step} {j + 1}/{nk}', flush=True)
    def root(c):
        seen = set()
        while c in main_par and c not in seen: seen.add(c); c = main_par[c]
        return c
    R = {c: root(c) for s_ in present for c in s_}
    par_ = {}
    def find(a):
        while par_.get(a, a) != a: par_[a] = par_.get(par_[a], par_[a]); a = par_[a]
        return a
    for c, o in list(main_par.items()) + list(main_heir.items()):
        ra, rb = find(c), find(o)
        if ra != rb: par_[ra] = rb
    res['cells'] = survival(present, dt)
    res['families_split'] = survival([{R[c] for c in s_} for s_ in present], dt)
    res['families_split']['n_families_per_frame'] = float(np.mean([len({R[c] for c in s_}) for s_ in present]))
    res['families_splitmerge'] = survival([{find(c) for c in s_} for s_ in present], dt)
    res['families_splitmerge']['n_families_per_frame'] = float(np.mean([len({find(c) for c in s_}) for s_ in present]))
    res['cells_per_frame'] = float(np.mean([len(s_) for s_ in present]))
    cpos = [f['cpos'] for f in fr]; spos = [f['spos'] for f in fr]
    res['reform'] = {}
    for r in RS:
        trc = tracks_of(cpos, r, L); trs = tracks_of(spos, r, L)
        res['reform'][str(r)] = {str(int(G)): dict(corners=reform_conditional(cpos, trc, r, L, max(1, int(round(G / dt))), nk, rng, dt=dt),
                                                   sinks=reform_conditional(spos, trs, r, L, max(1, int(round(G / dt))), nk, rng, dt=dt))
                                 for G in (60.0, 120.0, 300.0)}
        print(f'PROGRESS {0.6 + 0.3 * (RS.index(r) + 1) / len(RS):.4f} r={r}', flush=True)
    lanes = np.unpackbits(FE['lanes'])[:np.prod(FE['shape'])].reshape(FE['shape'])[idx].astype(bool)
    res['lanes'] = lane_stats(lanes, dt)
    res['lanes']['ac_features'] = ac_features(res['lanes']['autocorr'], res['lanes']['lags_s'])
    h = lanes.shape[1] // 2
    q = [lane_stats(lanes[:, a:a + h, b:b + h], dt)['autocorr'] for a in (0, h) for b in (0, h)]
    res['lanes']['autocorr_quadrants'] = q
    res['lanes']['ac_quadrant_features'] = [ac_features(x, res['lanes']['lags_s']) for x in q]
    json.dump(res, open(out, 'w'))
    ok = len(res['cells']['S']) > 1 and len(res['reform']) == len(RS) and res['cells_per_frame'] > 0
    print('ANAL2_OK' if ok else 'ANAL2_FAIL', run, dz, order, step, flush=True)
    print('FINAL ok' if ok else 'FINAL FAIL', flush=True)


# ---------------------------------------------------------------- moving-Voronoi control
def voro_seeds(N, speed, seed, L=504):
    rng = np.random.default_rng(seed)
    p0 = rng.uniform(0, L, (N, 2))
    A = rng.normal(0, 1, (N, 2, 2)); w = rng.uniform(0.002, 0.01, (N, 2, 2)); ph = rng.uniform(0, 2 * np.pi, (N, 2, 2))
    return lambda t: (p0 + speed * (A * np.sin(w * t + ph)).sum(2) / np.maximum(w.mean(2), 1e-9) * 0.01) % L


def voro_corners(P, L):
    """Circumcentres of the periodic Delaunay triangles (one per triangle) and their seed triples."""
    from scipy.spatial import Delaunay
    N = len(P)
    Q = np.concatenate([P + L * np.array([i, j]) for i in (-1, 0, 1) for j in (-1, 0, 1)])
    tri = Delaunay(Q).simplices
    a, b, c = Q[tri[:, 0]], Q[tri[:, 1]], Q[tri[:, 2]]
    d = 2 * (a[:, 0] * (b[:, 1] - c[:, 1]) + b[:, 0] * (c[:, 1] - a[:, 1]) + c[:, 0] * (a[:, 1] - b[:, 1]))
    ux = ((a ** 2).sum(1) * (b[:, 1] - c[:, 1]) + (b ** 2).sum(1) * (c[:, 1] - a[:, 1]) + (c ** 2).sum(1) * (a[:, 1] - b[:, 1])) / d
    uy = ((a ** 2).sum(1) * (c[:, 0] - b[:, 0]) + (b ** 2).sum(1) * (a[:, 0] - c[:, 0]) + (c ** 2).sum(1) * (b[:, 0] - a[:, 0])) / d
    cc = np.stack([ux, uy], 1)
    inside = (cc[:, 0] >= 0) & (cc[:, 0] < L) & (cc[:, 1] >= 0) & (cc[:, 1] < L)
    trip = [tuple(sorted(int(v) % N for v in t)) for t in tri[inside]]
    return cc[inside], trip


def cmd_voro(data, name, speed, seed, out):
    img = np.load(f'{data}/{name}_img_dz0.0.npy', mmap_mode='r'); nf, L = img.shape[0], img.shape[1]
    pos = voro_seeds(500, speed, seed, L)
    res = dict(name=name, frames=nf)
    ex_pos, ex_trip, pp_pos, pp_cells, labs = [], [], [], [], []
    for k in range(nf):
        cc, tp = voro_corners(pos(10.0 * k), L); ex_pos.append(cc); ex_trip.append(tp)
        lab = TL.segment(np.asarray(img[k]), 0, 0.01, method='hmax'); labs.append(lab)
        cp, cl = corners(lab); pp_pos.append(cp); pp_cells.append(cl)
        if k % 20 == 0: print(f'PROGRESS {0.6 * (k + 1) / nf:.4f} voro frame {k + 1}/{nf}', flush=True)
    # seed ids of pipeline cells: the seed nearest each cell's centre (fixed seeds: the true identity)
    seedmaps = []
    for k, lab in enumerate(labs):
        ids, cen = centres(lab); d, si = kd(pos(10.0 * k), L).query(cen)
        lut = np.zeros(lab.max() + 1, np.int64); lut[ids] = si; seedmaps.append(lut)
    res['by_step'] = {}
    for step in (1, 2, 4, 8):
        idx = np.arange(0, nf, step); nk = len(idx); dt = DT * step; RR = {}
        # exact combinatorial lifetime of each Delaunay triangle (consecutive sampled frames present)
        alive = {}; life, cens = [], []
        for j, k in enumerate(idx):
            cur = set(ex_trip[k])
            for t in list(alive):
                if t not in cur:
                    k0 = alive.pop(t)
                    if k0 > 0: life.append((j - k0) * dt); cens.append(False)
            for t in cur:
                if t not in alive: alive[t] = j
        for t, k0 in alive.items():
            if k0 > 0: life.append((nk - k0) * dt); cens.append(True)
        RR['exact_triangle'] = lifestats(life, cens)
        for r in RS:
            ep = [ex_pos[k] for k in idx]; et = [ex_trip[k] for k in idx]
            pp = [pp_pos[k] for k in idx]; pc = [pp_cells[k] for k in idx]; sm = [seedmaps[k] for k in idx]
            tre = tracks_of(ep, r, L); trp = tracks_of(pp, r, L)
            ce = lambda j, i: frozenset(et[j][i]); cp_ = lambda j, i: frozenset(int(sm[j][a]) for a in pc[j][i])
            e = dict(corners_exact=lifestats(*track_lifetimes(tre, nk, dt)), corners_pipeline=lifestats(*track_lifetimes(trp, nk, dt)))
            e['corners_exact']['survival'] = survival(track_idsets(tre, nk), dt); e['corners_pipeline']['survival'] = survival(track_idsets(trp, nk), dt)
            tsets = [set(et[j]) for j in range(nk)]; e['triangle_survival'] = survival(tsets, dt)
            e['sites_exact'] = classify(sites_of(tre, ep, ce, r, L, int(round(60 / dt)), nk, dt), LS)
            e['sites_pipeline'] = classify(sites_of(trp, pp, cp_, r, L, int(round(60 / dt)), nk, dt), LS)
            RR[str(r)] = e
        res['by_step'][str(step)] = RR
        print(f'PROGRESS {0.6 + 0.1 * (1 + (1, 2, 4, 8).index(step)):.4f} voro step {step}', flush=True)
    json.dump(res, open(out, 'w'))
    ok = res['by_step']['1']['exact_triangle']['n'] > 0
    print('VORO_OK' if ok else 'VORO_FAIL', name, flush=True)
    print('FINAL ok' if ok else 'FINAL FAIL', flush=True)


if __name__ == '__main__':
    c = sys.argv[1]; a = sys.argv[2:]
    if c == 'feat': cmd_feat(a[0], a[1], a[2], a[3], a[4])
    elif c == 'anal': cmd_anal(a[0], a[1], a[2], a[3], a[4], a[5], int(a[6]), a[7])
    elif c == 'anal2': cmd_anal2(a[0], a[1], a[2], a[3], a[4], a[5], int(a[6]), a[7])
    elif c == 'voro': cmd_voro(a[0], a[1], float(a[2]), int(a[3]), a[4])
    else: sys.exit('usage: see docstring')
