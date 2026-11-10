"""#61 chamber map (DICTO 10 Nov "draw the chamber map"; "walls could be cell walls"). (s, λ) plane, #61's range
λ-(c) = -1/4 - s/8 <= λ <= U(s) = min(1/3 + s/24, 3s/8). Cells from the Hopscotch walk: clash below -9s/8; linear shift between -9s/8
and -(4-s)/24 (s > 1/7); cubic shift up to -5s/8; Swap Rule holds above -5s/8 (inner wall -s/8). s >= 1/4: #61 Theorem 2 (holds)."""
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
s = np.linspace(0.10, 0.40, 2001)
lo = -0.25 - s / 8; U = np.minimum(1 / 3 + s / 24, 3 * s / 8)
w9, w5, w1, wq = -9 * s / 8, -5 * s / 8, -s / 8, -(4 - s) / 24
fig, ax = plt.subplots(figsize=(9, 6.4), dpi=170)
below = s < 0.25
C = dict(clash='#c9b8b4', lin='#e8c15a', cub='#e08a3c', holds='#8cc79a', thm='#b9dcc2')
ax.fill_between(s[below], lo[below], np.minimum(w9, 0)[below], color=C['clash'], lw=0)
m = below & (s > 1 / 7); ax.fill_between(s[m], w9[m], wq[m], color=C['lin'], lw=0)
top_lin = np.maximum(w9, wq); ax.fill_between(s[below], top_lin[below], w5[below], where=(w5 > top_lin)[below], color=C['cub'], lw=0)
ax.fill_between(s[below], w5[below], U[below], color=C['holds'], lw=0)
ax.fill_between(s[~below], lo[~below], U[~below], color=C['thm'], lw=0)
for y, lab, st in ((lo, 'λ = −1/4 − s/8  (range)', '-'), (U, 'λ = U(s)  (range)', '-')):
    ax.plot(s, y, color='#333', lw=1.2, ls=st)
for y, lab, msk in ((w9, '−9s/8', below), (w5, '−5s/8', below), (wq, '−(4 − s)/24', below & (s > 1 / 7))):
    ax.plot(s[msk], y[msk], color='#5a3a1a', lw=1.4)
ax.plot(s[below], w1[below], color='#2f6b3c', lw=1.1, ls='--')
ax.axvline(0.25, color='#333', lw=0.8, ls=':'); ax.axvline(1 / 7, color='#777', lw=0.7, ls=':')
for sv in (1 / 8, 1 / 6, 1 / 5, 9 / 40, 6 / 25, 49 / 200):
    for y in (-9 * sv / 8, -5 * sv / 8, -sv / 8) + ((-(4 - sv) / 24,) if sv > 1 / 7 else ()):
        ax.plot(sv, y, 'o', ms=3.4, color='#111')
ax.plot([0.25, 0.25], [-9 / 32, -5 / 32], 'o', ms=5, mfc='white', mec='#111')
txt = dict(fontsize=9.5, family='serif')
ax.text(0.155, -0.262, 'four-layer keys clash', **txt); ax.text(0.193, -0.186, 'linear shift', **txt); ax.text(0.172, -0.138, 'cubic shift', **txt)
ax.text(0.15, 0.0, 'Swap Rule holds', **txt); ax.text(0.30, -0.06, '#61 Theorem 2:\nSwap Rule holds\n(proved)', **txt)
for x, y, t in ((0.105, -9 * 0.105 / 8 - 0.004, 'λ = −9s/8'), (0.105, -5 * 0.105 / 8 - 0.006, 'λ = −5s/8'), (0.105, -0.105 / 8 + 0.004, 'λ = −s/8'),
                (0.205, -(4 - 0.205) / 24 + 0.004, 'λ = −(4 − s)/24'), (0.33, -0.25 - 0.33 / 8 - 0.012, 'λ = −1/4 − s/8'), (0.105, 3 * 0.105 / 8 + 0.006, 'λ = 3s/8')):
    ax.text(x, y, t, fontsize=8, color='#3a2a1a', family='serif')
ax.text(0.143, 0.115, 's = 1/7', fontsize=8, color='#555', ha='center'); ax.text(0.25, 0.155, 's = 1/4', fontsize=8, color='#333', ha='center')
ax.set_xlim(0.10, 0.40); ax.set_ylim(-0.31, 0.17); ax.set_xlabel('s  (layer spacing)', family='serif'); ax.set_ylabel('λ  (weight of the tetrahedral holes)', family='serif')
ax.set_title('#61, the Swap Rule below s = 1/4: the chamber map', family='serif', fontsize=12)
fig.text(0.5, 0.012, 'Dots: walls found exactly by the Hopscotch walk at s = 1/8, 1/6, 1/5, 9/40, 6/25, 49/200; lines through them fitted. '
         'All cells close at s = 1/4.', ha='center', fontsize=7.6, family='serif', color='#444')
ax.text(0.396, 0.158, 'DICTO', ha='right', va='top', fontsize=8, color='#777')
for sp_ in ax.spines.values(): sp_.set_linewidth(0.6)
plt.tight_layout(rect=(0, 0.03, 1, 1)); plt.savefig('chamber-map-61.png'); print('FINAL ok')
