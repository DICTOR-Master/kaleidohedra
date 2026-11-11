# Pictures for the connected HexOct tiles: each chosen pair in three views (c gold, h blue; solid faces, crisp edges, merged
# faces from exactfaces.union_faces) and small stacks 2H (ABAB), 3C (ABC), 4H (ABCB) built from the chosen tiles, 2 x 2 tiles
# per layer, 4 layers, drawn apart vertically so each tile reads (z-buffer renderer of the ring-build study, build.py).
# Usage: LOGO=<dicto-logo.png> python3 render.py -> figs/*.png
import os, sys, math, json
import numpy as np
from fractions import Fraction as Fr
from shapely.geometry import Polygon as SPoly
from shapely.ops import triangulate
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from tiles import tile, types, SYM, image
from stackings import POS
import exactfaces as E
import verify as V
from connect import shift
LOGO = os.environ.get('LOGO', os.path.expanduser('~/work/dicto-logo.png'))
OUT = os.path.join(HERE, 'figs'); os.makedirs(OUT, exist_ok=True)
D = (2 / 3) ** 0.5
def cart(p): return np.array([float(p[0]) + float(p[1]) / 2, float(p[1]) * 3 ** 0.5 / 2, float(p[2]) * D])
COL = {'c': '#d9a521', 'h': '#3f7fc4'}; EDGE = '#1c1c1c'

PAIRS = json.load(open(os.path.join(HERE, 'pairs.json')))

def ref_pieces(pair, t):
    lam = Fr(pair['lam']); w, L = {'c': ('ABC', 1), 'h': ('AB', 0)}[t]
    P = tile(w, L, lam)[0] if pair['split'] == 'RoH' else V.pieces_W(w, L, lam)
    return [shift(p[3], pair['t' + t][i]) for i, p in enumerate(P)]

def chosen_layer(pair, w, L):
    lam = Fr(pair['lam']); mode = pair['split']; T = types(w)
    get = (lambda w, L: tile(w, L, lam)[0]) if mode == 'RoH' else (lambda w, L: V.pieces_W(w, L, lam))
    REF = {'c': get('ABC', 1), 'h': get('AB', 0)}; t = T[L]
    P = get(w, L); RI = image(REF[t], (1, 0, 0, 1), False)
    M = next(M for M in SYM if image(P, M, False) == RI); Mi = V.inv(M); out = []
    for k, up, s, X, J in P:
        Y = sorted(V.f(M, p) for p in X)
        for r, R0 in enumerate(REF[t]):
            R = sorted(R0[3]); g = E.sub(R[0], Y[0])
            if g[2] == 0 and g[0].denominator == 1 and g[1].denominator == 1 and sorted(E.add(p, g) for p in Y) == R: break
        sh = V.lin(Mi, (pair['t' + t][r][0] + g[0], pair['t' + t][r][1] + g[1])); ball = (*POS[w[L]], Fr(L))
        out.append([(p[0] + sh[0] + ball[0], p[1] + sh[1] + ball[1], p[2] + ball[2]) for p in X])
    return t, out

def cnormal(f):
    M = np.array([[1, .5, 0], [0, 3 ** .5 / 2, 0], [0, 0, D]]); nc = np.linalg.inv(M).T @ np.array([float(x) for x in f['n']])
    return nc / np.linalg.norm(nc)

def face_tris(f):
    """triangles of a merged face (outer loop minus holes), Cartesian"""
    L3 = [[cart(p) for p in lp] for lp in f['loops']]; n = cnormal(f)
    o = L3[0][0]; u = L3[0][1] - o; u /= np.linalg.norm(u); v = np.cross(n, u)
    to2 = lambda X: ((X - o) @ u, (X - o) @ v)
    poly = SPoly([to2(X) for X in L3[0]], [[to2(X) for X in h] for h in L3[1:]]).buffer(0)
    out = []
    for T in triangulate(poly):
        if poly.contains(T.representative_point()) and T.area > 1e-12:
            out.append([o + a * u + b * v for a, b in list(T.exterior.coords)[:3]])
    return out, n

def solid_tris(pieces, rgb, fid0, offset=np.zeros(3)):
    faces = E.union_faces(pieces); tris = []
    for i, f in enumerate(faces):
        T, n = face_tris(f)
        for t in T: tris.append(([x + offset for x in t], fid0 + i, fid0 + i, rgb, n))
    return tris, len(faces)

if __name__ == '__main__':
    from build_render import View, render3d, hex2rgb, save_img
    views = [('above', View(22, -58)), ('side', View(2, -20)), ('below', View(-28, 122))]
    for pair in PAIRS:
        key = pair['key']
        for t in 'ch':
            tris, nf = solid_tris(ref_pieces(pair, t), hex2rgb(COL[t]), 0)
            for vn, v in views:
                img, _ = render3d(tris, v, 900, 820, edge_px=2.2, ring_px=0)
                save_img(img, os.path.join(OUT, f'{key}-{t}-{vn}.png'))
        # stacks
        for sname, w in (('2H', 'ABAB'), ('3C', 'ABCABC'), ('4H', 'ABCB')):
            tris = []; fid = 0
            for L in range(4):
                t, pcs = chosen_layer(pair, w, L)
                base = hex2rgb(COL[t]) * (0.92 + 0.08 * (L % 2))
                for a, b in ((0, 0), (1, 0), (0, 1), (1, 1)):
                    P = [[(p[0] + a, p[1] + b, p[2]) for p in X] for X in pcs]
                    tt, nf = solid_tris(P, base, fid, offset=np.array([0, 0, L * 0.55 * D])); tris += tt; fid += nf
            img, _ = render3d(tris, View(14, -62), 900, 1100, edge_px=1.9, ring_px=0)
            save_img(img, os.path.join(OUT, f'{key}-stack-{sname}.png'), label=f'{sname} ({w[:4]}...): ' + ' '.join(types(w)[:4]) + '  (bottom to top)')
        print('done', key, flush=True)
    # composites used by the sheet: figs/pair-<key>-views.png (c above/side/below, then h) and figs/pair-<key>-stacks.png
    from PIL import Image
    for pair in PAIRS:
        k = pair['key']
        for name, files, cols in (('views', [f'{k}-{t}-{v}.png' for t in 'ch' for v in ('above', 'side', 'below')], 3),
                                  ('stacks', [f'{k}-stack-{s}.png' for s in ('2H', '3C', '4H')], 3)):
            ims = [Image.open(os.path.join(OUT, f)).convert('RGB') for f in files]; w, h = ims[0].size
            S = Image.new('RGB', (w * cols, h * ((len(ims) + cols - 1) // cols)), 'white')
            for i, im in enumerate(ims): S.paste(im, ((i % cols) * w, (i // cols) * h))
            S.save(os.path.join(OUT, f'pair-{k}-{name}.png'))
        for f in os.listdir(OUT):
            if f.startswith(k + '-'): os.remove(os.path.join(OUT, f))   # single views are only kept inside the composites
