# The chosen small stack (DICTO 2026-10-31): two strings side by side of the 4H stacking ABCB, layers 0-2 (types h c h,
# positions A B C), at lambda = -1/8. Exact: which parts are joined over area, every shared wall (built once), ring and
# zip-tie totals, lowest points. Drawings: layer-by-layer assembly (tiles drawn apart by layer, book colours: c gold,
# h blue, tetrahedral pieces darker, octahedron halves lighter; layer letters A/B/C) and a ring mock-up (three-quarter and
# side view, style of mockup.py).
# Usage (dicto-big-brother): TILES_DIR=~/kres-tmp/endless LOGO=<logo> ~/geom/bin/python stack_build.py
#   -> ../out/stack-build.json, stack-assembly.png, stack-mockup.png, stack-walls.png
import os, sys, json, math
import numpy as np
from fractions import Fraction as Fr
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import build as B, exactfaces as E, stack as S, mockup as MK
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
STRINGS = [(0, 0), (1, 0)]; L0, L1 = 0, 2
COLS = {'c': ('#d9a521', '#e8c25a'), 'h': ('#3f7fc4', '#7fb0e0')}

def build_patch():
    _, offs = S.string(); tiles = []
    for si, o in enumerate(STRINGS):
        for L in range(L0, L1 + 1):
            tiles.append(dict(string=si, L=L, type=S.T[L % 4], pos=S.WORD[L % 4],
                              pieces=S.tile_abs(L, offs[L % 4][0] + o[0], offs[L % 4][1] + o[1])))
    return tiles

if __name__ == '__main__':
    tiles = build_patch(); out = dict(strings=STRINGS, layers=[L0, L1], types=[t['type'] for t in tiles[:L1 - L0 + 1]],
                                      positions=[t['pos'] for t in tiles[:L1 - L0 + 1]])
    g = S.contact_graph([t['pieces'] for t in tiles])
    out['contact'] = dict(parts=g['parts'], joins=g['joins'], pieces=g['components'], min_degree=g['min_degree'])
    name = lambda ti: f"string {tiles[ti]['string'] + 1} layer {tiles[ti]['L']} ({tiles[ti]['pos']}, {tiles[ti]['type']})"
    out['part_joins'] = [[name(g['part_list'][a][0]) + f" part {g['part_list'][a][1]}", name(g['part_list'][b][0]) + f" part {g['part_list'][b][1]}"] for a, b in g['edges']]
    print('contact', out['contact'], flush=True)
    # ring census with shared walls built once
    tri_owner = {}; per_tile = []; faces_of = []
    for ti, t in enumerate(tiles):
        faces = B.split_edges(E.union_faces([p['pts'] for p in t['pieces']])); faces_of.append(faces); n = 0
        for fi, f in enumerate(faces):
            for Tr in B.rings_of(f):
                tri_owner.setdefault(frozenset(Tr), []).append((ti, fi, Tr)); n += 1
        per_tile.append(n)
    walls = Counter()
    for k, own in tri_owner.items():
        assert len(own) <= 2
        if len(own) == 2:
            a, b = sorted(o[0] for o in own); A, Bt = tiles[a], tiles[b]
            kind = 'hexagon between layers' if A['string'] == Bt['string'] else ('side wall, same layer' if A['L'] == Bt['L'] else 'side wall, next layer')
            walls[(name(a), name(b), kind)] += 1
    sides = Counter()
    for k in tri_owner:
        Tr = list(k)
        for i in range(3): sides[frozenset((Tr[i], Tr[(i + 1) % 3]))] += 1
    mult = Counter(sides.values())
    R = len(tri_owner); NS = len(sides)
    out['rings'] = dict(separate_tiles=sum(per_tile), per_tile={name(i): n for i, n in enumerate(per_tile)}, stack=R,
                        saved=sum(per_tile) - R, shared_wall_rings=sum(walls.values()),
                        walls=[[a, b, k, n] for (a, b, k), n in sorted(walls.items())])
    out['ties'] = dict(separate_tiles=3 * sum(per_tile), stack=2 * NS, saved=3 * sum(per_tile) - 2 * NS, ring_sides=NS,
                       rings_meeting_per_side={str(k): v for k, v in sorted(mult.items())})
    zs = [p[2] for t in tiles for p in t['pieces'][0]['pts'] + [q for pc in t['pieces'] for q in pc['pts']]]
    zmin = min(zs); low = sorted({q for t in tiles for pc in t['pieces'] for q in pc['pts'] if q[2] == zmin})
    out['lowest_points'] = dict(z=str(zmin), points=[[str(x) for x in q] for q in low])
    out['height_layers'] = str(max(zs) - zmin)
    print(json.dumps({k: out[k] for k in ('rings', 'ties', 'lowest_points', 'height_layers')}, indent=1, default=str), flush=True)
    json.dump(out, open(os.path.join(B.OUT, 'stack-build.json'), 'w'), indent=1, default=str)

    # ---------- layer-by-layer assembly drawing ----------
    v = B.View(20, -60); D = B.D
    def tris_for(tsel, gap):
        out_t = []; fid = 0; rid = 0
        for ti in tsel:
            t = tiles[ti]; dz = np.array([0, 0, gap * (t['L'] - L0)])
            for f in faces_of[ti]:
                n = B.cnormal(f)
                # colour: tetrahedral piece darker, octahedron half lighter (by which piece holds the face centre region)
                cen = np.mean([B.cart(p) for p in f['loops'][0]], 0)
                for Tr in B.rings_of(f):
                    X = [B.cart(p) + dz for p in Tr]; c = np.mean([B.cart(p) for p in Tr], 0)
                    # which piece owns this ring triangle: the piece whose facet contains its centre
                    ci = tuple(sum(p[i] for p in Tr) / 3 for i in range(3)); col = COLS[t['type']][1]
                    for pc in t['pieces']:
                        if pc['kind'] == 'tet':
                            fs = E.facets(pc['pts'])
                            if all(E.dot(nn, ci) <= cc for nn, cc, q in fs): col = COLS[t['type']][0]
                    out_t.append((X, fid, rid, B.hex2rgb(col), n)); rid += 1
                fid += 1
        return out_t
    allt = list(range(len(tiles)))
    img_a, sc = B.render3d(tris_for(allt, 0.0), v, 1100, 1300)
    img_b, _ = B.render3d(tris_for(allt, 0.75), v, 1100, 1300)
    fig = plt.figure(figsize=(11, 6.8), facecolor='white')
    for k, (img, ttl) in enumerate(((img_b, 'layer by layer (drawn apart)'), (img_a, 'closed'))):
        ax = fig.add_axes([0.13 + k * 0.44, 0.02, 0.42, 0.9]); ax.imshow(np.clip(img, 0, 1)); ax.axis('off'); ax.set_title(ttl, fontsize=11, color='#333')
    # layer labels in the left margin, level with each layer of the drawn-apart view
    for L in range(L0, L1 + 1):
        t = [tt for tt in tiles if tt['L'] == L][0]
        fig.text(0.01, 0.02 + 0.9 * (1 - (0.75 - 0.27 * (L - L0))), f"layer {L}\n{t['pos']}  {t['type']}-tiles", fontsize=11, weight='bold',
                 color=COLS[t['type']][0], family='DejaVu Sans Mono', va='center')
    MK.logo(fig, 0.93, 0.06)
    fig.savefig(os.path.join(B.OUT, 'stack-assembly.png'), dpi=200, facecolor='white'); plt.close(fig)

    # ---------- ring mock-up of the stack ----------
    rings, bars = [], []
    ties = {}
    for ti, t in enumerate(tiles):
        for f in faces_of[ti]:
            n = B.cnormal(f)
            for Tr in B.rings_of(f):
                k = frozenset(Tr)
                if tri_owner[k][0][0] != ti: continue       # shared wall: draw once
                X = [B.cart(p) for p in Tr]; o, i = MK.ring_band(X); c = np.mean(X, 0)
                rings.append(dict(outer=o, inner=i, n=n, c=c, type=t['type']))
                for kk in range(3):
                    for s in (.25, .75):
                        p = X[kk] + (X[(kk + 1) % 3] - X[kk]) * s
                        ties.setdefault(tuple(np.round(p, 6)), []).append((c, n))
    for p, cs in ties.items():
        p = np.array(p); nb = sum(n for c, n in cs)
        for c, n in cs: bars.append((np.array([p + (c - p) / np.linalg.norm(c - p) * 0.07, p]), nb))
    def draw_stack(ax, view, title):
        items = [(float(view.proj(r['c'])[0, 2]), 'ring', r) for r in rings] + [(float(view.proj(b[0][1])[0, 2]) - 0.01, 'bar', b) for b in bars]
        items.sort(key=lambda x: -x[0])
        from matplotlib.patches import PathPatch
        from matplotlib.path import Path
        for d, kind, obj in items:
            if kind == 'ring':
                tint, edge = MK.TINT[obj['type']], MK.EDGE[obj['type']]; front = float(obj['n'] @ view.f) < 0
                o = view.proj(obj['outer'])[:, :2]; i = view.proj(obj['inner'])[:, :2][::-1]
                path = Path(np.vstack([o, o[:1], i, i[:1]]), [Path.MOVETO] + [Path.LINETO] * (len(o) - 1) + [Path.CLOSEPOLY]
                            + [Path.MOVETO] + [Path.LINETO] * (len(i) - 1) + [Path.CLOSEPOLY])
                nn = obj['n'] if front else -obj['n']
                sh = 0.62 + 0.30 * max(0.0, float(nn @ view.L1)) + 0.12 * max(0.0, float(nn @ view.L2))
                col = np.clip((0.55 + 0.45 * tint) * sh + (0.08 if front else 0.18), 0, 1)
                ax.add_patch(PathPatch(path, facecolor=(*col, 0.78 if front else 0.42), edgecolor=(*(edge if front else 0.5 * edge + 0.5), 1.0 if front else 0.55),
                                       lw=0.9 if front else 0.55, zorder=2))
            else:
                q = view.proj(obj[0])[:, :2]; front = float(obj[1] @ view.f) < 0
                ax.plot(q[:, 0], q[:, 1], color='#1a1a1a' if front else '#a8a8a8', lw=1.1 if front else 0.6, solid_capstyle='round', zorder=3)
        P = view.proj(np.vstack([r['outer'] for r in rings]))[:, :2]; lo, hi = P.min(0), P.max(0); pad = 0.05 * max(hi - lo)
        ax.set_xlim(lo[0] - pad, hi[0] + pad); ax.set_ylim(lo[1] - pad, hi[1] + pad); ax.set_aspect('equal'); ax.axis('off')
        ax.set_title(title, fontsize=12, color='#333')
    BG = '#f4f4f2'
    fig = plt.figure(figsize=(16, 10), facecolor=BG)
    draw_stack(fig.add_axes([0.01, 0.04, 0.55, 0.86]), MK.View(22, -58), 'three-quarter view')
    draw_stack(fig.add_axes([0.57, 0.04, 0.42, 0.86]), MK.View(0.5, -90), 'side view')
    fig.suptitle(f"HexOct ring stack · λ = −1/8 · two strings of h c h (layers A B C of 4H) · {R} rings · {2 * NS} zip ties",
                 fontsize=14, color='#222', y=0.975)
    MK.logo(fig, 0.94, 0.05)
    fig.savefig(os.path.join(B.OUT, 'stack-mockup.png'), dpi=160, facecolor=BG); plt.close(fig); print('saved drawings', flush=True)
