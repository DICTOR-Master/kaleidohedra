"""Figure for "Swaps traced through depth": one depth slice (uz, 0.1 Mm below the mean tau = 1 height, Bifrost en024048_hion,
Carlsson et al. 2016; Gudiksen et al. 2011; Hinode SDC Europe) with its cells in the element colours on a dark ground, and the
persistent swaps of a 10-minute window around it: rings = swaps confirmed at both adjacent depths (0.05 and 0.15 Mm, the counted
'upright' swaps), small grey dots = swaps seen at this depth only. Usage: fig3d.py STUDYDIR"""
import sys, os, pickle, json
import numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
S = sys.argv[1]
sys.path.insert(0, f'{S}/scripts')
import trace3d as T3, tiles as TL
D = f'{S}/data/trace3d'
dz, up, dn = 0.1, 0.05, 0.15
A = pickle.load(open(f'{D}/track_real_dz{dz}_s1.pkl', 'rb'))
Bu = pickle.load(open(f'{D}/track_real_dz{up}_s1.pkl', 'rb')); Bd = pickle.load(open(f'{D}/track_real_dz{dn}_s1.pkl', 'rb'))
Lu = pickle.load(open(f'{D}/link_{up}_{dz}.pkl', 'rb'))['links']; Lu = [{v: k for k, v in L.items()} for L in Lu]
Ld = pickle.load(open(f'{D}/link_{dz}_{dn}.pkl', 'rb'))['links']
cu = T3.confirm(A, Bu, Lu, 30); cd = T3.confirm(A, Bd, Ld, 30)
k0 = 130; win = 30                                  # frame 130 (snapshot 433), swaps within +-5 min
seg = np.load(f'{D}/seg_dz{dz}.npy', mmap_mode='r')
lab = np.asarray(seg[k0]).astype(np.int64)
G = TL.graph(lab); nb = {}
for a, b in G['contacts']: nb.setdefault(a, set()).add(b); nb.setdefault(b, set()).add(a)
COL = np.array([(138, 92, 196), (58, 112, 205), (72, 142, 72), (205, 62, 40), (232, 200, 82)]) / 255.0   # D I C T O
col = {}
for c in sorted(nb, key=lambda c: -len(nb[c])):
    used = {col[x] for x in nb[c] if x in col}
    col[c] = next((i for i in range(5) if i not in used), c % 5)
rgb = np.zeros(lab.shape + (3,))
for c, i in col.items(): rgb[lab == c] = COL[i]
bg = np.array([0.06, 0.06, 0.08])
img = bg + 0.42 * (rgb - bg)
edge = (lab != np.roll(lab, 1, 0)) | (lab != np.roll(lab, 1, 1))
img[edge] = (0.85, 0.85, 0.9)
sel = [i for i, s in enumerate(A['swaps']) if abs(s['q'] - k0) <= win]
upr = [i for i in sel if cu[i]['hit'] is not None and cd[i]['hit'] is not None]
one = [i for i in sel if i not in upr]
fig = plt.figure(figsize=(8.6, 9.2), facecolor='#0f0f14')
ax = fig.add_axes([0.07, 0.15, 0.88, 0.78]); ax.set_facecolor('#0f0f14')
dx = 24.0 / lab.shape[0]
ax.imshow(img, origin='lower', extent=[0, 24, 0, 24], interpolation='nearest')
ax.scatter([A['swaps'][i]['x'] * dx for i in one], [A['swaps'][i]['y'] * dx for i in one], s=10, c='#9a9aa6', alpha=0.8, lw=0,
           label=f'swap at this depth only ({len(one)})')
ax.scatter([A['swaps'][i]['x'] * dx for i in upr], [A['swaps'][i]['y'] * dx for i in upr], s=150, facecolors='none',
           edgecolors='#ffffff', linewidths=2.0, label=f'same swap at 0.05 and 0.15 Mm: counted ({len(upr)})')
ax.set_xlim(0, 24); ax.set_ylim(0, 24)
for s_ in ax.spines.values(): s_.set_color('#55555f')
ax.tick_params(colors='#b0b0bb', labelsize=8); ax.set_xlabel('Mm', color='#b0b0bb', fontsize=9); ax.set_ylabel('Mm', color='#b0b0bb', fontsize=9)
leg = fig.legend(loc='lower left', bbox_to_anchor=(0.06, 0.055), ncol=2, fontsize=8.5, facecolor='#1a1a22', edgecolor='#55555f', labelcolor='#e6e6ee', framealpha=0.9)
fig.text(0.04, 0.955, f'Granules as upflow cells 0.1 Mm below the surface ({len(np.unique(lab))} cells), swaps of the 10 min around this frame',
         color='#e6e6ee', fontsize=10.5)
fig.text(0.06, 0.012, 'Vertical velocity of the Bifrost run en024048_hion (Carlsson et al. 2016; Hinode SDC Europe).\n'
         'Cells coloured in the five element colours; walls in light grey.', color='#9a9aa6', fontsize=8)
fig.text(0.96, 0.012, 'DICTO · dictospheres.com', ha='right', va='bottom', color='#e6e6ee', fontsize=9)
os.makedirs(f'{S}/results/figures', exist_ok=True)
fig.savefig(f'{S}/results/figures/sun_3d_trace.png', dpi=130, facecolor=fig.get_facecolor())
print('FIG', len(sel), len(upr), len(one))
print('FINAL ok' if len(sel) > 0 else 'FINAL FAIL')
