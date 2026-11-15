#!/usr/bin/env python3
"""Scutoid trace on a shell stack of a compound eye (study 2026-11-16-compound-eye-scutoids).

Per shell (concentric about the fitted cornea sphere, chart = angles about the patch axis): local-contrast image -> bright
cross-sections found as local maxima -> watershed regions (seeded at those maxima) -> intensity-weighted centroids.
Centroids are linked shell to shell (Hungarian assignment, gate, gaps up to GAP shells closed by interpolation) into tracks.
Only tracks that span the whole depth range are kept, so every neighbour graph sees the same cells.
Neighbour sets: (1) Delaunay (= Voronoi of the centroids) per shell; (2) touching watershed regions per shell.
A neighbour change = an interior edge present at the top of the layer and absent at the bottom (majority over W shells at each
end), i.e. a T1 swap; a cell with such an edge is "scutoid-like". Also counted on depth-smoothed tracks (detection noise
removed) and per step (flicker).
Null: the same counter on straight (non-rearranging) columns at the measured top positions + measured noise, bootstrapped:
each column gets the whole residual series (raw minus depth-smoothed track) of a random interior cell, randomly turned and
circularly shifted in depth (keeps heavy tails and depth correlation); 50 draws. Expectation from the study's model: sum over edges of
P(swap | local anisotropy A) from table B of the README (pooled pilot rates).

Library use: scipy (ndimage, spatial.Delaunay, optimize.linear_sum_assignment), scikit-image (peak_local_max, watershed).
Usage: eyetrace.py STACK.npy LAYER_NAME D0 D1 PERIOD_PX OUT.json [synthetic]
"""
import sys, json, time, numpy as np
from scipy import ndimage as ndi
from scipy.spatial import Delaunay
from scipy.optimize import linear_sum_assignment
from skimage.feature import peak_local_max
from skimage.segmentation import watershed

W = 5          # shells averaged (majority) at the top and at the bottom
GAP = 3        # longest gap (shells) closed by interpolation
SM_UM = 6.0    # depth smoothing of tracks (Gaussian sigma, um) for the smoothed count
BANDPASS = False  # set by run(bandpass=True)
DSM = 2.0      # depth smoothing of the shell images before detection (Gaussian sigma, shells)

# README table B, pooled bee + fly + D. elpenor (edges, % swapped) -> P(swap | A) by bin
A_BINS = [1.0, 1.2, 1.4, 1.6, 3 ** 0.5, 2.0, 2.5, 3.0, 1e9]
A_P = [(62691 * .008 + 9058 * .001 + 265337 * .001) / (62691 + 9058 + 265337),
       (15609 * .032 + 2179 * .011 + 1813 * 0) / (15609 + 2179 + 1813),
       (5074 * .059 + 1017 * .055 + 218 * .014) / (5074 + 1017 + 218),
       (1583 * .090 + 423 * .106 + 21 * .048) / (1583 + 423 + 21),
       (1524 * .121 + 507 * .160 + 11 * 0) / (1524 + 507 + 11),
       (1227 * .205 + 491 * .301) / (1227 + 491), (468 * .288 + 254 * .398) / (468 + 254), (653 * .459 + 563 * .467) / (653 + 563)]


def norm_img(a, s, big):
    if BANDPASS:                                                      # difference of Gaussians about the lattice ring
        g = ndi.gaussian_filter(a, s) - ndi.gaussian_filter(a, big / 2.4); sd = np.sqrt(ndi.gaussian_filter(g ** 2, big)) + 1e-6
        return g / sd
    g = ndi.gaussian_filter(a, s); b = ndi.gaussian_filter(g, big)
    sd = np.sqrt(ndi.gaussian_filter((g - b) ** 2, big)) + 1e-6
    return (g - b) / sd


def detect(z, period, zthr, edge):
    pk = peak_local_max(z, min_distance=max(2, int(0.42 * period)), threshold_abs=zthr, exclude_border=edge)
    mk = np.zeros(z.shape, np.int32); mk[pk[:, 0], pk[:, 1]] = np.arange(1, len(pk) + 1)
    lab = watershed(-z, mk)                                           # full tessellation: regions touch their neighbours
    w = np.clip(z, 0, None)                                           # bright core weights
    idx = np.arange(1, len(pk) + 1)
    m0 = ndi.sum(w, lab, idx) + 1e-9
    ii, jj = np.indices(z.shape)
    ci = ndi.sum(w * ii, lab, idx) / m0; cj = ndi.sum(w * jj, lab, idx) / m0
    return np.c_[ci, cj], lab


def region_adjacency(lab):
    a = lab[:, :-1].ravel(); b = lab[:, 1:].ravel(); c = lab[:-1, :].ravel(); d = lab[1:, :].ravel()
    p = np.r_[np.c_[a, b], np.c_[c, d]]; p = p[p[:, 0] != p[:, 1]]
    p = np.sort(p, 1) - 1
    return set(map(tuple, np.unique(p, axis=0)))


def predict(T, k):
    """Position of track T expected at shell k: last seen position + mean drift of its last (up to) 4 seen steps."""
    seen = np.where(~np.isnan(T[:k, 0]))[0]; last = seen[-1]
    if len(seen) < 2: return T[last]
    s = seen[-5:]; v = (T[s[-1]] - T[s[0]]) / (s[-1] - s[0])
    return T[last] + v * (k - last)


def link(dets, gate):
    """dets: list of (n_k, 2). Predictive nearest assignment (Hungarian) shell to shell; gaps up to GAP shells.
    Returns tracks as arrays (n_shells, 2) with NaN where missing, and det index per shell."""
    K = len(dets); tracks = []; tidx = []
    active = []   # (track id, last k, last pos)
    for k in range(K):
        P = dets[k]
        cand = [t for t in active if k - t[1] <= GAP + 1]
        used = set()
        if cand and len(P):
            L = np.array([predict(tracks[t[0]], k) for t in cand]); C = np.linalg.norm(L[:, None] - P[None], axis=2)
            C2 = np.where(C < gate, C, 1e6); r, c = linear_sum_assignment(C2)
            for i, j in zip(r, c):
                if C2[i, j] < 1e6:
                    tid = cand[i][0]; tracks[tid][k] = P[j]; tidx[tid][k] = j; used.add(j)
                    cand[i] = (tid, k, P[j])
        newact = [t for t in cand if k - t[1] <= GAP]
        for j in range(len(P)):
            if j not in used:
                T = np.full((K, 2), np.nan); T[k] = P[j]; I = np.full(K, -1); I[k] = j
                tracks.append(T); tidx.append(I); newact.append((len(tracks) - 1, k, P[j]))
        active = newact
    return tracks, tidx


def follow_tracks(Z, P0, period, rad=0.35, iters=4, power=2):
    """Column following (gw16): each start point moves to the intensity-weighted centre (weights clip(Z, 0) ** power) of a disc
    of radius rad * period about its position in the previous plane, iterated (mean shift). Z: (K, N, N), cells bright."""
    K = len(Z); P0 = np.asarray(P0, float); n = len(P0); r = rad * period; g = np.arange(-int(np.ceil(r)), int(np.ceil(r)) + 1)
    G1, G2 = np.meshgrid(g, g, indexing='ij'); m = G1 ** 2 + G2 ** 2 <= r * r; off = np.c_[G1[m], G2[m]].astype(float)
    X = np.empty((K, n, 2)); p = P0.copy()
    for k in range(K):
        W = np.clip(Z[k], 0, None)
        for _ in range(iters):
            Q = p[:, None, :] + off[None]
            w = ndi.map_coordinates(W, Q.reshape(-1, 2).T, order=1, cval=0.0).reshape(n, -1) ** power
            sw = w.sum(1); p = np.where(sw[:, None] > 1e-9, (w[..., None] * Q).sum(1) / (sw[:, None] + 1e-12), p)
        X[k] = p
    return X


def follow_link(Z, dets, period, seeds=None, agree=0.25, merge=0.35):
    """Tracks by column following from the detections of several seed planes (top, middle, bottom by default), each followed up
    and down through the whole depth. Tracks from different seed planes that stay within agree * period of each other in every
    plane are one column; a column is CONFIRMED when at least two seed planes reproduce it (this is the forward-backward test:
    a follower that hops to a neighbour is not reproduced from the other end). Confirmed columns that come within merge * period
    of each other in any plane are both left untrusted. Returns tracks (K, 2) of confirmed columns, their detection index per plane
    (nearest detection within 0.3 period, else -1), a trust flag, and the mean positions of unconfirmed columns."""
    K = len(Z); seeds = sorted(set([0, K // 2, K - 1])) if seeds is None else seeds
    T, src = [], []
    for ks in seeds:
        if len(dets[ks]) == 0: continue
        dn = follow_tracks(Z[ks:], dets[ks], period); up = follow_tracks(Z[ks::-1], dets[ks], period)
        T.append(np.concatenate([up[::-1][:-1], dn], 0)); src += [ks] * len(dets[ks])
    X = np.concatenate(T, 1); src = np.array(src); M = X.shape[1]
    par = np.arange(M)
    def find(a):
        while par[a] != a: par[a] = par[par[a]]; a = par[a]
        return a
    from scipy.spatial import cKDTree
    for a, b in cKDTree(X[K // 2]).query_pairs(agree * period):
        if np.linalg.norm(X[:, a] - X[:, b], axis=1).max() < agree * period: par[find(a)] = find(b)
    roots = np.array([find(a) for a in range(M)]); groups = {}
    for a, r_ in enumerate(roots): groups.setdefault(r_, []).append(a)
    conf, unconf = [], []
    for r_, mem in groups.items():
        (conf if len(set(src[mem])) >= 2 else unconf).append(X[:, mem].mean(1))
    if not conf: return [], [], np.zeros(0, bool), [], dict(followed=M, columns=len(groups), confirmed=0, merged=0)
    C = np.stack(conf, 1); n = C.shape[1]; trust = np.ones(n, bool)
    for k in range(K):
        for a, b in cKDTree(C[k]).query_pairs(merge * period): trust[a] = trust[b] = False
    tidx = []
    for i in range(n):
        I = np.full(K, -1)
        for k in range(K):
            if len(dets[k]):
                d = np.linalg.norm(dets[k] - C[k, i], axis=1); j = int(np.argmin(d))
                if d[j] < 0.3 * period: I[k] = j
        tidx.append(I)
    others = [u.mean(0) for u in unconf]
    return [C[:, i] for i in range(n)], tidx, trust, others, dict(followed=M, columns=len(groups), confirmed=n, merged=int((~trust).sum()))


def fill(T):
    ok = ~np.isnan(T[:, 0])
    if ok.all(): return T
    k = np.arange(len(T)); T = T.copy()
    for d in range(2): T[~ok, d] = np.interp(k[~ok], k[ok], T[ok, d])
    return T


def delaunay_edges(X):
    tri = Delaunay(X); E = set()
    for s in tri.simplices:
        for a, b in ((0, 1), (1, 2), (0, 2)):
            i, j = sorted((s[a], s[b])); E.add((i, j))
    hull = set(np.unique(tri.convex_hull))
    return E, hull


def dense_edges(Xk, extra, period):
    """Delaunay edges among the n tracked cells (indices < n), with the graph built on ALL cells of the shell: tracked ones
    at Xk plus the untracked detections (extra), so that every counted edge is a true lattice neighbour pair."""
    n = len(Xk)
    if extra is not None and len(extra):
        d = np.linalg.norm(extra[:, None] - Xk[None], axis=2).min(1); P = np.r_[Xk, extra[d > 0.3 * period]]
    else: P = Xk
    E, hull = delaunay_edges(P)
    return {e for e in E if e[0] < n and e[1] < n}, hull


def count_swaps(X, interior, extras=None, period=1.0):
    """X: (K, n, 2) tracked positions; extras: per shell, untracked detections (dense graph). interior: bool (n,)."""
    K = X.shape[0]; Es = []
    for k in range(K):
        E, _ = dense_edges(X[k], None if extras is None else extras[k], period); Es.append({e for e in E if interior[e[0]] and interior[e[1]]})
    def maj(rng):
        cnt = {}
        for k in rng:
            for e in Es[k]: cnt[e] = cnt.get(e, 0) + 1
        return {e for e, c in cnt.items() if c > len(rng) / 2}
    top = maj(range(0, min(W, K))); bot = maj(range(max(0, K - W), K))
    lost = top - bot; gained = bot - top
    flick = [len(Es[k] ^ Es[k + 1]) / 2 for k in range(K - 1)]
    cells = set(i for e in lost | gained for i in e)
    return dict(top_edges=len(top), lost=len(lost), gained=len(gained), share=len(lost) / max(1, len(top)),
                cells_changed=len(cells), interior_cells=int(interior.sum()), flicker_per_step=float(np.mean(flick)) if flick else 0.0,
                lost_edges=[[int(a), int(b)] for a, b in sorted(lost)], gained_edges=[[int(a), int(b)] for a, b in sorted(gained)])


def anisotropy(X0, X1, E):
    """Per cell: singular-value ratio of the least-squares 2x2 map of neighbour offsets X0 -> X1."""
    n = X0.shape[0]; nb = [[] for _ in range(n)]
    for i, j in E: nb[i].append(j); nb[j].append(i)
    A = np.full(n, np.nan)
    for i in range(n):
        if len(nb[i]) < 3: continue
        P = X0[nb[i]] - X0[i]; Q = X1[nb[i]] - X1[i]
        M = np.linalg.lstsq(P, Q, rcond=None)[0]; s = np.linalg.svd(M, compute_uv=False)
        if s[1] > 0: A[i] = s[0] / s[1]
    return A


def p_swap(a):
    for k in range(len(A_BINS) - 1):
        if a < A_BINS[k + 1]: return A_P[k]
    return A_P[-1]


def run(S, depths, period, out, label, zthr=0.6, log=print, nullruns=True, img_seeds=10, window=False, psm=0.10, dsm=None, dark=False, bandpass=False, zthr_=None, tracker='link'):
    global BANDPASS; BANDPASS = bandpass
    if zthr_ is not None: zthr = zthr_
    K, N, _ = S.shape; edge = max(2, int(0.3 * period))   # small border cut; the interior rule removes border cells
    t0 = time.time()
    Z = np.stack([norm_img(S[k], psm * period, 1.2 * period) for k in range(K)])
    if dark: Z = -Z                                                   # cells are the dark centres (retina: bright honeycomb walls)
    dsm = DSM if dsm is None else dsm
    Z = ndi.gaussian_filter1d(Z, dsm, axis=0)                        # light depth smoothing (dsm shells)
    dets, labs = [], []
    for k in range(K):
        P, lab = detect(Z[k], period, zthr, edge); dets.append(P); labs.append(lab)
        if k % max(1, K // 10) == 0: log(f'PROGRESS {0.5 * k / K:.2f} {label} detect shell {k}/{K} ({len(P)} found, {time.time() - t0:.0f} s)')
    if window:                                                        # longest depth run where detections persist step to step
        f = []
        for k in range(K - 1):
            if len(dets[k]) == 0 or len(dets[k + 1]) == 0: f.append(0.0); continue
            dd = np.linalg.norm(dets[k][:, None] - dets[k + 1][None], axis=2).min(1)
            m = ((dets[k] > period) & (dets[k] < N - 1 - period)).all(1)
            f.append(float(np.mean(dd[m] < 0.15 * period)) if m.any() else 0.0)
        f = ndi.uniform_filter1d(np.array(f), 3); ok = f >= 0.8
        best, cur, b0 = (0, 0), 0, 0
        for k, v in enumerate(ok):
            if v:
                if cur == 0: b0 = k
                cur += 1
                if cur > best[1] - best[0]: best = (b0, b0 + cur)
            else: cur = 0
        k0, k1 = best[0], best[1] + 1
        if k1 - k0 < 12:
            log(f'PROGRESS 0.55 {label}: no persistent window (longest {k1 - k0} shells)'); return None, None, None, None, labs, dets
        S = S[k0:k1]; Z = Z[k0:k1]; depths = depths[k0:k1]; dets = dets[k0:k1]; labs = labs[k0:k1]; K = k1 - k0
        log(f'PROGRESS 0.52 {label}: persistent window {depths[0]:.0f}-{depths[-1]:.0f} um ({K} shells)')
    fstat = None
    if tracker == 'follow':
        tracks, tidx, ftrust, fothers, fstat = follow_link(Z, dets, period); full = list(range(len(tracks)))
    else:
        tracks, tidx = link(dets, 0.3 * period)
        full = [i for i, T in enumerate(tracks) if (~np.isnan(T[:, 0])).sum() >= 0.8 * K and np.isnan(T[:GAP + 1, 0]).sum() <= GAP
                and np.isnan(T[-GAP - 1:, 0]).sum() <= GAP and max_gap(T) <= GAP]                 # ends may miss up to GAP shells (held constant)
    if len(full) < 8:
        log(f'PROGRESS 0.55 {label}: only {len(full)} tracks span the layer: no count'); return None, None, None, None, labs, dets
    X = np.stack([fill(tracks[i]) for i in full], 1)                  # (K, n, 2)
    n = X.shape[1]
    # interior: away from the chart border at every depth, never on the hull
    inb = ((X > 1.0 * period) & (X < N - 1 - 1.0 * period)).all(2).all(0)
    onhull = np.zeros(n, bool)
    for k in range(K): _, h = delaunay_edges(X[k]); onhull[list(h)] = True
    interior = inb & ~onhull
    # trusted cells: the same track is found when linking bottom-up (forward-backward consistency, >= 95% of its detections)
    # and it never jumps (max deviation from its depth-smoothed path < 0.25 period). Only edges between trusted interior cells
    # are counted; all spanning cells stay in the Delaunay geometry.
    owner = {}
    if tracker == 'follow': confirmed = np.asarray(ftrust, bool); bidx = []    # seed-plane agreement + no merge (follow_link)
    else:
        btr, bidx = link(dets[::-1], 0.3 * period); confirmed = np.zeros(n, bool)
    for b, I in enumerate(bidx):
        for kk, j in enumerate(I[::-1]):
            if j >= 0: owner[(kk, int(j))] = b
    for c_, t in enumerate(full if tracker != 'follow' else []):
        ids = [owner.get((kk, int(j))) for kk, j in enumerate(tidx[t]) if j >= 0]
        if ids:
            vals, cnts = np.unique([-1 if v is None else v for v in ids], return_counts=True)
            confirmed[c_] = cnts.max() / len(ids) >= 0.95 and vals[np.argmax(cnts)] >= 0
    sm0 = ndi.gaussian_filter1d(X, SM_UM / (depths[1] - depths[0]), axis=0, mode='nearest')
    nojump = np.linalg.norm(X - sm0, axis=2).max(0) < 0.25 * period
    interior_all = interior.copy(); interior = interior & confirmed & nojump
    log(f'PROGRESS 0.55 {label}: {len(tracks)} tracks, {n} span the layer, {interior_all.sum()} interior, {interior.sum()} trusted '
        f'(confirmed {int(confirmed[interior_all].sum())}, no jump {int(nojump[interior_all].sum())})')
    used = [set(int(tidx[t][k]) for t in full if tidx[t][k] >= 0) for k in range(K)]
    extras = [dets[k][[j for j in range(len(dets[k])) if j not in used[k]]] for k in range(K)]
    tracked_share = float(np.mean([len(used[k]) / max(1, len(dets[k])) for k in range(K)]))
    # tracked share in the interior zone (more than 1.5 periods from the plane border): detections within 0.3 period of a
    # confirmed track, and of a trusted interior track
    def zone_share(sel):
        v = []
        for k in range(K):
            D = dets[k]
            if not len(D): continue
            z = ((D > 1.5 * period) & (D < N - 1 - 1.5 * period)).all(1)
            if sel.sum() and z.sum():
                d = np.linalg.norm(D[z][:, None] - X[k][sel][None], axis=2).min(1); v.append(float(np.mean(d < 0.3 * period)))
        return float(np.mean(v)) if v else 0.0
    tracked_share_zone = zone_share(confirmed); trusted_share_zone = zone_share(interior)
    raw = count_swaps(X, interior, extras, period)
    sm = sm0
    smooth = count_swaps(sm, interior, extras, period)
    noise = float(np.sqrt(np.mean((X - sm)[:, interior] ** 2)))      # rms per coordinate, px
    # touching regions: adjacency of watershed regions for tracks seen (not interpolated) in the shell
    def reg_edges(k):
        R = region_adjacency(labs[k]); inv = {tidx[t][k]: c for c, t in enumerate(full) if tidx[t][k] >= 0}
        return {tuple(sorted((inv[a], inv[b]))) for a, b in R if a in inv and b in inv and interior[inv[a]] and interior[inv[b]]}, set(inv.values())
    def reg_maj(rng):
        cnt = {}; seen = {}
        for k in rng:
            E, vis = reg_edges(k)
            for e in E: cnt[e] = cnt.get(e, 0) + 1
            for v in vis: seen[v] = seen.get(v, 0) + 1
        return {e for e, c in cnt.items() if c > len(rng) / 2}, {v for v, c in seen.items() if c > len(rng) / 2}
    rt, vt = reg_maj(range(0, W)); rb, vb = reg_maj(range(K - W, K)); both = vt & vb
    rt = {e for e in rt if e[0] in both and e[1] in both}; rb = {e for e in rb if e[0] in both and e[1] in both}
    region = dict(top_edges=len(rt), lost=len(rt - rb), gained=len(rb - rt), share=len(rt - rb) / max(1, len(rt)),
                  agree_with_delaunay_top=len(rt & dense_edges(X[0], extras[0], period)[0]) / max(1, len(rt)))
    log(f'PROGRESS 0.65 {label}: raw lost {raw["lost"]}/{raw["top_edges"]}, smoothed lost {smooth["lost"]}/{smooth["top_edges"]}, noise {noise:.2f} px')
    # null: straight columns at the smoothed top positions + iid jitter of the measured noise
    if not nullruns:
        return dict(raw=raw, smoothed=smooth, noise_px=noise, spanning=n, interior=int(interior.sum()), interior_untrusted=int(interior_all.sum()),
                    tracked_share=tracked_share, tracked_share_zone=tracked_share_zone, trusted_share_zone=trusted_share_zone, follow=fstat,
                    depth_um=[float(depths[0]), float(depths[-1])]), X, sm, interior, labs, dets
    rng = np.random.default_rng(7); nulls = []; nulls_sm = []
    base = np.repeat(sm[:1], K, 0)
    ex0 = [extras[0]] * K                                             # straight columns: the untracked cells stay put too
    zero = count_swaps(base, interior, ex0, period)
    res_all = (X - sm)[:, interior]                                   # measured residual series (K, m, 2): tails + depth correlation kept
    m = res_all.shape[1]
    for s in range(50):
        pick = rng.integers(0, m, n); shift = rng.integers(0, K, n); ang = rng.uniform(0, 2 * np.pi, n)
        Rr = np.stack([np.roll(res_all[:, pick[i]], shift[i], axis=0) for i in range(n)], 1)
        c, si = np.cos(ang), np.sin(ang)
        Rr = np.stack([c * Rr[..., 0] - si * Rr[..., 1], si * Rr[..., 0] + c * Rr[..., 1]], -1)
        J = base + Rr
        nulls.append(count_swaps(J, interior, ex0, period)['lost'])
        nulls_sm.append(count_swaps(ndi.gaussian_filter1d(J, SM_UM / (depths[1] - depths[0]), axis=0, mode='nearest'), interior, ex0, period)['lost'])
    # cells to render in the image null: the spanning columns (top positions) + every other track seen in >= 30% of the shells
    # (they stay in the images and can take over a track, so the null must contain them too)
    others = [np.nanmean(tracks[i], 0) for i, T in enumerate(tracks) if i not in set(full) and (~np.isnan(T[:, 0])).sum() >= 0.3 * K]
    if tracker == 'follow': others = list(fothers)
    P0 = sm[0]
    if others:
        O = np.array(others); dmin = np.linalg.norm(O[:, None] - P0[None], axis=2).min(1); O = O[dmin > 0.5 * period]
        P0 = np.r_[P0, O]
    imgnull = image_null(P0, K, N, period, depths, noise, seeds=img_seeds, log=log, label=label, psm=psm, dsm=dsm, bandpass=bandpass, zthr=zthr, tracker=tracker)
    log(f'PROGRESS 0.9 {label}: null raw {np.mean(nulls):.2f}+-{np.std(nulls):.2f}, null smoothed {np.mean(nulls_sm):.2f}+-{np.std(nulls_sm):.2f}')
    # anisotropy and model expectation on the smoothed tracks
    Etop, _ = dense_edges(sm[0], extras[0], period); Ein = [e for e in Etop if interior[e[0]] and interior[e[1]]]
    A = anisotropy(sm[0], sm[-1], Etop)
    eA = [max(A[i], A[j]) for i, j in Ein if np.isfinite(A[i]) and np.isfinite(A[j])]
    expect = float(sum(p_swap(a) for a in eA))
    lost_sm = set(tuple(e) for e in smooth['lost_edges'])
    swapA = [max(A[i], A[j]) for i, j in Ein if (i, j) in lost_sm and np.isfinite(A[i]) and np.isfinite(A[j])]
    res = dict(label=label, psm=psm, dsm=dsm, dark=dark, bandpass=bandpass, zthr=zthr, depth_um=[float(depths[0]), float(depths[-1])], shells=K, period_px=period,
               detections_per_shell=[int(len(d)) for d in dets[::max(1, K // 10)]], tracks=len(tracks), spanning=n,
               interior=int(interior.sum()), interior_before_trust=int(interior_all.sum()), tracked_share=tracked_share, confirmed=int(confirmed[interior_all].sum()),
               tracker=tracker, follow=fstat, tracked_share_zone=tracked_share_zone, trusted_share_zone=trusted_share_zone,
               nojump=int(nojump[interior_all].sum()), noise_px=noise, noise_over_period=noise / period,
               raw=raw, smoothed=smooth, region=region, control_straight_noiseless_lost=zero['lost'],
               null_raw_mean=float(np.mean(nulls)), null_raw_sd=float(np.std(nulls)), null_raw_max=int(np.max(nulls)),
               image_null=imgnull,
               null_smoothed_mean=float(np.mean(nulls_sm)), null_smoothed_sd=float(np.std(nulls_sm)), null_smoothed_max=int(np.max(nulls_sm)),
               A_median=float(np.nanmedian(A[interior])), A_p90=float(np.nanpercentile(A[interior], 90)),
               model_expected_lost=expect, A_of_swapped_edges=[float(a) for a in swapA])
    if out:
        np.savez_compressed(out.replace('.json', '_tracks.npz'), X=X, sm=sm, interior=interior, depths=depths, A=A)
        json.dump(res, open(out, 'w'), indent=1)
    return res, X, sm, interior, labs, dets


def max_gap(T):
    m = np.isnan(T[:, 0]); g = 0; best = 0
    for v in m:
        g = g + 1 if v else 0; best = max(best, g)
    return best


def render(Pk, N, period, rng, snr=1.5, blob=0.2):
    """One shell image: Gaussian blobs (sigma blob*period) at positions Pk + image noise."""
    yy, xx = np.indices((N, N)); img = np.zeros((N, N), np.float32); r = int(period * 0.6)
    for p in Pk:
        i0, j0 = int(p[0]), int(p[1])
        if i0 < -r or j0 < -r or i0 > N + r or j0 > N + r: continue
        sl = (slice(max(0, i0 - r), min(N, i0 + r)), slice(max(0, j0 - r), min(N, j0 + r)))
        img[sl] += np.exp(-((yy[sl] - p[0]) ** 2 + (xx[sl] - p[1]) ** 2) / (2 * (blob * period) ** 2))
    return img + rng.normal(0, 1 / snr, img.shape) * 0.5


def image_null(P0, K, N, period, depths, target_noise, seeds=10, log=print, label='', psm=0.10, dsm=None, bandpass=False, zthr=0.6, tracker='link'):
    """Null by images: straight columns at P0 (no rearrangement) + iid per-shell jitter, rendered and run through the same
    detection / linking / counting. Jitter calibrated so the pipeline's measured residual equals target_noise."""
    sj = 1.9 * target_noise; out = []
    for it in range(2):                                              # calibration of the jitter
        rng = np.random.default_rng(100 + it)
        S = np.stack([render(P0 + rng.normal(0, sj, P0.shape), N, period, rng) for _ in range(K)])
        r = run(S, depths, period, None, label + ' null-calibration', log=lambda *a: None, nullruns=False, psm=psm, dsm=dsm, bandpass=bandpass, zthr_=zthr, tracker=tracker)[0]
        sj *= target_noise / max(r['noise_px'], 1e-6)
    for sd in range(seeds):
        rng = np.random.default_rng(200 + sd)
        S = np.stack([render(P0 + rng.normal(0, sj, P0.shape), N, period, rng) for _ in range(K)])
        r = run(S, depths, period, None, label + ' null', log=lambda *a: None, nullruns=False, psm=psm, dsm=dsm, bandpass=bandpass, zthr_=zthr, tracker=tracker)[0]
        out.append((r['raw']['lost'], r['raw']['top_edges'], r['smoothed']['lost'], r['smoothed']['top_edges'], r['noise_px']))
        log(f'PROGRESS {0.9 + 0.09 * sd / seeds:.2f} {label}: image null seed {sd}: raw {out[-1][0]}/{out[-1][1]}, smoothed {out[-1][2]}, noise {out[-1][4]:.2f}')
    o = np.array(out, float)
    return dict(jitter_px=float(sj), seeds=seeds, raw_share_mean=float((o[:, 0] / np.maximum(o[:, 1], 1)).mean()),
                raw_share_sd=float((o[:, 0] / np.maximum(o[:, 1], 1)).std()), smoothed_share_mean=float((o[:, 2] / np.maximum(o[:, 3], 1)).mean()),
                smoothed_share_sd=float((o[:, 2] / np.maximum(o[:, 3], 1)).std()), raw_lost=o[:, 0].tolist(), raw_top=o[:, 1].tolist(),
                smoothed_lost=o[:, 2].tolist(), smoothed_top=o[:, 3].tolist(), noise=o[:, 4].tolist())


def synth_stack(kind, K=60, N=300, period=32.0, seed=3, snr=1.5, A=2.0, jit=0.12):
    """Rendered blob images on a hexagonal lattice: 'straight' (same at every depth), 'jitter' (static disorder 0.15 period + iid jitter
    jit period per shell, no rearrangement: must give the null rate), 'shear' (compressed across rows to anisotropy A at the bottom: must swap about 1/3 of edges)."""
    rng = np.random.default_rng(seed)
    a1 = np.array([1.0, 0.0]); a2 = np.array([0.5, 3 ** 0.5 / 2])
    pts = np.array([i * a1 + j * a2 for i in range(-20, 21) for j in range(-20, 21)]) * period
    pts = pts + N / 2; pts = pts[((pts > -period) & (pts < N + period)).all(1)]
    S = np.zeros((K, N, N), np.float32); yy, xx = np.indices((N, N))
    base_dis = rng.normal(0, 0.15 * period, pts.shape)               # static disorder: near-tied edges, so jitter alone can flip some
    for k in range(K):
        P = pts.copy()
        if kind == 'jitter': P = P + base_dis + rng.normal(0, jit * period, P.shape)
        if kind == 'shear':
            f = k / (K - 1); s = A ** f; c = N / 2
            P = np.c_[c + (P[:, 0] - c) * s ** 0.5, c + (P[:, 1] - c) / s ** 0.5]   # area kept; compress across rows (axis 1)
        S[k] = render(P, N, period, rng, snr)
    return S


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'synthetic':
        out = sys.argv[2]; allres = {}
        for kind in ['straight', 'shear'] + [f'jitter{s}' for s in range(5)]:
            S = synth_stack(kind.rstrip('0123456789'), seed=3 + (int(kind[6:]) if kind.startswith('jitter') else 0)); d = np.arange(len(S)) * 1.0
            r = run(S, d, 32.0, out.replace('.json', f'_{kind}.json'), 'synthetic ' + kind, img_seeds=6)[0]
            allres[kind] = {k: r[k] for k in ['spanning', 'interior', 'noise_px', 'null_raw_mean', 'null_smoothed_mean', 'control_straight_noiseless_lost', 'A_median']}
            allres[kind].update(img_null_raw=r['image_null']['raw_share_mean'], img_null_raw_sd=r['image_null']['raw_share_sd'], img_null_sm=r['image_null']['smoothed_share_mean'], null_raw_sd=r['null_raw_sd'], raw_lost=r['raw']['lost'], raw_top=r['raw']['top_edges'], smooth_lost=r['smoothed']['lost'], region_lost=r['region']['lost'], region_top=r['region']['top_edges'])
            print(kind, json.dumps(allres[kind]), flush=True)
        json.dump(allres, open(out, 'w'), indent=1)
        sys.exit(0)
    stack, label, d0, d1, period, out = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), sys.argv[6]
    S = np.load(stack, mmap_mode='r'); m = np.load(stack.replace('.npy', '_meta.npy'))
    dep = m[0] + m[1] * np.arange(S.shape[0]); sel = (dep >= d0 - 1e-6) & (dep <= d1 + 1e-6)
    r = run(np.asarray(S[sel], np.float32), dep[sel], period, out, label)[0]
    print(json.dumps({k: v for k, v in r.items() if k not in ('raw', 'smoothed')}, default=str)[:1500])
    print('raw', {k: v for k, v in r['raw'].items() if not k.endswith('edges')}); print('smoothed', {k: v for k, v in r['smoothed'].items() if not k.endswith('edges')})
