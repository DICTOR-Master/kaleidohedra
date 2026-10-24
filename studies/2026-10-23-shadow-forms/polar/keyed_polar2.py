# Pictures for the hull-and-remainder polar of the keyed pair. Non-convex Lotus Jewel Axes drawn from its true faces.
import numpy as np, itertools
from PIL import Image, ImageDraw, ImageFont
from scipy.spatial import ConvexHull
exec(open('keyed_polar1.py').read().split("vt = vol(TR[0])")[0])
def polar(P):
    E = ConvexHull(P).equations; Q = -E[:, :3] / E[:, 3:4]; return Q[ConvexHull(Q).vertices]
def hull_faces(V):
    h = ConvexHull(V); out = []
    for e in h.equations:
        if any(np.allclose(e, q, atol=1e-7) for q, _ in out): continue
        on = V[np.abs(V @ e[:3] + e[3]) < 1e-7]; c0 = on.mean(0); u = on[0] - c0; u /= np.linalg.norm(u); w = np.cross(e[:3], u)
        out.append((e, on[np.argsort(np.arctan2((on - c0) @ w, (on - c0) @ u))]))
    return [(e[:3], f) for e, f in out]
def lotus_faces():
    # dents: the Unborn at c_s = (phi/2) s sends its Tricap in direction -s into the Icosaxes at the origin
    F = []; tris = [tricap(*(-np.array(sg))) + np.array(sg) * phi/2 for sg in itertools.product((1, -1), repeat=3)]
    for n, f in hull_faces(ICO):
        if not np.isclose(abs(n).sum(), 3**.5): F.append((n, f)); continue
        t = [d for d in tris if np.allclose([v @ n for v in d[1:]], f[0] @ n)][0]
        base = {tuple(np.round(v, 9)) for v in t[1:]}
        for i in [i for i, v in enumerate(f) if tuple(np.round(v, 9)) not in base]:
            F.append((n, np.array([f[i-1], f[i], f[(i+1) % 6]])))
        ap, b = t[0], t[1:]
        for i in range(3):
            q = np.array([b[i], b[(i+1) % 3], ap]); m = np.cross(q[1]-q[0], q[2]-q[0]); m /= np.linalg.norm(m)
            if m @ (b.mean(0) - ap) < 0: m = -m      # dent walls face out of the hole, towards the base opening
            F.append((m, q))
    return F
def draw(faces, size, R, col, title, L=np.array([-.4, .6, .7])/np.linalg.norm([-.4, .6, .7])):
    im = Image.new('RGB', (size, size), 'white'); d = ImageDraw.Draw(im)
    P = np.vstack([f for _, f in faces]); c0 = P.mean(0); r = np.max(np.linalg.norm(P - c0, axis=1)); polys = []
    for n, f in faces:
        nn = R @ n
        if nn[2] <= 1e-9: continue
        W = (f - c0) @ R.T; sh = .45 + .55*max(0, nn @ L); cl = col(n, f)
        polys.append((W[:, 2].mean(), [(size/2 + q[0]/r*size*.40, size/2 - q[1]/r*size*.40 + 14) for q in W], tuple(int(x*sh) for x in cl)))
    for z, pts, cl in sorted(polys, key=lambda x: x[0]): d.polygon(pts, fill=cl, outline=tuple(max(0, x-70) for x in cl), width=2)
    d.text((10, 6), title, fill=(40, 40, 40), font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 17)); return im
def rot(a, b):
    Ry = np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]]); Rx = np.array([[1, 0, 0], [0, np.cos(b), -np.sin(b)], [0, np.sin(b), np.cos(b)]]); return Rx @ Ry
R = rot(.6, -.5)
GREEN, ORANGE, PINK, BLUE = (86, 168, 102), (232, 145, 63), (240, 143, 192), (90, 130, 200)
LJ = lotus_faces()
t1 = draw(LJ, 460, R, lambda n, f: PINK if len(f) == 3 and not np.isclose(abs(n).sum(), 3**.5) and not (np.isclose(abs(n), 1).any()) else GREEN, 'Lotus Jewel Axes (8 dents, pink)')
t2 = draw(hull_faces(ICO), 460, R, lambda n, f: GREEN, 'filled in: Icosaxes')
t3 = draw(hull_faces(polar(ICO)), 460, R, lambda n, f: (120, 200, 140), 'polar of Icosaxes (pyramids 1/φ)')
DX = hull_faces(UNB) + [fc for t in TR for fc in hull_faces(t)]
t4 = draw(DX, 460, R, lambda n, f: PINK if any(np.allclose(f[0], v) for t in TR for v in t) and len(f) == 3 else ORANGE, 'Dodecaxes (8 keys, pink)')
t5 = draw(hull_faces(UNB), 460, R, lambda n, f: ORANGE, 'keys off: Unborn Axes')
t6 = draw(hull_faces(polar(UNB)), 460, R, lambda n, f: (240, 180, 120), 'polar of Unborn Axes (pyramids 1/φ²)')
g = TR[0].mean(0); Rt = rot(np.pi/4, np.arctan(1/2**.5) + .75)
t7 = draw(hull_faces(TR[0]), 460, Rt, lambda n, f: PINK, 'the remainder: one Tricap')
t8 = draw(hull_faces(polar(TR[0] - g)), 460, Rt, lambda n, f: (200, 120, 170), 'polar of the Tricap (edges 1 : tan 72°)')
blank = Image.new('RGB', (460, 460), 'white'); d = ImageDraw.Draw(blank); f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 17)
for i, line in enumerate(['Lotus Jewel Axes = Icosaxes − 8 Tricaps', '      √5 = (1 + 2√5/3) − 8/(12φ²)', '', 'Dodecaxes = Unborn Axes + 8 Tricaps', '      2 = (1 + √5/3) + 8/(12φ²)', '', 'The same 8 Tricaps pass from', 'one solid to the other: fill in,', 'take the polar, keep the remainder.', '', 'DICTO\'s method, 24 Oct 2026']):
    d.text((20, 120 + 24*i), line, fill=(40, 40, 40), font=f)
sheet = Image.new('RGB', (1380, 1380), 'white')
for i, t in enumerate([t1, t2, t3, t4, t5, t6, t7, t8, blank]): sheet.paste(t, ((i % 3)*460, (i//3)*460))
ImageDraw.Draw(sheet).text((1270, 1350), 'DICTO', fill=(120, 120, 120), font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 20))
sheet.save('keyed-polar.png'); print('saved')
