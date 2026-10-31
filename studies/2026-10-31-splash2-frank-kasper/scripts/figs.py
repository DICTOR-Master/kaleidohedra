# Splash figures for Splash Rules II, Frank-Kasper run (dicto-big-brother): python3 figs.py out/splash2_fk.json <figdir>
# Floats only for drawing; every plotted value is an exact rational from splash.py. Series differ by colour AND marker shape.
import sys, os, json
from fractions import Fraction as Fr
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
D = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = plt.imread(next(p for p in (os.path.join(HERE, 'dicto-logo.png'), os.path.expanduser('~/kres-tmp/dicto-logo.png'), os.path.expanduser('~/k-research/papers/dicto-logo.png')) if os.path.exists(p)))
GOLD, INK, GREY, BLUE, RED = '#b8962e', '#222222', '#8a8a8a', '#2f5d8a', '#a8402e'
plt.rcParams.update({'font.size': 8, 'axes.linewidth': 1.0, 'font.family': 'DejaVu Sans', 'axes.edgecolor': '#555555'})
def mark(fig):
    fig.add_artist(AnnotationBbox(OffsetImage(LOGO, zoom=24 / LOGO.shape[0]), (0.995, 0.005), xycoords='figure fraction', box_alignment=(1, 0), frameon=False))
    fig.text(0.955, 0.012, 'DICTO · dictospheres.com', ha='right', va='bottom', fontsize=6.5, color='#8a6d1c')
def style(ax):
    ax.grid(True, color='#e6e6e6', linewidth=0.6, zorder=0); ax.tick_params(length=3, width=0.8)
    for s in ('top', 'right'): ax.spines[s].set_visible(False)
F = lambda s: float(Fr(s))
FK = [r for r in D['structures'] if r['ok']]
def per(r, k): return Fr(r['census'].get(k, 0), r['census']['N'])
fam = {'st': [r for r in FK if r['kind'] == 'st'], 'fk59': [r for r in FK if r['kind'] == 'fk59'], 'cif': [r for r in FK if r['kind'] == 'cif']}
tab = D['table']; known = [t for t in tab if not t['name'].startswith('hyp')]; hyp = [t for t in tab if t['name'].startswith('hyp')]
def x12t(t): return Fr(t['counts'][0], sum(t['counts']))
def plot_sets(ax, fx, fy, tx=None, ty=None, label=True):
    ax.scatter([fx(r) for r in fam['st']], [fy(r) for r in fam['st']], s=12, marker='o', color=BLUE, alpha=0.6, linewidths=0, label='square-triangle rows (62)' if label else None, zorder=3)
    ax.scatter([fx(r) for r in fam['fk59']], [fy(r) for r in fam['fk59']], s=14, marker='^', color=GOLD, alpha=0.7, linewidths=0, label='kagome slabs, FK 1959 (119)' if label else None, zorder=3)
    if tx:
        ax.scatter([tx(t) for t in known], [ty(t) for t in known], s=22, marker='D', facecolors='white', edgecolors=GREY, linewidths=1.0, label='known, counts from Deza et al. (13)' if label else None, zorder=4)
        ax.scatter([tx(t) for t in hyp if F(t['a0']) != 0], [ty(t) for t in hyp if F(t['a0']) != 0], s=34, marker='X', color=RED, linewidths=0.4, edgecolors='white', label='hypothetical, off the law (3)' if label else None, zorder=6)
    ax.scatter([fx(r) for r in fam['cif']], [fy(r) for r in fam['cif']], s=30, marker='s', color=INK, edgecolors='white', linewidths=0.8, label='real phases, computed here (18)' if label else None, zorder=5)

fig, axs = plt.subplots(2, 2, figsize=(7.4, 6.2), dpi=220)
# (a) Zbar against x12: the Yarmolyuk-Kripyakevich line
a = axs[0, 0]; style(a)
plot_sets(a, lambda r: F(r['x']['12']), lambda r: F(r['Zbar']), lambda t: float(x12t(t)), lambda t: F(t['Zbar']))
xs = [0.2, 0.72]; a.plot(xs, [68 / 5 - 2 / 5 * x for x in xs], color=INK, lw=1.0, zorder=2)
for r in fam['cif']:
    nm = r['meta']['name']
    if nm in ('A15', 'C15', 'Z', 'sigma', 'mu', 'R', 'T (Bergman)', 'nu'):
        dx, dy, ha = {'A15': (0.012, 0.0, 'left'), 'C15': (-0.012, -0.012, 'right'), 'Z': (0.012, 0.004, 'left'), 'sigma': (0.012, 0.004, 'left'),
                      'mu': (0.012, 0.005, 'left'), 'R': (-0.012, -0.012, 'right'), 'T (Bergman)': (0.012, 0.004, 'left'), 'nu': (-0.012, -0.012, 'right')}[nm]
        a.text(F(r['x']['12']) + dx, F(r['Zbar']) + dy, {'T (Bergman)': 'T', 'sigma': 'σ', 'mu': 'μ', 'nu': 'ν'}.get(nm, nm), fontsize=7, ha=ha, color=INK, zorder=7)
a.text(0.43, 13.535, 'Z̄ = 68/5 − (2/5)·x₁₂', fontsize=7.5, color=INK)
a.set_xlabel('share of icosahedral sites x₁₂'); a.set_ylabel('mean coordination Z̄'); a.set_title('(a) Z̄ is a straight line in x₁₂ (YK 1974)', fontsize=8.5, loc='left')
a.legend(fontsize=6, loc='lower left', frameon=False)
# (b) the YK defect: Zbar minus the line, against a0
a = axs[0, 1]; style(a)
res = lambda z, x: z - (Fr(68, 5) - Fr(2, 5) * x)
plot_sets(a, lambda r: F(r['a0']), lambda r: float(res(Fr(r['Zbar']), Fr(r['x']['12']))), lambda t: F(t['a0']), lambda t: float(res(Fr(t['Zbar']), x12t(t))), label=False)
xs = [-0.085, 0.01]; a.plot(xs, [-6 / 5 * x for x in xs], color=INK, lw=1.0, zorder=2)
for t in hyp:
    if F(t['a0']) != 0:
        lab_ = ':'.join(map(str, t['counts'])); off = {'7:4:2:2': (-0.003, 0.006, 'right'), '6:6:4:0': (0.004, -0.008, 'left')}.get(lab_, (0.003, -0.004, 'left'))
        a.text(F(t['a0']) + off[0], float(res(Fr(t['Zbar']), x12t(t))) + off[1], lab_, fontsize=6.5, color=RED, ha=off[2])
a.text(-0.083, 0.003, 'Z̄ − line = −(6/5)·a₀', fontsize=7.5)
a.set_xlabel('YK defect a₀ = x₁₂ − x₁₄/3 − 7x₁₅/6 − 2x₁₆'); a.set_ylabel('Z̄ − (68/5 − 2x₁₂/5)'); a.set_title('(b) off the line only through the YK defect', fontsize=8.5, loc='left')
# (c) per-slab counts in the kagome family against the share z of Z slabs: lines
a = axs[1, 0]; style(a)
K = fam['fk59']
zsh = lambda r: r['meta']['cellword'].count('0') / len(r['meta']['cellword'])
for key, col, mk, lab in (('N12', BLUE, 'o', 'Z12 sites  4 − z'), ('N16', GOLD, '^', 'Z16 sites  2 − 2z'), ('N14', INK, 's', 'Z14 = Z15 sites  2z'), ('bond6', RED, 'D', '6-bonds  4 + z')):
    a.scatter([zsh(r) for r in K], [r['census'].get(key, 0) / r['meta']['units'] for r in K], s=12, marker=mk, color=col, alpha=0.75, linewidths=0, label=lab, zorder=3)
a.set_xlabel('share z of Z slabs (letter 0)'); a.set_ylabel('count per kagome slab'); a.set_title('(c) kagome family: site counts are lines (window 1)', fontsize=8.5, loc='left')
a.legend(fontsize=6.3, frameon=False, loc='upper left', ncol=2); a.set_ylim(-0.2, 6.4)
# (d) interface counts need the pair share: Z16-Z16 6-bonds and 2266 tetrahedra
a = axs[1, 1]; style(a)
def p00(r):
    w = r['meta']['cellword']; n = len(w); return sum(1 for k in range(n) if w[k] == '0' and w[(k + 1) % n] == '0') / n
y = lambda r: r['census'].get('bond6_16_16', 0) / r['meta']['units']
a.scatter([4 - 5 * zsh(r) for r in K], [y(r) for r in K], s=12, marker='^', color=GOLD, alpha=0.4, linewidths=0, label='against the line 4 − 5z: band', zorder=3)
a.scatter([4 - 5 * zsh(r) + p00(r) for r in K], [y(r) for r in K], s=14, marker='o', facecolors='none', edgecolors=INK, linewidths=0.8, label='against 4 − 5z + p₀₀: exact', zorder=4)
a.plot([0, 4.1], [0, 4.1], color=INK, lw=0.8, zorder=2)
a.set_xlabel('prediction'); a.set_ylabel('Z16–Z16 6-bonds per slab'); a.set_title('(d) interface counts need pairs (window 2)', fontsize=8.5, loc='left')
a.legend(fontsize=6.3, frameon=False, loc='upper left')
fig.tight_layout(rect=(0, 0.03, 1, 1)); mark(fig)
fig.savefig(os.path.join(out, 'splash2-fk.png')); plt.close(fig)

# Figure 2: topological identities, all TCP structures: one number (Zbar or the 6-bond density) fixes them
fig, axs = plt.subplots(1, 2, figsize=(7.4, 3.0), dpi=220)
a = axs[0]; style(a)
a.scatter([F(r['Zbar']) for r in FK if r['kind'] != 'cif'], [float(per(r, 'T')) for r in FK if r['kind'] != 'cif'], s=10, marker='o', color=BLUE, alpha=0.6, linewidths=0, label='layered families (181)', zorder=3)
a.scatter([F(r['Zbar']) for r in fam['cif']], [float(per(r, 'T')) for r in fam['cif']], s=26, marker='s', color=INK, edgecolors='white', linewidths=0.8, label='real phases (18)', zorder=4)
a.plot([13.32, 13.51], [13.32 / 2 - 1, 13.51 / 2 - 1], color=INK, lw=0.8, zorder=2)
a.text(13.508, 5.668, 'tetrahedra per atom = Z̄/2 − 1\n6-bonds per atom = that − 5', fontsize=7, ha='right'); a.set_xticks([13.35, 13.40, 13.45, 13.50])
a.set_xlabel('mean coordination Z̄'); a.set_ylabel('tetrahedra per atom'); a.set_title('(a) identity: a line in Z̄', fontsize=8.5, loc='left')
a.legend(fontsize=6.3, frameon=False, loc='upper left')
a = axs[1]; style(a)
a.scatter([F(r['x']['12']) for r in FK], [float(per(r, 'tet_j2')) for r in FK], s=10, marker='o', color=BLUE, alpha=0.6, linewidths=0, label='all TCP structures', zorder=3)
a.scatter([F(r['x']['12']) for r in fam['cif']], [float(per(r, 'tet_j2')) for r in fam['cif']], s=26, marker='s', color=INK, edgecolors='white', linewidths=0.8, label='real phases', zorder=4)
a.set_xlabel('share of icosahedral sites x₁₂'); a.set_ylabel('tetrahedra with two 6-edges, per atom'); a.set_title('(b) a count no single number fixes', fontsize=8.5, loc='left')
a.legend(fontsize=6.3, frameon=False)
fig.tight_layout(rect=(0, 0.05, 1, 1)); mark(fig)
fig.savefig(os.path.join(out, 'identities.png')); plt.close(fig)
print('figures written')
