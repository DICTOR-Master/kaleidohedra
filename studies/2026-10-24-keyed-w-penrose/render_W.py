# Pictures of the keyed W (Penrose rhomb lines as ridges / grooves): alone from two sides, and with its neighbour across face 1 (pulled apart).
import numpy as np, json, os
from PIL import Image, ImageDraw, ImageFont
H = os.path.dirname(os.path.abspath(__file__)); V = np.load(os.path.join(H, 'keyedW-V.npy')); F = np.load(os.path.join(H, 'keyedW-F.npy'))
G = json.load(open(os.path.join(H, 'keyed-W-geometry.json'))); N1 = np.array(G['frame']['N'])
g = lambda X: X[..., [1, 2, 0]]
def rot(a, b):
    Ry = np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]]); Rx = np.array([[1, 0, 0], [0, np.cos(b), -np.sin(b)], [0, np.sin(b), np.cos(b)]]); return Rx @ Ry
def draw(parts, R, size, title, Lt=np.array([-.35, .55, .75])):
    Lt = Lt / np.linalg.norm(Lt); im = Image.new('RGB', (size, size), (246, 244, 239)); d = ImageDraw.Draw(im)
    P = np.vstack([p[0] for p in parts]); c0 = P.mean(0); r = np.max(np.linalg.norm(P - c0, axis=1)); polys = []
    for Vx, col in parts:
        W = (Vx - c0) @ R.T
        for f in F:
            a, b, c = W[f]; n = np.cross(b - a, c - a); nn = np.linalg.norm(n)
            if nn < 1e-12 or n[2] <= 0: continue
            n /= nn; sh = .42 + .58 * max(0, n @ Lt)
            polys.append(((a[2] + b[2] + c[2]) / 3, [(size / 2 + q[0] / r * size * .44, size / 2 - q[1] / r * size * .44) for q in (a, b, c)], tuple(int(x * sh) for x in col)))
    for z, pts, cl in sorted(polys, key=lambda x: x[0]): d.polygon(pts, fill=cl, outline=cl)
    d.text((14, 10), title, fill=(31, 36, 48), font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 20)); return im
GOLD, BLUE = (217, 169, 60), (120, 160, 210)
a = draw([(V, GOLD)], rot(0.7, -0.55), 640, 'Keyed W: ridges on its raised faces')
b = draw([(V, GOLD)], rot(0.7 + np.pi, 0.55), 640, 'another view: W has raised faces at both ends')
c = draw([(V - 0.18 * N1, GOLD), (g(V) + 0.18 * N1, BLUE)], rot(1.25, -0.35), 640, 'with its neighbour, pulled apart: ridges meet grooves')
sheet = Image.new('RGB', (1960, 720), (246, 244, 239)); [sheet.paste(t, (10 + i * 650, 10)) for i, t in enumerate((a, b, c))]
d = ImageDraw.Draw(sheet); f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 18)
d.text((20, 670), 'Option 2: the Penrose rhomb pattern (picture A) as lines; every W the same; ridge height about 1 mm at print scale, walls 30°', font=f, fill=(107, 114, 128))
d.text((1860, 690), 'DICTO', font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 20), fill=(150, 150, 150))
sheet.save('/home/dicto/Documents/papers-to-read/keyed-w-penrose-lines.png'); print('saved')
