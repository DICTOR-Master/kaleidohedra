# The Platonic Solids, series front cover, third design (DICTO, 15 Nov 2026: "just the five solids plain in a circle in DICTO order,
# Dodecahedron at the top"). The five Platonic solids, plain and opaque, in their element colours (DICTO square, 10-22), evenly on a
# circle (72 degrees apart): Dodecahedron at the top, then clockwise Icosahedron, Cube, Tetrahedron, Octahedron. All five at the same
# circumradius, so the circle reads balanced. Each turned to a recognisable view.
# Drawn like the Golden Cycle cover's solids (studies/2026-10-29-golden-cover/scripts/golden_square.py): solid faces, crisp
# antialiased edges (supersampled), here with gloss (a point-light highlight per pixel), depth shading and no haze, on the series ground.
# Run: python circle_scene.py OUT.png      env SS = supersampling (default 3). Output: the 2400 x 2200 picture block of the cover.
import os, sys, math, itertools
import numpy as np
from scipy.spatial import ConvexHull
from PIL import Image, ImageDraw
OUT = sys.argv[1]; SS = int(os.environ.get('SS', '3'))
W, H = 2400, 2200; GROUND = (20, 15, 11)
PHI = (1 + 5 ** 0.5) / 2
FAIL = []
def X(name, ok, detail=''):
    print(('X PASS ' if ok else 'X FAIL ') + name + (f': {detail}' if detail != '' else ''), flush=True)
    if not ok: FAIL.append(name)
cyc = lambda a, b, c: [(a, b, c), (c, a, b), (b, c, a)]
def signs(v): return sorted({tuple(x * s for x, s in zip(v, t)) for t in itertools.product((1, -1), repeat=3)})
CUBE8 = signs((1, 1, 1))
RAW = {
    'D': CUBE8 + [w for c in cyc(0, 1 / PHI, PHI) for w in signs(c)],
    'I': [w for c in cyc(0, 1, PHI) for w in signs(c)],
    'C': CUBE8,
    'T': [v for v in CUBE8 if v[0] * v[1] * v[2] > 0],
    'O': [w for c in cyc(1, 0, 0) for w in signs(c)],
}
NV, NF, NE = {'D': 20, 'I': 12, 'C': 8, 'T': 4, 'O': 6}, {'D': 12, 'I': 20, 'C': 6, 'T': 4, 'O': 8}, {'D': 30, 'I': 30, 'C': 12, 'T': 6, 'O': 12}
COL = {'D': (138, 92, 196), 'I': (58, 112, 205), 'C': (72, 142, 72), 'T': (205, 62, 40), 'O': (232, 200, 82)}   # element colours
ORDER = 'DICTO'
def faces(V):
    h = ConvexHull(V); F = {}
    for sm, eq in zip(h.simplices, h.equations): F.setdefault(tuple(np.round(eq, 9)), set()).update(sm)
    out = []
    for eq, idx in F.items():
        Q = V[list(idx)]; c = Q.mean(0); n = np.array(eq[:3]); a = Q[0] - c; a /= np.linalg.norm(a); b = np.cross(n, a)
        out.append((n, Q[np.argsort(np.arctan2((Q - c) @ b, (Q - c) @ a))]))
    return out
SOL = {}
for k in ORDER:
    V = np.array(RAW[k], float); V /= np.linalg.norm(V, axis=1).max()        # circumradius 1 for every solid
    F = faces(V); E = {tuple(sorted((tuple(np.round(Q[i], 9)), tuple(np.round(Q[(i + 1) % len(Q)], 9))))) for _, Q in F for i in range(len(Q))}
    d = [math.dist(a, b) for a, b in itertools.combinations(V, 2)]; e = min(d)
    X(f'{k}: {len(V)} corners, {len(F)} faces, {len(E)} edges', (len(V), len(F), len(E)) == (NV[k], NF[k], NE[k]))
    X(f'{k}: every corner at circumradius 1', np.abs(np.linalg.norm(V, axis=1) - 1).max() < 1e-12)
    X(f'{k}: all edges equal (shortest corner distance attained {NE[k]} times, to 1e-12)', sum(abs(x - e) < 1e-12 for x in d) == NE[k], f'edge {e:.12f}')
    SOL[k] = F
# ------------------------------------------------------------------ poses (x right, y up, z toward the viewer)
def rot(ax, deg):
    ax = np.array(ax, float); ax /= np.linalg.norm(ax); a = math.radians(deg)
    K = np.array([[0, -ax[2], ax[1]], [ax[2], 0, -ax[0]], [-ax[1], ax[0], 0]])
    return np.eye(3) + math.sin(a) * K + (1 - math.cos(a)) * K @ K
def align(a, b):   # rotation taking direction a to direction b
    a = np.array(a, float) / np.linalg.norm(a); b = np.array(b, float) / np.linalg.norm(b); v = np.cross(a, b); c = a @ b
    if np.linalg.norm(v) < 1e-12: return np.eye(3) if c > 0 else rot(np.cross(a, [1, 0, 0]) if abs(a[0]) < 0.9 else np.cross(a, [0, 1, 0]), 180)
    return rot(v, math.degrees(math.atan2(np.linalg.norm(v), c)))
Rx = lambda d: rot((1, 0, 0), d); Ry = lambda d: rot((0, 1, 0), d); Rz = lambda d: rot((0, 0, 1), d)
def upright(A, pts):   # turn about the view axis so the first of pts (after A) points straight up
    p = A @ np.array(pts, float); return Rz(90 - math.degrees(math.atan2(p[1], p[0]))) @ A
A_D = align((0, 1, PHI), (0, 0, 1)); A_I = align((0, 1, PHI), (0, 0, 1))
POSE = {
    'D': Rx(16) @ Ry(-14) @ A_D,                                        # a pentagon face toward the viewer, tipped to show its ring
    'I': Rx(12) @ Ry(10) @ upright(A_I, (0, -1, PHI)),                  # a corner toward the viewer: the five-triangle cap, one point up
    'C': Rx(24) @ Ry(-33),                                              # three faces: front, side and top (not square-on)
    'T': Rx(16) @ align((1, 1, 1), (0, 1, 0)),                          # apex up, standing on a face, two side faces seen
    'O': Rx(14) @ Ry(22),                                               # a corner up: the double pyramid
}
# ------------------------------------------------------------------ layout: a circle, D at the top, clockwise D I C T O
CX, CY, RC, RS = 1200, 1125, 720, 305      # circle centre (picture pixels), circle radius, solid circumradius (all five the same)
CEN = {}
for i, k in enumerate(ORDER):
    th = math.radians(90 - 72 * i); CEN[k] = (CX + RC * math.cos(th), CY - RC * math.sin(th))
X('D at the top of the circle', abs(CEN['D'][0] - CX) < 1e-9 and CEN['D'][1] < CY)
X('clockwise D I C T O: I right of the top, O left', CEN['I'][0] > CX and CEN['O'][0] < CX and CEN['C'][1] > CY and CEN['C'][0] > CX)
gaps = [math.dist(CEN[ORDER[i]], CEN[ORDER[(i + 1) % 5]]) for i in range(5)]
X('neighbours evenly spaced (72 degrees) and clear of each other', max(gaps) - min(gaps) < 1e-9 and min(gaps) > 2 * RS + 100, f'centre gap {min(gaps):.1f} px, solid diameter {2 * RS}')
X('all five inside the picture block', all(RS + 40 < x < W - RS - 40 and RS + 40 < y < H - RS - 40 for x, y in CEN.values()))
# ------------------------------------------------------------------ shading
L = np.array([-0.45, 0.62, 0.64]); L /= np.linalg.norm(L)                # key light from the upper left, in front
LP = np.array([-1.8, 2.4, 3.2])                                          # point light for the highlight, in circumradii from each centre
AMB, KD, KS, SHIN = 0.36, 0.64, 0.55, 70.0
canvas = np.ones((H * SS, W * SS, 3)) * np.array(GROUND, float)
lines = []
for k in ORDER:
    R = POSE[k]; base = np.array(COL[k], float); cx, cy = CEN[k]; s = RS * SS
    front = [(R @ n, Q @ R.T) for n, Q in SOL[k] if (R @ n)[2] > 1e-9]
    X(f'{k}: faces seen = {len(front)}', len(front) >= 2)
    for n, Q in front:
        pts = [((cx + v[0] * RS) * SS, (cy - v[1] * RS) * SS) for v in Q]
        x0, y0 = int(min(p[0] for p in pts)) - 2, int(min(p[1] for p in pts)) - 2; x1, y1 = int(max(p[0] for p in pts)) + 3, int(max(p[1] for p in pts)) + 3
        m = Image.new('L', (x1 - x0, y1 - y0), 0); ImageDraw.Draw(m).polygon([(px - x0, py - y0) for px, py in pts], fill=255)
        M = np.array(m, float) / 255
        yy, xx = np.mgrid[y0:y1, x0:x1].astype(float)
        u = (xx / SS - cx) / RS; v = -(yy / SS - cy) / RS                  # solid coordinates (circumradius 1)
        d = n @ Q[0]; z = (d - n[0] * u - n[1] * v) / n[2]                  # the face plane
        p = np.dstack([u, v, z]); l = LP - p; l /= np.linalg.norm(l, axis=2, keepdims=True)
        h = l + np.array([0, 0, 1.0]); h /= np.linalg.norm(h, axis=2, keepdims=True)
        spec = KS * np.clip(h @ n, 0, 1) ** SHIN
        diff = AMB + KD * max(0.0, n @ L)
        refl = 2 * n[2] * n - np.array([0, 0, 1.0]); env = 0.10 * max(0.0, refl[1])   # soft sky in the reflection: upper faces lighter
        depth = 0.80 + 0.20 * (np.clip(z, -1, 1) + 1) / 2                 # nearer = brighter; no haze, only darkening with depth
        col = base[None, None] * (diff + env) * depth[..., None] + 255 * spec[..., None]
        sl = canvas[y0:y1, x0:x1]; sl[:] = sl * (1 - M[..., None]) + np.clip(col, 0, 255) * M[..., None]
        lines.append((pts, tuple(int(c) for c in 0.30 * base)))
img = Image.fromarray(np.clip(canvas, 0, 255).astype(np.uint8)); dr = ImageDraw.Draw(img)
for pts, ec in lines: dr.line(pts + [pts[0]], fill=ec, width=int(round(2.4 * SS)), joint='curve')
img = img.resize((W, H), Image.LANCZOS) if SS > 1 else img
img.save(OUT)
print('PROGRESS 0.9 rendered', OUT, img.size, flush=True)
print('FINAL ok' if not FAIL else 'FINAL FAIL: ' + '; '.join(FAIL))
