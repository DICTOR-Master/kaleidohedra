# Plate of the HexOct family for the #86 draft: one row per member (pairs.json), c-tile three views (gold) then h-tile three views
# (blue); thicker edges for print at plate scale. Plus the stack figure: 4H (ABCB) and 2H/3C for the convex member, 4H for the
# ring-weight member. Usage: LOGO=... ~/geom/bin/python plate.py -> figs/family-plate.png, figs/family-stacks.png
import os, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from render import PAIRS, ref_pieces, chosen_layer, solid_tris, COL, OUT, D
from build_render import View, render3d, hex2rgb
from tiles import types
LABEL = {'A': 'λ = 3/8\n(convex)', 'B': 'λ = −1/8\nwhole octahedra', 'C': 'λ = −1/8\n(ring weight)', 'D': 'λ = −11/24', 'E': 'λ = 1/10\n(#75)'}
views = [View(22, -58), View(2, -20), View(-28, 122)]
W, H = 620, 580
fig, axs = plt.subplots(len(PAIRS), 6, figsize=(6 * 1.6, len(PAIRS) * 1.5 + 0.4), dpi=300)
for r, pair in enumerate(PAIRS):
    for t_i, t in enumerate('ch'):
        tris, _ = solid_tris(ref_pieces(pair, t), hex2rgb(COL[t]), 0)
        for v_i, v in enumerate(views):
            img, _ = render3d(tris, v, W, H, edge_px=3.2, ring_px=0)
            ax = axs[r, 3 * t_i + v_i]; ax.imshow(np.clip(img, 0, 1)); ax.set_xticks([]); ax.set_yticks([])
            for s in ax.spines.values(): s.set_visible(False)
    axs[r, 0].set_ylabel(f"{pair['name']}\n{LABEL[pair['name']]}", fontsize=7, rotation=0, ha='right', va='center', labelpad=4)
for c, txt in enumerate(['c-tile, above', 'c-tile, side', 'c-tile, below', 'h-tile, above', 'h-tile, side', 'h-tile, below']):
    axs[0, c].set_title(txt, fontsize=7)
lg = plt.imread(os.environ['LOGO']); la = fig.add_axes([0.01, 0.005, 0.07, 0.07]); la.imshow(lg); la.axis('off')
fig.subplots_adjust(left=0.11, right=0.995, top=0.97, bottom=0.01, wspace=0.02, hspace=0.04)
fig.savefig(os.path.join(OUT, 'family-plate.png'), facecolor='white'); plt.close(fig)

sel = [(PAIRS[0], 'ABAB', '2H'), (PAIRS[0], 'ABCABC', '3C'), (PAIRS[0], 'ABCB', '4H'), (PAIRS[2], 'ABCB', '4H')]
fig, axs = plt.subplots(1, 4, figsize=(9.6, 3.6), dpi=300)
for ax, (pair, w, nm) in zip(axs, sel):
    tris = []; fid = 0
    for L in range(4):
        t, pcs = chosen_layer(pair, w, L); base = hex2rgb(COL[t]) * (0.92 + 0.08 * (L % 2))
        for a, b in ((0, 0), (1, 0), (0, 1), (1, 1)):
            P = [[(p[0] + a, p[1] + b, p[2]) for p in X] for X in pcs]
            tt, nf = solid_tris(P, base, fid, offset=np.array([0, 0, L * 0.55 * D])); tris += tt; fid += nf
    img, _ = render3d(tris, View(14, -62), 700, 900, edge_px=2.6, ring_px=0)
    ax.imshow(np.clip(img, 0, 1)); ax.axis('off')
    ax.set_title(f"{pair['name']} ({LABEL[pair['name']].split(chr(10))[0]}): {nm}, " + ' '.join(types(w)[:4]), fontsize=7)
lg = plt.imread(os.environ['LOGO']); la = fig.add_axes([0.93, 0.01, 0.06, 0.12]); la.imshow(lg); la.axis('off')
fig.subplots_adjust(left=0.005, right=0.995, top=0.93, bottom=0.01, wspace=0.02)
fig.savefig(os.path.join(OUT, 'family-stacks.png'), facecolor='white'); plt.close(fig)
print('plate done', flush=True)
