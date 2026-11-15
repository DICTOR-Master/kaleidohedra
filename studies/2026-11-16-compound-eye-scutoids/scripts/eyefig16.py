#!/usr/bin/env python3
"""Figures for the gw16 trace (small, low-resolution derived views; data: Paukner et al. 2024, BossDB paukner2024).
1 eye-gw16-crosssection.png: one retina segment of one patch (the best-tracked one unless PATCH:SEGTOP is given): planes at its
  top, middle and bottom with the neighbour graph of the trusted columns; pairs that part are drawn by their sorting
  (red true exchange, yellow near-tie, grey artefact).
2 eye-gw16-swapmap.png: (a) counted retina columns and changes on the eye (angles about the cornea sphere centre), patch centres
  shaded by cornea unevenness U; (b) per patch, retina changes against U (bars: U over the 9 fit variants), all flagged changes
  minus the image null and the true exchanges.
Usage: eyefig16.py RUN_DIR FIG_DIR SUM16_JSON [PATCH:SEGTOP]   (SUM16_JSON from eyesum16.py run with the inspection file)"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import eyetrace as et
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt

RUN, FIG, SUMF = sys.argv[1], sys.argv[2], sys.argv[3]; os.makedirs(FIG, exist_ok=True)
S = json.load(open(f'{RUN}/summary.json')); P = [p for p in S['patches'] if 'skip' not in p and p.get('segments')]
SU = json.load(open(SUMF)); CALLS = SU['calls']
E = os.environ.get('EYE_DATA', os.path.expanduser('~/eye-data')) + '/'
OFF = np.array([0.0, 200.0, 100.0]); A_ = np.load(E + 'g16/gw16-sheet.npy'); CEN = A_[0, 6:9] * 4 + 1.5 - OFF
MARK = 'DICTO · dictospheres.com'
COL = {'true': '#e63946', 'near-tie': '#f4c430', 'artefact': '#9a9a9a'}


def mark(fig): fig.text(0.995, 0.008, MARK, ha='right', va='bottom', fontsize=8, color='0.35')


C = np.array([p['top_centre3'] for p in P]); u0 = (C - CEN).mean(0); u0 /= np.linalg.norm(u0)
g1 = np.cross(u0, [1.0, 0, 0]); g1 /= np.linalg.norm(g1); g2 = np.cross(u0, g1)


def ang(v):
    v = np.asarray(v, float) - CEN; v = v / np.linalg.norm(v, axis=-1, keepdims=True)
    t = np.arccos(np.clip(v @ u0, -1, 1)); x, y = v @ g1, v @ g2; r = np.hypot(x, y) + 1e-15
    return np.degrees(np.stack([t * x / r, t * y / r], -1))


def owner(x): return int(np.argmin(np.linalg.norm(C - np.asarray(x), axis=1)))


# ---- figure 1
if len(sys.argv) > 4: pt, s0 = map(int, sys.argv[4].split(':')); p = [q for q in P if q['patch'] == pt][0]; g = [x for x in p['segments'] if x['depth_um'][0] == s0][0]
else:
    p, g = max(((q, x) for q in P for x in q['segments'] if 'skip' not in x and x['layer'] == 'retina'), key=lambda t: t[1]['tracked_share_zone'])
Z = np.load(f"{RUN}/p{p['patch']}_{g['depth_um'][0]}_planes.npz"); sm, inter, lost, per = Z['sm'], Z['inter'], [tuple(e) for e in Z['lost']], float(Z['period'])
K = len(sm); d0, d1 = g['depth_um']
fig, ax = plt.subplots(1, 3, figsize=(12.6, 4.8))
ncall = {'true': 0, 'near-tie': 0, 'artefact': 0}
for i, j in lost: ncall[CALLS.get(f"{p['patch']}:{d0}:{i}-{j}", {}).get('call', 'artefact')] += 1
for a, img, k, title in [(ax[0], Z['top'], 0, f'top, {d0} µm below the cornea'), (ax[1], Z['mid'], K // 2, f'middle, {(d0 + d1) / 2:.0f} µm'),
                         (ax[2], Z['bot'], K - 1, f'bottom, {d1} µm')]:
    et.BANDPASS = True
    z = et.norm_img(np.asarray(img, np.float32), 0.15 * per, 1.2 * per); a.imshow(z, cmap='gray', vmin=-2.5, vmax=2.5, interpolation='bilinear')
    pos = sm[k]; Ed, _ = et.dense_edges(pos, None, per)
    for i, j in Ed:
        if inter[i] and inter[j]: a.plot([pos[i, 1], pos[j, 1]], [pos[i, 0], pos[j, 0]], '-', color='#2ec4d6', lw=0.5)
    for i, j in lost:
        c_ = CALLS.get(f"{p['patch']}:{d0}:{i}-{j}", {}).get('call', 'artefact')
        a.plot([pos[i, 1], pos[j, 1]], [pos[i, 0], pos[j, 0]], '-', color=COL[c_], lw=2.0)
    a.plot(pos[inter, 1], pos[inter, 0], 'o', ms=1.8, color='#7bd389')
    n = img.shape[0]; px = 0.5 * (961 - (d0 + (d1 - d0) * k / max(K - 1, 1))) / (961 - d0)
    a.plot([n * 0.06, n * 0.06 + 20 / px], [n * 0.95] * 2, 'w-', lw=3); a.text(n * 0.06, n * 0.92, '20 µm', color='w', fontsize=8)
    a.set_title(title, fontsize=9); a.set_xticks([]); a.set_yticks([]); a.set_xlim(0, n); a.set_ylim(n, 0)
fig.suptitle(f'Butterfly eye gw16 (Paukner et al. 2024, BossDB), retina, best-tracked patch: {int(inter.sum())} trusted columns, '
             f'{100 * g["tracked_share_zone"]:.0f}% of detections tracked\n{len(lost)} of {g["sm_top"]} neighbour pairs part (image null '
             f'{g["img_null_sm"] * g["sm_top"]:.1f}); sorted by eye: {ncall["true"]} true exchange (red), {ncall["near-tie"]} near-tie (yellow), '
             f'{ncall["artefact"]} artefact (grey)', fontsize=9)
plt.tight_layout(rect=(0, 0.03, 1, 0.90)); mark(fig); fig.savefig(f'{FIG}/eye-gw16-crosssection.png', dpi=72); plt.close(fig)
print('figure 1 patch', p['patch'], 'segment', g['depth_um'], ncall)

# ---- figure 2
fig, ax = plt.subplots(1, 2, figsize=(12.4, 5.6), gridspec_kw=dict(width_ratios=[1.25, 1]))
Us = [(q.get('cornea') or {}).get('U') for q in P]; vmax = max([u for u in Us if u is not None] + [0.3]); cmap = plt.get_cmap('Purples')
for q, u in zip(P, Us):
    a_ = ang(q['top_centre3']); ax[0].plot(a_[1], a_[0], 'h', ms=34, color=cmap(0.15 + 0.7 * (u or 0) / vmax), alpha=0.55, mec='none', zorder=0)
cells, pts = [], {'true': [], 'near-tie': [], 'artefact': []}
for i, q in enumerate(P):
    for g in q['segments']:
        if 'skip' in g or g['layer'] != 'retina': continue
        cells += [c for c in g['cells3'] if owner(c) == i]
        for s in g['swap3']:
            if owner(s[0]) != i: continue
            pts[CALLS.get(f"{q['patch']}:{g['depth_um'][0]}:{s[2][0]}-{s[2][1]}", {}).get('call', 'artefact')].append(ang(s[0]))
if cells: W = ang(np.array(cells)); ax[0].plot(W[:, 1], W[:, 0], '.', ms=1.0, color='0.35', label=f'counted retina columns, all segments ({len(cells)})')
for cl, mk in (('artefact', 'x'), ('near-tie', 'd'), ('true', 'o')):
    if pts[cl]: W = np.array(pts[cl]); ax[0].plot(W[:, 1], W[:, 0], mk, ms=4, color=COL[cl], label=f'{cl} ({len(W)})')
sm_ = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(0, vmax)); cb = plt.colorbar(sm_, ax=ax[0], shrink=0.7)
cb.set_label('cornea unevenness U = (k1 - k2)/(k1 + k2)', fontsize=8)
ax[0].set_xlabel('angle about the cornea sphere centre (deg)'); ax[0].set_ylabel('angle (deg)'); ax[0].set_aspect('equal'); ax[0].legend(fontsize=7, loc='best')
ax[0].set_title('retina neighbour changes (120-340 µm) on the eye; hexagons = patches shaded by U', fontsize=9)
R = [r for r in SU['patch_rows'] if r['layer'] == 'retina']
x = np.array([r['U'] for r in R]); y = np.array([r['excess_share'] * 100 for r in R]); yt = np.array([r['true_share'] * 100 for r in R])
ax[1].errorbar(x, y, xerr=[x - np.array([r['U_min'] for r in R]), np.array([r['U_max'] for r in R]) - x], fmt='o', color='#1d4ed8', ms=4, lw=0.8,
               label='all flagged changes minus image null')
ax[1].plot(x, yt, 'o', mfc='none', mec='#e63946', ms=7, label='true exchanges')
ax[1].axhline(0, color='0.5', lw=0.8); ax[1].set_xlabel('cornea unevenness U (bars: range over 9 fit variants)'); ax[1].set_ylabel('% of neighbour pairs (retina)')
ax[1].legend(fontsize=7); rho = (SU.get('spearman_retina') or {}).get('excess_share_vs_U') or {}
ax[1].set_title(f'per patch, retina: changes minus null vs U (Spearman rho {rho.get("rho", float("nan")):.2f}, p {rho.get("p_two_sided", float("nan")):.2f})', fontsize=9)
fig.suptitle('Butterfly eye gw16, 600 nm X-ray volume: neighbour changes of ommatidial columns along depth', fontsize=10)
plt.tight_layout(rect=(0, 0.03, 1, 0.95)); mark(fig); fig.savefig(f'{FIG}/eye-gw16-swapmap.png', dpi=72); plt.close(fig)
print('figure 2:', {k: len(v) for k, v in pts.items()}, 'cells', len(cells))
