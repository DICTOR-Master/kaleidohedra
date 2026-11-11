# render_hidden_fins.py, DICTO 11 Nov 2026 ("render the hidden fins of the twin sweep"). For a hop k, the twin sweep
# P = {(y, lam): X'_j.y - lam <= |X'_j|^2}; walls (2-faces between cells) found by slicing (as twin_sweep4d.py); hidden walls = edges of
# neither the top nor the bottom slice. Render the 3D slice at the slider height where the MOST hidden walls are present: every edge of
# that slice is a wall; its fin = triangle (centre, edge). Hidden fins gold, others light grey; translucent ghost of the slice.
# #87 census renderer (z-buffer, 3x supersampled, edges >= 2 px). Usage: render_hidden_fins.py <ffo dir> <render.py> <logo> <out.png> <k> [<k>]
import sys, os, numpy as np
ARGS = list(sys.argv); OUTP = os.path.abspath(ARGS[4]); LOGO = os.path.abspath(ARGS[3]); RENDER = os.path.abspath(ARGS[2]); LEVELS = [int(x) for x in ARGS[5:]]
here = os.path.expanduser('~/k-research/studies/2026-11-09-og-margin/scripts')
sys.argv = [ARGS[0], ARGS[1], '0', '0', '/dev/null']; exec(open(os.path.join(here, 'og_exchanges.py')).read().split('for k in range(KMAX + 1):')[0])
_keep = dict(faces=faces, symmetrise=symmetrise)
sys.argv = [ARGS[0], ARGS[1], '0', '/dev/null']; exec(open(os.path.join(here, 'exact_family.py')).read().split("t0 = time.time()")[0])
faces, symmetrise = _keep['faces'], _keep['symmetrise']
cwd0 = os.getcwd(); sys.argv = ['x', '.', '.', LOGO]; exec(open(RENDER).read().split('def plate(')[0])
from scipy.spatial import HalfspaceIntersection
from PIL import Image, ImageDraw, ImageFont
def twinf(x):
    re = float(x.a) + float(x.b) * S5
    return float(x.a) - float(x.b) * S5 if abs(re) < 1e-6 or x.b == 0 else float(x.a * x.a - 5 * x.b * x.b) / re
def slice_geom(X, b, lam):
    H = np.hstack([X, -(b + lam)[:, None]]); hs = HalfspaceIntersection(H, np.zeros(3)); P = dedupe(hs.intersections, 1e-10)
    inc = np.abs(X @ P.T - (b + lam)[:, None]) < 1e-9
    return P, inc
panels = []; W = [tuple(cv(x) for x in v) for v in OG]
for k in range(max(LEVELS) + 1):
    idx = {v: i for i, v in enumerate(W)}; Wfx = np.array([fl(v) for v in W]); F, ne, _ = exact_faces(W, idx, Wfx)
    feet = []
    for n_, d_, _ in F.values():
        s_ = d_ / dot(n_, n_); feet.append(tuple(s_ * x for x in n_))
    feet = list(dict.fromkeys(feet))
    if k in LEVELS:
        Wt = np.array([[twinf(x) for x in v] for v in feet]); X = Wt / np.einsum('ij,ij->i', Wt, Wt)[:, None]; X /= np.linalg.norm(X, axis=1).max(); b = np.einsum('ij,ij->i', X, X)
        LAM, toplam = choose_LAM(X, b); ev0 = events(X, b, LAM, TOL)
        lv = np.array(sorted(set(np.round([e[0] for e in ev0], 9)), reverse=True))
        cuts = list((lv[:-1] + lv[1:]) / 2); top = min(LAM * 0.9, max(toplam * 2, toplam + 0.1)); levels = [top] + cuts + [lv[-1] / 2, 0.0]
        adj = [set(tuple(sorted(p)) for p in adjacency(X, b, l)[0]) for l in levels]
        hidden = set().union(*adj) - adj[0] - adj[-1]
        best = max(range(1, len(levels) - 1), key=lambda q: len(adj[q] & hidden)); lam = levels[best]
        P, inc = slice_geom(X, b, lam)
        edges = []
        for (i, j) in adj[best]:
            vv = np.where(inc[i] & inc[j])[0]
            if len(vv) >= 2: edges.append(((i, j), P[vv[0]], P[vv[1]]))
        polys = []
        for i in range(len(X)):
            vv = np.where(inc[i])[0]
            if len(vv) >= 3:
                Q = P[vv]; c0 = Q.mean(0); B = np.linalg.svd(Q - c0)[2][:2]; q = (Q - c0) @ B.T; polys.append(list(vv[np.argsort(np.arctan2(q[:, 1], q[:, 0]))]))
        # centre of the slice: the origin of y-space (the sweep's axis point at this height)
        M = rot(20, 24); Pv = P @ M.T; lim = 1.08 * np.linalg.norm(P, axis=1).max(); O = np.zeros(3); C = Canvas(lim)
        nh = 0
        for t, ((i, j), a, bb) in enumerate(edges):
            tri = np.array([O, a @ M.T, bb @ M.T]); isH = (i, j) in hidden; nh += isH
            C.tri(tri, shade(rgb('#d4af37') if isH else np.array([0.80, 0.80, 0.84]), np.cross(tri[1], tri[2])), t)
        NF = []
        for f in polys:
            nv = np.zeros(3)
            for q in range(len(f)): nv += np.cross(Pv[f[q]], Pv[f[(q + 1) % len(f)]])
            NF.append(nv)
        C.outlines(); C.ghost(Pv, polys, NF, 0.08)
        panels.append((C.image(), f'hop {k}: slice at slider height {lam:.4f} (of {levels[0]:.3f} … 0)', f'{len(edges)} fins in this slice, {nh} of them hidden (gold); {len(hidden)} hidden walls in the whole sweep'))
        print(f'k {k}: lam {lam:.5f}, slice edges {len(edges)}, hidden in slice {nh}, hidden in sweep {len(hidden)}', flush=True)
    W = feet
os.chdir(cwd0)
im = Image.new('RGB', (len(panels) * (PX + 40) - 40, PX + 120), 'white'); dr = ImageDraw.Draw(im)
try: ft = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 30); fs = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 20)
except Exception: ft = fs = ImageFont.load_default()
dr.text((24, 12), 'Hidden fins of the twin sweep: walls that neither end world shows', fill=(30, 30, 40), font=ft)
for j, (img, t1, t2) in enumerate(panels):
    x = j * (PX + 40); im.paste(img, (x, 110)); dr.text((x + 24, 52), t1, fill=(50, 50, 60), font=fs); dr.text((x + 24, 78), t2, fill=(100, 100, 110), font=fs)
lg = Image.open(LOGO).convert('RGBA'); hh = 70; lg = lg.resize((int(lg.width * hh / lg.height), hh)); im.paste(lg, (im.width - lg.width - 8, im.height - hh - 8), lg)
dr.text((24, im.height - 34), 'DICTO · dictospheres.com · 3D slice of the twin hop sweep where most hidden walls are present · twin = √5 → −√5', fill=(120, 110, 90), font=fs)
im.save(OUTP, dpi=(300, 300)); print('FINAL ok')
