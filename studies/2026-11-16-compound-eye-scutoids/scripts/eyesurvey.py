#!/usr/bin/env python3
"""Survey one butterfly eye volume (Paukner et al. 2024, BossDB paukner2024; scale 2400_2400_600, kept on the compute machine,
never in git) for the scutoid test. Study 2026-11-16-compound-eye-scutoids, ledger [271] next step.

All in an isotropic 2.4 um grid (z averaged in fours).
  cornea      a local sphere through the SEED point (one point on the lens row per eye, read off the preview slices by eye,
              table below), fitted by RANSAC to lens-boundary voxels within 600 um; rays from its centre on a 0.01 rad grid find
              the first tissue (with 60 um of tissue behind it) within +-96 um of it; the cornea is the connected part of this
              height map (3 x 3 median) that holds the seed area (neighbouring rays differ by under 12 um), keeping only rays with facet-lens
              texture (band-pass energy 5-30 um below the surface above a quarter of the seed area's median); RANSAC points are
              boundary voxels backed by tissue (90% of samples 7-60 um inward), so thin shells (emptied head capsule, tube) drop out. A sphere was tried first and failed: in oval
              eyes and in heads with an emptied capsule or a sample tube it locks onto the wrong shell (recorded in the README).
  quadric     free algebraic quadric on the sheet (trimmed at 3 MAD): semi-axes and axis ratios if an ellipsoid; 30 bootstrap
              resamples. A free quadric on a cap is poorly posed, so the local U below is the main curvature measure.
  local U     the gw05 recipe on the sheet: discs of radius 132 um (0.2 rad at gw05's 660 um) centred 144 um apart, tangent
              plane by PCA, quadratic height fit, principal curvatures k1 >= k2 > 0, U = (k1 - k2)/(k1 + k2); a disc counts only
              if 80% of its 12 x 12 cells hold surface points (no eye rim, no crop).
  profile     along the smoothed inward normals of the counted discs, every 2.4 um to 600 um: tissue share, intensity, texture
              (rms of I - G(I, 4 vox)), structure tensor (gradient sigma 1, window 3 vox): share of voxels whose column axis lies
              within 30 deg of the surface normal. Clear zone and column runs are called from these and checked by eye.
  slice       one cross-section through the sheet centre, spanned by the mean normal and the sheet's long axis (for the figure).
Usage: eyesurvey.py NAME OUTDIR   (reads $EYE_DATA/NAME-s2400.npy)"""
import sys, os, json, time, numpy as np
from scipy import ndimage as ndi
from scipy.spatial import cKDTree

E = os.environ.get('EYE_DATA', os.path.expanduser('~/eye-data')) + '/'
NAME, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True)
VX = 2.4; T0 = time.time()
# one point on the lens row of each eye, iso grid (z/4, y, x), read off the middle preview slices
SEEDS = {'gw05': (125, 300, 355), 'gw06': (129, 330, 75), 'gw13': (50, 98, 428), 'gw14': (137, 420, 482),
         'gw16': (144, 300, 88), 'gw17': (150, 125, 250), 'gw07': (270, 450, 150)}
# tissue threshold overrides, read off intensity profiles across the seed: gw13 and gw14 sit in a grey medium (21 and 27-31 outside
# the cornea), gw17 is very dark (eye interior
# about 3 grey levels against 0.3 outside), so the default max(12, background + 8) misses its tissue
THR = {'gw13': 26.0, 'gw14': 40.0, 'gw17': 4.0}
def log(m): print(f'[{time.time() - T0:6.1f}s] {NAME} {m}', flush=True)

V = np.load(E + f'{NAME}-s2400.npy', mmap_mode='r'); Z = V.shape[0] // 4 * 4
I = np.asarray(V[:Z], dtype=np.float32).reshape(Z // 4, 4, V.shape[1], V.shape[2]).mean(1)
log(f'iso {I.shape}'); print('PROGRESS 0.1 iso', flush=True)
rng = np.random.default_rng(1)

# ---- cornea sheet
S = ndi.gaussian_filter(I, 2.0); bg = float(np.median(S[S < np.percentile(S, 30)]))
thr = THR.get(NAME, max(12.0, bg + 8.0))
obj = ndi.binary_closing(S > thr, iterations=2)      # no largest-component pick and no hole filling: in gw13 and gw17 the sample
bd = obj & ~ndi.binary_erosion(obj)                 # tube is the largest object, and filling it hides the eye; the seed gives locality
# for the rays the tissue mask is hole-filled per z slice (dark retina and pigment pockets count as tissue), except in the two
# eyes inside a sample tube, where filling would fill the tube
objf = obj.copy() if NAME in ('gw13', 'gw17') else np.stack([ndi.binary_fill_holes(o) for o in obj])
bd = objf & ~ndi.binary_erosion(objf)
L7_ = ndi.gaussian_filter(I, 0.7); lens_thr = float(min(150.0, np.percentile(L7_[obj], 99)))   # lens material: the brightest 1% (at most 150)
lens = ndi.maximum_filter((L7_ > lens_thr).astype(np.uint8), size=13) > 0
P = np.argwhere(bd & lens).astype(float); sh = np.array(I.shape)
P = P[np.all((P > 3) & (P < sh - 4), axis=1)]
seed = np.array(SEEDS[NAME], float)
def sphere_ls(X):
    A = np.c_[2 * X, np.ones(len(X))]; b = (X ** 2).sum(1); s_ = np.linalg.lstsq(A, b, rcond=None)[0]
    c_ = s_[:3]; return c_, float(np.sqrt(s_[3] + c_ @ c_))
# 1. local sphere: RANSAC on lens-boundary points within 600 um of the seed, the sphere passing within 12 um of the seed point
Q = P[np.linalg.norm(P - seed, axis=1) < 250]
log(f'lens-boundary points near the seed {len(Q)}')
Gq = np.stack([ndi.map_coordinates(ndi.gaussian_filter(S, 1.0, order=o), Q.T, order=1) for o in ((1, 0, 0), (0, 1, 0), (0, 0, 1))], 1)
Gq /= np.linalg.norm(Gq, axis=1, keepdims=True) + 1e-9; Xq = Q[:, :, None] + Gq[:, :, None] * np.arange(3, 26)[None, None, :]
Q = Q[(ndi.map_coordinates(S, Xq.transpose(1, 0, 2).reshape(3, -1), order=1, cval=0).reshape(len(Q), -1) > thr).mean(1) >= 0.9]   # thick-backed only
s0 = Q[np.argmin(np.linalg.norm(Q - seed, axis=1))]
Q = Q[rng.choice(len(Q), min(len(Q), 20000), replace=False)]; best = (0, None)
for it in range(8000):
    try: c_, R_ = sphere_ls(Q[rng.choice(len(Q), 4, replace=False)])
    except Exception: continue
    if not (60 < R_ < 800) or abs(np.linalg.norm(s0 - c_) - R_) > 5: continue
    k_ = int((np.abs(np.linalg.norm(Q - c_, axis=1) - R_) < 4).sum())
    if k_ > best[0]: best = (k_, (c_, R_))
c, R = best[1]
v0 = (s0 - c) / np.linalg.norm(s0 - c)
log(f'background {bg:.1f}, threshold {thr:.1f}, lens {lens_thr:.0f}; local sphere through the seed: R {R * VX:.0f} um ({best[0]} of {len(Q)} points within 10 um)')
# 2. rays from the sphere centre on a 0.01 rad grid about the seed direction: first tissue sample with 60 um of tissue behind it,
#    searched within +-96 um of the sphere; 3. flood fill over the grid from the seed ray, neighbours differing by under 7 um
BIN = 0.01
a_ = np.array([1.0, 0, 0]) if abs(v0[0]) < 0.9 else np.array([0, 1.0, 0])
e1 = np.cross(v0, a_); e1 /= np.linalg.norm(e1); e2 = np.cross(v0, e1)
g_ = np.arange(-1.5, 1.5001, BIN); NG = len(g_); GA, GB = [w.ravel() for w in np.meshgrid(g_, g_, indexing='ij')]
tt = np.hypot(GA, GB) + 1e-12
Dg = np.cos(tt)[:, None] * v0 + (np.sin(tt) / tt)[:, None] * (GA[:, None] * e1 + GB[:, None] * e2)
rs = np.arange(R + 40, R - 40, -0.25); hit = np.full(len(Dg), np.nan); valid = tt < 1.5
for k0 in range(0, len(Dg), 3000):
    sl_ = slice(k0, k0 + 3000); d_ = Dg[sl_]
    pts = c[None, :, None] + d_[:, :, None] * rs[None, None, :]
    inside = np.all((pts >= 0) & (pts <= (sh - 1)[None, :, None]), axis=1)
    tis = ndi.map_coordinates(objf.astype(np.float32), pts.transpose(1, 0, 2).reshape(3, -1), order=1, cval=0).reshape(len(d_), len(rs)) > 0.5
    first = np.where(tis.any(1), tis.argmax(1), -1)
    for q_ in np.flatnonzero((first > 0) & valid[sl_]):
        f0 = first[q_]
        if not inside[q_, f0] or f0 + 100 > len(rs) or tis[q_, f0:f0 + 100].mean() < 0.9: continue
        hit[k0 + q_] = rs[f0]
# facet-lens texture under each hit (band-pass energy 5-30 um below the surface); keep rays above a quarter of the seed area's median
DoG = ndi.gaussian_filter(I, 1.0) - ndi.gaussian_filter(I, 4.0); En = ndi.gaussian_filter(DoG ** 2, 3.0); del DoG
fh = np.flatnonzero(np.isfinite(hit)); enr = np.zeros(len(Dg))
Xe = (c[None, :, None] + Dg[fh][:, :, None] * (hit[fh][:, None, None] - np.arange(2, 13)[None, None, :]))
enr[fh] = ndi.map_coordinates(En, Xe.transpose(1, 0, 2).reshape(3, -1), order=1).reshape(len(fh), -1).mean(1)
near = np.isfinite(hit) & (tt < 0.08); eref = float(np.median(enr[near])) if near.any() else float(np.median(enr[fh]))
hit[np.isfinite(hit) & (enr < 0.25 * eref)] = np.nan
H = hit.reshape(NG, NG); ic = NG // 2
Hm = ndi.generic_filter(np.nan_to_num(H, nan=-1e9), lambda w: np.median(w[w > -1e8]) if (w > -1e8).sum() >= 5 else np.nan, size=3)
H = np.where(np.isfinite(H), Hm, np.nan)          # 3 x 3 median over the hits (facet bumps), steps then compared at 12 um
def flood(i0, j0):
    f = np.zeros_like(H, bool); f[i0, j0] = True; stack = [(i0, j0)]
    while stack:
        i, j = stack.pop()
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            a, b = i + di, j + dj
            if 0 <= a < NG and 0 <= b < NG and not f[a, b] and np.isfinite(H[a, b]) and abs(H[a, b] - H[i, j]) < 5:
                f[a, b] = True; stack.append((a, b))
    return f
# start from every hit within 40 cells (0.4 rad) of the seed ray; keep the largest connected sheet
filled = np.zeros_like(H, bool); tried = np.zeros_like(H, bool)
for i0 in range(ic - 40, ic + 41):
    for j0 in range(ic - 40, ic + 41):
        if np.isfinite(H[i0, j0]) and not tried[i0, j0]:
            f = flood(i0, j0); tried |= f
            if f.sum() > filled.sum(): filled = f
fl = filled.ravel()
Pc = c + Dg[fl] * H.ravel()[fl][:, None]; Nc = -Dg[fl]
log(f'rays {valid.sum()}, hits {np.isfinite(hit).sum()}, connected sheet from the seed {fl.sum()} points')
tree = cKDTree(Pc)
Ns = np.array([Nc[j].mean(0) for j in tree.query_ball_point(Pc, 20)]); Ns /= np.linalg.norm(Ns, axis=1, keepdims=True)

cs, Rs = sphere_ls(Pc); res = np.linalg.norm(Pc - cs, axis=1) - Rs
ext_pts = np.ptp(Pc, axis=0) * VX
log(f'reference sphere R {Rs * VX:.0f} um, rms {res.std() * VX:.1f} um; sheet extent (z, y, x) {np.round(ext_pts)} um')
print('PROGRESS 0.3 sheet', flush=True)

# ---- free quadric on the sheet
cen = Pc.mean(0); sc = np.abs(Pc - cen).max()
x, y, z = ((Pc - cen) / sc).T
M = np.c_[x * x, y * y, z * z, 2 * x * y, 2 * x * z, 2 * y * z, 2 * x, 2 * y, 2 * z, np.ones_like(x)]
def quadric_axes(q):
    A3 = np.array([[q[0], q[3], q[4]], [q[3], q[1], q[5]], [q[4], q[5], q[2]]])
    ctr = -np.linalg.solve(A3, q[6:9]); lam = np.linalg.eigvalsh(A3 / (ctr @ A3 @ ctr - q[9]))
    if np.all(lam > 0): return np.sort(1 / np.sqrt(lam))[::-1] * sc * VX, ctr
    return None, ''.join('+' if l > 0 else '-' for l in lam)
keepq = np.ones(len(M), bool)
for _ in range(4):
    q = np.linalg.svd(M[keepq], full_matrices=False)[2][-1]; rq = M @ q
    mq = 1.4826 * np.median(np.abs(rq[keepq])); keepq = np.abs(rq) < 3 * mq
ax, info = quadric_axes(q)
quad = dict(kind='ellipsoid', semi_axes_um=ax.tolist(), ratio_max_min=float(ax[0] / ax[2]), ratio_mid_min=float(ax[1] / ax[2])) if ax is not None \
    else dict(kind=f'not an ellipsoid (signs {info})')
bt = []
for b_ in range(30):
    ii = np.flatnonzero(keepq); ii = ii[rng.integers(0, len(ii), len(ii))]
    try: a_, _ = quadric_axes(np.linalg.svd(M[ii], full_matrices=False)[2][-1]); bt.append(a_[0] / a_[2] if a_ is not None else np.nan)
    except Exception: bt.append(np.nan)
bt = np.array(bt, float)
quad['bootstrap_ratio_max_min'] = dict(p10=float(np.nanpercentile(bt, 10)) if np.isfinite(bt).any() else None,
                                       p50=float(np.nanpercentile(bt, 50)) if np.isfinite(bt).any() else None,
                                       p90=float(np.nanpercentile(bt, 90)) if np.isfinite(bt).any() else None, non_ellipsoid=int(np.isnan(bt).sum()))
log(f'quadric {quad}')

# ---- local U on discs
RT = 132 / VX
def disc(p0, n0):
    idx = tree.query_ball_point(p0, RT)
    if len(idx) < 60: return None
    Q = Pc[idx] - p0; w, ev = np.linalg.eigh(np.cov(Q.T)); nrm = ev[:, 0] * np.sign(ev[:, 0] @ n0)
    a = np.array([1.0, 0, 0]) if abs(nrm[0]) < 0.9 else np.array([0, 1.0, 0])
    t1 = np.cross(nrm, a); t1 /= np.linalg.norm(t1); t2 = np.cross(nrm, t1)
    xx, yy, h = Q @ t1, Q @ t2, Q @ nrm
    cells = set(zip(np.floor((xx + RT) / (2 * RT / 12)).astype(int), np.floor((yy + RT) / (2 * RT / 12)).astype(int)))
    gx, gy = np.meshgrid(np.arange(12), np.arange(12)); cc = (gx + 0.5 - 6) ** 2 + (gy + 0.5 - 6) ** 2 <= 36
    cov = np.mean([(i, j) in cells for i, j in zip(gx[cc], gy[cc])])
    if cov < 0.8: return None
    MM = np.c_[np.ones_like(xx), xx, yy, xx * xx, xx * yy, yy * yy]; co = np.linalg.lstsq(MM, h, rcond=None)[0]
    H = np.array([[2 * co[3], co[4]], [co[4], 2 * co[5]]]) / VX; k = np.sort(np.linalg.eigvalsh(H))[::-1]
    if k[1] <= 0: return None
    return dict(r1=float(1 / k[0]), r2=float(1 / k[1]), U=float((k[0] - k[1]) / (k[0] + k[1])), n=len(idx), coverage=float(cov),
                rms_um=float((h - MM @ co).std() * VX), centre_iso=p0.tolist(), normal=nrm.tolist())
# disc centres: greedy farthest-point sampling at 144 um
order = rng.permutation(len(Pc)); taken = []; tk = None
for j in order:
    if tk is not None and tk.query_ball_point(Pc[j], 144 / VX): continue
    taken.append(j); tk = cKDTree(Pc[taken])
tiles = [t for t in (disc(Pc[j], Ns[j]) for j in taken) if t]
U = np.array([t['U'] for t in tiles]) if tiles else np.array([np.nan])
log(f'discs {len(taken)} placed, {len(tiles)} counted, U median {np.nanmedian(U):.3f}')
print('PROGRESS 0.5 curvature', flush=True)

# sample points for the profile: sheet points inside counted discs, with their smoothed inward normals
inside = np.zeros(len(Pc), bool)
for t in tiles: inside[tree.query_ball_point(np.array(t['centre_iso']), RT)] = True
cand = np.flatnonzero(inside) if inside.sum() > 200 else np.arange(len(Pc))
pick = rng.choice(cand, min(len(cand), 4000), replace=False); P0, N0 = Pc[pick], Ns[pick]
# ---- depth profile
depths = np.arange(0, 600 / VX, 1.0)
pts_all = P0[:, :, None] + N0[:, :, None] * depths[None, None, :]                 # (n, 3, nd)
lo = np.clip(np.floor(pts_all.min((0, 2))) - 12, 0, None).astype(int); hi = np.minimum(np.ceil(pts_all.max((0, 2))) + 12, sh).astype(int)
C = I[lo[0]:hi[0], lo[1]:hi[1], lo[2]:hi[2]]; Ob = obj[lo[0]:hi[0], lo[1]:hi[1], lo[2]:hi[2]].astype(np.float32)
HP = C - ndi.gaussian_filter(C, 4.0)
g = [ndi.gaussian_filter(C, 1.0, order=o) for o in ((1, 0, 0), (0, 1, 0), (0, 0, 1))]
J = {}
for i in range(3):
    for j in range(i, 3): J[i, j] = ndi.gaussian_filter(g[i] * g[j], 3.0)
del g
log(f'crop {C.shape}'); print('PROGRESS 0.8 tensor', flush=True)
prof = []
for di, d in enumerate(depths):
    p = (P0 + N0 * d) - lo
    ins = np.all((p >= 0) & (p <= np.array(C.shape) - 1), axis=1)
    if ins.sum() < 50: prof.append(dict(depth_um=float(d * VX), n=int(ins.sum()))); continue
    pp = p[ins].T
    tis = ndi.map_coordinates(Ob, pp, order=1); inten = ndi.map_coordinates(C, pp, order=1)
    hp = ndi.map_coordinates(HP, pp, order=1)
    T = np.zeros((pp.shape[1], 3, 3), np.float32)
    for (i, j), Jij in J.items():
        val = ndi.map_coordinates(Jij, pp, order=1); T[:, i, j] = val; T[:, j, i] = val
    w, vec = np.linalg.eigh(T)
    tub = (w[:, 1] - w[:, 0]) / (w[:, 1] + w[:, 0] + 1e-9)
    radial = N0[ins]; cosang = np.abs((vec[:, :, 0] * radial).sum(1))
    tm = tis > 0.5
    prof.append(dict(depth_um=float(d * VX), n=int(ins.sum()), tissue=float(tm.mean()), intensity=float(np.median(inten[tm])) if tm.any() else None,
                     texture=float(hp[tm].std()) if tm.sum() > 30 else None, tubularity=float(np.median(tub[tm])) if tm.sum() > 30 else None,
                     aligned30=float((cosang[tm] > np.cos(np.radians(30))).mean()) if tm.sum() > 30 else None))

# clear-zone call
dd = np.array([p_['depth_um'] for p_ in prof]); tx = np.array([p_.get('texture') or np.nan for p_ in prof])
ti = np.array([p_.get('tissue') or 0 for p_ in prof]); al = np.array([p_.get('aligned30') or np.nan for p_ in prof])
tsm = ndi.uniform_filter1d(np.nan_to_num(tx), 5)
ok = ti > 0.8
cone_ref = np.nanmax(np.where(ok & (dd < 120), tsm, np.nan)) if np.any(ok & (dd < 120)) else np.nan
deep = np.where(ok & (dd >= 120))[0]
ret_ref = float(np.nanpercentile(tsm[deep], 90)) if len(deep) else np.nan
low = ok & (tsm < 0.35 * min(cone_ref, ret_ref)) & (dd > 20)
bands = []; i = 0
while i < len(low):
    if low[i]:
        j = i
        while j + 1 < len(low) and low[j + 1]: j += 1
        if dd[j] - dd[i] >= 40 and np.any(ok[j + 1:] & (tsm[j + 1:] > 0.6 * ret_ref)): bands.append((float(dd[i]), float(dd[j])))
        i = j + 1
    else: i += 1
tissue_end = float(dd[np.where(ti > 0.8)[0].max()]) if np.any(ti > 0.8) else 0.0
# texture dip: the 40 um window (60 um down to 40 um above the tissue end) with the lowest texture, against the textured
# tissue below it (75th percentile); a clear zone gives a deep dip with textured retina underneath
dip = None; wn = int(round(40 / VX))
for k in range(len(dd) - wn):
    if dd[k] < 60 or dd[k + wn] > tissue_end - 40 or not np.all(ok[k:k + wn]): continue
    below = tsm[k + wn:][ok[k + wn:]]
    if len(below) < wn: continue
    r_ = float(np.mean(tsm[k:k + wn]) / np.percentile(below, 75))
    if dip is None or r_ < dip['ratio']: dip = dict(from_um=float(dd[k]), to_um=float(dd[k + wn]), ratio=r_)
# column trace depth: deepest depth reached from 20 um with aligned30 >= 0.5, allowing gaps under 10 um
# column runs: depth ranges where at least half the tissue voxels have their column axis within 30 deg of the surface normal
# (gaps under 10 um bridged); the longest run and the total aligned depth
alsm = ndi.uniform_filter1d(np.nan_to_num(al), 3); good = ok & (alsm >= 0.5)
runs = []; k = 0
while k < len(dd):
    if good[k]:
        j = k; g_ = 0
        while j + 1 < len(dd) and (good[j + 1] or g_ < 10 / VX):
            j += 1; g_ = 0 if good[j] else g_ + 1
        while not good[j]: j -= 1
        runs.append((float(dd[k]), float(dd[j]))); k = j + 1
    else: k += 1
run_end = max(runs, key=lambda r: r[1] - r[0]) if runs else None

# cross-section through the sheet centre: plane of the mean inward normal and the sheet's long axis
j0 = int(np.argmin(np.linalg.norm(Pc - Pc.mean(0), axis=1))); nbar = Ns.mean(0); nbar /= np.linalg.norm(nbar)
Qc = Pc - Pc[j0]; Qc = Qc - np.outer(Qc @ nbar, nbar); ev = np.linalg.eigh(np.cov(Qc.T))[1][:, -1]
Ngrid = 400; ext = min(float(np.abs(Qc @ ev).max()) + 20, 1100 / VX)
uu = np.linspace(-ext, ext, Ngrid); rr = np.linspace(-20, 650 / VX, Ngrid)
GU, GR = np.meshgrid(uu, rr)
pts = Pc[j0][:, None, None] + nbar[:, None, None] * GR[None] + ev[:, None, None] * GU[None]
sl = ndi.map_coordinates(I, pts.reshape(3, -1), order=1, cval=0).reshape(Ngrid, Ngrid)
np.save(f'{OUT}/{NAME}-xsec.npy', sl.astype(np.float32))

out = dict(name=NAME, shape_zyx=list(V.shape), iso_shape=list(I.shape), background=bg, threshold=thr,
           seed_iso=list(SEEDS[NAME]), sheet=dict(points=int(len(Pc)), extent_um=ext_pts.tolist()),
           sphere=dict(radius_um=Rs * VX, rms_um=float(res.std() * VX), local_seed_sphere_um=R * VX), quadric=quad,
           local=dict(tiles=len(tiles), U_median=float(np.nanmedian(U)), U_q25=float(np.nanpercentile(U, 25)), U_q75=float(np.nanpercentile(U, 75)),
                      U_max=float(np.nanmax(U)), discs_placed=len(taken), r1_median_um=float(np.median([t['r1'] for t in tiles])) if tiles else None,
                      r2_median_um=float(np.median([t['r2'] for t in tiles])) if tiles else None, tile_list=tiles),
           clear_zone_bands_um=bands, texture_dip=dip, tissue_end_um=tissue_end, column_runs_um=runs, longest_column_run_um=run_end, aligned_depth_um=float(good.sum() * VX),
           texture_ref=dict(cone=float(cone_ref), retina=ret_ref), profile=prof, xsec=dict(ext_um=float(ext * VX), top_um=48.0, bottom_um=-650.0),
           seconds=round(time.time() - T0, 1))
json.dump(out, open(f'{OUT}/{NAME}-survey.json', 'w'), indent=1)
log(f'clear-zone bands {bands}, dip {dip}, tissue to {tissue_end:.0f} um, column runs {runs}')
print('PROGRESS 1.0 done', flush=True); print('SURVEY ok', flush=True)
# diagnostic overlay (kept on the compute machine): the cornea sheet on the three middle iso slices
try:
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    f_, a3 = plt.subplots(1, 3, figsize=(15, 5)); mid = sh // 2; Pi = Pc.round().astype(int)
    for k, (axn, sl2) in enumerate(((0, I[mid[0]]), (1, I[:, mid[1]]), (2, I[:, :, mid[2]]))):
        a3[k].imshow(sl2, cmap='gray', vmax=np.percentile(sl2, 99.5)); m_ = np.abs(Pi[:, axn] - mid[axn]) <= 1
        rest = [i for i in range(3) if i != axn]; a3[k].plot(Pi[m_, rest[1]], Pi[m_, rest[0]], 'r.', ms=1)
        a3[k].plot(seed[rest[1]], seed[rest[0]], 'c+', ms=12)
    f_.savefig(f'{OUT}/{NAME}-sheet.png', dpi=50); plt.close(f_)
except Exception as ex: log(f'overlay skipped: {ex}')
