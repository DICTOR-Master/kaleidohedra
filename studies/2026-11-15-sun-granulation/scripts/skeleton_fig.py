"""Figure for "The skeleton: persistence or reappearance": left, the downflow-lane mask at 0.1 Mm below the mean tau = 1 height
(Bifrost en024048_hion; Carlsson et al. 2016; Gudiksen et al. 2011; Hinode SDC Europe) over a 10-minute window (brightness = share
of the window a pixel is lane), with the corner tracks of that window coloured by their lifetime; right, the lane autocorrelation
at fixed pixels (real and shuffled frames) and the persistence curves S(tau) of corners, corner sites and cells.
Usage: skeleton_fig.py STUDYDIR"""
import sys, os, pickle, json
import numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
S = sys.argv[1]
FE = pickle.load(open(f'{S}/data/skeleton/feat_en024048_hion_dz0.1.pkl', 'rb'))
lanes = np.unpackbits(FE['lanes'])[:np.prod(FE['shape'])].reshape(FE['shape'])
d = json.load(open(f'{S}/results/skeleton/anal/en024048_hion_dz0.1_real_s1.json'))
SM = json.load(open(f'{S}/results/skeleton/summary.json'))['planes']['en/0.1']
C = SM['curves']; x = SM['real/1']
k0, half = 120, 30                     # window frames 90-150 (10 min)
X0, X1 = 0, 252                        # 12 x 12 Mm sub-box (pixels)
occ = lanes[k0 - half:k0 + half].mean(0)[X0:X1, X0:X1]
D_, I_, C_, T_, O_ = [np.array(c) / 255 for c in ((138, 92, 196), (58, 112, 205), (72, 142, 72), (205, 62, 40), (232, 200, 82))]
bg = np.array([0.06, 0.06, 0.08])
img = bg + occ[..., None] * (0.55 * I_ + 0.15 - bg)
cmap = LinearSegmentedColormap.from_list('dicto', [D_, I_, C_, O_, T_])
fig = plt.figure(figsize=(13.0, 7.2), facecolor='#0f0f14')
ax = fig.add_axes([0.07, 0.22, 0.42, 0.68]); ax.set_facecolor('#0f0f14')
dx = 24.0 / FE['shape'][1]
ax.imshow(img, origin='lower', extent=[X0 * dx, X1 * dx, X0 * dx, X1 * dx], interpolation='nearest')
tracks = d['tracks_r3']['corners']
lmax = 1200.0; shown = 0
for t in sorted(tracks, key=len):
    ks = [k for k, _ in t]
    if ks[-1] < k0 - half or ks[0] > k0 + half: continue
    life = len(t) * 10.0
    if life < 60: continue
    P = np.array([p for _, p in t])
    if not ((P[:, 0] >= X0) & (P[:, 0] < X1) & (P[:, 1] >= X0) & (P[:, 1] < X1)).all(): continue
    if np.abs(np.diff(P, axis=0)).max() > 20: continue      # wrap-around jump at the box edge
    c = cmap(min(life, lmax) / lmax)
    ax.plot(P[:, 1] * dx, P[:, 0] * dx, color=c, lw=1.2 if life < 300 else 2.0, alpha=0.95)
    if life >= 300:
        m = P[len(P) // 2]; ax.scatter([m[1] * dx], [m[0] * dx], s=22, color=c, edgecolors='white', linewidths=0.5, zorder=3)
    shown += 1
ax.set_xlim(X0 * dx, X1 * dx); ax.set_ylim(X0 * dx, X1 * dx)
for s_ in ax.spines.values(): s_.set_color('#55555f')
ax.tick_params(colors='#b0b0bb', labelsize=8); ax.set_xlabel('Mm', color='#b0b0bb', fontsize=9); ax.set_ylabel('Mm', color='#b0b0bb', fontsize=9)
cax = fig.add_axes([0.09, 0.075, 0.38, 0.018])
cb = plt.colorbar(plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(0, lmax / 60)), cax=cax, orientation='horizontal')
cb.ax.tick_params(colors='#b0b0bb', labelsize=8); cb.outline.set_edgecolor('#55555f')
cax.set_title('corner track lifetime (min; dot = 5 min or more)', color='#b0b0bb', fontsize=8.5)
fig.text(0.04, 0.94, 'Downflow lanes over 10 min (brighter = lane longer) and the corner tracks, 0.1 Mm below the surface', color='#e6e6ee', fontsize=10.5)
lags = np.array(C['lags']) / 60
m = lanes.reshape(len(lanes), -1).astype(np.float32); an = m - m.mean(1, keepdims=True); sh = m.mean(1) - m.mean()
nl = len(lags)
ac_an = [float((an[:len(an) - l] * an[l:]).mean() / np.sqrt((an[:len(an) - l] ** 2).mean() * (an[l:] ** 2).mean())) for l in range(nl)]
ac_sh = [float((sh[:len(sh) - l] * sh[l:]).mean() / np.sqrt((sh[:len(sh) - l] ** 2).mean() * (sh[l:] ** 2).mean())) for l in range(nl)]
a1 = fig.add_axes([0.6, 0.58, 0.37, 0.32]); a2 = fig.add_axes([0.6, 0.15, 0.37, 0.32])
for a in (a1, a2):
    a.set_facecolor('#15151c')
    for s_ in a.spines.values(): s_.set_color('#55555f')
    a.tick_params(colors='#b0b0bb', labelsize=8); a.grid(color='#2a2a33', lw=0.5)
a1.plot(lags, C['lane_ac'], color=I_, lw=2, label='lane mask at fixed pixels')
a1.plot(lags, ac_an, color=C_, lw=1.6, label='same, box-wide lane share removed')
a1.plot(lags, ac_sh, color=O_, lw=1.0, alpha=0.8, label='box-wide lane share (whole plane)')
if 'lane_ac_shuf' in C: a1.plot(lags, C['lane_ac_shuf'], color='#9a9aa6', lw=1.2, ls='--', label='shuffled frames')
a1.axvline(5, color='#b0b0bb', lw=0.8, ls=':'); a1.text(5.15, -0.95, '5 min', color='#b0b0bb', fontsize=7.5)
a1.set_ylim(-1.0, 1.02); a1.axhline(0, color='#55555f', lw=0.6); a1.set_xlim(0, lags[-1]); a1.set_ylabel('autocorrelation at fixed pixels', color='#b0b0bb', fontsize=8.5)
a1.legend(fontsize=7, loc='upper right', framealpha=0.92, facecolor='#1a1a22', edgecolor='#55555f', labelcolor='#e6e6ee')
a1.set_title('Recurrence at fixed points: autocorrelation over lag', color='#e6e6ee', fontsize=9.5)
L = lambda v: np.array(v[:len(lags)])
a2.plot(lags[:len(C['corner_S'])], C['corner_S'], color=T_, lw=2, label='corners (tracked, r = 144 km)')
a2.plot(lags[:len(C['site_S'])], C['site_S'], color=O_, lw=2, label='corner sites (gaps up to 60 s joined)')
a2.plot(lags[:len(C['cell_S'])], C['cell_S'], color=C_, lw=2, label='cells (overlap rule)')
a2.plot(lags[:len(C['centre_S'])], C['centre_S'], color=D_, lw=1.5, label='cell centres (r = 144 km)')
if 'corner_S_shuf' in C: a2.plot(lags[:len(C['corner_S_shuf'])], C['corner_S_shuf'], color='#9a9aa6', lw=1.2, ls='--', label='corners, shuffled frames')
a2.axhline(0.5, color='#55555f', lw=0.8)
a2.set_ylim(0, 1.02); a2.set_xlim(0, lags[-1]); a2.set_xlabel('lag (min)', color='#b0b0bb', fontsize=9)
a2.set_ylabel('share still present', color='#b0b0bb', fontsize=8.5)
a2.legend(fontsize=7.5, facecolor='#1a1a22', edgecolor='#55555f', labelcolor='#e6e6ee')
a2.set_title('Persistence S(lag)', color='#e6e6ee', fontsize=9.5)
fig.text(0.04, 0.012, 'Vertical velocity of the Bifrost run en024048_hion (Carlsson et al. 2016; Gudiksen et al. 2011; Hinode SDC Europe); 12 x 12 Mm of the 24 Mm box.',
         color='#9a9aa6', fontsize=7.5)
fig.text(0.985, 0.012, 'DICTO · dictospheres.com', ha='right', va='bottom', color='#e6e6ee', fontsize=9)
os.makedirs(f'{S}/results/figures', exist_ok=True)
fig.savefig(f'{S}/results/figures/sun_skeleton.png', dpi=130, facecolor=fig.get_facecolor())
print('FIG tracks shown', shown, 'box-share ac min at', lags[int(np.argmin(ac_sh))], 'min')
print('FINAL ok' if shown > 0 else 'FINAL FAIL')
