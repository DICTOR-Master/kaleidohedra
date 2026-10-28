# #71 figure: (a) hydrogen sites per metal atom against hexagonality (hydrogen_sites.out, exact), (b) iron polytype energies
# (Tsumuraya et al., non-magnetic DFT) against the law's straight line through 3C and 2H.
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt, numpy as np
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9})
fig, (a, b) = plt.subplots(1, 2, figsize=(7.4, 3.0), dpi=200)
H = [0, 1, 1/2, 1/3, 3/5, 5/7]; NM = ['3C', '2H', '4H', '6H', 'Mg 10H', 'Mg 14H']; x = np.linspace(0, 1, 2)
for f, lab, col in ((lambda h: 2 - h, 'usable tetrahedral sites  2 − h', '#b8962e'), (lambda h: h, 'face-sharing pairs  h', '#3a6ea5'),
                    (lambda h: 1 + 0*h, 'octahedral sites  1', '#7a7a7a')):
    a.plot(x, f(x), color=col, lw=1.6, label=lab); a.plot(H, [f(h) for h in H], 'o', color=col, ms=4.5, mec='white', mew=0.8)
for h, n in zip(H, NM): a.annotate(n, (h, 2 - h), textcoords='offset points', xytext=(0, 6), ha='center', fontsize=6.5, color='#555')
a.set_xlabel('hexagonality h'); a.set_ylabel('per metal atom'); a.set_ylim(0, 2.35); a.set_xlim(-0.05, 1.05)
a.set_title('(a) Hydrogen sites: exact on every stacking', fontsize=9, loc='left'); a.legend(fontsize=6.8, frameon=False, loc='upper right')
FE = {'3C': (0, 106), '6H₁': (1/3, 80), '4H': (1/2, 82), '10H': (3/5, 60), '6H₂': (2/3, 59), '2H': (1, 27)}
b.plot([0, 1], [106, 27], color='#b8962e', lw=1.6, label='law: straight line 3C → 2H')
for k, (h, e) in FE.items():
    b.plot(h, e, 'o', color='#3a6ea5', ms=5, mec='white', mew=0.8); b.annotate(k, (h, e), textcoords='offset points', xytext=(4, -11) if k == '6H₂' else (-22, 3) if k == '10H' else (6, 2), fontsize=7)
b.set_xlabel('hexagonality h'); b.set_ylabel('energy, meV per atom'); b.set_xlim(-0.05, 1.12)
b.set_title('(b) Iron: close to the law, 4H above it', fontsize=9, loc='left'); b.legend(fontsize=6.8, frameon=False, loc='upper right')
for ax in (a, b):
    ax.spines[['top', 'right']].set_visible(False); ax.grid(alpha=0.25, lw=0.5)
fig.tight_layout(); import os; os.makedirs(os.path.expanduser('~/k-research/papers/real-materials-3/figures'), exist_ok=True)
fig.savefig(os.path.expanduser('~/k-research/papers/real-materials-3/figures/alloys.png')); print('ok')
