#!/usr/bin/env python3
"""DICTO · dictospheres.com — Special geometry of the human sacrum, Part A (study 2026-11-12-sacrum-geometry).

Measures a sacrum mesh (BodyParts3D, DBCLS) and a population of sacra (TotalSegmentator small set masks -> marching cubes),
with the same code on controls of known shape (cone, sphere, a sacrum phantom with known foramina, curvature and wedge) and on
non-sacred bones (5th and 4th lumbar vertebrae, hip bone, scapula) to see whether "notable" ratios turn up by chance.

Usage: python3 -I sacrum_geom.py MODE DLDIR OUTDIR [MAXSUBJ]
  MODE = pilot | full ; DLDIR = download folder (BodyParts3D obj/ + ts/ masks) ; OUTDIR = study folder (data/ figures/ written)
Prints PROGRESS lines, one 'ok/FAIL <check>' line per control, and a conditional FINAL line.
"""
import sys, os, json, gzip, struct, math, csv, time
sys.stdout.reconfigure(line_buffering=True)   # python -I ignores PYTHONUNBUFFERED; PROGRESS lines must reach the log live
import numpy as np
from scipy import ndimage, optimize
from scipy.spatial import cKDTree
import trimesh
from skimage import measure
from shapely.geometry import Polygon
from shapely.validation import make_valid
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

PHI = (1 + 5 ** 0.5) / 2
CONSTS = {'φ': PHI, 'φ²': PHI ** 2, '√φ': PHI ** 0.5, '√2': 2 ** 0.5, '√3': 3 ** 0.5, '√5': 5 ** 0.5,
          '3/2': 1.5, '4/3': 4 / 3, '5/4': 1.25, '2': 2.0, 'π/2': math.pi / 2, 'e/2': math.e / 2}
RMAX = 3.5           # ratios are folded to >= 1; the chance test works on [1, RMAX]
TOLS = [0.01, 0.02]  # relative tolerance for "near"
MARK = 'DICTO · dictospheres.com'
BP3D_CREDIT = 'Mesh: BodyParts3D, © The Database Center for Life Science, CC BY 4.0'
TS_CREDIT = 'Masks: TotalSegmentator dataset (Wasserthal et al. 2023), CC BY 4.0'
RES = 0.5            # raster pixel, mm
CHECKS = []


def check(name, ok, detail=''):
    CHECKS.append((name, bool(ok), detail))
    print(f"{'ok' if ok else 'FAIL'} {name} {detail}")


def unit(v): v = np.asarray(v, float); return v / np.linalg.norm(v)
def perp(v, n): return v - np.dot(v, n) * n


# ---------------------------------------------------------------- input
def read_nii(path):
    raw = gzip.open(path, 'rb').read()
    e = '<' if struct.unpack('<i', raw[:4])[0] == 348 else '>'
    dim = struct.unpack(e + '8h', raw[40:56]); datatype = struct.unpack(e + 'h', raw[70:72])[0]
    pixdim = struct.unpack(e + '8f', raw[76:108]); vox = int(struct.unpack(e + 'f', raw[108:112])[0])
    qcode, scode = struct.unpack(e + 'hh', raw[252:256])
    qb, qc, qd, qx, qy, qz = struct.unpack(e + '6f', raw[256:280])
    srow = np.array(struct.unpack(e + '12f', raw[280:328]), float).reshape(3, 4)
    dt = {2: 'u1', 4: 'i2', 8: 'i4', 16: 'f4', 64: 'f8', 256: 'i1', 512: 'u2', 768: 'u4'}[datatype]
    nx, ny, nz = dim[1:4]
    arr = np.frombuffer(raw, dtype=np.dtype(dt).newbyteorder(e), count=nx * ny * nz, offset=vox).reshape((nz, ny, nx)).transpose(2, 1, 0)
    if scode > 0:
        A = srow
    else:
        a = math.sqrt(max(0.0, 1 - qb * qb - qc * qc - qd * qd))
        R = np.array([[a*a+qb*qb-qc*qc-qd*qd, 2*(qb*qc-a*qd), 2*(qb*qd+a*qc)],
                      [2*(qb*qc+a*qd), a*a+qc*qc-qb*qb-qd*qd, 2*(qc*qd-a*qb)],
                      [2*(qb*qd-a*qc), 2*(qc*qd+a*qb), a*a+qd*qd-qb*qb-qc*qc]])
        qfac = pixdim[0] if pixdim[0] in (1.0, -1.0) else 1.0
        A = np.hstack([R @ np.diag([pixdim[1], pixdim[2], qfac * pixdim[3]]), [[qx], [qy], [qz]]])
    return arr, A


def mask_to_mesh(mask, A, sigma=0.6):
    lab, n = ndimage.label(mask > 0)
    if n == 0: return None
    sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
    m = (lab == 1 + int(np.argmax(sizes))).astype(np.float32)
    m = ndimage.gaussian_filter(np.pad(m, 2), sigma)
    v, f, _, _ = measure.marching_cubes(m, 0.5)
    v = v - 2
    mesh = trimesh.Trimesh((A[:, :3] @ v.T).T + A[:, 3], f, process=True)
    if mesh.is_watertight and mesh.volume < 0: mesh.invert()
    return mesh


def load_obj(path):
    m = trimesh.load(path, force='mesh', process=True)
    if m.is_watertight and m.volume < 0: m.invert()
    return m


def surf_centroid(mesh):
    a = mesh.area_faces
    return (mesh.triangles_center * a[:, None]).sum(0) / a.sum()


def sample(mesh, density, seed=1):
    n = int(min(2_000_000, max(20000, mesh.area * density)))
    P, fi = trimesh.sample.sample_surface(mesh, n, seed=seed)
    return np.asarray(P), mesh.face_normals[fi]


# ---------------------------------------------------------------- 2D tools
def raster_front(X, Y, F, N=None, res=RES, pad=4.0):
    """Front-most value of F per pixel on the (X, Y) plane; returns depth image, normal-index image, grid origin."""
    x0, y0 = X.min() - pad, Y.min() - pad
    nx, ny = int((X.max() + pad - x0) / res) + 1, int((Y.max() + pad - y0) / res) + 1
    ix, iy = ((X - x0) / res).astype(int), ((Y - y0) / res).astype(int)
    key = iy * nx + ix
    order = np.lexsort((F, key))
    k_sorted = key[order]
    last = np.r_[k_sorted[1:] != k_sorted[:-1], True]
    sel = order[last]
    D = np.full(ny * nx, np.nan); D[key[sel]] = F[sel]
    I = np.full(ny * nx, -1); I[key[sel]] = sel
    return D.reshape(ny, nx), I.reshape(ny, nx), (x0, y0, res)


def disk(rpx):
    r = int(math.ceil(rpx)); yy, xx = np.mgrid[-r:r + 1, -r:r + 1]; return (xx ** 2 + yy ** 2) <= rpx ** 2


def largest(mask):
    lab, n = ndimage.label(mask)
    if n == 0: return mask
    s = ndimage.sum(mask, lab, range(1, n + 1)); return lab == 1 + int(np.argmax(s))


def mask_polygon(mask, grid):
    x0, y0, res = grid
    cs = measure.find_contours(np.pad(mask.astype(float), 1), 0.5)
    c = max(cs, key=len)
    xy = np.c_[x0 + (c[:, 1] - 1 + 0.5) * res, y0 + (c[:, 0] - 1 + 0.5) * res]
    p = Polygon(xy).simplify(res * 0.5)
    return make_valid(p) if not p.is_valid else p


def iou(a, b):
    try:
        if not b.is_valid: b = make_valid(b)
        i = a.intersection(b).area; u = a.union(b).area
        return i / u if u > 0 else 0.0
    except Exception:
        return 0.0


def arc_pts(p, q, sag, n=40):
    """Circular arc from p to q through the point at signed sagitta sag*|pq| to the left of p->q."""
    p, q = np.asarray(p, float), np.asarray(q, float); d = q - p; L = np.linalg.norm(d)
    if abs(sag) < 1e-4 or L < 1e-9: return np.linspace(p, q, n, endpoint=False)
    nrm = np.array([-d[1], d[0]]) / L; m3 = (p + q) / 2 + nrm * sag * L
    (ax_, ay), (bx, by), (cx, cy) = p, m3, q
    D = 2 * (ax_ * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    ux = ((ax_**2 + ay**2) * (by - cy) + (bx**2 + by**2) * (cy - ay) + (cx**2 + cy**2) * (ay - by)) / D
    uy = ((ax_**2 + ay**2) * (cx - bx) + (bx**2 + by**2) * (ax_ - cx) + (cx**2 + cy**2) * (bx - ax_)) / D
    c = np.array([ux, uy]); R = np.linalg.norm(p - c)
    a0, am, a1 = (math.atan2(*(v - c)[::-1]) for v in (p, m3, q))
    tw = 2 * math.pi
    da = (a1 - a0) % tw if (am - a0) % tw <= (a1 - a0) % tw else -((a0 - a1) % tw)
    t = np.linspace(0, 1, n, endpoint=False); ang = a0 + da * t
    return c + R * np.c_[np.cos(ang), np.sin(ang)]


def fit_shapes(poly):
    """Fit triangle, curved triangle (3 circular-arc sides) and general quadrilateral (wedge) to a polygon by max IoU."""
    xy = np.array(poly.exterior.coords)
    xmin, ymin, xmax, ymax = poly.bounds; h = ymax - ymin
    top = xy[xy[:, 1] > ymax - 0.25 * h]
    t0 = np.array([[top[:, 0].min(), ymax], [top[:, 0].max(), ymax], [xy[np.argmin(xy[:, 1]), 0], ymin]])
    def tri(p): return Polygon(p.reshape(3, 2))
    best = None
    for s in (1.0, 0.9, 1.1):
        x0 = t0.copy(); x0[:2, 1] = ymin + s * h; x0 = x0.ravel()
        r = optimize.minimize(lambda p: 1 - iou(poly, tri(p)), x0, method='Nelder-Mead',
                              options={'maxiter': 3000, 'xatol': 1e-3, 'fatol': 1e-7})
        if best is None or r.fun < best.fun: best = r
    T = best.x.reshape(3, 2); out = {'triangle': {'vertices': T.tolist(), 'iou': 1 - best.fun}}
    # angles
    def ang(a, b, c):
        u, v = b - a, c - a; return math.degrees(math.acos(np.clip(u @ v / np.linalg.norm(u) / np.linalg.norm(v), -1, 1)))
    out['triangle']['angles_deg'] = [ang(T[0], T[1], T[2]), ang(T[1], T[2], T[0]), ang(T[2], T[0], T[1])]
    # curved triangle
    def ctri(p):
        V = p[:6].reshape(3, 2); s = p[6:]
        pts = np.vstack([arc_pts(V[i], V[(i + 1) % 3], s[i]) for i in range(3)])
        return Polygon(pts)
    r = optimize.minimize(lambda p: 1 - iou(poly, ctri(p)), np.r_[T.ravel(), 0, 0, 0], method='Nelder-Mead',
                          options={'maxiter': 5000, 'xatol': 1e-4, 'fatol': 1e-8})
    out['curved_triangle'] = {'vertices': r.x[:6].reshape(3, 2).tolist(), 'sagitta_over_side': r.x[6:].tolist(), 'iou': 1 - r.fun}
    # wedge (general quadrilateral; apex split in two)
    apex = T[2]; side = T[1] - T[0]
    q0 = np.r_[T[0], T[1], apex + 0.05 * side, apex - 0.05 * side]
    def quad(p): return Polygon(p.reshape(4, 2))
    r = optimize.minimize(lambda p: 1 - iou(poly, quad(p)), q0, method='Nelder-Mead',
                          options={'maxiter': 5000, 'xatol': 1e-4, 'fatol': 1e-8})
    out['wedge_quadrilateral'] = {'vertices': r.x.reshape(4, 2).tolist(), 'iou': 1 - r.fun}
    # boundary distance of best triangle
    b = Polygon(T).exterior; pts = np.array(poly.exterior.coords)
    from shapely.geometry import Point
    dd = np.array([b.distance(Point(p)) for p in pts[::max(1, len(pts) // 400)]])
    out['triangle']['boundary_mean_mm'] = float(dd.mean()); out['triangle']['boundary_max_mm'] = float(dd.max())
    return out


def fit_circle(x, y):
    A = np.c_[2 * x, 2 * y, np.ones_like(x)]; b = x * x + y * y
    cx, cy, k = np.linalg.lstsq(A, b, rcond=None)[0]; R0 = math.sqrt(k + cx * cx + cy * cy)
    r = optimize.least_squares(lambda p: np.hypot(x - p[0], y - p[1]) - p[2], [cx, cy, R0])
    res = r.fun; return {'centre': r.x[:2].tolist(), 'R': float(r.x[2]), 'rms': float(np.sqrt(np.mean(res ** 2))), 'max_abs': float(np.abs(res).max())}


def fit_logspiral(x, y, circ):
    """r = a exp(b theta) about a free centre; radial residuals; several starts."""
    best = None
    cx, cy = circ['centre']; R = circ['R']
    for b0 in (-0.4, -0.15, 0.0, 0.15, 0.4):
        for sh in (0.0, 0.3, -0.3):
            p0 = [cx + sh * R * 0.2, cy - sh * R * 0.2, math.log(R), b0]
            def resid(p):
                th = np.unwrap(np.arctan2(y - p[1], x - p[0])); th = th - th.mean()
                return np.hypot(x - p[0], y - p[1]) - np.exp(p[2] + p[3] * th)
            try:
                r = optimize.least_squares(resid, p0, max_nfev=4000)
            except Exception:
                continue
            if best is None or r.cost < best.cost: best = r
    res = best.fun; b = float(best.x[3])
    return {'centre': best.x[:2].tolist(), 'b': b, 'growth_per_quarter_turn': math.exp(abs(b) * math.pi / 2),
            'rms': float(np.sqrt(np.mean(res ** 2))), 'max_abs': float(np.abs(res).max()), '_p': best.x.tolist()}


def bic(rms, n, k): return n * math.log(max(rms, 1e-12) ** 2) + k * math.log(n)


# ---------------------------------------------------------------- chance model
def near(r, tol):
    hits = [k for k, c in CONSTS.items() if abs(r / c - 1) <= tol]
    return hits


def chance_fraction(tol, rmax=RMAX, names=None):
    iv = []
    for k, c in CONSTS.items():
        if names and k not in names: continue
        lo, hi = max(1.0, c / (1 + tol)), min(rmax, c * (1 + tol))
        if hi > lo: iv.append((math.log(lo), math.log(hi)))
    iv.sort(); tot = 0; cur = None
    for a, b in iv:
        if cur is None or a > cur[1]: tot += 0 if cur is None else cur[1] - cur[0]; cur = [a, b]
        else: cur[1] = max(cur[1], b)
    if cur: tot += cur[1] - cur[0]
    return tot / math.log(rmax)


def fold(r): return r if r >= 1 else 1 / r


# ---------------------------------------------------------------- generic ratio battery (any bone)
def battery(P):
    c = P.mean(0); _, _, Vt = np.linalg.svd(P - c, full_matrices=False); Q = (P - c) @ Vt.T
    e = np.sort(Q.max(0) - Q.min(0))[::-1]
    D, _, g = raster_front(Q[:, 0], Q[:, 1], Q[:, 2])
    S = ndimage.binary_fill_holes(ndimage.binary_closing(~np.isnan(D), disk(2)))
    S = largest(S)
    cols = S.sum(0) * RES; colx = g[0] + (np.arange(S.shape[1]) + 0.5) * RES
    occ = np.where(cols > 0)[0]; xa, xb = colx[occ[0]], colx[occ[-1]]; H = xb - xa
    def w_at(fr): return cols[np.argmin(np.abs(colx - (xa + fr * H)))]
    Wmax = cols.max(); poly = mask_polygon(S, g)
    r = {'e1/e2': e[0] / e[1], 'e2/e3': e[1] / e[2], 'e1/e3': e[0] / e[2], 'H/Wmax': H / Wmax,
         'w25/w50': w_at(.25) / w_at(.5), 'w75/w50': w_at(.75) / w_at(.5), 'w25/w75': w_at(.25) / w_at(.75),
         'perim/(2(H+W))': poly.length / (2 * (H + Wmax))}
    return {k: fold(float(v)) for k, v in r.items()}


# ---------------------------------------------------------------- curvature of a profile
def trim_ends(prof, tol=1.0, maxk=10):
    """Drop end points that belong to the end faces (end plate, tip): while an end point lies more than tol mm off the circle
    fitted to the points between the current ends, drop it (at most maxk per end; interior points are never dropped)."""
    i, j = 0, len(prof)
    for _ in range(2 * maxk):
        c = fit_circle(prof[i + 1:j - 1, 0], prof[i + 1:j - 1, 1]); cx, cy = c['centre']
        ri = abs(math.hypot(prof[i, 0] - cx, prof[i, 1] - cy) - c['R']); rj = abs(math.hypot(prof[j - 1, 0] - cx, prof[j - 1, 1] - cy) - c['R'])
        if max(ri, rj) <= tol: break
        if ri >= rj and i < maxk: i += 1
        elif j > len(prof) - maxk: j -= 1
        else: break
    return prof[i:j], [i, len(prof) - j]


def curv(prof, nboot=60):
    n = len(prof)
    seg = np.r_[0, np.cumsum(np.hypot(np.diff(prof[:, 0]), np.diff(prof[:, 1])))]
    circ = fit_circle(prof[:, 0], prof[:, 1]); spi = fit_logspiral(prof[:, 0], prof[:, 1], circ)
    o = {'n': n, 'arc_mm': float(seg[-1]), 'chord_mm': float(np.linalg.norm(prof[-1] - prof[0])), 'circle': circ,
         'logspiral': {k: v for k, v in spi.items() if k != '_p'},
         'bic_circle': bic(circ['rms'], n, 3), 'bic_spiral': bic(spi['rms'], n, 4),
         'arc_angle_deg': math.degrees(seg[-1] / circ['R'])}
    p0, p1 = prof[0], prof[-1]; d = unit(p1 - p0); nrm = np.array([-d[1], d[0]])
    o['max_depth_from_chord_mm'] = float(np.abs((prof - p0) @ nrm).max())
    rng = np.random.default_rng(7); bs, Rs = [], []
    for _ in range(nboot):
        k = np.unique(rng.integers(0, n, n))
        if len(k) < 8: continue
        cc = fit_circle(prof[k, 0], prof[k, 1]); Rs.append(cc['R'])
        bs.append(fit_logspiral(prof[k, 0], prof[k, 1], cc)['b'])
    o['R_boot_p2_5_p97_5'] = np.percentile(Rs, [2.5, 97.5]).tolist()
    o['b_boot_p2_5_p97_5'] = np.percentile(np.abs(bs), [2.5, 97.5]).tolist()
    return o, spi


# ---------------------------------------------------------------- the sacrum measurement
def measure_sacrum(sac, L5, hipL, hipR, tag):
    out = {'tag': tag}
    Ps, Ns = sample(sac, 12.0)
    cs = surf_centroid(sac)
    ex = unit(surf_centroid(hipL) - surf_centroid(hipR))             # towards the subject's left
    es0 = unit(perp(surf_centroid(L5) - cs, ex))                       # towards L5 (superior)
    ea = unit(np.cross(ex, es0))                                       # left x superior = anterior
    out['frame_world'] = {'left': ex.tolist(), 'superior': es0.tolist(), 'anterior': ea.tolist()}
    # S1 superior end plate: faces facing L5, near the midline, within 25 mm of L5, largest connected patch
    PL5, _ = sample(L5, 4.0); tL5 = cKDTree(PL5)
    Fc, Fn, Fa = sac.triangles_center, sac.face_normals, sac.area_faces
    dL5, _ = tL5.query(Fc)
    cand = (Fn @ es0 > 0.7) & (np.abs((Fc - cs) @ ex) < 20) & (dL5 < 25)
    comps = trimesh.graph.connected_components(sac.face_adjacency, nodes=np.where(cand)[0], min_len=1)
    comp = max(comps, key=lambda c: Fa[c].sum())
    w = Fa[comp]; B = (Fc[comp] * w[:, None]).sum(0) / w.sum()
    _, _, Vt = np.linalg.svd((Fc[comp] - B) * np.sqrt(w)[:, None], full_matrices=False)
    nb = Vt[2] * np.sign(Vt[2] @ es0)
    out['endplate'] = {'area_mm2': float(w.sum()), 'n_faces': int(len(comp)), 'dist_to_L5_median_mm': float(np.median(dL5[comp]))}
    # apex: midline sample farthest from B
    mid = np.abs((Ps - B) @ ex) < 15
    dB = np.linalg.norm(Ps - B, axis=1); P = Ps[mid][np.argmax(dB[mid])]
    ec = unit(perp(B - P, ex)); ef = unit(np.cross(ex, ec))
    out['frame_sacral'] = {'left': ex.tolist(), 'chord_up': ec.tolist(), 'front': ef.tolist()}
    X, C, F = (Ps - B) @ ex, (Ps - B) @ ec, (Ps - B) @ ef
    cP = float((P - B) @ ec)
    out['chord_mm'] = float(np.linalg.norm(P - B)); out['apex_c'] = cP
    ctop_ep = float(((Fc[comp] - B) @ ec).max())
    # promontory: most anterior end-plate point near the midline
    epx = (Fc[comp] - B) @ ex; epf = (Fc[comp] - B) @ ef
    near_mid = np.abs(epx) < 6
    Pr = Fc[comp][near_mid][np.argmax(epf[near_mid])] if near_mid.any() else Fc[comp][np.argmax(epf)]
    out['promontory_apex_mm'] = float(np.linalg.norm(Pr - P))
    # base angle: end plate normal vs chord, in the sagittal plane (positive = end plate faces forward)
    out['base_angle_deg'] = math.degrees(math.atan2(nb @ ef, nb @ ec))
    out['tilt_chord_vs_L5_axis_deg'] = math.degrees(math.acos(np.clip(ec @ es0, -1, 1)))
    # ---- front raster
    D, I, g = raster_front(X, C, F)
    occ = ~np.isnan(D)
    Sfull = largest(ndimage.binary_fill_holes(ndimage.binary_closing(occ, disk(2))))
    nf = np.full(D.shape, np.nan); nf[I >= 0] = (Ns[I[I >= 0]] @ ef)
    ys = g[1] + (np.arange(D.shape[0]) + 0.5) * RES; xs = g[0] + (np.arange(D.shape[1]) + 0.5) * RES
    YY, XX = np.meshgrid(ys, xs, indexing='ij')
    pelvic = (nf > 0.5) & (YY <= ctop_ep)
    pelvic = largest(ndimage.binary_fill_holes(ndimage.binary_closing(pelvic, disk(3))))
    out['outline_full'] = {}; out['outline_pelvic'] = {}
    polys = {}
    for nm, M in (('outline_full', Sfull), ('outline_pelvic', pelvic)):
        poly = mask_polygon(M, g); polys[nm] = poly
        xmn, ymn, xmx, ymx = poly.bounds
        out[nm] = {'width_mm': xmx - xmn, 'height_mm': ymx - ymn, 'area_mm2': poly.area, 'fits': fit_shapes(poly)}
    out['breadth_mm'] = out['outline_full']['width_mm']
    # ---- foramina: pits of the front depth map
    Dd = D.copy(); Dd[Sfull & ~occ] = np.nanmin(D) ; Dd[~Sfull] = np.nanmin(D) - 20
    Dd = np.nan_to_num(Dd, nan=np.nanmin(D) - 20)
    rpx = 7.0 / RES
    pit = ndimage.grey_closing(Dd, footprint=disk(rpx)) - Dd
    inner = ndimage.binary_erosion(Sfull, disk(3.0 / RES))
    candm = (pit > 2.0) & inner & (YY < -10) & (YY > cP + 3) & (np.abs(XX) > 6) & (np.abs(XX) < 40)
    lab, n = ndimage.label(candm)
    blobs = []
    for k in range(1, n + 1):
        m = lab == k; area = m.sum() * RES * RES
        if area < 3.0: continue
        wgt = pit[m]; bx = float((XX[m] * wgt).sum() / wgt.sum()); by = float((YY[m] * wgt).sum() / wgt.sum())
        blobs.append({'x': bx, 'c': by, 'area_mm2': float(area), 'depth_max_mm': float(pit[m].max()), 'score': float(wgt.sum() * RES * RES)})
    # pair left/right pits at matching level and mirrored distance; greedy by score; levels at least 8 mm apart
    Lb = [b for b in blobs if b['x'] > 0]; Rb = [b for b in blobs if b['x'] < 0]
    cand_pairs = sorted([(l['score'] + r_['score'], i, j) for i, l in enumerate(Lb) for j, r_ in enumerate(Rb)
                         if abs(l['c'] - r_['c']) < 7 and abs(l['x'] + r_['x']) < 10], reverse=True)
    usedL, usedR, picked = set(), set(), []
    for sc, i, j in cand_pairs:
        if i in usedL or j in usedR: continue
        lvl = (Lb[i]['c'] + Rb[j]['c']) / 2
        if any(abs(lvl - (Lb[a_]['c'] + Rb[b_]['c']) / 2) < 8 for a_, b_ in picked): continue
        picked.append((i, j)); usedL.add(i); usedR.add(j)
        if len(picked) == 4: break
    picked.sort(key=lambda ij: -(Lb[ij[0]]['c'] + Rb[ij[1]]['c']))
    sides = {'left': [Lb[i] for i, _ in picked], 'right': [Rb[j] for _, j in picked]}
    out['foramina'] = sides; out['foramina_blobs_all'] = len(blobs)
    out['foramina_pairs_found'] = len(picked)
    # ---- anterior midline profile (c, f): most anterior sample per 1 mm of c within |x| < 3 mm
    mm = (np.abs(X) < 3) & ((Ns @ ef) > 0.3)
    bins = np.arange(math.floor(cP), math.ceil(ctop_ep) + 1, 1.0)
    prof = []
    for a, b in zip(bins[:-1], bins[1:]):
        s = mm & (C >= a) & (C < b)
        if s.sum() >= 3: prof.append((float(C[s][np.argmax(F[s])]), float(F[s].max())))
    prof = np.array(prof)
    prof = prof[(prof[:, 0] >= cP + 2) & (prof[:, 0] <= ctop_ep)]
    prof, ntrim = trim_ends(prof); out['profile_trimmed_end_points'] = ntrim
    out['profile_n'] = int(len(prof))
    seg = np.r_[0, np.cumsum(np.hypot(np.diff(prof[:, 0]), np.diff(prof[:, 1])))]
    out['anterior_arc_mm'] = float(seg[-1]); out['anterior_chord_mm'] = float(np.linalg.norm(prof[-1] - prof[0]))
    out['curvature'], spi = curv(prof)
    circ = out['curvature']['circle']
    # ---- segments from foramen pair levels (Gray: the four pairs lie at the ends of the four transverse ridges)
    def arc_at(cv):
        return float(np.interp(cv, prof[:, 0], seg))
    lv = [(sides['left'][k]['c'] + sides['right'][k]['c']) / 2 for k in range(len(picked))]
    out['segments_valid'] = len(picked) == 4 and all(lv[k] - lv[k + 1] >= 8 for k in range(3)) and -lv[0] >= 8 and lv[3] - cP >= 8
    if out['segments_valid']:
        cPr = float((Pr - B) @ ec)   # S1 starts at the promontory (front edge of the S1 end plate)
        bounds = [cPr] + lv + [cP]
        Lc = [bounds[k] - bounds[k + 1] for k in range(5)]
        La = [abs(arc_at(bounds[k]) - arc_at(bounds[k + 1])) for k in range(5)]
        if cPr > prof[-1, 0]:   # the trimmed profile starts below the promontory: add the straight step to it
            La[0] += float(np.hypot(cPr - prof[-1, 0], (Pr - B) @ ef - prof[-1, 1]))
        out['promontory_c'] = cPr
        out['segments_chord_mm'] = Lc; out['segments_arc_mm'] = La
        sub = prof[prof[:, 0] >= lv[3]]
        if len(sub) >= 15: out['curvature_base_to_pair4'], _ = curv(sub)
        out['foramen_pair'] = []
        for k in range(4):
            l, r = sides['left'][k], sides['right'][k]
            out['foramen_pair'].append({'level_c': lv[k], 'transverse_spacing_mm': l['x'] - r['x'],
                                        'mid_offset_mm': (l['x'] + r['x']) / 2, 'level_diff_mm': l['c'] - r['c'],
                                        'area_left_mm2': l['area_mm2'], 'area_right_mm2': r['area_mm2']})
    # ---- auricular surfaces and wedge angles
    aur = {}
    for sd, hip, sg in (('left', hipL, 1), ('right', hipR, -1)):
        PH, _ = sample(hip, 4.0); th = cKDTree(PH); dh, _ = th.query(Fc)
        side = sg * ((Fc - B) @ ex) > 15
        dmin = float(np.percentile(dh[side], 0.5))
        sel = side & (dh < dmin + 3.0)
        w = Fa[sel]; cen = (Fc[sel] * w[:, None]).sum(0) / w.sum()
        _, sv, Vt = np.linalg.svd((Fc[sel] - cen) * np.sqrt(w)[:, None], full_matrices=False)
        nrm = Vt[2] * np.sign(sg * (Vt[2] @ ex))
        rms = float(np.sqrt(np.average(((Fc[sel] - cen) @ nrm) ** 2, weights=w)))
        aur[sd] = {'normal': nrm, 'area_mm2': float(w.sum()), 'plane_rms_mm': rms, 'gap_mm': dmin, 'centroid': cen}
    nLft, nRgt = aur['left']['normal'], aur['right']['normal']
    tot = 180 - math.degrees(math.acos(np.clip(nLft @ nRgt, -1, 1)))
    fr = math.degrees(math.atan2(nLft @ ec, nLft @ ex)) + math.degrees(math.atan2(nRgt @ ec, -(nRgt @ ex)))
    ax = math.degrees(math.atan2(nLft @ ef, nLft @ ex)) + math.degrees(math.atan2(nRgt @ ef, -(nRgt @ ex)))
    out['auricular'] = {sd: {k: (v.tolist() if isinstance(v, np.ndarray) else v) for k, v in a.items()} for sd, a in aur.items()}
    # SIGN NOTE (found 12 Nov after the full run): the frontal value is NEGATIVE when the bone is narrower below (phantom -38.5 =
    # its top-wide trapezoid); the key name '..._pos_narrower_below' is inverted but kept so the code matches data/results-full.json.
    # The axial key is correct: negative = narrower behind (wider in front).
    out['wedge'] = {'auricular_total_deg': tot, 'auricular_frontal_deg_pos_narrower_below': fr,
                    'auricular_axial_deg_pos_narrower_in_front': ax}
    # ---- the sacral ratios to test
    W = out['breadth_mm']; H = out['chord_mm']; SL = 1.0   # foramen level uncertainty (mm), from the phantom control
    R = {'breadth/chord (to tip)': W / H, 'breadth/promontory-tip (sacral index/100)': W / out['promontory_apex_mm'],
         'arc/chord (promontory to tip)': out['anterior_arc_mm'] / out['anterior_chord_mm'],
         'pelvic face width/height': out['outline_pelvic']['width_mm'] / out['outline_pelvic']['height_mm']}
    SIG = {}; UNT = {}
    if out.get('segments_valid'):
        Lc, La = out['segments_chord_mm'], out['segments_arc_mm']
        b4 = -out['foramen_pair'][3]['level_c']
        R['breadth/(base to 4th foramen pair)'] = W / b4; SIG['breadth/(base to 4th foramen pair)'] = W / b4 * SL / b4
        for k in range(3):
            for nm, Ls in (('chord', Lc), ('arc', La)):
                key = f'S{k+1}/S{k+2} ({nm})'; r_ = Ls[k] / Ls[k + 1]; R[key] = r_
                SIG[key] = r_ * math.hypot(math.sqrt(2) * SL / Ls[k], math.sqrt(2) * SL / Ls[k + 1])
        UNT['S4/(S5 + distal tip) (chord)'] = Lc[3] / Lc[4]
        tsp = [p['transverse_spacing_mm'] for p in out['foramen_pair']]
        for k in range(3):
            key = f'foramen spacing {k+1}/{k+2}'; r_ = tsp[k] / tsp[k + 1]; R[key] = r_
            SIG[key] = r_ * math.hypot(math.sqrt(2) * SL / tsp[k], math.sqrt(2) * SL / tsp[k + 1])
    out['ratios_sigma'] = SIG; out['ratios_untested'] = UNT
    out['ratios_raw'] = R
    out['ratios_folded'] = {k: fold(v) for k, v in R.items()}
    out['_draw'] = {'X': X, 'C': C, 'F': F, 'D': D, 'g': g, 'polys': polys, 'prof': prof, 'spi': spi, 'cP': cP,
                    'ctop': ctop_ep, 'B': B, 'P': P, 'ex': ex, 'ec': ec, 'ef': ef, 'aur': aur, 'Pr': Pr}
    return out


# ---------------------------------------------------------------- figures
def mark(fig, credit=None):
    fig.text(0.995, 0.005, MARK, ha='right', va='bottom', fontsize=8, color='#a07c1c')
    if credit: fig.text(0.005, 0.005, credit, ha='left', va='bottom', fontsize=6.5, color='#555')


def draw_front(ax, r, title):
    d = r['_draw']; D = d['D']; g = d['g']
    ext = [g[0], g[0] + D.shape[1] * RES, g[1], g[1] + D.shape[0] * RES]
    ax.imshow(D, origin='lower', extent=ext, cmap='bone', interpolation='nearest')
    for nm, col in (('outline_full', '#555'), ('outline_pelvic', '#1e88e5')):
        xy = np.array(d['polys'][nm].exterior.coords); ax.plot(xy[:, 0], xy[:, 1], color=col, lw=1)
    T = np.array(r['outline_full']['fits']['triangle']['vertices']); T = np.vstack([T, T[:1]])
    ax.plot(T[:, 0], T[:, 1], color='#d62728', lw=1.2, ls='--', label=f"triangle IoU {r['outline_full']['fits']['triangle']['iou']:.3f}")
    for sd, col in (('left', '#2ca02c'), ('right', '#2ca02c')):
        for b in r['foramina'][sd]: ax.plot(b['x'], b['c'], 'o', mfc='none', mec='#ffcc00', ms=7, mew=1.5)
    if 'foramen_pair' in r:
        for p in r['foramen_pair']: ax.axhline(p['level_c'], color='#ffcc00', lw=0.6, ls=':')
    ax.axhline(0, color='#9467bd', lw=0.8); ax.axhline(d['cP'], color='#9467bd', lw=0.8)
    ax.axvline(0, color='#9467bd', lw=0.5, ls=':')
    ax.set_title(title, fontsize=9); ax.set_xlabel("mm, to the subject's left →"); ax.set_ylabel('mm along the base–apex chord')
    ax.legend(fontsize=7, loc='lower right'); ax.set_aspect('equal')


def draw_profile(ax, r, title):
    d = r['_draw']; X, C, F = d['X'], d['C'], d['F']
    s = np.abs(X) < 3; ax.plot(F[s], C[s], ',', color='#999')
    pr = d['prof']; ax.plot(pr[:, 1], pr[:, 0], '.', color='#1e88e5', ms=3, label='anterior midline')
    c = r['curvature']['circle']; t = np.linspace(0, 2 * math.pi, 400)
    cx, cy = c['centre']
    ax.plot(cy + c['R'] * np.sin(t), cx + c['R'] * np.cos(t), color='#d62728', lw=0.8,
            label=f"circle R {c['R']:.1f} mm, rms {c['rms']:.2f}")
    p = d['spi']['_p']; th0 = np.unwrap(np.arctan2(pr[:, 1] - p[1], pr[:, 0] - p[0])); m0 = th0.mean()
    th = np.linspace(th0.min() - 0.3, th0.max() + 0.3, 200); rr = np.exp(p[2] + p[3] * (th - m0))
    ax.plot(p[1] + rr * np.sin(th), p[0] + rr * np.cos(th), color='#2ca02c', lw=0.8, ls='--',
            label=f"log spiral |b| {abs(p[3]):.3f}, rms {d['spi']['rms']:.2f}")
    ax.set_xlim(F[s].min() - 15, F[s].max() + 40); ax.set_ylim(d['cP'] - 10, d['ctop'] + 15)
    ax.set_aspect('equal'); ax.set_title(title, fontsize=9); ax.set_xlabel('mm, front →'); ax.set_ylabel('mm along chord')
    ax.legend(fontsize=7, loc='lower left')


def draw_axial(ax, r, sac_pts, title):
    d = r['_draw']; B, ex, ef, ec = d['B'], d['ex'], d['ef'], d['ec']
    X, F = (sac_pts - B) @ ex, (sac_pts - B) @ ef
    ax.plot(X, F, ',', color='#bbb')
    for sd, col in (('left', '#d62728'), ('right', '#1e88e5')):
        a = d['aur'][sd]; c = a['centroid'] - B; n = a['normal']
        cx, cf = c @ ex, c @ ef; nx_, nf_ = n @ ex, n @ ef; L = 35
        ax.plot([cx - nf_ * L, cx + nf_ * L], [cf + nx_ * L, cf - nx_ * L], color=col, lw=2,
                label=f"{sd} auricular plane (area {a['area_mm2']:.0f} mm²)")
    ax.set_aspect('equal'); ax.set_title(title, fontsize=9); ax.set_xlabel("mm, to the subject's left →"); ax.set_ylabel('mm, front →')
    ax.legend(fontsize=7, loc='lower center')


# ---------------------------------------------------------------- controls
def control_cone_sphere():
    cone = trimesh.creation.cone(radius=50.0, height=100.0, sections=512)
    P, N = sample(cone, 12.0)
    D, _, g = raster_front(P[:, 0], -P[:, 2], P[:, 1])  # view along y; apex down (z flipped)
    S = largest(ndimage.binary_fill_holes(ndimage.binary_closing(~np.isnan(D), disk(2))))
    poly = mask_polygon(S, g); fits = fit_shapes(poly)
    T = fits['triangle']; ap = T['angles_deg'][2]
    xmn, ymn, xmx, ymx = poly.bounds
    check('control cone: triangle IoU > 0.99', T['iou'] > 0.99, f"{T['iou']:.4f}")
    check('control cone: apex angle 53.13 +- 0.6 deg', abs(ap - 53.130) < 0.6, f'{ap:.3f}')
    check('control cone: width/height 1 +- 0.01', abs((xmx - xmn) / (ymx - ymn) - 1) < 0.01, f'{(xmx - xmn) / (ymx - ymn):.4f}')
    sph = trimesh.creation.icosphere(subdivisions=6, radius=50.0)
    P, _ = sample(sph, 12.0); s = np.abs(P[:, 0]) < 1.0
    prof = []
    for a in np.arange(-40, 40, 1.0):
        q = s & (P[:, 2] >= a) & (P[:, 2] < a + 1)
        if q.any(): prof.append((P[q, 2][np.argmax(P[q, 1])], P[q, 1].max()))
    prof = np.array(prof); c = fit_circle(prof[:, 0], prof[:, 1]); sp = fit_logspiral(prof[:, 0], prof[:, 1], c)
    check('control sphere: circle R 50 +- 0.3 mm', abs(c['R'] - 50) < 0.3, f"{c['R']:.3f} rms {c['rms']:.3f}")
    check('control sphere: log-spiral |b| < 0.03 (a circle)', abs(sp['b']) < 0.03, f"{sp['b']:.4f}")
    # golden spiral arc: the spiral fit must recover b = ln(phi)/(pi/2)
    bg = math.log(PHI) / (math.pi / 2); th = np.linspace(0, 1.2, 120); rr = 60 * np.exp(bg * th)
    x, y = rr * np.cos(th), rr * np.sin(th); cc = fit_circle(x, y); sg = fit_logspiral(x, y, cc)
    check('control golden spiral arc (69 deg): b recovered within 0.01', abs(abs(sg['b']) - bg) < 0.01, f"{sg['b']:.4f} vs {bg:.4f}")
    return {'cone_triangle': T, 'sphere_circle': c, 'sphere_spiral_b': sp['b'], 'golden_arc_b': sg['b'], 'golden_b': bg}


def phantom():
    """Curved plate (anterior surface radius 110 mm, thickness 18) with four pairs of radial holes, an 'L5' block and two
    'hip' slabs; built as a voxel mask at 0.5 mm in RAS world and meshed by the same marching-cubes path as the masks."""
    R, T, Hs, Wt, Wb = 110.0, 18.0, 110.0, 110.0, 24.0
    pt, pb = Hs / (2 * R), -Hs / (2 * R)
    holes_s = [30.0, 52.0, 70.0, 84.0]; holes_x = [26.0, 23.0, 20.0, 17.0]; holes_r = [4.5, 4.0, 3.5, 3.0]
    h = 0.5; xs = np.arange(-75, 75, h); ys = np.arange(-140, -60, h); zs = np.arange(-70, 105, h)
    Xg, Yg, Zg = np.meshgrid(xs, ys, zs, indexing='ij')
    rho = np.hypot(Yg, Zg); psi = np.arctan2(Zg, -Yg)
    hw = Wt / 2 - (Wt - Wb) / 2 * (pt - psi) / (pt - pb)
    shell = (rho >= R) & (rho <= R + T)
    plate = shell & (psi <= pt) & (psi >= pb) & (np.abs(Xg) <= hw)
    hole_pts = []
    for s_, x_, r_ in zip(holes_s, holes_x, holes_r):
        ps = pt - s_ / R; u = np.array([0, -math.cos(ps), math.sin(ps)])
        for sg in (1, -1):
            # distance from the radial line through (sg*x_, origin->u)
            px, py, pz = Xg - sg * x_, Yg, Zg
            along = py * u[1] + pz * u[2]
            dist = np.sqrt(px ** 2 + (py - along * u[1]) ** 2 + (pz - along * u[2]) ** 2)
            plate &= ~(dist < r_)
            hole_pts.append(np.array([sg * x_, -R * math.cos(ps), R * math.sin(ps)]))
    gap = 10.0 / (R + T / 2)
    l5 = shell & (psi >= pt + gap) & (psi <= pt + gap + 30.0 / R) & (np.abs(Xg) <= 22)
    top45 = (psi <= pt) & (psi >= pt - 0.45 * (pt - pb))
    lat = np.abs(Xg) - hw
    hipR = shell & top45 & (lat >= 2) & (lat <= 10) & (Xg > 0)
    hipL = shell & top45 & (lat >= 2) & (lat <= 10) & (Xg < 0)
    A = np.array([[h, 0, 0, xs[0]], [0, h, 0, ys[0]], [0, 0, h, zs[0]]])
    meshes = [mask_to_mesh(m, A, sigma=0.8) for m in (plate, l5, hipL, hipR)]
    # analytic expectations: side-surface plane over the hip region, foramen points, anterior radius
    pp = np.linspace(pt - 0.45 * (pt - pb), pt, 60); rr = np.linspace(R, R + T, 10); P2, R2 = np.meshgrid(pp, rr)
    hw2 = Wt / 2 - (Wt - Wb) / 2 * (pt - P2) / (pt - pb)
    sideL = np.c_[-hw2.ravel(), (-R2 * np.cos(P2)).ravel(), (R2 * np.sin(P2)).ravel()]
    sideR = sideL * np.array([-1, 1, 1])
    return meshes, {'R': R, 'holes': hole_pts, 'sideL': sideL, 'sideR': sideR, 'holes_s': holes_s}


def control_phantom(figdir):
    (sac, L5, hipL, hipR), ex = phantom()
    r = measure_sacrum(sac, L5, hipL, hipR, 'phantom')
    d = r['_draw']; B, e_x, e_c, e_f = d['B'], d['ex'], d['ec'], d['ef']
    check('control phantom: left axis = -x (RAS)', e_x @ np.array([-1, 0, 0]) > 0.99, f'{e_x.round(3).tolist()}')
    check('control phantom: anterior axis ~ +y', np.array(r['frame_world']['anterior']) @ np.array([0, 1, 0]) > 0.9)
    pr = d['prof']; c0, f0 = (-B) @ e_c, (-B) @ e_f
    dist = np.hypot(pr[:, 0] - c0, pr[:, 1] - f0) - 110
    print('DIAG phantom profile: n', len(pr), 'c range', pr[:, 0].min().round(1), pr[:, 0].max().round(1),
          'distance to the true centre minus 110: mean', dist.mean().round(2), 'min', dist.min().round(2), 'max', dist.max().round(2))
    print('DIAG profile sample', np.round(pr[::8], 1).tolist())
    print('DIAG true centre in chord frame', round(float(c0), 2), round(float(f0), 2), 'fit', r['curvature']['circle'])
    check('control phantom: anterior radius 110 +- 1.5 mm', abs(r['curvature']['circle']['R'] - 110) < 1.5,
          f"{r['curvature']['circle']['R']:.2f} rms {r['curvature']['circle']['rms']:.2f}")
    check('control phantom: 4 foramen pairs found', r['foramina_pairs_found'] == 4, f"{r['foramina_pairs_found']} (blobs {r['foramina_blobs_all']})")
    errs = []
    if r['foramina_pairs_found'] == 4:
        exp = ex['holes']  # order: pair k -> (left? sg=1 is +x = RIGHT in RAS), sg=-1 left
        for k in range(4):
            pR, pL = exp[2 * k], exp[2 * k + 1]
            for sd, pe in (('left', pL), ('right', pR)):
                b = r['foramina'][sd][k]; xe, ce = (pe - B) @ e_x, (pe - B) @ e_c
                errs.append(math.hypot(b['x'] - xe, b['c'] - ce))
        check('control phantom: foramen centres within 1.5 mm', max(errs) < 1.5, f'max {max(errs):.2f} mm')
        lv_e = [((exp[2 * k] - B) @ e_c + (exp[2 * k + 1] - B) @ e_c) / 2 for k in range(4)]
        lv_m = [p['level_c'] for p in r['foramen_pair']]
        b_e = [0.0] + lv_e + [r['apex_c']]; b_m = [0.0] + lv_m + [r['apex_c']]
        se = [b_e[k] - b_e[k + 1] for k in range(5)]; sm = [b_m[k] - b_m[k + 1] for k in range(4)]
        z = max(abs(sm[k] / sm[k + 1] - se[k] / se[k + 1]) / ((se[k] / se[k + 1]) * math.hypot(math.sqrt(2) / se[k], math.sqrt(2) / se[k + 1])) for k in range(3))
        check('control phantom: segment ratio errors within the propagated 1 mm level uncertainty (z < 1)', z < 1, f'max z {z:.2f}')
    else:
        check('control phantom: foramen centres within 1.5 mm', False, 'pairs missing')
    # expected wedge: planes fitted to the analytic side surfaces
    def pl(P, sg):
        c = P.mean(0); _, _, Vt = np.linalg.svd(P - c, full_matrices=False); n = Vt[2]; return n * np.sign(sg * (n @ e_x))
    nL, nR = pl(ex['sideL'], 1), pl(ex['sideR'], -1)
    fr_e = math.degrees(math.atan2(nL @ e_c, nL @ e_x)) + math.degrees(math.atan2(nR @ e_c, -(nR @ e_x)))
    ax_e = math.degrees(math.atan2(nL @ e_f, nL @ e_x)) + math.degrees(math.atan2(nR @ e_f, -(nR @ e_x)))
    w = r['wedge']
    check('control phantom: frontal auricular wedge within 2 deg', abs(w['auricular_frontal_deg_pos_narrower_below'] - fr_e) < 2,
          f"{w['auricular_frontal_deg_pos_narrower_below']:.2f} vs {fr_e:.2f}")
    check('control phantom: axial auricular wedge within 2 deg', abs(w['auricular_axial_deg_pos_narrower_in_front'] - ax_e) < 2,
          f"{w['auricular_axial_deg_pos_narrower_in_front']:.2f} vs {ax_e:.2f}")
    fig, axs = plt.subplots(1, 2, figsize=(10, 5.6))
    draw_front(axs[0], r, 'Control phantom, front view (4 known hole pairs)'); draw_profile(axs[1], r, 'Control phantom, midline profile (R = 110 mm)')
    mark(fig); fig.tight_layout(rect=(0, 0.02, 1, 1)); fig.savefig(os.path.join(figdir, 'fig6-control-phantom.png'), dpi=150); plt.close(fig)
    return strip(r)


def control_chance():
    rng = np.random.default_rng(3); u = np.exp(rng.uniform(0, math.log(RMAX), 400000))
    for tol in TOLS:
        mc = np.mean([bool(near(x, tol)) for x in u[:40000]]); ex = chance_fraction(tol)
        check(f'control chance model tol {tol}: Monte Carlo = exact union', abs(mc - ex) < 0.01, f'MC {mc:.4f} exact {ex:.4f}')


def strip(r):
    return {k: v for k, v in r.items() if not k.startswith('_')}


# ---------------------------------------------------------------- population
def load_ts_subject(d):
    need = ['sacrum', 'vertebrae_L5', 'hip_left', 'hip_right']
    if not all(os.path.exists(os.path.join(d, n + '.nii.gz')) for n in need): return None, 'missing file'
    arr, A = read_nii(os.path.join(d, 'sacrum.nii.gz'))
    m = arr > 0
    vox = abs(np.linalg.det(A[:, :3]))
    if m.sum() * vox < 40000: return None, f'sacrum mask too small ({m.sum() * vox / 1000:.0f} cm3)'
    if m[0].any() or m[-1].any() or m[:, 0].any() or m[:, -1].any() or m[:, :, 0].any() or m[:, :, -1].any():
        return None, 'sacrum touches the scan edge (incomplete)'
    meshes = {'sacrum': mask_to_mesh(m, A)}
    for n in need[1:] + ['vertebrae_L4']:
        p = os.path.join(d, n + '.nii.gz')
        if not os.path.exists(p): meshes[n] = None; continue
        a2, A2 = read_nii(p); mm = a2 > 0
        if mm.sum() * vox < 8000: meshes[n] = None; continue
        meshes[n] = mask_to_mesh(mm, A2)
    if meshes['vertebrae_L5'] is None or meshes['hip_left'] is None or meshes['hip_right'] is None:
        return None, 'L5 or a hip bone missing/too small'
    meshes['_A'] = A; meshes['_vox_mm'] = [float(np.linalg.norm(A[:, i])) for i in range(3)]
    return meshes, 'ok'


def summarise(vals):
    v = np.array([x for x in vals if x is not None and np.isfinite(x)])
    if len(v) == 0: return None
    return {'n': int(len(v)), 'mean': float(v.mean()), 'sd': float(v.std(ddof=1)) if len(v) > 1 else None,
            'sem': float(v.std(ddof=1) / math.sqrt(len(v))) if len(v) > 1 else None,
            'min': float(v.min()), 'max': float(v.max()), 'median': float(np.median(v))}


NWORK = 6


def subject_job(job):
    i, s, d, mt = job
    try:
        ms, why = load_ts_subject(d)
        if ms is None: return i, s, None, why
        rr = measure_sacrum(ms['sacrum'], ms['vertebrae_L5'], ms['hip_left'], ms['hip_right'], s)
        fw = rr['frame_world']
        rr['frame_check_ras'] = {'left·(-x)': -fw['left'][0], 'anterior·(+y)': fw['anterior'][1], 'superior·(+z)': fw['superior'][2]}
        rr['voxel_mm'] = ms['_vox_mm']
        rr['battery'] = {'sacrum': battery(sample(ms['sacrum'], 6.0)[0]), 'L5': battery(sample(ms['vertebrae_L5'], 6.0)[0])}
        if ms.get('vertebrae_L4') is not None: rr['battery']['L4'] = battery(sample(ms['vertebrae_L4'], 6.0)[0])
        rr['meta'] = {k: mt.get(k) for k in ('age', 'gender', 'institute', 'study_type', 'pathology')}
        if i >= 16: rr = strip(rr)
        else: rr['_draw'] = {k: v for k, v in rr['_draw'].items() if k in ('D', 'g', 'polys', 'cP')}
        return i, s, rr, 'ok'
    except Exception as e:
        return i, s, None, f'error {type(e).__name__}: {e}'


def main():
    mode, dl, outdir = sys.argv[1], sys.argv[2], sys.argv[3]
    maxsubj = int(sys.argv[4]) if len(sys.argv) > 4 else 10 ** 6
    datadir, figdir = os.path.join(outdir, 'data'), os.path.join(outdir, 'figures')
    os.makedirs(datadir, exist_ok=True); os.makedirs(figdir, exist_ok=True)
    t0 = time.time(); RESULT = {'mode': mode, 'constants': CONSTS, 'tolerances': TOLS, 'rmax': RMAX}
    if mode == 'phantom':
        control_phantom(figdir); print('FINAL ok' if all(ok for _, ok, _ in CHECKS) else 'FINAL FAIL phantom'); return
    print('PROGRESS 0.00 controls')
    RESULT['controls'] = {'cone_sphere': control_cone_sphere()}
    control_chance()
    RESULT['controls']['phantom'] = control_phantom(figdir)
    RESULT['chance_fraction'] = {str(t): chance_fraction(t) for t in TOLS}
    RESULT['chance_fraction_phi_only'] = {str(t): chance_fraction(t, names=['φ']) for t in TOLS}
    print(f'PROGRESS 0.10 controls done {time.time() - t0:.0f}s')
    # ---- BodyParts3D
    ob = os.path.join(dl, 'obj')
    sac, L5, L4, hipR, hipL, scap = (load_obj(os.path.join(ob, f)) for f in
                                      ('FJ3393.obj', 'FJ3168.obj', 'FJ3165.obj', 'FJ3152.obj', 'FJ3288.obj', 'FJ3384.obj'))
    r = measure_sacrum(sac, L5, hipL, hipR, 'BodyParts3D FJ3393')
    sp, _ = sample(sac, 6.0)
    fig, axs = plt.subplots(1, 3, figsize=(16, 6))
    draw_front(axs[0], r, 'BodyParts3D sacrum: front (pelvic) view, depth-shaded')
    draw_profile(axs[1], r, 'Anterior midline: circle and log-spiral fits')
    cA = np.mean([(r['_draw']['aur'][s_]['centroid'] - r['_draw']['B']) @ r['_draw']['ec'] for s_ in ('left', 'right')])
    draw_axial(axs[2], r, sp[np.abs((sp - r['_draw']['B']) @ r['_draw']['ec'] - cA) < 6], f'Slice at the auricular level (c = {cA:.0f} ± 6 mm): fitted planes')
    mark(fig, BP3D_CREDIT); fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(os.path.join(figdir, 'fig1-bp3d-sacrum.png'), dpi=150); plt.close(fig)
    RESULT['bp3d'] = {'sacrum': strip(r), 'mesh_faces': int(len(sac.faces)), 'watertight': bool(sac.is_watertight)}
    check('BodyParts3D sacrum: 4 foramen pairs found', r['foramina_pairs_found'] == 4, f"{r['foramina_pairs_found']}")
    check('BodyParts3D sacrum: end plate area 800-2500 mm2', 800 < r['endplate']['area_mm2'] < 2500, f"{r['endplate']['area_mm2']:.0f}")
    bat = {}
    for nm, m in (('sacrum', sac), ('L5', L5), ('L4', L4), ('hip bone (left)', hipL), ('scapula (right)', scap)):
        bat[nm] = battery(sample(m, 8.0)[0])
    RESULT['bp3d']['battery'] = bat
    print(f'PROGRESS 0.20 BodyParts3D done {time.time() - t0:.0f}s')
    # ---- population
    tsd = os.path.join(dl, 'ts'); subs = sorted(s for s in os.listdir(tsd) if os.path.isdir(os.path.join(tsd, s)))[:maxsubj] if os.path.isdir(tsd) else []
    meta = {}
    mp = os.path.join(tsd, 'meta.csv')
    if os.path.exists(mp):
        with open(mp, newline='', encoding='utf-8-sig') as fh:
            head = fh.readline(); fh.seek(0)
            rd = csv.DictReader(fh, delimiter=';' if ';' in head else ',')
            for row in rd: meta[row.get('image_id')] = row
    pop, skipped, sheets = [], {}, []
    import multiprocessing as mpr
    jobs = [(i, s_, os.path.join(tsd, s_), meta.get(s_, {})) for i, s_ in enumerate(subs)]
    with mpr.get_context('fork').Pool(NWORK) as pool:
        for k, (i, s_, res, why) in enumerate(pool.imap_unordered(subject_job, jobs)):
            if res is None: skipped[s_] = why
            else:
                if '_draw' in res: sheets.append((i, res))
                pop.append(strip(res))
            print(f'PROGRESS {0.2 + 0.75 * (k + 1) / max(1, len(subs)):.3f} subject {s_} ({len(pop)} used)')
    pop.sort(key=lambda p: p['tag']); sheets = [r_ for _, r_ in sorted(sheets, key=lambda t: t[0])][:12]
    if sheets:
        n = len(sheets); cols = 4; rows = math.ceil(n / cols)
        fig, axs = plt.subplots(rows, cols, figsize=(4 * cols, 4.4 * rows), squeeze=False)
        for a in axs.ravel(): a.axis('off')
        for a, rr in zip(axs.ravel(), sheets):
            a.axis('on'); draw_front(a, rr, f"{rr['tag']} ({rr['meta'].get('gender')}, {rr['meta'].get('age')})"); a.legend().remove()
        mark(fig, TS_CREDIT); fig.tight_layout(rect=(0, 0.02, 1, 1)); fig.savefig(os.path.join(figdir, 'fig4-population-front-sheet.png'), dpi=110); plt.close(fig)
    RESULT['population'] = {'subjects_tried': len(subs), 'used': len(pop), 'skipped': skipped}
    # ---- summaries
    keys = sorted({k for p in pop for k in p['ratios_raw']})
    RESULT['population']['ratios'] = {k: summarise([p['ratios_raw'].get(k) for p in pop]) for k in keys}
    scal = {'breadth_mm': lambda p: p['breadth_mm'], 'chord_mm': lambda p: p['chord_mm'], 'promontory_apex_mm': lambda p: p['promontory_apex_mm'],
            'anterior_arc_mm': lambda p: p['anterior_arc_mm'], 'circle_R_mm': lambda p: p['curvature']['circle']['R'],
            'circle_rms_mm': lambda p: p['curvature']['circle']['rms'], 'spiral_rms_mm': lambda p: p['curvature']['logspiral']['rms'],
            'spiral_abs_b': lambda p: abs(p['curvature']['logspiral']['b']), 'arc_angle_deg': lambda p: p['curvature']['arc_angle_deg'],
            'bic_spiral_minus_circle': lambda p: p['curvature']['bic_spiral'] - p['curvature']['bic_circle'],
            'base_angle_deg': lambda p: p['base_angle_deg'], 'triangle_iou_full': lambda p: p['outline_full']['fits']['triangle']['iou'],
            'curved_triangle_iou_full': lambda p: p['outline_full']['fits']['curved_triangle']['iou'],
            'wedge_iou_full': lambda p: p['outline_full']['fits']['wedge_quadrilateral']['iou'],
            'triangle_iou_pelvic': lambda p: p['outline_pelvic']['fits']['triangle']['iou'],
            'curved_triangle_iou_pelvic': lambda p: p['outline_pelvic']['fits']['curved_triangle']['iou'],
            'triangle_apex_angle_deg': lambda p: p['outline_full']['fits']['triangle']['angles_deg'][2],
            'auricular_total_deg': lambda p: p['wedge']['auricular_total_deg'],
            'auricular_frontal_deg': lambda p: p['wedge']['auricular_frontal_deg_pos_narrower_below'],
            'auricular_axial_deg': lambda p: p['wedge']['auricular_axial_deg_pos_narrower_in_front'],
            'foramen_pairs_found': lambda p: p['foramina_pairs_found'],
            'circle_R_to_pair4_mm': lambda p: p.get('curvature_base_to_pair4', {}).get('circle', {}).get('R', float('nan')),
            'spiral_abs_b_to_pair4': lambda p: abs(p.get('curvature_base_to_pair4', {}).get('logspiral', {}).get('b', float('nan'))),
            'arc_over_chord_tip': lambda p: p['anterior_arc_mm'] / p['anterior_chord_mm'],
            'segments_valid': lambda p: float(bool(p.get('segments_valid')))}
    RESULT['population']['scalars'] = {k: summarise([f(p) for p in pop]) for k, f in scal.items()}
    # near-constant hit rates: specific sacral ratios, generic battery per bone
    hr = {}
    for tol in TOLS:
        t = str(tol); hr[t] = {}
        def rate(lst):
            lst = [x for x in lst if x is not None and 1 <= x <= RMAX]
            return {'n': len(lst), 'near_any': float(np.mean([bool(near(x, tol)) for x in lst])) if lst else None,
                    'near_phi': float(np.mean([abs(x / PHI - 1) <= tol for x in lst])) if lst else None}
        hr[t]['bp3d_sacrum_specific'] = rate(list(r['ratios_folded'].values()))
        for nm in bat: hr[t][f'bp3d_battery_{nm}'] = rate(list(bat[nm].values()))
        hr[t]['pop_sacrum_specific'] = rate([v for p in pop for v in p['ratios_folded'].values()])
        for nm in ('sacrum', 'L5', 'L4'):
            hr[t][f'pop_battery_{nm}'] = rate([v for p in pop for v in p.get('battery', {}).get(nm, {}).values()])
        hr[t]['chance_loguniform'] = {'near_any': chance_fraction(tol), 'near_phi': chance_fraction(tol, names=['φ'])}
    RESULT['near_constant_rates'] = hr
    # per-ratio: is phi (or any constant) inside the population 95% interval of the MEAN, and of INDIVIDUALS?
    tests = {}
    for k, s in RESULT['population']['ratios'].items():
        if not s or not s.get('sd'): continue
        m, sd, se = s['mean'], s['sd'], s['sem']; mf = fold(m)
        tests[k] = {'mean': m, 'sd': sd, 'sem': se, 'cv_percent': 100 * sd / abs(m),
                    'constants_within_mean_CI95': [c for c, v in CONSTS.items() if any(abs(w - m) <= 1.96 * se for w in (v, 1 / v))],
                    'constants_within_2pct_of_mean': near(mf, 0.02),
                    'share_of_individuals_within_2pct_of_phi': float(np.mean([abs(fold(p['ratios_raw'][k]) / PHI - 1) <= 0.02 for p in pop if k in p['ratios_raw']]))}
    RESULT['population']['ratio_tests'] = tests
    # ---- population figure
    if pop:
        show = [k for k in ('breadth/promontory-tip (sacral index/100)', 'breadth/(base to 4th foramen pair)', 'pelvic face width/height',
                            'S1/S2 (chord)', 'S2/S3 (chord)', 'foramen spacing 1/2') if k in keys]
        fig, axs = plt.subplots(2, 3, figsize=(14, 7.5), squeeze=False)
        for a, k in zip(axs.ravel(), show):
            v = [fold(p['ratios_raw'][k]) for p in pop if k in p['ratios_raw']]
            a.hist(v, bins=20, color='#9e9e9e', edgecolor='white')
            bv = fold(r['ratios_raw'][k]) if k in r['ratios_raw'] else None
            if bv: a.axvline(bv, color='#1e88e5', lw=2, label=f'BodyParts3D {bv:.3f}')
            for cn, cv in CONSTS.items():
                if min(v) * 0.9 <= cv <= max(v) * 1.1: a.axvline(cv, color='#d4a017' if cn == 'φ' else '#c62828', lw=1, ls='--'); a.text(cv, a.get_ylim()[1] * 0.95, cn, fontsize=8, ha='center')
            a.set_title(f'{k} (folded ≥ 1), n = {len(v)}', fontsize=9); a.legend(fontsize=7)
        mark(fig, TS_CREDIT + '; ' + BP3D_CREDIT); fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(os.path.join(figdir, 'fig2-population-ratios.png'), dpi=140); plt.close(fig)
        fig, ax = plt.subplots(figsize=(9, 4.6)); t = '0.02'
        labs = [k for k in hr[t] if hr[t][k].get('near_any') is not None]
        vals = [hr[t][k]['near_any'] for k in labs]; phs = [hr[t][k]['near_phi'] for k in labs]
        yy = np.arange(len(labs)); ax.barh(yy, vals, color='#90a4ae', label='near any of 12 constants (±2 %)')
        ax.barh(yy, phs, color='#d4a017', label='near φ (±2 %)'); ax.set_yticks(yy); ax.set_yticklabels(labs, fontsize=8)
        ax.set_xlabel('share of ratios'); ax.legend(fontsize=8); ax.set_title('How often a ratio lands "near" a notable constant: sacrum vs other bones vs chance', fontsize=9)
        mark(fig); fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(os.path.join(figdir, 'fig3-near-constant-test.png'), dpi=140); plt.close(fig)
    # ---- outputs
    def js(o):
        if isinstance(o, dict): return {str(k): js(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)): return [js(v) for v in o]
        if isinstance(o, (np.floating,)): return float(o)
        if isinstance(o, (np.integer,)): return int(o)
        if isinstance(o, np.ndarray): return o.tolist()
        return o
    RESULT['checks'] = [{'name': n, 'ok': ok, 'detail': d} for n, ok, d in CHECKS]
    tagname = 'pilot' if mode == 'pilot' else 'full'
    json.dump(js(RESULT), open(os.path.join(datadir, f'results-{tagname}.json'), 'w'), indent=1, ensure_ascii=False)
    json.dump(js(pop), open(os.path.join(datadir, f'population-{tagname}.json'), 'w'), indent=0, ensure_ascii=False)
    with open(os.path.join(datadir, f'population-{tagname}.csv'), 'w', newline='') as fh:
        fh.write(f'# {MARK} · sacrum study 2026-11-12 · {TS_CREDIT}\n')
        wr = csv.writer(fh); cols = ['subject', 'gender', 'age', 'pairs'] + list(scal) + keys
        wr.writerow(cols)
        for p in pop:
            wr.writerow([p['tag'], p['meta'].get('gender'), p['meta'].get('age'), p['foramina_pairs_found']] +
                        [f'{f(p):.4f}' for f in scal.values()] + [f"{p['ratios_raw'][k]:.4f}" if k in p['ratios_raw'] else '' for k in keys])
    nfail = sum(1 for _, ok, _ in CHECKS if not ok)
    need_pop = 1 if mode == 'pilot' else 20
    print(f'population used {len(pop)} of {len(subs)}; checks {len(CHECKS) - nfail}/{len(CHECKS)} ok; {time.time() - t0:.0f}s')
    print('PROGRESS 1.00 done')
    ok_all = nfail == 0 and len(pop) >= min(need_pop, len(subs)) and len(subs) > 0
    print('FINAL ok' if ok_all else f'FINAL FAIL {nfail} failed checks, population {len(pop)}/{len(subs)}')
    sys.exit(0 if ok_all else 1)


if __name__ == '__main__':
    main()
