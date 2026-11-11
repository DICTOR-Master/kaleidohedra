# render_angeli_levels.py, DICTO 11 Nov 2026 ("render the twin hull Angeli for levels 2 and 3"). The Angelus (Vacuus of the twin hull)
# at given levels of the OG family: twin hull from the exact corners of D_k (sqrt5 -> -sqrt5), fins O-A-B for every hull edge AB,
# coloured by the plane through O they lie in (sheets), with a translucent ghost of the twin hull. #87 census renderer (own z-buffer,
# 3x supersampled, edges >= 2 px). Usage: render_angeli_levels.py <five-fold-octet dir> <render.py> <logo> <out.png> <k> [<k> ...]
import sys, os, numpy as np
D, RENDER, LOGO, OUTP = sys.argv[1:5]; LEVELS = [int(x) for x in sys.argv[5:]]
here = os.path.expanduser('~/k-research/studies/2026-11-09-og-margin/scripts')
sys.argv = [sys.argv[0], D, '0', '/dev/null']; exec(open(os.path.join(here, 'exact_family.py')).read().split("t0 = time.time()")[0])
cwd = os.getcwd(); sys.argv = ['x', '.', '.', LOGO]; exec(open(RENDER).read().split('def plate(')[0]); os.chdir(cwd)
from scipy.spatial import ConvexHull
from PIL import Image, ImageDraw, ImageFont
NAMES = {2: 'level 2: regular icosahedron', 3: 'level 3: regular dodecahedron'}
def twinf(x):
    re = float(x.a) + float(x.b) * S5
    return float(x.a) - float(x.b) * S5 if abs(re) < 1e-6 or x.b == 0 else float(x.a * x.a - 5 * x.b * x.b) / re
os.chdir(D); W = [tuple(cv(x) for x in v) for v in OG]; panels = []
for k in range(max(LEVELS) + 1):
    idx = {v: i for i, v in enumerate(W)}; Wfx = np.array([fl(v) for v in W]); F, ne, _ = exact_faces(W, idx, Wfx)
    if k in LEVELS:
        cor = sorted(set(i for mem in F for i in mem)); T = np.array([[twinf(x) for x in W[i]] for i in cor]); T /= np.linalg.norm(T, axis=1).max()
        h = ConvexHull(T); hv = h.vertices; T = T[hv]; h = ConvexHull(T)
        En = h.equations; n = len(En); par = list(range(n))
        def find(i):
            while par[i] != i: par[i] = par[par[i]]; i = par[i]
            return i
        for f in range(n):
            for g in h.neighbors[f]:
                if np.abs(En[f] - En[g]).max() < 1e-9: par[find(f)] = find(g)
        grp = {}
        for f in range(n): grp.setdefault(find(f), set()).update(h.simplices[f].tolist())
        faces = []
        for pts in grp.values():
            ii = np.array(sorted(pts)); Q = T[ii]; c0 = Q.mean(0); B = np.linalg.svd(Q - c0)[2][:2]; q = (Q - c0) @ B.T
            faces.append(list(ii[np.argsort(np.arctan2(q[:, 1], q[:, 0]))]))
        E = sorted({(min(a, b), max(a, b)) for f in faces for a, b in zip(f, f[1:] + f[:1])})
        planes = {}
        for i, (a, b) in enumerate(E):
            nn = np.cross(T[a], T[b]); nn /= np.linalg.norm(nn); nn *= np.sign(nn[np.argmax(np.abs(nn) > 1e-9)]); planes.setdefault(tuple(np.round(nn, 7)), []).append(i)
        pidx = {i: j for j, ids in enumerate(planes.values()) for i in ids}
        apex = sorted(set(round(float(np.degrees(np.arccos(T[a] @ T[b] / (np.linalg.norm(T[a]) * np.linalg.norm(T[b]))))), 4) for a, b in E))
        M = rot(20, 24); Wv = T @ M.T; lim = 1.08; O = np.zeros(3); C = Canvas(lim)
        for i, (a, b) in enumerate(E):
            tri = np.array([O, Wv[a], Wv[b]]); C.tri(tri, shade(rgb(PAL[pidx[i] % len(PAL)]), np.cross(tri[1], tri[2])), i)
        NF = []
        for f in faces:
            nv = np.zeros(3)
            for j in range(len(f)): nv += np.cross(Wv[f[j]], Wv[f[(j + 1) % len(f)]])
            NF.append(nv)
        C.outlines(); C.ghost(Wv, faces, NF, 0.10)
        panels.append((C.image(), f'{NAMES.get(k, f"level {k}")}', f'{len(E)} fins, {len(planes)} fin planes, apex {apex}°'))
        print(f'k {k}: corners {len(T)}, faces {len(faces)}, edges {len(E)}, fin planes {len(planes)}, apex {apex}', flush=True)
    feet = {}
    for n_, d_, _ in F.values():
        s_ = d_ / dot(n_, n_); feet[tuple(s_ * x for x in n_)] = 1
    W = list(feet)
os.chdir(cwd)
im = Image.new('RGB', (len(panels) * (PX + 40) - 40, PX + 120), 'white'); dr = ImageDraw.Draw(im)
try: ft = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 30); fs = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 20)
except Exception: ft = fs = ImageFont.load_default()
dr.text((24, 12), 'Angeli of the OG family: the twin hull Vacuus at levels ' + ', '.join(map(str, LEVELS)), fill=(30, 30, 40), font=ft)
for j, (img, t1, t2) in enumerate(panels):
    x = j * (PX + 40); im.paste(img, (x, 110)); dr.text((x + 24, 52), t1, fill=(50, 50, 60), font=fs); dr.text((x + 24, 78), t2, fill=(100, 100, 110), font=fs)
lg = Image.open(LOGO).convert('RGBA'); hh = 70; lg = lg.resize((int(lg.width * hh / lg.height), hh)); im.paste(lg, (im.width - lg.width - 8, im.height - hh - 8), lg)
dr.text((24, im.height - 34), 'DICTO · dictospheres.com · fins coloured by their plane through the centre · twin = √5 → −√5', fill=(120, 110, 90), font=fs)
im.save(os.path.abspath(OUTP), dpi=(300, 300)); print('FINAL ok')
