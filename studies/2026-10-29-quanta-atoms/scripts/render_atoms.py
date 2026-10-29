# Icons for "All the atoms" (Quanta of Space, DICTO 10-29): every solid with exact geometry in DICTO Solids (dataset v5,
# solids/*.json), drawn the same way: one pose, flat shading, edges only where the surface folds (coplanar triangles merged),
# gold for DICTO's new shapes, silver for known or rediscovered ones. Usage: render_atoms.py <solids dir> <out dir>
import sys, os, json, glob, math, numpy as np
from PIL import Image, ImageDraw
src, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
def rot(ax, a):
    ax = np.array(ax, float); ax /= np.linalg.norm(ax); K = np.array([[0, -ax[2], ax[1]], [ax[2], 0, -ax[0]], [-ax[1], ax[0], 0]])
    return np.eye(3) + math.sin(a) * K + (1 - math.cos(a)) * K @ K
VIEW = rot((1, 0.55, 0.15), 0.85); light = np.array([-0.4, 0.55, 0.75]); light /= np.linalg.norm(light)
N, SS = 420, 3; W = N * SS; GROUND = (20, 15, 11); EDGE = (40, 28, 14)
for f in sorted(glob.glob(os.path.join(src, '*.json'))):
    d = json.load(open(f)); V = np.array([[float(x) for x in v['decimal']] for v in d['vertices']]); F = d['faces']   # polygons
    V = V - V.mean(0); V = V @ VIEW.T; V /= np.abs(V[:, :2]).max(); P = V[:, :2] * (0.44 * W) + W / 2; P[:, 1] = W - P[:, 1]
    def normal(f):   # Newell's method: works for any planar polygon
        q = V[f]; r = np.roll(q, -1, 0); nn = np.array([((q[:, 1] - r[:, 1]) * (q[:, 2] + r[:, 2])).sum(), ((q[:, 2] - r[:, 2]) * (q[:, 0] + r[:, 0])).sum(), ((q[:, 0] - r[:, 0]) * (q[:, 1] + r[:, 1])).sum()])
        return nn / (np.linalg.norm(nn) + 1e-12)
    n = [normal(f) for f in F]; convex = d.get('convex') in (True, 'True')
    new = str(d.get('status', '')).startswith('new')
    base = np.array((217, 165, 33) if new else (196, 198, 208), float)
    img = Image.new('RGB', (W, W), GROUND); dr = ImageDraw.Draw(img)
    for i in sorted(range(len(F)), key=lambda i: V[F[i]][:, 2].mean()):
        if convex and n[i][2] < -1e-9: continue
        b = 0.42 + 0.58 * max(0.0, float(n[i] @ light)) if n[i][2] >= 0 else 0.3
        pts = [tuple(P[k]) for k in F[i]]
        dr.polygon(pts, fill=tuple(int(c * b) for c in base)); dr.line(pts + [pts[0]], fill=EDGE, width=SS)
    img.resize((N, N), Image.LANCZOS).save(os.path.join(out, os.path.basename(f)[:-5] + '.png'))
print('icons', len(glob.glob(os.path.join(out, '*.png'))))
