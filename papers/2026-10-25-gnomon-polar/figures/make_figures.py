# Figure 1 of the gnomon-polar draft: the twelve stations of the golden cycle as multiples of I (log scale), the clean stations and the
# four clean gnomons marked. Values from checks.py / gnomon-all12.txt (exact; decimals for plotting only).
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
p = (1 + 5 ** .5) / 2; s5 = 5 ** .5
names = ['I', 'Cleo\nstar', 'D′', 'ID', 'OG', 'rTI', 'TI', 'H', 'jtI', 'RT', 'M', 'I·φ³']
v = [1, 2, 20/9 + 44/45*s5, 57/8 + 127/40*s5, 645/76 + 287/76*s5, 183/8 + 39/40*s5, 24 + 3/5*s5, 87 - 132/5*s5, 3321/38 - 999/38*s5, 243/2 - 81/2*s5, 47/2 + 21/2*s5, 38 + 17*s5]
clean_st = {0: '1', 1: '2', 9: '81/φ²', 10: 'φ⁸', 11: 'φ⁹'}
clean_g = {1: '+ I', 6: '+ (3/4)φ⁻² I', 7: '+ 18φ⁻⁴ I', 11: '+ φ⁷ I'}
gold, grey, ink = '#b8862e', '#9a9a9a', '#2b2620'
fig, ax = plt.subplots(figsize=(9.2, 4.6), dpi=200)
xs = range(12)
for i in range(1, 12):
    c = gold if i in clean_g else grey
    ax.plot([i - 1, i], [v[i - 1], v[i]], color=c, lw=3.2 if i in clean_g else 1.4, solid_capstyle='round', zorder=1)
    if i in clean_g:
        px, py, ha = {1: (0.35, 2.3, 'right'), 6: (5.5, 36, 'center'), 7: (6.75, 38, 'center'), 11: (10.45, 72, 'right')}[i]
        ax.text(px, py, clean_g[i], color=gold, fontsize=9, ha=ha, va='center', fontweight='bold')
for i in xs:
    ax.scatter([i], [v[i]], s=46 if i in clean_st else 26, color=gold if i in clean_st else 'white', edgecolor=ink, lw=1.0, zorder=3)
    lab = f'{v[i]:.2f}' if i not in clean_st else clean_st[i]
    ax.text(i, v[i] / 1.32, lab, ha='center', va='top', fontsize=7.6, color=ink if i in clean_st else '#5a554d', fontweight='bold' if i in clean_st else 'normal')
ax.set_yscale('log'); ax.set_ylim(0.55, 140); ax.set_xlim(-0.5, 11.6)
ax.set_xticks(list(xs)); ax.set_xticklabels(names, fontsize=8.6)
ax.set_ylabel('volume / volume of I (log scale)', fontsize=9)
for s in ('top', 'right'): ax.spines[s].set_visible(False)
ax.tick_params(axis='y', labelsize=8)
ax.text(0.0, 1.04, 'One turn of the twelve-station golden cycle: what each step adds', transform=ax.transAxes, fontsize=10.5, color=ink, fontweight='bold')
ax.text(1.0, -0.2, 'DICTO · dictospheres.com', transform=ax.transAxes, ha='right', fontsize=7.5, color='#777')
ax.text(0.0, -0.2, 'gold: exact landmarks (dots) and steps whose gnomon is a rational multiple of φᵏ·I (thick)', transform=ax.transAxes, fontsize=7.5, color='#555')
fig.tight_layout(); fig.savefig('fig1-gnomon-ladder.png'); print('saved')
