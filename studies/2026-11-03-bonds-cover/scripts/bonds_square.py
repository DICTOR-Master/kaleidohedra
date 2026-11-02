# The DICTONIC square (book cover): cover for the book "DICTONIC Bonds: from the Octet to the Rule of Halves" (2026-11-03), after the
# HexOct, Golden Cycle, Alicia and Star Cores squares. Cyclic Latin square 8 x 8: row i, column j holds position (i+j) mod 8 of DICTONIC,
# so DICTONIC reads across the top and down the left and every position (piece) comes once in each row and column. Each position is one
# of the eight pieces of the four DICTONIC bonds, in the book's order (preface): D Icosaxes, I Unborn Axes (Golden bond, ch. 3);
# C Lotus Jewel Axes, T Dodecaxes (Keyed bond, ch. 3); O Samson, N Delilah (Delian bond, ch. 4); I Sonsam, C Lahdeli (Twinned Delian
# bond, ch. 8). Exact geometry from the DICTO Solids dataset v7 (solids/<slug>.json, decimal corners and faces), each piece drawn at one
# circumradius in the squares' one pose. One colour per bond (the squares' palette): Golden gold, Keyed violet, Delian teal, Twinned
# Delian blue. Two pieces are not convex (the Lotus Jewel Axes' dents, the Dodecaxes' keys), so the pieces are drawn with a depth
# buffer, not by sorting faces; edges are the borders between visible face planes (coplanar parts of one face are one face).
# Letters: the HexOct LED letters (DSEG14 Classic, OFL), reciprocal colours (DICTO 11-03): Golden and Keyed swap gold/violet, Delian and
# Twinned Delian swap teal/blue, so the letters use only the four piece colours.
# Usage: bonds_square.py <dataset solids dir>
import math, os, sys, json, numpy as np
from scipy import ndimage
from PIL import Image, ImageDraw, ImageFont
SOL = sys.argv[1]
WORD = 'DICTONIC'; n = 8
M = [[(i + j) % n for j in range(n)] for i in range(n)]
assert all(len(set(r)) == n for r in M) and all(len({M[i][j] for i in range(n)}) == n for j in range(n))
assert ''.join(WORD[k] for k in M[0]) == WORD and ''.join(WORD[M[i][0]] for i in range(n)) == WORD
PIECES = [('Icosaxes', 'dicto-icosaxes', 14), ('Unborn Axes', 'dicto-unborn-axes', 14), ('Lotus Jewel Axes', 'dicto-lotus-jewel-axes', 54),
          ('Dodecaxes', 'dicto-dodecaxes', 54), ('Samson', 'dicto-samson', 10), ('Delilah', 'dicto-delilah', 8),
          ('Sonsam', 'dicto-sonsam', 13), ('Lahdeli', 'dicto-lahdeli', 8)]   # name, dataset slug, faces (as a check)
BOND = [0, 0, 1, 1, 2, 2, 3, 3]
BONDTONE = [(217, 165, 33), (138, 92, 196), (43, 179, 163), (58, 112, 205)]          # gold, violet, teal, blue
BONDLETTER = [(190, 140, 255), (255, 205, 70), (96, 156, 255), (90, 232, 212)]        # reciprocal (DICTO 11-03): each bond's letters in its partner bond's
# piece colour, brightened as the Star Cores letters (same values): Golden violet, Keyed gold, Delian blue, Twinned Delian teal
def load(slug):
    m = json.load(open(os.path.join(SOL, slug + '.json')))
    return np.array([[float(x) for x in v['decimal']] for v in m['vertices']]), [list(f) for f in m['faces']]
def outward(V, F):
    """faces wound consistently (every edge once each way), turned so the signed volume is positive (outward normals)."""
    E = {}
    for f in F:
        for k in range(len(f)): E[(f[k], f[(k + 1) % len(f)])] = E.get((f[k], f[(k + 1) % len(f)]), 0) + 1
    assert all(c == 1 and E.get((b, a)) == 1 for (a, b), c in E.items()), 'faces not consistently wound'
    vol = sum(np.dot(V[f[0]], np.cross(V[f[k]], V[f[k + 1]])) for f in F for k in range(1, len(f) - 1)) / 6
    return (F if vol > 0 else [f[::-1] for f in F]), abs(vol)
GEOM = []
for name, slug, nf in PIECES:
    V, F = load(slug); assert len(F) == nf, (name, len(F)); F, vol = outward(V, F)
    c = V.mean(0); V = V - c; V = V / np.linalg.norm(V, axis=1).max()
    print(name, len(V), 'corners', len(F), 'faces', 'volume', round(vol, 6)); GEOM.append((V, F))
def rot(ax, a):
    ax = np.array(ax, float); ax /= np.linalg.norm(ax); K = np.array([[0, -ax[2], ax[1]], [ax[2], 0, -ax[0]], [-ax[1], ax[0], 0]])
    return np.eye(3) + math.sin(a) * K + (1 - math.cos(a)) * K @ K
VIEW = rot((1, 0.55, 0.15), 0.85)   # the squares' general pose
GROUND = (20, 15, 11); EDGE = (40, 26, 12)
N = 2400; SS = 2; W = N * SS; cell = 0.92 * W / n; sc = 0.44 * cell; x0 = 0.04 * W
light = np.array([-0.4, 0.55, 0.75]); light /= np.linalg.norm(light)
def sprite(V, F, tone):
    """depth-buffered drawing of one piece: (rgb, mask) of side S, centred; +z towards the viewer."""
    S = int(2 * sc) + 16; h = S / 2; P = V @ VIEW.T
    X = h + P[:, 0] * sc; Y = h - P[:, 1] * sc; Z = P[:, 2]
    depth = np.full((S, S), -np.inf); fid = np.full((S, S), -1)
    planes, shade = {}, []
    for f in F:
        Q = V[f]; nn = np.zeros(3)
        for k in range(len(Q)): nn += np.cross(Q[k], Q[(k + 1) % len(Q)])
        nn /= np.linalg.norm(nn); key = tuple(np.round(np.r_[nn, nn @ Q[0]], 5))
        if key not in planes: planes[key] = len(planes); shade.append(nn)
        pid = planes[key]
        for k in range(1, len(f) - 1):   # faces are convex polygons (3-9 sides): fan triangles
            a, b, c = f[0], f[k], f[k + 1]
            xs, ys = np.array([X[a], X[b], X[c]]), np.array([Y[a], Y[b], Y[c]])
            i0, i1 = max(0, int(np.floor(ys.min()))), min(S - 1, int(np.ceil(ys.max())))
            j0, j1 = max(0, int(np.floor(xs.min()))), min(S - 1, int(np.ceil(xs.max())))
            yy, xx = np.mgrid[i0:i1 + 1, j0:j1 + 1] + 0.5
            den = (ys[1] - ys[2]) * (xs[0] - xs[2]) + (xs[2] - xs[1]) * (ys[0] - ys[2])
            if abs(den) < 1e-9: continue
            l0 = ((ys[1] - ys[2]) * (xx - xs[2]) + (xs[2] - xs[1]) * (yy - ys[2])) / den
            l1 = ((ys[2] - ys[0]) * (xx - xs[2]) + (xs[0] - xs[2]) * (yy - ys[2])) / den
            l2 = 1 - l0 - l1; inside = (l0 >= -1e-6) & (l1 >= -1e-6) & (l2 >= -1e-6)
            z = l0 * Z[a] + l1 * Z[b] + l2 * Z[c]
            dsub, fsub = depth[i0:i1 + 1, j0:j1 + 1], fid[i0:i1 + 1, j0:j1 + 1]
            win = inside & (z > dsub + 1e-7); dsub[win] = z[win]; fsub[win] = pid
    rgb = np.zeros((S, S, 3)); tone = np.array(tone, float)
    for pid, nn in enumerate(shade):
        b = 0.45 + 0.55 * max(0, (VIEW @ nn) @ light); rgb[fid == pid] = tone * b
    mask = fid >= 0
    border = np.zeros((S, S), bool)   # borders between visible planes and the outline
    border[:, 1:] |= fid[:, 1:] != fid[:, :-1]; border[:, :-1] |= fid[:, 1:] != fid[:, :-1]
    border[1:, :] |= fid[1:, :] != fid[:-1, :]; border[:-1, :] |= fid[1:, :] != fid[:-1, :]
    border = ndimage.binary_dilation(border, iterations=SS) & ndimage.binary_dilation(mask, iterations=SS)   # ~2 px at the final size
    rgb[border] = EDGE; mask = mask | border
    return rgb, mask
img = np.ones((W, W, 3)) * np.array(GROUND, float)
SPR = [sprite(V, F, BONDTONE[BOND[k]]) for k, (V, F) in enumerate(GEOM)]
for i in range(n):
    for j in range(n):
        rgb, mask = SPR[M[i][j]]; S = mask.shape[0]; cx, cy = x0 + (j + 0.5) * cell, x0 + (i + 0.5) * cell
        oy, ox = int(round(cy - S / 2)), int(round(cx - S / 2)); sub = img[oy:oy + S, ox:ox + S]
        sub[mask] = rgb[mask]
img = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
f = ImageFont.truetype('DSEG14Classic-Regular.ttf', int(0.047 * W))
def carved(ch, col):   # Star Cores' carved LED letter (DICTO 10-31: opposite letter colours)
    box = int(0.1 * W); edge = int(round(1.5 * int(0.002 * W)))   # DICTO 11-03 'slightly more black around letter outlines': rim 1.5x (9 -> 14 px at W = 4800)
    def lay(t, sw=0):
        m = Image.new('L', (box, box), 0); ImageDraw.Draw(m).text((box / 2, box / 2), t, font=f, fill=255, anchor='mm', stroke_width=sw, stroke_fill=255)
        return np.array(m, float) / 255
    On, Rim, Ghost = lay(ch), lay(ch, edge), lay('~')
    glow = ndimage.gaussian_filter(On, 0.005 * W); glow /= glow.max()
    core = np.array(col, float); halo = 0.55 * core + 0.45 * 255
    rgb = (core * On[..., None] + halo * (1 - On[..., None])) * (On + 0.6 * glow)[..., None] / np.maximum(On + 0.6 * glow, 1e-6)[..., None]
    rim = (Rim - On) > 0.3
    rgb = np.where(rim[..., None], np.array([8, 6, 4.]), rgb)
    rgb = np.where(((Ghost - Rim) > 0.5)[..., None], halo, rgb)
    alpha = np.clip(np.maximum.reduce([On, 1.0 * rim, 0.45 * glow, 0.14 * Ghost]), 0, 1)
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)), Image.fromarray((alpha * 255).astype(np.uint8)), (box, box)
CARVE = {k: carved(WORD[k], BONDLETTER[BOND[k]]) for k in range(n)}
for i in range(n):
    for j in range(n):
        t, m, (bw, bh) = CARVE[M[i][j]]; cx, cy = x0 + (j + 0.5) * cell, x0 + (i + 0.5) * cell
        img.paste(t, (int(cx - bw / 2), int(cy - bh / 2)), m)
img = img.resize((N, N), Image.LANCZOS); img.save(os.environ.get('OUT', '../bonds-square.png')); print('ok')
