# Figure of #68: volume per pair relative to the cubic stacking (%) against the hexagonality, with the straight line through the
# two pure stackings (the Hexagonality Law's ideal form). SiC GGA(vdW) (Kawanishi and Mizoguchi), Si and Ge PBEsol (Keller et al.).
import numpy as np, os
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
S = {'silicon carbide (GGA+vdW)': ('#2f6db0', 'o', {0: 7.542/3*3.079**2, 1/3: 15.113/6*3.077**2, .4: 37.800/15*3.076**2, .5: 10.085/4*3.076**2, 1: 5.059/2*3.074**2}),
     'silicon (PBEsol)': ('#a9862a', 's', {0: 40.152, 1/3: 40.106, .5: 40.095, 1: 40.109}),
     'germanium (PBEsol)': ('#b0457a', '^', {0: 45.596, 1/3: 45.535, .5: 45.516, 1: 45.493})}
fig, ax = plt.subplots(figsize=(9, 5.4), dpi=200)
for s in ('top', 'right'): ax.spines[s].set_visible(False)
ax.set_axisbelow(True); ax.grid(axis='y', color='#e5e5e5')
for name, (col, mk, d) in S.items():
    h = np.array(sorted(d)); v = np.array([d[k] for k in h]); y = 100 * (v / d[0] - 1)
    ax.plot([0, 1], [0, y[-1]], color=col, lw=1.2, ls='--')
    ax.plot(h, y, color=col, lw=2, marker=mk, ms=7, mec='white', mew=1.5, label=name)
    ax.annotate(name, (1, y[-1]), xytext=(6, 0), textcoords='offset points', va='center', fontsize=9, color='#1a1a1a')
ax.set_xlabel('hexagonality h (share of hexagonal layers)', fontsize=10); ax.set_ylabel('volume per pair, change from cubic (%)', fontsize=10)
ax.set_title('Real polytypes against the straight line (dashed: the line through the two pure stackings)', fontsize=10, loc='left')
ax.set_xlim(-0.03, 1.36)
fig.text(0.98, 0.01, 'DICTO', color='#b8962e', fontsize=12, ha='right', family='serif', weight='bold')
out = os.path.expanduser('~/kres-tmp/fig68'); os.makedirs(out, exist_ok=True)
fig.savefig(os.path.join(out, 'real-polytypes.png'), bbox_inches='tight', facecolor='white'); print('ok')
