# Cube/octahedron changeover (DICTO 10-23 'could also run separately to octahedra and cubes'; open-work item 7, 10-24).
# Cubes at C = Z^3 and the cube centres V = (1/2,1/2,1/2)+Z^3 given a weight w (power diagram). Each C cell is the cube |p_i| <= 1/2
# cut by the 8 planes |x|+|y|+|z| <= 3/4 - w; each V cell the same with -w. w = -3/4: cubes only; growing w: truncated cubes +
# octahedra; w = 1/4 - 1/sqrt2: regular truncated cubes; w = -1/4: cuboctahedra + octahedra (factor x's x -> 0 end); w = 0: Kelvin.
import sys, itertools, numpy as np
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__))); from solidraw import draw_solids
from scipy.spatial import ConvexHull, HalfspaceIntersection
from PIL import Image, ImageDraw, ImageFont
def cell(w):
    H = [[s*(i == k) for k in range(3)] + [-0.5] for i in range(3) for s in (1, -1)]
    H += [list(sg) + [-(0.75 - w)] for sg in itertools.product((1, -1), repeat=3)]
    if 0.75 - w <= 0: return None
    try: return HalfspaceIntersection(np.array(H, float), np.zeros(3)).intersections
    except Exception: return None
def check(w, n=200000):
    rs = np.random.default_rng(1); P = rs.random((n, 3)); tot = np.zeros(n, int)
    for cen, ww in ((np.zeros(3), w), (np.full(3, .5), -w)):
        V = cell(ww)
        if V is None or len(V) < 4: continue
        E = ConvexHull(V).equations
        for c in itertools.product(range(-1, 2), repeat=3):
            tot += (((P - cen - c) @ E[:, :3].T + E[:, 3]) <= 1e-9).all(1)
    return (tot == 0).sum(), (tot > 1).sum()
special = [(-0.70, 'cubes, small octahedra'), (0.25 - 0.5**.5, 'regular truncated cubes'), (-0.25, 'cuboctahedra + octahedra'),
           (-0.12, 'factor x'), (0.0, 'Kelvin')]
COL = {'C': (86, 168, 102), 'V': (232, 145, 63)}
th = np.radians(28); ph = np.radians(-22)
R = np.array([[1, 0, 0], [0, np.cos(ph), -np.sin(ph)], [0, np.sin(ph), np.cos(ph)]]) @ np.array([[np.cos(th), 0, np.sin(th)], [0, 1, 0], [-np.sin(th), 0, np.cos(th)]])
Lt = np.array([-.4, .6, .7]); Lt /= np.linalg.norm(Lt)
tiles = []
for w, name in special:
    VC, VV = cell(w), cell(-w)
    vc, vv = ConvexHull(VC).volume, ConvexHull(VV).volume
    gap, dbl = check(w)
    r = 0.75 + w
    print('w=%+.4f %-26s C vol %.5f (1-4r^3/3 %.5f)  V vol %.5f  sum %.5f  corners %d/%d  uncovered %d doubled %d' % (w, name, vc, 1 - 4*r**3/3 if r <= .5 else float('nan'), vv, vc + vv, len(ConvexHull(VC).vertices), len(ConvexHull(VV).vertices), gap, dbl))
    ps = [{'V': VC, 'name': 'C'}] + [{'V': VV + np.array(s)*.5, 'name': 'V'} for s in itertools.product((1, -1), repeat=3) if s[0] > 0 or s[1] > 0 or s[2] < 0]
    im = draw_solids(ps, 520, R, COL, Lt)
    d = ImageDraw.Draw(im); f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 22)
    d.text((14, 12), name, fill=(40, 40, 40), font=f); tiles.append(im)
strip = Image.new('RGB', (520*len(tiles), 520), 'white')
for i, t in enumerate(tiles): strip.paste(t, (520*i, 0))
d = ImageDraw.Draw(strip); d.text((strip.width - 110, 492), 'DICTO', fill=(120, 120, 120), font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 20))
strip.save('changeover-strip.png'); print('saved changeover-strip.png')
