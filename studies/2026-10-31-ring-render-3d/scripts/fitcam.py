# Camera fit for the ring renders: finds the pose of the ring model in one of DICTO's photos from the outline alone.
# White plastic vs wood: low saturation + bright -> largest blob -> convex hull.  Model outline: convex hull of the projected
# ring-mesh vertices (pinhole, principal point at the image centre).  Coarse: 6000 random rotations, orthographic, scale and
# centroid matched, IoU of hulls; refine the best 12 with the pinhole model (rotation, translation, focal length) by
# Nelder-Mead on 1 - IoU.  Gravity: of the support directions of the bipyramid (6 faces, 9 edges, 5 vertices) the one whose
# image is closest to 'straight down' with the camera above the table (phone held upright) -- or forced with SUPPORT=.
# CAM_ELEV=<deg> instead sets the table square to gravity seen by an upright camera at that elevation.
# Writes a camera spec (JSON) for scene.py.  The photo is read only; nothing derived from it is written except numbers.
# Usage (dicto-big-brother): ~/geom/bin/python fitcam.py photo.jpg model.obj out.json [support-index]
import sys, json, math
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
from scipy.optimize import minimize
from scipy.spatial.transform import Rotation as Rot
from shapely.geometry import MultiPoint
sys.path.insert(0, __import__('os').path.dirname(__file__))
import ringmesh as RM

photo, objp, outp = sys.argv[1:4]
im = Image.open(photo).convert('RGB'); W0, H0 = im.size; k = 4
sm = np.asarray(im.resize((W0 // k, H0 // k), Image.LANCZOS)).astype(float) / 255
mx, mn = sm.max(2), sm.min(2); sat = (mx - mn) / (mx + 1e-6)
mask = (sat < 0.26) & (mx > 0.42)
mask = ndi.binary_opening(mask, iterations=1); mask = ndi.binary_closing(mask, iterations=3)
lab, nl = ndi.label(mask); big = np.argmax(ndi.sum(mask, lab, range(1, nl + 1))) + 1; mask = lab == big
ys, xs = np.nonzero(mask); PH = MultiPoint(np.c_[xs * k + k / 2, ys * k + k / 2]).convex_hull
print('photo hull area', PH.area, 'bounds', [round(b) for b in PH.bounds])

V = []
for line in open(objp):
    if line.startswith('o '): name = line[2:].strip()
    if line.startswith('v ') and name == 'Rings': V.append([float(x) for x in line.split()[1:4]])
V = np.array(V)[::7]; ctr = V.mean(0); V = V - ctr
cx, cy = W0 / 2, H0 / 2

def iou(A, B):
    i = A.intersection(B).area; return i / (A.area + B.area - i)

def ortho_score(Rm):
    q = (V @ Rm.T)[:, :2]; Hq = MultiPoint(q).convex_hull
    s = math.sqrt(PH.area / Hq.area); c = np.array(Hq.centroid.coords[0]); pc = np.array(PH.centroid.coords[0])
    Hq2 = MultiPoint((q - c) * s + pc).convex_hull
    return iou(Hq2, PH), s, pc - c * s

def proj(x):
    Rm = Rot.from_rotvec(x[:3]).as_matrix(); Xc = V @ Rm.T + x[3:6]; f = math.exp(x[6])
    if np.any(Xc[:, 2] <= 1e-3): return None
    return np.c_[f * Xc[:, 0] / Xc[:, 2] + cx, f * Xc[:, 1] / Xc[:, 2] + cy]

def loss(x):
    p = proj(x)
    if p is None: return 1.0
    return 1 - iou(MultiPoint(p).convex_hull, PH) + 0.01 * (x[6] - math.log(1515)) ** 2

import os
if os.environ.get('FROMX'):                      # reuse a previous fit (skips the search)
    x = np.array(json.load(open(os.environ['FROMX']))['x']); best = type('B', (), {'fun': loss(x)})()
else:
    rng = np.random.default_rng(1); cands = []
    for R0 in Rot.random(6000, random_state=2):
        sc_, s, off = ortho_score(R0.as_matrix()); cands.append((sc_, R0.as_rotvec(), s))
    cands.sort(key=lambda c: -c[0]); best = None
    for sc_, rv, s in cands[:12]:
        f = 1515.0; z = f / s; pc = np.array(PH.centroid.coords[0])
        x0 = np.r_[rv, (pc[0] - cx) * z / f, (pc[1] - cy) * z / f, z, math.log(f)]
        r = minimize(loss, x0, method='Nelder-Mead', options=dict(maxiter=3000, xatol=1e-5, fatol=1e-6))
        r = minimize(loss, r.x, method='Nelder-Mead', options=dict(maxiter=3000, xatol=1e-6, fatol=1e-7))
        print('start ortho IoU %.3f -> %.4f' % (sc_, 1 - r.fun))
        if best is None or r.fun < best.fun: best = r
    x = best.x
if len(sys.argv) > 5 and sys.argv[5] == 'turn60':
    # the other reading of a nearly symmetric outline: model turned 60 degrees about its apex axis, refined again
    x0 = x.copy(); x0[:3] = (Rot.from_rotvec(x[:3]) * Rot.from_euler('z', 60, degrees=True)).as_rotvec()
    best = minimize(loss, x0, method='Nelder-Mead', options=dict(maxiter=4000, xatol=1e-6, fatol=1e-7)); x = best.x
Rm = Rot.from_rotvec(x[:3]).as_matrix(); t = x[3:6]; f = math.exp(x[6])
print('best IoU %.4f  f %.0f px  distance %.3f m' % (1 - best.fun, f, t[2]))

# support directions of the bipyramid (object frame of ringmesh.bipyramid, centred like V)
rings, verts = RM.bipyramid(); faces = {}
for r in rings: faces.setdefault(r['face'], r['n'])
FN = [np.asarray(n) for n in faces.values()]
E = [];  ln = [f for f in FN]
for i in range(len(FN)):
    for j in range(i + 1, len(FN)):
        if math.degrees(math.acos(np.clip(FN[i] @ FN[j], -1, 1))) < 115: E.append(RM.unit(FN[i] + FN[j]))
VD = [RM.unit(v) for v in verts]
sup = [('face', n) for n in FN] + [('edge', n) for n in E] + [('vertex', n) for n in VD]
rows = []
for i, (kind, n) in enumerate(sup):
    g = Rm @ n; p0 = proj(x)[0]; a = np.array([f * t[0] / t[2] + cx, f * t[1] / t[2] + cy])
    b = t + 0.02 * g; b = np.array([f * b[0] / b[2] + cx, f * b[1] / b[2] + cy]); dimg = RM.unit(b - a)
    ang = math.degrees(math.acos(np.clip(dimg @ [0, 1], -1, 1))); above = (t @ g) > 0
    elev = math.degrees(math.asin(np.clip(-RM.unit(t) @ -g, -1, 1)))     # camera elevation above the table
    rows.append((i, kind, ang, above, elev)); print('%2d %-6s image angle to down %6.1f  camera above %s  elevation %5.1f' % (i, kind, ang, above, elev))
if len(sys.argv) > 4 and sys.argv[4] != 'auto': si = int(sys.argv[4])
else: si = min([r for r in rows if r[3]], key=lambda r: r[2])[0]
n_s = sup[si][1]; print('support', si, sup[si][0])
if os.environ.get('REST'):
    # physical fit: the model rests on one support (face / edge / vertex) of the bipyramid, the phone is held upright
    # (roll penalised); free: camera azimuth, elevation, small roll, position, focal length.  Best IoU over the supports
    # listed in REST (comma-separated indices, or 'all').
    B = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0.]])
    def Q0of(n):
        a = np.cross(n, [0, 0, -1.]); sa = np.linalg.norm(a); ca = n @ [0, 0, -1.]
        return np.eye(3) if sa < 1e-9 else Rot.from_rotvec(a / sa * math.atan2(sa, ca)).as_matrix()
    def Rmof(az, el, roll, Q0):
        return (Rot.from_euler('z', roll).as_matrix() @ Rot.from_euler('x', el).as_matrix() @ B
                @ Rot.from_euler('z', az).as_matrix() @ Q0)
    def loss_r(p, Q0):
        Rr = Rmof(p[0], p[1], p[2], Q0); xx = np.r_[Rot.from_matrix(Rr).as_rotvec(), p[3:7]]
        return loss(xx) + 0.5 * p[2] ** 2 + (0 if 0.17 < p[1] < 1.5 else 1)
    ids = range(len(sup)) if os.environ['REST'] == 'all' else map(int, os.environ['REST'].split(','))
    res = []
    for i in ids:
        Q0 = Q0of(sup[i][1]); coarse = []
        for az in np.radians(np.arange(0, 360, 8)):
            for el in np.radians(np.arange(15, 86, 7)):
                sc_, s, off = ortho_score(Rmof(az, el, 0, Q0)); coarse.append((sc_, az, el, s))
        coarse.sort(key=lambda c: -c[0]); bi = None
        for sc_, az, el, s in coarse[:4]:
            f0 = 1800.0; z = f0 / s; pc = np.array(PH.centroid.coords[0])
            p0 = np.r_[az, el, 0, (pc[0] - cx) * z / f0, (pc[1] - cy) * z / f0, z, math.log(f0)]
            r = minimize(loss_r, p0, args=(Q0,), method='Nelder-Mead', options=dict(maxiter=4000, xatol=1e-6, fatol=1e-7))
            if bi is None or r.fun < bi.fun: bi = r
        res.append((bi.fun, i, bi.x)); print('rest on %2d %-6s IoU %.4f  el %.1f roll %.1f' % (i, sup[i][0], 1 - loss(np.r_[Rot.from_matrix(Rmof(*bi.x[:3], Q0)).as_rotvec(), bi.x[3:7]]), math.degrees(bi.x[1]), math.degrees(bi.x[2])))
    fun, si, p = min(res, key=lambda r: r[0]); Q0 = Q0of(sup[si][1])
    Rm = Rmof(p[0], p[1], p[2], Q0); t = p[3:6]; f = math.exp(p[6]); n_s = sup[si][1]
    x = np.r_[Rot.from_matrix(Rm).as_rotvec(), p[3:7]]; best = type('B', (), {'fun': loss(x)})()
    print('REST support', si, sup[si][0], 'IoU %.4f f %.0f' % (1 - best.fun, f))
if os.environ.get('CAM_ELEV'):
    # table set from the photo instead: camera held upright (no roll) at this elevation; the model keeps its fitted pose
    # and is lowered onto the table at its lowest point
    e = math.radians(float(os.environ['CAM_ELEV'])); gobj = Rm.T @ np.array([0, math.cos(e), math.sin(e)])
    from scipy.spatial import ConvexHull                  # rest on the hull facet nearest to that gravity (no floating)
    eq = ConvexHull(V).equations; n_s = eq[np.argmax(eq[:, :3] @ gobj), :3]
    print('facet tilt from upright camera gravity %.1f deg' % math.degrees(math.acos(np.clip(n_s @ gobj, -1, 1))))
    print('table from camera elevation', os.environ['CAM_ELEV'])

# world frame: table z = 0, up = -n_s; camera on the -Y side
up = -n_s; Cobj = -Rm.T @ t
hz = RM.unit(Cobj - (Cobj @ up) * up); ey = -hz; ex = np.cross(ey, up)      # camera azimuth toward -Y
Q = np.array([ex, ey, up])                                                  # rows: world axes in object coords
Vall = (V) @ Q.T
z0 = -Vall[:, 2].min()
# full mesh lowest point (V is subsampled; use it, small error)
Mobj = np.eye(4); Mobj[:3, :3] = Q; Mobj[:3, 3] = Q @ (-ctr) + [0, 0, z0]
C = Q @ Cobj + [0, 0, z0]
xc, yc, zc = Q @ Rm.T[:, 0], Q @ Rm.T[:, 1], Q @ Rm.T[:, 2]
cam = np.eye(4); cam[:3, 0] = xc; cam[:3, 1] = -yc; cam[:3, 2] = -zc; cam[:3, 3] = C
json.dump(dict(M_obj=Mobj.tolist(), cam=cam.tolist(), lens_mm=f * 36 / W0, iou=1 - best.fun, f_px=f, support=si,
               x=list(map(float, x)), res=[W0 // 2, H0 // 2]), open(outp, 'w'), indent=1)
print('wrote', outp, 'lens %.1f mm' % (f * 36 / W0))
