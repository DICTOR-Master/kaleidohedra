# The Platonic Solids, series front cover, circle design (DICTO, 15 Nov 2026: "just the five solids plain in a circle in DICTO order,
# Dodecahedron at the top"; then the five at EQUAL VOLUME, see-through). The five Platonic solids, plain, evenly on a circle 72 degrees
# apart: Dodecahedron at the top, then clockwise Icosahedron, Cube, Tetrahedron, Octahedron, in their element colours (DICTO square,
# 10-22), all of the same volume. Drawn in DICTO's see-through standard (not real glass: no refraction, DICTO 15 Nov "why are the
# crystals and colours broken up weirdly"): every face an even tint of the solid's colour, laid back faces first, so the back faces and
# back edges show straight through, undistorted and fainter; front faces lit softly from the upper left; thin small glints only (nothing
# clips to white); crisp antialiased edges (supersampled), front edges in a light tint of the colour, back edges fainter. No haze.
# Run: python seethrough_circle.py OUT.png      env SS = supersampling (default 3). Output: the 2400 x 2200 picture block of the cover.
import os, sys, math, itertools
import numpy as np
from scipy.spatial import ConvexHull
from PIL import Image, ImageDraw
OUT = sys.argv[1]; SS = int(os.environ.get('SS', '3'))
W, H, GROUND = 2400, 2200, np.array((20, 15, 11), float)
PHI = (1 + 5 ** 0.5) / 2; R2, R5 = 2 ** 0.5, 5 ** 0.5
FAIL = []
def X(name, ok, detail=''):
    print(('X PASS ' if ok else 'X FAIL ') + name + (f': {detail}' if detail != '' else ''), flush=True)
    if not ok: FAIL.append(name)
cyc = lambda a, b, c: [(a, b, c), (c, a, b), (b, c, a)]
def signs(v): return sorted({tuple(x * t for x, t in zip(v, s)) for s in itertools.product((1, -1), repeat=3)})
CUBE8 = signs((1, 1, 1))
SOLIDS = {   # edge 1
    'D': [tuple(x * PHI / 2 for x in v) for v in CUBE8 + [w for c in cyc(0, 1 / PHI, PHI) for w in signs(c)]],
    'I': [tuple(x / 2 for x in w) for c in cyc(0, 1, PHI) for w in signs(c)],
    'C': [tuple(x / 2 for x in v) for v in CUBE8],
    'T': [tuple(x / (2 * R2) for x in v) for v in CUBE8 if v[0] * v[1] * v[2] > 0],
    'O': [tuple(x / R2 for x in w) for c in cyc(1, 0, 0) for w in signs(c)],
}
ORDER = 'DICTO'
NV, NF, NE = {'D': 20, 'I': 12, 'C': 8, 'T': 4, 'O': 6}, {'D': 12, 'I': 20, 'C': 6, 'T': 4, 'O': 8}, {'D': 30, 'I': 30, 'C': 12, 'T': 6, 'O': 12}
COL = {'D': (138, 92, 196), 'I': (58, 112, 205), 'C': (72, 142, 72), 'T': (205, 62, 40), 'O': (232, 200, 82)}   # element colours
VOL1 = {'D': (15 + 7 * R5) / 4, 'I': 5 * (3 + R5) / 12, 'C': 1.0, 'T': 1 / (6 * R2), 'O': R2 / 3}   # exact volumes at edge 1
VCOMMON = 36.0                                    # common volume in cover units^3 (1 unit = 100 px)
EDGE = {k: (VCOMMON / VOL1[k]) ** (1 / 3) for k in ORDER}
print('edges at equal volume (cube edge = 1): ' + ', '.join(f'{k} {EDGE[k] / EDGE["C"]:.6f}' for k in ORDER), flush=True)
def rot(ax, deg):
    ax = np.array(ax, float); ax /= np.linalg.norm(ax); a = math.radians(deg)
    K = np.array([[0, -ax[2], ax[1]], [ax[2], 0, -ax[0]], [-ax[1], ax[0], 0]])
    return np.eye(3) + math.sin(a) * K + (1 - math.cos(a)) * K @ K
def align(a, b):
    a = np.array(a, float) / np.linalg.norm(a); b = np.array(b, float) / np.linalg.norm(b); v = np.cross(a, b)
    return rot(v, math.degrees(math.atan2(np.linalg.norm(v), a @ b)))
Rx = lambda d: rot((1, 0, 0), d); Ry = lambda d: rot((0, 1, 0), d); Rz = lambda d: rot((0, 0, 1), d)
def upright(A, p):
    q = A @ np.array(p, float); return Rz(90 - math.degrees(math.atan2(q[1], q[0]))) @ A
A5 = align((0, 1, PHI), (0, 0, 1))
POSE = {   # x right, y up, z toward the viewer
    'D': Rx(16) @ Ry(-14) @ A5,                       # a pentagon face toward the viewer, tipped to show its ring
    'I': Rx(12) @ Ry(10) @ upright(A5, (0, -1, PHI)),  # a corner toward the viewer: the five-triangle cap, one point up
    'C': Rx(24) @ Ry(-33),                            # three faces: front, side and top (not square-on)
    'T': Rx(16) @ Ry(15) @ align((1, 1, 1), (0, 1, 0)),   # apex up, standing on a face
    'O': Rx(14) @ Ry(22),                             # a corner up: the double pyramid
}
CX, CY, RC = 1200, 1125, 720
CEN = {}
for i, k in enumerate(ORDER):
    th = math.radians(90 - 72 * i); CEN[k] = (CX + RC * math.cos(th), CY - RC * math.sin(th))
X('D at the top of the circle', abs(CEN['D'][0] - CX) < 1e-9 and CEN['D'][1] < CY)
X('clockwise D I C T O', CEN['I'][0] > CX > CEN['O'][0] and CEN['C'][1] > CY and CEN['C'][0] > CX and CEN['T'][0] < CX)
gaps = [math.dist(CEN[ORDER[i]], CEN[ORDER[(i + 1) % 5]]) for i in range(5)]
X('evenly spaced, 72 degrees', max(gaps) - min(gaps) < 1e-9, f'{min(gaps):.1f} px between centres')
def faces(V):
    h = ConvexHull(V); F = {}
    for sm, eq in zip(h.simplices, h.equations): F.setdefault(tuple(np.round(eq, 9)), set()).update(sm)
    out = []
    for eq, idx in F.items():
        idx = list(idx); Q = V[idx]; c = Q.mean(0); n = np.array(eq[:3]); a = Q[0] - c; a /= np.linalg.norm(a); b = np.cross(n, a)
        order = np.argsort(np.arctan2((Q - c) @ b, (Q - c) @ a)); out.append((n, [idx[i] for i in order]))
    return out
def tet_vol(V, F):
    return sum(abs(np.dot(V[f[0]], np.cross(V[f[i]], V[f[i + 1]]))) / 6 for _, f in F for i in range(1, len(f) - 1))
# ------------------------------------------------------------------ drawing
L = np.array([-0.45, 0.62, 0.64]); L /= np.linalg.norm(L)       # soft key light, upper left front
LP = np.array([-2.0, 2.6, 3.4])                                  # point light for the glints (in circumradii from each centre)
A_FRONT, A_BACK = 0.55, 0.60
canvas = np.ones((H * SS, W * SS, 3)) * GROUND
reach = {}
def lay(region, mask, col, a):
    m = (mask * a)[..., None]; region[:] = region * (1 - m) + col * m
for k in ORDER:
    P = np.array(SOLIDS[k], float); d = [math.dist(a, b) for a, b in itertools.combinations(P, 2)]
    X(f'{k}: edge-1 coordinates exact (shortest corner distance 1 in doubles, attained {NE[k]} times)', abs(min(d) - 1) < 1e-12 and sum(abs(x - 1) < 1e-12 for x in d) == NE[k])
    V = P * EDGE[k]; F = faces(V)
    E = {tuple(sorted((f[i], f[(i + 1) % len(f)]))) for _, f in F for i in range(len(f))}
    X(f'{k}: {len(V)} corners, {len(F)} faces, {len(E)} edges', (len(V), len(F), len(E)) == (NV[k], NF[k], NE[k]))
    vol = tet_vol(V - V.mean(0), F)
    X(f'{k}: volume = {VCOMMON}', abs(vol - VCOMMON) < 1e-9, f'{vol:.12f}')
    Vr = V @ POSE[k].T; rc = np.linalg.norm(Vr, axis=1).max(); reach[k] = rc * 100
    cx, cy = CEN[k]
    pix = lambda v: ((cx + v[0] * 100) * SS, (cy - v[1] * 100) * SS)
    pts2 = [pix(v) for v in Vr]
    X(f'{k}: inside the picture block (circumradius {reach[k]:.0f} px)', all(30 * SS < x < (W - 30) * SS and 30 * SS < y < (H - 30) * SS for x, y in pts2))
    x0 = int(min(p[0] for p in pts2)) - 6 * SS; x1 = int(max(p[0] for p in pts2)) + 6 * SS
    y0 = int(min(p[1] for p in pts2)) - 6 * SS; y1 = int(max(p[1] for p in pts2)) + 6 * SS
    reg = canvas[y0:y1, x0:x1]
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(float); u = (xx / SS - cx) / 100; v = -(yy / SS - cy) / 100
    base = np.array(COL[k], float)
    Fn = [(POSE[k] @ n, f) for n, f in F]
    front_of = {}
    for n, f in Fn:
        for i in range(len(f)): front_of.setdefault(tuple(sorted((f[i], f[(i + 1) % len(f)]))), []).append(n[2] > 1e-9)
    def poly_mask(f):
        m = Image.new('L', (x1 - x0, y1 - y0), 0); ImageDraw.Draw(m).polygon([(pts2[i][0] - x0, pts2[i][1] - y0) for i in f], fill=255)
        return np.array(m, float) / 255
    def edge_mask(es, width):
        m = Image.new('L', (x1 - x0, y1 - y0), 0); dr = ImageDraw.Draw(m)
        for a, b in es: dr.line([(pts2[a][0] - x0, pts2[a][1] - y0), (pts2[b][0] - x0, pts2[b][1] - y0)], fill=255, width=width)
        for a, b in es:
            for p in (a, b): r_ = width / 2; dr.ellipse([pts2[p][0] - x0 - r_, pts2[p][1] - y0 - r_, pts2[p][0] - x0 + r_, pts2[p][1] - y0 + r_], fill=255)
        return np.array(m, float) / 255
    # 1 back faces: even tint, a little darker (the far side)
    for n, f in Fn:
        if n[2] <= 1e-9: lay(reg, poly_mask(f), base * (0.95 + 0.10 * max(0.0, -n @ L)), A_BACK)
    # 2 back edges (both faces at the back): fainter, the colour itself
    back_e = [e for e, fr in front_of.items() if not any(fr)]
    lay(reg, edge_mask(back_e, int(round(2.0 * SS))), np.minimum(base * 1.15 + 20, 255), 0.55)
    # 3 front faces: even tint, soft light, thin glints (capped well below white)
    for n, f in Fn:
        if n[2] <= 1e-9: continue
        M = poly_mask(f)
        z = (n @ Vr[f[0]] - n[0] * u - n[1] * v) / n[2]
        p = np.dstack([u, v, z]) / rc; l = LP - p; l /= np.linalg.norm(l, axis=2, keepdims=True)
        h = l + np.array([0, 0, 1.0]); h /= np.linalg.norm(h, axis=2, keepdims=True)
        glint = 0.45 * np.clip(h @ n, 0, 1) ** 3000
        col = base[None, None] * (1.05 + 0.25 * max(0.0, n @ L))
        col = col * (1 - glint[..., None]) + np.array([255, 250, 240.]) * glint[..., None]
        lay(reg, M, np.minimum(col, 248), A_FRONT + 0.3 * glint)
    # 4 front edges (silhouette and front faces): crisp, a light tint of the colour
    front_e = [e for e, fr in front_of.items() if any(fr)]
    lay(reg, edge_mask(front_e, int(round(2.6 * SS))), base * 0.45 + 255 * 0.45, 0.95)
cl = [gaps[i] - reach[ORDER[i]] - reach[ORDER[(i + 1) % 5]] for i in range(5)]
X('neighbours clear of each other (centre distance > sum of circumradii)', min(cl) > 40, [round(c) for c in cl])
img = Image.fromarray(np.clip(canvas, 0, 255).astype(np.uint8))
img = img.resize((W, H), Image.LANCZOS) if SS > 1 else img
mx = np.array(img).max(axis=2)
X('nothing clips to white (largest channel < 250)', mx.max() < 250, int(mx.max()))
img.save(OUT)
print('PROGRESS 0.9 rendered', OUT, img.size, flush=True)
print('FINAL ok' if not FAIL else 'FINAL FAIL: ' + '; '.join(FAIL))
