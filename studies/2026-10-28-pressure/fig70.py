# Figure of #70: the cubic margin E(6H) - E(3C) + P (V(6H) - V(3C)) per atom pair against pressure, first order, for SiC, Si, Ge;
# dashed beyond each material's own transition (Si, Ge: beta-tin near 11 and 10 GPa); SiC's experimental 6H -> 3C above ~4.5 GPa marked.
import json, os, numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
d = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pressure.json')))
S = {'silicon carbide': ('SiC (GGA+vdW, Kawanishi-Mizoguchi)', '#2f6db0', None), 'silicon': ('Si (PBEsol, Keller et al.)', '#a9862a', 11.0), 'germanium': ('Ge (PBEsol, Keller et al.)', '#b0457a', 10.0)}
fig, ax = plt.subplots(figsize=(9, 5.2), dpi=200)
for s in ('top', 'right'): ax.spines[s].set_visible(False)
ax.set_axisbelow(True); ax.grid(axis='y', color='#e5e5e5'); ax.axhline(0, color='#888', lw=1)
P = np.linspace(0, 30, 301)
for name, (key, col, ptr) in S.items():
    e, v, _ = d[key]['margins']['3C vs 6H']
    y = e + v * P
    if ptr:
        m = P <= ptr; ax.plot(P[m], y[m], color=col, lw=2.2); ax.plot(P[~m], y[~m], color=col, lw=1.4, ls='--')
        ax.scatter([ptr], [e + v * ptr], color=col, s=30, zorder=3)
        ax.annotate(f'{name}: β-tin', (ptr, e + v * ptr), xytext=(6, 6), textcoords='offset points', fontsize=8.5, color='#1a1a1a')
    else:
        ax.plot(P, y, color=col, lw=2.2)
    ax.annotate(name, (30, e + v * 30), xytext=(4, 0), textcoords='offset points', va='center', fontsize=9.5, color='#1a1a1a')
ax.axvline(4.5, color='#2f6db0', lw=0.8, ls=':'); ax.text(4.7, ax.get_ylim()[1] * 0.92, 'SiC: 6H → 3C observed above ~4.5 GPa', fontsize=8.5, color='#2f6db0')
ax.set_xlabel('pressure (GPa)', fontsize=10); ax.set_ylabel('margin of cubic 3C over 6H (meV per atom pair)', fontsize=10)
ax.set_title('The volume term under pressure, first order: SiC gains, Si and Ge lose margin', fontsize=10, loc='left')
ax.set_xlim(0, 36)
fig.text(0.98, 0.01, 'DICTO', color='#b8962e', fontsize=12, ha='right', family='serif', weight='bold')
out = os.path.expanduser('~/kres-tmp/fig70'); os.makedirs(out, exist_ok=True)
fig.savefig(os.path.join(out, 'pressure-margins.png'), bbox_inches='tight', facecolor='white'); print('ok')
