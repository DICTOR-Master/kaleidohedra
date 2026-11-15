#!/usr/bin/env python3
"""Compound-eye scutoids pilot (DICTO 16 Nov 2026). Neighbour graph of ommatidial columns at the crystalline-cone layer versus at
depth d, columns extended along their axes. Input: ODA-3D ommatidial tables (Currea et al. 2023, CC BY 4.0, figshare
10.6084/m9.figshare.21521142; ODA code MIT licence, github.com/jpcurrea/ODA, column meanings from its analysis_tools.py:
x_,y_,z_ = cone centre, dx_,dy_,dz_ = axis smoothed over neighbours, dx,dy,dz = raw cone axis, same rotated frame).
Swap counting follows the lens study (studies/2026-11-15-scutoid-lenses, Delaunay neighbour sets at two surfaces), done here
in local tangent patches.
Usage: python eyeswap.py DATADIR OUTJSON"""
import sys, csv, json, math, time
import numpy as np
from scipy.spatial import cKDTree, Delaunay
from multiprocessing import Pool

DATADIR, OUT = sys.argv[1], sys.argv[2]
SPECIES = ['drosophila_mauritiana', 'apis_mellifera', 'deilephila_elpenor', 'manduca_sexta']
DEPTHS = [0, 10, 25, 50, 75, 100, 150, 200, 250, 300, 400]
K = 25
SQ3 = math.sqrt(3)
ABINS = [1.0, 1.2, 1.4, 1.6, SQ3, 2.0, 2.5, 3.0, 1e9]
T0 = time.time()
def prog(f, what): print(f'PROGRESS {f:.2f} {what} ({time.time() - T0:.0f} s)', flush=True)

def load(sp):
    rows = list(csv.DictReader(open(f'{DATADIR}/{sp}.csv')))
    smoothed_given = 'dx_' in rows[0]
    cols = ['x_', 'y_', 'z_'] + (['dx_', 'dy_', 'dz_'] if smoothed_given else ['dx', 'dy', 'dz']) + ['dx', 'dy', 'dz', 'lens_diameter', 'theta', 'phi']
    A = []
    for r in rows:
        try: A.append([float(r[c]) for c in cols])
        except (ValueError, KeyError): pass
    A = np.array(A); A = A[np.all(np.isfinite(A), axis=1)]
    P, S, Rw = A[:, 0:3], A[:, 3:6], A[:, 6:9]
    if not smoothed_given:   # manduca table has no smoothed axes: first-order neighbour average of the raw axes (ODA default order 1)
        _, idx = cKDTree(P).query(P, k=7); Ru = unit(Rw); S = np.zeros_like(Ru)
        for i in range(len(P)):
            V = Ru[idx[i]]; V = np.where(((V @ Ru[i]) < 0)[:, None], -V, V); S[i] = V.mean(0)
    return P, S, Rw, A[:, 9], A[:, 10], A[:, 11], len(rows), smoothed_given

def unit(v): return v / np.linalg.norm(v, axis=1)[:, None]

def fit_sphere(P):
    M = np.c_[2 * P, np.ones(len(P))]; b = (P ** 2).sum(1)
    s = np.linalg.lstsq(M, b, rcond=None)[0]; c = s[:3]; R = math.sqrt(s[3] + c @ c); return c, R

def frames(N):
    t = np.where(np.abs(N[:, 0:1]) < 0.9, np.array([[1.0, 0, 0]]), np.array([[0, 1.0, 0]]))
    e1 = unit(np.cross(N, t)); e2 = np.cross(N, e1); return e1, e2

def graph(P, N):
    """Local Delaunay neighbour sets in each point's tangent plane (normal N). Returns edge set (mutual) and boundary flags."""
    tree = cKDTree(P); _, idx = tree.query(P, k=min(K, len(P)))
    e1, e2 = frames(N); nb = []; bd = np.zeros(len(P), bool)
    for i in range(len(P)):
        Q = P[idx[i]] - P[i]; XY = np.c_[Q @ e1[i], Q @ e2[i]]
        try: T = Delaunay(XY)
        except Exception: nb.append(set()); bd[i] = True; continue
        ip, ix = T.vertex_neighbor_vertices; v0 = int(np.where(idx[i] == i)[0][0]) if i in idx[i] else 0
        nb.append(set(int(idx[i][j]) for j in ix[ip[v0]:ip[v0 + 1]]))
        if v0 in set(T.convex_hull.ravel()): bd[i] = True
    E = set()
    for i in range(len(P)):
        for j in nb[i]:
            if i < j and i in nb[j]: E.add((i, j))
    return E, bd, nb

def local_map(P0, Pd, N0, Nd, nb0):
    """Per point: least-squares 2x2 map from neighbour offsets at depth 0 to depth d (tangent planes); returns A, folded, s2."""
    a0, b0 = frames(N0); ad, bd_ = frames(Nd); A = np.ones(len(P0)); fold = np.zeros(len(P0), bool); S2 = np.ones(len(P0))
    for i in range(len(P0)):
        js = list(nb0[i])
        if len(js) < 3: fold[i] = True; continue
        X = np.c_[(P0[js] - P0[i]) @ a0[i], (P0[js] - P0[i]) @ b0[i]]
        Y = np.c_[(Pd[js] - Pd[i]) @ ad[i], (Pd[js] - Pd[i]) @ bd_[i]]
        M = np.linalg.lstsq(X, Y, rcond=None)[0]; s = np.linalg.svd(M, compute_uv=False)
        if np.linalg.det(M) <= 0 or s[1] < 0.05: fold[i] = True; A[i] = np.inf; continue
        A[i] = s[0] / s[1]; S2[i] = s[1]
    return A, fold, S2

def expand(bd, nb, rings):
    out = bd.copy()
    for _ in range(rings):
        new = out.copy()
        for i in np.where(out)[0]:
            for j in nb[i]: new[j] = True
        out = new
    return out

def run_variant(args):
    sp, var, seed = args
    P0, Ns, Nr, lens, th, ph, nrows, sgiven = load(sp)
    c, R = fit_sphere(P0)
    inward = unit(c - P0)
    Ns = unit(Ns); Nr = unit(Nr)
    Ns = np.where(((Ns * inward).sum(1) < 0)[:, None], -Ns, Ns); Nr = np.where(((Nr * inward).sum(1) < 0)[:, None], -Nr, Nr)
    tilt = np.degrees(np.arccos(np.clip((Ns * Nr).sum(1), -1, 1)))
    if var == 'smooth': D = Ns
    elif var == 'raw': D = Nr
    elif var == 'noise':
        rng = np.random.default_rng(seed); e1, e2 = frames(Ns); sd = math.radians(float(np.sqrt(np.mean(tilt ** 2)) / math.sqrt(2)))
        D = unit(Ns + np.tan(rng.normal(0, sd, len(Ns)))[:, None] * e1 + np.tan(rng.normal(0, sd, len(Ns)))[:, None] * e2)
    elif var == 'similarity': D = None
    E0, bd0, nb0 = graph(P0, Ns)
    tree = cKDTree(P0); dnn = tree.query(P0, k=7)[0][:, 1:]
    spacing = float(np.median(dnn[:, :6].mean(1)))
    interior = ~expand(bd0, nb0, 2)
    E0i = {e for e in E0 if interior[e[0]] and interior[e[1]]}
    out = {'species': sp, 'variant': var, 'smoothed_axes_from_table': sgiven, 'n_rows': nrows, 'n_used': int(len(P0)), 'sphere_R': round(R, 1),
           'median_spacing': round(spacing, 2), 'median_lens_diameter': round(float(np.median(lens)), 2),
           'spacing_over_lens': round(spacing / float(np.median(lens)), 3),
           'axis_tilt_raw_vs_smooth_deg_median': round(float(np.median(tilt)), 2),
           'axis_tilt_rms_deg': round(float(np.sqrt(np.mean(tilt ** 2))), 2),
           'interior_points': int(interior.sum()), 'interior_edges': len(E0i), 'depths': []}
    # convergence tensor from a 10 um step of the smoothed-axis model: principal Δφ/D values (1/um)
    if var == 'smooth':
        Pd = P0 + 10 * Ns; a0, b0 = frames(Ns); kmax = np.full(len(P0), np.nan); kmin = np.full(len(P0), np.nan)
        for i in np.where(interior)[0]:
            js = list(nb0[i])
            if len(js) < 3: continue
            X = np.c_[(P0[js] - P0[i]) @ a0[i], (P0[js] - P0[i]) @ b0[i]]; Y = np.c_[(Pd[js] - Pd[i]) @ a0[i], (Pd[js] - Pd[i]) @ b0[i]]
            M = np.linalg.lstsq(X, Y, rcond=None)[0]; Kt = (np.eye(2) - 0.5 * (M + M.T)) / 10; ev = np.linalg.eigvalsh(Kt)
            kmin[i], kmax[i] = ev[0], ev[1]
        ok = np.isfinite(kmax)
        dstar = np.where((SQ3 * kmax - kmin) > 0, (SQ3 - 1) / np.maximum(SQ3 * kmax - kmin, 1e-12), np.inf)
        q = lambda v: [round(float(x), 5) for x in np.nanpercentile(v[ok], [10, 50, 90])]
        out['convergence'] = {'kmax_p10_50_90_per_um': q(kmax), 'kmin_p10_50_90_per_um': q(kmin),
                              'dphi_max_deg_p50': round(math.degrees(float(np.nanmedian(kmax[ok])) * spacing), 2),
                              'dphi_min_deg_p50': round(math.degrees(float(np.nanmedian(kmin[ok])) * spacing), 2),
                              'dstar_um_p10_50_90': [round(float(x), 1) for x in np.percentile(dstar[ok], [10, 50, 90])]}
        # regions (terciles of theta and phi) for the map
        out['_dstar'] = dstar; out['_th'] = th; out['_ph'] = ph
    for d in DEPTHS:
        if var == 'similarity':
            s = 1 - d / R; Pd = c + s * (P0 - c)
        else:
            Pd = P0 + d * D
        Ed, bdd, _ = graph(Pd, Ns)
        A, fold, S2 = local_map(P0, Pd, Ns, Ns, nb0)
        good = {e for e in E0i if not (fold[e[0]] or fold[e[1]] or bdd[e[0]] or bdd[e[1]])}
        lost = {e for e in good if e not in Ed}
        row = {'d_um': d, 'edges_counted': len(good), 'lost': len(lost), 'lost_fraction': round(len(lost) / max(len(good), 1), 4),
               'folded_points': int(fold[interior].sum()), 'A_p50': round(float(np.median(A[interior & ~fold])), 3) if (interior & ~fold).any() else None,
               'A_p90': round(float(np.percentile(A[interior & ~fold], 90)), 3) if (interior & ~fold).any() else None}
        bins = []
        Ae = {e: max(A[e[0]], A[e[1]]) for e in good}
        for lo, hi in zip(ABINS[:-1], ABINS[1:]):
            es = [e for e in good if lo <= Ae[e] < hi]; nl = sum(e in lost for e in es)
            bins.append({'A_from': round(lo, 3), 'A_to': round(hi, 3) if hi < 1e8 else 'inf', 'edges': len(es), 'lost': nl,
                         'frac': round(nl / len(es), 4) if es else None})
        row['by_A'] = bins
        if var == 'smooth' and sp == 'apis_mellifera' and d in (150, 200, 300):
            t3 = np.nanpercentile(th, [33.3, 66.7]); p3 = np.nanpercentile(ph, [33.3, 66.7])
            ti = np.digitize(th, t3); pi = np.digitize(ph, p3); grid = {}
            for a in range(3):
                for b in range(3):
                    es = [e for e in good if ti[e[0]] == a and pi[e[0]] == b]; nl = sum(e in lost for e in es)
                    grid[f'theta{a}_phi{b}'] = [len(es), nl]
            row['region_theta_phi_terciles_edges_lost'] = grid
        out['depths'].append(row)
    for k in [k for k in out if k.startswith('_')]: out.pop(k)
    return out

def synthetic():
    """C2: hexagonal mosaic, rows along x. across: compress y (perpendicular to rows); along: compress x."""
    n = 40; P = np.array([[i + 0.5 * (j % 2), j * SQ3 / 2, 0.0] for i in range(n) for j in range(n)]); N = np.tile([0, 0, 1.0], (len(P), 1))
    E0, bd, nb = graph(P, N); interior = ~expand(bd, nb, 3); E0i = {e for e in E0 if interior[e[0]] and interior[e[1]]}
    res = {}
    for case in ['across', 'along']:
        first = None; seq = []
        for A in [1.0, 1.3, 1.6, 1.70, 1.72, 1.74, 1.76, 2.0, 3.0, 5.0, 10.0]:
            sx, sy = (1.0, 1 / A) if case == 'across' else (1 / A, 1.0)
            Pd = P * [sx, sy, 1]; Ed, _, _ = graph(Pd, N); lost = len([e for e in E0i if e not in Ed]); seq.append([A, lost])
            if lost and first is None: first = A
        res[case] = {'first_A_with_swaps': first, 'A_lost': seq, 'interior_edges': len(E0i)}
    return res

if __name__ == '__main__':
    prog(0.0, 'start')
    syn = synthetic(); prog(0.05, f'synthetic control {syn["across"]["first_A_with_swaps"]} / {syn["along"]["first_A_with_swaps"]}')
    tasks = [(sp, v, 7) for sp in SPECIES for v in ['smooth', 'raw', 'noise', 'similarity']]
    res = {'synthetic_C2': syn, 'runs': []}
    with Pool(min(16, len(tasks))) as pool:
        for k, r in enumerate(pool.imap_unordered(run_variant, tasks)):
            res['runs'].append(r); prog(0.05 + 0.9 * (k + 1) / len(tasks), f'{r["species"]} {r["variant"]}')
    checks = {}
    checks['C1_similarity_zero_swaps'] = all(all(d['lost'] == 0 for d in r['depths']) for r in res['runs'] if r['variant'] == 'similarity')
    a1 = syn['across']['first_A_with_swaps']; checks['C2_across_rows_first_swap_at_sqrt3'] = a1 is not None and 1.70 < a1 <= 1.76
    checks['C2_along_rows_no_swap_to_A10'] = syn['along']['first_A_with_swaps'] is None
    checks['zero_depth_zero_swaps'] = all(r['depths'][0]['lost'] == 0 for r in res['runs'])
    checks['all_16_runs_present'] = len(res['runs']) == 16
    res['checks'] = {k: bool(v) for k, v in checks.items()}
    json.dump(res, open(OUT, 'w'), indent=1)
    for k, v in res['checks'].items(): print('CHECK', k, v)
    for r in sorted(res['runs'], key=lambda r: (r['species'], r['variant'])):
        print(r['species'], r['variant'], 'spacing/lens', r['spacing_over_lens'], 'edges', r['interior_edges'],
              ' '.join(f"{d['d_um']}:{d['lost_fraction']}" for d in r['depths']), r.get('convergence', ''))
    prog(1.0, 'done')
    if all(checks.values()): print('FINAL ok')
    else: print('FINAL FAIL')
