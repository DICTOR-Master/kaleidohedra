"""Space-time slicing at a tilt (README section "Space-time slicing at a tilt", 16 Nov 2026; DICTO's question: "are there
scutoid structures that transcend persistence or recurrence, is it possible that time is not running in a linear direction").

The frames (2D + time) are stacked into one 3D labelled block L[t, y, x]; each cell of the block is a 3D region. The block is then
cut by parallel planes whose normal makes an angle theta with the t-axis, in the coordinates (x / v, y / v, t) with a speed scale v:
  h(t, x) = t cos(theta) + (x / v) sin(theta).
Each plane is read as a tiling (cells = connected pieces of the 3D cells in the plane; the part of the plane outside the block is one
cell OUT, so a plane is a sphere tiling and Euler V - E + F = 2 must hold). Consecutive planes (step dt cos(theta) in h, i.e. one
frame at fixed x) are compared by the shared event logger (studies/2026-11-15-event-logger/scripts/eventlog.py, imported unchanged).
Pieces keep their identity from plane to plane by overlap within the same 3D cell (the 3D label is the identity; no cross-cell
matching). Events that involve OUT are boundary events; the counts compared across tilts are interior events whose place lies in a
core of the block (margins in x, y and t) that is the same for every tilt, per unit core volume.

Theory (README): in a generic sweep of a simple 3D cell complex whose cells each have one lowest and one highest point in the sweep
direction, the plane changes only at the complex's corners, by birth (1 of 4 edges down), swap (2) or death (3): the argument of
DICTO's #104 Theorem 1 and of studies/2026-11-15-tissue-null-models THEORY section 2. Births per volume = deaths per volume = cells
per volume, swaps = corners - births - deaths, in the bulk. For cells of any shape (stratified Morse theory): for every cell that does
not touch the block boundary, (pieces born) - (pieces of the same cell that join) = Euler characteristic of the cell, in every
generic direction. Both are checked here.

Usage:
  spacetime_tilt.py block KIND OUTDIR [opts]   KIND sunA | sunB | pv | mv  (sunA/sunB take order real | shuf:SEED)
  spacetime_tilt.py slice BLOCK.npz THETA_DEG V_KMS OUT.json
Data credit: Bifrost code, Gudiksen et al. 2011, A&A 531, A154; run en024048_hion, Carlsson, Hansteen, Gudiksen, Leenaarts & De
Pontieu 2016, A&A 585, A4; Hinode Science Data Centre Europe (sdc.uio.no). Seed paths of the moving-Voronoi block copied from
control_voronoi.py (this study). Watershed and labelling: scikit-image (van der Walt et al. 2014, PeerJ 2:e453; BSD licence)."""
import sys, os, json, time
import numpy as np
from collections import Counter, defaultdict
from scipy import ndimage as ndi
from scipy.spatial import cKDTree, Delaunay
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', '2026-11-15-event-logger', 'scripts'))
import tiles as TL
import eventlog as EL
from skimage.measure import label as sklabel, euler_number
from skimage.segmentation import watershed

DT, DX = 10.0, 24000.0 / 504          # s, km (Bifrost en024048_hion grid)
X0, NB = 0, 250                       # sub-box: pixels [X0, X0 + NB) in x and y (12 Mm)
MXY, MT = 24, 30                      # core margins: 24 px (1.1 Mm, about one cell), 30 frames (300 s)
AMIN = 5                              # pixels: smaller extra pieces of a cell are digital fragments


def order_of(order, n):
    if order == 'real': return np.arange(n)
    return np.random.default_rng(int(order.split(':')[1])).permutation(n)     # as trace3d.py / stepcal_prep.py


# ---------------------------------------------------------------- blocks
def block_sunA(data, order, thr):
    """3D cells: markers = 3D connected components (6-connectivity in t, y, x) of upflow above mean + thr std (per frame, smoothed
    1.5 px as the census), then a 3D marker watershed of the smoothed uz. Smoothing and threshold on the full periodic plane."""
    F = np.load(f'{data}/en024048_hion_uz_dz0.1.npy', mmap_mode='r')
    perm = order_of(order, F.shape[0])
    f = np.empty((F.shape[0], NB, NB), np.float32); mk = np.zeros(f.shape, bool)
    for k, j in enumerate(perm):
        g = ndi.gaussian_filter(np.asarray(F[j], np.float64), 1.5, mode='wrap')
        m = g > g.mean() + thr * g.std()
        f[k] = g[X0:X0 + NB, X0:X0 + NB]; mk[k] = m[X0:X0 + NB, X0:X0 + NB]
    lab, n = ndi.label(mk)
    sz = np.bincount(lab.ravel()); keep = sz >= 20; keep[0] = False
    info = dict(markers=int(n), markers_kept=int(keep.sum()), largest_marker_share=float(np.sort(sz[1:])[-1] / mk.sum()))
    lut = np.zeros(n + 1, np.int32); lut[keep] = np.arange(1, keep.sum() + 1)
    L = watershed(-f, lut[lab], connectivity=1).astype(np.int32)
    return L, info


def block_sunB(data, seg, order):
    """3D cells = census tracks: per-frame cells of the census segmentation, persistent labels by the census overlap rule."""
    S = np.load(seg, mmap_mode='r'); perm = order_of(order, S.shape[0])
    L = np.empty((S.shape[0], NB, NB), np.int32); prev, nid = None, 1
    for k, j in enumerate(perm):
        raw = np.asarray(S[j]).astype(np.int64)
        if prev is None:
            lab = raw.copy(); nid = int(raw.max()) + 1
        else:
            lab, _, _, nid = TL.match(prev, raw, nid)
        prev = lab; L[k] = lab[X0:X0 + NB, X0:X0 + NB]
    u, inv = np.unique(L, return_inverse=True)
    return (inv.reshape(L.shape) + 1).astype(np.int32), dict(tracks=int(len(u)))


def block_pv(seed, vc, nt):
    """3D Poisson-Voronoi in (x km, y km, t * vc km); intensity chosen so the cells are granule-sized (spacing about 1.2 Mm)."""
    rng = np.random.default_rng(seed)
    lam = 0.58e-9                                  # per km^3
    pad = 3000.0
    lo = np.array([-pad, -pad, -pad]); hi = np.array([NB * DX + pad, NB * DX + pad, nt * DT * vc + pad])
    n = rng.poisson(lam * np.prod(hi - lo)); P = rng.uniform(lo, hi, (n, 3))
    tt, yy, xx = np.meshgrid(np.arange(nt) * DT * vc, (np.arange(NB) + 0.5) * DX, (np.arange(NB) + 0.5) * DX, indexing='ij')
    _, idx = cKDTree(P).query(np.stack([xx.ravel(), yy.ravel(), tt.ravel()], 1), workers=4)
    L = (idx.reshape(nt, NB, NB) + 1).astype(np.int32)
    # exact corners: circumcentres of the Delaunay tetrahedra and their 4 neighbours (the corner's 4 edges)
    D = Delaunay(P)
    T = P[D.simplices]; a = T[:, 1:] - T[:, :1]; b = 0.5 * (a ** 2).sum(2)
    C = T[:, 0] + np.linalg.solve(a, b[..., None])[..., 0]
    info = dict(seeds=int(n), lam_per_km3=lam, vc=vc)
    return L, info, dict(C=C, nb=D.neighbors)


def pv_exact(ex, theta, v, vc, nt):
    """Exact interior counts by corner index i (edges going down) inside the core, for direction (theta, v)."""
    C, nb = ex['C'], ex['nb']; th = np.radians(theta)
    h = (C[:, 2] / vc) * np.cos(th) + (C[:, 0] / v) * np.sin(th)
    ok = (nb >= 0).all(1)
    i = np.where(ok[:, None], h[nb] < h[:, None], False).sum(1)
    x, y, t = C[:, 0] / DX - 0.5, C[:, 1] / DX - 0.5, C[:, 2] / vc
    core = ok & (x >= MXY) & (x < NB - MXY) & (y >= MXY) & (y < NB - MXY) & (t >= MT * DT) & (t <= (nt - 1 - MT) * DT)
    c = Counter(i[core].tolist())
    return {str(k): int(c.get(k, 0)) for k in range(5)}


def block_mv(nt):
    """2D Voronoi of 500 moving seeds (control_voronoi.py, seed 1, speed 1) in the 504-px periodic box, stacked; sub-box kept."""
    L0, N, speed = 504, 500, 1.0
    rng = np.random.default_rng(1)
    p0 = rng.uniform(0, L0, (N, 2))
    A = rng.normal(0, 1, (N, 2, 2)); w = rng.uniform(0.002, 0.01, (N, 2, 2)); ph = rng.uniform(0, 2 * np.pi, (N, 2, 2))
    pos = lambda t: (p0 + speed * (A * np.sin(w * t + ph)).sum(2) / np.maximum(w.mean(2), 1e-9) * 0.01) % L0
    vel = lambda t: speed * (A * w * np.cos(w * t + ph)).sum(2) / np.maximum(w.mean(2), 1e-9) * 0.01      # px per s
    yy, xx = np.indices((NB, NB)); grid = np.stack([yy.ravel(), xx.ravel()], 1) + 0.5 + X0
    L = np.empty((nt, NB, NB), np.int32); sp = []
    for k in range(nt):
        _, idx = cKDTree(pos(DT * k), boxsize=L0).query(grid % L0)
        L[k] = idx.reshape(NB, NB) + 1
        sp.append(np.hypot(*vel(DT * k).T) * DX)
    sp = np.concatenate(sp)
    return L, dict(seeds=N, seed_speed_kms_rms=float(np.sqrt((sp ** 2).mean())), seed_speed_kms_max=float(sp.max()),
                   seed_x_speed_kms_max=float(np.abs(np.concatenate([vel(DT * k)[:, 1] for k in range(nt)])).max() * DX))


def block_checks(L):
    """Is the block a simple cell complex? Cells connected and balls (voxel Euler number 1, 6-connectivity, for cells not touching
    the block boundary); corner windows (2 x 2 x 2 voxels with >= 4 cells) with exactly 4 cells (simple) or more; corner count in
    the core (connected clusters of corner windows)."""
    nt = L.shape[0]
    objs = ndi.find_objects(L)
    chi, ncomp, interior = Counter(), Counter(), 0
    for lab, sl in enumerate(objs, 1):
        if sl is None: continue
        if any(s.start == 0 or s.stop == L.shape[d] for d, s in enumerate(sl)):
            continue
        interior += 1
        m = L[sl] == lab
        ncomp[int(ndi.label(m)[1])] += 1
        chi[int(euler_number(np.pad(m, 1), connectivity=1))] += 1
    W = np.stack([L[a:nt - 1 + a, b:NB - 1 + b, c:NB - 1 + c] for a in (0, 1) for b in (0, 1) for c in (0, 1)], -1)
    W.sort(-1); nd = 1 + (np.diff(W, axis=-1) != 0).sum(-1)
    del W
    corner = nd >= 4
    cl, ncl = ndi.label(corner, structure=np.ones((3, 3, 3)))
    cen = np.array(ndi.center_of_mass(corner, cl, range(1, ncl + 1))) if ncl else np.zeros((0, 3))
    inc = ((cen[:, 0] >= MT) & (cen[:, 0] <= nt - 1 - MT) & (cen[:, 1] >= MXY) & (cen[:, 1] < NB - MXY) &
           (cen[:, 2] >= MXY) & (cen[:, 2] < NB - MXY)) if ncl else np.zeros(0, bool)
    mx = ndi.maximum(nd, cl, range(1, ncl + 1)) if ncl else np.zeros(0)
    cells_core = len(np.unique(L[MT:nt - MT, MXY:NB - MXY, MXY:NB - MXY]))
    return dict(cells=int(len([o for o in objs if o is not None])), cells_interior=interior,
                interior_connected=int(ncomp.get(1, 0)), interior_euler=dict((str(k), v) for k, v in sorted(chi.items())),
                corner_windows=int(corner.sum()), corner_windows_simple=int((nd == 4).sum()), corner_windows_5plus=int((nd >= 5).sum()),
                corners=int(ncl), corners_core=int(inc.sum()), corners_core_simple=int((np.asarray(mx)[inc] == 4).sum()) if ncl else 0,
                cells_meeting_core=int(cells_core), edge_windows=int((nd == 3).sum()))


def cmd_block(kind, out, opts):
    t0 = time.time(); os.makedirs(out, exist_ok=True)
    nt = 242; extra = None
    if kind == 'sunA':
        order, thr = opts[0], float(opts[1]); L, info = block_sunA(opts[2], order, thr); name = f'sunA_{order.replace(":", "")}_thr{thr}'
    elif kind == 'sunB':
        order = opts[0]; L, info = block_sunB(opts[1], opts[2], order); name = f'sunB_{order.replace(":", "")}'
    elif kind == 'pv':
        vc = float(opts[0]); L, info, extra = block_pv(int(opts[1]), vc, nt); name = f'pv_vc{vc}_s{opts[1]}'
    elif kind == 'mv':
        L, info = block_mv(nt); name = 'mv_s1'
    print(f'PROGRESS 0.5 block {name} built {time.time() - t0:.0f}s', flush=True)
    chk = block_checks(L)
    info.update(kind=kind, name=name, shape=list(L.shape), checks=chk, seconds=round(time.time() - t0, 1))
    if extra is not None:
        info['exact'] = {f'{th}_{v}': pv_exact(extra, th, v, info['vc'], nt) for th in (0, 15, 30) for v in (1.5, 3.0, 6.0)}
    np.savez_compressed(f'{out}/{name}.npz', L=L, info=json.dumps(info))
    print('BLOCK ' + json.dumps(info), flush=True); print('BLOCK_OK', name, flush=True)


# ---------------------------------------------------------------- slicing
def match_pieces(Cp, Sp, Cn, Sn, nid):
    """Pieces of the new plane keep the id of the piece of the SAME 3D cell they overlap most (mutual best, overlap counted only
    where the 3D label is the same in both planes). OUT is id 0 always."""
    m = (Sp == Sn) & (Sn > 0)
    K = np.int64(Cn.max() + 1)
    u, c = np.unique(Cp[m].astype(np.int64) * K + Cn[m], return_counts=True)
    old, new = u // K, u % K
    bp, bh = {}, {}
    for o, n, k in zip(old.tolist(), new.tolist(), c.tolist()):
        if k > bp.get(n, (0, -1))[1]: bp[n] = (o, k)
        if k > bh.get(o, (0, -1))[1]: bh[o] = (n, k)
    mp = {n: o for n, (o, k) in bp.items() if bh[o][0] == n}
    areas_n = np.bincount(Cn.ravel()); areas_o = np.bincount(Cp.ravel())
    for n in np.flatnonzero(areas_n).tolist():
        if n == 0: mp[0] = 0
        elif n not in mp: mp[n] = nid; nid += 1
    lut = np.zeros(K, np.int64)
    for n, v in mp.items(): lut[n] = v
    Pn = lut[Cn]
    kept = set(mp.values()) & set(np.flatnonzero(areas_o).tolist())
    born = set(mp.values()) - set(np.flatnonzero(areas_o).tolist())
    died = set(np.flatnonzero(areas_o).tolist()) - kept
    par, her = defaultdict(dict), defaultdict(dict)
    for o, n, k in zip(old.tolist(), new.tolist(), c.tolist()):
        pn = mp[n]
        if pn in born and k / areas_n[n] >= 0.01: par[pn][o] = k / areas_n[n]
        if o in died and k / areas_o[o] >= 0.01: her[o][pn] = k / areas_o[o]
    return Pn, born, died, dict(par), dict(her), nid


def cmd_slice(blockf, theta, v, outf):
    t0 = time.time()
    Z = np.load(blockf); L = Z['L']; binfo = json.loads(str(Z['info']))
    nt = L.shape[0]; th = np.radians(theta)
    ct, st = np.cos(th), np.sin(th)
    xkm = (np.arange(NB) + 0.5) * DX
    dh = DT * ct
    hmax = (nt - 1) * DT * ct + xkm[-1] * st / v
    hmin = xkm[0] * st / v * 0                    # h >= 0 at t = 0, x >= 0
    nsl = int(np.ceil((hmax - hmin) / dh)) + 1
    K = max(1, int(round(60.0 / DT)))              # flicker window: 6 planes = 60 s at fixed x
    yy = np.arange(NB)[:, None]; xx = np.arange(NB)[None, :]
    rows, truth, swaps, fails, euler_bad, multi = [], Counter(), [], Counter(), 0, 0
    per_cell = defaultdict(lambda: [0, 0])         # 3D label -> [pieces born, same-cell joins] (interior cells only matter)
    seen_label, prevT, prev = set(), None, None
    nid = 1; nfrag = 0; clumppat = Counter(); pend = []; twostep = 0
    tcore = (MT * DT, (nt - 1 - MT) * DT)
    core = lambda cy, cx, tt: (MXY <= cx < NB - MXY) and (MXY <= cy < NB - MXY) and (tcore[0] <= tt <= tcore[1])
    for k in range(nsl):
        hk = hmin + k * dh
        tx = (hk - xkm * st / v) / ct
        f = np.rint(tx / DT).astype(int); valid = (f >= 0) & (f < nt)
        S = L[np.clip(f, 0, nt - 1)[None, :], yy, xx] * valid[None, :]
        if not valid.any():
            continue
        Sp_ = np.pad(S, 1)                          # OUT border
        Cn = sklabel(Sp_, background=0, connectivity=1)
        # digital fragments: a piece under AMIN pixels that is not its cell's largest piece (a Voronoi or watershed cell drawn in
        # pixels can touch itself only at a pixel corner) is given to the nearest other cell; then the pieces are recomputed
        sz = np.bincount(Cn.ravel()); labc = np.zeros(len(sz), np.int64); labc[Cn.ravel()] = Sp_.ravel()
        big = np.zeros(int(labc.max()) + 1, np.int64); np.maximum.at(big, labc[1:], sz[1:])
        frag = (sz < AMIN) & (sz < big[labc]); frag[0] = False
        if frag.any():
            fm = frag[Cn]
            _, (iy, ix) = ndi.distance_transform_edt(fm, return_indices=True)
            Sp_ = Sp_[iy, ix]; nfrag += int(frag.sum())
            Cn = sklabel(Sp_, background=0, connectivity=1)
        if prev is None:
            Pn = Cn.astype(np.int64); nid = int(Pn.max()) + 1; born = set(np.unique(Pn).tolist()) - {0}; died = set(); par = her = {}
        else:
            Pn, born, died, par, her, nid = match_pieces(prev[0], prev[1], Cn, Sp_, nid)
        G = TL.graph(Pn)
        ids = np.unique(Pn)
        # 3D label and centroid of every piece
        flat = Pn.ravel(); lab_vals = np.zeros(int(ids.max()) + 1, np.int64); lab_vals[flat] = Sp_.ravel()
        IY, IX = np.indices(Pn.shape); cnt = np.bincount(flat); sy = np.bincount(flat, IY.ravel()); sx = np.bincount(flat, IX.ravel())
        cen = {int(i): (sy[i] / cnt[i] - 1, sx[i] / cnt[i] - 1) for i in ids if i}
        labs_now = Counter(int(lab_vals[i]) for i in ids if i)
        multi += sum(1 for c_ in labs_now.values() if c_ > 1)
        touch_out = {b for (a, b) in G['contacts'] if a == 0}
        T = EL.Tiling([str(i) for i in ids], [[str(a), str(b)] for (a, b), n in G['segs'].items() for _ in range(n)],
                      [[str(c) for c in cs] for cs, _ in G['junctions']], 2, 'sphere', k, loops=G['loops'],
                      parents={str(a): {str(b): s for b, s in d.items()} for a, d in par.items()},
                      heirs={str(a): {str(b): s for b, s in d.items()} for a, d in her.items()})
        chk = EL.check_tiling(T)
        if not chk.get('euler_ok', False): euler_bad += 1
        tloc = lambda cx: (hk - (cx + 0.5) * DX * st / v) / ct
        # truth events from 3D identity
        if prev is not None:
            labs_prev = prev[3]
            firsts, gone = set(), set()
            for b in born:
                L3 = int(lab_vals[b]); cy, cx = cen[b]; inn = core(cy, cx, tloc(cx)) and b not in touch_out
                if L3 not in seen_label and L3 not in firsts: kind = 'cell first appears'; firsts.add(L3)
                elif L3 not in labs_prev and L3 not in firsts: kind = 'cell reappears'; firsts.add(L3)
                elif L3 not in labs_prev: kind = 'new piece of a present cell'
                elif par.get(b): kind = 'piece splits off'
                else: kind = 'new piece of a present cell'
                if kind != 'piece splits off': per_cell[L3][0] += 1
                if inn: truth[kind] += 1
            for d in died:
                L3 = prev[4][d]; cy, cx = prev[5][d]; inn = core(cy, cx, prev[6](cx)) and d not in prev[7]
                if L3 not in labs_now and L3 not in gone: kind = 'cell vanishes'; gone.add(L3)
                elif L3 not in labs_now: kind = 'piece of a present cell vanishes'
                elif her.get(d): kind = 'pieces of one cell join'
                else: kind = 'piece of a present cell vanishes'
                if kind == 'pieces of one cell join': per_cell[L3][1] += 1
                if inn: truth[kind] += 1
            ev = EL.classify(prevT, T)
            ok, _, _ = EL.balance(prevT, T, ev)
            if not ok: fails['balance'] += 1
            for e in ev:
                cs = [int(c) for c in e['cells']]
                if 0 in cs or any(c in touch_out or c in prev[7] for c in cs): rows.append(('boundary', e['type'])); continue
                pts = [cen[c] if c in cen else prev[5][c] for c in cs]
                cy, cx = np.mean([p[0] for p in pts]), np.mean([p[1] for p in pts])
                inn = core(cy, cx, tloc(cx))
                rows.append(('core' if inn else 'interior', e['type']))
                if inn and e['type'] == 'clump': clumppat[e['pattern']] += 1
                # two-step swap through a four-fold pixel corner (as census.py): contact a-b lost, then c-d gained within 60 s
                if e['pattern'] == 'born 0 died 0 lost 1 gained 0':
                    pend.append((k, tuple(cs), inn))
                elif e['pattern'] == 'born 0 died 0 lost 0 gained 1':
                    c1, d1 = [str(c) for c in cs]
                    for j in range(len(pend) - 1, -1, -1):
                        k0, (a, b), inn0 = pend[j]
                        if k - k0 > K: continue
                        a1, b1 = str(a), str(b)
                        if len({a1, b1, c1, d1}) == 4 and {c1, d1} <= (T.nb[a1] & T.nb[b1]):
                            pend.pop(j)
                            if inn0: twostep += 1; swaps.append((k, 'two-step', tuple(sorted([a, b] + cs)), None))
                            break
                if e['type'] == 'swap' and inn:
                    swaps.append((k, e['pattern'], tuple(sorted(cs)), e))
        else:
            for b in born:
                per_cell[int(lab_vals[b])][0] += 1
        seen_label |= set(labs_now)
        prev = (Pn, Sp_, None, set(labs_now), {int(i): int(lab_vals[i]) for i in ids}, cen, tloc, touch_out)
        prevT = T
        if k % 50 == 0: print(f'PROGRESS {(k + 1) / nsl:.4f} plane {k + 1}/{nsl}', flush=True)
    # persistent swaps: a swap among the same four pieces repeated (undone) within K planes is flicker
    last = {}; flick = set()
    for j, (k, pat, cs, e) in enumerate(swaps):
        if cs in last and k - swaps[last[cs]][0] <= K: flick.add(j); flick.add(last[cs])
        last[cs] = j
    cnt = Counter((w, t) for w, t in rows)
    core_counts = {t: n for (w, t), n in cnt.items() if w == 'core'}
    vol = ((NB - 2 * MXY) * DX / 1000) ** 2 * ((nt - 1 - 2 * MT) * DT / 60)           # Mm^2 min
    # Morse check on cells that do not touch the block boundary: pieces born - joins = voxel Euler number (from the block stage)
    res = dict(block=binfo['name'], theta=theta, v=v, planes=nsl, step_h_s=dh, core_volume_Mm2min=vol,
               core_events=core_counts, core_swaps_twostep=twostep, core_swaps_all=len(swaps), core_swaps_persistent=len(swaps) - len(flick), core_clump_patterns=dict(clumppat.most_common(8)),
               truth_core=dict(truth), boundary_events=dict(Counter(t for w, t in rows if w == 'boundary')),
               interior_outside_core=dict(Counter(t for w, t in rows if w == 'interior')),
               planes_failing_euler=euler_bad, balance_failures=fails.get('balance', 0), planes_cells_in_several_pieces=multi, digital_fragments_reassigned=nfrag,
               seconds=round(time.time() - t0, 1))
    objs = ndi.find_objects(L); morse = Counter()
    for lab, sl in enumerate(objs, 1):
        if sl is None or any(s.start == 0 or s.stop == L.shape[d] for d, s in enumerate(sl)): continue
        chi = int(euler_number(np.pad(L[sl] == lab, 1), connectivity=1))
        b, j = per_cell.get(lab, [0, 0])
        morse['holds' if b - j == chi else 'fails'] += 1
    res['morse_interior_cells'] = dict(morse)
    with open(outf, 'w') as fo: json.dump(res, fo, indent=1)
    print('SLICE ' + json.dumps(res), flush=True)
    print('SLICE_OK', blockf, theta, v, flush=True)


if __name__ == '__main__':
    if sys.argv[1] == 'block': cmd_block(sys.argv[2], sys.argv[3], sys.argv[4:])
    elif sys.argv[1] == 'slice': cmd_slice(sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), sys.argv[5])
