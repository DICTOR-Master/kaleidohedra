# #72 figure: (a) volume per formula unit of BaRuO3 (measured, Jin et al.) and BaMnO3 (DFT AFM, Chen and Millis) against h;
# (b) LiCoO2 interlayer distance per CoO2 layer (measured, Motohashi et al.) against the share of O1-type gaps.
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt, numpy as np, os
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9})
fig, (a, b) = plt.subplots(1, 2, figsize=(7.4, 3.0), dpi=200)
RU = {'3C': (0, 64.28), '6H': (1/3, 65.88), '4H': (1/2, 67.51), '9R': (2/3, 68.91)}
x = np.linspace(0, 1, 2)
xr = np.array([0, 0.72]); a.plot(xr, 64.25 + 6.82*xr, color='#b8962e', lw=1.6, label='BaRuO$_3$ law line (measured)')
for k, (h, v) in RU.items():
    a.plot(h, v, 'o', color='#b8962e', ms=5, mec='white', mew=0.8, alpha=0.55 if k == '6H' else 1)
    a.annotate(k, (h, v), textcoords='offset points', xytext=(-6, 6), fontsize=7)
MN = {'3C': (0, 61.9), '4H': (1/2, 66.1), '2H': (1, 71.0)}
a.plot([0, 1], [61.9, 71.0], color='#3a6ea5', lw=1.6, ls='--', label='BaMnO$_3$ line 3C → 2H (DFT)')
for k, (h, v) in MN.items():
    a.plot(h, v, 's', color='#3a6ea5', ms=5, mec='white', mew=0.8); a.annotate(k, (h, v), textcoords='offset points', xytext=(5, -10), fontsize=7)
a.set_xlabel('hexagonality h'); a.set_ylabel('volume, Å$^3$ per ABO$_3$'); a.set_xlim(-0.05, 1.1)
a.set_title('(a) Hexagonal perovskites', fontsize=9, loc='left'); a.legend(fontsize=6.8, frameon=False, loc='upper left')
b.plot([0, 1], [4.81, 4.24], color='#b8962e', lw=1.6, label='law line O3 → O1')
for k, (h, d, mk) in {'O3, x = 0.35': (0, 4.81, 'o'), 'H1-3, x = 0.12': (1/2, 4.52, 'o'), 'O1, x = 0': (1, 4.24, 'o')}.items():
    b.plot(h, d, mk, color='#3a6ea5', ms=5, mec='white', mew=0.8); b.annotate(k, (h, d), textcoords='offset points', xytext=(6, 3) if h < 1 else (-58, 6), fontsize=7)
b.plot(0, 4.68, 'o', mfc='white', mec='#3a6ea5', ms=5); b.annotate('O3, x = 1', (0, 4.68), textcoords='offset points', xytext=(6, -10), fontsize=7)
b.set_xlabel('share of O1-type gaps (h)'); b.set_ylabel('Å per CoO$_2$ layer'); b.set_xlim(-0.05, 1.1)
b.set_title('(b) Li$_x$CoO$_2$ on charge', fontsize=9, loc='left'); b.legend(fontsize=6.8, frameon=False, loc='upper right')
for ax in (a, b): ax.spines[['top', 'right']].set_visible(False); ax.grid(alpha=0.25, lw=0.5)
fig.tight_layout(); fig.savefig(os.path.expanduser('~/kres-tmp/oxides.png')); print('ok')
