"""Figures: (1) the primary segmentation on one snapshot (uz 0.1 Mm below the mean tau = 1 height; cells outlined), with the cells
that take part in a swap in the next 10 s filled; (2) persistent swaps per cell lifetime against the time step for every setting.
Usage: figures.py STUDYDIR"""
import sys, os, json, glob, itertools
import numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
S = sys.argv[1]
sys.path.insert(0, f'{S}/scripts'); sys.path.insert(0, f'{S}/../2026-11-15-event-logger/scripts')
import tiles as TL, eventlog as EL
os.makedirs(f'{S}/results/figures', exist_ok=True)
F = np.load(f'{S}/data/bifrost/en024048_hion_uz_dz0.1.npy', mmap_mode='r')
k = 120
a, b = np.asarray(F[k], float), np.asarray(F[k + 1], float)
la = TL.segment(a, 1.5, 0.25, method='thr').astype(np.int64)
lb, par, her, _ = TL.match(la, TL.segment(b, 1.5, 0.25, method='thr'), int(la.max()) + 1)
A = TL.to_tiling(EL.Tiling, la, TL.graph(la), 0.0); B = TL.to_tiling(EL.Tiling, lb, TL.graph(lb), 10.0, par)
A.heirs = {str(x): {str(y): s for y, s in v.items()} for x, v in her.items()}
ev = EL.classify(A, B)
sw = {int(c) for e in ev if e['type'] == 'swap' for c in e['cells']}
sp = {int(c) for e in ev if e['type'] in ('split', 'merge') for c in e['cells']}
edge = (la != np.roll(la, 1, 0)) | (la != np.roll(la, 1, 1))
fig, ax = plt.subplots(1, 2, figsize=(13, 6.5))
dx = 24.0 / la.shape[0]
ext = [0, 24, 0, 24]
ax[0].imshow(a / 1000.0, origin='lower', cmap='gray', extent=ext)
ov = np.zeros(la.shape + (4,))
ov[np.isin(la, list(sw))] = (0.85, 0.2, 0.2, 0.45)
ov[np.isin(la, list(sp))] = (0.2, 0.4, 0.9, 0.45)
ov[edge] = (1.0, 0.85, 0.1, 1.0)
ax[0].imshow(ov, origin='lower', extent=ext)
ax[0].set_title(f'Bifrost en024048_hion, vertical velocity 0.1 Mm below mean tau=1\n{len(np.unique(la))} cells; red: in a swap in the next 10 s, blue: split or merge', fontsize=9)
ax[0].set_xlabel('Mm'); ax[0].set_ylabel('Mm')
for f in sorted(glob.glob(f'{S}/results/census/*.json')):
    R = json.load(open(f)); tag = os.path.basename(f)[:-5]
    st = sorted(R['steps'], key=int)
    x = [R['steps'][s]['dt_s'] for s in st]; y = [R['steps'][s]['swaps_per_cell_lifetime'] for s in st]
    ls = '-' if tag.startswith('en_uz0.1') else ('--' if tag.startswith('qs') else ':')
    ax[1].plot(x, y, ls, marker='o', ms=3, label=tag)
ax[1].set_xscale('log', base=2); ax[1].set_xlabel('time step (s)'); ax[1].set_ylabel('persistent swaps per cell lifetime')
ax[1].set_title('Step dependence: every setting', fontsize=9); ax[1].legend(fontsize=6, ncol=2); ax[1].grid(alpha=0.3)
fig.text(0.99, 0.01, 'DICTO', ha='right', va='bottom', fontsize=8, color='0.4')
plt.tight_layout(); plt.savefig(f'{S}/results/figures/sun_swaps.png', dpi=110)
print('FIG_OK', len(sw), len(sp))
