"""Test (1) of the grid-or-physics follow-up: the same smoothed density field, sampled on a finer voxel grid.
The density contrast (256^3 grid) is smoothed with a Gaussian of r.m.s. width R; at R = 4 Mpc/h the factor at the 256^3 Nyquist frequency is
e^-79, so the smoothed field is band-limited and zero-padding its Fourier transform samples the same continuous field on a G_out^3 grid
exactly (control: the G_out grid at the old voxel centres reproduces the 256^3 field). Basins (void_basins.basins, 26-neighbour steepest
descent), walls (shared voxel faces, now with area in (Mpc/h)^2 and the mean smoothed field on the wall), tracking and events
(basin_events.stage2x) as before.
Usage: grid_refine.py DATA_DIR OUT_PREFIX R G_out workers a_min [quick]"""
import sys, os, json, time
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from void_basins import basins
import basin_events as BE


def smooth_up(delta, R, L, Go):
    G = delta.shape[0]
    k = 2 * np.pi * np.fft.fftfreq(G, L / G); kz = 2 * np.pi * np.fft.rfftfreq(G, L / G)
    k2 = k[:, None, None] ** 2 + k[None, :, None] ** 2 + kz[None, None, :] ** 2
    F = np.fft.rfftn(delta.astype(np.float64)) * np.exp(-0.5 * k2 * R * R)
    if Go == G: return np.fft.irfftn(F, s=delta.shape), 0.0
    h = G // 2
    P = np.zeros((Go, Go, Go // 2 + 1), np.complex128)
    for sx, dx in ((slice(0, h), slice(0, h)), (slice(h + 1, G), slice(Go - h + 1, Go))):     # drop the Nyquist planes (weight e^-79)
        for sy, dy in ((slice(0, h), slice(0, h)), (slice(h + 1, G), slice(Go - h + 1, Go))):
            P[dx, dy, :h] = F[sx, sy, :h]
    nyq = float(max(np.abs(F[h]).max(), np.abs(F[:, h]).max(), np.abs(F[:, :, h]).max()) / np.abs(F).max())
    del F
    return np.fft.irfftn(P, s=(Go,) * 3) * (Go / G) ** 3, nyq


def walls_f(lab, f):
    nb = int(lab.max()) + 1
    keys, fs = [], []
    for ax in range(3):
        l2 = np.roll(lab, -1, axis=ax); m = lab != l2
        a, b = lab[m].astype(np.int64), l2[m].astype(np.int64)
        keys.append(np.minimum(a, b) * nb + np.maximum(a, b)); fs.append(0.5 * (f[m] + np.roll(f, -1, axis=ax)[m]))
        del l2, m
    keys = np.concatenate(keys); fs = np.concatenate(fs)
    u, inv, c = np.unique(keys, return_inverse=True, return_counts=True)
    fw = np.bincount(inv, weights=fs) / c
    return np.stack([u // nb, u % nb], 1), c, fw


def stage1(args):
    path, R, L, Go, cache, ref = args
    if os.path.exists(cache):
        z = np.load(cache); return dict(cache=cache, nb=int(z['nb']), ctrl=float(z['ctrl']), nyq=float(z['nyq']))
    d = np.load(path)
    f, nyq = smooth_up(d, R, L, Go)
    ctrl = 0.0
    if Go != d.shape[0]:
        f0, _ = smooth_up(d, R, L, d.shape[0]); s = Go // d.shape[0]
        ctrl = float(np.abs(f[::s, ::s, ::s] - f0).max() / f0.std()); del f0
    lab, mins = basins(f)
    pairs, area, fw = walls_f(lab, f)
    vol = np.bincount(lab.ravel()).astype(np.float64) * (L / Go) ** 3
    assert (vol > 0).all()
    np.savez_compressed(cache, lab=lab, mins=mins, pairs=pairs, area=area, fwall=fw, vol=vol, nb=len(mins), unit_area=(L / Go) ** 2,
                        fmin=f.ravel()[mins], ctrl=ctrl, nyq=nyq)
    return dict(cache=cache, nb=len(mins), ctrl=ctrl, nyq=nyq)


def main():
    data, outp, R, Go, workers, a_min = sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), float(sys.argv[6])
    quick = len(sys.argv) > 7
    t0 = time.time()
    meta = json.load(open(f'{data}/meta.json')); L = meta['L_Mpc_h']
    snaps = [s for s in meta['snapshots'] if s['a'] >= a_min - 1e-9]
    if quick: snaps = snaps[:3]
    a_of = [s['a'] for s in snaps]
    cdir = f'{data}/basins-R{R:g}-G{Go}'; os.makedirs(cdir, exist_ok=True)
    jobs = [(f'{data}/delta_{s["k"]:04d}.npy', R, L, Go, f'{cdir}/b_{s["k"]:04d}.npz', None) for s in snaps]
    st1 = []
    with Pool(workers) as pool:
        for i, r in enumerate(pool.imap(stage1, jobs)):
            st1.append(r)
            print(f'PROGRESS {0.6 * (i + 1) / len(jobs):.3f} stage1 {i + 1}/{len(jobs)} basins {r["nb"]} ctrl {r["ctrl"]:.2e} t={time.time() - t0:.0f}s', flush=True)
    caches = [j[4] for j in jobs]
    curves = [BE.neighbour_curve(np.load(c), L) for c in caches]
    rules = [('faces', 1), ('phys', 10.0), ('eps', 0.01)]
    variants = [(k, r) for k in (1, 2, 4) for r in rules] if not quick else [(1, ('faces', 1))]
    out = dict(R_Mpc_h=R, grid=Go, a_min=a_min, L_Mpc_h=L, nbody=meta, n_snapshots=len(snaps),
               control_max_dev_at_old_voxels=max(r['ctrl'] for r in st1), nyquist_weight=max(r['nyq'] for r in st1),
               eps_list=list(BE.EPS_LIST), neighbour_curve_first=curves[0], neighbour_curve_last=curves[-1],
               neighbour_curve_mean=list(np.mean(curves, 0)), basins_per_snapshot=[r['nb'] for r in st1], variants=[])
    with Pool(min(workers, len(variants))) as pool:
        res = [pool.apply_async(BE.stage2x, (caches, k, rule, a_of, L)) for k, rule in variants]
        for i, ((k, rule), h) in enumerate(zip(variants, res)):
            r = h.get(); out['variants'].append(r)
            print(f'PROGRESS {0.6 + 0.4 * (i + 1) / len(variants):.3f} stage2 k={k} rule={rule} alone {r["fraction_alone"]:.3f} clumped '
                  f'{r["fraction_clumped"]:.3f} per basin per step {r["per_basin_per_step"]:.3f} t={time.time() - t0:.0f}s', flush=True)
    json.dump(out, open(f'{outp}.json', 'w'), indent=1)
    ok = all(v['balance_failures'] == 0 for v in out['variants']) and out['control_max_dev_at_old_voxels'] < 1e-6
    print('control (max deviation at old voxels / field std)', out['control_max_dev_at_old_voxels'], 'nyquist weight', out['nyquist_weight'])
    print('neighbour curve mean', dict(zip(BE.EPS_LIST, np.round(out['neighbour_curve_mean'], 3))))
    print('WALL', time.time() - t0)
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
