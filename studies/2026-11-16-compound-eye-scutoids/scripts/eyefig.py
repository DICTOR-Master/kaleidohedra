#!/usr/bin/env python3
"""Figures for the compound-eye scutoid trace (small, low-resolution derived views; data: Paukner et al. 2024, BossDB paukner2024).
1 eye-crosssection.png: cone shell and a retina segment (top and bottom plane) of one patch with the counted neighbour graph;
  red = neighbour pairs lost along depth, yellow dashed = pairs gained.
2 eye-swapmap.png: every counted cell and every neighbour change on the eye surface (angles about the eye centre), patches shaded
  by cornea curvature unevenness U.
Usage: eyefig.py RUN_DIR FIG_DIR TILED_UNITS_JSON [PATCH]   (TILED_UNITS_JSON from eyesum.py: only cells and changes counted
once, in their own patch tile, are drawn)"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import eyeshells as es, eyetrace as et
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

RUN, FIG = sys.argv[1], sys.argv[2]; os.makedirs(FIG, exist_ok=True)
S = json.load(open(f'{RUN}/summary.json')); P = [p for p in S['patches'] if 'skip' not in p]
E = os.environ.get('EYE_DATA', os.path.expanduser('~/eye-data')) + '/'; fr = np.load(E + 'frame_iso.npy'); frame = (fr[:3], fr[3:6], fr[6:])
MARK = 'DICTO · dictospheres.com'


def mark(fig): fig.text(0.995, 0.008, MARK, ha='right', va='bottom', fontsize=8, color='0.35')


def ang(v):
    u0, g1, g2 = frame; v = np.asarray(v, float); v = v / np.linalg.norm(v, axis=-1, keepdims=True)
    t = np.arccos(np.clip(v @ u0, -1, 1)); x, y = v @ g1, v @ g2; r = np.hypot(x, y) + 1e-15
    return np.degrees(np.stack([t * x / r, t * y / r], -1))


# ---- figure 1: choose the patch / retina segment with most lost edges (or the given patch)
best = None
for p in P:
    for g in p.get('retina_segments', []):
        if 'skip' in g: continue
        if (len(sys.argv) > 4 and p['patch'] != int(sys.argv[4])): continue
        sc = g['sm_lost'] - g['img_null_sm'] * g['sm_top']
        if best is None or sc > best[0]: best = (sc, p, g)
_, p, g = best
V = np.load(E + 'gw05-s600.npy', mmap_mode='r'); c, R, uc, f1, f2 = es.patch_axes(p['A'], p['B'])
Sf, path, dirs, ratios, e1s = es.make_fibre_stack(V, c + (R - 300 / 0.6) * uc, -uc, 180, N=500, px_um=0.3)
a0, a1 = g['planes']; per = p['retina_period_px']
r, X, sm, inter, labs, dets = et.run(Sf[a0:a1 + 1], np.arange(a0, a1 + 1) * 1.0, per, None, 'fig', log=lambda *m: None, nullruns=False,
                                     psm=0.15, dark=True, bandpass=True, zthr_=0.0)
used = [set() for _ in range(len(dets))]
dep = np.arange(10, 131, 1.0); Sc, _ = es.make_stack(V, p['A'], p['B'], dep, 400)
rc, Xc, smc, interc, labsc, detsc = et.run(Sc, dep, p['cone_period_px'], None, 'figc', log=lambda *m: None, nullruns=False, window=True)
fig, ax = plt.subplots(1, 3, figsize=(12.6, 4.6))


def panel(a, img, pos, interior, extras, period, lost, gained, title, px_um):
    et.BANDPASS = False
    z = et.norm_img(img, 0.12 * period, 1.2 * period); a.imshow(z, cmap='gray', vmin=-2.5, vmax=2.5, interpolation='bilinear')
    Ed, _ = et.dense_edges(pos, extras, period)
    for i, j in Ed:
        if interior[i] and interior[j]: a.plot([pos[i, 1], pos[j, 1]], [pos[i, 0], pos[j, 0]], '-', color='#2ec4d6', lw=0.7)
    for i, j in lost: a.plot([pos[i, 1], pos[j, 1]], [pos[i, 0], pos[j, 0]], '-', color='#e63946', lw=2.2)
    for i, j in gained: a.plot([pos[i, 1], pos[j, 1]], [pos[i, 0], pos[j, 0]], '--', color='#ffd23f', lw=2.0)
    a.plot(pos[interior, 1], pos[interior, 0], 'o', ms=3, color='#7bd389')
    n = img.shape[0]; a.plot([n * 0.06, n * 0.06 + 20 / px_um], [n * 0.95] * 2, 'w-', lw=3); a.text(n * 0.06, n * 0.92, '20 µm', color='w', fontsize=8)
    a.set_title(title, fontsize=9); a.set_xticks([]); a.set_yticks([]); a.set_xlim(0, n); a.set_ylim(n, 0)


def extras_of(dets_k, pos_k, period):
    d = np.linalg.norm(dets_k[:, None] - pos_k[None], axis=2).min(1); return dets_k[d > 0.3 * period]


kc = 0; k0c = int(round(rc['depth_um'][0] - dep[0]))
panel(ax[0], Sc[k0c], smc[0], interc, extras_of(detsc[0], smc[0], p['cone_period_px']), p['cone_period_px'],
      [tuple(e) for e in rc['smoothed']['lost_edges']], [], f'cone layer, {rc["depth_um"][0]:.0f} µm below the cornea\n'
      f'{int(interc.sum())} cells, {rc["smoothed"]["lost"]} of {rc["smoothed"]["top_edges"]} neighbour pairs change down to {rc["depth_um"][1]:.0f} µm',
      0.001 * (R * 0.6 - rc['depth_um'][0]))
lost = [tuple(e) for e in r['smoothed']['lost_edges']]; gained = [tuple(e) for e in r['smoothed']['gained_edges']]
d0, d1 = g['depth_below_cornea_um']
panel(ax[1], Sf[a0], sm[0], inter, extras_of(dets[0], sm[0], per), per, lost, [], f'retina, top of a 20 µm segment (~{d0:.0f} µm deep)\n'
      f'{int(inter.sum())} tracked cells; red: pairs that part\n(inspection: mostly long edges across missed cells, not trusted)', 0.3)
panel(ax[2], Sf[a1], sm[-1], inter, extras_of(dets[-1], sm[-1], per), per, lost, gained, f'same cells at the bottom (~{d1:.0f} µm deep)\n'
      f'{r["smoothed"]["lost"]} lost / {r["smoothed"]["gained"]} gained of {r["smoothed"]["top_edges"]} pairs', 0.3)
fig.suptitle('Butterfly compound eye (Paukner et al. 2024, BossDB): ommatidia cross-sections with the neighbour graph', fontsize=10)
plt.tight_layout(rect=(0, 0.03, 1, 0.95)); mark(fig); fig.savefig(f'{FIG}/eye-crosssection.png', dpi=80); plt.close(fig)
print('figure 1 patch', p['patch'], 'segment', g['planes'], 'retina lost', r['smoothed']['lost'], 'job value', g['sm_lost'])

# ---- figure 2: swap map on the eye surface
fig, ax = plt.subplots(figsize=(7.2, 6.4))
Us = [q['cornea']['unevenness'] for q in P if q.get('cornea')]; vmax = max(Us) if Us else 1
cmap = plt.get_cmap('Purples')
for q in P:
    if not q.get('cornea'): continue
    ctr = ang(es.patch_axes(q['A'], q['B'])[2])
    ax.add_patch(Rectangle((ctr[1] - 5.7, ctr[0] - 5.7), 11.4, 11.4, color=cmap(0.15 + 0.7 * q['cornea']['unevenness'] / vmax), alpha=0.6, lw=0, zorder=0))
cells, sw_r, sw_c = [], [], []
TU = json.load(open(sys.argv[3])); PT = [q for q in TU['patches'] if 'skip' not in q]
for q in PT:
    for gg in q.get('retina_segments', []):
        if 'skip' in gg: continue
        cells += gg.get('cells_tile', []); sw_r += [ang(np.array(t) - c) for t, _ in gg.get('swap_tile', [])]
    if q.get('cone') and 'swap_tile' in q['cone']:
        sw_c += [ang(np.array(t) - c) for t, _ in q['cone']['swap_tile']]
if cells:
    C = np.degrees(np.array(cells)); ax.plot(C[:, 1], C[:, 0], '.', ms=2.0, color='0.25', label='counted retina cells (top of each 20 µm segment)')
if sw_r:
    W = np.array(sw_r); ax.plot(W[:, 1], W[:, 0], 'o', ms=4, color='#e63946', label=f'retina neighbour changes ({len(W)}; segmentation not trusted)')
if sw_c:
    W = np.array(sw_c); ax.plot(W[:, 1], W[:, 0], 's', ms=5, color='#1d4ed8', label=f'cone-layer neighbour changes ({len(W)})')
sm_ = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(0, vmax)); cb = plt.colorbar(sm_, ax=ax, shrink=0.7)
cb.set_label('cornea curvature unevenness U = (k1 - k2)/(k1 + k2)', fontsize=8)
ax.set_xlabel('angle about the eye centre (deg)'); ax.set_ylabel('angle about the eye centre (deg)'); ax.set_aspect('equal')
ax.legend(fontsize=7, loc='upper left'); ax.set_title('Where ommatidia change neighbours (butterfly eye, 600 nm X-ray volume)\neach square = one patch tile, shaded by cornea curvature unevenness', fontsize=9)
plt.tight_layout(rect=(0, 0.03, 1, 1)); mark(fig); fig.savefig(f'{FIG}/eye-swapmap.png', dpi=80); plt.close(fig)
print('figure 2: retina swaps', len(sw_r), 'cone swaps', len(sw_c), 'cells', len(cells))
