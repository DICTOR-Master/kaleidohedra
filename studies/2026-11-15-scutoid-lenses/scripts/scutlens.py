#!/usr/bin/env python3
"""Scutoid lenses pilot (study 2026-11-15-scutoid-lenses). Ray-geometry model of aperture arrays in front of an eye.
Parts: A single-aperture depth of focus + the fingerprint observation; B the exactly-one law for hole arrays in the plane
(hex, square, Poisson); C hole layouts on a spectacle mask (flat sheet, bent hex sheet, geodesic icosahedral, golden spiral,
random) judged over gaze directions; D neighbour swaps (scutoids) of the hole columns between the back and front surfaces.
Usage: scutlens.py OUT.json [--quick]. Prints PROGRESS lines and FINAL ok iff every control passes.
All eye dimensions are typical textbook values (assumed, not measured): see README."""
import sys, json, time, math
import numpy as np
from scipy.spatial import Delaunay
from scipy.special import j1

T0 = time.time()
def prog(f, what): print(f'PROGRESS {f:.3f} {what} ({time.time()-T0:.0f} s)', flush=True)
OUT = sys.argv[1]; QUICK = '--quick' in sys.argv
rng = np.random.default_rng(20261115)
LAM = 555e-9                      # m, photopic peak
ARCMIN = math.pi / 180 / 60
R_C = 13.5                        # mm, corneal apex in front of the eye's centre of rotation C
R_P = 10.5                        # mm, entrance pupil in front of C
R_M = 25.5                        # mm, spectacle mask (12 mm vertex distance) from C
HD = 1.0                          # mm, hole diameter (commercial pinhole glasses: 0.9-1.2 mm)
CAP = math.radians(25.0)          # gaze range judged
res = {'assumed': dict(lambda_nm=555, cornea_from_C_mm=R_C, pupil_from_C_mm=R_P, mask_from_C_mm=R_M, hole_mm=HD, gaze_halfangle_deg=25)}
checks = {}

# ---------------- Part A: single aperture ----------------
def dof_total_D(p_mm, beta_arcmin):   # geometric: blur angle = p * defocus; +-beta/p
    return 2 * beta_arcmin * ARCMIN / (p_mm * 1e-3)
def airy_diam_arcmin(p_mm): return 2.44 * LAM / (p_mm * 1e-3) / ARCMIN
A = []
for p in [0.5, 0.8, 1.0, 1.36, 1.6, 2.0, 3.0, 4.0, 6.0]:
    A.append(dict(p_mm=p, dof_total_D_2arcmin=round(dof_total_D(p, 2), 2), airy_diam_arcmin=round(airy_diam_arcmin(p), 2),
                  light_vs_3mm=round((p / 3) ** 2, 3)))
popt = {dD: round(1e3 * math.sqrt(2.44 * LAM / dD), 3) for dD in [0.5, 1, 2, 4, 8, 16]}   # geometric blur = Airy diameter
res['A_single_aperture'] = A; res['A_best_pinhole_mm_for_defocus_D'] = popt
# fingerprint: near point 60 cm (residual accommodation 1/0.6 D), ridge period s
S_RIDGE = 0.48; NEAR = 0.60
def mtf_disk(x): return 1.0 if x == 0 else 2 * j1(math.pi * x) / (math.pi * x)
def mtf_diff(f_cpr, p_mm):         # diffraction MTF of a circular aperture, f in cycles/rad
    fc = (p_mm * 1e-3) / LAM; v = f_cpr / fc
    return 0.0 if v >= 1 else 2 / math.pi * (math.acos(v) - v * math.sqrt(1 - v * v))
FP = []
for p in [3.0, 2.0, 1.5, 1.0, 0.7, 0.5]:
    for d_cm in [40, 25, 15, 10, 7.5, 5]:
        d = d_cm / 100; dD = max(0.0, 1 / d - 1 / NEAR)
        feat = S_RIDGE * 1e-3 / d                      # ridge period angle (rad)
        b = p * 1e-3 * dD                              # blur disk diameter (rad)
        f = 1 / feat
        m = mtf_disk(b * f) * mtf_diff(f, p)
        FP.append(dict(pupil_mm=p, dist_cm=d_cm, defocus_D=round(dD, 2), ridge_arcmin=round(feat / ARCMIN, 1),
                       blur_arcmin=round(b / ARCMIN, 1), blur_over_ridge=round(b / feat, 2), ridge_contrast=round(m, 3)))
res['A_fingerprint'] = FP
res['A_fingerprint_limit'] = 'blur/ridge -> (p/s)(1 - d/near point) as d -> 0; diffraction/ridge = 2.44 lambda d/(p s) -> 0'
prog(0.1, 'part A done')

# ---------------- Part B: exactly-one law in the plane ----------------
def circ_overlap(R, r, d):         # area of intersection of discs radius R, r at centre distance d (arrays)
    d = np.asarray(d, float); out = np.zeros_like(d)
    full = d <= abs(R - r); out[full] = math.pi * min(R, r) ** 2
    part = (d < R + r) & ~full; dd = d[part]
    a1 = np.arccos(np.clip((dd**2 + R*R - r*r) / (2*dd*R), -1, 1)); a2 = np.arccos(np.clip((dd**2 + r*r - R*R) / (2*dd*r), -1, 1))
    out[part] = R*R*a1 + r*r*a2 - 0.5*np.sqrt(np.clip((-dd+R+r)*(dd+R-r)*(dd-R+r)*(dd+R+r), 0, None))
    return out
def lattice(kind, a, L):
    n = int(L / a) + 3; i, j = np.meshgrid(np.arange(-n, n + 1), np.arange(-n, n + 1)); i = i.ravel(); j = j.ravel()
    if kind == 'hex': return np.c_[a * (i + 0.5 * j), a * j * math.sqrt(3) / 2]
    return np.c_[a * i, a * j]
def plane_stats(P, rho, r_h, Q):   # Q: sample pupil centres; returns P(n50=0,1,>=2), mean throughput
    from scipy.spatial import cKDTree
    t = cKDTree(P); n0 = n1 = n2 = 0; thr = 0.0
    lists = t.query_ball_point(Q, rho + r_h)
    for q, L in zip(Q, lists):
        if not L: n0 += 1; continue
        ov = circ_overlap(rho, r_h, np.linalg.norm(P[L] - q, axis=1)) if r_h > 0 else None
        if r_h > 0: n = int((ov >= 0.5 * math.pi * r_h * r_h).sum()); thr += ov.sum() / (math.pi * rho * rho)
        else: n = int((np.linalg.norm(P[L] - q, axis=1) < rho).sum())
        n0 += n == 0; n1 += n == 1; n2 += n >= 2
    m = len(Q); return n0 / m, n1 / m, n2 / m, thr / m
NB = 4000 if QUICK else 10000
B = {}
for p in [2.0, 3.0, 4.0]:
    rho = p / 2
    for kind in ['hex', 'square']:
        for rh in [0.0, HD / 2]:
            rows = []
            for ratio in np.arange(0.70, 1.81, 0.02):
                a = ratio * p; P = lattice(kind, a, 4 * a + 4 * rho)
                cell = np.array([[a, 0], [a * 0.5, a * math.sqrt(3) / 2]]) if kind == 'hex' else np.array([[a, 0], [0, a]])
                Q = rng.random((NB, 2)) @ cell
                s = plane_stats(P, rho, rh, Q); rows.append([round(ratio, 2)] + [round(x, 4) for x in s])
            best = max(rows, key=lambda r: r[2])
            B[f'{kind}_p{p}_hole{rh*2}'] = dict(best_spacing_over_pupil=best[0], best_P1=best[2], best_P0=best[1], best_P2=best[3],
                                                best_throughput=best[4], scan=rows)
    prog(0.1 + 0.15 * (p - 1) / 3, f'part B pupil {p}')
# Poisson control: P(n=1) = mu e^-mu, max 1/e
mus = np.linspace(0.5, 1.5, 11); pois = []
for mu in mus:
    Lbox = 80.0; rho = 1.0; lam = mu / (math.pi * rho * rho); acc = []
    for rep in range(8):              # pilot fault 15 Nov: one realization per mu was too noisy for the control
        N = rng.poisson(lam * Lbox * Lbox); P = rng.random((N, 2)) * Lbox; Q = 5 + rng.random((NB // 2, 2)) * (Lbox - 10)
        acc.append(plane_stats(P, rho, 0.0, Q)[1])
    pois.append([round(mu, 2), round(float(np.mean(acc)), 4), round(mu * math.exp(-mu), 4)])
B['poisson_points'] = pois
res['B_plane'] = B
pmax = 1 / math.e
checks['poisson_P1_matches_mu_exp_minus_mu'] = max(abs(r[1] - r[2]) for r in pois) < 0.012
checks['exactly_one_never_everywhere'] = all(v['best_P1'] < 1 for k, v in B.items() if k != 'poisson_points')
checks['hex_beats_poisson'] = B['hex_p3.0_hole0.0']['best_P1'] > pmax
prog(0.3, 'part B done')

# ---------------- Part C: layouts on a mask, judged over gaze ----------------
def unit(v): return v / np.linalg.norm(v, axis=-1, keepdims=True)
def sph(theta, phi): return np.c_[np.sin(theta) * np.cos(phi), np.sin(theta) * np.sin(phi), np.cos(theta)]
HOLECAP = math.radians(42)
def lay_hexflat(a):
    P = lattice('hex', a, R_M * math.tan(HOLECAP)); P = P[np.hypot(*P.T) <= R_M * math.tan(HOLECAP)]
    H = np.c_[P, np.full(len(P), R_M)]; return H, np.tile([0, 0, 1.0], (len(H), 1))
def lay_hexbent(a):                 # perforated flat sheet bent onto the sphere about C (azimuthal equidistant)
    P = lattice('hex', a, R_M * HOLECAP); r = np.hypot(*P.T); P = P[r <= R_M * HOLECAP]; r = np.hypot(*P.T)
    H = R_M * sph(r / R_M, np.arctan2(P[:, 1], P[:, 0])); return H, unit(H)
def icosa(vertex_up):
    g = (1 + 5 ** .5) / 2
    V = np.array([[-1, g, 0], [1, g, 0], [-1, -g, 0], [1, -g, 0], [0, -1, g], [0, 1, g], [0, -1, -g], [0, 1, -g], [g, 0, -1], [g, 0, 1], [-g, 0, -1], [-g, 0, 1]], float)
    V = unit(V); F = []
    for i in range(12):
        for j in range(i + 1, 12):
            for k in range(j + 1, 12):
                if all(np.dot(V[x], V[y]) > 0.4 for x, y in [(i, j), (j, k), (i, k)]): F.append((i, j, k))
    up = V[0] if vertex_up else unit(V[F[0][0]] + V[F[0][1]] + V[F[0][2]])
    z = np.array([0, 0, 1.0]); ax = np.cross(up, z); s = np.linalg.norm(ax); c = np.dot(up, z)
    if s > 1e-12:
        ax /= s; K = np.array([[0, -ax[2], ax[1]], [ax[2], 0, -ax[0]], [-ax[1], ax[0], 0]]); Rm = np.eye(3) + s * K + (1 - c) * K @ K; V = V @ Rm.T
    return V, F
def lay_geodesic(a, vertex_up):
    V, F = icosa(vertex_up); best = None
    for nu in range(4, 80):
        pts = []
        for (i, j, k) in F:
            for u in range(nu + 1):
                for v in range(nu + 1 - u):
                    pts.append((u * V[i] + v * V[j] + (nu - u - v) * V[k]) / nu)
        P = np.unique(np.round(unit(np.array(pts)), 9), axis=0)
        from scipy.spatial import cKDTree
        near = P[P[:, 2] > math.cos(math.radians(20))]; dd, _ = cKDTree(P).query(near, 2); sp = R_M * dd[:, 1].mean()
        if best is None or abs(sp - a) < abs(best[0] - a): best = (sp, nu, P)
        if sp < a * 0.9: break
    P = best[2][best[2][:, 2] >= math.cos(HOLECAP)]; return R_M * P, P, best[1], best[0]
def lay_golden(a):
    N = int(round(4 * math.pi * R_M ** 2 / (math.sqrt(3) / 2 * a * a))); k = np.arange(N) + 0.5
    z = 1 - 2 * k / N; phi = k * math.pi * (3 - 5 ** .5); P = np.c_[np.sqrt(1 - z * z) * np.cos(phi), np.sqrt(1 - z * z) * np.sin(phi), z]
    P = P[P[:, 2] >= math.cos(HOLECAP)]; return R_M * P, P
def lay_random(a):
    area = 2 * math.pi * R_M ** 2 * (1 - math.cos(HOLECAP)); N = rng.poisson(area / (math.sqrt(3) / 2 * a * a))
    z = rng.uniform(math.cos(HOLECAP), 1, N); phi = rng.uniform(0, 2 * math.pi, N)
    P = np.c_[np.sqrt(1 - z * z) * np.cos(phi), np.sqrt(1 - z * z) * np.sin(phi), z]; return R_M * P, P
def gaze_samples(n):
    z = rng.uniform(math.cos(CAP), 1, n); phi = rng.uniform(0, 2 * math.pi, n)
    return np.c_[np.sqrt(1 - z * z) * np.cos(phi), np.sqrt(1 - z * z) * np.sin(phi), z]
def judge(H, Nh, p, d_obj, G):
    rho = p / 2; out = []; seps = []; nlist = []; thr = []
    for gs in np.array_split(G, max(1, len(G) // 2000)):
        hu = H @ gs.T                                   # (N, g)
        if d_obj is None:                               # distant object: rays parallel to gaze
            q = H[:, None, :] - (hu - R_P)[:, :, None] * gs[None, :, :]
            cosi = np.abs(Nh @ gs.T); rh = HD / 2 * np.sqrt(cosi)
        else:
            Oc = R_C + d_obj; O = Oc * gs
            t = (Oc - R_P) / (Oc - hu)
            q = O[None] + (H[:, None, :] - O[None]) * t[:, :, None]
            w = unit(H[:, None, :] - O[None]); cosi = np.abs(np.einsum('nk,ngk->ng', Nh, w)); rh = HD / 2 * t * np.sqrt(cosi)
        dist = np.linalg.norm(q - R_P * gs[None], axis=2)
        ov = np.zeros_like(dist); m = dist < rho + rh
        if m.any(): ov[m] = np.array([circ_overlap(rho, r, np.array([dd]))[0] for r, dd in zip(rh[m], dist[m])])
        sig = ov >= 0.5 * math.pi * rh * rh
        n = sig.sum(0); nlist.append(n); thr.append(ov.sum(0) / (math.pi * rho * rho))
        for g in np.where(n >= 2)[0]:
            Qs = q[sig[:, g], g]; seps.append(max(np.linalg.norm(x - y) for x in Qs for y in Qs))
    n = np.concatenate(nlist); thr = np.concatenate(thr); th = np.degrees(np.arccos(np.clip(G[:, 2], -1, 1)))
    bins = {f'{lo}-{hi}deg_P1': round(float((n[(th >= lo) & (th < hi)] == 1).mean()), 4) for lo, hi in [(0, 10), (10, 20), (20, 25.01)]}
    return dict(P0=round(float((n == 0).mean()), 4), P1=round(float((n == 1).mean()), 4), P2=round(float((n >= 2).mean()), 4),
                throughput=round(float(thr.mean()), 4), throughput_min=round(float(thr.min()), 4),
                scheiner_sep_mm=round(float(np.mean(seps)), 3) if seps else 0.0,
                scheiner_arcmin_per_D=round(float(np.mean(seps)) * 1e-3 / ARCMIN, 1) if seps else 0.0, **bins)
NG = 3000 if QUICK else 8000
G = gaze_samples(NG)
C = {}; layouts_used = {}
spacings = {'commercial_3.0mm': 3.0, 'bestplane_p3': round(B['hex_p3.0_hole1.0']['best_spacing_over_pupil'] * 3.0, 3)}
jobs = [(sn, a) for sn, a in spacings.items()]; step = 0
for sn, a in jobs:
    L = {}
    L['hex_flat_sheet'] = lay_hexflat(a)
    L['hex_bent_sheet'] = lay_hexbent(a)
    Hg, Ng_, nu, sp = lay_geodesic(a, False); L['geodesic_face_centre_up'] = (Hg, Ng_); layouts_used[f'{sn}_geodesic_nu'] = [nu, round(sp, 3)]
    Hv, Nv, nu2, sp2 = lay_geodesic(a, True); L['geodesic_pentagon_on_axis'] = (Hv, Nv)
    L['golden_spiral'] = lay_golden(a)
    L['random_control'] = lay_random(a)
    for ln, (H, Nh) in L.items():
        layouts_used[f'{sn}_{ln}_holes'] = int(len(H))
        for p in [2.0, 3.0, 4.0]:
            for dn, d in [('far', None), ('read40cm', 400.0)]:
                C[f'{sn}|{ln}|p{p}|{dn}'] = judge(H, Nh, p, d, G)
        step += 1; prog(0.3 + 0.5 * step / (len(jobs) * len(L)), f'part C {sn} {ln}')
res['C_mask_layouts'] = C; res['C_layout_info'] = layouts_used
checks['C_no_layout_exactly_one_everywhere'] = all(v['P1'] < 1 for v in C.values())
checks['C_random_worse_than_hexbent'] = all(C[f'{sn}|random_control|p3.0|far']['P1'] < C[f'{sn}|hex_bent_sheet|p3.0|far']['P1'] for sn in spacings)

# ---------------- Part D: columns between back and front surface; neighbour swaps ----------------
def delaunay_edges(XY, keep):
    T = Delaunay(XY).simplices; E = set()
    for t in T:
        for x, y in [(t[0], t[1]), (t[1], t[2]), (t[0], t[2])]:
            if keep[x] and keep[y]: E.add((min(x, y), max(x, y)))
    return E
def stereo(P, centre, R):           # stereographic projection of points on sphere (centre, R) from its -z pole
    r = P - centre; return r[:, :2] / (1 + r[:, 2:3] / R)
def front_points(Udir, kind):
    if kind == 'concentric_27.5': R = 27.5; c = np.zeros(3); t = np.full(len(Udir), R)
    elif kind == 'plano_front':
        t = 27.5 / Udir[:, 2]; return Udir * t[:, None], None, None
    else:
        R = {'base6D_R87.2': 87.2, 'base10D_R52.3': 52.3, 'base2D_R261': 261.5}[kind]; c = np.array([0, 0, 27.5 - R])
        b = Udir @ c; t = b + np.sqrt(b * b - (c @ c - R * R))
    return Udir * t[:, None], c, R
def swaps(H):
    U = unit(H); back = R_M * U; keep = U[:, 2] >= math.cos(math.radians(30))
    Eb = delaunay_edges(stereo(back, np.zeros(3), R_M), keep); row = {}
    for kind in ['concentric_27.5', 'base2D_R261', 'base6D_R87.2', 'base10D_R52.3', 'plano_front']:
        Fp, c, R = front_points(U, kind)
        XY = Fp[:, :2] if c is None else stereo(Fp, c, R)
        Ef = delaunay_edges(XY, keep); row[kind] = len(Eb ^ Ef) // 2
    row['interior_edges'] = len(Eb); return row
def max_aspect(kind):               # local anisotropy of the radial map back sphere -> front surface, over the gaze cap
    worst = 1.0
    for th in np.radians(np.linspace(1, 30, 30)):
        e = 1e-5; u0 = sph(np.array([th]), np.array([0.0]))
        ut = sph(np.array([th]), np.array([e / max(math.sin(th), 1e-9)])); ur = sph(np.array([th + e]), np.array([0.0]))
        f0 = front_points(u0, kind)[0][0]; ft = front_points(ut, kind)[0][0]; fr = front_points(ur, kind)[0][0]
        st = np.linalg.norm(ft - f0) / (R_M * e); sr = np.linalg.norm(fr - f0) / (R_M * e); worst = max(worst, max(st, sr) / min(st, sr))
    return round(worst, 4)
D = {'max_aspect_ratio': {k: max_aspect(k) for k in ['concentric_27.5', 'base2D_R261', 'base6D_R87.2', 'base10D_R52.3', 'plano_front']}}
a = 3.0
D['hex_bent_sheet'] = swaps(lay_hexbent(a)[0]); D['hex_flat_sheet'] = swaps(lay_hexflat(a)[0])
D['geodesic_face_centre_up'] = swaps(lay_geodesic(a, False)[0]); D['geodesic_pentagon_on_axis'] = swaps(lay_geodesic(a, True)[0])
D['golden_spiral'] = swaps(lay_golden(a)[0]); D['random_control'] = swaps(lay_random(a)[0])
# control: hexagonal lattice stretched along a row by k flips its row edges exactly beyond sqrt(3)
P = lattice('hex', 1.0, 12.0); keep = np.hypot(*P.T) < 8
E0 = delaunay_edges(P, keep)
ctrl = {}
for k in [1.0, 1.5, 1.70, 1.76, 2.0]:
    ctrl[str(k)] = len(E0 ^ delaunay_edges(P * [k, 1], keep)) // 2
D['control_hex_stretch_swaps'] = ctrl
res['D_column_swaps_a3mm'] = D
checks['D_concentric_zero_swaps'] = all(D[l]['concentric_27.5'] == 0 for l in D if isinstance(D[l], dict) and 'concentric_27.5' in D[l] and l != 'max_aspect_ratio')
checks['D_stretch_control_sqrt3'] = ctrl['1.0'] == 0 and ctrl['1.5'] == 0 and ctrl['1.7'] == 0 and ctrl['1.76'] > 0
prog(0.95, 'part D done')
checks = {k: bool(v) for k, v in checks.items()}; res['checks'] = checks
json.dump(res, open(OUT, 'w'), indent=1)
nf = sum(not v for v in checks.values())
for k, v in checks.items(): print('CHECK', k, v)
print(f'wrote {OUT} in {time.time()-T0:.0f} s')
print('FINAL ok' if nf == 0 else f'FINAL FAIL ({nf} checks)')
