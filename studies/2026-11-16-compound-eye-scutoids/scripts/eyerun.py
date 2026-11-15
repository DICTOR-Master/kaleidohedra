#!/usr/bin/env python3
"""Scutoid trace over many patches of butterfly eye gw05 (Paukner et al. 2024, BossDB paukner2024; 600 nm volume kept on the
compute machine, never in git). Study 2026-11-16-compound-eye-scutoids, ledger [267].

Per patch (axis given by angles (A, B) in the coarse eye frame):
  cone layer   radial shells about the fitted cornea sphere, depths 10-130 um, persistent window chosen automatically;
  retina       planes perpendicular to the locally measured column direction (structure tensor, re-measured every 10 um),
               stepped along it from 300 um below the cornea for 180 um (the rhabdoms run 11-24 deg off the sphere radius
               and bend, so radial shells cut them obliquely and the cells cannot be followed: tried and recorded);
  count        eyetrace.run: segmentation, tracks, neighbour changes (Delaunay and touching regions), bootstrap and image nulls,
               anisotropy A and the README model expectation;
  curvature    local quadric fit to the cornea (points within 0.2 rad of the patch axis): principal curvatures k1 >= k2,
               unevenness U = (k1 - k2) / (k1 + k2).
Swapped edges are mapped to eye-surface angles (A, B) for the figure.
Synthetic controls (straight, shear past sqrt3, jittered at two strengths x 5 seeds) run first.
Usage: eyerun.py OUTDIR WORKERS IMG_SEEDS [pilot]"""
import sys, os, json, time, numpy as np
from multiprocessing import Pool
from scipy import ndimage as ndi
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import eyeshells as es, eyetrace as et

E = '/home/dicto/eye-data/'
OUT = sys.argv[1]; WORKERS = int(sys.argv[2]); SEEDS = int(sys.argv[3]); PILOT = len(sys.argv) > 4 and sys.argv[4] == 'pilot'
os.makedirs(OUT, exist_ok=True)
T0 = time.time()


def log(m): print(m, flush=True)


def fft_period(img):
    """Lattice spacing a (px) from the strongest ring of the power spectrum (row spacing x 2/sqrt3)."""
    N = img.shape[0]; a = img - ndi.gaussian_filter(img, 40); w = np.hanning(N)[:, None] * np.hanning(N)[None]
    P = np.abs(np.fft.fft2(a * w)) ** 2; f = np.fft.fftfreq(N); fr = np.hypot(*np.meshgrid(f, f, indexing='ij'))
    bins = np.linspace(1 / 70, 1 / 12, 60); h, _ = np.histogram(fr, bins, weights=P); n, _ = np.histogram(fr, bins); h = h / np.maximum(n, 1)
    i = np.argmax(h); return 2 / 3 ** 0.5 / ((bins[i] + bins[i + 1]) / 2), float(h[i] / np.median(h))


def global_angles(v, frame):
    u0, g1, g2 = frame; v = v / np.linalg.norm(v, axis=-1, keepdims=True)
    t = np.arccos(np.clip(v @ u0, -1, 1)); x, y = v @ g1, v @ g2; r = np.hypot(x, y) + 1e-15
    return np.stack([t * x / r, t * y / r], -1)


def cornea_points():
    I = np.load(E + 'gw05-iso2400.npy'); s = np.load(E + 'sphere_iso.npy'); c, R = s[:3], s[3]
    S = ndi.gaussian_filter(I, 2.0); obj = ndi.binary_closing(S > 12, iterations=2)
    L, n = ndi.label(obj); obj = L == (np.argmax(np.bincount(L.ravel())[1:]) + 1); obj = ndi.binary_fill_holes(obj)
    bd = obj & ~ndi.binary_erosion(obj); lens = ndi.maximum_filter((ndi.gaussian_filter(I, 0.7) > 150).astype(np.uint8), size=13) > 0
    P = np.argwhere(bd & lens).astype(float); Z, Y, X = I.shape
    P = P[(P[:, 0] > 3) & (P[:, 0] < Z - 4) & (P[:, 1] > 3) & (P[:, 1] < Y - 4) & (P[:, 2] > 3) & (P[:, 2] < X - 4)]
    P = P[np.abs(np.linalg.norm(P - c, axis=1) - R) < 10]                       # band of +-24 um about the sphere (no shape bias)
    return (P * 4 + 1.5) * 0.6, (c * 4 + 1.5) * 0.6                              # um, full-volume frame


def curvature(Pum, cum, v, half=0.2):
    d = Pum - cum; nd = np.linalg.norm(d, axis=1); m = (d @ v) / nd > np.cos(half)
    if m.sum() < 200: return None
    t1 = np.cross(v, [1.0, 0, 0]); t1 /= np.linalg.norm(t1); t2 = np.cross(v, t1)
    x, y, h = d[m] @ t1, d[m] @ t2, d[m] @ v
    M = np.c_[np.ones_like(x), x, y, x * x, x * y, y * y]; co = np.linalg.lstsq(M, h, rcond=None)[0]
    res = h - M @ co
    H = -np.array([[2 * co[3], co[4]], [co[4], 2 * co[5]]]); k = np.sort(np.linalg.eigvalsh(H))[::-1]
    return dict(k1_per_mm=float(k[0] * 1000), k2_per_mm=float(k[1] * 1000), radius1_um=float(1 / k[0]), radius2_um=float(1 / k[1]),
                unevenness=float((k[0] - k[1]) / (k[0] + k[1])), points=int(m.sum()), rms_um=float(res.std()))


def swaps_xyz(res, X0, X1, to3d0, to3d1):
    """Lost edges -> midpoint 3D positions at the top and bottom of the layer."""
    out = []
    for i, j in res['smoothed']['lost_edges']:
        out.append([to3d0((X0[i] + X0[j]) / 2).tolist(), to3d1((X1[i] + X1[j]) / 2).tolist()])
    return out


def patch(args):
    A0, B0, idx = args
    V = np.load(E + 'gw05-s600.npy', mmap_mode='r'); fr = np.load(E + 'frame_iso.npy'); frame = (fr[:3], fr[3:6], fr[6:])
    c, R, uc, f1, f2 = es.patch_axes(A0, B0); rec = dict(patch=idx, A=A0, B=B0); lg = lambda m: log(f'[patch {idx}] {m}')
    # --- cone layer on radial shells
    dep = np.arange(10, 131, 1.0); N = 400
    S, meta = es.make_stack(V, A0, B0, dep, N)
    if (S < 0).mean() > 0.001: rec['skip'] = 'cone shells leave the volume'; return rec
    per, q = fft_period(S[int(np.argmin(np.abs(dep - 50)))]); rec['cone_period_px'] = per; rec['cone_fft_contrast'] = q
    if q < 20: rec['skip'] = f'no clear cone lattice (contrast {q:.0f})'; return rec
    r, X, sm, inter, labs, dets = et.run(S, dep, per, f'{OUT}/p{idx}_cone.json', f'p{idx} cone', log=lg, img_seeds=SEEDS, window=True)
    if r:
        D = es.chart_dirs(uc, f1, f2, N)
        def to3d_shell(pt, d):
            i, j = pt; ii, jj = int(np.clip(round(i), 0, N - 1)), int(np.clip(round(j), 0, N - 1)); return c + (R - d / 0.6) * D[ii, jj]
        d0, d1 = r['depth_um']
        r['swap_xyz'] = swaps_xyz(r, sm[0], sm[-1], lambda p: to3d_shell(p, d0), lambda p: to3d_shell(p, d1))
        r['cells_A'] = global_angles(np.array([to3d_shell(p, d0) - c for p in sm[0][inter]]), frame).tolist()
        json.dump(r, open(f'{OUT}/p{idx}_cone.json', 'w'), indent=1)
    rec['cone'] = {k: v for k, v in (r or {}).items() if k not in ('raw', 'smoothed', 'A_of_swapped_edges', 'swap_xyz', 'cells_A', 'image_null')}
    if r: rec['cone'].update(raw_lost=r['raw']['lost'], raw_top=r['raw']['top_edges'], sm_lost=r['smoothed']['lost'], sm_top=r['smoothed']['top_edges'],
                             cells_changed=r['smoothed']['cells_changed'], region_lost=r['region']['lost'], region_top=r['region']['top_edges'],
                             img_null_raw=r['image_null']['raw_share_mean'], img_null_raw_sd=r['image_null']['raw_share_sd'],
                             img_null_sm=r['image_null']['smoothed_share_mean'], img_null_sm_sd=r['image_null']['smoothed_share_sd'])
    del S
    # --- retina on fibre-following planes
    p0 = c + (R - 300 / 0.6) * uc; Nf = 500; px = 0.3
    lim = np.array(V.shape) - 1
    try:
        S, path, dirs, ratios, e1s = es.make_fibre_stack(V, p0, -uc, 180, N=Nf, px_um=px)
    except Exception as e:
        rec['retina_skip'] = f'fibre stack failed: {e}'; return rec
    if (S < 0).mean() > 0.001: rec['retina_skip'] = 'retina planes leave the volume'; return rec
    fq = [fft_period(S[k]) for k in range(10, 171, 10)]
    perf = float(np.median([f[0] for f in fq])) * 0.9
    rec['retina_period_px'] = perf; rec['retina_fibre_eig_ratio'] = float(np.median(ratios[:, 0]))
    rec['retina_bend_deg'] = float(np.degrees(np.arccos(np.clip(dirs[0] @ dirs[-1], -1, 1))))
    rec['retina_angle_to_radial_deg'] = float(np.degrees(np.arccos(np.clip(abs(dirs[len(dirs) // 2] @ uc), -1, 1))))
    def to3d_plane(pt, k):
        e1 = e1s[k]; e2 = np.cross(dirs[k], e1); g = (np.asarray(pt) - (Nf - 1) / 2) * px / 0.6
        return path[k] + g[0] * e1 + g[1] * e2
    segs = []; L = 20
    for a in range(20, 180 - L + 1, L):
        q = float(np.median([fft_period(S[k])[1] for k in range(a, a + L, 5)]))
        seg = dict(planes=[a, a + L - 1], depth_below_cornea_um=[float(R * 0.6 - np.linalg.norm(path[a] - c) * 0.6),
                                                                 float(R * 0.6 - np.linalg.norm(path[a + L - 1] - c) * 0.6)], fft_contrast=q)
        if q < 15: seg['skip'] = f'no clear lattice (contrast {q:.0f})'; segs.append(seg); continue
        r, X, sm, inter, labs, dets = et.run(S[a:a + L], np.arange(a, a + L) * 1.0, perf, None, f'p{idx} retina {a}', log=lambda *m: None,
                                             img_seeds=SEEDS, psm=0.15, dark=True, bandpass=True, zthr_=0.0)
        if r is None or r['interior'] < 30 or r['tracked_share'] < 0.3:
            seg['skip'] = 'too few trusted cells' if r is None else f"too few trusted cells ({r['interior']}, tracked share {r['tracked_share']:.2f})"
            segs.append(seg); continue
        seg.update(trusted=r['interior'], tracked_share=r['tracked_share'], noise_px=r['noise_px'], sm_lost=r['smoothed']['lost'],
                   sm_top=r['smoothed']['top_edges'], raw_lost=r['raw']['lost'], raw_top=r['raw']['top_edges'], region_lost=r['region']['lost'],
                   region_top=r['region']['top_edges'], cells_changed=r['smoothed']['cells_changed'],
                   img_null_raw=r['image_null']['raw_share_mean'], img_null_raw_sd=r['image_null']['raw_share_sd'],
                   img_null_sm=r['image_null']['smoothed_share_mean'], img_null_sm_sd=r['image_null']['smoothed_share_sd'],
                   boot_null_sm=r['null_smoothed_mean'], boot_null_sm_sd=r['null_smoothed_sd'], A_median=r['A_median'], A_p90=r['A_p90'],
                   model_expected_lost=r['model_expected_lost'],
                   swap_xyz=swaps_xyz(r, sm[0], sm[-1], lambda p_: to3d_plane(p_, a), lambda p_: to3d_plane(p_, a + L - 1)),
                   cells_A=global_angles(np.array([to3d_plane(p_, a) - c for p_ in sm[0][inter]]), frame).tolist())
        segs.append(seg)
        lg(f"retina planes {a}-{a + L - 1}: lost {seg['sm_lost']}/{seg['sm_top']}, image null {seg['img_null_sm']:.3f}, trusted {seg['interior'] if 'interior' in seg else seg['trusted']}")
    rec['retina_segments'] = segs
    ok = [g for g in segs if 'skip' not in g]
    rec['retina'] = dict(segments_used=len(ok), sm_lost=sum(g['sm_lost'] for g in ok), sm_top=sum(g['sm_top'] for g in ok),
                         null_expect=sum(g['img_null_sm'] * g['sm_top'] for g in ok),
                         null_sd=float(np.sqrt(sum((g['img_null_sm_sd'] * g['sm_top']) ** 2 for g in ok))))
    lg(f'done {time.time() - T0:.0f} s')
    return rec


def synthetic(_):
    out = {}
    kinds = [('straight', 0, 0.0), ('shear', 0, 0.0)] + [(f'jitterL{s}', s, 0.05) for s in range(5)] + [(f'jitterH{s}', s, 0.12) for s in range(5)]
    if PILOT: kinds = kinds[:3]
    for kind, sd, jit in kinds:
        S = et.synth_stack(kind.rstrip('0123456789').rstrip('LH'), seed=3 + sd, jit=jit); d = np.arange(len(S)) * 1.0
        r = et.run(S, d, 32.0, None, 'synthetic ' + kind, log=lambda *a: None, img_seeds=max(3, SEEDS // 2))[0]
        out[kind] = dict(raw_lost=r['raw']['lost'], raw_top=r['raw']['top_edges'], sm_lost=r['smoothed']['lost'], sm_top=r['smoothed']['top_edges'],
                         noise_px=r['noise_px'], img_null_raw=r['image_null']['raw_share_mean'], img_null_raw_sd=r['image_null']['raw_share_sd'],
                         img_null_sm=r['image_null']['smoothed_share_mean'], img_null_sm_sd=r['image_null']['smoothed_share_sd'],
                         boot_null_raw=r['null_raw_mean'], boot_null_raw_sd=r['null_raw_sd'])
        log(f'synthetic {kind}: raw {r["raw"]["lost"]}/{r["raw"]["top_edges"]}, image null share {r["image_null"]["raw_share_mean"]:.3f}')
    return out


if __name__ == '__main__':
    fr = np.load(E + 'frame_iso.npy'); frame = (fr[:3], fr[3:6], fr[6:])
    grid = [(round(a, 2), round(b, 2)) for a in np.arange(-0.5, 0.51, 0.2) for b in np.arange(-0.5, 0.51, 0.2)]
    if PILOT: grid = [(0.09, 0.27)]
    jobs = [(a, b, i) for i, (a, b) in enumerate(grid)]
    log(f'PROGRESS 0.00 {len(jobs)} patches, {WORKERS} workers, image-null seeds {SEEDS}')
    Pum, cum = cornea_points(); log(f'cornea points {len(Pum)}')
    curv = {}
    for a, b, i in jobs:
        _, _, uc, _, _ = es.patch_axes(a, b); curv[i] = curvature(Pum, cum, uc)
    with Pool(WORKERS) as pool:
        syn_async = pool.map_async(synthetic, [0])
        recs = []
        for k, rec in enumerate(pool.imap_unordered(patch, jobs)):
            rec['cornea'] = curv[rec['patch']]; recs.append(rec)
            log(f'PROGRESS {0.95 * (k + 1) / len(jobs):.2f} patch {rec["patch"]} ({rec["A"]}, {rec["B"]}) '
                f'{rec.get("skip", "")} cone {rec.get("cone", {}).get("sm_lost", "-")}/{rec.get("cone", {}).get("sm_top", "-")} '
                f'retina {rec.get("retina", {}).get("sm_lost", "-")}/{rec.get("retina", {}).get("sm_top", "-")} {rec.get("retina_skip", "")}')
        syn = syn_async.get()[0]
    recs.sort(key=lambda r: r['patch'])
    json.dump(dict(synthetic=syn, patches=recs, seconds=time.time() - T0), open(f'{OUT}/summary.json', 'w'), indent=1, default=float)
    # control verdicts
    ok = syn['straight']['raw_lost'] == 0 and 0.25 <= syn['shear']['raw_lost'] / max(1, syn['shear']['raw_top']) <= 0.42
    for tag in ['jitterL', 'jitterH']:
        ks = [k for k in syn if k.startswith(tag)]
        if not ks: continue
        obs = sum(syn[k]['raw_lost'] for k in ks); exp = sum(syn[k]['img_null_raw'] * syn[k]['raw_top'] for k in ks)
        sd = np.sqrt(sum((syn[k]['img_null_raw_sd'] * syn[k]['raw_top']) ** 2 for k in ks)) + 1e-9
        log(f'control {tag}: observed {obs} lost, image null {exp:.1f} +- {sd:.1f} (z = {(obs - exp) / sd:.1f})')
        syn[tag + '_pooled'] = dict(observed=obs, null=exp, null_sd=sd)
    json.dump(dict(synthetic=syn, patches=recs, seconds=time.time() - T0), open(f'{OUT}/summary.json', 'w'), indent=1, default=float)
    log(f'controls straight/shear {"ok" if ok else "FAIL"}; {time.time() - T0:.0f} s')
    if ok: print('FINAL ok')
    else: print('FINAL FAIL controls')
