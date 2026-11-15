"""Test (2) of the grid-or-physics follow-up: grid-free basins on tracer particles (the same particles at every snapshot).
Walls are faces of the tracers' periodic Voronoi tessellation, computed here from the Delaunay triangulation (Qhull, Barber, Dobkin &
Huhdanpaa 1996, through scipy) of the tracers plus their copies within a margin of the box faces: a face per Delaunay edge, its corners
the circumcentres of the tetrahedra around that edge, its area by the shoelace formula in the bisector plane; cell volume = sum over faces
of area * half-distance / 3. Checks per snapshot: every tetrahedron touching an original tracer has its circumsphere inside the copied
region; the cell volumes sum to L^3. (freud 3.6.1 / voro++ was tried first and dropped: its neighbour list was not symmetric and gave
14.60 instead of 15.535 neighbours on Poisson points.) Generic points: three cells along an edge, four at a corner.
Modes:
  zobov  - ZOBOV zones (Neyrinck 2008, arXiv:0712.3049): density = 1 / Voronoi volume; each tracer points to its lowest-density Voronoi
           neighbour if that is lower; a zone = all tracers draining to one minimum. No merging of zones into voids (as for the basins).
  smooth - the same watershed on the Gaussian-smoothed density contrast (r.m.s. width R) of ALL particles of the same run, read at the
           tracers by cubic-spline interpolation of the band-limited field, so the zones match the voxel basins in scale.
Zone volume = sum of Voronoi volumes; wall = all Voronoi faces between tracers of two zones, area in (Mpc/h)^2. Tracking and events:
basin_events.stage2x (minimum containment by tracer identity).
Usage: tracer_zones.py TRAC_DIR OUT_PREFIX mode m R workers a_min [quick]   (m: use the first n/m tracers, a random subset)"""
import sys, os, json, time
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import basin_events as BE


EDGES = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))


def voronoi_periodic(pos, L, margin):
    """Periodic Voronoi cells of pos (n x 3 in [0, L)): volumes V, directed face list (qi -> pj, both directions) with areas w."""
    from scipy.spatial import Delaunay
    n = len(pos); P, I = [pos], [np.arange(n)]
    for sh in np.array([(a, b, c) for a in (-1, 0, 1) for b in (-1, 0, 1) for c in (-1, 0, 1) if (a, b, c) != (0, 0, 0)]):
        q = pos + sh * L; mk = np.all((q > -margin) & (q < L + margin), axis=1); P.append(q[mk]); I.append(np.nonzero(mk)[0])
    P = np.concatenate(P); I = np.concatenate(I)
    S = Delaunay(P).simplices; S = S[(S < n).any(1)]
    X = P[S]; D = X[:, 1:] - X[:, :1]; rhs = 0.5 * (D ** 2).sum(2)
    c = X[:, 0] + np.linalg.solve(D, rhs[..., None])[..., 0]
    r = np.sqrt(((c - X[:, 0]) ** 2).sum(1))
    if not (np.all(c - r[:, None] > -margin) and np.all(c + r[:, None] < L + margin)):
        raise RuntimeError('margin too small: a circumsphere leaves the copied region')
    ga = np.concatenate([S[:, a] for a, b in EDGES]); gb = np.concatenate([S[:, b] for a, b in EDGES])
    cc = np.concatenate([c] * 6); del X, D, c
    lo, hi = np.minimum(ga, gb), np.maximum(ga, gb); key = lo.astype(np.int64) * len(P) + hi
    o = np.argsort(key, kind='stable'); key, lo, hi, cc = key[o], lo[o], hi[o], cc[o]
    st = np.r_[0, np.nonzero(key[1:] != key[:-1])[0] + 1]; cnt = np.diff(np.r_[st, len(key)]); g = np.repeat(np.arange(len(st)), cnt)
    eu, ev = lo[st], hi[st]
    nrm = P[ev] - P[eu]; dist = np.sqrt((nrm ** 2).sum(1)); nrm /= dist[:, None]
    e = np.zeros_like(nrm); e[np.arange(len(nrm)), np.argmin(np.abs(nrm), 1)] = 1.0
    u = np.cross(nrm, e); u /= np.sqrt((u ** 2).sum(1))[:, None]; v = np.cross(nrm, u)
    cbar = np.add.reduceat(cc, st, axis=0) / cnt[:, None]
    dc = cc - cbar[g]; x = (dc * u[g]).sum(1); y = (dc * v[g]).sum(1)
    o = np.lexsort((np.arctan2(y, x), g)); x, y = x[o], y[o]
    nx = np.roll(x, -1); ny = np.roll(y, -1); last = np.r_[st[1:] - 1, len(x) - 1]
    nx[last] = x[st]; ny[last] = y[st]
    area = 0.5 * np.abs(np.add.reduceat(x * ny - nx * y, st))
    a1 = eu < n; a2 = ev < n
    qi = np.r_[eu[a1], ev[a2]]; pj = np.r_[I[ev[a1]], I[eu[a2]]]; w = np.r_[area[a1], area[a2]]; hd = np.r_[dist[a1], dist[a2]]
    V = np.bincount(qi, weights=w * hd / 6.0, minlength=n)
    return V, qi.astype(np.int64), pj.astype(np.int64), w


def stage1(args):
    tpath, dpath, mode, m, R, L, cache = args
    if os.path.exists(cache):
        z = np.load(cache); return dict(nb=int(z['nb']), volerr=float(z['volerr']), asym=int(z['asym']))
    pos = np.load(tpath); n = len(pos) // m; pos = pos[:n].astype(np.float64)
    V, qi, pj, w = voronoi_periodic(pos, L, margin=7.0 * L / n ** (1 / 3))     # checked: every circumsphere must stay inside
    volerr = abs(V.sum() - L ** 3) / L ** 3
    if mode == 'zobov':
        f = 1.0 / (V * n / L ** 3) - 1.0                       # density contrast of the tracers
    else:
        from scipy import ndimage
        d = np.load(dpath).astype(np.float64); G = d.shape[0]
        k = 2 * np.pi * np.fft.fftfreq(G, L / G); kz = 2 * np.pi * np.fft.rfftfreq(G, L / G)
        k2 = k[:, None, None] ** 2 + k[None, :, None] ** 2 + kz[None, None, :] ** 2
        fs = np.fft.irfftn(np.fft.rfftn(d) * np.exp(-0.5 * k2 * R * R), s=d.shape)
        c = ndimage.spline_filter(fs, order=3, mode='grid-wrap')
        f = ndimage.map_coordinates(c, (pos / (L / G)).T, order=3, mode='grid-wrap', prefilter=False)
    # watershed on the Voronoi graph: point to the lowest neighbour if lower
    o = np.lexsort((f[pj], qi)); qs, ps = qi[o], pj[o]
    first = np.r_[True, qs[1:] != qs[:-1]]
    low = np.arange(n); bi, bj = qs[first], ps[first]
    low[bi] = np.where(f[bj] < f[bi], bj, bi)
    p = low
    while True:
        q = p[p]
        if np.array_equal(q, p): break
        p = q
    mins, lab = np.unique(p, return_inverse=True)
    lab = lab.astype(np.int32)
    # walls (each face appears once per direction; keep i < j)
    s = qi < pj; a, b, ar = lab[qi[s]], lab[pj[s]], w[s]; fm = 0.5 * (f[qi[s]] + f[pj[s]])
    asym = int(abs(np.count_nonzero(qi < pj) - np.count_nonzero(qi > pj)))   # 0 by construction (both directions kept)
    mk = a != b; a, b, ar, fm = a[mk].astype(np.int64), b[mk].astype(np.int64), ar[mk], fm[mk]
    nb = len(mins); key = np.minimum(a, b) * nb + np.maximum(a, b)
    u, inv = np.unique(key, return_inverse=True)
    area = np.bincount(inv, weights=ar); fw = np.bincount(inv, weights=ar * fm) / area
    vol = np.bincount(lab, weights=V, minlength=nb)
    np.savez_compressed(cache, lab=lab, mins=mins, pairs=np.stack([u // nb, u % nb], 1), area=area, fwall=fw, vol=vol, nb=nb, unit_area=1.0,
                        volerr=volerr, asym=asym, n=n)
    return dict(nb=nb, volerr=volerr, asym=asym)


def main():
    tdir, outp, mode, m, R, workers, a_min = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), float(sys.argv[5]), int(sys.argv[6]), \
        float(sys.argv[7])
    quick = len(sys.argv) > 8
    t0 = time.time()
    meta = json.load(open(f'{tdir}/meta.json')); L = meta['L_Mpc_h']
    snaps = [s for s in meta['snapshots'] if s['a'] >= a_min - 1e-9]
    if quick: snaps = snaps[:3]
    a_of = [s['a'] for s in snaps]
    cdir = f'{tdir}/zones-{mode}-m{m}' + (f'-R{R:g}' if mode == 'smooth' else ''); os.makedirs(cdir, exist_ok=True)
    jobs = [(f'{tdir}/tracers_{s["k"]:04d}.npy', f'{tdir}/delta_{s["k"]:04d}.npy', mode, m, R, L, f'{cdir}/z_{s["k"]:04d}.npz') for s in snaps]
    st1 = []
    with Pool(workers) as pool:
        for i, r in enumerate(pool.imap(stage1, jobs)):
            st1.append(r)
            print(f'PROGRESS {0.6 * (i + 1) / len(jobs):.3f} stage1 {i + 1}/{len(jobs)} zones {r["nb"]} volerr {r["volerr"]:.1e} t={time.time() - t0:.0f}s', flush=True)
    caches = [j[6] for j in jobs]
    curves = [BE.neighbour_curve(np.load(c), L) for c in caches]
    rules = [('faces', 0.0), ('eps', 0.01)]
    variants = [(k, r) for k in (1, 2, 4) for r in rules] if not quick else [(1, ('faces', 0.0))]
    out = dict(mode=mode, m=m, n_tracers=meta['n_tracers'] // m, R_Mpc_h=R if mode == 'smooth' else None, a_min=a_min, L_Mpc_h=L, nbody=meta,
               n_snapshots=len(snaps), max_volume_error=max(r['volerr'] for r in st1), max_nlist_asymmetry=max(r['asym'] for r in st1),
               eps_list=list(BE.EPS_LIST), neighbour_curve_first=curves[0], neighbour_curve_last=curves[-1],
               neighbour_curve_mean=list(np.mean(curves, 0)), zones_per_snapshot=[r['nb'] for r in st1], variants=[])
    with Pool(min(workers, len(variants))) as pool:
        res = [pool.apply_async(BE.stage2x, (caches, k, rule, a_of, L)) for k, rule in variants]
        for i, ((k, rule), h) in enumerate(zip(variants, res)):
            r = h.get(); out['variants'].append(r)
            print(f'PROGRESS {0.6 + 0.4 * (i + 1) / len(variants):.3f} stage2 k={k} rule={rule} alone {r["fraction_alone"]:.3f} clumped '
                  f'{r["fraction_clumped"]:.3f} per basin per step {r["per_basin_per_step"]:.3f} t={time.time() - t0:.0f}s', flush=True)
    json.dump(out, open(f'{outp}.json', 'w'), indent=1)
    ok = all(v['balance_failures'] == 0 for v in out['variants']) and out['max_volume_error'] < 1e-6 and out['max_nlist_asymmetry'] == 0
    print('volume error', out['max_volume_error'], 'nlist asymmetry', out['max_nlist_asymmetry'])
    print('neighbour curve mean', dict(zip(BE.EPS_LIST, np.round(out['neighbour_curve_mean'], 3))))
    print('WALL', time.time() - t0)
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
