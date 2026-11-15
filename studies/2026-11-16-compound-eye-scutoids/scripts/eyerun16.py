#!/usr/bin/env python3
"""Second scutoid trace: butterfly eye gw16 (Paukner et al. 2024, BossDB paukner2024, butterfly_retina_xray_grp03_gw16), an
apposition eye whose columns run without a gap from the cone tips down through the retina. Study 2026-11-16-compound-eye-scutoids.
The 600 nm block (x 100-1900, y 200-2300, all z) stays on the compute machine, outside git (no licence stated).

Per patch (a point of the cornea sheet found by eyesurvey.py, with its inward normal; 150 um apart):
  planes      planes perpendicular to the cornea normal (eyeshells.make_fibre_stack with the measured axis switched off, see MAXDEV),
              1 um apart, 300 um wide; the pixel size shrinks with depth towards the cornea sphere centre, so the plane frame removes
              the even part of the convergence (a similarity, which never changes a neighbour set) and the lattice period stays
              about constant in pixels; one fresh stack per depth segment (SEGS) and one for the whole retina range (FULL);
  tracking    eyetrace.run with tracker='follow': cells detected in the top, middle and bottom planes are followed up and down
              by mean shift; a column counts only when two seed planes reproduce it and no other column merges with it;
  count       per segment, neighbour pairs (Delaunay of all detections) present at the top and absent at the bottom, between
              trusted interior columns; image null (straight columns + calibrated jitter, rendered and run through the same
              pipeline), bootstrap null, convergence anisotropy A per cell, the README model expectation;
  cornea      surface re-found at 0.6 um along the sheet normals in a disc about the patch; local quadric -> principal
              curvatures and U = (k1 - k2)/(k1 + k2) in 9 variants (3 disc radii x 3 surface thresholds) for its uncertainty;
  overlays    for every lost pair, small crops of five planes through the segment with the tracks (kept on the compute machine,
              for inspection by eye).
Synthetic controls (straight, shear past sqrt3, jittered at two strengths x 5 seeds) run through the same tracker and settings.
Every cell and change is counted once, in the patch whose top-plane centre is nearest in 3D (tile partition, eyesum16.py).
Usage: eyerun16.py OUTDIR WORKERS IMG_SEEDS [pilot]"""
import sys, os, json, time, numpy as np
from multiprocessing import Pool
from scipy import ndimage as ndi
from scipy.spatial import cKDTree
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import eyeshells as es, eyetrace as et

E = os.environ.get('EYE_DATA', os.path.expanduser('~/eye-data')) + '/'
VOL = E + 'gw16-s600blk.npy'; SHEET = E + 'g16/gw16-sheet.npy'
OFF = np.array([0.0, 200.0, 100.0])           # block origin (z, y, x) in the full 600 nm volume
if __name__ == '__main__':                       # worker processes (spawn / forkserver) read the settings from the environment
    os.environ.update(EYE16_OUT=sys.argv[1], EYE16_WORKERS=sys.argv[2], EYE16_SEEDS=sys.argv[3],
                      EYE16_PILOT='1' if len(sys.argv) > 4 and sys.argv[4] == 'pilot' else '0')
OUT = os.environ.get('EYE16_OUT'); WORKERS = int(os.environ.get('EYE16_WORKERS', 1)); SEEDS = int(os.environ.get('EYE16_SEEDS', 3))
PILOT = os.environ.get('EYE16_PILOT') == '1'
D0, D1 = 60.0, 345.0                       # depth range of the plane stack below the cornea (um)
NPL, PX = 600, 0.5                          # plane size (px) and pixel size at the top (um): 300 um, about 22 lattice periods
SPACING = 150.0                             # patch spacing on the cornea (um)
# detection settings from the pilots on patch 0 (README): cones are bright discs; the retina shows bright column cores best with
# stronger in-plane (0.25 period) and depth (8 um) smoothing; dark centres and weaker smoothing tracked 50-58% there
DET_CONE = dict(psm=0.12, dark=False, bandpass=True, zthr_=0.0, dsm=3.0)
DET_RET = dict(psm=0.25, dark=False, bandpass=True, zthr_=0.0, dsm=8.0)
def per_um(d): return 13.5 * (961 - d) / (961 - 80)   # lattice spacing: 13.5 um measured at 80 um (pilot), shrinking towards the sphere centre
R_CONV = 961.0                                # cornea reference sphere radius (survey, rms 7.9 um)
# depth segments (um below the cornea): the clean cone window, then the continuous retina range of the survey cut in ~55 um pieces;
# the cone tips (92-120 um) are kept as their own segment and reported, though they hold little lattice signal
SEGS = [(68, 92, 'cone'), (92, 120, 'tips'), (120, 175, 'retina'), (175, 230, 'retina'), (230, 285, 'retina'), (285, 340, 'retina')]
FULL = (120, 340)
# plane frame: the structure-tensor axis follows the layering at the cone tips and in ring-artefact bands (pilot: cone window tracked
# 0.39 in the column-following frame against 0.88 on the fixed cornea normal; retina 0.51-0.63 either way), so the planes stay
# perpendicular to the cornea sheet normal (a measured axis is accepted only within MAXDEV of it, i.e. never)
MAXDEV = 0.001
if PILOT: SEGS = [SEGS[0], SEGS[2]]
T0 = time.time()


def log(m): print(m, flush=True)


def fft_period(img):
    """Lattice spacing a (px) from the strongest ring of the power spectrum (row spacing x 2/sqrt3)."""
    N = img.shape[0]; a = img - ndi.gaussian_filter(img, 40); w = np.hanning(N)[:, None] * np.hanning(N)[None]
    P = np.abs(np.fft.fft2(a * w)) ** 2; f = np.fft.fftfreq(N); fr = np.hypot(*np.meshgrid(f, f, indexing='ij'))
    bins = np.linspace(1 / 90, 1 / 10, 80); h, _ = np.histogram(fr, bins, weights=P); n, _ = np.histogram(fr, bins); h = h / np.maximum(n, 1)
    i = np.argmax(h); return 2 / 3 ** 0.5 / ((bins[i] + bins[i + 1]) / 2), float(h[i] / np.median(h))


def sheet():
    A = np.load(SHEET); return A[:, :3] * 4 + 1.5 - OFF, A[:, 3:6]           # 600 nm voxels in the block, inward normals


def patch_points(P, N, shape):
    """Sheet points whose whole plane stack stays inside the block, thinned to SPACING by greedy farthest-point sampling."""
    half = NPL * PX / 2 / 0.6 * 1.05 + 60
    ok = np.ones(len(P), bool)
    for d in (D0 - 20, D1 + 10):
        Q = P + N * d / 0.6; ok &= np.all((Q > half) & (Q < np.array(shape) - 1 - half), axis=1)
    idx = np.flatnonzero(ok); rng = np.random.default_rng(5); order = rng.permutation(idx); taken = []
    for j in order:
        if taken and np.min(np.linalg.norm(P[taken] - P[j], axis=1)) < SPACING / 0.6: continue
        taken.append(j)
    c = P[idx].mean(0); taken.sort(key=lambda j: np.linalg.norm(P[j] - c))
    return taken


def cornea_U(V, p, n, P, N):
    """Cornea re-found at 0.6 um: rays along the sheet normal on a tangent grid (6 um) about p; the surface is the first sample
    (from 40 um outside) above a threshold; quadric fit in discs of 100, 132 and 180 um radius, thresholds at 30, 50 and 70% of
    the way from outside to lens grey. Returns U, radii and the variant spread."""
    t1 = np.cross(n, [1.0, 0, 0]); t1 /= np.linalg.norm(t1); t2 = np.cross(n, t1)
    g = np.arange(-180, 181, 6) / 0.6; GA, GB = [w.ravel() for w in np.meshgrid(g, g, indexing='ij')]
    keep = np.hypot(GA, GB) <= 180 / 0.6; GA, GB = GA[keep], GB[keep]
    # local normal of the sheet near each grid point, so rays stay perpendicular on a curved cap
    tr = cKDTree(P); base = p[None] + GA[:, None] * t1 + GB[:, None] * t2
    _, j = tr.query(base); nn = N[j]
    s = np.arange(-40, 40, 0.6) / 0.6
    pts = base[:, None, :] + (s[None, :, None] - ((base - P[j]) * nn).sum(1)[:, None, None]) * nn[:, None, :]
    shp = np.array(V.shape) - 1; inside = np.all((pts >= 0) & (pts <= shp), axis=2).all(1)
    if inside.mean() < 0.5: return None
    lo = np.floor(pts[inside].reshape(-1, 3).min(0)).astype(int); hi = np.ceil(pts[inside].reshape(-1, 3).max(0)).astype(int) + 2
    B = ndi.gaussian_filter(np.asarray(V[lo[0]:hi[0], lo[1]:hi[1], lo[2]:hi[2]], np.float32), 1.0)
    prof = ndi.map_coordinates(B, (pts[inside] - lo).reshape(-1, 3).T, order=1).reshape(inside.sum(), -1)
    out_g = np.median(prof[:, :15]); lens_g = np.percentile(prof, 95)
    res = []
    for fr_ in (0.3, 0.5, 0.7):
        thr = out_g + fr_ * (lens_g - out_g); above = prof > thr; first = np.where(above.any(1), above.argmax(1), -1)
        okr = first > 0; S_ = pts[inside][okr, first[okr]]                    # surface points (voxels)
        for rad in (100, 132, 180):
            d = S_ - p; x, y, h = d @ t1 * 0.6, d @ t2 * 0.6, -(d @ n) * 0.6
            m = np.hypot(x, y) <= rad
            if m.sum() < 60: continue
            M = np.c_[np.ones(m.sum()), x[m], y[m], x[m] ** 2, x[m] * y[m], y[m] ** 2]; co = np.linalg.lstsq(M, h[m], rcond=None)[0]
            r_ = h[m] - M @ co; ok2 = np.abs(r_) < 3 * np.median(np.abs(r_)) + 1e-9           # trim facet bumps / outliers once
            co = np.linalg.lstsq(M[ok2], h[m][ok2], rcond=None)[0]
            H = -np.array([[2 * co[3], co[4]], [co[4], 2 * co[5]]]); k = np.sort(np.linalg.eigvalsh(H))[::-1]
            if k[1] <= 0: continue
            v = np.linalg.eigh(H)[1][:, -1]
            res.append(dict(frac=fr_, radius_um=rad, k1=float(k[0]), k2=float(k[1]), U=float((k[0] - k[1]) / (k[0] + k[1])),
                            rms_um=float((h[m][ok2] - M[ok2] @ co).std()), n=int(ok2.sum()), dir1=(v[0] * t1 + v[1] * t2).tolist()))
    if not res: return None
    main = [r for r in res if r['frac'] == 0.5 and r['radius_um'] == 132]
    main = main[0] if main else res[0]; Us = [r['U'] for r in res]
    return dict(U=main['U'], radius1_um=1 / main['k1'], radius2_um=1 / main['k2'], rms_um=main['rms_um'], dir1=main['dir1'],
                U_min=float(min(Us)), U_max=float(max(Us)), U_sd=float(np.std(Us)), variants=res)


def to3d(pt, k, path, dirs, e1s, scale):
    e1 = e1s[k]; e2 = np.cross(dirs[k], e1); g = (np.asarray(pt, float) - (NPL - 1) / 2) * PX * scale[k] / 0.6
    return path[k] + g[..., :1] * e1 + g[..., 1:2] * e2


def overlays(S, sm, interior, lost, period, out):
    """Crops (3 periods wide) of the top, middle and bottom planes about each lost pair, tracks marked (for inspection)."""
    from PIL import Image, ImageDraw
    K = len(S); ks = [0, K // 4, K // 2, 3 * K // 4, K - 1]; h = int(1.6 * period); tiles = []
    for (i, j) in lost:
        row = []
        for k in ks:
            c = ((sm[k, i] + sm[k, j]) / 2).round().astype(int)
            a0, b0 = c - h
            img = np.pad(np.asarray(S[k], np.float32), h, mode='edge')[a0 + h:a0 + 3 * h, b0 + h:b0 + 3 * h]
            lo_, hi_ = np.percentile(img, [1, 99.5]); im = Image.fromarray((np.clip((img - lo_) / (hi_ - lo_ + 1e-6), 0, 1) * 255).astype(np.uint8)).convert('RGB')
            im = im.resize((4 * h, 4 * h)); dr = ImageDraw.Draw(im)
            near = np.flatnonzero(np.linalg.norm(sm[k] - c, axis=1) < 1.6 * period)
            for q in near:
                y, x = (sm[k, q] - (a0, b0)) * 2
                col = (230, 57, 70) if q in (i, j) else ((123, 211, 137) if interior[q] else (120, 120, 120))
                dr.ellipse([x - 3, y - 3, x + 3, y + 3], outline=col, width=2)
            yi, xi = (sm[k, i] - (a0, b0)) * 2; yj, xj = (sm[k, j] - (a0, b0)) * 2; dr.line([xi, yi, xj, yj], fill=(230, 57, 70), width=1)
            row.append(np.asarray(im))
        tiles.append(np.concatenate(row, 1))
    if tiles: Image.fromarray(np.concatenate(tiles, 0)).save(out)


def lost_info(sm, dets, period, lost):
    """For each lost pair (i, j): the two cells o1, o2 opposite it in the top Delaunay graph; the sum of the angles at o1 and o2
    over i-j at the top and at the bottom (180 deg = tie; above 180 the other diagonal is the Delaunay edge); the pair length in
    periods at both ends; and each cell's support (share of planes with a detection within 0.3 period of its track)."""
    from scipy.spatial import Delaunay
    tri = Delaunay(sm[0]); opp = {}
    for t in tri.simplices:
        for a in range(3):
            i, j, o = t[a], t[(a + 1) % 3], t[(a + 2) % 3]; opp.setdefault(tuple(sorted((int(i), int(j)))), []).append(int(o))
    def angsum(X, i, j, os_):
        tot = 0.0
        for o in os_:
            u, v = X[i] - X[o], X[j] - X[o]; tot += np.degrees(np.arccos(np.clip(u @ v / (np.linalg.norm(u) * np.linalg.norm(v) + 1e-12), -1, 1)))
        return tot
    def support(c):
        return float(np.mean([len(D) > 0 and np.linalg.norm(D - sm[k, c], axis=1).min() < 0.3 * period for k, D in enumerate(dets)]))
    out = []
    for i, j in lost:
        os_ = opp.get((min(i, j), max(i, j)), [])
        out.append(dict(pair=[int(i), int(j)], opposite=os_, top_sum=angsum(sm[0], i, j, os_) if len(os_) == 2 else None,
                        bottom_sum=angsum(sm[-1], i, j, os_) if len(os_) == 2 else None,
                        len_top=float(np.linalg.norm(sm[0, i] - sm[0, j]) / period), len_bottom=float(np.linalg.norm(sm[-1, i] - sm[-1, j]) / period),
                        support=[support(i), support(j)]))
    return out


def patch(args):
    j, idx = args
    V = np.load(VOL, mmap_mode='r'); P, N = sheet(); p_s, n_s = P[j], N[j]
    rec = dict(patch=idx, sheet_index=int(j), point_full_vox=(p_s + OFF).tolist(), normal=n_s.tolist()); lg = lambda m: log(f'[patch {idx}] {m}')
    rec['cornea'] = cornea_U(V, p_s, n_s, P, N)
    def stack(s0, s1):
        """Planes from s0 to s1 um below the cornea, started on the sheet normal at s0 (direction measured afresh per segment)."""
        dep = np.arange(s0, s1 + 1e-9, 1.0); sc = (R_CONV - dep) / (R_CONV - s0)   # even convergence towards the sphere centre, removed
        S_, path_, dirs_, rat_, e1s_ = es.make_fibre_stack(V, p_s + n_s * s0 / 0.6, n_s, s1 - s0, N=NPL, px_um=PX, max_dev_deg=MAXDEV, px_scale=sc)
        return S_, path_, dirs_, rat_, e1s_, sc, dep
    S, path, dirs, ratios, e1s, scale, depths = stack(FULL[0], FULL[1])
    if (S < 0).mean() > 0.001: rec['skip'] = 'planes leave the block'; return rec
    rec.update(period_um_top=per_um(SEGS[0][0]), period_um_bottom=per_um(FULL[1]),
               bend_deg=float(np.degrees(np.arccos(np.clip(dirs[0] @ dirs[-1], -1, 1)))),
               angle_to_normal_deg=float(np.degrees(np.arccos(np.clip(dirs[len(dirs) // 2] @ n_s, -1, 1)))),
               fft_period_um=[[float(depths[k]), float(fft_period(S[k])[0] * PX * scale[k])] for k in range(0, len(S), 20)])
    # whole-range following (no count): how many columns are reproduced from both ends through the continuous retina range
    period = per_um(FULL[0]) / PX
    rf = et.run(S, depths, period, None, f'p{idx} full', log=lambda *m: None, nullruns=False, tracker='follow', **DET_RET)[0]
    rec['full_range'] = None if rf is None else dict(depth_um=FULL, tracked_share_zone=rf['tracked_share_zone'], trusted_share_zone=rf['trusted_share_zone'],
                                                     follow=rf['follow'], trusted=rf['interior'], lost=rf['smoothed']['lost'], top=rf['smoothed']['top_edges'])
    del S
    segs = []
    for (s0, s1, layer) in SEGS:
        Sg, path, dirs, ratios, e1s, scale, dep = stack(s0, s1); K = len(Sg); a_, b_ = 0, K - 1; period = per_um(s0) / PX
        if 'top_centre3' not in rec: rec['top_centre3'] = to3d(np.array([(NPL - 1) / 2] * 2), 0, path, dirs, e1s, scale).tolist()
        det = DET_CONE if layer == 'cone' else DET_RET; seg = dict(depth_um=[s0, s1], layer=layer, period_px=period,
                                                                   dir_rejected=int(np.isnan(ratios[:, 0]).sum()), dir_measured=int(len(ratios)))
        r, X, sm, inter, labs, dets = et.run(Sg, dep, period, None, f'p{idx} {s0}-{s1}', log=lambda *m: None, img_seeds=SEEDS, tracker='follow', **det)
        if r is None or r['interior'] < 30:
            seg['skip'] = 'too few trusted columns' if r is None else f"too few trusted columns ({r['interior']})"; segs.append(seg); continue
        lost = [tuple(e) for e in r['smoothed']['lost_edges']]; gained = [tuple(e) for e in r['smoothed']['gained_edges']]
        Etop, _ = et.dense_edges(sm[0], None, period); Ein = [e for e in Etop if inter[e[0]] and inter[e[1]]]
        A = et.anisotropy(sm[0], sm[-1], Etop)
        M_all = np.linalg.lstsq(sm[0][inter] - sm[0][inter].mean(0), sm[-1][inter] - sm[-1][inter].mean(0), rcond=None)[0]
        s_ = np.linalg.svd(M_all, compute_uv=False)
        seg.update({k: v for k, v in r.items() if k not in ('raw', 'smoothed', 'A_of_swapped_edges', 'image_null', 'region', 'depth_um', 'label')})
        seg.update(raw_lost=r['raw']['lost'], raw_top=r['raw']['top_edges'], sm_lost=r['smoothed']['lost'], sm_top=r['smoothed']['top_edges'],
                   sm_gained=r['smoothed']['gained'], cells_changed=r['smoothed']['cells_changed'],
                   img_null_raw=r['image_null']['raw_share_mean'], img_null_raw_sd=r['image_null']['raw_share_sd'],
                   img_null_sm=r['image_null']['smoothed_share_mean'], img_null_sm_sd=r['image_null']['smoothed_share_sd'],
                   img_null_sm_lost=r['image_null']['smoothed_lost'], img_null_sm_top=r['image_null']['smoothed_top'],
                   boot_null_sm=r['null_smoothed_mean'], boot_null_sm_sd=r['null_smoothed_sd'], region_lost=r['region']['lost'], region_top=r['region']['top_edges'],
                   A_global=float(s_[0] / s_[1]),
                   A_of_lost=[float(max(A[x], A[y])) for x, y in lost if np.isfinite(A[x]) and np.isfinite(A[y])],
                   A_of_pairs=[float(max(A[x], A[y])) for x, y in Ein if np.isfinite(A[x]) and np.isfinite(A[y])],
                   cells3=to3d(sm[0][inter], a_, path, dirs, e1s, scale).tolist(),
                   edges3=[to3d((sm[0][x] + sm[0][y]) / 2, a_, path, dirs, e1s, scale).tolist() for x, y in Ein],
                   swap3=[[to3d((sm[0][x] + sm[0][y]) / 2, a_, path, dirs, e1s, scale).tolist(), to3d((sm[-1][x] + sm[-1][y]) / 2, b_, path, dirs, e1s, scale).tolist(),
                           [int(x), int(y)]] for x, y in lost])
        seg['lost_info'] = lost_info(sm, dets, period, lost)
        try: overlays(Sg, sm, inter, lost, period, f'{OUT}/p{idx}_{s0}_lost.png')
        except Exception as e: seg['overlay_error'] = str(e)
        np.savez_compressed(f'{OUT}/p{idx}_{s0}_planes.npz', top=Sg[0].astype(np.float16), mid=Sg[K // 2].astype(np.float16), bot=Sg[-1].astype(np.float16),
                            sm=sm, inter=inter, lost=np.array(lost).reshape(-1, 2), gained=np.array(gained).reshape(-1, 2), period=period)
        lg(f"{s0}-{s1} um: lost {seg['sm_lost']}/{seg['sm_top']}, image null {seg['img_null_sm'] * seg['sm_top']:.1f}, trusted {seg['interior']}, "
           f"tracked {seg['tracked_share_zone']:.2f}, {time.time() - T0:.0f} s")
        segs.append(seg)
    rec['segments'] = segs
    return rec


def synthetic(_):
    out = {}
    kinds = [('straight', 0, 0.0), ('shear', 0, 0.0)] + [(f'jitterL{s}', s, 0.05) for s in range(5)] + [(f'jitterH{s}', s, 0.12) for s in range(5)]
    if PILOT: kinds = kinds[:3]
    for kind, sd, jit in kinds:
        S = et.synth_stack(kind.rstrip('0123456789').rstrip('LH'), seed=3 + sd, jit=jit); d = np.arange(len(S)) * 1.0
        r = et.run(S, d, 32.0, None, 'synthetic ' + kind, log=lambda *a: None, img_seeds=max(3, SEEDS // 2), tracker='follow', **DET_RET)[0]
        out[kind] = dict(raw_lost=r['raw']['lost'], raw_top=r['raw']['top_edges'], sm_lost=r['smoothed']['lost'], sm_top=r['smoothed']['top_edges'],
                         noise_px=r['noise_px'], tracked_share_zone=r['tracked_share_zone'], trusted=r['interior'],
                         img_null_raw=r['image_null']['raw_share_mean'], img_null_raw_sd=r['image_null']['raw_share_sd'],
                         img_null_sm=r['image_null']['smoothed_share_mean'], img_null_sm_sd=r['image_null']['smoothed_share_sd'])
        log(f'synthetic {kind}: raw {r["raw"]["lost"]}/{r["raw"]["top_edges"]}, smoothed {r["smoothed"]["lost"]}, tracked share {r["tracked_share_zone"]:.2f}, '
            f'image null share {r["image_null"]["raw_share_mean"]:.3f}')
    return out


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    V = np.load(VOL, mmap_mode='r'); P, N = sheet(); pts = patch_points(P, N, V.shape)
    if PILOT: pts = pts[:1]
    jobs = [(j, i) for i, j in enumerate(pts)]
    log(f'PROGRESS 0.00 {len(jobs)} patches, {WORKERS} workers, image-null seeds {SEEDS}, depth {D0:.0f}-{D1:.0f} um')
    with Pool(WORKERS) as pool:
        syn_async = pool.map_async(synthetic, [0])
        recs = []
        for k, rec in enumerate(pool.imap_unordered(patch, jobs)):
            recs.append(rec); G = [g for g in rec.get('segments', []) if 'skip' not in g]
            log(f'PROGRESS {0.95 * (k + 1) / len(jobs):.2f} patch {rec["patch"]} {rec.get("skip", "")} lost {sum(g["sm_lost"] for g in G)}/{sum(g["sm_top"] for g in G)} '
                f'tracked {np.mean([g["tracked_share_zone"] for g in G]) if G else float("nan"):.2f} U {(rec.get("cornea") or {}).get("U", float("nan")):.2f}')
        syn = syn_async.get()[0]
    recs.sort(key=lambda r: r['patch'])
    ok = syn['straight']['raw_lost'] == 0 and 0.25 <= syn['shear']['raw_lost'] / max(1, syn['shear']['raw_top']) <= 0.42
    for tag in ['jitterL', 'jitterH']:
        ks = [k for k in syn if k.startswith(tag)]
        if not ks: continue
        obs = sum(syn[k]['raw_lost'] for k in ks); exp = sum(syn[k]['img_null_raw'] * syn[k]['raw_top'] for k in ks)
        sd = np.sqrt(sum((syn[k]['img_null_raw_sd'] * syn[k]['raw_top']) ** 2 for k in ks)) + 1e-9
        log(f'control {tag}: observed {obs} lost, image null {exp:.1f} +- {sd:.1f}')
        syn[tag + '_pooled'] = dict(observed=obs, null=exp, null_sd=sd)
    json.dump(dict(synthetic=syn, patches=recs, segments=SEGS, full_range=FULL, seconds=time.time() - T0), open(f'{OUT}/summary.json', 'w'), indent=1, default=float)
    log(f'controls straight/shear {"ok" if ok else "FAIL"}; {time.time() - T0:.0f} s')
    if ok: print('FINAL ok')
    else: print('FINAL FAIL controls')
