# Step 1 of DICTO's "photo-real ring renders" test (2026-10-31): cut the PET-bottle-cap security rings out of his top-view
# photo of three big triangles (4 rings each) lying on tatami.
#   white mask   = low saturation + high value (white plastic vs beige tatami), morphological open/close
#   ring markers = the tatami holes enclosed by the white mask (each ring's open centre), filtered by size and roundness
#   ring pixels  = watershed of the white mask from the hole markers (splits rings that touch / are tied together)
#   corners      = outer contour in polar form about the hole centroid; the three corner directions maximise
#                  r(t)+r(t+120)+r(t+240); the rounded tips (max r near each direction) are the warp anchors, and
#                  tipfrac = 1/(2 q), q = side-midpoint radius / tip radius, records how round the ring is
#   sides        = apparent band width, brightness and size of central (turned-over) vs corner rings
#   output       = RGBA cut-out per ring rotated so one corner points up, + JSON of its three corners in cut-out pixels;
#                  zip-tie patches cut across the ring-ring boundaries where the boundary is whitest
# The photo is DICTO's own and PRIVATE: inputs and outputs live outside any git repo (PHOTO, OUTDIR env vars).
# Usage (dicto-big-brother): PHOTO=~/kres-tmp/ringphoto/2026-10-31-tetra-nets.jpg OUTDIR=~/kres-tmp/ringphoto/derived \
#        ~/geom/bin/python cutout.py
import os, json, math
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
from skimage.color import rgb2hsv
from skimage.segmentation import watershed
from skimage.measure import find_contours

PHOTO = os.path.expanduser(os.environ['PHOTO']); OUT = os.path.expanduser(os.environ['OUTDIR'])
os.makedirs(OUT, exist_ok=True)
img = np.asarray(Image.open(PHOTO).convert('RGB')).astype(np.float64) / 255
H, W = img.shape[:2]
hsv = rgb2hsv(img); S, V = hsv[..., 1], hsv[..., 2]

# ---------- white mask ----------
# local tatami brightness varies (lighting falls off top to bottom), so compare V with a heavily blurred background
bgV = ndi.median_filter(V[::8, ::8], size=25); bgV = ndi.zoom(bgV, (H / bgV.shape[0], W / bgV.shape[1]), order=1)[:H, :W]
white = (S < 0.16) & (V > bgV * 0.92) | (S < 0.09) & (V > 0.45)
white = ndi.binary_opening(white, np.ones((3, 3)))
white = ndi.binary_closing(white, np.ones((5, 5)))
lab, n = ndi.label(white); sizes = ndi.sum(white, lab, range(1, n + 1))
white = np.isin(lab, 1 + np.flatnonzero(sizes > 4000))       # drop tatami speckle

# ---------- holes = ring centres ----------
holes_all = ndi.binary_fill_holes(white) & ~white
hl, hn = ndi.label(holes_all); hs = ndi.sum(holes_all, hl, range(1, hn + 1))
cand = []
for k in range(1, hn + 1):
    if hs[k - 1] < 3000: continue
    ys, xs = np.nonzero(hl == k); cy, cx = ys.mean(), xs.mean()
    r = np.hypot(ys - cy, xs - cx); fill = hs[k - 1] / (math.pi * r.max() ** 2)
    cand.append((k, hs[k - 1], fill, cx, cy))
cand = [c for c in cand if c[2] > 0.35]
print('hole candidates', len(cand), [(int(c[1]), round(c[2], 2)) for c in cand])
markers = np.zeros((H, W), np.int32)
for i, (k, *_ ) in enumerate(cand): markers[hl == k] = i + 1
# grow each hole a little into the ring so the watershed starts from the band
dist_to_hole = ndi.distance_transform_edt(markers == 0)
filled = ndi.binary_fill_holes(white)
ws = watershed(dist_to_hole, markers, mask=filled)         # nearest-hole partition of the filled white region
rings = []
for i, (k, area, fill, cx, cy) in enumerate(cand):
    region = (ws == i + 1)
    band = region & white
    hole = markers == i + 1
    # remove tatami streaks clinging to the band (thin, horizontal): open with a disk, keep the main piece
    yy, xx = np.mgrid[-5:6, -5:6]; disk = (yy ** 2 + xx ** 2) <= 25
    band = ndi.binary_opening(band, disk) | (band & ndi.binary_dilation(hole, iterations=12))
    bl, bn = ndi.label(band); band = bl == (1 + np.argmax(ndi.sum(band, bl, range(1, bn + 1))))
    # outer contour of the ring = boundary of (band | hole), largest piece
    solid = ndi.binary_fill_holes(band | hole)
    sl, sn = ndi.label(solid); solid = sl == (1 + np.argmax(ndi.sum(solid, sl, range(1, sn + 1))))
    cont = max(find_contours(solid.astype(float), 0.5), key=len)       # (row, col)
    ang = np.arctan2(cont[:, 0] - cy, cont[:, 1] - cx); rad = np.hypot(cont[:, 0] - cy, cont[:, 1] - cx)
    # r(theta) on a 1-degree grid (max per bin), smoothed
    bins = ((np.degrees(ang) % 360)).astype(int); rr = np.zeros(360)
    for b, r in zip(bins, rad): rr[b] = max(rr[b], r)
    for b in range(360):
        if rr[b] == 0: rr[b] = rr[b - 1]
    rs = ndi.uniform_filter1d(rr, 15, mode='wrap')
    t0 = int(np.argmax([rs[t] + rs[(t + 120) % 360] + rs[(t + 240) % 360] for t in range(120)]))
    dirs = [t0, (t0 + 120) % 360, (t0 + 240) % 360]
    # warp anchors: the three rounded tips (max r near each corner direction) and the side midpoints (min r between them).
    # q = r_mid / r_tip; in a model triangle of circumradius R the tips are mapped to the points at distance R/(2q) from the
    # centre (so the side midpoints land on the model sides and neighbouring rings just touch) -> 'tipfrac' = 1/(2q)
    tips = []; mids = []
    for j in range(3):
        w = [(dirs[j] + d) % 360 for d in range(-20, 21)]; b = w[int(np.argmax(rs[w]))]
        tips.append(np.array([cx, cy]) + rs[b] * np.array([math.cos(math.radians(b)), math.sin(math.radians(b))]))
        mids.append(rs[[(dirs[j] + d) % 360 for d in range(45, 76)]].min())
    corners = np.array(tips); rtip = np.mean([np.linalg.norm(t - [cx, cy]) for t in tips]); q = np.mean(mids) / rtip
    side = np.mean([np.linalg.norm(corners[j] - corners[j - 1]) for j in range(3)])
    rings.append(dict(i=i, cx=cx, cy=cy, band=band, hole=hole, corners=corners, side=side, tipfrac=1 / (2 * q), area=int(band.sum())))
print('rings', len(rings))
# ---------- the two sides (DICTO: the bands are slightly conical; the central ring of each big triangle is turned over) ----------
# apparent band width seen from above = band pixels / outer perimeter; brightness of the band; mean outer tip radius
CENTRAL = {1, 6, 9}     # middle ring of each big triangle (it shares a tied side with each of the other three)
sides = {}
for r in rings:
    solid = ndi.binary_fill_holes(r['band'] | r['hole']); per = (solid ^ ndi.binary_erosion(solid)).sum()
    dt = ndi.distance_transform_edt(r['band'])
    r['width'] = r['band'].sum() / per; r['dtmax'] = float(np.percentile(dt[dt > 0], 95)) * 2
    r['bright'] = float(V[r['band']].mean()); r['central'] = r['i'] in CENTRAL
    r['tipR'] = float(np.mean([np.linalg.norm(t - [r['cx'], r['cy']]) for t in r['corners']]))
    r['holefrac'] = r['hole'].sum() / solid.sum()
for g, nm in ((True, 'central'), (False, 'corner')):
    G = [r for r in rings if r['central'] == g]
    sides[nm] = {k: round(float(np.mean([r[k] for r in G])), 3) for k in ('width', 'dtmax', 'bright', 'tipR', 'holefrac', 'tipfrac')}
    sides[nm]['n'] = len(G)
print('sides', sides)

# ---------- cut-outs, rotated so corner 0 points up ----------
# soft matte: white plastic has low saturation, tatami fringe is beige (S ~ 0.25) -> fade alpha out between S 0.13 and 0.20
matte = np.clip((0.20 - S) / 0.07, 0, 1) * ndi.gaussian_filter(white.astype(float), 0.8)
alpha_full = white.astype(np.float64)
meta = []
for r in rings:
    i = r['i']; c = r['corners']; cen = c.mean(0)
    # soft alpha: band mask feathered by 1 px
    a = ndi.gaussian_filter(r['band'].astype(float), 0.8) * np.clip((0.20 - S) / 0.07, 0, 1)
    # choose the corner whose direction is closest to 'up' then rotate so it is exactly up
    up = int(np.argmax([((p - cen) / np.linalg.norm(p - cen)) @ [0, -1] for p in c]))
    rot = math.degrees(math.atan2(c[up][1] - cen[1], c[up][0] - cen[0])) + 90   # degrees to rotate clockwise in image
    R = int(r['side'] * 0.75) + 24
    x0, y0 = int(cen[0]) - R, int(cen[1]) - R
    crop = np.zeros((2 * R, 2 * R, 4))
    ys, xs = slice(max(0, y0), min(H, y0 + 2 * R)), slice(max(0, x0), min(W, x0 + 2 * R))
    crop[ys.start - y0:ys.stop - y0, xs.start - x0:xs.stop - x0, :3] = img[ys, xs]
    crop[ys.start - y0:ys.stop - y0, xs.start - x0:xs.stop - x0, 3] = a[ys, xs]
    im = Image.fromarray((crop * 255).astype(np.uint8), 'RGBA').rotate(rot, resample=Image.BICUBIC, center=(R, R))
    # same rotation on the corners (PIL rotates counter-clockwise by +angle in image coords with y down)
    t = math.radians(rot); M = np.array([[math.cos(t), math.sin(t)], [-math.sin(t), math.cos(t)]])
    cc = (c - [x0, y0] - R) @ M.T + R
    order = [up, (up + 1) % 3, (up + 2) % 3]; cc = cc[order]
    im.save(os.path.join(OUT, f'ring-{i:02d}.png'))
    meta.append(dict(file=f'ring-{i:02d}.png', central=r['central'], width_px=round(r['width'], 2), size=2 * R, corners=cc.round(2).tolist(), tipfrac=round(r['tipfrac'], 4), side_px=round(r['side'], 1),
                     band_px=r['area'], photo_centre=[round(r['cx']), round(r['cy'])]))

# ---------- zip-tie patches ----------
# Tie centres picked by eye on a 3x zoom of the photo (the automatic ring-ring contact finder lands between the two ties of a
# side). Across-the-side direction = from the nearer to the farther of the two nearest ring centres.
TIE_POINTS = [(570, 557), (613, 603), (487, 630), (487, 693), (630, 713), (590, 733)]
cen = np.array([[r['cx'], r['cy']] for r in rings])
ties = []
for p in TIE_POINTS:
    p = np.array(p, float); k = np.argsort(np.linalg.norm(cen - p, axis=1))[:2]
    d = cen[k[1]] - cen[k[0]]; d /= np.linalg.norm(d); ties.append(dict(p=p, d=d, pair=tuple(int(x) for x in k)))
tmeta = []
for j, t in enumerate(ties):
    p, d = t['p'], t['d']; L, Wd = 30, 13      # half-length across the side, half-width along it (photo px)
    rot = math.degrees(math.atan2(d[1], d[0]))   # across-side direction -> horizontal
    R = 50; x0, y0 = int(p[0]) - R, int(p[1]) - R
    crop = np.zeros((2 * R, 2 * R, 4))
    crop[..., :3] = img[y0:y0 + 2 * R, x0:x0 + 2 * R]; crop[..., 3] = matte[y0:y0 + 2 * R, x0:x0 + 2 * R]
    im = Image.fromarray((crop * 255).astype(np.uint8), 'RGBA').rotate(rot, resample=Image.BICUBIC, center=(R, R))
    im = np.asarray(im.crop((R - L, R - Wd, R + L, R + Wd))).astype(float)
    # soft window along the side so the patch blends into the band it is pasted on
    wy = np.clip((Wd - np.abs(np.arange(2 * Wd) - Wd + 0.5)) / 5, 0, 1); wx = np.clip((L - np.abs(np.arange(2 * L) - L + 0.5)) / 6, 0, 1)
    im[..., 3] *= np.outer(wy, wx)
    Image.fromarray(im.astype(np.uint8), 'RGBA').save(os.path.join(OUT, f'tie-{j}.png'))
    tmeta.append(dict(file=f'tie-{j}.png', pair=t['pair'], photo=[round(p[0]), round(p[1])]))

json.dump(dict(rings=meta, ties=tmeta, sides=sides), open(os.path.join(OUT, 'cutouts.json'), 'w'), indent=1)

# ---------- debug overlay ----------
ov = img.copy() * 0.55
pal = np.array([[1, .3, .3], [.3, 1, .3], [.3, .5, 1], [1, 1, .3], [1, .3, 1], [.3, 1, 1], [1, .6, .2], [.6, .3, 1],
                [.2, .8, .5], [.9, .5, .7], [.5, .9, .1], [.1, .6, .9], [.8, .8, .8], [.6, .6, .2]])
for r in rings: ov[r['band']] = 0.4 * ov[r['band']] + 0.6 * pal[r['i'] % len(pal)]
oi = Image.fromarray((ov * 255).astype(np.uint8))
from PIL import ImageDraw
dr = ImageDraw.Draw(oi)
for r in rings:
    c = r['corners']; dr.polygon([tuple(p) for p in c], outline=(255, 255, 255)); dr.text((r['cx'], r['cy']), str(r['i']), fill=(255, 255, 0))
for t in tmeta: dr.rectangle([t['photo'][0] - 6, t['photo'][1] - 6, t['photo'][0] + 6, t['photo'][1] + 6], outline=(255, 0, 0), width=3)
oi.save(os.path.join(OUT, 'debug-segmentation.jpg'), quality=88)
print(json.dumps([(m['file'], m['side_px'], m['band_px']) for m in meta]))
print('ties', [(t['file'], t['pair'], t['photo']) for t in tmeta])
